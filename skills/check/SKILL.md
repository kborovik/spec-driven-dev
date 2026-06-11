---
name: check
description: |
  Read-only drift detector. Diffs SPEC.md vs current code and reports violations
  grouped by severity. not writes — suggests remedies via spec or build skills,
  not invokes them. Triggers when user asks to check drift, audit spec, verify
  invariants, or ask if code still matches invariants. Phrasings: "check drift",
  "audit the spec", "does the code still match invariants", "check invariants",
  "spec vs code", "is the spec still accurate?", "did the code drift?".
allowed-tools: Read, Grep, Glob, Bash(git *), Bash(python3 *), Skill
model: sonnet
---

# check — drift report

Pure diagnostic. Reports violations. Writes nothing to SPEC or code. User decides remedy.

## PREAMBLE

`/sdd:check` is read-only per read-only-cmd invariant; memo + `.gitignore` guard writes in REPO-LOCAL `.claude/` per scope-set invariant so sibling state not SPEC or code not violate read-only contract. Sub-agent delegation allowed throughout (check is read-only so not coordination hazard). The mechanical audit set is deterministic so delegated to a published script per the mechanical-realization invariant — the skill body never re-derives those greps per run. Recipes parametric per parametric-recipe invariant — repo-specific extensions load via the script's `.claude/scripts/check-extras.sh` hook probe and the LLM consults `.claude/check-extras.md` judgment-class extras. Following sections defer to this preamble; defensive re-justification omitted.

## LOAD

1. Read `SPEC.md`. If missing → "no spec, nothing to check." Stop.
2. Parse invocation args (two-option surface per dispatch invariant):
   - bare (no args) → memo-driven default sweep covering invariants + interfaces + tasks; first-run (memo absent or invalidated) degrades to full re-classify and writes fresh memo on clean.
   - `--full` → delete `.claude/check-state.json` upfront → run full sweep and write fresh memo on clean and propagate `--full` to mechanical audit script → per-row history listing (skip body-row aggregation per drift-verdict-vocab invariant). Mid-run interrupt not memo so next run also full — safe failure mode for " not trust cache".
   - Unknown arg → bail w/ `unknown arg <arg> — accepted forms: bare invocation, --full`. Legacy section-name args and legacy multi-flag forms (retired per dispatch invariant) not admitted.
3. Run the mechanical audit script (MECHANICAL CORE below) at audit start — its `memo|ADVISORY|…` rows report any fired invalidation trigger and the per-row `v_row_shas` dirty set that scopes §V re-classification.
4. §V row bodies for classification is sourced via the script's `emit-v-slices` mode (see SCOPE), not whole-file `SPEC.md` Read — large SPEC > Read token cap so full-file Read paginates; the script slice is canonical §V-body source every single-agent narrow-scope and sub-agent batch paths per the batch invariant.

## MECHANICAL CORE — audit script

The mechanical audit set — SPEC-FORMAT structural rules (section catalog + order, row grammar, rightmost-`|` column extraction, archive markers + sibling shape), `§T` cites / `§B` fix grammar, monotonic-ID, cite-DAG resolution + edge-type, history-residue patterns + pre-filters + oversized-cell advisory, pinned-invariant-header grep, memo bookkeeping (sha / rev-parse), token estimate — is deterministic so owned by `${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py` per the mechanical-realization invariant. not re-derived as per-run LLM greps; the script's regex is single source of truth every these audits (mirrors the canonical-agent-block verbatim contract — per-run paraphrase not permitted).

