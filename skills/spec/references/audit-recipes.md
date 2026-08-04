# spec references — APPLY audit sub-recipes

Conditional detail split from spec SKILL.md per token-budget invariant (skill-body budget).
Telegraph register (SPEC-ADJACENT).
Read @ first audit fire per APPLY step 1; the step-1 table routes each audit here.

## SWEEP-§T SCOPE AUDIT

Every sweep-§T row (remediating §V-class violation) in delta ! task line declares scope as grep pattern or vocab table per sweep-§T-scope invariant; named-procedure or named-site list not accepted.
No pattern → bail w/ `sweep §T row scope ! grep pattern per sweep-§T scope rule`; user supplies pattern, retry.

## PINNED-CITE AUDIT

**Sub-recipe (a) — PUBLISHED-scope ban**: grep `§[VTB]\.[0-9]+` in delta touching PUBLISHED scope (per scope-set invariant).
Match → bail `pinned §-cite not allowed in PUBLISHED — use placeholder form (§V.<n>) or inline rule embedding` until rewrite.
No PUBLISHED delta → no-op.

**Sub-recipe (b) — SPEC.md-narrative §V resolution**: grep `§V\.[0-9]+` in delta touching SPEC.md narrative (§G/§C/§I/§V/§T/§B body).
Pre-filter backtick-wrapped tokens `grep -v -E '`[^`]*§V\.[0-9]+[^`]*`'` (invert scan, grep -v -E per tooling-preference invariant) — historical-quote form per verbatim invariant exempt.
Each surviving match resolves against current SPEC.md §V row set (parse `^V[0-9]+:` openers).
Unresolved → bail `stale §V.<n> cite in delta — row absent (likely folded); backtick-wrap historical or substitute live row` until rewrite.
No narrative delta → no-op.

(a) defends against PUBLISHED-touching deltas via spec-cmd flow — `/sdd:spec` normally writes SPEC.md only so typically no-op. (b) closes post-fold authoring gap — fold-time sweep (condense prong-1) substitutes existing cites @ fold-commit; new bare cites to folded id authored post-fold bypass until next `/sdd:check`.
Pattern-match catches what LLM prose-review missed (see §B history).

## NEXT-BLOCK-SECTION AUDIT

Audits touched user-typeable `<plugin>/skills/<n>/SKILL.md` per skills-only architecture invariant.
User-typeable = frontmatter lacks `disable-model-invocation: true` and `user-invocable: false` (skill dir surfaces as `/<plugin>:<n>` natively unless opted out).

Each touched file in post-amend tree:
1. Grep `^(disable-model-invocation|user-invocable):\s*` over frontmatter block.
2. Opt-out match → no-op for this file (auto-fire or programmatic-only, no slash-cmd surface).
3. Else grep `## OUTPUT — "Next" block` heading in post-amend file.
   Match → no-op; else bail `<skill> SKILL.md lacks Next-block section per /<plugin>:<n> response-shape contract` until author adds §.

Defends against new user-typeable skill bodies (or cross-plugin migrations) omitting Next-block contract sister skills carry — V20-class runtime rule governs response shape, not authoring-time presence (see §B history).
Structurally no-op while APPLY step 4 writes SPEC.md only (mirrors pinned-cite (a) posture).

## FOLD-FIRST AUDIT

Per fold-first authoring invariant (§V.<n>).
Mechanical decision-gate.

Each proposed new §V row in delta:

1. Closest existing §V row by topic — heuristic: shared scope tokens (e.g. `PUBLISHED`, `GITHUB-FACING`, `SPEC-ADJACENT`), shared procedure ref (e.g. `/sdd:spec`, `/sdd:check`), shared verb pattern (e.g. `audit`, `auto-fire`, `gate`).
   None identifiable → step 3 w/ "no fold candidate" note.
2. AskUserQuestion per decision-gate invariant (§V.<n>):
   - **question**: `New §V row proposed: <delta one-line>. Closest existing row §V.<m>: <m-summary>. Fold into existing or split as new row?`
   - **header**: `Fold-first`
   - **options** (3, mutually exclusive, label = action):
     - `Fold into §V.<m>` → reroute delta as §V.<m> amend (inline addition to existing row).
     - `New row (cite §B recurrence-class)` → proceed; requires §B.<k> cite in delta justifying split (audit greps `§B\.[0-9]+` post-selection).
     - `New row (orthogonal concept)` → proceed; user-typed orthogonal-concept declaration recorded in commit msg post-selection.
3. Fold-into → re-render delta as §V.<m> amend, re-enter APPLY @ step 0 per Re-entry rule (re-prune + re-audit — not jump to show-user); new-row branches → record justification, proceed to show-user.

Defends against premature-split class — small audit or enforcement-meta additions creating new §V row when inline amend sufficed. "mirrors §V.<n>" alone insufficient justification per fold-first authoring invariant.
