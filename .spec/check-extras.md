# check-extras — §V body overflow

/sdd:condense-extracted §V row bodies for token-budget management. Consulted verbatim by /sdd:check sub-agents via RECIPE_EXCERPT. Row ordering: ascending §V id.

## §V1 spec-adjacent-register

V1: spec-adjacent-register — SPEC.md, `skills/**/SKILL.md`, SPEC-FORMAT.md, spec-referencing prose ! telegraph per telegraph skill; /sdd:explain decodes on demand.

## §V2 github-facing-register

V2: github-facing-register — README, issues, PRs, commit-msg bodies ! steno per steno skill; commit subjects = per-skill fixed templates, verbatim.

## §V3 verbatim-preservation

V3: verbatim-preservation — code, backticked text, paths, URLs, identifiers, numbers, versions, error strings, SQL, regex, JSON, YAML, quoted strings never compressed; backtick-wrapped tokens exempt every residue + cite audit.

## §V4 symbol-set

V4: symbol-set — telegraph (LLM-facing: SPEC.md, skill bodies) keeps `→ ≥ ≤ ! ? §`; human-facing prose (steno surfaces, CLAUDE.md, chat) spells out `→ ≥ ≤ &` as words, retains `|` for list/table separators + `§` for cites only; heavier math operators ! ASCII words.

## §V10 sole-source-of-truth

V10: sole-source-of-truth — SPEC.md @ repo root is sole live spec; no docs/ tree, no sidecars; SPEC.archive.md sibling carries immutable archived rows only.

## §V11 shape-semantics-split

V11: shape-semantics-split — SPEC-FORMAT.md binds row shape + section catalog + citation grammar; §V rows bind semantics + enforcement; neither restates the other.

## §V12 monotonic-numbering

V12: monotonic-numbering — V/T/B ids strictly increasing in section order; gaps OK, reuse banned; sole renumber path = /sdd:reorganize (map append + cite sweep, same commit).

## §V13 cite-resolution

V13: cite-resolution — every cite ! resolve: `cites` tokens → live/archived V/T/B row or live §I kind, `fix` tokens → §V row, free-text `§<S>.<n>` → §<S> row; renumber sweeps citers same commit.

## §V14 pinned-cite-ban

V14: pinned-cite-ban — PUBLISHED bodies ! placeholder (`§V.<n>`) or named-invariant form, never pinned §-digit cites; SPEC.md-narrative + REPO-LOCAL pinned cites ! resolve live.

## §V15 renumber-chain-walk

V15: renumber-chain-walk — `.spec/spec-renumber-map.json` append-only; historical id resolves newest-first to live id or `archive` sentinel (→ SPEC.archive.md §V.retired block, never live row).

## §V16 archive-semantics

V16: archive-semantics — archived §T/§B + retired §V rows migrate verbatim to SPEC.archive.md w/ per-section markers per SPEC-FORMAT; archived rows stay cite-resolvable, never edited.

## §V20 write-ownership

V20: write-ownership — /sdd:spec sole SPEC.md author; exclusions: /sdd:build flips one §T status cell per closed task; /sdd:condense + /sdd:reorganize apply operator-confirmed structural sweeps; /sdd:check + /sdd:explain write nothing; every skill auto-commit path-scoped to owned files (`git commit -m <subject> [-m <body>] -- <paths>` / `--only`; `-m` flags ! precede `--` — tokens after `--` parse as pathspecs, commit aborts) — bare `git add <paths>` + `git commit` banned (commits whole index → pre-staged file leaks into the scoped commit), subsumes per-skill `never git add -A` (closes §B.12, §B.13).

## §V21 write-serialize

V21: write-serialize — SPEC.md + code writes serialize main-thread; reads delegable to read-only sub-agents; exclusion: github post-spec-commit chain runs write-capable `/sdd:build` child on fold-produced §T ids (`POST-SPEC-CHILD=1` implies `--no-chain`) and bundled `code-review` sub-agent (scratch writes only, no repo edits; spawn general-purpose Agent, not read-only Explore); child build verification failure halts and reports to parent session without mid-loop interactive prompts or SPEC.md writes; parent posts `gh pr comment` on draft PR then Next leads `/sdd:build` and, when fail class b/c, `/sdd:spec` BACKPROP (github-workflow invariant) (closes §B.37, §B.65, §B.74).

