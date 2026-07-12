---
name: check
description: |
  Read-only drift detector. Diffs SPEC.md vs current code, reports violations
  grouped by severity. Writes nothing — suggests remedies via spec or build
  skills, never invokes them. Triggers when user asks to check drift, audit
  spec, or verify invariants. Phrasings: "check drift", "audit the spec",
  "check invariants", "spec vs code", "is the spec still accurate?",
  "did the code drift?".
allowed-tools: Read, Grep, Bash(python3 */check-mechanical.py *), Agent, TaskCreate, TaskUpdate
disallowed-tools: Edit, Write
model: sonnet
---

# check — drift report

Pure diagnostic.
Reports violations; writes nothing to SPEC or code; user decides remedy.
Only sibling state: memo + `.gitignore` guard in REPO-LOCAL `.spec/` (cache, not source of truth — code + SPEC.md are truth).
Mechanical audits owned by published script per mechanical-realization invariant — never re-derive its greps per run.
Behavioral judgment stays LLM.
Recipes parametric per parametric-recipe invariant — repo-specific extensions: `.spec/scripts/check-extras.sh` hook (mechanical, run by script) + `.spec/check-extras.md` (judgment-class, consulted by LLM).
Read-only → sub-agent delegation safe throughout.

## PROGRESS

Multi-phase run per response-shape invariant → emit live harness checklist.
Phases: LOAD, audit (mechanical core), §V classify, §I + cite-DAG, §T, REPORT + WRITE-MEMO.
TaskCreate one task per phase @ LOAD start; TaskUpdate `in_progress` @ phase entry → `completed` @ phase exit. `--full` adds no phase (same recipe, memo dropped).
Checklist = ephemeral harness UI: never repo state, never the memo, never substitutes REPORT or the `## Next` block.

## LOAD

1. Load spec overview (SCOPE, not whole-file Read per single-load invariant) — `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py emit-overview`.
   Prints §G/§C/§I/§T/§B bodies + §V id list (no §V bodies — those arrive via `emit-v-slices` step 4; whole-file Read here double-loads SPEC.md + re-hits the Read token cap).
   Script exits non-zero "no SPEC.md" → "no spec, nothing to check."
   Stop.
2. Parse `$ARGUMENTS` (two forms only, per dispatch invariant):
   - bare → memo-driven default sweep: invariants + interfaces + tasks.
     Memo absent or invalidated → full re-classify.
     Fresh memo written on clean.
   - `--full` → delete `.spec/check-state.json` upfront, classify all rows, propagate `--full` to audit script (restores per-row history listing instead of aggregation).
     Interrupt mid-run → no memo → next run also full ("don't trust cache" fails safe).
   - other → bail w/ `unknown arg <arg> — accepted forms: bare invocation, --full`.
     Legacy section-name args and multi-flag forms retired.
3. Run audit script (MECHANICAL CORE).
   Its `memo|ADVISORY|…` rows report fired invalidation triggers + the `v_row_shas` dirty set that scopes §V re-classification.
4. §V row bodies come from the script's `emit-v-slices` mode (SCOPE), never whole-file Read — large SPEC paginates past the Read token cap.
   Script slice is canonical §V-body source for single-agent and sub-agent paths.

## MECHANICAL CORE — audit script

Deterministic audit set — SPEC-FORMAT structural rules (section catalog + order, row grammar, rightmost-`|` column extraction, archive markers + sibling shape), `§T` cite / `§B` fix grammar, monotonic-ID, cite-DAG resolution + edge-type, history-residue patterns + pre-filters + oversized-cell advisory, pinned-invariant-header grep, MECHANIZE-block byte-identity across the user-invocable SKILL.md set, auto-fire sub-skill slash-dispatch ban, allowed-tools grant-use (no zero-body-use grant), CLAUDE.md presence + direct-instruction marker block, human-facing naked-symbol + banned-idiom scan, sembr multi-sentence-line scan, memo bookkeeping, token estimate — owned by `${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py`.
Script regex is single source of truth; per-run paraphrase not permitted (mirrors canonical-agent-block verbatim contract) — the MECHANIZE-block check supersedes any hand-run `awk|md5|uniq` block sweep, the dispatch-target check any hand-run skill-body slash grep, the grant-use check any hand-run `allowed-tools` grant sweep, the human-facing scan any hand-run symbol or idiom grep.

