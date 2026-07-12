# check-extras — §V body overflow

/sdd:condense-extracted §V row bodies for token-budget management. Consulted verbatim by /sdd:check sub-agents via RECIPE_EXCERPT. Row ordering: ascending §V id.

## §V3 verbatim-preservation

V3: verbatim-preservation — code, backticked text, paths, URLs, identifiers, numbers, versions, error strings, SQL, regex, JSON, YAML, quoted strings never compressed; backtick-wrapped tokens exempt every residue + cite audit.

## §V4 symbol-set

V4: symbol-set — telegraph (LLM-facing: SPEC.md, skill bodies) keeps `→ ≥ ≤ ! ? §`; human-facing prose (steno surfaces, CLAUDE.md, chat) spells out `→ ≥ ≤ &` as words, retains `|` for list/table separators + `§` for cites only; heavier math operators ! ASCII words.

## §V20 write-ownership

V20: write-ownership — /sdd:spec sole SPEC.md author; exclusions: /sdd:build flips one §T status cell per closed task; /sdd:condense + /sdd:reorganize apply operator-confirmed structural sweeps; /sdd:check + /sdd:explain write nothing; every skill auto-commit path-scoped to owned files (`git commit -m <subject> [-m <body>] -- <paths>` / `--only`; `-m` flags ! precede `--` — tokens after `--` parse as pathspecs, commit aborts) — bare `git add <paths>` + `git commit` banned (commits whole index → pre-staged file leaks into the scoped commit), subsumes per-skill `never git add -A` (closes §B.12, §B.13).

## §V23 decision-gate

V23: decision-gate — enumerable runtime choice ! AskUserQuestion w/ mutually-exclusive action labels; selection drives same-turn behavior; prose "or keep going?" forms banned. Discriminator: same-turn-effect choice (recipe paused mid-loop) → gate, never a passive Next list; next-turn operator-dispatch choice (recipe ended per recipe-step-no-dispatch) → Next block item.

## §V24 response-shape

V24: response-shape — user-typeable skill output ends `## Next` (1–5 atomic items, no `Reply` prefix, positional dispatch `run <int>` / `run /<plugin>:<cmd> [args]`); dispatched `<cmd>` + any "route through" prose name only `user-invocable` skills — auto-fire sub-skills (telegraph, backprop, socratic, steno, monitor, github) never a dispatch target (read-only, `user-invocable: false` per §V.61); bug→spec user route = `/sdd:spec <intent>` (gate→BACKPROP per §V.25), never `/sdd:backprop`; optional `## Hint` ≤ 3 lines precedes; multi-phase run {check, build `--all`, condense, reorganize} ! emit live harness checklist — TaskCreate per recipe phase @ start, TaskUpdate in_progress→completed @ transition; checklist ephemeral harness UI, never repo state, never substitutes REPORT or `## Next` (closes §B.14).

## §V27 backprop-protocol

V27: backprop-protocol — every bug → §B row; recurrence class → new or tightened §V preferred; two commits cross-cited: spec commit (§B + §V + §T) first, build commit (failing test first, then fix) cites the new rows.

## §V28 freshness-contract

V28: freshness-contract — live rows = clean current design; history → commit-msg bodies + archive; residue set {amendment-counter `(∆)`, dated-retirement, supersession-narration} pruned @ spec write, audited @ check, trimmed @ condense — one shared pattern set, owned by script.

## §V40 mechanical-realization

V40: mechanical-realization — deterministic audit rules realized once in `scripts/check-mechanical.py`; skill bodies + SPEC-FORMAT state contracts, never duplicate parser pseudo-code; per-run regex paraphrase banned.

## §V41 parametric-recipe

V41: parametric-recipe — published recipes + script name no repo-literal paths beyond SPEC.md + plugin-internal files; §I ids derive from kind prefixes, never hardcoded surface shapes; repo-specific enforcement → `.spec/scripts/check-extras.sh` + `.spec/check-extras.md`.

## §V42 scope-set

V42: scope-set — audit scopes: PUBLISHED (marketplace source dirs; root `./` → repo root), REPO-LOCAL (`.spec/**`, `.claude/**`, README.md, CLAUDE.md), SPEC-ADJACENT (SPEC.md, skill bodies, SPEC-FORMAT.md), GITHUB-FACING (README, issues, PRs, commit bodies); each audit names its scope.

