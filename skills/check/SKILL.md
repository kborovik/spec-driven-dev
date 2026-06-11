---
name: check
description: |
  Read-only drift detector. Diffs SPEC.md vs current code, reports violations
  grouped by severity. Writes nothing — suggests remedies via spec or build
  skills, never invokes them. Triggers when user asks to check drift, audit
  spec, or verify invariants. Phrasings: "check drift", "audit the spec",
  "check invariants", "spec vs code", "is the spec still accurate?",
  "did the code drift?".
allowed-tools: Read, Grep, Glob, Bash(git *), Bash(python3 *), Agent, Skill
model: sonnet
---

# check — drift report

Pure diagnostic. Reports violations; writes nothing to SPEC or code; user decides remedy. Only sibling state: memo + `.gitignore` guard in REPO-LOCAL `.claude/` (cache, not source of truth — code + SPEC.md are truth). Mechanical audits owned by published script per mechanical-realization invariant — never re-derive its greps per run. Behavioral judgment stays LLM. Recipes parametric per parametric-recipe invariant — repo-specific extensions: `.claude/scripts/check-extras.sh` hook (mechanical, run by script) + `.claude/check-extras.md` (judgment-class, consulted by LLM). Read-only → sub-agent delegation safe throughout.

## LOAD

1. Read `SPEC.md`. Missing → "no spec, nothing to check." Stop.
2. Args (two forms only, per dispatch invariant):
   - bare → memo-driven default sweep: invariants + interfaces + tasks. Memo absent or invalidated → full re-classify. Fresh memo written on clean.
   - `--full` → delete `.claude/check-state.json` upfront, classify all rows, propagate `--full` to audit script (restores per-row history listing instead of aggregation). Interrupt mid-run → no memo → next run also full ("don't trust cache" fails safe).
   - other → bail w/ `unknown arg <arg> — accepted forms: bare invocation, --full`. Legacy section-name args and multi-flag forms retired.
3. Run audit script (MECHANICAL CORE). Its `memo|ADVISORY|…` rows report fired invalidation triggers + the `v_row_shas` dirty set that scopes §V re-classification.
4. §V row bodies come from the script's `emit-v-slices` mode (SCOPE), never whole-file Read — large SPEC paginates past the Read token cap. Script slice is canonical §V-body source for single-agent and sub-agent paths.

## MECHANICAL CORE — audit script

Deterministic audit set — SPEC-FORMAT structural rules (section catalog + order, row grammar, rightmost-`|` column extraction, archive markers + sibling shape), `§T` cite / `§B` fix grammar, monotonic-ID, cite-DAG resolution + edge-type, history-residue patterns + pre-filters + oversized-cell advisory, pinned-invariant-header grep, memo bookkeeping, token estimate — owned by `${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py`. Script regex is single source of truth; per-run paraphrase not permitted (mirrors canonical-agent-block verbatim contract).

Run at audit start (`${CLAUDE_PLUGIN_ROOT}` invalid in frontmatter `allowed-tools` → frontmatter grants broad `Bash(python3 *)`):

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py audit [--full]
```

Reads `SPEC.md` (+ `SPEC.archive.md` sibling if exists) from cwd; discovers PUBLISHED scope from `.claude-plugin/marketplace.json`; probes `.claude/scripts/check-extras.sh` (exists + executable → run, append its `id|verdict|evidence` rows — language-agnostic contract). Emits pipe-table `id|verdict|evidence`:

- `format|VIOLATE|format: <detail>` — SPEC-FORMAT breach.
- `cite|UNRESOLVED|<citer> <id> …` / `cite|TYPE-MISMATCH|…` — cite-DAG. `cite|ambiguous|…` = bare-form phase-label / gate-ID collision subset → LLM adjudicates per CHECK §-cite.
- `history|VIOLATE|<row> … history: <pattern>` — inlined-history residue. `history|ADVISORY|oversized cells …` = smell, not VIOLATE.
- `pinned-header|VIOLATE|<file:line> …` — PUBLISHED body pins invariant number in header.
- `token|ADVISORY|SPEC.md ~<n>k tokens > budget …` — estimate `bytes/3.4` per token-budget invariant.
- `memo|ADVISORY|<trigger>` — invalidation (`schema_version` mismatch or `last_clean_sha` unreachable → drop memo, full sweep) or scope feed `v_row_shas drift: V<n>,…`.
- `tasks|ADVISORY|flipped-since-clean: T<n>,…` — §T rows flipped `.`→`x` since clean sha.
- `diff|ADVISORY|touched: <paths>` — paths changed since clean sha.

Merge into REPORT verbatim: `format` / `history` / `cite` / `pinned-header` rows → their REPORT blocks; `token` + `memo`-invalidation → `## advisory`. Scope-feed rows (`memo` drift, `tasks` flipped-set, `diff` touched-set) carry stable comma-joined fields consumed machine-side — chained into `emit-v-slices --dirty`, never surfaced in advisory, never hand-rolled via `git diff`.

