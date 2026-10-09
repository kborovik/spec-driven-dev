---
name: condense
description: |
  SPEC.md condenser — token-budget sweep.
  Triggers when user invokes `/sdd:condense` or asks to condense spec or /sdd:check
  emits `## advisory` token-budget overflow line. Phrasings: "/sdd:condense",
  "condense SPEC.md", "SPEC too big", "shrink the spec", "token budget".
allowed-tools: AskUserQuestion, Read, Edit, Write, Bash(git *), Bash(python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-mechanical.py *), Agent, Skill(sdd:*), TaskCreate, TaskUpdate
---

# condense — SPEC.md condenser

Operator-triggered six-prong sweep.
Scope: SPEC.md + `SPEC.archive.md` + `.spec/check-extras.md`.
Not auto-fire — /sdd:check emits advisory when token estimate > 20k; operator invokes next turn.
Single atomic commit (all firing prongs or none); rollback `git revert`.
Writes serialize main-thread; per-prong scan reads delegable to sub-agents.

## PROGRESS

Phases: LOAD, PROPOSE (six-prong scan), CONFIRM, EXECUTE.
Per `${CLAUDE_SKILL_DIR}/../_fragments/PROGRESS.md` (TaskCreate, TaskUpdate).
CONFIRM cancel / subset-skip → unreached phases `deleted`, not `completed`.

## LOAD

1. Read `SPEC.md`.
   Missing → "no spec, nothing to condense."
   Stop.
2. Read `${CLAUDE_PLUGIN_ROOT}/SPEC-FORMAT.md` — row schema + section catalog.
3. Baseline tokens = bytes / `check-mechanical.py` `TOKEN_RATIO` (single source; not hardcode divisor).
   Record.

## PROPOSE

Six prongs, execution order 1 → 6.
Per prong: scan SPEC.md for trigger match; emit firing-set + skip-set w/ 1-line rationale each.

One script call: `python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-mechanical.py emit-condense-propose`; exact script-path grant pin via `${CLAUDE_SKILL_DIR}` frontmatter substitution (script-sole use, same variable in grant + body cmd) per tooling-preference invariant.
Emit labeled tables (`## fold-seeds`, `## superseded`, `## archive-window`, `## residue`, `## v-weights`) with columns unchanged vs standalone modes.
Consume this emit — never five separate emit-* calls.

### Prong 1 — §V fold-first sweep

Fold pattern-mirrored sibling §V rows into target row inline.
Seed = `## fold-seeds` table (`cluster_members|co_citers`) — connected components of live §V rows sharing a citer (§T `cites` or §B `fix` naming ≥ 2 live §V rows).
Seed advisory not auto-apply: co-citation is candidacy signal not proof; operator confirms each fold @ CONFIRM (LLM judges topic coherence).
Augment seed w/ topic-keyword overlap (shared scope tokens / procedure refs / verb pattern) where co-citation thin.
Fires first — fold reshapes later prongs (prong 6 re-runs weights after fold when this prong fires).

### Prong 2 — SUPERSEDED §T inline marker

Candidates = `## superseded` table (`tid|superseded_v|original_cites`) — closed §T (status `x`) whose §V cite resolves into no live §V row (only archived §V.retired block or nowhere) → SUPERSEDED candidate.
Live-only resolution — distinct from cite-DAG audit live+archive scope.
Consume table; not by-hand per-cite resolution.
Operator confirms each (content-amend-away not cite-detectable).
Replace task body wholesale: `T<n>|x|SUPERSEDED — §V.<m> amend|<original cites>`.
Preserves row id; closes cite-DAG-miss audit noise.

### Prong 3 — §T/§B window-vs-archive split

Candidates = `## archive-window` table (`action|tid_lo|tid_hi|count|marker`) — closed §T (status `x`) vs `ARCHIVE_CLOSED_T` (single source; not hardcode).
`skip` action → prong 3 skip (no archive).
`archive` + `keep` rows → keep newest N closed live, archive older closed id-asc; `marker` cell is the SPEC-FORMAT §T archive-marker H2.
Consume table only; not hand-count closed §T.
On archive: older closed rows → `SPEC.archive.md` (repo-root sibling, committed, id ascending). §T/§B gain per-section marker from table (form `## archived: §<S>.<a>..§<S>.<b> → SPEC.archive.md (<n> rows)`).
Archive carries verbatim row text. /sdd:check cite-DAG sweep eager-probes archive; archived rows stable so memo HOLD-SINCE-CLEAN across runs.

### Prong 4 — history-residue prune

