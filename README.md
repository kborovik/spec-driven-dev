<h1 align="center">
  Spec-Driven Development (SDD)
</h1>

## What this is

SDD is a Claude Code plugin that stores a project's rules in one file, `SPEC.md`.
Use it so each later task follows the same rules as the first, including after you clear the chat or hand the repo to someone else.
An LLM can write code faster than it can stay consistent with its own earlier decisions.
`SPEC.md` is the text the agent re-reads on every command, so those rules stay in context.

What that gives you:

- **A stable address for every row.**
  Code comments, tests, and commits can point at `§V.<n>`, `§T.<n>`, or `§B.<n>`.
- **A short spec.**
  Telegraph, the grammar in `SPEC.md`, uses about 40% fewer tokens than the same content in Claude prose.
  The measurement is under [Telegraph encoding](#telegraph-encoding).
- **A stricter spec after a real failure.**
  A missing rule becomes a `§B` row and usually a new `§V` invariant.
- **One writer.**
  The main Claude session edits code, edits `SPEC.md`, flips task status, and commits.
  Sub-agents may read.
  They do not edit files.
  The same spec and the same task produce the same plan.
- **A drift report after time away.**
  `/sdd:check` lists broken `§V` invariants and open `§T` tasks.

> The spec is the one file whose token cost is always justified.
> Any other text must save tokens later, save context, or be removed.

### Who reads SPEC.md

`SPEC.md` is written for the LLM.
`/sdd:spec` writes it.
`/sdd:build` and `/sdd:check` read it.
`/sdd:explain` turns one citation back into plain sentences when you want to read a row.

The format follows from that reader.
Rows are short fragments.
Tables use pipes.
The model re-reads the file on every command, so the format favors short tokens over full sentences.

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

## How the commands connect

```
   ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐
   │/sdd:design │──►│ /sdd:spec  │──►│ /sdd:build │──►│ /sdd:check │
   │  propose   │   │   writes   │   │ plan, edit │   │ read-only  │
   └────────────┘   └─────▲──────┘   └─────┬──────┘   └─────┬──────┘
                          │                │                │
                          │                ▼ on failure     │ on drift
                          │          ┌────────────┐         │
                          │          │  backprop  │         │
                          │          │ §B and §V  │         │
                          │          └─────┬──────┘         │
                          │                │                │
                          └────────────────┴────────────────┘
                                     amend SPEC.md
```

- **One spec file.**
  The spec is `SPEC.md` at the repo root.
- **One writer.**
  `/sdd:spec` writes the spec.
  `/sdd:build` may change a `.` to `x`.
  Those are the only writes.
- **Read-only commands write nothing.**
  `/sdd:check` reports drift.
  `/sdd:explain` turns a citation into prose.

## SPEC.md format

The file has six sections, in a fixed order.
Each row is addressed as `§<S>.<n>`.

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

Status `.` means todo.
Status `x` means done.
A literal `|` inside a cell is written `\|`.
An empty cell is `-`.
Backticks are allowed.

## Commands

### `/sdd:design`

`/sdd:design` is for a structural choice: tradeoffs, named alternatives, or how a subsystem should be shaped.
The model proposes a shape.
You critique it.
The loop stops when `## Open Questions` is empty.
The result is saved to `designs/<slug>.md`.
`/sdd:spec` later copies the decisions into `§V` and `§T` rows.
The draft file stays in the working tree until you remove it or keep it.

```bash
/sdd:design how should the release pipeline split monorepo plugins?
```

`/sdd:design` stops when every structural question has a decision.
`/sdd:spec` stops when the intent is specific enough to write or change the spec.

### `/sdd:spec`

`/sdd:spec` is the only command that edits `SPEC.md`, aside from a status flip in `/sdd:build`.
You pass free-form intent.
The `socratic` skill reads what you wrote and picks the mode.

With no `SPEC.md`, the mode is **NEW** or **DISTILL**.
A concrete intent finishes in at most one turn.
A vague intent gets one question at a time until the intent is specific.

With an existing `SPEC.md`, the mode is **BACKPROP**, **AMEND**, or rarely **NEW**.
**NEW** on an existing spec needs an explicit request to start over.
**BACKPROP** needs the symptom, where it showed up, and the class of bug that would recur.
**AMEND** needs the target row and the change.

```bash
/sdd:spec a CLI that ingests JSON over stdin and emits Parquet
/sdd:spec build the spec from this codebase
/sdd:spec V<n>'s `≤` should be `<` for unsigned tokens
/sdd:spec rate-limiter dropped requests under 100rps
```

### `/sdd:build`

`/sdd:build` plans a task, edits the code, then verifies the result.
Edits run on the main session.
Planning reads may use sub-agents.

- `§T.<n>` implements that task.
- `--next` implements the lowest-numbered row with status `.`.
- `--all` implements every `.` row in `§T` order.
- An empty argument does the same thing as `--next`.

Each task runs four steps:

1. **PLAN.**
   Cite every `§V` and `§I` row the task touches, then edit.
   The plan is printed in the same turn so you can read it.
   A gap is marked so you can send it to `/sdd:spec` afterward.
   The build leaves rule-making to `/sdd:spec`.
2. **EDIT.**
   Make the change.
   Run tests or the build.
3. **VERIFY.**
   On failure, classify the cause.
   A code bug is fixed and the check is run again.
   A wrong spec, or an edge case the spec never stated, goes to `backprop` through `/sdd:spec <cause>`.
   That appends a `§B` row and usually a new `§V` row.
   The build resumes against the updated spec.
4. **CLOSE.**
   Change `.` to `x` only after verification passes.

An unclear rule is a defect in the spec.
A failed check is classified before it is run again.
`/sdd:build` edits `SPEC.md` only to flip a status cell.
A question about a rule goes back to `/sdd:spec`.

### `/sdd:check`

`/sdd:check` is a read-only drift report.
It compares `SPEC.md` with the working tree.
It always audits `§V`, `§I`, and `§T` together.

- An empty argument re-checks `§V` rows touched since the last clean run.
  Untouched rows stay marked `HOLD-SINCE-CLEAN`.
- `--full` deletes `.spec/check-state.json` first and classifies every row again.

Violations are grouped as `VIOLATE`, `RISK`, or `STALE`.
The report names a next command, usually `/sdd:spec <intent>` or `/sdd:build`.
It never runs that command.

### `/sdd:explain`

`/sdd:explain` turns a telegraph citation into plain English, with the rows it cites.

```bash
/sdd:explain §V.<n>    # one invariant
/sdd:explain §T.<n>    # one task plus every §V and §I it cites
/sdd:explain §B.<n>    # one bug plus the invariant that catches a repeat
/sdd:explain --next    # the next unfinished task
```

Use it in review or onboarding when a row such as `every req → auth check before handler` is hard to read.

### `/sdd:condense`

`/sdd:condense` shrinks an oversized `SPEC.md`.
`/sdd:check` suggests it when the estimate passes about 20k tokens.
One commit applies six edits:

- Fold sibling invariants.
- Mark superseded tasks.
- Archive old `§T` and `§B` rows to `SPEC.archive.md`.
- Remove inlined history.
- Rewrite prose into telegraph.
- Move long audit recipes out of the spec.

Roll back with `git revert`.

### `/sdd:reorganize`

`/sdd:reorganize` is a clarity pass, at most once per major revision of the spec.
It groups `§V` invariants by topic, renumbers them, and updates every citation in the same commit.
Old numbers still resolve through `/sdd:explain`.
The map is `.spec/spec-renumber-map.json`.

## Workflows

### New project

```bash
/sdd:design how should we shape the parser / renderer split?   # optional; structural questions only
/sdd:spec build a static-site generator that converts a Markdown directory into a single-page HTML bundle
# review §G §C §I §V in SPEC.md, then amend if needed
/sdd:build --next   # plan, implement, and verify the scaffold task
/sdd:build --next   # renderer task
/sdd:check          # before opening a pull request
```

### Existing repo

```bash
/sdd:spec build the spec from this codebase   # picks DISTILL
/sdd:check                                    # what already drifts from the distilled spec
/sdd:spec V<n>'s bound is too loose for the rate-limiter   # picks AMEND
/sdd:build §T.<n>                             # one task
```

### A bug in production

```bash
/sdd:spec webhook handler retried POSTs after 5xx, double-charged 11 customers
# picks BACKPROP: appends §B, adds §V "POST handler ! idempotent on retry",
# adds a §T fix task, commits SPEC.md
/sdd:build --next              # failing test first, then the fix; the commit cites the new §B and §V
/sdd:check                     # confirm the new §V holds
```

### Before merge

```bash
/sdd:check
/sdd:explain §V.<n>            # when a violation is unclear
```

## Telegraph encoding

Telegraph is the short grammar `SPEC.md` is written in.
Articles, filler, and auxiliary verbs are dropped.
Tables stay compact.
The symbol set kept in the spec is `→ ≥ ≤ ! ? §`.
A heavier sign is written as a word.
Code, paths, identifiers, URLs, numbers, and error strings stay verbatim.
The full symbol table is the SYMBOLS section of `skills/telegraph/SKILL.md`.

The encoded form uses about 40% fewer tokens than the same content in prose.
The measured per-row mean is 41% (median 39%, n=30) on this repo's own `SPEC.md`.
Reproduce it with [`benchmarks/telegraph/telegraph-bench.py`](benchmarks/telegraph/telegraph-bench.py).
Methodology, per-row results, and caveats are in the [benchmark write-up](benchmarks/telegraph/README.md).

Prose: "The authentication middleware must verify the token expiry on every request before the handler runs."
Telegraph: `V<n>: every req → auth check before handler`

When a row is hard to read, `/sdd:explain §V.<n>` expands it.
Text for a human reviewer uses `steno`, which keeps normal grammar.

## Backprop

Backprop records a failure as a spec rule so the same class of bug is caught next time.
`/sdd:spec` appends a `§B` row and usually a new `§V` row.
That commit lands first.
`/sdd:build` then writes the failing test, applies the fix, and cites those rows.
The spec record remains even if the code fix waits.
A clear code bug is fixed in place.

Backprop runs when:

- A `/sdd:build` failure comes from a missing or wrong rule.
- `/sdd:check` reports `VIOLATE` and the cause is known.
- You pass `/sdd:spec` a bug report, a production incident, or a user report.
  The classifier picks **BACKPROP** for that kind of intent.

## FAQ

**Why Markdown?**
Markdown and pipe tables diff cleanly, render in pull-request tools, and avoid quoting issues.
The spec is for a person and one LLM.
It does not need a build system.

**Why one file?**
A spec under about 1000 lines fits in context at low cost.
One file keeps the rules from drifting apart across files.
When the spec passes about 20k tokens, `/sdd:check` raises an advisory.
`/sdd:condense` then archives old `§T` and `§B` rows to `SPEC.archive.md`.

**When does `/sdd:build` update the spec after a failure?**
A clear code bug is fixed in place.
A missing or wrong rule goes through `backprop`.

**Can the spec be prose instead of telegraph?**
Yes.
Each later read then uses about 1.7 times the tokens for the same content.
That is the measured cut of about 40%, inverted.

## Files

`telegraph`, `backprop`, `socratic`, and `steno` run from the commands above.
Each directory under `skills/` is one slash command.
`skills/spec/` is `/sdd:spec`.

```
.claude-plugin/plugin.json       plugin manifest (name: sdd)
.claude-plugin/marketplace.json  marketplace manifest for direct install
skills/design/                   /sdd:design — propose, then critique, then designs/<slug>.md
skills/spec/                     /sdd:spec — the only SPEC.md writer
skills/build/                    /sdd:build — plan, then execute
skills/check/                    /sdd:check — read-only drift report
skills/explain/                  /sdd:explain — telegraph to prose
skills/condense/                 /sdd:condense — token-budget shrink
skills/reorganize/               /sdd:reorganize — group §V, renumber, update citations
skills/telegraph/                short-grammar encoder; runs on spec writes
skills/backprop/                 bug-to-spec protocol; runs from /sdd:build on a spec failure
skills/socratic/                 one question to sharpen intent; called by /sdd:spec
skills/steno/                    short prose for text a human reviews
scripts/check-mechanical.py      deterministic checks used by /sdd:check
benchmarks/telegraph/            token-reduction benchmark, results, and write-up
SPEC-FORMAT.md                   format contract for every SPEC.md
```

## Attribution and license

SDD is adapted from [**JuliusBrussee/cavekit**](https://github.com/JuliusBrussee/cavekit) (v4.0.0, MIT).
The upstream repo has the original project, its history, and `v3.1.0` (the full Hunt lifecycle, with sub-agents, parallel workers, and design-system enforcement).

MIT.
See [`LICENSE`](LICENSE).