Run at audit start (`${CLAUDE_PLUGIN_ROOT}` doesn't expand in frontmatter `allowed-tools` → script-path pin uses mid-glob `Bash(python3 */check-mechanical.py *)`; leading `*` absorbs the unexpanded plugin-root prefix, per tooling-preference invariant. git stays unused — all rev-parse/show/diff run inside the script):

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py audit [--full]
```

Reads `SPEC.md` (+ `SPEC.archive.md` sibling if exists) from cwd; discovers PUBLISHED scope from `.claude-plugin/marketplace.json`; probes `.spec/scripts/check-extras.sh` (exists + executable → run, append its `id|verdict|evidence` rows — language-agnostic contract).
Emits pipe-table `id|verdict|evidence`:

- `format|VIOLATE|format: <detail>` — SPEC-FORMAT breach.
- `cite|UNRESOLVED|<citer> <id> …` / `cite|TYPE-MISMATCH|…` — cite-DAG. `cite|ambiguous|…` = bare-form phase-label / gate-ID collision subset → LLM adjudicates per CHECK §-cite.
- `history|VIOLATE|<row> … history: <pattern>` — inlined-history residue. `history|ADVISORY|oversized cells …` = smell, not VIOLATE.
- `pinned-header|VIOLATE|<file:line> …` — PUBLISHED body pins invariant number in header.
- `mechanize|DRIFT|<path> … md5 <a> != <b>` / `mechanize|MISSING|<path> …` — user-invocable `skills/*/SKILL.md` (minus frontmatter `user-invocable: false`) carries the byte-identical canonical MECHANIZE block per mechanize-scan invariant; DRIFT = divergent block, MISSING = absent sentinel.
  Script-owned byte-identity check — never hand-run `awk|md5|uniq` per run.
- `dispatch|VIOLATE|<path:line> … slash-dispatches auto-fire sub-skill <cmd>` — a skill body names an auto-fire sub-skill (`user-invocable: false`) in `/<plugin>:<sub-skill>` slash form per response-shape invariant; the slash form is never a valid dispatch target (backtick-wrapped exempt).
  Sub-skill set derived frontmatter-only, plugin name from manifest — script-owned, never hand-grep skill bodies per run (closes §B.14).
- `grant|VIOLATE|<path:line> grants <tool> zero body use …` — a frontmatter `allowed-tools` grant the skill body never invokes per tooling-preference invariant (zero-body-use grant banned, nothing to pre-approve).
  Sound by construction: flagged only on total body-absence — canonical token, alias (`Explore` for the sub-agent spawner), the operation verb a body uses for the tool (`rewrite` for the editor), or a `Bash` command anchor; `Glob` matched case-sensitively so wildcard prose (`mid-glob`) never masks a missing grant.
  Spans the PUBLISHED + REPO-LOCAL skill set — script-owned, never hand-run the grant sweep per run (a manual sweep misses rows).
- `claude-md|MISSING|CLAUDE.md absent …` / `claude-md|VIOLATE|CLAUDE.md missing … marker block …` — repo-root `CLAUDE.md` (the human-clarity carrier) present + carries the `sdd:direct-instruction` begin/end marker block per human-clarity invariant; MISSING = absent file, VIOLATE = block absent or mis-ordered.
  Symbol-cleanliness rides the `symbols` row (CLAUDE.md in the human-facing scan set), not re-checked here.
  Script-owned, never hand-verify CLAUDE.md per run.
- `symbols|VIOLATE|<file:line> naked <sym> …` — a human-facing surface (README, CLAUDE.md, manifest) carries a naked `→ ≥ ≤ & ~` outside a backtick span or fenced block per symbol-set + human-clarity invariants; SPEC-adjacent telegraph keeps the set, so it is never scanned.
  Script-owned, never hand-run the symbol grep per run.
- `idiom|VIOLATE|<file:line> banned idiom <phrase> …` — a human-facing surface carries a banned idiom / jargon-idiom phrase per human-clarity invariant, matched against a curated low-false-positive BOUNDARIES subset (multi-word idiom + hyphenated jargon-idiom; ambiguous single words excluded).
  Backtick-span + fenced-block exempt (a code-span or fenced example naming a banned phrase, e.g. CLAUDE.md's ban list, is fine).
  Script-owned, never hand-run the idiom grep per run (a manual sweep forgets to re-run it) (closes §B.22).
- `sembr|ADVISORY|<file:line> multi-sentence source line …` — a prose source line in the sembr file set (README, CLAUDE.md, `designs/*.md`, skill bodies) holds ≥ 2 sentences per sembr invariant; fence / `|`-table / frontmatter / blockquote / backtick-span exempt, pipe-row files never in the set.
  Advisory only (source-format rule, never dirty).
  Script-owned, never hand-run the multi-sentence line scan per run.
- `token|ADVISORY|SPEC.md ~<n>k tokens > budget …` — estimate `bytes/3.4` per token-budget invariant.
- `memo|ADVISORY|<trigger>` — invalidation (`schema_version` mismatch or `last_clean_sha` unreachable → drop memo, full sweep) or scope feed `v_row_shas drift: V<n>,…`.
- `tasks|ADVISORY|flipped-since-clean: T<n>,…` — §T rows flipped `.`→`x` since clean sha.
- `diff|ADVISORY|touched: <paths>` — paths changed since clean sha.
- `scope|ADVISORY|v-path-dirty: V<n>,…` — §V rows whose body path tokens (quoted/backticked path-like strings) intersect the touched-set; script-computed, consumed by SCOPE step 1 in place of a hand-run grep over the §V section.
- `batch|ADVISORY|recommended: <n> agents` — §V-classification sub-agent count from §V row count + PUBLISHED file census per batch invariant; consumed by Batch protocol step 1, never hand-computed.

Merge into REPORT verbatim: `format` / `history` / `cite` / `pinned-header` / `mechanize` / `dispatch` / `grant` / `claude-md` / `symbols` / `idiom` rows → their REPORT blocks (`mechanize` DRIFT/MISSING + `dispatch` VIOLATE + `grant` VIOLATE + `claude-md` MISSING/VIOLATE + `symbols` VIOLATE + `idiom` VIOLATE → invariant drift); `token` + `sembr` + `memo`-invalidation → `## advisory`.
Scope-feed rows (`memo` drift, `tasks` flipped-set, `diff` touched-set, `scope` v-path-dirty) carry stable comma-joined fields consumed machine-side — chained into `emit-v-slices --dirty`, never surfaced in advisory, never hand-rolled via `git diff` or a hand-grep over §V bodies. `batch|ADVISORY` likewise consumed machine-side (Batch protocol step 1), never surfaced in advisory.

## MEMO

`.spec/check-state.json`, schema v3:

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

- **read** — `audit` mode emits `memo|ADVISORY|…` per fired trigger.
  Per-row `v_row_shas` drift → only edited §V rows re-classify; hash-stable rows carry forward HOLD-SINCE-CLEAN. `oversized_cell_ack` suppresses the oversized-cells advisory while the acknowledged set is unchanged; re-fires on new cell (acknowledged smell not re-nagged).
- **write** — `write-memo` mode (WRITE-MEMO) computes clean-set membership, per-row hashes, ack, idempotent `.spec/.gitignore` guard.
  LLM never decides clean, never hand-writes memo.

Memo update = side-effect of every clean run, no user prompt. §V non-row content (archive-marker line) unhashed → no re-classify on edit; format audit covers marker shape.

## SCOPE — memo-driven default

Both scope dimensions script-emitted; LLM consumes the scope-feed rows, never hand-rolls `git diff`.
Memo valid →

1. **§V dirty** = rows in `memo|ADVISORY|v_row_shas drift` + rows in `scope|ADVISORY|v-path-dirty` (script intersects §V body path tokens — quoted/backticked path-like strings — with the touched-set; no hand-grep over the §V section).
   Neither source → emit `V<n> HOLD-SINCE-CLEAN`, skip.
2. **§T** re-verify scoped to `tasks|ADVISORY|flipped-since-clean` rows.
   Historical `x` unchanged → HOLD-SINCE-CLEAN.
3. **§I + cite-DAG** full-sweep every run (cite-DAG owned by script; §I shape-diff cheap, no triage gain).

First-run, invalidated memo, or `--full` → classify all §V rows.

§V bodies for the classified set:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py emit-v-slices [--dirty V<n>,...]
```

Prints each §V row body w/ source range — header `## V<n> SPEC.md:<start>-<end>` + verbatim row text. `--dirty` = comma-list from step 1; omit on first-run / `--full` (all rows).
Sidesteps Read pagination, not bulk-load cost: single-agent path loads full slice set in-thread (may spill to persisted file past inline output cap); sub-agent batches distribute per spawn.

## CHECK invariants

Script never classifies behavior — §V claim → verifiable-code-claim translation + verdict stays LLM.
For each dirty `V<n>`:

1. Translate invariant → verifiable claim about code.
2. Recipe scope (invariant may reduce scope per scope-set invariant, e.g. PUBLISHED-only; default full repo).
   Touch set = script touched-set intersect scope; first-run / `--full` → scope itself.
3. Touch set empty → `V<n> SCOPE-EMPTY: <reason>`, evidence `scope-touch overlap empty`, skip grep.
   Silence differs verified-absence.
4. Row clean since `last_clean_sha` + scope untouched → `V<n> HOLD-SINCE-CLEAN`, evidence `HOLD-since-clean @ <last_clean_sha>`, skip grep.
5. Else grep/read relevant files; verdict in {HOLD, VIOLATE, VIOLATE-CAPTURED, UNVERIFIABLE, SCOPE-EMPTY, HOLD-SINCE-CLEAN, LATENT} per drift-verdict-vocab invariant.
   - Surfaced {VIOLATE, VIOLATE-CAPTURED, UNVERIFIABLE} → REPORT body row + distinct remedy hint.
   - Silence {HOLD, HOLD-SINCE-CLEAN, SCOPE-EMPTY, LATENT} → no body row, no hint; collapse to summary `suppressed` count w/ per-reason breakdown.
     Verdicts still recorded in memo (`last_v_classifications`).
   - VIOLATE-CAPTURED = live violation, `§B`-recorded, remediation forward-only (e.g. historical commit body) → emit `<row-id> VIOLATE-CAPTURED: <evidence>; see §B.<n>`; classify on `§B` cite presence (e.g. captured-sha list in REPO-LOCAL extension).
   - LATENT = trigger condition structurally absent from repo state → audit no-op until condition fires.
     Differs UNVERIFIABLE (missing audit infrastructure for an otherwise-verifiable claim).
6. Record file:line evidence.

Recipes never name repo-literal paths beyond `SPEC.md`.
Repo-specific enforcement → extras hook + extras md per LOAD.

### Batch protocol (parallel invariant audit)

Invariant audit MAY parallelize via Explore sub-agents:

1. **Batch count** = the audit's `batch|ADVISORY|recommended: <n> agents` row — script-computed from §V row count + PUBLISHED file census; formula owned by the script per mechanical-realization invariant, never re-derived here. `n` = 1 → main-thread single-agent path.
   Narrow-scope collapse (PUBLISHED census small vs §V count → fewer agents amortize cross-cutting greps better) folds into the row already, closing the eyeballed-file-count proxy class (§B.7).
2. **Partition** = contiguous V<n> spans per batch (cite locality → shared file reads).
3. **Prompt** = canonical block below, copied verbatim per batch, fill only `{...}` placeholders — no paraphrase, no per-call schema improvisation. `{V_SLICE}` + `{LINE_START}`/`{LINE_END}` filled from `emit-v-slices` output (batch = contiguous span; line bounds from the `## V<n> SPEC.md:<start>-<end>` headers), never re-Read SPEC.md.
   Single-agent path sources same slice in-thread.
4. **Aggregate** — main thread concatenates per-batch tables → REPORT invariant drift block.
5. **Failure** — agent error or timeout → re-run that range serially (strict fallback, not retry); other batch results retained.

Cite-DAG, format, history, pinned-header, mechanize-block, dispatch-target, grant-use stay w/ the script — never delegated to §V batches.

#### Canonical agent prompt block

```
You are an invariants audit sub-agent. Read-only tools (Explore-class palette). No edits, no commits.

INPUT — SPEC.md invariants slice (lines {LINE_START}–{LINE_END}):

{V_SLICE}

INPUT — audit recipe (CHECK invariants step 5 behavioral-claim classification + judgment-class REPO-LOCAL extras from `.spec/check-extras.md`, verbatim):

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

Mechanical cite-DAG resolution (typed-prefix cites → expected-section rows, archive-probe, backtick pre-filter) owned by script → `cite|UNRESOLVED` + `cite|TYPE-MISMATCH` fold into REPORT cite drift.
LLM adjudicates only `cite|ambiguous|…` (bare-form phase-label / gate-ID collisions) — per-hit verdict in {spec-cite, phase-label, ambiguous}; clear cases auto-classify, residual → operator review.
Never re-run mechanical resolution.
Script's edge set = authoritative citer list for `/sdd:spec` renumber-sweep.

## CHECK interfaces

For each I item: locate implementation; classify

- **MATCH** — code shape = spec shape.
- **DRIFT** — impl exists, shape differs.
- **MISSING** — impl absent.
- **EXTRA** — code exposes surface not in interfaces section.

### List-shape sub-recipe

Interface field w/ enumerated list (verb set, cmd set, tool list, config keys, env vars) → mechanical set-diff, not manual re-read: extract spec set; build code symbol set via grep or AST (CLI verb registry, exported cmd map, config-key constants); `spec - code` → MISSING, `code - spec` → EXTRA.
Catches enumerated drift free-text re-read slips past.

## CHECK tasks

For each T<n>:

1. `x` + predates `last_clean_sha` per memo → `T<n> HOLD-SINCE-CLEAN`, skip re-verify.
2. `x` flipped since memo (or first-run / `--full`) → verify claimed work present; no evidence → flag **STALE**.
3. `.` → note pending.

## REPORT

Telegraph register, grouped by severity.
Mechanical rows from script merge into their blocks; behavioral `V<n>` from §V batches; `I.<key>` / `T<n>` from interface + task audits.

```
## invariant drift
V<n> VIOLATE: auth/mw.go:47 uses `<` not `≤`. see §B.<n>.
V<n> VIOLATE-CAPTURED: <commit-sha> body contains heavy math operators; see §B.<n>.
V<n> UNVERIFIABLE: no test covers every req path.
§T.<n> VIOLATE: history: dated-retirement in task body — prune per freshness-contract invariant.
mechanize DRIFT: skills/explain/SKILL.md MECHANIZE block diverges from canonical.
dispatch VIOLATE: skills/build/SKILL.md:96 slash-dispatches auto-fire sub-skill /<plugin>:<sub-skill>.
grant VIOLATE: skills/explain/SKILL.md:8 grants Grep zero body use.
idiom VIOLATE: README.md:25 banned idiom load-bearing in human-facing prose.

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

Silence-class verdicts excluded from body — collapsed in summary `suppressed` count w/ per-reason breakdown.
Rows roll forward run-to-run; HOLD re-verifies on next dirty-scope hit; LATENT re-classifies when trigger fires; HOLD-SINCE-CLEAN re-verifies on touch-set intersect; SCOPE-EMPTY re-verifies on scope expansion.

**Body-row aggregation** (mechanical core): `history`-class VIOLATE rows collapse per section (§V/§T/§B) when section count > threshold (script-owned) → single summary row `§<S>: <n> rows (<count> <pattern>, ...) → /sdd:condense body-trim` w/ breakdown across {amendment-counter, dated-retirement, supersession-narration}; below-threshold sections keep per-row form. `--full` restores per-row listing.

```
## invariant drift
§V: 49 rows (29 amendment-counter, 12 dated-retirement, 8 supersession-narration) → /sdd:condense body-trim
§B.<n> VIOLATE: history: amendment-counter @ SPEC.md:<line>
```

**Checkpoint** — clean-run REPORT ! contain `## checkpoint` H2 reflecting `write-memo` outcome, single line before `## summary` (state mutation needs salient signal, not buried prose):

- memo advanced → `clean → memo <old-sha> → <new-sha>`
- memo unchanged (HEAD not shifted) → `clean — memo @ <sha>`
- dirty run (any VIOLATE / DRIFT / MISSING / STALE / UNRESOLVED / TYPE-MISMATCH) → omit section.

**Advisory** — fired conditions ! emit `## advisory` H2 between `## checkpoint` and `## summary` (or leading output when no checkpoint).
One line per fired `token|ADVISORY` / `sembr|ADVISORY` / `memo|ADVISORY` / `history|ADVISORY` row.
No line → omit heading.

```
## checkpoint
clean — memo @ 060a9d2

## advisory
memo schema_version mismatch — memo dropped, full sweep
SPEC.md ~30k tokens > 20k budget; consider /sdd:condense

## summary
0 violate. 1 violate-captured. 39 suppressed (18 hold-since-clean, 2 latent, 19 hold).
```

## WRITE-MEMO

Source the live id-set skeleton from the script — never hand-enumerate (closes omitted-row silent-undercoverage class):

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py emit-row-ids
```

Emits one blank-verdict row per live §V/§I/§T id (`id||`, header `id|verdict|evidence`).
Fill verdicts + evidence from REPORT classification — behavioral rows only (§V/§I/§T); never hand-merge the `audit` mechanical rows (memo invariant).
Feed the filled skeleton to stdin; `--from-audit` re-runs the mechanical audit internally + merges it:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py write-memo --from-audit < <filled-skeleton>
```

Script merges its internal mechanical audit w/ the behavioral rows, validates vocab per row type, computes clean-set membership (clean iff no VIOLATE / UNVERIFIABLE / UNRESOLVED / TYPE-MISMATCH / DRIFT / MISSING / STALE / EXTRA), writes memo only when clean (schema v3, per-row hashes, `last_clean_sha` = HEAD, oversized-cell ack, `.gitignore` guard).
Exit `0` = clean (memo advanced); `1` = dirty (memo untouched, offenders on stderr — CI-gateable); `2` = invalid vocab. `## checkpoint` line reflects the outcome.

## REMEDY HINTS

Populate the Next block (not a separate section) — map drift classes → candidate items, surface most acute:

- VIOLATE / DRIFT → `/sdd:spec <description citing §V.<n>>` (gate routes to BACKPROP).
- VIOLATE-CAPTURED → no action; baseline `§B`-recorded, remediation forward-only.
- `history:` VIOLATE → `/sdd:spec amend §<S>.<n>` to prune inlined history; task-row residue → `/sdd:condense` body-trim.
- `format:` VIOLATE → `/sdd:spec amend §<S>.<n>` (or `/sdd:condense` when archive-marker / window split).
- SUPPRESSED → no action; rolls forward until trigger fires / touch intersects / scope expands.
- MISSING → `/sdd:build <task-cite>` if task exists; else `/sdd:spec amend task` to add row.
- STALE → `/sdd:spec amend <task-cite>` to uncheck status.
- EXTRA → invariant mandates the surface → `/sdd:spec amend interfaces` (cause known); invariant silent → `/sdd:spec <surface> missing from interfaces section` (cause TBD, `§B` row starts conversation).
- UNRESOLVED / TYPE-MISMATCH → `/sdd:spec amend §<S>.<n>` to repair stale or wrong-section cite.

Never invoke fixes.
Report only.

## MECHANIZE — script-candidate scan

Recipe end → before the `## Next` block, scan this run for a mechanization candidate.
Candidate = any of:

- ≥ 2 same-shape deterministic calls this run (identical command modulo args)
- LLM-side join / sort / count / dedup over script-emittable data
- multi-step parse collapsible to one script emit mode
- fresh regex paraphrase of an existing mechanical rule (mechanical-realization invariant class)

Hit → emit exactly one `## Next` item naming the observed pattern + proposed script mode; none → no item.
Never self-implement the mechanization mid-run (recipe-step-no-dispatch + write-ownership invariants).
Route by cwd:

- dev repo (this plugin) → /sdd:spec → new §T row
- consumer repo, plugin-target → monitor dispatched `mechanization-candidate` path (monitor-protocol invariant)
- consumer repo-local → consumer /sdd:spec → `.spec/check-extras` row

## OUTPUT — "Next" block

Heading `## Next`; 1–5 atomic items (one sentence each, no `Reply` prefix); positional dispatch (`run <int>` or `run /<plugin>:<cmd> [args]`).
Optional `## Hint` (≤ 3 lines) precedes when item selection needs hidden state (severity order VIOLATE > DRIFT > MISSING > STALE > EXTRA; record-vs-amend choice).
Items are slash-cmd follow-ups; before `/sdd:build --next` confirm ≥ 1 pending `.` task else suggest `/sdd:spec` seed.

Example (drift found):

```
## summary
1 violate. 1 drift.

## Hint

VIOLATE outranks DRIFT — record the V<n> breach via item 1 before fixing the interface drift, so `§B` captures the cause not just the symptom.

## Next

1. /sdd:spec V<n> violated at auth/mw.go — record the drift
2. /sdd:spec I.api drifted at route.go — record interface drift
```

Variants: clean + pending `.` task → `/sdd:build --next` + `/sdd:check` later; terminal (all closed, clean) → `/sdd:spec` to seed.

## NON-GOALS

- Zero writes to SPEC or code.
  Memo + `.gitignore` guard written by the script's `write-memo` mode only.
- Mechanical audits stay in the script; behavioral §V classification, interface shape-diff, task STALE-verify stay LLM; reads delegable to Explore sub-agents.
- No scores, no grades.
  Binary per item: holds or drifts.
