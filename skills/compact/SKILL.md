---
name: compact
description: |
  SPEC.md compactor — token-budget sweep.
  Triggers when user invokes `/sdd:compact` or asks to compact spec or /sdd:check
  emits `## advisory` token-budget overflow line. Phrasings: "/sdd:compact",
  "compact SPEC.md", "SPEC too big", "shrink the spec", "token budget".
allowed-tools: AskUserQuestion, Read, Edit, Write, Bash(git *), Skill
model: sonnet
---

# compact — SPEC.md compactor

Operator-triggered six-prong sweep. Scope: SPEC.md + `SPEC.archive.md` + `.claude/check-extras.md`. Not auto-fire — /sdd:check emits advisory when token estimate > 25k; operator invokes next turn. Single atomic commit (all firing prongs or none); rollback `git revert`. Writes serialize main-thread; per-prong scan reads delegable to sub-agents.

## LOAD

1. Read `SPEC.md`. Missing → "no spec, nothing to compact." Stop.
2. Read `${CLAUDE_PLUGIN_ROOT}/SPEC-FORMAT.md` — row schema + section catalog.
3. Baseline tokens = bytes / `check-mechanical.py` `TOKEN_RATIO` (single source; not hardcode divisor). Record.

## PROPOSE

Six prongs, execution order 1 → 6. Per prong: scan SPEC.md for trigger match; emit firing-set + skip-set w/ 1-line rationale each.

### Prong 1 — §V fold-first sweep

Fold pattern-mirrored sibling §V rows into target row inline. Seed script-computed: `check-mechanical.py emit-fold-seeds` emits `cluster_members|co_citers` table — connected components of live §V rows sharing a citer (§T `cites` or §B `fix` naming ≥ 2 live §V rows). Seed advisory not auto-apply: co-citation is candidacy signal not proof; operator confirms each fold @ CONFIRM (LLM judges topic coherence). Augment seed w/ topic-keyword overlap (shared scope tokens / procedure refs / verb pattern) where co-citation thin. Fires first — fold reshapes later prongs (prong 6 inherits folded shape).

### Prong 2 — SUPERSEDED §T inline marker

Candidates script-computed: `check-mechanical.py emit-superseded` emits `tid|superseded_v|original_cites` table — closed §T (status `x`) whose §V cite resolves into no live §V row (only archived §V.retired block or nowhere) → SUPERSEDED candidate. Live-only resolution — distinct from cite-DAG audit live+archive scope. Consume table; not by-hand per-cite resolution. Operator confirms each (content-amend-away not cite-detectable). Replace task body wholesale: `T<n>|x|SUPERSEDED — §V.<m> amend|<original cites>`. Preserves row id; closes cite-DAG-miss audit noise.

### Prong 3 — §T/§B window-vs-archive split

Trigger: closed §T rows > 50. Older closed rows → `SPEC.archive.md` (repo-root sibling, committed, id ascending). §T/§B gain per-section marker `## archived: §<S>.<a>..§<S>.<b> → SPEC.archive.md (<n> rows)`. Archive carries verbatim row text. /sdd:check cite-DAG sweep eager-probes archive; archived rows stable so memo HOLD-SINCE-CLEAN across runs.

### Prong 4 — history-residue prune

Prune history residue across live §V/§T/§B row bodies — SPEC.md is clean current design; history lives in commit log + archive. Pattern set single-sourced by freshness-contract invariant (shared w/ /sdd:check audit + /sdd:spec write-time prune):

- amendment-counter `(∆)` markers → drop.
- `retired YYYY-MM-DD` clause inlined in live row → drop (wholesale-retired row is reorganize archival job).
- supersession-narration → drop: `pre-amend …`, `prior … retired/dropped/superseded`, recurrence-class lineage, surfaced-by prose. Commit msg + `§B.cause`/`§T.cites` cite-DAG preserve narrative.
- standalone `Closes §B.<x>` sentence → `(closes §B.<x>)` suffix on prior clause.