Run at audit start (body-level `${CLAUDE_PLUGIN_ROOT}` expansion; the variable not valid in frontmatter `allowed-tools` patterns so frontmatter grants broad `Bash(python3 *)`):

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py audit [--full]
```

`--full` propagates from LOAD step 2 user invocation → restores per-row history listing (skip body-row aggregation per drift-verdict-vocab invariant); bare invocation aggregates per section above threshold.

Reads `SPEC.md` (+ `SPEC.archive.md` sibling if exists) from cwd; discovers PUBLISHED scope from `.claude-plugin/marketplace.json` (parametric per parametric-recipe invariant); probes REPO-LOCAL `.claude/scripts/check-extras.sh` hook (exists and executable → run, append its `id|verdict|evidence` rows — language-agnostic contract per parametric-recipe invariant). Emits the standardized pipe-table `id|verdict|evidence`:

- `format|VIOLATE|format: <detail>` — SPEC-FORMAT rule breach (evidence prefix `format:`).
- `cite|UNRESOLVED|<citer> <id> …` or `cite|TYPE-MISMATCH|…` — cite-DAG resolution + edge-type. `cite|ambiguous|…` is bare-form phase-label / gate-ID collision subset (consumers admitting bare-form REPO-LOCAL scope) → LLM adjudicates per CHECK §-cite; none every this repo's typed-prefix-only scope.
- `history|VIOLATE|<row> … history: <pattern>` — inlined-history residue (evidence prefix `history:`). `history|ADVISORY|oversized cells …` is smell, not VIOLATE.
- `pinned-header|VIOLATE|<file:line> …` — PUBLISHED body pins invariant number in header.
- `token|ADVISORY|SPEC.md ~<n>k tokens > budget …` — token estimate (`bytes/3.4`) per token-budget invariant.
- `memo|ADVISORY|<trigger>` — memo invalidation (`schema_version` mismatch or `last_clean_sha` unreachable → drop memo, full sweep) or scope feed `v_row_shas drift: V<n>,…` (per-row drift → re-classify named §V rows only — comma-joined field, not prose).
- `tasks|ADVISORY|flipped-since-clean: T<n>,…` — §T rows flipped `.`→`x` since the memo clean sha (machine-side scope feed; empty field when none).
- `diff|ADVISORY|touched: <paths>` — paths changed since the memo clean sha (machine-side scope feed; comma-joined).

Main thread merges this table into REPORT verbatim — `format` / `history` / `cite` / `pinned-header` rows fold into their REPORT blocks, `token` / `memo`-invalidation rows into `## advisory`. The scope-feed rows (`memo` `v_row_shas drift`, `tasks` flipped-set, `diff` touched-set) carry stable comma-joined fields (not surrounding prose) so feed SCOPE machine-side — chained into `emit-v-slices --dirty`, not surfaced in the `## advisory` block, not hand-rolled via `git diff`.

## MEMO

`.claude/check-state.json` is persistent memo (REPO-LOCAL cache, not source of truth — code and SPEC.md is truth). Schema v3:

```json
{
  "schema_version": 3,
  "last_clean_sha": "<git HEAD @ last clean run>",
  "v_row_shas": { "V<n>": "<sha256 of §V row body>" },
  "last_run_at": "<ISO-8601 timestamp>",
  "last_v_classifications": { "V<n>": "HOLD|HOLD-SINCE-CLEAN|SCOPE-EMPTY|VIOLATE-CAPTURED|LATENT" },
  "oversized_cell_ack": "<sha256 over sorted oversized cell-id set>"
}
```

Script owns both ends per the memo invariant:

- **read** — `audit` mode emits `memo|ADVISORY|…` rows every fired invalidation trigger: `schema_version` differs current or `last_clean_sha` unreachable (`git rev-parse` fails) → drop memo, degrade to full sweep; per-row `v_row_shas` drift → edited §V rows re-classified, hash-stable rows carry forward HOLD-SINCE-CLEAN. `oversized_cell_ack` is sha over the acknowledged oversized cell-id set — the script suppresses the `history|ADVISORY|oversized cells` row while the set is unchanged, re-fires when a new oversized cell appears (mirrors silence-class roll-forward — recurring smell not re-nags once acknowledged @ last clean run).
- **write** — `write-memo` mode (see WRITE-MEMO) computes clean-set membership itself + per-row hashes + the oversized-cell ack + idempotent `.claude/.gitignore` guard; LLM not decide clean, not hand-write memo.

Memo update is side-effect every clean run, not user-prompt. `v_row_shas` per-row keying invalidates edited rows only (not siblings); §V-section non-row content (archive-marker line) unhashed so not fires a re-classify, format audit covers marker shape so not coverage gap.