## §V43 drift-verdict-vocab

V43: drift-verdict-vocab — dirty {VIOLATE, UNVERIFIABLE, UNRESOLVED, TYPE-MISMATCH, DRIFT, MISSING, STALE, EXTRA}; silent {HOLD, HOLD-SINCE-CLEAN, SCOPE-EMPTY, LATENT}; surfaced-clean {VIOLATE-CAPTURED}; §I-clean {MATCH} (§I rows only); script validates verdict admissibility per row type → no LLM-side remap; new verdict ! extend script vocab + this row same commit (closes §B.8).

## §V44 memo

V44: memo — `.spec/check-state.json` = cache, not truth; script owns both ends (read → invalidation advisories; write → clean runs only, per-row §V hashes, oversized-cell ack, `.gitignore` guard); `write-memo --from-audit` re-runs mechanical rows internally → stdin = behavioral verdicts only, hand-merge banned; exit 0 clean / 1 dirty (memo untouched, CI-gateable) / 2 invalid vocab; LLM never decides clean, never hand-writes memo (closes §B.9).

## §V45 scope-feed

V45: scope-feed — default-sweep scope = script-emitted rows (v_row_shas drift, flipped-since-clean, touched minus SPEC.md + archive sibling); comma-joined fields chain into `emit-v-slices --dirty`; LLM never hand-rolls `git diff`.

## §V46 batch

V46: batch — §V classification MAY parallelize; count = script audit `batch|ADVISORY|recommended: <n> agents` row: `ceil(|V|/15)` clamp [1, 4], PUBLISHED file census < `ceil(|V|/2)` → 1 agent; LLM never hand-computes count; contiguous spans, canonical prompt block copied verbatim (fill `{...}` only); failed batch re-runs serially (closes §B.7).

## §V48 token-budget

V48: token-budget — estimate = bytes / 3.4; > 20k tokens → check advisory → operator /sdd:condense; > 50 closed §T rows → window-vs-archive split; canonical values here, mirrored as script constants, retuned via AMEND + script sync same commit.

## §V49 extras-hook

V49: extras-hook — executable `.spec/scripts/check-extras.sh` runs inside script audit, rows appended verbatim (language-agnostic `id|verdict|evidence` contract); judgment-class extras live in `.spec/check-extras.md`, consulted by check + build pre-commit probe; condense-extracted §V bodies live here too, SPEC.md row left a `→ .spec/check-extras.md §V<n>` stub — /sdd:spec AMEND of a stub-redirected §V resolves the target to its body file + path-scopes write + commit there (check-extras.md, not SPEC.md) (closes §B.23).

## §V61 sub-skill-flags

V61: sub-skill-flags — auto-fire sub-skills (telegraph, backprop, socratic, steno, monitor, github) ! `user-invocable: false`, never `disable-model-invocation: true` (hides skill from Skill tool, breaks consumer engagement); description ! advertise user-request trigger phrasings owned by a user-invocable caller (selector weighs model-invocable sub-skill on user turns → colliding phrasing mis-dispatches, description-layer §B.14 class) — state caller-engagement instead (socratic-desc form).

## §V62 tooling-preference

V62: tooling-preference — pattern scans builtin Grep (harness-bundled ripgrep; consumer-installed `rg` never assumed); invert/exclusion scans (Grep lacks `-v`) → POSIX `grep -v -E` or two-pass Grep line-subtract; recipe patterns Rust-regex-expressible only — no lookaround/backref; JSON parse `jq`, fallback python3; audit core single-file stdlib-only python3; `allowed-tools` grant = pre-approval (auto-run listed tool sans prompt, never a restriction — unlisted tools stay callable per session perms), so narrowest pattern over body-prescribed invocations for prompt-control + intent-doc, zero-body-use grant banned (nothing to pre-approve); script-sole-use interpreter grant pins script path (mid-glob `Bash(python3 */check-mechanical.py *)` form); pin inexpressible (`${CLAUDE_PLUGIN_ROOT}` no-expand in frontmatter) → broad grant + inline note citing upstream limit; real tool denial = `disallowed-tools` (drops from pool, clears next user turn) — documented zero-writes (/sdd:check, /sdd:explain per §V.20) enforced via `disallowed-tools: Edit, Write`, not `allowed-tools` omission (omission only prompts) (closes §B.10).