## §V22 recipe-step-no-dispatch

V22: recipe-step-no-dispatch — slash-cmd dispatch = operator turn only; recipes end @ commit + Next block; exclusions: (1) /sdd:build verify-fail → mid-loop spec BACKPROP; (2) green-path chain default-on per `skills/_fragments/CHAIN.md` — one hop per operator turn (hopped recipe never hops again): operator build pass → check and stop; operator check clean + pending `.` §T → build --next and stop; `--no-chain` disables; `POST-SPEC-CHILD=1` implies `--no-chain`; issue-linked READY (operator-run or post-spec remainder) implies no check hop — merge Next remains (closes §B.66); dirty check never auto-remedy; (3) github post-spec-commit chain — spec APPLY commit + draft PR → run write-capable `/sdd:build` on fold-produced §T ids then bundled `code-review` sub-agent (skip on doc-or-comment diff per github-workflow invariant) then github READY remainder same session; no operator re-type (closes §B.36, §B.47, §B.52).

## §V23 decision-gate

V23: decision-gate — enumerable runtime choice ! AskUserQuestion w/ mutually-exclusive action labels; selection drives same-turn behavior; prose "or keep going?" forms banned. Discriminator: same-turn-effect choice (recipe paused mid-loop) → gate, never a passive Next list; next-turn operator-dispatch choice (recipe ended per recipe-step-no-dispatch) → Next block item.

## §V24 response-shape

V24: response-shape — user-typeable skill output ends `## Next` (1–5 atomic items, no `Reply` prefix, positional dispatch `run <int>` / `run /sdd:<cmd> [args]`); canonical contract in `skills/_fragments/NEXT.md`; dispatched `<cmd>` names only `user-invocable` skills — auto-fire sub-skills never a dispatch target; sole non-slash exception = issue-linked merge pause item naming the operator phrasing that auto-fires github MERGE (e.g. say "merge the PR"); issue-linked READY Next item #1 = that phrasing; `/sdd:check` listed not hopped (closes §B.14, §B.44, §B.66); bug→spec user route = `/sdd:spec <intent>`, never `/sdd:backprop`; optional `## Hint` ≤ 3 lines precedes; multi-phase run {check, build `--all`, condense, reorganize} ! emit live harness checklist per PROGRESS fragment; BACKPROP Next leads with concrete `/sdd:build §T.n` (resume card); green-path chain one hop per operator turn per CHAIN fragment.

## §V25 socratic-gate

