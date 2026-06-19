<h1 align="center">
  Spec-Driven Development (SDD)
</h1>

## What this is

**Code consistency is the casualty of LLM agent velocity.** 

LLMs write code faster than any human can read it — and faster than the agent can stay coherent with itself. SDD keeps the spec small, dense, and durable. It's the part the agent re-reads every turn, so task ten is built against the same constraints as task one.

The mechanics:

- **Every row has an address.** `§V.<n>` / `§T.<n>` / `§B.<n>` are stable cites — code comments link to the invariant they uphold, tests reference the bug they guard, commits cite the task they close. `SPEC.md` survives `/clear` and team handoff.
- **Telegraph encoding cuts tokens about 40%** vs Claude prose for the same content (measured per-row mean 41%, median 39%, n=30 — see [`benchmarks/telegraph/`](benchmarks/telegraph/)). The savings come from terse grammar — dropped articles/filler, fragments, unpadded pipe tables — plus compact `§`-refs and a curated low-token symbol set (`→ ≥ ≤ ! ? § |`); Distinct from `steno` (the bundled human-facing shorthand).
- **Every test failure feeds back into the spec.** A `§B` row, usually a new `§V` invariant. The drift report stays trustworthy because every prior failure tightened the spec.
- **Main Claude does all the writes.** Code edits, `SPEC.md` mutations, status flips, commits. Read-only audits (e.g. `/sdd:check`) may fan out to sub-agents. No orchestrator. Same spec + same task produces the same plan.
- **Re-onboarding is one command.** Come back to the repo after a week, run `/sdd:check`. You get a read-only drift report: which `§V` invariants the code violates, which `§T` tasks remain. No digging through old transcripts.

> The spec is the only artifact that earns its tokens. Everything else must save more tokens later, save the agent's context, or get cut.

### SPEC.md is for the LLM, not you

`SPEC.md` is an LLM-facing artifact. You operate it through Claude — `/sdd:spec` writes, `/sdd:build` and `/sdd:check` read, `/sdd:explain` decodes a citation back to prose when you want to read along. The loop is `human → /sdd:* → Claude → SPEC.md`, not hand-editing in your editor.

That framing is load-bearing. Telegraphic fragments over full sentences, pipe tables over bulleted lists, dropped line citations — all optimized for the model that re-parses the spec every command, not the human skimming it. If you want to skim it as a human, `/sdd:explain` is the front door.

## Install

```bash
/plugin marketplace add kborovik/spec-driven-dev
```

```bash
/plugin install sdd@spec-driven-dev
```

Then in any repo:

```bash
/sdd:spec   # creates SPEC.md if missing
```

## The mental model

```
   ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐
   │/sdd:design │──►│ /sdd:spec  │──►│ /sdd:build │──►│ /sdd:check │
   │  propose   │   │  mutator   │   │ plan→exec  │   │ read-only  │
   └────────────┘   └─────▲──────┘   └─────┬──────┘   └─────┬──────┘
                          │                │                │
                          │                ▼ on failure     │ on drift
                          │          ┌────────────┐         │
                          │          │  backprop  │         │
                          │          │ §B (+ §V)  │         │
                          │          └─────┬──────┘         │
                          │                │                │
                          └────────────────┴────────────────┘
                                     amend SPEC.md
```

- **One spec file.** `SPEC.md`. No `docs/` tree, no JSON sidecars.
- **One writer.** `/sdd:spec`. (`/sdd:build` may flip a `.` to `x`; nothing else writes.)
- **Read-only commands write nothing.** `/sdd:check` (drift report) and `/sdd:explain` (decompression).

## SPEC.md format

Six fixed sections, fixed order. Each row is addressable as `§<S>.<n>`.

```markdown
# SPEC

## §G GOAL

one line. what code must do.

## §C CONSTRAINTS

- non-negotiable boundary
- tech / language / library locked in

## §I INTERFACES

external surface — what the world sees.

- cmd: `foo bar` → stdout JSON
- api: POST /x → 200 {id}
- file: `config.yaml` schema …
- env: `FOO_KEY` required

## §V INVARIANTS

numbered. testable. each ! MUST hold.
V<n>: every req → auth check before handler
V<n>: token expiry ≤ current_time → reject
V<n>: DB write ! in transaction

## §T TASKS

id|status|task|cites
T<n>|.|scaffold repo|-
T<n>|.|impl §I.api POST /x|V<n>
T<n>|x|add §V.<n> middleware|V<n>,I.api

## §B BUGS

id|date|cause|fix
B<n>|2026-04-20|token `<` not `≤`|V<n>
B<n>|2026-04-21|race on write|V<n>
```

