# SPEC — sdd plugin

## §G GOAL

LLM writes code faster than humans read → standards + logic drift unchecked; counter: one telegraph SPEC.md authoritative over code; plugin skills keep code shape + component contracts aligned over time.

## §C CONSTRAINTS

- installable Claude Code plugin marketplace; root-source plugin `sdd` (`.claude-plugin/marketplace.json`, source `./`)
- skills-only: every surface = `skills/<name>/SKILL.md`; no commands/ tree, no hooks
- `scripts/check-mechanical.py` single-file, stdlib-only python3
- no orchestrator, no swarm: main Claude executes; sub-agents read-only
- no state beyond SPEC.md + git + REPO-LOCAL `.claude/` cache

## §I INTERFACES

external surface — what operator + consuming repo see.

- design: `/sdd:design <topic>` → propose-critique loop → `designs/<slug>.md` (SPEC.md untouched)
- spec: `/sdd:spec <intent>` → socratic gate → SPEC.md delta preview → apply + auto-commit
- build: `/sdd:build [§T.n|--next|--all]` → plan → edit → verify → flip §T `.`→`x` + commit per task
- check: `/sdd:check [--full]` → read-only drift REPORT (severity blocks, checkpoint, advisory, summary) + Next block
- explain: `/sdd:explain [§-cite|--next]` → prose expansion w/ cited siblings, zero writes
- compact: `/sdd:compact` → six-prong token sweep, single atomic commit
- reorganize: `/sdd:reorganize [--taxonomy-only]` → §V cluster + renumber + cite sweep, single atomic commit
- script: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py <mode>` → pipe-table `id|verdict|evidence`; modes: audit, write-memo, emit-v-slices, emit-superseded, emit-fold-seeds, emit-v-weights, emit-row-ids, emit-overview, --self-test
- format: `SPEC-FORMAT.md` → row shape + section catalog contract; loaded by spec, check, compact, reorganize

## §V INVARIANTS

numbered, testable, named; each ! hold. ids clustered by topic; gaps = cluster spans + closure history.

V1: spec-adjacent-register — SPEC.md, `skills/**/SKILL.md`, SPEC-FORMAT.md, spec-referencing prose ! telegraph per telegraph skill; /sdd:explain decodes on demand.
V2: github-facing-register — README, issues, PRs, commit-msg bodies ! steno per steno skill; commit subjects = per-skill fixed templates, verbatim.
V3: verbatim-preservation — code, backticked text, paths, URLs, identifiers, numbers, versions, error strings, SQL, regex, JSON, YAML, quoted strings never compressed; backtick-wrapped tokens exempt every residue + cite audit.
V4: symbol-set — keep set `→ ≥ ≤ ! ? §` (steno adds `&`, list-`|`); heavier math operators ! ASCII words.
V10: sole-source-of-truth — SPEC.md @ repo root is sole live spec; no docs/ tree, no sidecars; SPEC.archive.md sibling carries immutable archived rows only.
V11: shape-semantics-split — SPEC-FORMAT.md binds row shape + section catalog + citation grammar; §V rows bind semantics + enforcement; neither restates the other.
V12: monotonic-numbering — V/T/B ids strictly increasing in section order; gaps OK, reuse banned; sole renumber path = /sdd:reorganize (map append + cite sweep, same commit).
V13: cite-resolution — every cite ! resolve: `cites` tokens → live/archived V/T/B row or live §I kind, `fix` tokens → §V row, free-text `§<S>.<n>` → §<S> row; renumber sweeps citers same commit.
V14: pinned-cite-ban — PUBLISHED bodies ! placeholder (`§V.<n>`) or named-invariant form, never pinned §-digit cites; SPEC.md-narrative + REPO-LOCAL pinned cites ! resolve live.
V15: renumber-chain-walk — `.claude/spec-renumber-map.json` append-only; historical id resolves newest-first to live id or `archive` sentinel (→ SPEC.archive.md §V.retired block, never live row).
V16: archive-semantics — archived §T/§B + retired §V rows migrate verbatim to SPEC.archive.md w/ per-section markers per SPEC-FORMAT; archived rows stay cite-resolvable, never edited.
V20: write-ownership — /sdd:spec sole SPEC.md author; exclusions: /sdd:build flips one §T status cell per closed task; /sdd:compact + /sdd:reorganize apply operator-confirmed structural sweeps; /sdd:check + /sdd:explain write nothing.
V21: write-serialize — SPEC.md + code writes serialize main-thread; reads delegable to read-only sub-agents.
V22: recipe-step-no-dispatch — slash-cmd dispatch = operator turn only; recipes end @ commit + Next block; sole exclusion: /sdd:build verify-fail routes cause to spec skill mid-loop.
V23: decision-gate — enumerable runtime choice ! AskUserQuestion w/ mutually-exclusive action labels; selection drives same-turn behavior; prose "or keep going?" forms banned.
V24: response-shape — user-typeable skill output ends `## Next` (1–5 atomic items, no `Reply` prefix, positional dispatch `run <int>` / `run /<plugin>:<cmd> [args]`); optional `## Hint` ≤ 3 lines precedes; multi-phase run {check, build `--all`, compact, reorganize} ! emit live harness checklist — TaskCreate per recipe phase @ start, TaskUpdate in_progress→completed @ transition; checklist ephemeral harness UI, never repo state, never substitutes REPORT or `## Next`.
V25: socratic-gate — /sdd:spec mode {NEW, DISTILL, BACKPROP, AMEND, FOLD-IN} = gate byproduct of free-form `$ARGUMENTS`; no mode prefixes, no skip flags; concrete intent converges ≤ 1 turn.
V26: first-principle-probe — NEW mode fires foundational-claim question exactly once, declinable; `first-principle-asked` recorded regardless of answer.
V27: backprop-protocol — every bug → §B row; recurrence class → new or tightened §V preferred; two commits cross-cited: spec commit (§B + §V + §T) first, build commit (failing test first, then fix) cites the new rows.
V28: freshness-contract — live rows = clean current design; history → commit-msg bodies + archive; residue set {amendment-counter `(∆)`, dated-retirement, supersession-narration} pruned @ spec write, audited @ check, trimmed @ compact — one shared pattern set, owned by script.
V29: fold-first — new §V row vs amend of closest existing row ! operator gate; split justification = §B recurrence cite or declared orthogonal concept; "mirrors existing row" alone insufficient.
V30: sweep-scope — sweep-class §T row ! declare scope as grep pattern or vocab table; named-procedure + named-site lists rejected.
V31: design-lifecycle — /sdd:design writes `designs/<slug>.md` only (write-new); fold-in mutates SPEC.md only; draft persists in working tree, operator disposes.
V40: mechanical-realization — deterministic audit rules realized once in `scripts/check-mechanical.py`; skill bodies + SPEC-FORMAT state contracts, never duplicate parser pseudo-code; per-run regex paraphrase banned.
V41: parametric-recipe — published recipes + script name no repo-literal paths beyond SPEC.md + plugin-internal files; §I ids derive from kind prefixes, never hardcoded surface shapes; repo-specific enforcement → `.claude/scripts/check-extras.sh` + `.claude/check-extras.md`.
V42: scope-set — audit scopes: PUBLISHED (marketplace source dirs; root `./` → repo root), REPO-LOCAL (`.claude/**`, README.md, CLAUDE.md), SPEC-ADJACENT (SPEC.md, skill bodies, SPEC-FORMAT.md), GITHUB-FACING (README, issues, PRs, commit bodies); each audit names its scope.
V43: drift-verdict-vocab — dirty {VIOLATE, UNVERIFIABLE, UNRESOLVED, TYPE-MISMATCH, DRIFT, MISSING, STALE, EXTRA}; silent {HOLD, HOLD-SINCE-CLEAN, SCOPE-EMPTY, LATENT}; surfaced-clean {VIOLATE-CAPTURED}; §I-clean {MATCH} (§I rows only); script validates verdict admissibility per row type → no LLM-side remap; new verdict ! extend script vocab + this row same commit (closes §B.8).
V44: memo — `.claude/check-state.json` = cache, not truth; script owns both ends (read → invalidation advisories; write → clean runs only, per-row §V hashes, oversized-cell ack, `.gitignore` guard); `write-memo --from-audit` re-runs mechanical rows internally → stdin = behavioral verdicts only, hand-merge banned; exit 0 clean / 1 dirty (memo untouched, CI-gateable) / 2 invalid vocab; LLM never decides clean, never hand-writes memo (closes §B.9).
V45: scope-feed — default-sweep scope = script-emitted rows (v_row_shas drift, flipped-since-clean, touched minus SPEC.md + archive sibling); comma-joined fields chain into `emit-v-slices --dirty`; LLM never hand-rolls `git diff`.
V46: batch — §V classification MAY parallelize; count = script audit `batch|ADVISORY|recommended: <n> agents` row: `ceil(|V|/15)` clamp [1, 4], PUBLISHED file census < `ceil(|V|/2)` → 1 agent; LLM never hand-computes count; contiguous spans, canonical prompt block copied verbatim (fill `{...}` only); failed batch re-runs serially (closes §B.7).
V47: check-dispatch — /sdd:check accepts bare (memo-driven) or `--full` (drop memo, re-classify all) only; other args bail.
V48: token-budget — estimate = bytes / 3.4; > 25k tokens → check advisory → operator /sdd:compact; > 50 closed §T rows → window-vs-archive split; canonical values here, mirrored as script constants, retuned via AMEND + script sync same commit.
V49: extras-hook — executable `.claude/scripts/check-extras.sh` runs inside script audit, rows appended verbatim (language-agnostic `id|verdict|evidence` contract); judgment-class extras live in `.claude/check-extras.md`, consulted by check + build pre-commit probe.
V60: skills-only — every surface = `skills/<name>/SKILL.md` dispatched natively as `/<plugin>:<name>`; no commands/ tree, no hooks, no orchestrator.
V61: sub-skill-flags — auto-fire sub-skills (telegraph, backprop, socratic, steno, monitor) ! `user-invocable: false`, never `disable-model-invocation: true` (hides skill from Skill tool, breaks consumer engagement).
V62: tooling-preference — pattern scans `rg --pcre2`; JSON parse `jq`, fallback python3; audit core single-file stdlib-only python3; frontmatter grant = narrowest pattern over body-prescribed invocations: zero-body-use grant banned; script-sole-use interpreter grant pins script path (mid-glob `Bash(python3 */check-mechanical.py *)` form); pin inexpressible (`${CLAUDE_PLUGIN_ROOT}` no-expand in frontmatter) → broad grant + inline note citing upstream limit (closes §B.10).
V63: plugin-shape — PUBLISHED discovery parses `.claude-plugin/marketplace.json` `plugins[].source` (root `./` → repo root, nested path → subdir); plugin name from manifest, never assumed equal to dir name.
V64: single-load — §V bodies enter run context via script `emit-v-slices` only; whole-file SPEC.md Read banned where script emit mode covers need; full read reserved to operator rewrite sweeps (/sdd:compact, /sdd:reorganize) (closes §B.6).
V65: monitor-protocol — consumer-repo skill deviation → capture (skill, version, expected vs actual) ! redact consumer paths/code/identifiers pre-publish; dedup `gh issue list` pre-file, hit → comment not new issue; AskUserQuestion gate every gh write (§V.23); target = manifest `.repository` (§V.41); cwd = plugin repo → backprop hand-off (§V.27), no issue filed.