## MEMO

`.claude/check-state.json`, schema v3:

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

Script owns both ends per memo invariant:

- **read** — `audit` mode emits `memo|ADVISORY|…` per fired trigger. Per-row `v_row_shas` drift → only edited §V rows re-classify; hash-stable rows carry forward HOLD-SINCE-CLEAN. `oversized_cell_ack` suppresses the oversized-cells advisory while the acknowledged set is unchanged; re-fires on new cell (acknowledged smell not re-nagged).
- **write** — `write-memo` mode (WRITE-MEMO) computes clean-set membership, per-row hashes, ack, idempotent `.claude/.gitignore` guard. LLM never decides clean, never hand-writes memo.

Memo update = side-effect of every clean run, no user prompt. §V non-row content (archive-marker line) unhashed → no re-classify on edit; format audit covers marker shape.

## SCOPE — memo-driven default

Both scope dimensions script-emitted; LLM consumes the scope-feed rows, never hand-rolls `git diff`. Memo valid →

1. **§V dirty** = rows in `memo|ADVISORY|v_row_shas drift` + rows whose body path tokens (quoted/backticked path-like strings) intersect `diff|ADVISORY|touched`. Neither source → emit `V<n> HOLD-SINCE-CLEAN`, skip.
2. **§T** re-verify scoped to `tasks|ADVISORY|flipped-since-clean` rows. Historical `x` unchanged → HOLD-SINCE-CLEAN.
3. **§I + cite-DAG** full-sweep every run (cite-DAG owned by script; §I shape-diff cheap, no triage gain).

First-run, invalidated memo, or `--full` → classify all §V rows.

§V bodies for the classified set:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py emit-v-slices [--dirty V<n>,...]
```

Prints each §V row body w/ source range — header `## V<n> SPEC.md:<start>-<end>` + verbatim row text. `--dirty` = comma-list from step 1; omit on first-run / `--full` (all rows). Sidesteps Read pagination, not bulk-load cost: single-agent path loads full slice set in-thread (may spill to persisted file past inline output cap); sub-agent batches distribute per spawn.

## CHECK invariants

Script never classifies behavior — §V claim → verifiable-code-claim translation + verdict stays LLM. For each dirty `V<n>`:

1. Translate invariant → verifiable claim about code.
2. Recipe scope (invariant may reduce scope per scope-set invariant, e.g. PUBLISHED-only; default full repo). Touch set = script touched-set intersect scope; first-run / `--full` → scope itself.
3. Touch set empty → `V<n> SCOPE-EMPTY: <reason>`, evidence `scope-touch overlap empty`, skip grep. Silence differs verified-absence.
4. Row clean since `last_clean_sha` + scope untouched → `V<n> HOLD-SINCE-CLEAN`, evidence `HOLD-since-clean @ <last_clean_sha>`, skip grep.
5. Else grep/read relevant files; verdict in {HOLD, VIOLATE, VIOLATE-CAPTURED, UNVERIFIABLE, SCOPE-EMPTY, HOLD-SINCE-CLEAN, LATENT} per drift-verdict-vocab invariant.
   - Actionable {HOLD, VIOLATE, VIOLATE-CAPTURED, UNVERIFIABLE} → REPORT body row (HOLD silent) + distinct remedy hint.
   - Silence {SCOPE-EMPTY, HOLD-SINCE-CLEAN, LATENT} → no body row, no hint; collapse to summary `suppressed` count w/ per-reason breakdown. Verdicts still recorded in memo (`last_v_classifications`).
   - VIOLATE-CAPTURED = live violation, `§B`-recorded, remediation forward-only (e.g. historical commit body) → emit `<row-id> VIOLATE-CAPTURED: <evidence>; see §B.<n>`; classify on `§B` cite presence (e.g. captured-sha list in REPO-LOCAL extension).
   - LATENT = trigger condition structurally absent from repo state → audit no-op until condition fires. Differs UNVERIFIABLE (missing audit infrastructure for an otherwise-verifiable claim).