## §V63 plugin-shape

V63: plugin-shape — PUBLISHED discovery parses `.claude-plugin/marketplace.json` `plugins[].source` (root `./` → repo root, nested path → subdir); plugin name from manifest, never assumed equal to dir name.

## §V64 single-load

V64: single-load — §V bodies enter run context via script `emit-v-slices` only; whole-file SPEC.md Read banned where script emit mode covers need; full read reserved to operator rewrite sweeps (/sdd:condense, /sdd:reorganize) (closes §B.6).

## §V65 monitor-protocol

V65: monitor-protocol — entry paths: auto-fire deviation (consumer-repo skill deviation → capture skill, version, expected vs actual) + dispatched `mechanization-candidate` (MECHANIZE `## Next` item only, consumer repo, never auto-fire, skips backprop hand-off; issue title `<skill>: mech candidate — <pattern>`); ! redact consumer paths/code/identifiers pre-publish; dedup `gh issue list` pre-file, hit → comment not new issue; AskUserQuestion gate every gh write (§V.23) surfacing resolved `--repo` target; gh-write target = manifest `.repository` (§V.41), asserted == resolved `--repo` immediately pre-write — repo named in deviation excerpt never bleeds into `<target>`; deviation path cwd = plugin repo → backprop hand-off (§V.27), no issue filed (closes §B.11).

## §V66 mechanize-scan

V66: mechanize-scan — user-invocable recipe ({design, spec, build, check, explain, condense, reorganize}) ends w/ MECHANIZE probe — canonical verbatim block per SKILL.md, sentinel `MECHANIZE` grep-sweepable; auto-fire sub-skills excluded; candidate = ≥ 2 same-shape deterministic calls (identical command modulo args) | LLM-side join/sort/count/dedup over script-emittable data | multi-step parse collapsible to one emit mode | fresh regex paraphrase (§V.40 class); hit → exactly one `## Next` item carrying observed pattern + proposed script mode, none → no item; never self-implement mid-run (§V.22, §V.20); routing: dev repo → /sdd:spec → §T row; consumer plugin-target → monitor dispatched path (§V.65); consumer repo-local → consumer /sdd:spec → extras row.

## §V67 human-clarity

V67: human-clarity — human-facing prose (steno surfaces, CLAUDE.md, chat) ! simple technical language: clarity primary, compression subordinate — a word that aids the skim stays; one idea/sentence, short sentences; plain words, no idiom/slang (per steno BOUNDARIES); symbols spelled out per symbol-set rule; technical term defined on first use or avoided; main point first, detail after; operator-asks-Claude-to-decide → state choice (1 sentence), options plainly, recommend (1 sentence). Canonical detail-carriers: steno skill body (register mechanics) + `CLAUDE.md` @ root (plain-imperative restatement governing chat/human-facing output, no telegraph). Sync obligation: any V1/V4/V67 amend ! same-commit re-sync of both carriers + sweep of skill-body register notes/examples. Spans GITHUB-FACING + REPO-LOCAL human surfaces; orthogonal to register-assignment + symbol-set rules.

## §V68 table-use

V68: table-use — info presented as prose or short list, never `|`-table; `|`-table reserved for keyed fixed-schema data rows (§T/§B/§I row schema, spec-skill audit table, similar id-keyed sets); prose-comparison or concept table → bullet list. Spans skill bodies (telegraph) + human-facing surfaces (steno, CLAUDE.md, README, chat); register-orthogonal — sibling to symbol-set + human-clarity rows, not subordinate.

## §V69 github-workflow

V69: github-workflow — passive `skills/github/SKILL.md` (`user-invocable: false`, auto-fire on gh issue/PR ops per sub-skill-flags invariant) governs gh-CLI workflow: issues via `gh issue create`, PRs via `gh pr create` to generic structures (github-facing bodies steno per github-facing-register invariant, PR body carries `Closes #<issue>`); per-PR branch via `gh issue develop <n> --checkout` (in-place checkout, one branch per session — no dedicated worktree); merge = `gh pr merge --squash --delete-branch` (commits squashed, branch deleted); unmerged close → `gh pr close` + `git branch -D <branch>`, no squash; issue/PR linkage = native `gh issue develop` linked branch + PR-body `Closes #<issue>`.
