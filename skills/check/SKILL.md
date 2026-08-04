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
argument-hint: "[--full]"
model: sonnet
context: fork
background: false
---

# check — drift report

Pure diagnostic.
Reports violations; writes nothing to SPEC or code; user decides remedy.
Only sibling state: memo + `.gitignore` guard in REPO-LOCAL `.spec/` (cache, not source of truth — code + SPEC.md are truth).
Mechanical audits owned by published script per mechanical-realization invariant — never re-derive its greps per run.
Behavioral judgment stays LLM.
Recipes parametric per parametric-recipe invariant — repo-specific extensions: `.spec/scripts/check-extras.sh` hook (mechanical, run by script) + `.spec/check-extras.md` (judgment-class, consulted by LLM).
Read-only → sub-agent delegation safe throughout.
Runs `context: fork` + `background: false` — run isolates to the fork, REPORT returns as the result; no conversation history in fork (recipe self-contained). Agent tool absent → Batch single-agent path.
Conditional detail lives in `references/` one level deep per token-budget invariant (skill-body budget) — each pointer names its load moment; Read on that moment only.

## PROGRESS

Multi-phase run per response-shape invariant → emit live harness checklist.
Phases: LOAD, audit (mechanical core), §V classify, §I + cite-DAG, §T, REPORT + WRITE-MEMO.
TaskCreate one task per phase @ LOAD start; TaskUpdate `in_progress` @ phase entry → `completed` @ phase exit. `--full` adds no phase (same recipe, memo dropped).
Checklist = ephemeral harness UI: never repo state, never the memo, never substitutes REPORT or the `## Next` block.

## LOAD

Step 1 + 3 outputs arrive injected below (`!` preprocessing, pre-model); `disableSkillShellExecution` consumers see a disabled-by-policy marker instead → run the per-step fallback cmd manually.

1. Spec overview (SCOPE, not whole-file Read per single-load invariant):

!`python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-mechanical.py emit-overview`

   Fallback: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py emit-overview`.
   Prints §G/§C/§I/§T/§B bodies + §V id list; §V bodies arrive via `emit-v-slices` only (step 4).
   Script error "no SPEC.md" → "no spec, nothing to check."
   Stop.
2. Parse `$ARGUMENTS` (two forms only, per dispatch invariant):
   - bare → memo-driven default sweep: invariants + interfaces + tasks.
     Memo absent or invalidated → full re-classify.
     Fresh memo written on clean.
   - `--full` → delete `.spec/check-state.json` upfront, classify all rows, propagate `--full` to audit script (restores per-row history listing instead of aggregation).
     Interrupt mid-run → no memo → next run also full ("don't trust cache" fails safe).
   - other → bail w/ `unknown arg <arg> — accepted forms: bare invocation, --full`.
3. Audit output (MECHANICAL CORE):

!`python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-mechanical.py audit $ARGUMENTS`

   Fallback: the MECHANICAL CORE fenced cmd.
   Its `memo|ADVISORY|…` rows report fired invalidation triggers + the `v_row_shas` dirty set that scopes §V re-classification.
4. §V row bodies come from the script's `emit-v-slices` mode (SCOPE), never whole-file Read — large SPEC paginates past the Read token cap.

## MECHANICAL CORE — audit script

Deterministic audit set — SPEC-FORMAT structural rules, cite + fix grammar, monotonic-ID, cite-DAG, history-residue + oversized-cell advisory, pinned-invariant-header, MECHANIZE-block byte-identity, auto-fire slash-dispatch ban, grant-use, CLAUDE.md marker block, human-facing symbol + idiom scan, sembr scan, memo bookkeeping, token estimate — owned by `${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py`.
Script regex is single source of truth; per-run paraphrase not permitted (mirrors canonical-agent-block verbatim contract) — each script row supersedes any hand-run sweep of the same rule (MECHANIZE `awk|md5|uniq` check, dispatch grep, grant sweep, symbol grep, idiom grep).

Output injected @ LOAD step 3; fallback cmd (mid-glob grant pin per tooling-preference invariant; git ops all run inside the script):

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py audit [--full]
```

Reads `SPEC.md` (+ `SPEC.archive.md` sibling if exists) from cwd; discovers PUBLISHED scope from `.claude-plugin/marketplace.json`; probes `.spec/scripts/check-extras.sh` (exists + executable → run, append its `id|verdict|evidence` rows — language-agnostic contract).
Emits pipe-table `id|verdict|evidence` — full row catalog + REPORT merge rules: Read `references/audit-rows.md` @ first audit-output parse.
Merge summary: dirty-class rows (`format` / `cite` / `history` / `pinned-header` / `mechanize` / `dispatch` / `grant` / `claude-md` / `symbols` / `idiom`) → their REPORT blocks; `token` + `skill-token` + `sembr` + `memo`-invalidation → `## advisory`; scope-feed rows (`memo` drift, `tasks`, `diff`, `scope`) + `batch` consumed machine-side, never surfaced, never hand-rolled via `git diff` or a hand-grep over §V bodies.

## MEMO

`.spec/check-state.json`, schema v3 — field shapes: Read `references/memo-schema.md` when needed.

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

Invariant audit MAY parallelize via Explore sub-agents.
Batch count = the audit's `batch|ADVISORY|recommended: <n> agents` row — script-computed per batch invariant, never re-derived here; `n` = 1 → main-thread single-agent path.
`n` > 1 → Read `references/batch-protocol.md` before spawning: 5-step protocol (partition, canonical prompt block copied verbatim fill-`{...}`-only, aggregate, serial fallback on agent failure).
Cite-DAG, format, history, pinned-header, mechanize-block, dispatch-target, grant-use stay w/ the script — never delegated to §V batches.

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

Telegraph register, grouped by severity — block templates + example rows: Read `references/report-template.md` @ REPORT assembly.
Mechanical rows from script merge into their blocks; behavioral `V<n>` from §V batches; `I.<key>` / `T<n>` from interface + task audits.
Block order: `## invariant drift`, `## cite drift`, `## interface drift`, `## task drift`, then checkpoint / advisory / summary per below.
Silence-class verdicts excluded from body — collapsed in summary `suppressed` count w/ per-reason breakdown; roll-forward semantics per `references/report-template.md`.

**Body-row aggregation** (mechanical core): `history`-class VIOLATE rows collapse per section (§V/§T/§B) when section count > threshold (script-owned) → single summary row `§<S>: <n> rows (<count> <pattern>, ...) → /sdd:condense body-trim` w/ breakdown across {amendment-counter, dated-retirement, supersession-narration}; below-threshold sections keep per-row form. `--full` restores per-row listing.

**Checkpoint** — clean-run REPORT ! contain `## checkpoint` H2 reflecting `write-memo` outcome, single line before `## summary` (state mutation needs salient signal, not buried prose):

- memo advanced → `clean → memo <old-sha> → <new-sha>`
- memo unchanged (HEAD not shifted) → `clean — memo @ <sha>`
- dirty run (any VIOLATE / DRIFT / MISSING / STALE / UNRESOLVED / TYPE-MISMATCH) → omit section.

**Advisory** — fired conditions ! emit `## advisory` H2 between `## checkpoint` and `## summary` (or leading output when no checkpoint).
One line per fired `token|ADVISORY` / `skill-token|ADVISORY` / `sembr|ADVISORY` / `memo|ADVISORY` / `history|ADVISORY` row.
No line → omit heading.

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

Populate the Next block (not a separate section) — drift-class → candidate-item map: Read `references/report-template.md` (Remedy map §) @ Next-block assembly; surface most acute.
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
