# SPEC — sdd plugin

## §G GOAL

LLM writes code faster than humans read → standards + logic drift unchecked; counter: one telegraph SPEC.md authoritative over code; plugin skills keep code shape + component contracts aligned over time.

## §C CONSTRAINTS

- installable Claude Code plugin marketplace; root-source plugin `sdd` (`.claude-plugin/marketplace.json`, source `./`)
- skills-only: every surface = `skills/<name>/SKILL.md`; no commands/ tree, no hooks
- `scripts/check-mechanical.py` single-file, stdlib-only python3
- no orchestrator, no swarm: main Claude executes; sub-agents read-only; exclusion: github post-spec-commit `/sdd:build` child on fold-produced §T ids write-capable; bundled `code-review` sub-agent scratch writes only (github-workflow invariant)
- no state beyond SPEC.md + git + REPO-LOCAL `.spec/` cache

## §I INTERFACES

external surface — what operator + consuming repo see.

- design: `/sdd:design <topic>` → Claude Code plan mode propose-critique → approved plan → hand title/body (Problem + Proposal + Design decisions + Effect + Out of scope + Unresolved when present)/Acceptance/class to github ISSUE + stop; later fold via `/sdd:spec github issue N` or same-session `/sdd:spec fold-design` (preserves issue N linkage; no default `designs/` write)
- spec: `/sdd:spec <intent>` → socratic gate → SPEC.md delta preview → apply + auto-commit; fold-design + micro-AMEND paths; `github issue N` / fold-design+issue N → push default branch then issue branch then one commit ahead of base (not spec delta) then draft PR (`Related: #<issue>`; no Closes; no review-at-create) before spec delta, including when SPEC.md missing; block runs once (open PR → switch and stop); SPEC.md present → draft + commit + PUSH; SPEC.md missing → no delta write; later NEW/DISTILL/AMEND/build on that branch PUSH; post-spec chain builds fold-produced §T ids (new + Acceptance-touched existing `.`) then review then READY; non-issue path: no BRANCH, no PR
- build: `/sdd:build [§T.n|§T.a,§T.b,…|--next|--all|--no-chain]` → plan → edit → verify → flip §T `.`→`x` + commit; green-path one hop per operator turn → check; issue-linked → PUSH per task, READY once post-loop (no check hop; Next merge phrasing); post-spec child (`POST-SPEC-CHILD=1`): fold-produced §T ids, implies `--no-chain`, PUSH only; task-scoped acceptance @ build; full acceptance @ MERGE only; MERGE probes checks + reviewDecision + mergeable
- check: `/sdd:check [--full|--no-chain]` → forked read-only recipe + script; REPORT + Next; clean chain → `## chain` hop line → main thread build --next
- explain: `/sdd:explain [§-cite|--next]` → prose expansion w/ cited siblings, zero writes
- condense: `/sdd:condense` → six-prong token sweep, single atomic commit
- reorganize: `/sdd:reorganize [--taxonomy-only]` → §V cluster + renumber + cite sweep (updates SPEC.md stubs and `.spec/check-extras.md` row prefixes), single atomic commit
- script: `python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-mechanical.py <mode>` → pipe-table `id|verdict|evidence`; modes: audit, write-memo, fix-sembr, emit-v-slices, emit-superseded, emit-fold-seeds, emit-v-weights, emit-row-ids, emit-overview, emit-token-estimate, emit-prune-patterns, emit-residue, emit-archive-window, emit-condense-propose, emit-check-agent-prompt, --self-test
- fragments: `skills/_fragments/*` shared recipe text (MECHANIZE, NEXT, CHAIN, ACCEPTANCE-GATE, POST-SPEC-CHAIN, …) — not slash surfaces
- format: `SPEC-FORMAT.md` → row shape + section catalog contract; loaded by spec, check, condense, reorganize

## §V INVARIANTS

numbered, testable, named; each ! hold. ids clustered by topic; gaps = cluster spans + closure history.

