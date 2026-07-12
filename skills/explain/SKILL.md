---
name: explain
description: |
  Telegraph → prose. Expand one SPEC.md citation into plain English. Read-only;
  inverse of telegraph skill (telegraph encoder). Triggers: "/sdd:explain",
  "what does §V.<n> mean", "decompress this", "explain in prose", "I don't
  read telegraph". Writes → /sdd:spec.
allowed-tools: Read
disallowed-tools: Edit, Write
model: sonnet
---

# explain — decompress spec into prose

Inverse of `telegraph` skill.
Human-facing.
Reads SPEC.md, expands one citation → plain English w/ cited context.
Zero writes.

## LOAD

1. Read `SPEC.md`.
   Missing → "no spec, nothing to explain."
   Bail.
2. Parse `$ARGUMENTS`:
   - `§T.n` / `§V.n` / `§B.n` / `§I.<key>` → that row
   - `§G` / `§C` → full section
   - `--next` or empty → lowest-numbered §T row w/ status `.`
3. `.spec/spec-renumber-map.json` exists (written by reorganize skill per §V renumber permission) → on `§V.<n>` arg, walk `old:V<n> → new:V<m>` chain newest-first to end, resolve result against current SPEC.md.
   Map read, never mutated (read-only-diagnostic invariant).
   Absent → arg resolves directly.
4. Citation absent → list valid ids in target section.
   Bail.

## EXPAND

1. Quote raw telegraph line(s) verbatim in code block.
2. Restate in plain English — full sentences, no telegraph symbols, no fragments.
3. Pull cited siblings:
   - §T → expand every §V and §I it cites.
   - §V → list §T tasks citing it, §B bugs referencing it.
   - §B → expand broken §V and fixing §T.
   - §I → name constraining §V invariants.
   - §G / §C → no cross-cites; prose only.
4. Close w/ one line: what reader should now understand.

## OUTPUT SHAPE

```
## §T.<n> — add auth middleware

> T<n>|.|add auth mw|V<n>,I.api

In plain English: this task adds an authentication middleware that runs before
every request reaches its handler.

Cited invariants:
- §V.<n> — every request must pass an auth check before the handler runs.

Cited interfaces:
- §I.api — POST /x returns 200 with {id:string}; the middleware must not
  change this shape.

Status: not started (`.`).

Bottom line: implement a middleware that enforces §V.<n> without altering §I.api.

## Hint

§T.<n> is pending — typical next step is item 1 to start work, or item 2 if you want to read the cited invariant first.

## Next

1. /sdd:build §T.<n> — start implementation
2. /sdd:explain §V.<n> — read the cited invariant in prose
```

## MECHANIZE — script-candidate scan

Recipe end → before the `## Next` block, scan this run for a mechanization candidate.
Candidate = any of:

- ≥ 2 same-shape deterministic calls this run (identical command modulo args)
- LLM-side join / sort / count / dedup over script-emittable data
- multi-step parse collapsible to one script emit mode
- fresh regex paraphrase of an existing mechanical rule (mechanical-realization invariant class)

Hit → emit exactly one `## Next` item naming the observed pattern + proposed script mode; none → no item.
Never self-implement the mechanization mid-run (recipe-step-no-dispatch + write-ownership invariants).
Route by cwd:

- dev repo (this plugin) → /sdd:spec → new §T row
- consumer repo, plugin-target → monitor dispatched `mechanization-candidate` path (monitor-protocol invariant)
- consumer repo-local → consumer /sdd:spec → `.spec/check-extras` row

## OUTPUT — "Next" block

Heading `## Next`; 1–5 atomic items (one sentence each, no `Reply` prefix); positional dispatch (`run <int>` or `run /<plugin>:<cmd> [args]`).
Optional `## Hint` (≤ 3 lines) precedes when item selection needs hidden state (closed-vs-pending row implications, citation-form edge cases).
Read-only → items are slash-cmd follow-ups: `/sdd:build §T.n` only for `.` rows; closed `x` rows → `/sdd:explain --next` or `/sdd:check`.

Closed §T row (terminal state) — tail of output:

```
Status: complete (`x`).

Bottom line: §V.<n> is enforced by the middleware shipped under §T.<n>.

## Hint

Closed rows are historical. `run 1` skips to live work; `run 2` audits whether the closed task drifted out of code.

## Next

1. /sdd:explain --next — read the next pending §T row
2. /sdd:check — audit whether the closed task still holds
```

"Bottom line" stays — summarizes citation, never directs action.
Action only in Next; pre-action context in optional Hint.

## NON-GOALS

- Zero writes.
  No SPEC.md edits, no code edits.
- No code reads.
  Spec-only (spec-vs-code → `/sdd:check`).
- No telegraph in output.
  Prose is the whole point.
- One id per call.
  Loop for multiple.