## §T TASKS

id|status|task|cites
T1|x|add CI: script --self-test + audit dirty-verdict gate on push/PR|V40,V62
T2|x|bump plugin version 1.1.0 + sync manifest description post-consistency-pass|-
T3|x|create REPO-LOCAL `.claude/skills/release/SKILL.md`: gh release flow — bump `.claude-plugin/plugin.json` version + commit, tag `v<version>`, `gh release create` w/ generated notes|V24,V41,V42
T4|x|add script `emit-overview` mode (§G/§C/§I/§T/§B bodies + §V id list, no §V bodies); check LOAD step 1 → emit-overview i/o whole-file Read|V64,V40
T5|x|sweep: add PROGRESS § to multi-phase recipes — scope vocab {check, build, compact, reorganize}; per skill TaskCreate per recipe phase, TaskUpdate per transition, frontmatter allowed-tools += `TaskCreate`, `TaskUpdate`|V24,V62
T6|x|script audit emits batch-advisory row from §V row count + PUBLISHED file census; check batch step 1 consumes row, retire hand-computed heuristic|V46,V40
T7|x|init `skills/monitor/SKILL.md`: auto-fire deviation capture per monitor-protocol; trigger in frontmatter description only, existing skill bodies byte-identical|V65,V61
T8|x|script: admit MATCH as clean verdict on §I rows, per-row-type vocab validation + self-tests|V43,V40
T9|x|script: write-memo `--from-audit` re-runs mechanical side internally, stdin = behavioral verdicts only; check WRITE-MEMO recipe drops hand-merge|V44,V40
T10|.|script: write-memo dirty → exit 1 (memo untouched), invalid vocab stays 2; self-test covers exit codes|V44
T11|.|sweep frontmatter grants — scope `rg -n 'Bash\(' skills/*/SKILL.md`: zero-use → drop (check `Bash(git *)`); script-sole-use python3 → mid-glob pin (check, compact); jq-fallback python3 (reorganize, monitor) stays broad + note|V62
T12|.|open upstream FR anthropics/claude-code: env-var expansion in skill frontmatter `allowed-tools`|V62