V1: spec-adjacent-register — → `.spec/check-extras.md §V1`
V2: github-facing-register — → `.spec/check-extras.md §V2`
V3: verbatim-preservation — → `.spec/check-extras.md §V3`
V4: symbol-set — → `.spec/check-extras.md §V4`
V10: sole-source-of-truth — → `.spec/check-extras.md §V10`
V11: shape-semantics-split — → `.spec/check-extras.md §V11`
V12: monotonic-numbering — → `.spec/check-extras.md §V12`
V13: cite-resolution — → `.spec/check-extras.md §V13`
V14: pinned-cite-ban — → `.spec/check-extras.md §V14`
V15: renumber-chain-walk — → `.spec/check-extras.md §V15`
V16: archive-semantics — → `.spec/check-extras.md §V16`
V20: write-ownership — → `.spec/check-extras.md §V20`
V21: write-serialize — → `.spec/check-extras.md §V21`
V22: recipe-step-no-dispatch — → `.spec/check-extras.md §V22`
V23: decision-gate — → `.spec/check-extras.md §V23`
V24: response-shape — → `.spec/check-extras.md §V24`
V25: socratic-gate — → `.spec/check-extras.md §V25`
V26: first-principle-probe — → `.spec/check-extras.md §V26`
V27: backprop-protocol — → `.spec/check-extras.md §V27`
V28: freshness-contract — → `.spec/check-extras.md §V28`
V29: fold-first — → `.spec/check-extras.md §V29`
V30: sweep-scope — → `.spec/check-extras.md §V30`
V31: design-lifecycle — → `.spec/check-extras.md §V31`
V40: mechanical-realization — → `.spec/check-extras.md §V40`
V41: parametric-recipe — → `.spec/check-extras.md §V41`
V42: scope-set — → `.spec/check-extras.md §V42`
V43: drift-verdict-vocab — → `.spec/check-extras.md §V43`
V44: memo — → `.spec/check-extras.md §V44`
V45: scope-feed — → `.spec/check-extras.md §V45`
V46: batch — → `.spec/check-extras.md §V46`
V47: check-dispatch — → `.spec/check-extras.md §V47`
V48: token-budget — → `.spec/check-extras.md §V48`
V49: extras-hook — → `.spec/check-extras.md §V49`
V60: skills-only — → `.spec/check-extras.md §V60`
V61: sub-skill-flags — → `.spec/check-extras.md §V61`
V62: tooling-preference — → `.spec/check-extras.md §V62`
V63: plugin-shape — → `.spec/check-extras.md §V63`
V64: single-load — → `.spec/check-extras.md §V64`
V65: monitor-protocol — → `.spec/check-extras.md §V65`
V66: mechanize-scan — → `.spec/check-extras.md §V66`
V67: human-clarity — → `.spec/check-extras.md §V67`
V68: table-use — → `.spec/check-extras.md §V68`
V69: github-workflow — → `.spec/check-extras.md §V69`
V70: sembr — → `.spec/check-extras.md §V70`
V71: consumer-core-profile — → `.spec/check-extras.md §V71`
V72: shared-fragments — → `.spec/check-extras.md §V72`
V73: backprop-resume-card — → `.spec/check-extras.md §V73`
V74: micro-amend — → `.spec/check-extras.md §V74`
V75: auto-fire-engage-log — → `.spec/check-extras.md §V75`
V76: thin-check — → `.spec/check-extras.md §V76`
V77: skill-effort — → `.spec/check-extras.md §V77`

## §T TASKS
## archived: §T.1..§T.20 → SPEC.archive.md (20 rows)

