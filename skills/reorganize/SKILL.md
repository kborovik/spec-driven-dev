---
name: reorganize
description: |
  SPEC.md §V cluster + renumber + cite-DAG sweep. Operator-triggered manual
  clarity-shape pass — distinct from /sdd:compact (token reduction). Triggers
  when operator invokes `/sdd:reorganize` or asks to renumber §V, regroup
  invariants by topic, or tidy §V order. Phrasings: "/sdd:reorganize",
  "reorganize the spec", "regroup §V by topic", "renumber invariants",
  "cluster §V rows", "tidy §V order", "taxonomy pass".
allowed-tools: AskUserQuestion, Read, Edit, Write, Grep, Bash(git *), Skill
model: opus
---

# reorganize — §V cluster + renumber + cite-DAG sweep

Operator-triggered clarity-shape pass over SPEC.md §V section. Cadence is at-most once per major epoch (months) — skill body documents intent, not hard /sdd:check enforcement. Single atomic commit, rollback via `git revert`.

## PREAMBLE

`/sdd:reorganize` is state-mutator scoped to SPEC.md + `.claude/spec-clusters.json` + `.claude/spec-renumber-map.json` + cite-DAG sweep targets (PUBLISHED + REPO-LOCAL + SPEC.md internal + `SPEC.archive.md` when exists). Operator invokes only — not auto-fire per recipe-step-no-dispatch rule. Owns §V renumber permission carved out of monotonic-id invariant.

Distinct concern from /sdd:compact: compact targets token reduction (folds, archives, trims); reorganize targets clarity shape (cluster + renumber). Reorganize not direct token drop; not fold rows. Writes serialize main-thread per write-serialize invariant; classification reads delegable to sub-agents.

Mutation contract is single commit per atomic-operation discipline; not partial application. Cite-DAG sweep per cite-resolution invariant runs in same commit.

## LOAD

1. Read `SPEC.md`. Missing → "no spec, nothing to reorganize." Stop.
2. Read `${CLAUDE_PLUGIN_ROOT}/SPEC-FORMAT.md` every row schema and section catalog.
3. Parse `$ARGUMENTS`:
   - empty → full cluster + renumber + sweep propose
   - `--taxonomy-only` → PROPOSE report only, not mutation (mirrors /sdd:compact `--dry-run`)
4. Discovery probe — repo-agnostic plugin scope per published-scope invariant:
   - (a) `<repo>/.claude-plugin/marketplace.json` exists → parse `plugins[].source` via `jq` (fallback `python3` per tooling-preference invariant) → derive {dir-name → plugin-name} map per plugin-name-vs-dir invariant; PUBLISHED scope is `{<dir>/**}` over each `source` value.
   - (b) else `<repo>/.claude-plugin/plugin.json` exists → single-plugin map; PUBLISHED scope is `{<repo>/**}` minus REPO-LOCAL.
   - (c) else → empty map; sweep targets REPO-LOCAL + SPEC.md internal only.
5. Persist probe — load `.claude/spec-clusters.json` if exists (cold-start vs delta-propose branch):
   - shape `[{cluster:<name>, rows:[{fingerprint:<hash>, current_id:V<n>}, ...]}, ...]`
   - per-row key is §V body-text fingerprint (sha256 over row body w/o leading `V<n>:` prefix), stable across renumber — id-as-key invalidates persist every run.
   - not exist → cold-start path.
6. Renumber-map probe — `.claude/spec-renumber-map.json` exists → load every context (chain-walk semantics on subsequent runs):
   - shape `[{run:<iso-date>, topic:<cluster>, old:V<n>, new:V<m>}, ...]` — append-only. `new` field admits sentinel `archive` is archived-terminus marker per archive-sibling schema.
   - provenance via `git log .claude/spec-renumber-map.json`, not in-file `run_sha` field.

## ARCHIVE-RETIRED

Phase fires pre-CLUSTER. Scan §V rows for body opening `retired YYYY-MM-DD` → flag for migration to `SPEC.archive.md ## §V.retired` block per archive-sibling schema. Flagged rows not enter cluster taxonomy and not consume new ids @ renumber.