## §B BUGS

id|date|cause|fix
B1|2026-06-11|sub-skill flags inverted: `disable-model-invocation` hid auto-fire skills from Skill tool, kept slash surface|V61
B2|2026-06-11|marketplace root source `./` lstrip-emptied → plugin dropped from PUBLISHED scope|V63
B3|2026-06-11|§I id derivation hardcoded dev-repo slash-bullets → zero ids in consumer repos, colon ids uncitable|V41
B4|2026-06-11|backprop promised one commit; spec APPLY + build committed separately → 3 docs disagreed|V27
B5|2026-06-11|compression claim drift: measured ~30% vs legacy "quarter"/"4x" in README|-
B6|2026-06-11|check LOAD step 1 whole-file Read + step 4 `emit-v-slices` double-loaded SPEC.md every run; large spec re-hits Read pagination cap @ step 1|V64
B7|2026-06-11|batch narrow-scope override keyed on post-classification audit file-scope → LLM eyeballed repo file count as proxy|V46
B8|2026-06-11|clean §I rows classify MATCH but memo vocab lacked it → LLM silently remapped MATCH→HOLD, no doc stated mapping|V43
B9|2026-06-11|dirty run demanded full hand-merged table then refused write, exited 0 → unusable as CI gate|V44
B10|2026-06-11|frontmatter grant matched command name not arg pattern: `${CLAUDE_PLUGIN_ROOT}` no-expand in `allowed-tools` → broad `Bash(python3 *)` 4 skills; check carried zero-use `Bash(git *)`|V62
