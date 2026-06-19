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
- condense: `/sdd:condense` → six-prong token sweep, single atomic commit
- reorganize: `/sdd:reorganize [--taxonomy-only]` → §V cluster + renumber + cite sweep, single atomic commit
- script: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py <mode>` → pipe-table `id|verdict|evidence`; modes: audit, write-memo, emit-v-slices, emit-superseded, emit-fold-seeds, emit-v-weights, emit-row-ids, emit-overview, emit-token-estimate, --self-test
- format: `SPEC-FORMAT.md` → row shape + section catalog contract; loaded by spec, check, condense, reorganize

## §V INVARIANTS

numbered, testable, named; each ! hold. ids clustered by topic; gaps = cluster spans + closure history.

V1: spec-adjacent-register — SPEC.md, `skills/**/SKILL.md`, SPEC-FORMAT.md, spec-referencing prose ! telegraph per telegraph skill; /sdd:explain decodes on demand.
V2: github-facing-register — README, issues, PRs, commit-msg bodies ! steno per steno skill; commit subjects = per-skill fixed templates, verbatim.
V3: verbatim-preservation — code, backticked text, paths, URLs, identifiers, numbers, versions, error strings, SQL, regex, JSON, YAML, quoted strings never compressed; backtick-wrapped tokens exempt every residue + cite audit.
V4: symbol-set — telegraph (LLM-facing: SPEC.md, skill bodies) keeps `→ ≥ ≤ ! ? §`; human-facing prose (steno surfaces, CLAUDE.md, chat) spells out `→ ≥ ≤ &` as words, retains `|` for list/table separators + `§` for cites only; heavier math operators ! ASCII words.
V10: sole-source-of-truth — SPEC.md @ repo root is sole live spec; no docs/ tree, no sidecars; SPEC.archive.md sibling carries immutable archived rows only.
V11: shape-semantics-split — SPEC-FORMAT.md binds row shape + section catalog + citation grammar; §V rows bind semantics + enforcement; neither restates the other.
V12: monotonic-numbering — V/T/B ids strictly increasing in section order; gaps OK, reuse banned; sole renumber path = /sdd:reorganize (map append + cite sweep, same commit).
V13: cite-resolution — every cite ! resolve: `cites` tokens → live/archived V/T/B row or live §I kind, `fix` tokens → §V row, free-text `§<S>.<n>` → §<S> row; renumber sweeps citers same commit.
V14: pinned-cite-ban — PUBLISHED bodies ! placeholder (`§V.<n>`) or named-invariant form, never pinned §-digit cites; SPEC.md-narrative + REPO-LOCAL pinned cites ! resolve live.
V15: renumber-chain-walk — `.claude/spec-renumber-map.json` append-only; historical id resolves newest-first to live id or `archive` sentinel (→ SPEC.archive.md §V.retired block, never live row).
V16: archive-semantics — archived §T/§B + retired §V rows migrate verbatim to SPEC.archive.md w/ per-section markers per SPEC-FORMAT; archived rows stay cite-resolvable, never edited.
V20: write-ownership — → `.claude/check-extras.md §V20`
V21: write-serialize — SPEC.md + code writes serialize main-thread; reads delegable to read-only sub-agents.
V22: recipe-step-no-dispatch — slash-cmd dispatch = operator turn only; recipes end @ commit + Next block; sole exclusion: /sdd:build verify-fail routes cause to spec skill mid-loop.
V23: decision-gate — enumerable runtime choice ! AskUserQuestion w/ mutually-exclusive action labels; selection drives same-turn behavior; prose "or keep going?" forms banned. Discriminator: same-turn-effect choice (recipe paused mid-loop) → gate, never a passive Next list; next-turn operator-dispatch choice (recipe ended per recipe-step-no-dispatch) → Next block item.
V24: response-shape — → `.claude/check-extras.md §V24`
V25: socratic-gate — /sdd:spec mode {NEW, DISTILL, BACKPROP, AMEND, FOLD-IN} = gate byproduct of free-form `$ARGUMENTS`; no mode prefixes, no skip flags; concrete intent converges ≤ 1 turn.
V26: first-principle-probe — NEW mode fires foundational-claim question exactly once, declinable; `first-principle-asked` recorded regardless of answer.
V27: backprop-protocol — every bug → §B row; recurrence class → new or tightened §V preferred; two commits cross-cited: spec commit (§B + §V + §T) first, build commit (failing test first, then fix) cites the new rows.
V28: freshness-contract — → `.claude/check-extras.md §V28`
V29: fold-first — new §V row vs amend of closest existing row ! operator gate; split justification = §B recurrence cite or declared orthogonal concept; "mirrors existing row" alone insufficient.
V30: sweep-scope — sweep-class §T row ! declare scope as grep pattern or vocab table; named-procedure + named-site lists rejected.
V31: design-lifecycle — /sdd:design writes `designs/<slug>.md` only (write-new); fold-in mutates SPEC.md only; draft persists in working tree, operator disposes.
V40: mechanical-realization — deterministic audit rules realized once in `scripts/check-mechanical.py`; skill bodies + SPEC-FORMAT state contracts, never duplicate parser pseudo-code; per-run regex paraphrase banned.
V41: parametric-recipe — published recipes + script name no repo-literal paths beyond SPEC.md + plugin-internal files; §I ids derive from kind prefixes, never hardcoded surface shapes; repo-specific enforcement → `.claude/scripts/check-extras.sh` + `.claude/check-extras.md`.
V42: scope-set — audit scopes: PUBLISHED (marketplace source dirs; root `./` → repo root), REPO-LOCAL (`.claude/**`, README.md, CLAUDE.md), SPEC-ADJACENT (SPEC.md, skill bodies, SPEC-FORMAT.md), GITHUB-FACING (README, issues, PRs, commit bodies); each audit names its scope.
V43: drift-verdict-vocab — → `.claude/check-extras.md §V43`
V44: memo — → `.claude/check-extras.md §V44`
V45: scope-feed — default-sweep scope = script-emitted rows (v_row_shas drift, flipped-since-clean, touched minus SPEC.md + archive sibling); comma-joined fields chain into `emit-v-slices --dirty`; LLM never hand-rolls `git diff`.
V46: batch — → `.claude/check-extras.md §V46`
V47: check-dispatch — /sdd:check accepts bare (memo-driven) or `--full` (drop memo, re-classify all) only; other args bail.
V48: token-budget — estimate = bytes / 3.4; > 20k tokens → check advisory → operator /sdd:condense; > 50 closed §T rows → window-vs-archive split; canonical values here, mirrored as script constants, retuned via AMEND + script sync same commit.
V49: extras-hook — executable `.claude/scripts/check-extras.sh` runs inside script audit, rows appended verbatim (language-agnostic `id|verdict|evidence` contract); judgment-class extras live in `.claude/check-extras.md`, consulted by check + build pre-commit probe.
V60: skills-only — every surface = `skills/<name>/SKILL.md` dispatched natively as `/<plugin>:<name>`; no commands/ tree, no hooks, no orchestrator.
V61: sub-skill-flags — → `.claude/check-extras.md §V61`
V62: tooling-preference — → `.claude/check-extras.md §V62`
V63: plugin-shape — PUBLISHED discovery parses `.claude-plugin/marketplace.json` `plugins[].source` (root `./` → repo root, nested path → subdir); plugin name from manifest, never assumed equal to dir name.
V64: single-load — §V bodies enter run context via script `emit-v-slices` only; whole-file SPEC.md Read banned where script emit mode covers need; full read reserved to operator rewrite sweeps (/sdd:condense, /sdd:reorganize) (closes §B.6).
V65: monitor-protocol — → `.claude/check-extras.md §V65`
V66: mechanize-scan — → `.claude/check-extras.md §V66`
V67: human-clarity — human-facing prose (steno surfaces, CLAUDE.md, chat) ! clarity standard: one idea/sentence, short sentences; plain words, no idiom/slang (per steno BOUNDARIES); symbols spelled out per symbol-set rule; technical term defined on first use or avoided; main point first, detail after; operator-asks-Claude-to-decide → state choice (1 sentence), options plainly, recommend (1 sentence). Canonical detail-carriers: steno skill body (register mechanics) + `CLAUDE.md` @ root (plain-imperative restatement governing chat/human-facing output, no telegraph). Sync obligation: any V1/V4/V67 amend ! same-commit re-sync of both carriers + sweep of skill-body register notes/examples. Spans GITHUB-FACING + REPO-LOCAL human surfaces; orthogonal to register-assignment + symbol-set rules.

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
T10|x|script: write-memo dirty → exit 1 (memo untouched), invalid vocab stays 2; self-test covers exit codes|V44
T11|x|sweep frontmatter grants — scope `rg -n 'Bash\(' skills/*/SKILL.md`: zero-use → drop (check `Bash(git *)`); script-sole-use python3 → mid-glob pin (check, compact); jq-fallback python3 (reorganize, monitor) stays broad + note|V62
T12|x|open upstream FR anthropics/claude-code: env-var expansion in skill frontmatter `allowed-tools`|V62
T13|x|patch `skills/monitor/SKILL.md`: assert resolved gh-write `--repo` target == manifest `.repository` immediately pre-write + GATE surfaces resolved target; reject excerpt-named repo|V65,B11
T14|x|sweep skill auto-commits to path-scoped `git commit -- <paths>`; scope `rg -n 'git add' skills/*/SKILL.md .claude/skills/*/SKILL.md`; bare `git add X && git commit` → path-scoped form|V20,B12
T15|x|sweep rg → builtin Grep — scope `grep -nE 'rg [-*]' skills/*/SKILL.md`: body `rg --pcre2` invocations → Grep tool calls; invert pre-filters → `grep -v -E`; grants `Bash(rg *)` → `Bash(grep *)` (spec, reorganize); closed §T/§B rows verbatim-exempt|V62,V3
T16|x|sweep: copy canonical MECHANIZE block into user-invocable SKILL.md set — scope `grep -L 'MECHANIZE' skills/*/SKILL.md` minus `user-invocable: false` frontmatter|V66,V30
T17|x|patch `skills/monitor/SKILL.md`: add dispatched `mechanization-candidate` entry path (REDACT → TARGET → DEDUP → GATE → WRITE, title `<skill>: mech candidate — <pattern>`); auto-fire deviation path byte-untouched|V65,V66
T18|x|sweep path-scoped commit recipes — pin `-m <subject> [-m <body>]` before `--`; scope `grep -n 'git commit -- ' skills/*/SKILL.md`: build, compact, reorganize unpinned → insert before `--` (spec, release already pinned)|V20,V30
T19|x|script: audit mode asserts every user-invocable SKILL.md carries byte-identical canonical MECHANIZE block — scope `grep -L 'MECHANIZE' skills/*/SKILL.md` minus `user-invocable: false`, block md5 uniform across set; emit `id|verdict|evidence` row (DRIFT divergent, MISSING absent) + self-test; check audit consumes row, retires hand-run `awk|md5|uniq` verbatim check|V66,V40
T20|x|script: audit asserts no skill body slash-dispatches an auto-fire sub-skill — scope `grep -rnE '/sdd:(telegraph|backprop|socratic|steno|monitor)\b' skills/*/SKILL.md`, non-backtick hit → VIOLATE (slash form never user-invocable); emit `id|verdict|evidence` row + self-test; check audit consumes row, retires hand-grep|V24,V40,B14
T21|x|reframe `skills/backprop/SKILL.md` frontmatter description — drop user-entry trigger phrasings colliding w/ /sdd:spec (`X broke`, `we got bit by`, `post-mortem on Y`, `this should never recur`, `add a §V for`); restate sub-skill engaged via /sdd:spec BACKPROP mode (socratic-desc form: caller-engaged, not user-invoked); skill body byte-untouched|V24,V61,B14
T22|x|sweep frontmatter allowed-tools grants — scope `grep -nE '^allowed-tools:' skills/*/SKILL.md .claude/skills/release/SKILL.md`: drop inert zero-body-use `Skill` grant (telegraph, steno, socratic); narrow release `Bash` → body-prescribed subset; build `Bash` stays broad (consumer verify cmds unpinnable) + inline note|V62
T23|x|patch read-only skill frontmatter — scope vocab {check, explain} (zero-writes per write-ownership invariant): add `disallowed-tools: Edit, Write` (`allowed-tools` omission only prompts, never denies); script-routed memo write + reads unaffected|V20,V62
T24|x|drop zero-body-use frontmatter grants left by prior grant sweep — scope `grep -nE '^allowed-tools:' skills/*/SKILL.md`: grant ∉ body invocation → drop (backprop `Skill`, design `Skill`, explain `Glob`+`Skill`)|V62
T25|x|drop surviving zero-body-use grants T24 sweep missed — scope `grep -nE '^allowed-tools:' skills/*/SKILL.md`: grant token ∉ body invocation → drop (backprop `Glob`; check `Glob`+`Skill` — `Agent` kept, Batch-protocol Explore spawns)|V62,B17
T26|x|script: audit asserts no frontmatter `allowed-tools` grant is zero-body-use — scope `grep -nE '^allowed-tools:' skills/*/SKILL.md .claude/skills/release/SKILL.md`, grant token ∉ skill-body invocation → VIOLATE; emit `id|verdict|evidence` row + self-test; check audit consumes row, retires hand-run grant sweep|V62,V40,B17
T27|x|script: add `emit-token-estimate` mode — single-line `bytes/TOKEN_RATIO` estimate from SPEC.md; /sdd:compact LOAD baseline + check token-budget advisory consume it i/o `wc -c` + hand-division|V40,V48
T28|x|rename surface compact→condense: scope `grep -rln 'compact' skills/ scripts/ README.md .claude/ .claude-plugin/ SPEC-FORMAT.md`; rewrite skill-name forms (`/sdd:compact`, dir `skills/compact/`, frontmatter `name:`, prose "compactor"); leave generic-word + benchmark-fixture + SPEC.md closed-§T rows verbatim|V60
T29|x|sweep stale 25k→20k token-budget advisory threshold across derivative docs — scope `grep -rn '25k' skills/ README.md`: condense SKILL.md (advisory prose + retune note), check SKILL.md (REPORT example), README ×2 → rewrite 20k per V48 canonical + script TOKEN_BUDGET mirror|V48
T30|x|patch skills/socratic/SKILL.md CONVERGENCE escape — replace prose "or keep going?" w/ AskUserQuestion gate (labels "Return now" / "Keep going") per V23 two-sided dispatch|V23,B18
T31|x|sweep human-facing surfaces → spell out symbols per V4/V67 — scope `grep -nE '[→≥≤&~]' README.md .claude-plugin/plugin.json`: prose `→`→word, `≥`→at least, `≤`→at most, `&`→and, `~N%`→about N%; backtick/fenced telegraph-example + ASCII-diagram rows exempt (verbatim)|V4,V67,B19
T32|x|script: audit asserts human-facing surface carries no non-exempt naked symbol — scope `grep -nE '[→≥≤&~]' README.md .claude-plugin/plugin.json`, symbol outside backtick-span + fenced block → VIOLATE; emit `id|verdict|evidence` row + self-test; check audit consumes row, retires hand-run symbol sweep|V4,V67,V40,B19
T33|x|fix `.claude-plugin/plugin.json` description token-cut figure 30%→40% to match measured benchmark (benchmarks/telegraph results JSON) — scope `grep -n 'token cut' .claude-plugin/plugin.json`|B20
T34|x|sweep human-facing skill bodies per V4/V67 — scope `grep -lnE '[→≥≤&]' skills/steno/SKILL.md skills/design/SKILL.md`: steno SYMBOLS spell out `→ ≥ ≤ &` as words (retain `| §` raw, drop `→ leads-to` symbol def), EXAMPLES raw `&`→`and` + `prod`→`production`, add acronym-expand-on-first-use rule, tighten BOUNDARIES tech-vocab exclusion to closed list + ban observed idiom (load-bearing, by-construction, hand-rolled, clean-slate, prior-art, carry-cost), add QUESTION shape (plain decision first, options plainly, cites to tail), add cite-placement rule (cite rides tail, never carries the sentence); design register note `readable symbols → & §` → spelled-out form; fenced telegraph-policy blocks + `§`/`|` exempt|V4,V67,B21
T35|.|author `CLAUDE.md` @ repo root — plain-imperative restatement of V67 clarity standard for chat/human-facing output (point first, one idea/sentence, plain words, no idiom/slang, spell out `→ ≥ ≤ &`, expand acronyms on first use, cites to tail, operator-decide → state+options+recommend); sourced from V67 + steno body; no telegraph, no pinned `§`-digit cites (named-invariant form per V14); carries a stable marker block for the T36 audit|V67,B21
T36|.|script: audit asserts `CLAUDE.md` present @ root, carries the direct-instruction marker block, + symbol-clean (extends T32 naked-symbol scope `[→≥≤&]` to `CLAUDE.md`, wholly human-facing — symbol outside backtick-span + fenced block → VIOLATE; absent file → MISSING); emit `id|verdict|evidence` row + self-test; check audit consumes row|V67,V40,B21

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
B11|2026-06-11|monitor gh-write hit upstream `anthropics/claude-code` not plugin `.repository` — target unasserted pre-write, excerpt-named repo bled into `<target>`|V65
B12|2026-06-11|/sdd:check-created `.claude/.gitignore` guard swept into next backprop spec commit — `git add SPEC.md` + bare `git commit` commits whole index not just SPEC.md|V20
B13|2026-06-12|path-scoped commit recipe `git commit -- <paths>` gave msg separately → `-m` appended after `--` parsed as pathspec, commit aborts; bit release (fixed) + spec|V20
B14|2026-06-13|Next-block + "route through" prose named `/sdd:backprop F5` as user dispatch; backprop read-only + `user-invocable: false`, real route `/sdd:spec <intent>`→BACKPROP|V24
B15|2026-06-13|`allowed-tools` cast as access-restriction (least-privilege) in tooling-preference invariant; CC 2.1.177 = pre-approval grant (auto-run, never denies) — real tool denial = `disallowed-tools`|V62
B16|2026-06-13|grant sweep scoped to {telegraph,steno,socratic}, left zero-body-use `Skill`/`Glob` grants in backprop/design/explain unenforced|V62
B17|2026-06-13|T24 grant sweep under-covered — dropped backprop `Skill` but left `Glob`; check `Glob`+`Skill` never in scope; no mechanical audit enforces V62, manual sweeps miss rows|V62
B18|2026-06-17|socratic CONVERGENCE escape used prose "or keep going?" decision form; predated V23 two-sided-dispatch amendment — same-turn-effect mid-loop choice must be AskUserQuestion gate|V23
B19|2026-06-18|README.md + manifest description predate V4/V67 symbol-set amendment — naked `→` in prose + `~N%` approximations never swept post-amend|V67
B20|2026-06-18|manifest description token-cut figure stale (30%) vs measured ~40%; B5-class claim drift|-
B21|2026-06-19|human-facing skill bodies (steno SYMBOLS+EXAMPLES, design register note `readable symbols → & §`) + absent CLAUDE.md predate/diverge from V4/V67 symbol+clarity amend; symbol-audit T32 scopes README + manifest only → clarity detail-carriers never re-synced post-amend, design emitted telegraph chat proposal (session-example.md): raw `→ ≡ ·`, bare acronyms, idiom, cite-led sentences|V67