## SCOPE — memo-driven default

Both scope dimensions is script-emitted machine-side (per the memo invariant) — the LLM consumes the `audit` scope-feed rows, not hand-rolls `git diff`. When memo exists and not invalidated, §V classification scope is dirty set:

1. **§V dirty** is (rows w/ `v_row_shas` drift per script `memo|ADVISORY|v_row_shas drift: …` row) + (rows whose body-text path tokens intersect the script `diff|ADVISORY|touched: …` row — path tokens is quoted/backticked path-like strings in invariant body matched against the script's touched-set). Row in neither source → emit `V<n> HOLD-SINCE-CLEAN` per memo invariant, not re-classify. not re-derive the touched set via `git diff` — the script's `diff|ADVISORY` field is the source.
2. **§T** closed-row re-verify scoped to the script `tasks|ADVISORY|flipped-since-clean: …` row (rows flipped `.` → `x` since `last_clean_sha`, machine-side). Historical `x` (unchanged, not in field) → HOLD-SINCE-CLEAN.
3. **§I + cite-DAG** is full-sweep every run (cite-DAG owned by script; §I shape-diff cheap so not triage gain).

First-run (memo absent or invalidated per script `memo|ADVISORY`) or `--full` (memo deleted upfront) → classify all §V rows.

§V row bodies for the classified set (single-agent narrow-scope and sub-agent batch paths) is emitted by the script — not whole-file `SPEC.md` Read for §V bodies:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py emit-v-slices [--dirty V<n>,...]
```

Script reads `SPEC.md` directly and prints each §V row body w/ its source line range — header `## V<n> SPEC.md:<start>-<end>` followed by the verbatim row text, one block per row. `--dirty` is comma-list of the dirty set per step 1 (default empty is all rows); first-run or `--full` is omit `--dirty` (all rows). Read token cap paginates a large SPEC so the script slice sidesteps pagination and is a dirty-filterable canonical §V-body source per the batch invariant — but not bulk-load: the narrow-scope single-agent path (batch 1) still loads the full dirty-filtered slice set in-thread (set may itself spill to a persisted file > inline output cap), whereas sub-agent batch paths distribute that load per-spawn. Pagination-sidestep differs bulk-load-sidestep.

## CHECK invariants

The script does not classify behavioral invariants — `§V` claim → verifiable-code-claim translation and HOLD/VIOLATE judgment stays LLM. For each dirty `V<n>`:

1. Translate invariant into verifiable claim about code.
2. Determine recipe scope (some invariants reduce scope per scope-set invariant, e.g. PUBLISHED-only; every invariant w/o scope reduction is full repo) and compute touch set is the script `diff|ADVISORY|touched: …` set intersect scope (memo-driven default; first-run or `--full` is scope itself). not hand-roll `git diff` — the script's touched-set is the source per the memo invariant.
3. Touch set empty → emit `V<n> SCOPE-EMPTY: <reason>` per drift-verdict-vocab invariant; record evidence `scope-touch overlap empty`; skip grep. Silence differs verified-absence.
4. Row clean since `last_clean_sha` per memo and recipe scope not intersected by current touch → emit `V<n> HOLD-SINCE-CLEAN` per memo invariant; record evidence `HOLD-since-clean @ <last_clean_sha>`; skip grep.
5. Else grep / read relevant files; classify **HOLD** / **VIOLATE** / **VIOLATE-CAPTURED** / **UNVERIFIABLE** / **SCOPE-EMPTY** / **HOLD-SINCE-CLEAN** / **LATENT** per drift-verdict-vocab invariant. Actionable set is {HOLD, VIOLATE, VIOLATE-CAPTURED, UNVERIFIABLE} — each → REPORT body row (HOLD silent) + distinct remedy-hint path. Silence set is {SCOPE-EMPTY, HOLD-SINCE-CLEAN, LATENT} — operationally identical: not REPORT body row, not remedy hint; aggregator (main thread) collapses → summary line under unified `suppressed` label w/ per-reason breakdown per drift-verdict-vocab invariant. Classifier-internal verdicts preserved every memo precision (`last_v_classifications`). Verdict semantics: VIOLATE-CAPTURED is live violation and `§B`-recorded and remediation forward-only (e.g. historical commit body, archived artifact) — emit form `<row-id> VIOLATE-CAPTURED: <evidence>; see §B.<n>`; recipe-author classifies based on `§B` cite presence (e.g. captured-sha list in REPO-LOCAL extension). LATENT is invariant trigger condition structurally absent from current repo state so audit no-op until condition fires (e.g. invariant constrains impl-code class not present per repo constraints; invariant triggers @ artifact size threshold currently unmet); distinct from UNVERIFIABLE (which signals missing audit infrastructure every claim that should otherwise be verifiable).
6. Record address + file:line evidence.

Recipes ! parametric — not name repo-literal paths beyond `SPEC.md`. Project-specific enforcement in the `.claude/scripts/check-extras.sh` hook (mechanical, run by the audit script) + `.claude/check-extras.md` judgment-class extras (verdict guidance, captured-sha lists) consulted by the LLM during classification.

### Batch protocol (parallel invariant audit)

Invariant audit MAY parallelize via Explore sub-agents (per PREAMBLE). Per-batch shape:

1. **Batch count** is `ceil(|V|/15)` clamped `[1, 4]`. <15 rows → 1 agent (main-thread, not overhead win); ≥60 → cap 4 (diminishing returns and per-agent context bloat). **Narrow-scope override**: row count ≥ 15 and unique-file-scope (distinct PUBLISHED files any row's audit reach touches per scope-set invariant) < `ceil(|V|/2)` → 1 agent regardless of row count. Rationale is cross-cutting greps amortize across rows (one `rg` invocation scans full PUBLISHED scope once so shared across audits) and rows in {LATENT, HOLD-by-inspection} not delegate-bearing mechanical work so thin sub-agent deliverable per spawn and local `rg` cost < 4 agent-spawn cost every narrow repo. Threshold is row count x file-scope diversity, not row count alone — narrow-scope dogfood repos w/ cross-cutting audits stay single-thread regardless of |V|.
2. **Range partition** is contiguous V<n> spans assigned per-batch. Cite locality preserved so adjacent invariants share file scope so agent reuses file reads.
3. **Agent prompt** is canonical block below — dispatcher copies verbatim per batch, fills only `{...}` placeholders. not paraphrase framing, not improvise schema language per call. `{V_SLICE}` and `{LINE_START}`/`{LINE_END}` is filled from the script's `emit-v-slices` output (per SCOPE), not re-Read SPEC.md for slice text: batch is contiguous V<n> span, `{V_SLICE}` is the batch rows' verbatim body text, `{LINE_START}`/`{LINE_END}` is first and last row's source line from the `## V<n> SPEC.md:<start>-<end>` headers. Narrow-scope single-agent path (batch count 1) sources the same slice in-thread so bulk-loads the full slice set into the main thread (no per-spawn distribution) — sidesteps Read-cap pagination, not the bulk-load cost.
4. **Aggregation** is main thread concatenates per-batch tables → REPORT invariant drift block.
5. **Failure** is agent error or timeout → main thread re-runs that range serially (strict fallback, not retry); other agents' batch results retained.

Cite-DAG resolution and format and history and pinned-header is owned by the audit script (MECHANICAL CORE) — not delegated to §V batches.

#### Canonical agent prompt block

Dispatcher copies the fenced block verbatim per batch; fills only `{...}` placeholders. not rewrite, not paraphrase, not omit lines.

```
You are an invariants audit sub-agent. Read-only tools (Explore-class palette). No edits, no commits.

INPUT — SPEC.md invariants slice (lines {LINE_START}–{LINE_END}):

{V_SLICE}

INPUT — audit recipe (CHECK invariants step 5 behavioral-claim classification + judgment-class REPO-LOCAL extras from `.claude/check-extras.md`, verbatim):

{RECIPE_EXCERPT}

INPUT — scope sets (per scope-set invariant in SPEC.md):

PUBLISHED = {PUBLISHED_PATHS}
REPO-LOCAL = {REPO_LOCAL_PATHS}
SPEC-ADJACENT = {SPEC_ADJACENT_PATHS}
GITHUB-FACING = {GITHUB_FACING_PATHS}

OUTPUT — pipe-table only. Columns: `id|verdict|evidence`.

- `id` is invariant row identifier (`V<n>`).
- `verdict` in {HOLD, VIOLATE, VIOLATE-CAPTURED, UNVERIFIABLE, SCOPE-EMPTY, HOLD-SINCE-CLEAN, LATENT}.
- `evidence` ≤ 1 line, one of `file:line` or `no test covers …` or `scope-touch overlap empty` or `HOLD-since-clean @ <sha>` or `<file:line>; see §B.<n>` (VIOLATE-CAPTURED form) or `<trigger-condition-absent reason>` (LATENT form).

No prose preamble before the table. No trailing summary after the table. No commentary between rows. Pipe-table only — first line is header `id|verdict|evidence`, subsequent lines one row per assigned V<n>.
```

Verbatim-copy contract closes the dispatcher-improvisation class — block is single source of truth every sub-agent input and output shape; per-call paraphrase not permitted.

## CHECK §-cite — ambiguous adjudication

Mechanical cite-DAG resolution (typed-prefix cites → expected-section rows, archive-probe, backtick pre-filter) is owned by the audit script → `cite|UNRESOLVED` and `cite|TYPE-MISMATCH` rows fold into REPORT cite drift. LLM adjudicates only the `cite|ambiguous|…` subset (bare-form phase-label / gate-ID collisions every consumers admitting bare-form REPO-LOCAL scope) — per-hit verdict in {spec-cite, phase-label, ambiguous}; clear cases auto-classify, residual → operator review. not re-run the mechanical resolution.

The script's cite-DAG edge set is authoritative citer list every `/sdd:spec` renumber-sweep — replaces free-text grep.

## CHECK interfaces

For each I item:

1. Locate implementation.
2. Classify:
   - **MATCH** — shape in code = shape in spec.
   - **DRIFT** — impl exists, shape differs.
   - **MISSING** — impl absent.
   - **EXTRA** — code exposes surface not in interfaces section.

### List-shape sub-recipe

Interface field w/ enumerated list (verb set, cmd set, tool list, config keys, env vars) → mechanical set-diff not manual re-read:

1. extract list-valued field → spec set.
2. build code symbol set via grep or AST (e.g. CLI verb registry, exported cmd map, config-key constants).
3. diff: `spec - code` → MISSING rows; `code - spec` → EXTRA rows.

Catches enumerated drift (missing verb, undocumented flag) that free-text re-read slips past.

## CHECK tasks

For each T<n>:

1. If `x`:
   - Memo says row `x` predates `last_clean_sha` (status unchanged since last clean run) → emit `T<n> HOLD-SINCE-CLEAN` per memo invariant; skip re-verify.
   - Else verify claimed work present (re-verify rows flipped `.` → `x` since memo; every rows under `--full` or first-run).
2. If `.`: note as pending.
3. Flag `x` rows with no evidence as **STALE**.

## REPORT

Telegraph register. Grouped by severity. Mechanical rows (`format` / `cite` / `history` / `pinned-header` / `token` / `memo`) from the audit script merge into their blocks; behavioral `V<n>` rows from the §V batches; `I.<key>` / `T<n>` from interface and task audits.

```
## invariant drift
V<n> VIOLATE: auth/mw.go:47 uses `<` not `≤`. see §B.<n>.
V<n> VIOLATE-CAPTURED: <commit-sha> body contains heavy math operators; see §B.<n>.
V<n> UNVERIFIABLE: no test covers every req path.
§T.<n> VIOLATE: history: dated-retirement in task body — prune per freshness-contract invariant.

## cite drift
T<n>.cites V<m> UNRESOLVED: V<m> absent from invariants section.
§B.<n>.fix T<k> TYPE-MISMATCH: target is task row, expected invariant row.
CLAUDE.md:<line> cite UNRESOLVED: row absent.

## interface drift
I.api DRIFT: POST /x returns `{result}` not `{id}`. route.go:112.
I.cmd MISSING: `foo bar` absent from cli/*.go.

## task drift
T<n> STALE: status `x`, no middleware file exists.

## summary
2 violate. 1 violate-captured. 1 missing. 1 stale. 1 unverifiable. 1 unresolved. 1 type-mismatch. 5 suppressed (1 scope-empty, 2 hold-since-clean, 2 latent).
```

Silence-class verdicts {SCOPE-EMPTY, HOLD-SINCE-CLEAN, LATENT} excluded from REPORT body — collapsed in summary line under unified `suppressed` count w/ per-reason breakdown per drift-verdict-vocab invariant. Rows roll forward run-to-run; LATENT re-classifies to HOLD or VIOLATE when trigger condition fires; HOLD-SINCE-CLEAN re-verifies on touch-set intersect; SCOPE-EMPTY re-verifies on scope expansion.

Body-row aggregation (mechanical core): `history`-class actionable VIOLATE rows collapse per section (§V/§T/§B) when section count > threshold (owned by mechanical audit script per drift-verdict-vocab invariant) → single per-section summary row `§<S>: <n> rows (<count> <pattern>, ...) → /sdd:compact body-trim` w/ pattern breakdown across {amendment-counter, dated-retirement, supersession-narration}; below-threshold sections retain per-row form. `--full` invocation (LOAD step 2) propagates to the script and restores per-row listing for inspection. Mirrors silence-class summary collapse — fold-equivalent applied to actionable subclass when remedy uniform across the set.

Canonical example (aggregated history block, §V over threshold + §B below):

```
## invariant drift
§V: 49 rows (29 amendment-counter, 12 dated-retirement, 8 supersession-narration) → /sdd:compact body-trim
§B.<n> VIOLATE: history: amendment-counter @ SPEC.md:<line>

## summary
2 violate.
```

Clean-run REPORT ! contain `## checkpoint` H2 section per checkpoint-advancement invariant — reflects the script's `write-memo` outcome as single line emitted before `## summary`:

- memo advanced (`last_clean_sha` mutates post-write) → `clean → memo <old-sha> → <new-sha>`
- memo unchanged (rerun, HEAD not shifted so `last_clean_sha` stays) → `clean — memo @ <sha>`
- dirty run (exists VIOLATE or DRIFT or MISSING or STALE or UNRESOLVED or TYPE-MISMATCH) → omit section (existing `## summary` violate count carries signal)

State mutation ! salient signal — buried prose not sufficient for operator to confirm clean and checkpoint advancement.

Canonical example (clean run, memo advanced):

```
## checkpoint
clean → memo fdc6cac → 060a9d2

## summary
0 violate. 1 violate-captured. 39 suppressed (18 hold-since-clean, 2 latent, 19 hold).
```

Final-output ! contain `## advisory` H2 section — emits between `## checkpoint` and `## summary` (or leads output when not checkpoint emitted). One line per fired condition, sourced from the script's `token|ADVISORY` and `memo|ADVISORY` and `history|ADVISORY` rows. Omit heading entirely when not line emits.

Canonical example (clean run w/ token overflow + memo schema invalidation):

```
## checkpoint
clean — memo @ 060a9d2

## advisory
memo schema_version mismatch — memo dropped, full sweep
SPEC.md ~30k tokens > 25k budget; consider /sdd:compact

## summary
0 violate. 1 violate-captured. 39 suppressed (18 hold-since-clean, 2 latent, 19 hold).
```

## WRITE-MEMO

Source the canonical live id-set skeleton from the script not hand-enumerate the live row set — the script already parses/hashes the §V + §I + §T id set so the verdict table is assembled by filling verdicts against the skeleton, closing the omitted-row silent-undercoverage class per the memo invariant:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py emit-row-ids
```

Emits one blank-verdict row per live id (`id||`, header `id|verdict|evidence`). Fill each row's verdict and evidence from the REPORT classification (§V batches, §I/§T audits); merge with the script's mechanical rows (`format`/`cite`/`history`/… from `audit`). Then feed the **merged** verdict table to the script's `write-memo` mode on stdin:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py write-memo < <merged-table>
```

Script validates the verdict vocab, computes clean-set membership itself (clean iff not VIOLATE or UNVERIFIABLE or UNRESOLVED or TYPE-MISMATCH or DRIFT or MISSING or STALE or EXTRA in table), and writes the memo (schema v3, per-row `v_row_shas`, `last_clean_sha` is git HEAD, `last_v_classifications` is `V<n>` verdicts, `oversized_cell_ack` is sha over the clean-run oversized cell-id set, idempotent `.claude/.gitignore` guard) only when clean. Dirty run → script not writes, emits offenders on stderr. LLM not decide clean, not hand-write memo. The `## checkpoint` line reflects the write outcome.

## REMEDY HINTS (used to populate the Next block, not as a separate output section)

Map each drift class to a candidate Next item — pick the most acute classes and surface them as numbered descriptions (no leading dispatch label):

- VIOLATE / DRIFT → `/sdd:spec bug: <description citing V.n>`.
- VIOLATE-CAPTURED → no action; baseline already `§B`-recorded, remediation forward-only per drift-verdict-vocab invariant.
- `history:` VIOLATE → `/sdd:spec amend §<S>.<n>` to prune inlined history from the invariant or bug row; task-row residue → `/sdd:compact` body-trim per token-budget compact invariant prong.
- `format:` VIOLATE → `/sdd:spec amend §<S>.<n>` (or `/sdd:compact` when archive-marker / window split) to repair the SPEC-FORMAT breach.
- SUPPRESSED (silence-class: scope-empty, hold-since-clean, latent) → no action; non-actionable per drift-verdict-vocab invariant; rolls forward run-to-run until trigger condition fires (LATENT) or touch set intersects (HOLD-SINCE-CLEAN) or scope expands (SCOPE-EMPTY).
- MISSING → `/sdd:build <task-cite>` if task exists; else `/sdd:spec amend task` to add row.
- STALE → `/sdd:spec amend <task-cite>` to uncheck status.
- EXTRA → invariant mandates surface (e.g. some invariant ! verb in CLI) → `/sdd:spec amend interfaces` (drift cause known: interface shape not invariant mandate, invariant row already records); invariant silent → `/sdd:spec bug: <surface> not in interfaces section` (drift cause TBD, `§B` row starts conversation).
- UNRESOLVED / TYPE-MISMATCH → `/sdd:spec amend §<S>.<n>` to repair stale or wrong-section cite.

Never invoke fixes. Report only.

## OUTPUT — "Next" block

Heading `## Next`; 1–5 atomic items (one sentence each, no `Reply` prefix); positional dispatch (`run <int>` or `run /<plugin>:<cmd> [args]`). Optional `## Hint` (≤ 3 lines) precedes when item selection needs hidden state (severity ordering VIOLATE > DRIFT > MISSING > STALE > EXTRA; `/sdd:spec bug:` vs `amend` choice). check is read-only so items are slash-cmd follow-ups; before `/sdd:build --next` confirm ≥ 1 pending task `.` else suggest `/sdd:spec` seed.

Canonical example (drift found):

```
## summary
1 violate. 1 drift.

## Hint

VIOLATE outranks DRIFT — record the V<n> breach via item 1 before fixing the interface drift, so `§B` captures the cause not just the symptom.

## Next

1. /sdd:spec bug: V<n> violation at auth/mw.go — record the drift
2. /sdd:spec bug: I.api DRIFT at route.go — record interface drift
```

Variants: clean run w/ pending task `.` → swap items to `/sdd:build --next` + `/sdd:check` later; terminal (all tasks closed and clean) → `/sdd:spec` to seed.

## NON-GOALS

- Zero writes to SPEC or code. Memo + `.gitignore` guard in REPO-LOCAL `.claude/` (cache), written by the audit script's `write-memo` mode — not SPEC or code mutation.
- Mechanical audits delegate to `${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py` — deterministic, not re-derived per run. Behavioral `§V` classification and interface shape-diff and task STALE-verify stay LLM; reads may delegate to Explore sub-agents (per PREAMBLE).
- No scores, no grades. Binary per item: holds or drifts.