**Status markers:** `.` todo · `x` done.
**Cell rules:** literal `|` becomes `\|`. Empty cell = `-`. Backticks OK.

## Commands

### `/sdd:design` — propose-then-critique

Use when there's a structural choice to weigh — tradeoffs, named alternatives, subsystem shape. The model proposes a shape, you critique, the loop converges only when `## Open Questions` is empty. Persists to `designs/<slug>.md`. `/sdd:spec` later folds the converged design into `§V` / `§T` rows; the draft file stays in the working tree for you to remove or keep.

```bash
/sdd:design how should the release pipeline split monorepo plugins?
```

Distinct from `/sdd:spec`'s socratic gate: socratic converges on **enough** (sharpen vague intent); design converges on **exhausted** (every structural question has a decision).

### `/sdd:spec` — mutate the spec

The sole mutator. The argument is **free-form intent** — the socratic gate (the bundled `socratic` skill) reads what you wrote and picks a mode. You don't pick the mode yourself.

| project state    | possible modes                                                         | gate behavior                                                                                                        |
| ---------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| no `SPEC.md`     | **NEW** or **DISTILL**                                                 | concrete intent passes in at most 1 turn; vague intent triggers single-question dialogue to convergence              |
| `SPEC.md` exists | **BACKPROP** or **AMEND** or **NEW** (rare, requires explicit re-init) | mode emerges from convergence triple — symptom + surface + recurrence-class for BACKPROP, §-target + delta for AMEND |

Examples (all free-form — the gate classifies):

```bash
/sdd:spec a CLI that ingests JSON over stdin and emits Parquet
/sdd:spec build the spec from this codebase
/sdd:spec V<n>'s `≤` should be `<` for unsigned tokens
/sdd:spec rate-limiter dropped requests under 100rps
```

### `/sdd:build` — plan, then execute

Plan, then execute, then verify loop. EXECUTE serializes on main thread; PLAN reads may delegate to sub-agents.

| arg form | scope                                      |
| -------- | ------------------------------------------ |
| `§T.n`   | implement that one task                    |
| `--next` | lowest-numbered row with status `.`        |
| `--all`  | every `.` row in §T order                  |
| (empty)  | same as `--next`                           |

Loop per task:

1. **PLAN** — cite every §V / §I the task touches, then proceed to EDIT. The plan is emitted inline for transparency, not a wait-state. Gaps are annotated so you can route them back to `/sdd:spec` post-hoc; the build never invents rules.
2. **EDIT** — make the change, run tests / build.
3. **VERIFY** — on failure, classify: (a) code bug, then fix and re-run; (b) spec wrong or unspecified edge case, then invoke `backprop` (via `/sdd:spec <cause>`), let it append `§B` and usually a new `§V`, resume against the updated spec.
4. **CLOSE** — flip `.` to `x` only when verification is green.

**Ambiguity is a spec defect, not a coding judgement.** `/sdd:build` never silently retries and never edits `SPEC.md` beyond flipping a status cell — every rule-shaped question routes back to `/sdd:spec`.

### `/sdd:check` — drift report

Read-only diagnostic. Diffs `SPEC.md` against the working tree. Always audits §V + §I + §T together.

| arg      | what it does                                                                       |
| -------- | ---------------------------------------------------------------------------------- |
| (empty)  | memo-driven sweep — re-audits §V rows touched since last clean run; rest HOLD-SINCE-CLEAN |
| `--full` | force full re-classify — deletes `.claude/check-state.json` upfront, rebuilds memo  |

Output groups violations by severity (`VIOLATE` / `RISK` / `STALE`) and suggests a remedy — usually `/sdd:spec <intent>` or `/sdd:build`. It never runs them itself.

### `/sdd:explain` — telegraph to prose

The inverse of `telegraph`. Given any citation, returns plain English with cited context.

```bash
/sdd:explain §V.<n>    # expand a specific invariant
/sdd:explain §T.<n>    # expand a task + every §V/§I it cites
/sdd:explain §B.<n>    # expand a bug + the invariant that catches recurrence
/sdd:explain --next    # expand the next unfinished task
```

