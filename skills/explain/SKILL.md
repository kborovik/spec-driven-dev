---
name: explain
description: |
  Telegraph → prose. Expand one SPEC.md citation into plain English. Read-only;
  inverse of telegraph skill (telegraph encoder). Triggers: "/sdd:explain",
  "what does §V.<n> mean", "decompress this", "explain in prose", "I don't
  read telegraph". Writes → /sdd:spec.
allowed-tools: Read, Bash(python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-mechanical.py *)
disallowed-tools: Edit, Write
argument-hint: "[§-cite | --next]"
effort: medium
---

# explain — decompress spec into prose

Inverse of `telegraph` skill.
Human-facing.
Reads SPEC.md, expands one citation → plain English w/ cited context.
Zero writes.

## LOAD

1. Spec overview via `python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-mechanical.py emit-overview` — §G/§C/§I/§T/§B bodies + §V id list; not whole-file Read per single-load invariant (exact script-path grant pin via `${CLAUDE_SKILL_DIR}` frontmatter substitution per tooling-preference invariant).
   Script error "SPEC.md not found" → "no spec, nothing to explain."
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
5. §V bodies (target row + cited siblings) via `python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-mechanical.py emit-v-slices --dirty V<n>,...`; stub row `→ .spec/check-extras.md §V<n>` → Read that § there.

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

## MECHANIZE

Load `${CLAUDE_SKILL_DIR}/../_fragments/MECHANIZE.md`.

## OUTPUT — "Next" block

Per `${CLAUDE_SKILL_DIR}/../_fragments/NEXT.md`.
Read-only follow-ups: `/sdd:build §T.n` only for `.` rows; closed `x` → `/sdd:explain --next` or `/sdd:check`.
"Bottom line" summarizes citation, never directs action.

## NON-GOALS

- Zero writes.
  No SPEC.md edits, no code edits.
- No code reads.
  Spec-only (spec-vs-code → `/sdd:check`).
- No telegraph in output.
  Prose is the whole point.
- One id per call.
  Loop for multiple.
