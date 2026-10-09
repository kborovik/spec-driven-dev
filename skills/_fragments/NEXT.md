# Next-block contract (canonical)

User-typeable skill output ends with heading `## Next`.
1–5 atomic items (one sentence each, no `Reply` prefix).
Positional dispatch: `run <int>` or `run /sdd:<cmd> [args]`.
Optional `## Hint` (≤ 3 lines) may precede when selection needs hidden state.

Dispatched `<cmd>` names only user-invocable skills — never auto-fire sub-skills (telegraph, backprop, socratic, steno, monitor, github).
Bug → spec user route = `/sdd:spec <intent>`, never `/sdd:backprop`.

**Issue-linked merge pause (sole non-slash exception):** after READY, Next item #1 names the operator phrasing that auto-fires github MERGE, for example `merge when approved — say "merge the PR"` or `merge PR <pr> — say "merge the PR" when review approves`.
That item is not a `/sdd:*` dispatch; it documents the auto-fire trigger only.
`/sdd:check` listed not hopped after that item.

Recipe ends at commit + Next (or report + Next for read-only skills), except green-path chain and build verify-fail mid-loop spec per recipe-step-no-dispatch invariant.