6. Record file:line evidence.

Recipes never name repo-literal paths beyond `SPEC.md`. Repo-specific enforcement → extras hook + extras md per LOAD.

### Batch protocol (parallel invariant audit)

Invariant audit MAY parallelize via Explore sub-agents:

1. **Batch count** = `ceil(|V|/15)` clamped `[1, 4]`. <15 rows → main-thread. **Narrow-scope override**: |V| ≥ 15 and unique-file-scope (distinct PUBLISHED files audits touch) < `ceil(|V|/2)` → 1 agent regardless — cross-cutting greps amortize (one `rg` scans full scope once), and local `rg` cost < agent-spawn cost on narrow repo. Threshold = row count x file-scope diversity, not row count alone.
2. **Partition** = contiguous V<n> spans per batch (cite locality → shared file reads).
3. **Prompt** = canonical block below, copied verbatim per batch, fill only `{...}` placeholders — no paraphrase, no per-call schema improvisation. `{V_SLICE}` + `{LINE_START}`/`{LINE_END}` filled from `emit-v-slices` output (batch = contiguous span; line bounds from the `## V<n> SPEC.md:<start>-<end>` headers), never re-Read SPEC.md. Single-agent path sources same slice in-thread.
4. **Aggregate** — main thread concatenates per-batch tables → REPORT invariant drift block.
5. **Failure** — agent error or timeout → re-run that range serially (strict fallback, not retry); other batch results retained.

Cite-DAG, format, history, pinned-header stay w/ the script — never delegated to §V batches.

#### Canonical agent prompt block

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

Block = single source of truth for sub-agent input + output shape; verbatim-copy contract closes the dispatcher-improvisation class.

## CHECK §-cite — ambiguous adjudication

Mechanical cite-DAG resolution (typed-prefix cites → expected-section rows, archive-probe, backtick pre-filter) owned by script → `cite|UNRESOLVED` + `cite|TYPE-MISMATCH` fold into REPORT cite drift. LLM adjudicates only `cite|ambiguous|…` (bare-form phase-label / gate-ID collisions) — per-hit verdict in {spec-cite, phase-label, ambiguous}; clear cases auto-classify, residual → operator review. Never re-run mechanical resolution. Script's edge set = authoritative citer list for `/sdd:spec` renumber-sweep.

## CHECK interfaces

For each I item: locate implementation; classify

- **MATCH** — code shape = spec shape.
- **DRIFT** — impl exists, shape differs.
- **MISSING** — impl absent.
- **EXTRA** — code exposes surface not in interfaces section.

### List-shape sub-recipe

Interface field w/ enumerated list (verb set, cmd set, tool list, config keys, env vars) → mechanical set-diff, not manual re-read: extract spec set; build code symbol set via grep or AST (CLI verb registry, exported cmd map, config-key constants); `spec - code` → MISSING, `code - spec` → EXTRA. Catches enumerated drift free-text re-read slips past.

## CHECK tasks

For each T<n>:

1. `x` + predates `last_clean_sha` per memo → `T<n> HOLD-SINCE-CLEAN`, skip re-verify.
2. `x` flipped since memo (or first-run / `--full`) → verify claimed work present; no evidence → flag **STALE**.
3. `.` → note pending.

## REPORT

Telegraph register, grouped by severity. Mechanical rows from script merge into their blocks; behavioral `V<n>` from §V batches; `I.<key>` / `T<n>` from interface + task audits.

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

Silence-class verdicts excluded from body — collapsed in summary `suppressed` count w/ per-reason breakdown. Rows roll forward run-to-run; LATENT re-classifies when trigger fires; HOLD-SINCE-CLEAN re-verifies on touch-set intersect; SCOPE-EMPTY re-verifies on scope expansion.

**Body-row aggregation** (mechanical core): `history`-class VIOLATE rows collapse per section (§V/§T/§B) when section count > threshold (script-owned) → single summary row `§<S>: <n> rows (<count> <pattern>, ...) → /sdd:compact body-trim` w/ breakdown across {amendment-counter, dated-retirement, supersession-narration}; below-threshold sections keep per-row form. `--full` restores per-row listing.

