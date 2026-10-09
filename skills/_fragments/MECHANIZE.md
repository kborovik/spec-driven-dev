# MECHANIZE — script-candidate scan (canonical)

Loaded by pointer from every user-invocable skill.
Single source per mechanize-scan invariant — skill bodies never copy this block.

## PROBE

Recipe end → before the `## Next` block, scan this run for a mechanization candidate.

Candidate = any of:

- ≥ 2 same-shape deterministic calls this run (identical command modulo args)
- LLM-side join / sort / count / dedup over script-emittable data
- multi-step parse collapsible to one script emit mode
- fresh regex paraphrase of an existing mechanical rule (mechanical-realization invariant class)

Hit → emit exactly one `## Next` item naming the observed pattern + proposed script mode; none → no item.
Never self-implement the mechanization mid-run (recipe-step-no-dispatch + write-ownership invariants).

## ROUTE

Route by cwd:

- dev repo (this plugin) → /sdd:spec → new §T row
- consumer repo, plugin-target → /sdd:spec mechanization-candidate (monitor-protocol invariant)
- consumer repo-local → consumer /sdd:spec → `.spec/check-extras` row