Useful for code review, onboarding, or when you'd otherwise have to translate `every req → auth check before handler` in your head.

### `/sdd:condense` — token-budget sweep

Operator-triggered condenser for an oversized `SPEC.md` (advisory fires in `/sdd:check` when the estimate exceeds about 20k tokens). Six prongs — fold sibling invariants, mark superseded tasks, archive old §T/§B rows to `SPEC.archive.md`, prune inlined history, rewrite prose to telegraph, extract heavy audit recipes. Single atomic commit, rollback via `git revert`.

### `/sdd:reorganize` — §V cluster + renumber

Operator-triggered clarity pass (at most once per major epoch): clusters §V invariants by topic, renumbers them, and sweeps every citation in the same commit. Renumber history persists to `.claude/spec-renumber-map.json` so old citations still resolve via `/sdd:explain`.

## Skills

Each skill dir surfaces directly as a slash command (e.g. `skills/spec/` becomes `/sdd:spec`). SKILL.md frontmatter (`description`, `allowed-tools`, `model`) is honored on dispatch.

| skill        | role                                                                   |
| ------------ | ---------------------------------------------------------------------- |
| `design`     | propose-then-critique writes `designs/<slug>.md`                       |
| `spec`       | sole mutator                                                           |
| `build`      | plan, then execute loop                                                |
| `check`      | drift report                                                           |
| `explain`    | telegraph to prose decoder                                             |
| `condense`   | token-budget condensation sweep                                        |
| `reorganize` | §V cluster + renumber + cite sweep                                     |
| `telegraph`  | telegraph encoder (about 40% reduction vs prose); auto-fires on writes |
| `backprop`   | bug to spec protocol; fires on non-code-bug verification failures      |
| `socratic`   | single-question intent gate; invoked by `/sdd:spec`                    |
| `steno`      | human-facing terse-prose register for reviewer-read text               |

You don't usually invoke `telegraph`, `backprop`, `socratic`, or `steno` directly — Claude picks them up from the command flow. `backprop`, for example, fires automatically when a `/sdd:build` verification failure smells like under-specification (clear code bugs are just fixed).

## Workflows

### Greenfield — new project

```bash
/sdd:design how should we shape the parser / renderer split?   # optional — only if structural Qs
/sdd:spec build a static-site generator that converts a Markdown directory into a single-page HTML bundle
# review §G/§C/§I/§V in SPEC.md, amend if needed
/sdd:build --next   # plan, implement, verify T<n> (scaffold)
/sdd:build --next   # T<n> (renderer)
/sdd:check          # before opening a PR
```

### Brownfield — existing repo

```bash
/sdd:spec build the spec from this codebase   # gate routes to DISTILL
/sdd:check                     # see what already drifts from the distilled spec
/sdd:spec V<n>'s bound is too loose for the rate-limiter   # gate routes to AMEND
/sdd:build §T.<n>              # tackle a specific task
```

### A bug just hit production

```bash
/sdd:spec webhook handler retried POSTs after 5xx, double-charged 11 customers
# gate routes to BACKPROP: appends §B, adds §V "POST handler ! idempotent on retry",
# adds a §T fix task, commits SPEC.md
/sdd:build --next              # failing test first, then the fix; commit cites the new §B/§V
/sdd:check                     # confirm new §V is now upheld
```

### Pre-merge sanity

```bash
/sdd:check
/sdd:explain §V.<n>            # if a violation is unclear, decompress it
```

## Telegraph encoding

`telegraph` writes telegraphic grammar — dropped articles, aux verbs, and filler, fragments, compact pipe tables — with a curated low-token symbol set (`→ ≥ ≤ ! ? §`). Anything heavier is written as the ASCII word: a multi-token math operator costs 2–4 tokens vs a 1-token word, so a symbol earns its place only where it reads clearer than the word.

