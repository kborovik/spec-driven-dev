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

Operator-triggered six-prong sweep. Single atomic commit, rollback via `git revert`.

## PREAMBLE

`/sdd:compact` is state-mutator scoped to SPEC.md + `SPEC.archive.md` + `.claude/check-extras.md`. not auto-fire per recipe-step-no-dispatch rule — operator invokes only; advisory surfaces in /sdd:check final-output when `check-mechanical.py` token estimate (`bytes/3.4` per token-budget-compact invariant) > 25k threshold. Writes serialize main-thread; per-prong scan reads delegable to sub-agents per write-serialize invariant. Mutation contract is single commit per atomic-operation discipline; not partial application.

## LOAD

1. Read `SPEC.md`. Missing → "no spec, nothing to compact." Stop.
2. Read `${CLAUDE_PLUGIN_ROOT}/SPEC-FORMAT.md` every row schema and section catalog.
3. Compute baseline `tokens ~ bytes/3.4` per token-budget-compact invariant (single source is `check-mechanical.py` `TOKEN_RATIO` per mechanical-realization invariant; not hardcode divisor). Record.

## PROPOSE

Six prongs in execution order 1 → 2 → 3 → 4 → 5 → 6 (prong number is execution order per token-budget-compact invariant). Per-prong fire decision: scan SPEC.md every trigger match, emit firing-set + skip-set w/ per-prong rationale 1-liner.

### Prong 1 — §V fold-first sweep

Cluster pattern-mirrored sibling §V rows per fold-first-authoring invariant. Co-citation seed script-computed per mechanical-realization invariant — `check-mechanical.py emit-fold-seeds` emits clusters of live §V rows sharing a citer (a §T whose `cites` or a §B whose `fix` names ≥ 2 live §V rows), connected-component over the co-citation graph, as a `cluster_members|co_citers` table. Seed is advisory not auto-apply — operator confirms each fold @ CONFIRM gate per fold-first-authoring invariant (LLM judgment over topic coherence; co-citation is candidacy signal not proof). Augment seed w/ topic-keyword overlap (shared scope tokens, shared procedure refs, shared verb pattern) where co-citation thin. Emit candidate clusters {target-§V, sibling-§V, …} → fold sibling body into target as inline addition. Fires first because structural fold-in re-shapes subsequent prongs (audit-recipe extraction in prong 6 inherits folded shape).

### Prong 2 — SUPERSEDED §T inline marker

Candidate set script-computed per mechanical-realization invariant — `check-mechanical.py emit-superseded` resolves each closed §T's (status `x`) §V cites against LIVE §V rows only; a cite absent from live §V (resolving only into the archived §V.retired block or nowhere) → SUPERSEDED candidate (cited §V amended away or folded). Live-only resolution, distinct from cite-DAG audit live+archive scope (where an archived cite holds resolved). Consume the emitted `tid|superseded_v|original_cites` table not by-hand per-cite resolution. Operator confirms each because content-amend-away not cite-detectable. Replace task body wholesale w/ `T<n>|x|SUPERSEDED — §V.<m> amend|<original cites>`. Preserves row id (monotonic-numbering invariant) and closes cite-DAG-miss audit noise.

### Prong 3 — §T and §B window-vs-archive split

Trigger is closed §T row count > 50 (load-bearing — hardcoded in token-budget-compact invariant body, retunable via /sdd:spec AMEND). Older closed rows → `SPEC.archive.md` (repo-root sibling, committed to git, sorted by id ascending per archive-schema invariant). SPEC.md §T and §B sections gain per-section marker `## archived: §<S>.<a>..§<S>.<b> → SPEC.archive.md (<n> rows)`. Archive carries verbatim row text per verbatim-preservation invariant. Eager-probed by /sdd:check cite-DAG sweep per memo invariant — archived rows in stable set so memo HOLD-SINCE-CLEAN across runs.

### Prong 4 — history-residue prune

Generalizes prior §V tail-trim → full history-residue prune across live §V/§T/§B row bodies per freshness-contract invariant (SPEC.md is clean current design; history in commit log + archive, not inlined). Pattern set single-sourced by freshness-contract invariant (shared w/ /sdd:check history-residue audit and /sdd:spec write-time prune):

- amendment-counter `(∆)` markers → drop (clean current state carries no edit tally).
- dated-retirement `retired YYYY-MM-DD` clause inlined in live row → drop (wholesale-retired row is reorganize archival job).
- supersession-narration → drop — `pre-amend …`, `prior … retired/dropped/superseded`, recurrence-class lineage (e.g. `Recurrence-class extension of §B.<x>`), surfaced-by prose (e.g. `surfaced by /sdd:check`); commit message and `§B.cause` + `§T.cites` cite-DAG preserve narrative.
- `Closes §B.<x>` standalone sentence → fold to `(closes §B.<x>)` suffix on prior clause.

**§T body-trim** — closed-task implementation-transcript residue owned here because /sdd:build flips status cell only per status-flip invariant so §T body not reachable by /sdd:spec write-time prune (status-flip path skips §T body): oversized `task` cell carrying step-by-step transcript → one-line goal; surplus detail → commit-msg body. Mirrors §B `cause` one-line trim.