**§T body-trim** — owned here because /sdd:build flips status cell only, so §T body not reachable by /sdd:spec write-time prune: oversized `task` cell carrying step-by-step transcript → one-line goal; surplus → commit-msg body. Mirrors §B `cause` one-line trim.

Pre-filters (match exempt): backtick-wrapped tokens (pattern-definition rows not self-flag); cite-modifier `§V.<n>(∆)`; wholesale-retired `V<n>: retired YYYY-MM-DD` rows pending reorganize. Verbatim-preservation holds: code, paths, URLs, identifiers, error strings, regex.

### Prong 5 — §V prose → telegraph rewrite

Rewrite embedded English connectives per telegraph skill. Targets: `Why:`, `For example`, `In other words`, explanatory `because` / `due to` clauses. Verbatim-preservation holds: code, paths, URLs, identifiers, numbers, versions, error strings, SQL, regex, JSON, YAML, quoted strings.

### Prong 6 — §V audit-recipe extraction

Heavy set script-computed: `check-mechanical.py emit-v-weights` emits `v_row|bytes|tokens|cum_pct|heavy` table, heaviest first; heavy = top rows whose cumulative weight first reaches ≥ 50% of §V-section total (tie-break descending weight then ascending id — run-stable). Not by inspection. Heavy rows: extract audit-recipe content → `.claude/check-extras.md` (REPO-LOCAL extension); SPEC.md row keeps 1-line ref. Check skill loader already path-probes `.claude/check-extras.md` — no check-skill amend.

## CONFIRM

Always fires post-PROPOSE. Single bulk AskUserQuestion covers full sweep — mid-flow re-prompt not allowed:

- **question**: `Compact SPEC.md: prongs {<firing-set>} firing, {<skip-set>} skipped. Baseline ~<n>k tokens, est. ~<m>k post-sweep. Apply?`
- **header**: `Compact gate`
- **options** (4, mutually exclusive, label is action description):
  - `apply all firing prongs` → EXECUTE full firing set.
  - `force-skip prong 3` → EXECUTE minus prong 3 (archive split deferred; prong 3 load-bearing so explicit override).
  - `subset` → user supplies N in {1..6} via Other-typed input; EXECUTE prong N only.
  - `cancel` → no mutation; PROPOSE report retained as final output.

## EXECUTE

Single atomic commit:

1. Apply firing prongs in order (1 → 6 minus skips).
2. Prong 3 fired → `git add SPEC.archive.md`.
3. Prong 6 fired → `git add .claude/check-extras.md`.
4. Prong 1 fired → cite-DAG sweep same commit; touch REPO-LOCAL citers renumbered by fold.
5. `git add` artifacts + `SPEC.md`; auto-commit msg `compact SPEC.md: prongs {<firing-set>} (~<n>k → ~<m>k tokens)`; no user prompt.

EXECUTE ends @ commit. Rollback `git revert <compact-sha>`. Drift cascade → Next-block item #1; operator dispatches next turn.

## OUTPUT — "Next" block

Heading `## Next`; 1–5 atomic items (one sentence each, no `Reply` prefix); positional dispatch (`run <int>` or `run /<plugin>:<cmd> [args]`). Optional `## Hint` (≤ 3 lines) precedes when item selection needs hidden state. State-mutator → post-EXECUTE prefer `/sdd:check` (confirm cite-DAG + format-layer + token-budget clean).

Example after EXECUTE (firing-set {1,2,3,4,5}; commit auto-fired):

```
## Next

1. /sdd:check — cascade scan over compacted SPEC.md
2. /sdd:build --next — start the next pending §T row
3. git revert <compact-sha> — rollback if compaction breaks downstream
```

Variants: CONFIRM cancel (no commit) → swap item 1 for `/sdd:compact` (re-run to apply after spec review), drop item 3. CONFIRM subset → Next-block unchanged.

## NON-GOALS

- not auto-fire — /sdd:check emits advisory; operator invokes /sdd:compact next turn.
- not partial commit — every firing prong applies or none.
- not retune thresholds (25k advisory, 20k window, > 50 closed-§T archive trigger) in this skill body — values live in token-budget-compact invariant row, retunable via /sdd:spec AMEND only.