```
## invariant drift
§V: 49 rows (29 amendment-counter, 12 dated-retirement, 8 supersession-narration) → /sdd:compact body-trim
§B.<n> VIOLATE: history: amendment-counter @ SPEC.md:<line>
```

**Checkpoint** — clean-run REPORT ! contain `## checkpoint` H2 reflecting `write-memo` outcome, single line before `## summary` (state mutation needs salient signal, not buried prose):

- memo advanced → `clean → memo <old-sha> → <new-sha>`
- memo unchanged (HEAD not shifted) → `clean — memo @ <sha>`
- dirty run (any VIOLATE / DRIFT / MISSING / STALE / UNRESOLVED / TYPE-MISMATCH) → omit section.

**Advisory** — fired conditions ! emit `## advisory` H2 between `## checkpoint` and `## summary` (or leading output when no checkpoint). One line per fired `token|ADVISORY` / `memo|ADVISORY` / `history|ADVISORY` row. No line → omit heading.

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

Source the live id-set skeleton from the script — never hand-enumerate (closes omitted-row silent-undercoverage class):

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py emit-row-ids
```

Emits one blank-verdict row per live §V/§I/§T id (`id||`, header `id|verdict|evidence`). Fill verdicts + evidence from REPORT classification; merge w/ the script's mechanical rows from `audit`; feed merged table to stdin:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py write-memo < <merged-table>
```

Script validates vocab, computes clean-set membership (clean iff no VIOLATE / UNVERIFIABLE / UNRESOLVED / TYPE-MISMATCH / DRIFT / MISSING / STALE / EXTRA), writes memo only when clean (schema v3, per-row hashes, `last_clean_sha` = HEAD, oversized-cell ack, `.gitignore` guard). Dirty run → no write, offenders on stderr. `## checkpoint` line reflects the outcome.

## REMEDY HINTS

Populate the Next block (not a separate section) — map drift classes → candidate items, surface most acute:

- VIOLATE / DRIFT → `/sdd:spec bug: <description citing V.n>`.
- VIOLATE-CAPTURED → no action; baseline `§B`-recorded, remediation forward-only.
- `history:` VIOLATE → `/sdd:spec amend §<S>.<n>` to prune inlined history; task-row residue → `/sdd:compact` body-trim.
- `format:` VIOLATE → `/sdd:spec amend §<S>.<n>` (or `/sdd:compact` when archive-marker / window split).
- SUPPRESSED → no action; rolls forward until trigger fires / touch intersects / scope expands.
- MISSING → `/sdd:build <task-cite>` if task exists; else `/sdd:spec amend task` to add row.
- STALE → `/sdd:spec amend <task-cite>` to uncheck status.
- EXTRA → invariant mandates the surface → `/sdd:spec amend interfaces` (cause known); invariant silent → `/sdd:spec bug: <surface> not in interfaces section` (cause TBD, `§B` row starts conversation).
- UNRESOLVED / TYPE-MISMATCH → `/sdd:spec amend §<S>.<n>` to repair stale or wrong-section cite.

Never invoke fixes. Report only.

## OUTPUT — "Next" block

Heading `## Next`; 1–5 atomic items (one sentence each, no `Reply` prefix); positional dispatch (`run <int>` or `run /<plugin>:<cmd> [args]`). Optional `## Hint` (≤ 3 lines) precedes when item selection needs hidden state (severity order VIOLATE > DRIFT > MISSING > STALE > EXTRA; `bug:` vs `amend` choice). Items are slash-cmd follow-ups; before `/sdd:build --next` confirm ≥ 1 pending `.` task else suggest `/sdd:spec` seed.

Example (drift found):

```
## summary
1 violate. 1 drift.

## Hint

VIOLATE outranks DRIFT — record the V<n> breach via item 1 before fixing the interface drift, so `§B` captures the cause not just the symptom.

## Next

1. /sdd:spec bug: V<n> violation at auth/mw.go — record the drift
2. /sdd:spec bug: I.api DRIFT at route.go — record interface drift
```

Variants: clean + pending `.` task → `/sdd:build --next` + `/sdd:check` later; terminal (all closed, clean) → `/sdd:spec` to seed.

## NON-GOALS

- Zero writes to SPEC or code. Memo + `.gitignore` guard written by the script's `write-memo` mode only.
- Mechanical audits stay in the script; behavioral §V classification, interface shape-diff, task STALE-verify stay LLM; reads delegable to Explore sub-agents.
- No scores, no grades. Binary per item: holds or drifts.
