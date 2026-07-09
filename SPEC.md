# SPEC — sdd plugin

## §G GOAL

LLM writes code faster than humans read → standards + logic drift unchecked; counter: one telegraph SPEC.md authoritative over code; plugin skills keep code shape + component contracts aligned over time.

## §C CONSTRAINTS

- installable Claude Code plugin marketplace; root-source plugin `sdd` (`.claude-plugin/marketplace.json`, source `./`)
- skills-only: every surface = `skills/<name>/SKILL.md`; no commands/ tree, no hooks
- `scripts/check-mechanical.py` single-file, stdlib-only python3
- no orchestrator, no swarm: main Claude executes; sub-agents read-only
- no state beyond SPEC.md + git + REPO-LOCAL `.spec/` cache

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
V3: verbatim-preservation — → `.claude/check-extras.md §V3`
V4: symbol-set — → `.claude/check-extras.md §V4`
V10: sole-source-of-truth — SPEC.md @ repo root is sole live spec; no docs/ tree, no sidecars; SPEC.archive.md sibling carries immutable archived rows only.
V11: shape-semantics-split — SPEC-FORMAT.md binds row shape + section catalog + citation grammar; §V rows bind semantics + enforcement; neither restates the other.
V12: monotonic-numbering — V/T/B ids strictly increasing in section order; gaps OK, reuse banned; sole renumber path = /sdd:reorganize (map append + cite sweep, same commit).
V13: cite-resolution — every cite ! resolve: `cites` tokens → live/archived V/T/B row or live §I kind, `fix` tokens → §V row, free-text `§<S>.<n>` → §<S> row; renumber sweeps citers same commit.
V14: pinned-cite-ban — PUBLISHED bodies ! placeholder (`§V.<n>`) or named-invariant form, never pinned §-digit cites; SPEC.md-narrative + REPO-LOCAL pinned cites ! resolve live.
V15: renumber-chain-walk — `.spec/spec-renumber-map.json` append-only; historical id resolves newest-first to live id or `archive` sentinel (→ SPEC.archive.md §V.retired block, never live row).
V16: archive-semantics — archived §T/§B + retired §V rows migrate verbatim to SPEC.archive.md w/ per-section markers per SPEC-FORMAT; archived rows stay cite-resolvable, never edited.
V20: write-ownership — → `.claude/check-extras.md §V20`
V21: write-serialize — SPEC.md + code writes serialize main-thread; reads delegable to read-only sub-agents.
V22: recipe-step-no-dispatch — slash-cmd dispatch = operator turn only; recipes end @ commit + Next block; sole exclusion: /sdd:build verify-fail routes cause to spec skill mid-loop.
V23: decision-gate — → `.claude/check-extras.md §V23`
V24: response-shape — → `.claude/check-extras.md §V24`
V25: socratic-gate — /sdd:spec mode {NEW, DISTILL, BACKPROP, AMEND, FOLD-IN} = gate byproduct of free-form `$ARGUMENTS`; no mode prefixes, no skip flags; concrete intent converges ≤ 1 turn.
V26: first-principle-probe — NEW mode fires foundational-claim question exactly once, declinable; `first-principle-asked` recorded regardless of answer.
V27: backprop-protocol — → `.claude/check-extras.md §V27`
V28: freshness-contract — → `.claude/check-extras.md §V28`
V29: fold-first — new §V row vs amend of closest existing row ! operator gate; split justification = §B recurrence cite or declared orthogonal concept; "mirrors existing row" alone insufficient.
V30: sweep-scope — sweep-class §T row ! declare scope as grep pattern or vocab table; named-procedure + named-site lists rejected.
V31: design-lifecycle — /sdd:design writes `designs/<slug>.md` only (write-new); fold-in mutates SPEC.md only; draft persists in working tree, operator disposes.
V40: mechanical-realization — → `.claude/check-extras.md §V40`
V41: parametric-recipe — → `.claude/check-extras.md §V41`
V42: scope-set — → `.claude/check-extras.md §V42`
V43: drift-verdict-vocab — → `.claude/check-extras.md §V43`
V44: memo — → `.claude/check-extras.md §V44`
V45: scope-feed — → `.claude/check-extras.md §V45`
V46: batch — → `.claude/check-extras.md §V46`
V47: check-dispatch — /sdd:check accepts bare (memo-driven) or `--full` (drop memo, re-classify all) only; other args bail.
V48: token-budget — → `.claude/check-extras.md §V48`
V49: extras-hook — → `.claude/check-extras.md §V49`
V60: skills-only — every surface = `skills/<name>/SKILL.md` dispatched natively as `/<plugin>:<name>`; no commands/ tree, no hooks, no orchestrator.
V61: sub-skill-flags — → `.claude/check-extras.md §V61`
V62: tooling-preference — → `.claude/check-extras.md §V62`
V63: plugin-shape — → `.claude/check-extras.md §V63`
V64: single-load — → `.claude/check-extras.md §V64`
V65: monitor-protocol — → `.claude/check-extras.md §V65`
V66: mechanize-scan — → `.claude/check-extras.md §V66`
V67: human-clarity — → `.claude/check-extras.md §V67`
V68: table-use — → `.claude/check-extras.md §V68`
V69: github-workflow — → `.claude/check-extras.md §V69`

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
T35|x|author `CLAUDE.md` @ repo root — plain-imperative restatement of V67 clarity standard for chat/human-facing output (point first, one idea/sentence, plain words, no idiom/slang, spell out `→ ≥ ≤ &`, expand acronyms on first use, cites to tail, operator-decide → state+options+recommend); sourced from V67 + steno body; no telegraph, no pinned `§`-digit cites (named-invariant form per V14); carries a stable marker block for the T36 audit|V67,B21
T36|x|script: audit asserts `CLAUDE.md` present @ root, carries the direct-instruction marker block, + symbol-clean (extends T32 naked-symbol scope `[→≥≤&]` to `CLAUDE.md`, wholly human-facing — symbol outside backtick-span + fenced block → VIOLATE; absent file → MISSING); emit `id|verdict|evidence` row + self-test; check audit consumes row|V67,V40,B21
T37|x|sweep README.md banned idiom/metaphor → literal phrasing per V67 BOUNDARIES — scope `grep -nE 'load-bearing|smell|earns its' README.md`: L19 `earns its tokens`, L25 `load-bearing`, L214/L297 `smells like`, L257 `earns its place` → plain restatement; backtick/fenced telegraph-example rows exempt|V67,B22
T38|x|script: audit asserts human-facing surface carries no banned exact-phrase idiom/jargon-idiom — scope `discover_human_facing` set (README.md, CLAUDE.md, plugin manifest), match curated low-false-positive BOUNDARIES subset (jargon-idiom + multi-word idiom exact phrases; ambiguous single words excluded, backtick-span/fenced exempt); emit `id|verdict|evidence` row + self-test; check audit consumes row, retires hand-run idiom grep|V67,V40,B22
T39|x|sweep leading-pipe prose tables → bullet list per table-use invariant — scope `grep -nE '^\|' skills/*/SKILL.md README.md CLAUDE.md`: pipe-table presenting prose comparison or concept set → bullet list; keyed fixed-schema data tables (§T/§B/§I schema, SPEC-FORMAT row tables, spec-skill audit table) left verbatim; fenced/backticked example tables exempt; design DISTINCTION FROM SOCRATIC table = first known target|V68,V3
T40|x|init `skills/github/SKILL.md`: passive (`user-invocable: false`) gh-CLI workflow governor — `gh issue create` + `gh pr create` generic structures, `gh issue develop <n> --checkout` + per-PR `git worktree`, `gh pr merge --squash --delete-branch` w/ worktree prune on merge, cleanup-only on unmerged close, `Closes #<issue>` linking|V69,V61,V2,V41
T41|x|patch `skills/spec/SKILL.md` AMEND + APPLY step 4 — resolve §V target to its body file (SPEC.md row vs `→ .claude/check-extras.md §V<n>` stub redirect); read/show/write the actual body + path-scope `git commit -- <body-file>` there, not unconditional SPEC.md|V49,V20,B23
T42|x|sweep `skills/github/SKILL.md` — drop git-worktree steps per §V.69 amend; scope `grep -nE 'worktree' skills/github/SKILL.md`: BRANCH `git worktree add` + path prose → `gh issue develop <n> --checkout` in-place only, MERGE `git worktree remove` → drop, CLOSE → `gh pr close` + `git branch -D`, frontmatter desc + NON-GOALS worktree mentions dropped|V69
T43|x|script: audit emits `scope|ADVISORY|v-path-dirty: V<n>,…` row — §V row-body path tokens (quoted/backticked path-like strings) intersect touched-set, computed script-side; check SCOPE step 1 consumes row i/o hand-run grep over §V section; + self-test|V45,V40
T44|.|move spec-owned files `.claude/` → `.spec/`: `git mv` check-extras.md + `.gitignore`; regenerable local check-state.json deleted; rewrite path refs — scope `grep -rn '\.claude/' skills/ scripts/ README.md SPEC.md` (25 SPEC.md stub rows + 22 skill-body refs + script strings/self-tests + 2 README lines); exempt `.claude/skills/**` (repo-local skill discovery) + backticked historical §B/closed-§T rows verbatim|V15,V41,V42,V44,V49

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
B22|2026-06-19|README.md prose carries banned idiom/metaphor (`load-bearing`, `smells like`, `earns its tokens`/`earns its place`) violating V67 BOUNDARIES; idiom ban human-review-only — mechanical audit scans symbol-set not enumerable banned-term sets → idiom drift undetected (B19/B21 symbol-scope sibling)|V67
B23|2026-06-22|spec AMEND + APPLY assume §V body in SPEC.md (write + `git commit -- SPEC.md`); /sdd:condense relocates §V bodies to `.claude/check-extras.md` + leaves stub row → amending condensed body (github enum add §V.61+§V.24) fell outside recipe write-scope, write + commit redirected to check-extras.md by hand|V49
