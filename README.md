<h1 align="center">
  Spec-Driven Development (SDD)
</h1>

## Introduction

**SDD** is a **Claude Code plugin** that stores a project's rules in one file, `SPEC.md`.
Compression keeps that file small enough to stay in context.

- **Compression.**
  Telegraph, the grammar in `SPEC.md`, uses about 40% fewer tokens than the same content in prose.
  The measurement is under [Telegraph encoding](#telegraph-encoding).
- **Always in context.**
  `SPEC.md` stays in context on every command.
  A later task follows the same rules as the first.
- **No extra lookups.**
  A citation such as `§V.<n>` is an address in `SPEC.md`.
  The command reads that row from the file already in context.

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
The skill enters Claude Code plan mode and writes the proposal to the session plan file.
You critique it.
The loop stops when `## Open Questions` is empty.
You approve the plan in the plan-mode prompt.

After you approve, the skill opens a GitHub issue with the plan as its body.
The issue gets a class label: `enhancement`, `bug`, or `documentation`.
The default label is `enhancement`.
The issue body ends with an `## Acceptance` checklist built from the plan's success criterion.
Then the skill stops.
It does not write `designs/<slug>.md` unless you ask for a copy.

Fold the issue into the spec later with `/sdd:spec github issue N`.
In the same session, `/sdd:spec fold-design` also works and keeps the link to issue N.
An older `designs/<slug>.md` draft still folds with `/sdd:spec designs/<slug>.md`.

```bash
/sdd:design how should the release pipeline split monorepo plugins?
# after you approve: a labeled GitHub issue is opened
/sdd:spec github issue N
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
/sdd:spec github issue 12   # fold an issue into §V and §T; see Issue-linked pull request
```

A small amend (one target, one cell or line, no new `§V` row) still shows a preview.
Its confirm option `Apply` comes first.
After a **BACKPROP**, the next item names the exact `/sdd:build §T.<n>` to run.
After a **DISTILL**, the next items are `/sdd:check` and a confirm pass over rows marked `?`.

### Issue-linked pull request

Every GitHub issue you work on gets one pull request linked to it.
No corresponding GitHub issue means no git branch, no GitHub PR.
In that case the work commits on the current branch.

`/sdd:spec github issue N` runs these steps once, before it writes any spec change:

1. Push the default branch when it is ahead of `origin`.
2. Check out the issue branch with `gh issue develop N --checkout`.
3. Make one empty commit, so the branch is one commit ahead of its base.
4. Open a draft with `gh pr create --draft`.
   The body has a `Related: #<issue>` line.
   It has no close trailer, and review does not run at this point.

A missing `SPEC.md` does not skip the pull request.
When an open pull request for the issue already exists, the command switches to its branch and opens no second one.

With `SPEC.md` present, the fold drafts the spec change on the issue branch.
After you confirm, it commits and pushes.
Then a chain runs once with no wait for you:

1. A sub-agent runs `/sdd:build` on the fold-produced `§T` ids only.
   Those ids are the new `§T` rows and the existing open rows that got acceptance notes in this fold.
2. The bundled `code-review` skill reviews the branch.
   A doc-or-comment diff skips review.
   That diff changes only `SPEC.md`, `SPEC.archive.md`, `.spec/check-extras.md`, `SPEC-FORMAT.md`, `README.md`, `CLAUDE.md`, or files under `designs/`, or it changes only comment and whitespace lines.
3. The parent applies the review findings, runs the checks again, pushes, and runs `gh pr ready`.

**Acceptance gate.**
Before any step closes issue N, build and the github skill read the issue's `## Acceptance` checklist.
Each open item needs evidence: a test name, a code path, or a command result.
An item without evidence blocks the close.
An issue with no `## Acceptance` section produces an advisory, not a silent pass.

The close trailer (`Closes #<issue>`) is added only at merge, after the acceptance gate passes.
Merge is a squash with branch delete.
The squash commit subject holds `#<issue>`, the linked issue number, so `git log` shows which issue closed.

### `/sdd:build`

`/sdd:build` plans a task, edits the code, then verifies the result.
Edits run on the main session.
Planning reads may use sub-agents.

- `§T.<n>` implements that task.
- `--next` implements the lowest-numbered row with status `.`.
- `--all` implements every `.` row in `§T` order.
- `§T.<a>,§T.<b>` implements those rows in `§T` order.
- `--no-chain` turns off the follow-up check described below.
- An empty argument does the same thing as `--next`.

After a task passes, build runs `/sdd:check` on the closed task in the same turn.
This follow-up is called the green-path chain.
It makes one hop per turn: a command reached by a hop does not hop again.
On an issue-linked branch, build instead pushes after each task and marks the pull request ready once at the end.
It then asks you to say "merge the PR" when review approves.

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
- `--no-chain` turns off the follow-up build described below.

Violations are grouped as `VIOLATE`, `RISK`, or `STALE`.
The report names a next command, usually `/sdd:explain`, `/sdd:spec <intent>`, or `/sdd:build`.
A report with violations never runs a fix.
A clean report with open tasks runs `/sdd:build --next` once in the same turn.
Check itself runs in a read-only forked context, so that build runs in the main session.

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
/sdd:design how should we shape the parser / renderer split?   # optional; opens a GitHub issue
/sdd:spec github issue N    # fold that issue; or describe the project directly:
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

`telegraph`, `backprop`, `socratic`, `steno`, `github`, and `monitor` run from the commands above.
You do not call them by slash command.
Each other directory under `skills/` is one slash command.
`skills/spec/` is `/sdd:spec`.
Skill frontmatter is honored on dispatch: `description`, `argument-hint`, `allowed-tools`, `disallowed-tools`, `user-invocable`, `context`, and `effort`.
`check` and `explain` set `effort: medium`.
No skill sets `model`, so each skill uses the session model.

```
.claude-plugin/plugin.json       plugin manifest (name: sdd)
.claude-plugin/marketplace.json  marketplace manifest for direct install
skills/design/                   /sdd:design — plan mode, then a labeled GitHub issue
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
skills/github/                   gh issue and pull-request workflow; runs on gh operations
skills/monitor/                  files a plugin issue when an sdd skill misbehaves
skills/_fragments/               shared recipe text loaded by the skills (not commands)
scripts/check-mechanical.py      deterministic checks used by /sdd:check
benchmarks/telegraph/            token-reduction benchmark, results, and write-up
SPEC-FORMAT.md                   format contract for every SPEC.md
```

## Attribution and license

SDD is adapted from [**JuliusBrussee/cavekit**](https://github.com/JuliusBrussee/cavekit) (v4.0.0, MIT).
The upstream repo has the original project, its history, and `v3.1.0` (the full Hunt lifecycle, with sub-agents, parallel workers, and design-system enforcement).

MIT.
See [`LICENSE`](LICENSE).