Pre-filters (match exempt, not pruned): backtick-wrapped tokens per verbatim-preservation invariant (code-context pattern-definitions and quoted historical refs — rows documenting these patterns not self-flag); cite-modifier `§V.<n>(∆)` (∆-on-citation differs ∆-on-retired-value); wholesale-retired §V row `V<n>: retired YYYY-MM-DD` pending reorganize archival. Mechanical pattern-match per telegraph register; verbatim-preservation invariant preserves code blocks, paths, URLs, identifiers, error strings, regex.

### Prong 5 — §V prose → telegraph rewrite

Embedded English connectives rewrite per telegraph encoding (per telegraph skill). Pattern targets: `Why:` or `For example` or `In other words` or explanatory `because` or `due to` clauses. Verbatim-preservation invariant honored — code blocks, paths, URLs, identifiers, numbers, versions, error strings, SQL, regex, JSON, YAML, quoted strings preserved.

### Prong 6 — §V audit-recipe extraction

Heavy §V row set script-computed per mechanical-realization invariant — `check-mechanical.py emit-v-weights` ranks per-§V-row byte/token weight (`v_row|bytes|tokens|cum_pct|heavy` table, heaviest first) and flags the heavy set is top rows whose cumulative weight first reaches ≥ 50% §V-section total (stable tie-break descending weight then ascending id so run-stable) — not by inspection. Heavy-flagged rows extract audit-recipe content → `.claude/check-extras.md` per parametric-recipe invariant (REPO-LOCAL extension). SPEC.md §V row retains 1-line ref pointing at REPO-LOCAL extension recipe. Loader recipe in check skill body already path-probes `.claude/check-extras.md` so not check-skill amend required.

## CONFIRM

Always fires post-PROPOSE. Emit AskUserQuestion per decision-gate invariant — single bulk-confirm covers full sweep (mid-flow re-prompt not allowed per atomic-operation discipline):

- **question**: `Compact SPEC.md: prongs {<firing-set>} firing, {<skip-set>} skipped. Baseline ~<n>k tokens, est. ~<m>k post-sweep. Apply?`
- **header**: `Compact gate`
- **options** (4, mutually exclusive, label is action description):
  - `apply all firing prongs` → EXECUTE w/ full firing set.
  - `force-skip prong 3` → EXECUTE w/ prongs minus 3 (archive split deferred; prong 3 load-bearing per token-budget invariant so explicit override).
  - `subset` → single-prong path; user supplies N in {1, 2, 3, 4, 5, 6} via Other-typed input; EXECUTE prong N only.
  - `cancel` → propose-only path; stop, not mutation; PROPOSE report retained as final output.

## EXECUTE

Single atomic commit per atomic-operation discipline:

1. Apply firing-set prongs in execution order (1 → 2 → 3 → 4 → 5 → 6 minus skip).
2. Prong 3 fire → `git add SPEC.archive.md` alongside `SPEC.md`.
3. Prong 6 fire → `git add .claude/check-extras.md` alongside.
4. Prong 1 fire → cite-DAG sweep in same commit per cite-resolution invariant; touch citers in REPO-LOCAL renumbered by fold.
5. `git add` artifacts + `SPEC.md`; auto-commit msg `compact SPEC.md: prongs {<firing-set>} (~<n>k → ~<m>k tokens)`; not user prompt for commit step.

EXECUTE ends @ commit. Rollback is `git revert <compact-sha>` per single-commit shape. Drift cascade surfaces as Next-block item #1 per response-shape invariant — operator dispatches next turn.

## OUTPUT — "Next" block

Heading `## Next`; 1–5 atomic items (one sentence each, not `Reply` prefix); positional dispatch (`run <int>` or `run /<plugin>:<cmd> [args]`). Optional `## Hint` (≤ 3 lines) precedes when item selection needs hidden state. compact is state-mutator so post-EXECUTE prefer `/sdd:check` (confirm cite-DAG and format-layer and token-budget clean post-sweep).

Example after EXECUTE (firing-set {1,2,3,4,5}; commit auto-fired):

```
## Next

1. /sdd:check — cascade scan over compacted SPEC.md
2. /sdd:build --next — start the next pending §T row
3. git revert <compact-sha> — rollback if compaction breaks downstream
```

Variants: CONFIRM cancel (propose-only exit, not commit) → swap item 1 for `/sdd:compact` (re-run to apply after spec review) and drop item 3 (not commit to revert); CONFIRM subset (single-prong commit) → Next-block unchanged.

## NON-GOALS

- not auto-fire — operator-triggered only per recipe-step-no-dispatch rule. /sdd:check emits advisory; operator invokes /sdd:compact next turn.
- not partial commit — single atomic commit per atomic-operation discipline; every firing prong applies or none applies.
- not retune thresholds (25k advisory, 20k window, > 50 closed §T archive trigger) in this skill body — values live in token-budget-compact invariant row, retunable via /sdd:spec AMEND only.
