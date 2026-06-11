---
name: spec
description: |
  Sole semantic author of SPEC.md @ repo root — create, amend, fold designs,
  or backprop bugs (§T status-flip → build, archive → compact, §V renumber →
  reorganize; those carve-outs not authoring paths).
  Triggers when user asks to write spec, start new spec, distill spec from
  code, add invariants, amend a section, or record a bug. Common phrasings:
  "write the spec for...", "new spec", "distill spec from code",
  "spec this idea", "import existing repo", "pull invariants out of code",
  "this bug keeps biting", "post-mortem on Y".
allowed-tools: AskUserQuestion, Read, Edit, Write, Grep, Bash(git *), Bash(rg *), Skill
model: opus
---

# spec — spec mutator

The `telegraph` skill (telegraph encoder) applies to all writes here.

## DISPATCH

**Step 0 (precondition):** `git status --porcelain SPEC.md` empty → continue; not → bail w/ "SPEC.md has uncommitted changes; commit or stash first" (auto-commit on apply assumes clean baseline; porcelain form catches staged + untracked, which `git diff --quiet` misses).

**Step 1 (design-fold-in shortcut):** input arg is path matching `designs/*.md` and file exists and `SPEC.md` exists @ repo root → FOLD-IN procedure (skip socratic gate; design skill Open-Questions-empty rule is persistence pre-condition so design content already converged). Design path w/o SPEC.md → bail w/ "fold-in needs SPEC.md; init via NEW or DISTILL first" (design skill degrades gracefully sans SPEC.md so converged drafts can predate it). Else → continue to gate.

Engage `sdd:socratic` gate w/ user input as intent. Gate runs single-question loop until convergence triple matches one mode:

- **NEW** is goal and first-principle-asked and (≥ 1 invariant or ≥ 1 task)
- **DISTILL** is explicit "build from code" intent (gate exits ≤ 1 turn — walks repo, no further interrogation)
- **BACKPROP** is symptom and surface and recurrence-class
- **AMEND** is §-target and delta

Two paths (SPEC.md presence is the only branch — mode is gate byproduct, not user-typed prefix):

1. ** not `SPEC.md` @ repo root** → gate restricted to {NEW, DISTILL}; post-convergence → run mode-specific procedure below.
2. **`SPEC.md` exists** → gate ranges over {BACKPROP, AMEND, NEW}; post-convergence → run mode-specific procedure. NEW available but rare → require explicit re-init confirmation before overwrite.

Concrete first-turn input → gate passes ≤ 1 turn (zero-friction); vague → dialogue continues until convergence. not skip flag, not prefix back-doors.

## NEW — idea → spec

Input: user idea.

Steps:
1. Extract goal (1 line, telegraph). → §G.
2. List constraints user stated or implied. → §C.
3. List external surfaces user named. → §I.
4. Propose initial invariants. → §V (numbered V<n>). first-principle (foundational claim) probed by gate; user may decline → NEW converges on derived invariants only. late first-principle → AMEND §V back-door (AMEND is the only late-entry path; not second authoring path).
5. Break goal into ordered tasks. → §T pipe table, all status `.`, ids T<n>.
6. §B section with header row only (`id|date|cause|fix`).

→ APPLY.

## DISTILL — code → spec

Walk repo. Produce §G (infer from README/package.json/main entry), §C (infer from stack), §I (enumerate public APIs/CLIs/configs), §V (derive from tests and assertions), §T (one task per known TODO or missing test), §B (empty). Flag uncertain items with `?` in text so user can confirm.

→ APPLY.

## BACKPROP — bug → §B + §V

Input: gate-produced triple (symptom and surface and recurrence-class).

Steps:
1. Parse bug description.
2. Find root cause (read relevant code).
3. Decide: would a new invariant catch recurrence? If yes → draft `V<next>`.
4. Append §B row: `B<next>|<date>|<cause>|<fix>` — fix cell is `V<N>` when step 3 drafted an invariant, sentinel `-` otherwise (per SPEC-FORMAT §B fix grammar).
5. If drafted: append new invariant to §V.
6. If fix also changes behavior → add/update §T rows.

→ APPLY.

Rule: every bug gets a §B entry. Invariant optional but preferred.

## AMEND — targeted edit

Input: gate-produced §-target and delta.

Read that section. Show current in steno per steno skill if target in {§V, §B} (audience is user reviewing proposal); telegraph per telegraph skill otherwise. Ask user what changes.

→ APPLY.

Never silently rewrite sections user did not name.

## FOLD-IN — design draft → §V or §T amend

Input: path to `designs/<slug>.md` (design draft converged per design skill Open-Questions-empty rule).