1. Grep `^V[0-9]+:\s+retired\s+[0-9]{4}-[0-9]{2}-[0-9]{2}\b` in SPEC.md §V section → flagged-set (one entry per row body opening retirement-date form).
2. Citer-protection probe every flagged `V<n>` via cite-resolution invariant cite-DAG:
   - Typed columns: §T.cites and §B.fix bare-form `V<n>` token match in active SPEC.md (including closed `x` rows).
   - Free-text contexts: `§V.<n>` in §V or §C or §I body cells of active SPEC.md.
   - Backtick pre-filter `` `[^`]*(§[VTB]\.[0-9]+|\b[VTB][0-9]+\b)[^`]*` `` (rg --pcre2 per tooling-preference invariant) — historical refs in §B/§T narrative columns excluded per verbatim-preservation invariant.
3. exists live citer every any flagged row → bail `cannot archive §V.<n> — live citers: <list>` and stop. Operator resolves (fold cited content into surviving row or rewrite citer or unflag row by removing `retired` opener) pre-retry.
4. not live citers → flagged-set passes to PROPOSE (surfaced as `## To archive` block in proposal) and EXECUTE (archive write + renumber-map sentinel emission per row).

## CLUSTER

LLM judgment over each non-archived §V row body text — assign to topic-coherent cluster. ARCHIVE-RETIRED flagged rows skip cluster assignment because migrated verbatim to archive sibling @ EXECUTE. Two paths:

- **Cold-start** (not `.claude/spec-clusters.json`): propose full taxonomy from scratch. Default cluster span is 10 ids per cluster (`V<n>..V<n+9>` per range), operator-overridable @ PROPOSE.
- **Delta** (`.claude/spec-clusters.json` exists): fingerprint-match each current §V row against persist; reassign moved/new rows, retain cluster home every matched fingerprints. Emit delta-set (new rows, moved rows, dropped rows).

Cluster name is short noun phrase, topic-coherent (e.g. `spec-mutator-contract`, `audit-mechanics`, `release-flow`, `cite-resolution`). Per-row classification is LLM judgment, operator-overridable @ PROPOSE.

## PROPOSE

Render cluster diagram in steno register per github-facing-register invariant (audience is operator reviewing proposal). Form: `## <cluster-name> (V<a>..V<b>, <n> rows)` H2 per cluster containing per-row line `- V<old> → V<new>: <one-line summary>`. Trailing summary line: `<m> clusters, <total> rows, renumber map writes <k> mappings`.

When ARCHIVE-RETIRED flagged-set not empty, additionally render `## To archive` H2 block (sibling to cluster H2s) containing per-row line `- V<old>: <one-line body summary>` per flagged row. Operator sees archive set distinct from cluster set so subset-skip path informed @ CONFIRM.

Operator critiques cluster boundaries, names, row assignments. Iterate until stable (no operator delta requested). Cold-start is entire taxonomy under review; delta-run is only changed rows and new clusters under review.

`--taxonomy-only` arg → emit PROPOSE report and stop. not CONFIRM, not EXECUTE.

## CONFIRM

Emit AskUserQuestion per decision-gate invariant — single bulk-confirm covers renumber + sweep (mid-flow re-prompt not allowed per atomic-operation discipline):

- **question**: `Reorganize SPEC.md: <m> clusters, <k> id renumbers, <a> archive-retired rows, cite-DAG sweep over <s> sites. Apply?`
- **header**: `Reorganize gate`
- **options** (3, mutually exclusive, label is action description):
  - `apply renumber + cite-DAG sweep + archive-retired` → proceed to EXECUTE w/ full proposed map and archive flagged set.
  - `subset` → operator-typed cluster list or `skip archive-retired` keyword (e.g. `cite-resolution,audit-mechanics`; `skip archive-retired` retains flagged rows in active SPEC.md §V section for current run); re-render PROPOSE w/ filtered set, re-emit CONFIRM.
  - `cancel` → stop, no mutation.

## EXECUTE

Single atomic commit per atomic-operation discipline:

1. Archive-retired migration (when ARCHIVE-RETIRED flagged-set not empty and CONFIRM not `skip archive-retired`):
   - Append flagged rows verbatim to `SPEC.archive.md ## §V.retired` block per archive-sibling schema; create block if absent (sibling to `## §T TASKS` and `## §B BUGS` H2s). Each archived row preserves leading `V<orig-n>:` prefix and `retired YYYY-MM-DD — ...` body verbatim per verbatim-preservation invariant. Rows sorted by `<orig-n>` ascending.
   - Delete archived rows from active SPEC.md §V section.
   - Emit/update SPEC.md §V section archive marker `## archived: §V.retired → SPEC.archive.md (<n> retired rows)` directly under §V section heading. not id-range form because retired ids non-contiguous.
   - Per archived `V<n>`, append renumber-map entry `{run:<iso-date>, topic:'retired', old:V<n>, new:'archive'}`. Archived rows not consume new id so not paired live-renumber entry.
2. Append renumber entries → `.claude/spec-renumber-map.json` every surviving non-archived renumbered row (one entry per row, `{run:<iso-date>, topic:<cluster>, old:V<n>, new:V<m>}`). Append-only — never rewrite prior runs.
3. Rewrite SPEC.md §V section in cluster order over surviving non-archived rows: row body text preserved verbatim per verbatim-preservation invariant, only leading `V<n>:` prefix renumbered. Archived ids skipped (not live rows post-migrate).
4. Persist taxonomy → `.claude/spec-clusters.json` (overwrite w/ post-run state); rows keyed by fingerprint, `current_id` updated to `V<new>`. Archived rows not persist (terminus in archive sibling, not cluster taxonomy).
5. Cite-DAG sweep per cite-resolution invariant w/ renumber map as input:
   - Target set is PUBLISHED + REPO-LOCAL + SPEC.md internal + `SPEC.archive.md` (when exists).
   - Backtick pre-filter is `` `[^`]*(§[VTB]\.[0-9]+|\b[VTB][0-9]+\b)[^`]*` `` (rg --pcre2 per tooling-preference invariant) — excludes §B/§T narrative historical refs per verbatim-preservation invariant.
   - every surviving cite `§V.<old>` or bare `V<old>` in typed column → substitute `§V.<new>` or `V<new>` per context (live-renumber entries).
   - Archive-sentinel entries (`new:'archive'`) not trigger substitution — citer-protection gate @ ARCHIVE-RETIRED already excluded live citers so sweep encounters no live cite to flagged ids.
   - §T.cites and §B.fix typed columns contain bare-form tokens — substitute in-place.
6. Idempotent `.claude/.gitignore` probe — both `.claude/spec-clusters.json` and `.claude/spec-renumber-map.json` not in gitignore (git-tracked per scope-set invariant); not guard add.
7. `git add SPEC.md SPEC.archive.md .claude/spec-clusters.json .claude/spec-renumber-map.json` + touched cite-sweep sites (SPEC.archive.md staged when archive-retired fired or pre-existing); auto-commit msg `reorganize SPEC.md §V: <m> clusters, <k> renumbers, <a> archive-retired`; not user prompt for commit step.

EXECUTE ends @ commit. Rollback is `git revert <reorganize-sha>` per single-commit shape. Drift cascade surfaces as Next-block item per response-shape invariant — operator dispatches next turn.

## CHAIN-WALK SEMANTICS

`.claude/spec-renumber-map.json` is append-only history of all runs. Stacked runs admit duplicate `old:` keys: run-1 entry `{old:V<a>, new:V<b>}`, run-2 entry `{old:V<b>, new:V<c>}` → historical-id `V<a>` resolves via newest-first walk `V<a> → V<b> → V<c>` (terminating when not further `old:V<n>` match for current target).

Sentinel `archive` in `new` field is archived-terminus marker per archive-sibling schema — chain-walk lookup landing on `archive` sentinel emits `archived → SPEC.archive.md ## §V.retired V<n>` and not resolves to live row. Distinct terminus from "no further mapping" (current live id) so consumers distinguish active rename chain from archive migration.

Chain-walk consumers is reorganize itself (re-running w/ persisted map containing prior entries) and explain skill LOAD (historical-id resolution against current SPEC.md). Both walk newest-first per persisted-map ordering — read-only consumption preserves cite-resolution invariant.

## OUTPUT — "Next" block

Heading `## Next`; 1–5 atomic items (one sentence each, not `Reply` prefix); positional dispatch (`run <int>` or `run /<plugin>:<cmd> [args]`). Optional `## Hint` (≤ 3 lines) precedes when item selection needs hidden state. reorganize is state-mutator so post-EXECUTE prefer follow-up /sdd:check (confirm cite-DAG and format-layer clean post-renumber).

Example after EXECUTE (renumber + cite-DAG sweep applied; commit auto-fired):

```
## Next

1. /sdd:check — cascade scan over reorganized SPEC.md
2. /sdd:build --next — start the next pending §T row
3. git revert <reorganize-sha> — rollback if renumber breaks downstream
```

Variants: `--taxonomy-only` exit (not commit) → swap item 1 for `/sdd:reorganize` (apply for real) and drop item 3; CONFIRM cancel → swap item 1 for `/sdd:reorganize --taxonomy-only` (re-propose w/ filter) and drop item 3.

## NON-GOALS

- not auto-fire — operator-triggered only per recipe-step-no-dispatch rule.
- not partial commit — single atomic commit per atomic-operation discipline.
- not token reduction — clarity-shape pass only; token reduction routes through /sdd:compact.
- not row folds — reorganize preserves row body content (collapse N rows into one belongs to /sdd:compact prong 1). ARCHIVE-RETIRED migrates retired rows verbatim to archive sibling so row count drops, body content not collapsed.
- not cadence enforcement in /sdd:check — skill body documents intent only.
- not hardcoded plugin dir names — discovery probe drives PUBLISHED scope per plugin-name-vs-dir invariant.