id|status|task|cites
T21|x|backprop frontmatter description: drop user trigger phrasings; state caller engagement via /sdd:spec BACKPROP|V24,V61,B14
T22|x|drop zero-body-use frontmatter grants; narrow release Bash grant; build Bash stays broad|V62
T23|x|patch read-only skill frontmatter — scope vocab {check, explain} (zero-writes per write-ownership invariant): add `disallowed-tools: Edit, Write` (`allowed-tools` omission only prompts, never denies); script-routed memo write + reads unaffected|V20,V62
T24|x|drop zero-body-use frontmatter grants left by prior grant sweep — scope `grep -nE '^allowed-tools:' skills/*/SKILL.md`: grant ∉ body invocation → drop (backprop `Skill`, design `Skill`, explain `Glob`+`Skill`)|V62
T25|x|drop surviving zero-body-use grants T24 sweep missed — scope `grep -nE '^allowed-tools:' skills/*/SKILL.md`: grant token ∉ body invocation → drop (backprop `Glob`; check `Glob`+`Skill` — `Agent` kept, Batch-protocol Explore spawns)|V62,B17
T26|x|script: audit flags zero-body-use `allowed-tools` grants + self-test|V62,V40,B17
T27|x|script: add `emit-token-estimate` mode — single-line `bytes/TOKEN_RATIO` estimate from SPEC.md; /sdd:compact LOAD baseline + check token-budget advisory consume it i/o `wc -c` + hand-division|V40,V48
T28|x|rename surface compact → condense|V60
T29|x|sweep stale 25k→20k token-budget advisory threshold across derivative docs — scope `grep -rn '25k' skills/ README.md`: condense SKILL.md (advisory prose + retune note), check SKILL.md (REPORT example), README ×2 → rewrite 20k per V48 canonical + script TOKEN_BUDGET mirror|V48
T30|x|patch skills/socratic/SKILL.md CONVERGENCE escape — replace prose "or keep going?" w/ AskUserQuestion gate (labels "Return now" / "Keep going") per V23 two-sided dispatch|V23,B18
T31|x|sweep human-facing surfaces → spell out symbols per V4/V67 — scope `grep -nE '[→≥≤&~]' README.md .claude-plugin/plugin.json`: prose `→`→word, `≥`→at least, `≤`→at most, `&`→and, `~N%`→about N%; backtick/fenced telegraph-example + ASCII-diagram rows exempt (verbatim)|V4,V67,B19
T32|x|script: audit flags naked symbols on human-facing surfaces + self-test|V4,V67,V40,B19
T33|x|fix `.claude-plugin/plugin.json` description token-cut figure 30%→40% to match measured benchmark (benchmarks/telegraph results JSON) — scope `grep -n 'token cut' .claude-plugin/plugin.json`|B20
T34|x|sweep steno + design bodies for symbol-set + clarity rules|V4,V67,B21
T35|x|author root `CLAUDE.md` clarity carrier w/ marker block|V67,B21
T36|x|script: audit `CLAUDE.md` presence + marker block + symbol-clean|V67,V40,B21
T37|x|sweep README.md banned idiom/metaphor → literal phrasing per V67 BOUNDARIES — scope `grep -nE 'load-bearing|smell|earns its' README.md`: L19 `earns its tokens`, L25 `load-bearing`, L214/L297 `smells like`, L257 `earns its place` → plain restatement; backtick/fenced telegraph-example rows exempt|V67,B22
T38|x|script: audit banned idiom phrases on human-facing surfaces + self-test|V67,V40,B22
T39|x|sweep prose pipe-tables → bullet lists|V68,V3
T40|x|init `skills/github` passive gh-CLI workflow governor|V69,V61,V2,V41
T41|x|patch `skills/spec/SKILL.md` AMEND + APPLY step 4 — resolve §V target to its body file (SPEC.md row vs `→ .claude/check-extras.md §V<n>` stub redirect); read/show/write the actual body + path-scope `git commit -- <body-file>` there, not unconditional SPEC.md|V49,V20,B23
T42|x|github skill: drop git-worktree steps|V69
T43|x|script: audit emits `scope|ADVISORY|v-path-dirty: V<n>,…` row — §V row-body path tokens (quoted/backticked path-like strings) intersect touched-set, computed script-side; check SCOPE step 1 consumes row i/o hand-run grep over §V section; + self-test|V45,V40
T44|x|move spec-owned files `.claude/` → `.spec/`|V15,V41,V42,V44,V49
T45|x|re-anchor steno + `CLAUDE.md` on simple technical language|V67,V2
T46|x|sweep repo `.md` prose → semantic line breaks per V70 — scope `grep -rlE '[.!?] [A-Z]' README.md CLAUDE.md designs/*.md skills/*/SKILL.md`: multi-sentence source line → one sentence per line; fenced blocks, `|`-tables, frontmatter + V70-exempt files untouched|V70
T47|x|script: audit emits sembr advisory row — scope V70 file set, prose line w/ ≥ 2 sentence terminators outside fence/`|`-table/frontmatter → ADVISORY `id|verdict|evidence` row + self-test; check audit consumes row i/o hand-run line scan|V70,V40
T48|x|script: add `fix-sembr` rewrite mode + self-test|V70,V40
T49|x|split oversized SKILL.md bodies → `references/`|V48,V1
T50|x|script: audit emits `skill-token|ADVISORY|<path> ~<n>k > 5k` per oversized published SKILL.md body — scope `skills/*/SKILL.md`, estimate bytes/3.4, threshold = V48 skill-body constant; + self-test; check audit consumes row i/o hand-run size check|V48,V40
T51|x|telegraph frontmatter `paths: [SPEC.md, SPEC-FORMAT.md]` — harness auto-load on matching-file touch replaces description-only auto-fire; probe plugin-skill `paths` support first, unsupported → record + drop|V61,V1
T52|x|eval harness: skill-creator `evals/evals.json` per user-invocable skill (output assertions, objectively checkable) + description trigger evals (8-10 should-trigger, 8-10 near-miss negatives, 3 runs each) — fire-rate baseline for auto-fire governors github + monitor first|V61,V65,V69
T53|x|`!` dynamic-context injection for deterministic recipe steps|V40,V62
T54|x|`context: fork` + `background: false` for /sdd:check — body + §V slices + batch outputs isolate to fork, REPORT returns as result; probe TaskCreate checklist + write-memo behavior in fork pre-adopt|V21,V64
T55|x|frontmatter + description hygiene sweep over user-invocable skills|V62
T56|x|probe `${CLAUDE_SKILL_DIR}` substitution in frontmatter Bash rules (supported v2.1.129+) — exact script-path pin expressible → sweep mid-glob `Bash(python3 */check-mechanical.py *)` grants to pinned form, amend V62 pin-inexpressible note same commit; not expressible → record result, keep mid-glob|V62
T57|x|sweep bare `Skill` grants → `Skill(sdd:*)` prefix form per V62 narrowest-grant — scope `grep -nE '^allowed-tools:.*Skill' skills/*/SKILL.md`|V62
T58|x|extend `discover_repo_local` walk to `.spec/**` per scope-set invariant + self-test asserting `.spec/check-extras.md` in cite-DAG file set — scope `grep -n 'def discover_repo_local' scripts/check-mechanical.py`|V42,B24
T59|x|sweep whole-file `Read SPEC.md` LOAD steps out of build + explain bodies → script `emit-overview` + `emit-v-slices` reads per single-load invariant — scope `grep -n 'Read .SPEC.md.' skills/build/SKILL.md skills/explain/SKILL.md`|V64,B25
T60|x|script: reconcile history-residue pattern set as sole member source (role-tag write-time fold rules vs audit-detect) + `emit-prune-patterns` mode + self-test — scope `grep -n 'HR_' scripts/check-mechanical.py`|V40,V28,B26
T61|x|sweep restated residue members + hand-coded retired-row regex → set name + script emit pointer per mechanical-realization invariant — scope vocab {skills/spec/references/write-time-prune.md, skills/condense/SKILL.md, skills/reorganize/SKILL.md}|V40,V28,B26
T62|x|port grok-fork workflow: init `skills/_fragments/` (MECHANIZE, NEXT, PROGRESS, PATH-SCOPED-COMMIT, CHAIN, CHECK-AGENT-PROMPT, UPSTREAM-FR, ACCEPTANCE-GATE, POST-SPEC-CHAIN); user-invocable skills point, never copy|V72,V66
T63|x|port issue-linked PR flow: github ISSUE/BRANCH/PR/PUSH/READY/MERGE/CLOSE + spec `github issue N` before-delta draft PR + post-spec chain + acceptance gate|V69,V21,V22,I.spec
T64|x|port build: multi-id args, `--no-chain`, resume card, POST-SPEC-CHILD, task-scoped acceptance, POST-LOOP READY|V22,V69,V73,I.build
T65|x|port check: `--no-chain`, `effort: medium`, green-path hop via REPORT `## chain` line from fork, explain-first remedies, reorganize advisory|V22,V47,V76,V77,I.check
T66|x|port design: plan mode (`EnterPlanMode`/`ExitPlanMode`) → github ISSUE + class label → stop; fold via `/sdd:spec github issue N` or `fold-design`; evals updated|V31,V69,I.design
T67|x|port spec: micro-AMEND, DISTILL second pass, Step 0b body-file porcelain, BACKPROP resume card, monitor mechanization-candidate route|V74,V73,V20,V65
T68|x|port script: merge grok-fork audits + emit modes (emit-residue, emit-archive-window, emit-condense-propose, emit-check-agent-prompt) w/ Claude modes (emit-prune-patterns, skill-token); design-lifecycle audit on `skills/design`; `--no-chain` accepted; self-test|V40,V31,V47,V69,V71,V77
T69|x|port auto-fire engage log (github, monitor, steno, telegraph) + caller-engagement descriptions|V75,V61
T70|x|frontmatter: drop `model:` lines from published skills; `effort: medium` on check + explain only|V77,V62
T71|x|apply PR #9 review findings (sdd-only audit gate, CLAUDE.md audit, §B cite shift, single chain owner, memo blanks, archive markers, slice lines, prompt source, CI)|V71,V67,V13,V69,V44,V16,V64,V72

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
B21|2026-06-19|human-facing skill bodies + absent CLAUDE.md predate symbol + clarity amend|V67
B22|2026-06-19|README banned idiom; audit scanned symbols not idiom set|V67
B23|2026-06-22|spec AMEND assumed §V body in SPEC.md; condense stubs redirect to check-extras|V49
B24|2026-08-04|script REPO-LOCAL discovery hand-mirrored scope-set row w/o sync tie; T44 `.claude/`→`.spec/` move updated path strings, not the `discover_repo_local` walk → `.spec/check-extras.md` cites escaped cite-DAG sweep|V42
B25|2026-08-04|single-load authoring sweep scoped to check LOAD only — build + explain LOAD step 1 kept whole-file `Read SPEC.md`; sibling recipes unswept @ amend, B19/B21 under-scope class|V64
B26|2026-08-04|declared single-source residue set had no consumable script emission — three prose surfaces restated members + reorganize hand-coded retired-row regex; copies diverged (fold rule prose-only, lineage condense-only, `PF_RETIRED_INPLACE` script-only)|V40
B27|2026-07-21|MECHANIZE byte-identity forced multi-skill copy-paste; DRIFT class on any edit drift|V66,V72
B28|2026-07-21|/sdd:design slash-only + designs/ file fought plan mode; no GitHub issue hand-off|V31
B29|2026-07-21|discover_sembr_files omits skills/_fragments/**; multi-sentence fragment lines unaudited|V70
B30|2026-07-21|condense+reorganize copy PROGRESS/NEXT body instead of _fragments pointer|V72
B31|2026-07-21|telegraph+steno frontmatter advertise user-says triggers; collide w/ caller dispatch|V61
B32|2026-07-21|closed-§T archive threshold 50 hardcode in condense; not script constant per V48|V48
B33|2026-07-21|PROGRESS pointer sweep left task-checklist grant without body literal on condense+reorganize|V62
B34|2026-07-21|Closes #N / issue close w/o Acceptance audit → silent-pass|V69
B35|2026-08-22|post-spec-commit chain copied into APPLY + POST-APPLY → double build+review|V69
B36|2026-08-22|spec-side post-spec chain omitted READY remainder|V69
B37|2026-08-22|V21 read-only default blocked review sub-agent scratch writes|V21
B38|2026-08-22|post-spec build child had no discriminator; took operator-run READY path|V69
B39|2026-08-23|squash-merge default subject PR title `(#PR)`; `Closes #<issue>` on PR body not squash commit → git log cannot recover closed issue|V69
B40|2026-08-23|acceptance-gate trigger keyed on close trailer after close trailer banned on build commits|V69
B41|2026-08-23|emit-v-weights ranks already-stubbed §V rows as heavy|V48
B42|2026-08-23|grant-use audit extras-only; recipes omit required grants|V62
B43|2026-08-23|github CLOSE `git branch -D` while still on issue-linked branch; git refuses delete current branch|V69
B44|2026-08-23|Next "merge when approved" has no user-invocable dispatch; github auto-fire only|V24,V69
B45|2026-08-23|build issue-linked READY inside per-task loop; `--all` re-runs review+pr-ready each row|V69,V22
B46|2026-08-23|V47 check-dispatch bare/`--full` only; §I+skill+README accept `--no-chain`|V47
B47|2026-08-23|CHAIN "at most one hop" vs two default edges; hop depth per turn vs per recipe unclear|V22,V24
B48|2026-08-23|condense NON-GOALS all-or-none firing set; CONFIRM offers force-skip + subset|-
B49|2026-08-23|condense prong 6 consumes pre-fold v-weights while prong 1 claims fold-first reshape|V48
B50|2026-08-23|monitor "5th member" roster omits github; V61 lists six auto-fire skills|V61
B51|2026-08-23|post-spec child `/sdd:build --all` closes whole backlog into one issue PR|V69
B52|2026-08-23|POST-SPEC-CHILD inherits green-path chain; child may hop check then build --next|V21,V22,V69
B53|2026-08-23|spec Step 0 porcelain checks SPEC.md only; stub AMEND body file uncommitted work leaks|V20,V49
B54|2026-08-23|spec github fold: branch vs delta-write order underspecified; dirty checkout risk|V69,V20
B55|2026-08-23|ACCEPTANCE-GATE COMMENT posts every ALLOW; build per-task gate → N comments per `--all`|V69
B56|2026-08-23|design POST-APPROVE duplicates github ISSUE create steps; dual ownership drift class|V31,V72,V69
B57|2026-08-23|design prescribes plan-file write/patch; allowed-tools omits write; grant audit pattern misses|V62
B58|2026-08-23|github body `<n>` means issue id and PR id in different sections|V69
B59|2026-08-23|build+explain whole-file SPEC.md Read; single-load prefers script emit where covered|V64
B60|2026-08-23|reorganize CONFIRM subset re-emits CONFIRM inside no-mid-flow-reprompt gate|V23
B61|2026-08-23|V69+§I+ACCEPTANCE-GATE claim full accept @ PR ready; task-scoped recipes = MERGE-only full gate|V69
B62|2026-08-23|V25 lists FOLD-IN as socratic mode; FOLD-IN is dispatch shortcut bypassing gate|V25
B63|2026-08-23|check description "never invokes" remedies; body+V22 green-path chain invokes build|V22,V76
B64|2026-08-23|spec POST-APPLY names FOLD-IN github issue only; fold-design+issue N same issue-linked path under-specified|V31,V69
B65|2026-08-23|post-spec child fail → parent Next build-only; no BACKPROP offer for class b/c|V21,V27,V69
B66|2026-08-23|issue-linked READY hops `/sdd:check`; check Next drops merge phrasing|V22,V24,V69
B67|2026-08-23|README Issue-linked PR still says post-spec `/sdd:build --all`|V69
B68|2026-08-23|design ISSUE body drops Effect + Out of scope + Unresolved; fold from issue sees reduced plan|V31
B69|2026-08-23|READY remainder unless-operator-declines vs post-spec no-wait|V69
B70|2026-08-23|fold-produced ids omit existing `.` §T rows that received Acceptance notes; MERGE blocks after ready|V69
B71|2026-08-23|READY review-apply then `gh pr ready` with no re-verify|V69
B72|2026-08-23|MERGE runs `gh pr merge` with no probe of checks or `reviewDecision` or mergeable|V69
B73|2026-08-23|CLOSE deletes local branch only; remote branch remains|V69
B74|2026-08-23|post-spec child fail reports to parent session; draft PR has no GitHub comment|V21,V69
B75|2026-09-04|run_audit plugin-skill + README audits fire when plugin_dirs empty → consumer check always dirty|V71
B76|2026-09-12|consumer README symbols/idiom still fire when plugin_dirs empty after V71 skip → memo blocked|V71
B77|2026-10-08|github-issue spec fold defers draft PR until after spec commit; missing SPEC.md skips PR so later modes commit off the issue branch|V69
