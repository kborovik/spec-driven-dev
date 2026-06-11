---
name: explain
description: |
  Telegraph → prose. Expand any SPEC.md citation into plain English. Read-only.
  Inverse of the telegraph skill (telegraph encoder). Triggers when human wants
  to understand a §V invariant, §T task, §B bug, or §I interface without the
  encoding. Phrasings: "/sdd:explain", "what does §V.<n> mean", "decompress
  this", "explain in prose", "I don't read telegraph". not for writes — those
  go through /sdd:spec.
allowed-tools: Read, Grep, Glob, Skill
model: sonnet
---

# explain — decompress spec into prose

Inverse of the `telegraph` skill (telegraph encoder). Human-facing. Reads SPEC.md, expands one citation into plain English with cited context. Writes nothing.

## LOAD

1. Read `SPEC.md`. If missing → "no spec, nothing to explain." Stop.
2. Parse `$ARGUMENTS`:
   - `§T.n` / `§V.n` / `§B.n` / `§I.<key>` → that row
   - `§G` / `§C` → that section in full
   - `--next` or empty → lowest-numbered §T row with status `.`
3. Renumber-map probe — `.claude/spec-renumber-map.json` exists (written by reorganize skill per §V renumber permission) → on `§V.<n>` arg, walk `old:V<n> → new:V<m>` chain newest-first until not further mapping, then resolve substituted id against current SPEC.md. Read-only contract preserved per read-only-diagnostic invariant — map consulted, not mutated. not exist → arg resolves directly against current SPEC.md.
4. If citation absent → list valid ids in target section. Stop.

## EXPAND

For the chosen citation:

1. Quote the raw telegraph line(s) verbatim in a code block.
2. Restate in plain English. No telegraph symbols, no fragments — full sentences.
3. Pull in cited siblings:
   - §T row → expand every §V and §I it cites.
   - §V row → list §T tasks that cite it and §B bugs that reference it.
   - §B row → expand the §V it broke and the fixing §T.
   - §I row → name §V invariants that constrain it.
   - §G / §C → no cross-cites; just prose.
4. Close with one line: what the reader should now understand.

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

## OUTPUT — "Next" block

Heading `## Next`; 1–5 atomic items (one sentence each, no `Reply` prefix); positional dispatch (`run <int>` or `run /<plugin>:<cmd> [args]`). Optional `## Hint` (≤ 3 lines) precedes when item selection needs hidden state (closed-vs-pending row implications, citation-form edge cases). explain is read-only so items are slash-cmd follow-ups: `/sdd:build §T.n` only for `.` rows; closed `x` rows → `/sdd:explain --next` or `/sdd:check`.

Example for a closed §T row (terminal state):

```
## §T.<n> — add auth middleware

> T<n>|x|add auth mw|V<n>,I.api

In plain English: this task added an authentication middleware...

Status: complete (`x`).

Bottom line: §V.<n> is enforced by the middleware shipped under §T.<n>.

## Hint

Closed rows are historical. `run 1` skips to live work; `run 2` audits whether the closed task drifted out of code.

## Next

1. /sdd:explain --next — read the next pending §T row
2. /sdd:check — audit whether the closed task still holds
```

The "Bottom line" sentence stays — it summarizes the citation, it does not direct action. Action lives only in Next; pre-action context lives in optional Hint.

## NON-GOALS

- Zero writes. No SPEC.md edits. No code edits.
- No code reads. Spec-only. (Use `/sdd:check` if you want spec-vs-code.)
- No telegraph in output. Prose is the whole point.
- No multi-citation expansion in one call. One id per invocation; loop if needed.