Prune history residue across live §V/§T/§B row bodies — SPEC.md is clean current design; history lives in commit log + archive.
Candidates = `## residue` table (`section|id|pattern|line`) — every live row hit by the script-owned `PRUNE_PATTERNS` set or oversized §T `task` / §B `cause` cells (`oversized-cell`), after the same pre-filters as the audit path.
Empty body (header only) → prong 4 skip.
Consume table; not hand regex / per-run pattern paraphrase (freshness-contract + mechanical-realization invariants — single source with `audit_history_residue`).
Per-hit action = `action` cell of the matching `emit-prune-patterns` row (`id|role|pattern|action`): `residue` → drop (commit msg + `§B.cause`/`§T.cites` cite-DAG preserve narrative); `fold` → apply fold action; `pre-filter` → exempt.
`oversized-cell` → §T body-trim / §B cause one-line trim (surplus → commit-msg body).

**§T body-trim** — owned here because /sdd:build flips status cell only, so §T body not reachable by /sdd:spec write-time prune: oversized `task` cell carrying step-by-step transcript → one-line goal; surplus → commit-msg body.
Mirrors §B `cause` one-line trim.

Verbatim-preservation holds: code, paths, URLs, identifiers, error strings, regex.

### Prong 5 — §V prose → telegraph rewrite

Rewrite embedded English connectives per telegraph skill.
Targets: `Why:`, `For example`, `In other words`, explanatory `because` / `due to` clauses.
Verbatim-preservation holds: code, paths, URLs, identifiers, numbers, versions, error strings, SQL, regex, JSON, YAML, quoted strings.

### Prong 6 — §V audit-recipe extraction

Heavy set = `## v-weights` table (`v_row|bytes|tokens|cum_pct|heavy`), heaviest first.
Prong 1 fired → re-run `python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-mechanical.py emit-v-weights` post-fold and consume that table; else consume the `## v-weights` table from PROPOSE.
Consume stub-skip from table: extract `heavy=yes` only; `heavy=no` (already-stubbed `→ .spec/check-extras.md §V<n>` rows) → no re-extract.
Not by inspection.
Not a second stub-detect pass — the table owns stub-skip.
Heavy rows: extract audit-recipe content → `.spec/check-extras.md` (REPO-LOCAL extension); SPEC.md row keeps 1-line ref.
Check skill loader already path-probes `.spec/check-extras.md` — no check-skill amend.

## CONFIRM

Always fires post-PROPOSE.
Single bulk AskUserQuestion covers full sweep — mid-flow re-prompt not allowed:

- **question**: `Condense SPEC.md: prongs {<firing-set>} firing, {<skip-set>} skipped. Baseline ~<n>k tokens, est. ~<m>k post-sweep. Apply?`
- **header**: `Condense gate`
- **options** (4, mutually exclusive, label is action description):
  - `apply all firing prongs` → EXECUTE full firing set.
  - `force-skip prong 3` → EXECUTE minus prong 3 (archive split deferred; prong 3 load-bearing so explicit override).
  - `subset` → user supplies N in {1..6} via Other-typed input; EXECUTE prong N only.
  - `cancel` → no mutation; PROPOSE report retained as final output.

## EXECUTE

Single atomic commit:

1. Apply firing prongs in order (1 → 6 minus skips).
2. Prong 3 fired → `git add SPEC.archive.md`.
3. Prong 6 fired → `git add .spec/check-extras.md`.
4. Prong 1 fired → cite-DAG sweep same commit; touch REPO-LOCAL citers renumbered by fold.
5. Stage remaining artifacts + `SPEC.md` (`git add`), then path-scoped commit per `${CLAUDE_SKILL_DIR}/../_fragments/PATH-SCOPED-COMMIT.md`: `git commit -m <subject> -- <staged artifacts> SPEC.md`; auto-commit msg `condense SPEC.md: prongs {<firing-set>} (~<n>k → ~<m>k tokens)`; no user prompt.

EXECUTE ends @ commit.
Rollback `git revert <condense-sha>`.
Drift cascade → Next-block item #1; operator dispatches next turn.

## MECHANIZE

Load `${CLAUDE_SKILL_DIR}/../_fragments/MECHANIZE.md`.

## OUTPUT — "Next" block

Per `${CLAUDE_SKILL_DIR}/../_fragments/NEXT.md`.
State-mutator → post-EXECUTE prefer `/sdd:check` (confirm cite-DAG + format-layer + token-budget clean).
CONFIRM cancel (no commit) → `/sdd:condense` re-run; drop revert item.
CONFIRM subset → Next-block unchanged.

## NON-GOALS

- not auto-fire — /sdd:check emits advisory; operator invokes /sdd:condense next turn.
- not partial commit — the confirmed prong set applies in one commit or not at all; CONFIRM may narrow that set (force-skip, subset), never split the commit.
- not retune thresholds (`TOKEN_BUDGET` 20k-token advisory, `ARCHIVE_CLOSED_T` closed-§T archive trigger) in this skill body — canonical values live in the token-budget invariant row (SPEC.md) w/ mechanical mirrors in `check-mechanical.py` constants; retune via /sdd:spec AMEND + sync the script constant same commit.