V25: socratic-gate — /sdd:spec gate modes {NEW, DISTILL, BACKPROP, AMEND} = gate byproduct of free-form `$ARGUMENTS`; FOLD-IN (fold-design, designs/*, github issue N) = DISPATCH shortcut bypassing socratic; no mode prefixes, no skip flags; concrete intent converges ≤ 1 turn (closes §B.62).

## §V26 first-principle-probe

V26: first-principle-probe — NEW mode fires foundational-claim question exactly once, declinable; `first-principle-asked` recorded regardless of answer.

## §V27 backprop-protocol

V27: backprop-protocol — every bug → §B row; recurrence class → new or tightened §V preferred; two commits cross-cited: spec commit (§B + §V + §T) first, build commit (failing test first, then fix) cites the new rows.

## §V28 freshness-contract

V28: freshness-contract — live rows = clean current design; history → commit-msg bodies + archive; residue set {amendment-counter `(∆)`, dated-retirement, supersession-narration} pruned @ spec write, audited @ check, trimmed @ condense — one shared pattern set, owned by script.

## §V29 fold-first

V29: fold-first — new §V row vs amend of closest existing row ! operator gate; split justification = §B recurrence cite or declared orthogonal concept; "mirrors existing row" alone insufficient.

## §V30 sweep-scope

V30: sweep-scope — sweep-class §T row ! declare scope as grep pattern or vocab table; named-procedure + named-site lists rejected.

## §V31 design-lifecycle

V31: design-lifecycle — /sdd:design uses Claude Code plan mode (`EnterPlanMode` → harness plan file → `ExitPlanMode`); primary artifact = session plan, not `designs/`; plan mode owns plan-file writes (harness); post-approve ! hand title + steno body + `## Acceptance` + class to github ISSUE (github owns `gh label create` + `gh issue create --label`; default class enhancement); ISSUE body = Problem + Proposal + Design decisions + Effect on in-flight SPEC items + Out of scope + Unresolved when present + `## Acceptance` from Success criterion; then stop; Next leads issue URL + `/sdd:spec github issue N`; same-session `/sdd:spec fold-design` retains created issue N linkage; legacy `designs/*.md` still folds; optional `designs/<slug>.md` export on operator ask (closes §B.56, §B.68).

## §V40 mechanical-realization

V40: mechanical-realization — deterministic audit rules realized once in `scripts/check-mechanical.py`; skill bodies + SPEC-FORMAT state contracts, never duplicate parser pseudo-code; per-run regex paraphrase banned; script-owned pattern/member sets enter prose by set name + emit-mode pointer only, member enumeration never restated (closes §B.26).

## §V41 parametric-recipe

V41: parametric-recipe — published recipes + script name no repo-literal paths beyond SPEC.md + plugin-internal files; §I ids derive from kind prefixes, never hardcoded surface shapes; repo-specific enforcement → `.spec/scripts/check-extras.sh` + `.spec/check-extras.md`.

## §V42 scope-set

V42: scope-set — audit scopes: PUBLISHED (marketplace source dirs; root `./` → repo root), REPO-LOCAL (`.spec/**`, `.claude/**`, README.md, CLAUDE.md), SPEC-ADJACENT (SPEC.md, skill bodies, SPEC-FORMAT.md), GITHUB-FACING (README, issues, PRs, commit bodies); each audit names its scope; scope-membership edit ! same-commit script discovery-fn + self-test sync (closes §B.24).

## §V43 drift-verdict-vocab

V43: drift-verdict-vocab — dirty {VIOLATE, UNVERIFIABLE, UNRESOLVED, TYPE-MISMATCH, DRIFT, MISSING, STALE, EXTRA}; silent {HOLD, HOLD-SINCE-CLEAN, SCOPE-EMPTY, LATENT}; surfaced-clean {VIOLATE-CAPTURED}; §I-clean {MATCH} (§I rows only); script validates verdict admissibility per row type → no LLM-side remap; new verdict ! extend script vocab + this row same commit (closes §B.8).

## §V44 memo

V44: memo — `.spec/check-state.json` = cache, not truth; script owns both ends (read → invalidation advisories; write → clean runs only, per-row §V hashes, oversized-cell ack, `.gitignore` guard); `write-memo --from-audit` re-runs mechanical rows internally → stdin = behavioral verdicts only, hand-merge banned; exit 0 clean / 1 dirty (memo untouched, CI-gateable) / 2 invalid vocab; LLM never decides clean, never hand-writes memo (closes §B.9).

## §V45 scope-feed

V45: scope-feed — default-sweep scope = script-emitted rows (v_row_shas drift, flipped-since-clean, touched minus SPEC.md + archive sibling); comma-joined fields chain into `emit-v-slices --dirty`; LLM never hand-rolls `git diff`.

## §V46 batch

V46: batch — §V classification MAY parallelize; count = script audit `batch|ADVISORY|recommended: <n> agents` row: `ceil(|V|/15)` clamp [1, 4], PUBLISHED file census < `ceil(|V|/2)` → 1 agent; LLM never hand-computes count; contiguous spans, canonical prompt block copied verbatim (fill `{...}` only); failed batch re-runs serially (closes §B.7).

## §V47 check-dispatch

V47: check-dispatch — /sdd:check accepts bare (memo-driven), `--full` (drop memo, re-classify all), `--no-chain` (suppress green-path hop), or `--full --no-chain`; other args bail; arg set single-sourced as script `CHECK_DISPATCH_ARGS` (closes §B.46).

## §V48 token-budget

V48: token-budget — estimate = bytes / 3.4; SPEC.md > 20k tokens → check advisory → operator /sdd:condense; > 50 closed §T rows → window-vs-archive split; published SKILL.md body > 5k tokens → check advisory → conditional detail splits to `references/` one level deep (harness compaction re-attaches first 5k tokens per skill); condense prong 6 heavy set = prefix of live §V rows ranked desc byte-weight whose cum first reaches ≥ 50% of §V-section total, excluding already-stubbed `→ .spec/check-extras.md §V<n>` rows (stub = extraction-complete; re-extract no-op); canonical values (20k, 50 closed §T, 5k skill body, 50% heavy, stub-skip) here, mirrored as script constants (`emit-v-weights` owns heavy+stub-skip), retuned via AMEND + script sync same commit (closes §B.41).

## §V49 extras-hook

V49: extras-hook — executable `.spec/scripts/check-extras.sh` runs inside script audit, rows appended verbatim (language-agnostic `id|verdict|evidence` contract); judgment-class extras live in `.spec/check-extras.md`, consulted by check + build pre-commit probe; condense-extracted §V bodies live here too, SPEC.md row left a `→ .spec/check-extras.md §V<n>` stub — /sdd:spec AMEND of a stub-redirected §V resolves the target to its body file + path-scopes write + commit there (check-extras.md, not SPEC.md); /sdd:reorganize renumbering sweeps both SPEC.md stub pointers and `.spec/check-extras.md` heading/row prefixes (closes §B.23).

## §V60 skills-only

V60: skills-only — every surface = `skills/<name>/SKILL.md` dispatched natively as `/<plugin>:<name>`; no commands/ tree, no hooks, no orchestrator.

## §V61 sub-skill-flags

V61: sub-skill-flags — auto-fire sub-skills (telegraph, backprop, socratic, steno, monitor, github) ! `user-invocable: false`, never `disable-model-invocation: true` (hides skill from Skill tool, breaks consumer engagement); description ! advertise user-request trigger phrasings owned by a user-invocable caller (selector weighs model-invocable sub-skill on user turns → colliding phrasing mis-dispatches, description-layer §B.14 class) — state caller-engagement instead (socratic-desc form).

## §V62 tooling-preference

V62: tooling-preference — pattern scans builtin Grep (harness-bundled ripgrep; consumer-installed `rg` never assumed); invert/exclusion scans (Grep lacks `-v`) → POSIX `grep -v -E` or two-pass Grep line-subtract; recipe patterns Rust-regex-expressible only — no lookaround/backref; JSON parse `jq`, fallback python3; audit core single-file stdlib-only python3; `allowed-tools` grant = pre-approval (auto-run listed tool sans prompt, never a restriction — unlisted tools stay callable per session perms); grant set = body-prescribed catalogued tools (coverage + zero-body-use) — missing grant → VIOLATE (prescribed spawn/edit/write ! auto-run); extra grant → VIOLATE (nothing to pre-approve); script `classify_grants` both directions (closes §B.42); script-sole-use interpreter grant pins the exact script path via `${CLAUDE_SKILL_DIR}` / `${CLAUDE_PROJECT_DIR}` frontmatter substitution (CC v2.1.129+; same variable in grant + body cmd so the rule matches the run; pre-2.1.129 rule stays literal → prompts, never denies); pin inexpressible → mid-glob `Bash(python3 */check-mechanical.py *)` fallback + inline note citing the limit; real tool denial = `disallowed-tools` (drops from pool, clears next user turn) — documented zero-writes (/sdd:check, /sdd:explain per §V.20) enforced via `disallowed-tools: Edit, Write`, not `allowed-tools` omission (omission only prompts); upstream product FR (platform limit class, e.g. env no-expand) ! submit via Claude Code feedback channel when programmatically reachable — recipe auto-sends under operator gate (decision-gate invariant), human `/feedback` paste = fallback only when channel unavailable (closes §B.10).

## §V63 plugin-shape

V63: plugin-shape — PUBLISHED discovery parses `.claude-plugin/marketplace.json` (else `.claude-plugin/plugin.json`) `plugins[].source` (root `./` → repo root, nested path → subdir); plugin name from manifest, never assumed equal to dir name.

## §V64 single-load

V64: single-load — §V bodies enter run context via script `emit-v-slices` only; whole-file SPEC.md Read banned where script emit mode covers need; full read reserved to operator rewrite sweeps (/sdd:condense, /sdd:reorganize) and /sdd:explain cited-sibling expansion (no emit covers cross-section prose); /sdd:build census via `emit-overview`, SPEC.md read only for status-cell write path (closes §B.6, §B.59).

## §V65 monitor-protocol

V65: monitor-protocol — entry paths: auto-fire deviation (consumer-repo skill deviation → capture skill, version, expected vs actual) + dispatched `mechanization-candidate` (engaged via `/sdd:spec mechanization-candidate` from MECHANIZE `## Next` item, consumer repo, skips backprop hand-off; issue title `<skill>: mech candidate — <pattern>`); ! redact consumer paths/code/identifiers pre-publish; dedup `gh issue list` pre-file, hit → comment not new issue; AskUserQuestion gate every gh write (§V.23) surfacing resolved `--repo` target; gh-write target = manifest `.repository` (§V.41), asserted == resolved `--repo` immediately pre-write — repo named in deviation excerpt never bleeds into `<target>`; deviation path cwd = plugin repo → backprop hand-off (§V.27), no issue filed (closes §B.11).