not socratic gate — design skill enforces convergence pre-persist so /sdd:spec trusts content. Multi-target by nature: a single design may propose new §V row(s), new §T row(s), §I edit(s), or §B row(s) in one apply.

Steps:
1. Read `designs/<slug>.md`. Parse proposed amendments: new §V invariants, new §T rows, §I edits, §B rows.
2. Draft each amendment in telegraph per telegraph skill (target sections + delta text).

→ APPLY.

Rule: fold-in mutates SPEC.md only; design file persists in working tree post-apply (not `git rm`, not `git add`, not `rm`) per design-file lifecycle invariant — APPLY write step is SPEC.md-only so structurally enforced. User removes or preserves manually. Provenance via SPEC.md commit message containing slug and git history.

## APPLY (all modes, post-delta)

Runs after a mode hands off its drafted delta. Five steps in order; audits fire on triggering condition, not on mode authorship.

**Step 0 — write-time prune** (delta-rewrite stage, not bail-gate so ordered ahead of the audit table):

- delta modifies a pre-existing §V row → §V-row residue prune per write-time prune section.
- delta adds or rewrites a §B `cause` cell → one-line trim per write-time prune section.
- pruned content → commit-msg body (picked up @ step 4); step 3 show-user displays post-prune form. Prune-first guarantees every audit sees final-form delta.

**Step 1 — audit table** (condition-gated; on-fail column names the owning recipe section — bail strings and sub-recipe detail live there only, not restated here):

```
audit       | fires when delta…                                        | on fail
sweep-scope | contains sweep-§T row (§V-violation remediation)         | bail → sweep-§T scope audit
pinned-cite | touches PUBLISHED (a) or SPEC.md narrative (b)           | bail → pinned-cite audit, matching sub-recipe
next-block  | touches user-typeable SKILL.md                           | bail → Next-block-section audit
fold-first  | adds §V row to pre-existing §V section, mode not FOLD-IN | AskUserQuestion gate → Fold-first audit
```

pinned-cite (a) + next-block rows structurally no-op while step 4 writes SPEC.md only — retained defensive (fire only if a future mode widens the write set).

Table written in named-invariant + placeholder cite form only (`per <named> invariant`, `§V.<n>`) — `skills/**` in PUBLISHED, where pinned §-digit cites are banned by pinned-cite sub-recipe (a); body pinned-cite count is 0, stays 0.

**Step 2 — render-split**: §V and §B content rows → steno per steno skill (audience is user reviewing proposal); all else → telegraph per telegraph skill (§T and §I pipe/prose forms already human-legible, §G/§C targets, header-only §B row).

**Step 3 — show-user**: present the rendered diff preview; await user OK.

**Step 4 — write + commit**: on user OK → write SPEC.md in telegraph per telegraph skill and auto-commit `git add SPEC.md`; not user prompt for commit step (uniform every mode). Commit message per mode:

```
NEW      → init SPEC.md (V<1>..V<n>, T<1>..T<m>)
DISTILL  → init SPEC.md from code
BACKPROP → backprop §B.<n>(+) + §V.<N>(+): <one-line cause>   (trimmed forensics → commit-msg body, from step 0)
AMEND    → amend §<S>.<n>(+): <one-line>                       (pruned-history delta → commit-msg body, from step 0)
FOLD-IN  → fold-in §V.<n>(+) and §T.<n>(+): <slug>            (omit absent sections from message)
```

**Re-entry**: any stage rewriting the delta after step 0 — concretely fold-first's fold-into reroute (new §V row → existing-row amend) — re-enters APPLY @ step 0; the rewritten delta newly satisfies the §V-row delta prune and audits that already ran saw a delta that no longer exists.

APPLY ends @ commit. `## POST-APPLY` fires after, unchanged.

## sweep-§T scope audit (pre-show-user)

every sweep-§T row (remediating §V-class violation) in delta ! task-line declare scope as grep pattern or vocab table per sweep-§T-scope invariant; named-procedure or named-site list not accepted. not pattern → bail draft w/ `sweep §T row scope ! grep pattern per sweep-§T scope rule` before show-user gate; user supplies pattern, retry audit. Mechanical pattern-match, not LLM-judgment per mechanical-not-LLM-judgment invariant.

## pinned-cite audit (pre-show-user)

Two sub-recipes — PUBLISHED-scope ban and SPEC.md-narrative §V resolution. Mechanical pattern-match, not LLM-judgment per mechanical-not-LLM-judgment invariant.

