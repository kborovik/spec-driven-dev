# check references — REPORT templates + examples

Conditional detail split from check SKILL.md per token-budget invariant (skill-body budget).
Telegraph register (SPEC-ADJACENT).
Read @ REPORT assembly; SKILL.md REPORT § holds the structural rules.

## Severity-block template

```
## invariant drift
V<n> VIOLATE: auth/mw.go:47 uses `<` not `≤`. see §B.<n>.
V<n> VIOLATE-CAPTURED: <commit-sha> body contains heavy math operators; see §B.<n>.
V<n> UNVERIFIABLE: no test covers every req path.
§T.<n> VIOLATE: history: dated-retirement in task body — prune per freshness-contract invariant.
mechanize DRIFT: skills/explain/SKILL.md MECHANIZE block diverges from canonical.
dispatch VIOLATE: skills/build/SKILL.md:96 slash-dispatches auto-fire sub-skill /<plugin>:<sub-skill>.
grant VIOLATE: skills/explain/SKILL.md:8 grants Grep zero body use.
idiom VIOLATE: README.md:25 banned idiom load-bearing in human-facing prose.

## cite drift
T<n>.cites V<m> UNRESOLVED: V<m> absent from invariants section.
§B.<n>.fix T<k> TYPE-MISMATCH: target is task row, expected invariant row.
CLAUDE.md:<line> cite UNRESOLVED: row absent.

## interface drift
I.api DRIFT: POST /x returns `{result}` not `{id}`. route.go:112.
I.cmd MISSING: `foo bar` absent from cli/*.go.

## task drift
T<n> STALE: status `x`, no middleware file exists.

## summary
2 violate. 1 violate-captured. 1 missing. 1 stale. 1 unverifiable. 1 unresolved. 1 type-mismatch. 5 suppressed (1 scope-empty, 2 hold-since-clean, 2 latent).
```

## Body-row aggregation template

Aggregated `history`-class form (section count > script-owned threshold):

```
## invariant drift
§V: 49 rows (29 amendment-counter, 12 dated-retirement, 8 supersession-narration) → /sdd:condense body-trim
§B.<n> VIOLATE: history: amendment-counter @ SPEC.md:<line>
```

## Remedy map — drift class → Next-block item

- VIOLATE / DRIFT → `/sdd:spec <description citing §V.<n>>` (gate routes to BACKPROP).
- VIOLATE-CAPTURED → no action; baseline `§B`-recorded, remediation forward-only.
- `history:` VIOLATE → `/sdd:spec amend §<S>.<n>` to prune inlined history; task-row residue → `/sdd:condense` body-trim.
- `format:` VIOLATE → `/sdd:spec amend §<S>.<n>` (or `/sdd:condense` when archive-marker / window split).
- SUPPRESSED → no action; rolls forward until trigger fires / touch intersects / scope expands.
- MISSING → `/sdd:build <task-cite>` if task exists; else `/sdd:spec amend task` to add row.
- STALE → `/sdd:spec amend <task-cite>` to uncheck status.
- EXTRA → invariant mandates the surface → `/sdd:spec amend interfaces` (cause known); invariant silent → `/sdd:spec <surface> missing from interfaces section` (cause TBD, `§B` row starts conversation).
- UNRESOLVED / TYPE-MISMATCH → `/sdd:spec amend §<S>.<n>` to repair stale or wrong-section cite.

## Checkpoint + advisory example

```
## checkpoint
clean — memo @ 060a9d2

## advisory
memo schema_version mismatch — memo dropped, full sweep
SPEC.md ~30k tokens > 20k budget; consider /sdd:condense

## summary
0 violate. 1 violate-captured. 39 suppressed (18 hold-since-clean, 2 latent, 19 hold).
```