## §V66 mechanize-scan

V66: mechanize-scan — user-invocable recipe ({design, spec, build, check, explain, condense, reorganize}) ends w/ MECHANIZE probe; canonical criteria live once in `skills/_fragments/MECHANIZE.md`; each skill carries `## MECHANIZE` section pointing at that fragment (script audits pointer presence — MISSING/DRIFT — not multi-file byte-identity; closes §B.27); auto-fire sub-skills excluded; candidate = ≥ 2 same-shape deterministic calls | LLM-side join/sort/count/dedup over script-emittable data | multi-step parse collapsible to one emit mode | fresh regex paraphrase (mechanical-realization class); hit → exactly one `## Next` item with pattern + proposed script mode; never self-implement mid-run; routing: dev repo → /sdd:spec → §T; consumer plugin-target → /sdd:spec mechanization-candidate; consumer repo-local → consumer /sdd:spec → extras.

## §V67 human-clarity

V67: human-clarity — human-facing prose (steno surfaces, chat, README when present) ! simple technical language: clarity primary, compression subordinate — a word that aids the skim stays; one idea/sentence, short sentences; plain words, no idiom/slang (per steno BOUNDARIES); symbols spelled out per symbol-set rule; technical term defined on first use or avoided; main point first, detail after; operator-asks-Grok-to-decide → state choice (1 sentence), options plainly, recommend (1 sentence). Canonical detail-carrier: steno skill body (register mechanics). Sync obligation: any V1/V4/V67 amend ! same-commit re-sync of steno skill + sweep of skill-body register notes/examples. CLAUDE.md optional (Grok project rules); if present, scanned as human-facing; presence + marker block not required. Spans GITHUB-FACING + REPO-LOCAL human surfaces; orthogonal to register-assignment + symbol-set rules.