Result: every spec write lands about 40% leaner in tokens than the equivalent prose while staying machine- and human-readable. The measured per-row mean is 41% (median 39%, n=30 across §V/§T/§B rows of this repo's own `SPEC.md`), reproducible via [`benchmarks/telegraph/telegraph-bench.py`](benchmarks/telegraph/telegraph-bench.py) — **full methodology, per-row results, and caveats in the [benchmark write-up](benchmarks/telegraph/README.md)**. `steno` (bundled) handles reviewer-facing text and keeps grammar intact so reviewers don't slow down.

Rules:

- Drop articles (a/an/the). Drop filler. Drop aux verbs where a fragment works.
- Short synonyms (`fix` over `implement`).
- **Preserve verbatim:** code, paths, identifiers, URLs, numbers, error strings, SQL, regex.

Full symbol table: `skills/telegraph/SKILL.md` SYMBOLS section.

**Example.** Prose: "The authentication middleware must verify the token expiry on every request before allowing the handler to execute."
Telegraph: `V<n>: every req → auth check before handler`

If telegraph encoding slows you down on review, `/sdd:explain §V.<n>` decompresses on demand.

## Backprop in detail

Backprop is the one non-obvious thing SDD does that vanilla plan-then-execute doesn't. Six steps:

1. **Capture** — record the failing case verbatim (test name, error, stack, repro).
2. **Trace** — find the cause: code bug, spec wrong, or unspecified edge case.
3. **Append §B** — add a row: `id|date|cause|fix`. Telegraph-encoded.
4. **Decide on §V** — would an invariant have caught the _class_ of this bug? If yes, add or tighten one. Cite it from the new §B row.
5. **Write the failing test first** — in the `/sdd:build` resume: watch it fail, then ship the fix. The test stays as a permanent guard.
6. **Two commits, cross-cited** — the spec commit lands first (§B + §V, via `/sdd:spec`); the code commit (test + fix) follows via `/sdd:build` and cites them. The record survives even when the fix is deferred.

Triggers:

- Test/build fails inside `/sdd:build` verification.
- `/sdd:check` reports a `VIOLATE` whose root cause is identified.
- User: `/sdd:spec <description>` — post-mortems, prod incidents, user reports; gate routes to BACKPROP on bug-class intent.

## FAQ

**Why Markdown, not YAML / JSON?** Markdown + pipe tables grep cleanly, diff cleanly, render in every PR tool, and don't trip on quoting. JSON specs invite tooling that defeats the point — the spec is for humans and one LLM, not a build system.

**Why one file?** Sub-1000-line specs fit in context cheaply. Multi-file specs invite cross-file inconsistency and force `grep` ceremony. When the spec outgrows its budget (about 20k tokens — `/sdd:check` raises an advisory), `/sdd:condense` folds, trims, and archives old `§T`/`§B` rows to `SPEC.archive.md` instead of splitting.

**Does `/sdd:build` always backprop on failure?** Only on failures that aren't clear code bugs. Typos and wrong loop bounds get fixed without a spec change. Anything that smells like under-specification routes through `backprop`.

**Can I skip telegraph encoding and write prose specs?** Yes, but every future load of the spec into context pays about 1.7x the tokens for the same content (the measured about 40% cut, inverted). Optional in syntax, expensive in practice.

## Files

```
.claude-plugin/plugin.json       plugin manifest (name: sdd)
.claude-plugin/marketplace.json  marketplace manifest for direct install
skills/design/                   /sdd:design — propose-then-critique design loop to designs/<slug>.md
skills/spec/                     /sdd:spec — sole SPEC.md mutator
skills/build/                    /sdd:build — plan-execute loop
skills/check/                    /sdd:check — read-only drift report
skills/explain/                  /sdd:explain — telegraph to prose decoder
skills/condense/                 /sdd:condense — token-budget condensation sweep
skills/reorganize/               /sdd:reorganize — §V cluster + renumber + cite-DAG sweep
skills/telegraph/                auto-fire telegraph encoder for SPEC-adjacent writes
skills/backprop/                 auto-fire bug to spec protocol on /sdd:build verify-fail
skills/socratic/                 intent-sharpening gate invoked by /sdd:spec
skills/steno/                    human-facing terse-prose register
scripts/check-mechanical.py      deterministic audit core used by /sdd:check
benchmarks/telegraph/            telegraph token-reduction benchmark — bench script + results JSON + README write-up
SPEC-FORMAT.md                   structural format contract for every SPEC.md
```

## Attribution and license

SDD is adapted from [**JuliusBrussee/cavekit**](https://github.com/JuliusBrussee/cavekit) (v4.0.0, MIT-licensed). For the original project, history, and `v3.1.0` (full Hunt lifecycle with sub-agents, parallel workers, and design-system enforcement), see the upstream repo.

MIT. See [`LICENSE`](LICENSE).