**Sub-recipe (a) — PUBLISHED-scope ban**: grep `§[VTB]\.[0-9]+` in proposed delta touching PUBLISHED scope (per scope-set invariant). Match → bail `pinned §-cite not allowed in PUBLISHED — use placeholder form (§V.<n>) or inline rule embedding` until user rewrites. not delta to PUBLISHED → sub-recipe no-op.

**Sub-recipe (b) — SPEC.md-narrative §V resolution**: grep `§V\.[0-9]+` in proposed delta touching SPEC.md narrative (§G or §C or §I or §V or §T or §B body). Pre-filter backtick-wrapped tokens `grep -v -E '`[^`]*§V\.[0-9]+[^`]*`'` (rg --pcre2 per tooling invariant) — historical-quote form per verbatim invariant is exempt. every surviving match, resolve target row against current SPEC.md §V row set (parse `^V[0-9]+:` openers in §V section). Unresolved → bail `stale §V.<n> cite in delta — row absent (likely folded); backtick-wrap historical or substitute live row` until rewrite. not delta to SPEC.md narrative → sub-recipe no-op.

Sub-recipe (a) defensive against PUBLISHED-touching deltas slipping in via spec-cmd flow — `/sdd:spec` normally writes SPEC.md only so typically no-op. Sub-recipe (b) closes post-fold authoring-time gap — fold-time sweep (compact prong-1) substitutes existing cites @ fold-commit, but new bare cites to folded-row id authored after the fold bypass until next `/sdd:check` surfaces. Pattern-match catches violations LLM prose-review missed (see §B history).

## Next-block-section audit (pre-show-user)

Audits a touched user-typeable `<plugin>/skills/<n>/SKILL.md` per skills-only architecture invariant. User-typeable test is frontmatter not `disable-model-invocation: true` and not `user-invocable: false` (skill dir name surfaces as `/<plugin>:<n>` natively unless opted out). Mechanical pattern-match, not LLM-judgment.

Recipe: every touched `<plugin>/skills/<n>/SKILL.md` in post-amend tree:
1. Read frontmatter — `rg --pcre2 -n '^(disable-model-invocation|user-invocable):\s*' <file>` over the frontmatter block.
2. Match `disable-model-invocation: true` or `user-invocable: false` → audit no-op every this file (auto-fire or programmatic-only skill, no slash-cmd surface).
3. Else (user-typeable) → grep `## OUTPUT — "Next" block` heading in post-amend target file. Match → audit no-op. not match → bail `<skill> SKILL.md lacks Next-block section per /<plugin>:<n> response-shape contract` until author adds section.

Defensive against new user-typeable skill bodies (or skill migrations across plugins) omitting the Next-block contract that sister user-typeable skills carry. V20-class runtime rule governs response shape but not enforce authoring-time presence so omission slips until `/sdd:check` surfaces (see §B history). Structurally no-op while APPLY step 4 writes SPEC.md only (mirrors pinned-cite sub-recipe (a) defensive posture) — fires only if a future mode widens the write set.

## Fold-first audit (pre-show-user)

Per fold-first authoring invariant (§V.<n>). Mechanical decision-gate, not LLM-judgment.

Recipe: every proposed new §V row in delta:

1. Identify closest existing §V row by topic — heuristic: shared scope tokens (e.g. `PUBLISHED`, `GITHUB-FACING`, `SPEC-ADJACENT`), shared procedure ref (e.g. `/sdd:spec`, `/sdd:check`), shared verb pattern (e.g. `audit`, `auto-fire`, `gate`). not closest match identifiable → skip directly to step 3 w/ "no fold candidate" note.
2. Emit AskUserQuestion per decision-gate invariant (§V.<n>):
   - **question**: `New §V row proposed: <delta one-line>. Closest existing row §V.<m>: <m-summary>. Fold into existing or split as new row?`
   - **header**: `Fold-first`
   - **options** (3 — mutually exclusive, label is action description):
     - `Fold into §V.<m>` → re-route delta as §V.<m> amend; rewrites proposed row as inline addition to existing row.
     - `New row (cite §B recurrence-class)` → proceed w/ new row, requires §B.<k> cite in delta justifying split (audit checks delta body grep `§B\.[0-9]+` post-selection).
     - `New row (orthogonal concept)` → proceed w/ new row, requires user-typed orthogonal-concept declaration recorded in commit message post-selection.
3. Selection drives next mutation per decision-gate invariant: fold-into → re-render delta as §V.<m> amend and re-enter APPLY @ step 0 per Re-entry rule (rewritten delta re-prunes and re-audits — not jump straight to show-user); new-row branches → record justification (§B cite or orthogonal declaration) and proceed to show-user.

