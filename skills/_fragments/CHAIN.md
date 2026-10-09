# Green-path chain (canonical)

Default-on for solo operators per recipe-step-no-dispatch invariant.
Operator may pass `--no-chain` on build or check to disable for that run.
`POST-SPEC-CHILD=1` implies `--no-chain` — the post-spec build child never hops.
Issue-linked READY (operator-run or post-spec remainder) implies no check hop.

## Edges (same turn, high confidence only)

| From | Condition | Same-turn continue |
|------|-----------|-------------------|
| build pass | §T flipped `.`→`x`, auto-commit landed; not issue-linked READY | `/sdd:check` cascade over just-closed §T |
| issue-linked READY | operator-run or post-spec remainder | no check hop; Next merge phrasing leads; `/sdd:check` listed not hopped |
| check clean | ≥ 1 pending `.` §T | `/sdd:build --next` (or concrete `§T.n`); check runs `context: fork` → REPORT `## chain` hop line, main thread runs build |
| build FAIL | class (b)/(c) | mid-loop `/sdd:spec` BACKPROP (already required) |
| check dirty | any surface violation | never auto-remedy; Next only |

## Rules

- One hop per operator turn: the recipe the operator dispatched may hop once; a recipe reached by a hop never hops again.
  Concretely: operator build pass hops to check and stops there; operator check clean hops to build --next and stops there.
- `--all` / multi-id build: chain check once after the last closed row, not after every row.
- `--no-chain` wins over default-on.
- `POST-SPEC-CHILD=1` never hops (implies `--no-chain`).
- Issue-linked READY (operator-run or post-spec remainder) implies no check hop — Next merge phrasing leads; `/sdd:check` listed not hopped.
- Backprop handoff after build FAIL still mid-loop; after BACKPROP APPLY, prefer concrete `/sdd:build §T.n` (resume card).