## §V68 table-use

V68: table-use — info presented as prose or short list, never `|`-table; `|`-table reserved for keyed fixed-schema data rows (§T/§B/§I row schema, spec-skill audit table, similar id-keyed sets); prose-comparison or concept table → bullet list. Spans skill bodies (telegraph) + human-facing surfaces (steno, CLAUDE.md, README, chat); register-orthogonal — sibling to symbol-set + human-clarity rows, not subordinate.

## §V69 github-workflow

V69: github-workflow — passive `skills/github/SKILL.md` (`user-invocable: false`, auto-fire on gh issue/PR ops per sub-skill-flags invariant) governs gh-CLI workflow: issues via `gh issue create` (body problem + `## Acceptance` lines; design hands payload to github ISSUE including Effect + Out of scope + Unresolved when present); every worked GitHub issue ! one issue-linked PR; no corresponding GitHub issue → no git branch + no `gh pr create` (work stays current branch; plain git commit still in scope); `/sdd:spec github issue N` or fold-design with issue N first action = draft PR before spec delta, once, including when `SPEC.md` missing (clean tree): open PR for the issue → `git switch` that branch and stop (no second `gh issue develop`, no second empty commit, no second `gh pr create`); else fetch, fast-forward `<default-base>` when behind, `git push origin <default-base>` only when ahead (named refspec; never bare `git push`; rejected or diverged → stop and report; already up to date → success; no force), then BRANCH `gh issue develop <issue> --checkout` (in-place, one branch per session), then one commit ahead of that base on a still-clean tree (not the spec delta; `git commit --allow-empty` satisfies; a staged index must not ride that commit; `gh pr create` rejects zero-ahead), then `gh pr create --draft` (generic structure; github-facing bodies steno; `Related: #<issue>` line; no `Closes`/`Fixes`/`Resolves` trailer @ create; no Acceptance copy; no secondary Closes; no review-at-create); SPEC.md present → spec drafting continues on that branch (preview, write delta, path-scoped commit) then PUSH to the open PR; SPEC.md missing → do not write a delta and do not invent SPEC.md; next NEW or DISTILL on that branch creates it and PUSHes; later AMEND and build PUSH; no second PR; then run write-capable `/sdd:build §T.<a>,§T.<b>,…` on fold-produced §T ids (new rows this fold + existing `.` rows that received Acceptance notes this fold; not whole backlog; spawn prompt ! `POST-SPEC-CHILD=1` implies `--no-chain`; child drops READY; failure halts to parent — parent `gh pr comment` steno on draft PR + Next `/sdd:build` and class b/c `/sdd:spec` BACKPROP) then bundled `code-review` sub-agent then READY remainder; bundled `code-review` skips on a doc-or-comment diff (post-spec remainder and operator-run READY): every changed path in {`SPEC.md`, `SPEC.archive.md`, `.spec/check-extras.md`, `SPEC-FORMAT.md`, `README.md`, `CLAUDE.md`, `designs/**`} or every changed line outside that set is comment or whitespace; `skills/**`, any script, or any other non-comment line → review runs; skip continues READY remainder (no findings; re-run verify; pass → push + `gh pr ready`); operator `/review` unchanged; MERGE `reviewDecision` probe unchanged; chain runs once after the spec commit on the open PR — owner github PR recipe; spec stops before the chain (draft PR already open) (closes §B.35, §B.36, §B.38, §B.51, §B.52, §B.67, §B.70, §B.74, §B.77); later issue-linked commits `git push` (PUSH); READY remainder: post-spec apply open bug + suggestion, list nits, no wait; operator-run READY ? wait nits; then re-run task verify — fail → no `gh pr ready`; pass → push + `gh pr ready`; operator-run issue-linked READY once per run not per task; issue-linked READY implies no green-path check hop — Next merge phrasing leads (closes §B.66, §B.69, §B.71); issue-linked task build = task-scoped acceptance evidence only; full acceptance gate = MERGE / issue close only (not PR ready; closes §B.61); build commit never carries close trailer; MERGE = ACCEPTANCE-GATE then probe `gh pr checks <pr>` + `gh pr view <pr> --json reviewDecision,mergeable` (empty checks skip; required reviews missing or CHANGES_REQUESTED or unmergeable → BLOCK, no merge) then add `Closes #<issue>` then `gh pr merge <pr> --squash --delete-branch --subject "<title> (#<issue>)" --body "Closes #<issue>"` (closes §B.39, §B.72); evidence comment once per issue-linked run (closes §B.55); unmerged CLOSE → `gh pr close <pr> --delete-branch` then `git switch <default-base>` then `git branch -D <branch>` (closes §B.43, §B.73); placeholders `<issue>` vs `<pr>` never dual `<n>` (closes §B.58); consumer-repo no hardcoded owner/repo (parametric-recipe invariant).

