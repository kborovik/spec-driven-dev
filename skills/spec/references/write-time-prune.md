# spec references — write-time prune pattern set

Conditional detail split from spec SKILL.md per token-budget invariant (skill-body budget).
Telegraph register (SPEC-ADJACENT).
Read @ APPLY step 0 when a prune condition matches; SKILL.md step 0 holds the fire conditions.

Per freshness-contract invariant (SPEC.md is clean current design; history in commit log + archive, not inlined).
Auto-rewrites delta → clean current state; pruned history → auto-commit msg body (recoverable via code + `git log`).
Show-user diff displays post-prune row — prune reviewed, not blind.

**§V-row delta prune** (delta patches pre-existing §V row): strip inlined-history residue.
Member set = script-owned `PRUNE_PATTERNS` (sole source per freshness-contract + mechanical-realization invariants — shared w/ /sdd:check history-residue audit + token-budget condense body-trim prong); consume `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py emit-prune-patterns` → `id|role|pattern|action` table, never a restated member list.
Role application @ write: `residue` rows → apply `action` (drop); `fold` rows → apply fold action; `pre-filter` rows → exempt match before the residue scan.
Stripped content → commit-msg body per APPLY step 4.

**§B cause trim** (delta adds/rewrites §B `cause` cell): auto-trim → one-line bug-class description; multi-line forensics (repro transcript, root-cause walk, sha lineage) → commit-msg body per APPLY step 4.
Preview shows trimmed form, not raw forensics.

§T body not pruned here — /sdd:build flips status cell only per status-flip invariant so §T rows authored one-line @ creation (NEW + BACKPROP drafts); pre-existing §T residue owned by token-budget condense body-trim prong + /sdd:check oversized-cell advisory backstop.
