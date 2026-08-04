# spec references — write-time prune pattern set

Conditional detail split from spec SKILL.md per token-budget invariant (skill-body budget).
Telegraph register (SPEC-ADJACENT).
Read @ APPLY step 0 when a prune condition matches; SKILL.md step 0 holds the fire conditions.

Per freshness-contract invariant (SPEC.md is clean current design; history in commit log + archive, not inlined).
Auto-rewrites delta → clean current state; pruned history → auto-commit msg body (recoverable via code + `git log`).
Show-user diff displays post-prune row — prune reviewed, not blind.

**§V-row delta prune** (delta patches pre-existing §V row): strip inlined-history residue.
Pattern set (single source per freshness-contract invariant — shared w/ /sdd:check history-residue audit + token-budget condense body-trim prong):

- amendment-counter `(∆)` markers → drop (clean current state carries no edit tally).
- dated-retirement `retired YYYY-MM-DD` clause in live row → drop (wholesale-retired row is reorganize archival job, not amend residue).
- supersession-narration (`pre-amend …`, `prior … retired/dropped/superseded`) → drop.
- `Closes §B.<x>` standalone narration → fold to `(closes §B.<x>)` suffix.

Pre-filters (exempt, not pruned): backtick-wrapped tokens per verbatim-preservation invariant (code-context pattern-defs + quoted historical refs — §V row whose subject is a retirement rule not self-flag); cite-modifier `§V.<n>(∆)` (∆-on-citation marks amended cross-ref, differs ∆-on-retired-value).
Stripped content → commit-msg body per APPLY step 4.

**§B cause trim** (delta adds/rewrites §B `cause` cell): auto-trim → one-line bug-class description; multi-line forensics (repro transcript, root-cause walk, sha lineage) → commit-msg body per APPLY step 4.
Preview shows trimmed form, not raw forensics.

§T body not pruned here — /sdd:build flips status cell only per status-flip invariant so §T rows authored one-line @ creation (NEW + BACKPROP drafts); pre-existing §T residue owned by token-budget condense body-trim prong + /sdd:check oversized-cell advisory backstop.