## §V70 sembr

V70: sembr — repo `.md` prose source lines ! semantic line breaks (sembr.org): one sentence per line, clause-boundary break OK; source-format only — rendered output unchanged; scope: README.md, CLAUDE.md, `designs/*.md`, `skills/**/SKILL.md`, `skills/_fragments/**`; exempt: pipe-row files (SPEC.md, SPEC.archive.md, `.spec/check-extras.md`), fenced blocks, `|`-tables, frontmatter; GitHub issue/PR/comment bodies out of scope (GFM renders single newline as hard break); register-orthogonal — sibling to table-use.

## §V71 consumer-core-profile

V71: consumer-core-profile — core loop = design? → spec → build → check → explain; maintenance = condense/reorganize; plugin-meta (UPSTREAM-FR fragment, monitor issue path for plugin repo) loads only when cwd is plugin `.repository` or operator targets plugin; consumer non-plugin repos skip UPSTREAM-FR body weight; plugin-internal mechanical audits (skill-body + plugin-README needles; ids `design-lifecycle`, `github-workflow`, `write-serialize`, condense-stub `token`, README Issue-linked PR, `symbols`, `idiom`) skip when `plugin_dirs(repo_root)` empty — empty → no row (not MISSING/VIOLATE); plugin repo (non-empty `plugin_dirs`) still emits (README, CLAUDE.md, manifests for `symbols`/`idiom`); consumer extras-hook + cite-DAG + history + token-budget + memo/scope-feed stay; `sembr` ADVISORY stays (closes §B.75, §B.76).

