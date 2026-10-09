# PROGRESS checklist (canonical)

Multi-phase run per response-shape invariant → emit live harness checklist.
TaskCreate one task per phase (or per §T row for build `--all`) at start.
TaskUpdate `in_progress` at phase/row entry → `completed` at exit.
Cancel / subset-skip → unreached phases `deleted`, not `completed`.
Checklist = ephemeral harness UI: never repo state, never substitutes REPORT or `## Next`.