Defensive against premature-split class — small audit or enforcement-meta additions creating new §V row when inline amend sufficed. Closes pattern-mirroring split recurrence — "mirrors §V.<n>" alone not sufficient justification per fold-first authoring invariant (§V.<n>).

## write-time prune (pre-show-user)

Per freshness-contract invariant (SPEC.md is clean current design; history in commit log + archive, not inlined). Auto-rewrite proposed delta → clean current state; pruned history routes to auto-commit message body (recoverable on-demand via code + `git log`). Show-user diff displays post-prune row so silent prune reviewed not blind. Mechanical pattern-match, not LLM-judgment.

**§V-row delta prune** (delta modifies a pre-existing §V row): strip inlined-history residue pre-show-user. Pattern set (single source per freshness-contract invariant — shared w/ /sdd:check history-residue audit and token-budget compact body-trim prong):

- amendment-counter `(∆)` markers → drop (clean current state carries no edit tally).
- dated-retirement `retired YYYY-MM-DD` clause inlined in live row → drop (wholesale-retired row is reorganize archival job, not amend residue).
- supersession-narration (`pre-amend …`, `prior … retired/dropped/superseded`) → drop.
- `Closes §B.<x>` standalone narration → fold to `(closes §B.<x>)` suffix.

Pre-filters (match exempt, not pruned): backtick-wrapped tokens per verbatim-preservation invariant (code-context pattern-definitions and quoted historical refs — a §V row whose subject is a retirement/deprecation rule not self-flag); cite-modifier `§V.<n>(∆)` (∆-on-citation marks an amended cross-ref, differs ∆-on-retired-value). Stripped content → commit-msg body per APPLY step 4 (`amend §<S>.<n>(+)` or `fold-in` message gains pruned-history block).

**§B cause trim** (delta adds or rewrites a §B `cause` cell): proposed cause cell auto-trims → one-line bug-class description pre-show-user; multi-line forensics (repro transcript, root-cause walk, commit-sha lineage) route to commit-msg body per APPLY step 4 (`backprop §B.<n>(+)` or `fold-in` message). Preview shows one-line cause so user reviews trimmed form, not raw forensics.

§T body not write-time-pruned here — /sdd:build flips status cell only per status-flip invariant so §T rows authored one-line @ creation (NEW and BACKPROP §T drafts); pre-existing §T residue owned by token-budget compact body-trim prong + /sdd:check oversized-cell advisory backstop.

## POST-APPLY

every procedure (NEW or DISTILL or BACKPROP or AMEND or FOLD-IN) post-commit ! surface `/sdd:check` as Next-block item #1 per §V.<n>; operator dispatches `/sdd:check` next turn → cascade scan over the just-applied delta. not silent commit-then-done. Recipe step ends @ commit — slash-cmd dispatch is operator turn only.

Catches the class where SPEC.md amend invalidates derivative content in `<plugin>/**` (skills, commands, READMEs) without manual audit. Next-block surfacing is baseline, not optional — operator dispatch is only path to `/sdd:check` invocation.

## OUTPUT RULES

Defer to `${CLAUDE_PLUGIN_ROOT}/SPEC-FORMAT.md` — row shape, section catalog, citation forms, header conventions.

## OUTPUT — "Next" block

Heading `## Next`; 1–5 atomic items (one sentence each, no `Reply` prefix); positional dispatch (`run <int>` or `run /<plugin>:<cmd> [args]`). Optional `## Hint` (≤ 3 lines) precedes when item selection needs hidden state. Two output moments, distinct item leads: show-user turn (diff pending) → apply and revise lead; post-commit turn → `/sdd:check` is item #1 every mode per POST-APPLY, then `/sdd:build §T.n` when a pending §T row exists.

Example @ show-user, NEW mode diff pending (Hint skipped — items self-explanatory):

```
## Next

1. accept the spec as written
2. /sdd:spec rework the V<N> invariant before building
```

Example @ show-user, AMEND mode diff pending (Hint skipped):

```
## Next

1. apply the diff to `SPEC.md`
2. revise the proposed wording
```

Example post-commit, any mode (`/sdd:check` leads per POST-APPLY):

```
## Next

1. /sdd:check — cascade scan over the just-applied delta
2. /sdd:build T<n> — start the next pending task
```

## NON-GOALS

- Writes serialize on main thread; reads may delegate to sub-agents — SPEC.md draft + apply + commit stays main-thread; BACKPROP root-cause + NEW/DISTILL code-walk reads delegable.
- No dashboards, no logs, no state files beyond SPEC.md itself.
- No auto-build after spec. User invokes build explicitly.