## §V72 shared-fragments

V72: shared-fragments — canonical cross-skill recipe text lives in `skills/_fragments/` (MECHANIZE, NEXT, PROGRESS, PATH-SCOPED-COMMIT, CHAIN, CHECK-AGENT-PROMPT, UPSTREAM-FR, ACCEPTANCE-GATE, POST-SPEC-CHAIN); single-skill conditional detail lives in that skill's `references/` per token-budget invariant; user-invocable skills point, never copy, never paraphrase after pointer; restated §V body in skill → named-invariant cite only; NON-GOALS + audit rationale state unique boundaries, never reprint recipe above; `_fragments` is not a slash surface.

## §V73 backprop-resume-card

V73: backprop-resume-card — BACKPROP APPLY writes `.spec/backprop-handoff.json` `{B,V,T,test_name_hint}`; Next leads with concrete `/sdd:build §T.n`; build LOAD consumes + deletes on close; card is resume pointer, not design truth; `.spec/.gitignore` lists `backprop-handoff.json` from first `.spec/` write (NEW/DISTILL init or first BACKPROP, whichever first).

## §V74 micro-amend

V74: micro-amend — single-§ single-line AMEND with no new §V row uses shortened APPLY gate (preview + Apply-led AskUserQuestion; skip fold-first); structural modes keep full gate.

## §V75 auto-fire-engage-log

V75: auto-fire-engage-log — auto-fire sub-skills (telegraph, steno, monitor, github) emit one telegraph `engaged sdd:<name>` line when they fire so the operator sees the governor.

## §V76 thin-check

V76: thin-check — check SKILL.md is phase + script orchestration; conditional detail in `skills/check/references/` one level deep (token-budget invariant); sub-agent prompt from `emit-check-agent-prompt` / CHECK-AGENT-PROMPT fragment; runs `context: fork` read-only — green-path hop returns via REPORT `## chain` line, main thread dispatches build.

## §V77 skill-effort

V77: skill-effort — published `skills/*/SKILL.md` leave frontmatter `model` unset (session model inherits); `explain` + `check` set `effort: medium`; every other skill leaves `effort` unset; script audit VIOLATE on any frontmatter `model:` line, on `explain`/`check` effort other than `medium`, or on any other skill `effort:` line; README honored-frontmatter sentence names `effort`; audit skips when `plugin_dirs()` empty (per consumer-core-profile invariant).
