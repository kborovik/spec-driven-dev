# check-extras — §V body overflow

/sdd:condense-extracted §V row bodies for token-budget management. Consulted verbatim by /sdd:check sub-agents via RECIPE_EXCERPT. Row ordering: ascending §V id.

## §V20 write-ownership

V20: write-ownership — /sdd:spec sole SPEC.md author; exclusions: /sdd:build flips one §T status cell per closed task; /sdd:condense + /sdd:reorganize apply operator-confirmed structural sweeps; /sdd:check + /sdd:explain write nothing; every skill auto-commit path-scoped to owned files (`git commit -m <subject> [-m <body>] -- <paths>` / `--only`; `-m` flags ! precede `--` — tokens after `--` parse as pathspecs, commit aborts) — bare `git add <paths>` + `git commit` banned (commits whole index → pre-staged file leaks into the scoped commit), subsumes per-skill `never git add -A` (closes §B.12, §B.13).

## §V24 response-shape

V24: response-shape — user-typeable skill output ends `## Next` (1–5 atomic items, no `Reply` prefix, positional dispatch `run <int>` / `run /<plugin>:<cmd> [args]`); dispatched `<cmd>` + any "route through" prose name only `user-invocable` skills — auto-fire sub-skills (telegraph, backprop, socratic, steno, monitor) never a dispatch target (read-only, `user-invocable: false` per §V.61); bug→spec user route = `/sdd:spec <intent>` (gate→BACKPROP per §V.25), never `/sdd:backprop`; optional `## Hint` ≤ 3 lines precedes; multi-phase run {check, build `--all`, condense, reorganize} ! emit live harness checklist — TaskCreate per recipe phase @ start, TaskUpdate in_progress→completed @ transition; checklist ephemeral harness UI, never repo state, never substitutes REPORT or `## Next` (closes §B.14).

## §V28 freshness-contract

V28: freshness-contract — live rows = clean current design; history → commit-msg bodies + archive; residue set {amendment-counter `(∆)`, dated-retirement, supersession-narration} pruned @ spec write, audited @ check, trimmed @ condense — one shared pattern set, owned by script.

## §V43 drift-verdict-vocab

V43: drift-verdict-vocab — dirty {VIOLATE, UNVERIFIABLE, UNRESOLVED, TYPE-MISMATCH, DRIFT, MISSING, STALE, EXTRA}; silent {HOLD, HOLD-SINCE-CLEAN, SCOPE-EMPTY, LATENT}; surfaced-clean {VIOLATE-CAPTURED}; §I-clean {MATCH} (§I rows only); script validates verdict admissibility per row type → no LLM-side remap; new verdict ! extend script vocab + this row same commit (closes §B.8).

## §V44 memo

V44: memo — `.claude/check-state.json` = cache, not truth; script owns both ends (read → invalidation advisories; write → clean runs only, per-row §V hashes, oversized-cell ack, `.gitignore` guard); `write-memo --from-audit` re-runs mechanical rows internally → stdin = behavioral verdicts only, hand-merge banned; exit 0 clean / 1 dirty (memo untouched, CI-gateable) / 2 invalid vocab; LLM never decides clean, never hand-writes memo (closes §B.9).

## §V46 batch

V46: batch — §V classification MAY parallelize; count = script audit `batch|ADVISORY|recommended: <n> agents` row: `ceil(|V|/15)` clamp [1, 4], PUBLISHED file census < `ceil(|V|/2)` → 1 agent; LLM never hand-computes count; contiguous spans, canonical prompt block copied verbatim (fill `{...}` only); failed batch re-runs serially (closes §B.7).

## §V61 sub-skill-flags

V61: sub-skill-flags — auto-fire sub-skills (telegraph, backprop, socratic, steno, monitor) ! `user-invocable: false`, never `disable-model-invocation: true` (hides skill from Skill tool, breaks consumer engagement); description ! advertise user-request trigger phrasings owned by a user-invocable caller (selector weighs model-invocable sub-skill on user turns → colliding phrasing mis-dispatches, description-layer §B.14 class) — state caller-engagement instead (socratic-desc form).

## §V62 tooling-preference

V62: tooling-preference — pattern scans builtin Grep (harness-bundled ripgrep; consumer-installed `rg` never assumed); invert/exclusion scans (Grep lacks `-v`) → POSIX `grep -v -E` or two-pass Grep line-subtract; recipe patterns Rust-regex-expressible only — no lookaround/backref; JSON parse `jq`, fallback python3; audit core single-file stdlib-only python3; `allowed-tools` grant = pre-approval (auto-run listed tool sans prompt, never a restriction — unlisted tools stay callable per session perms), so narrowest pattern over body-prescribed invocations for prompt-control + intent-doc, zero-body-use grant banned (nothing to pre-approve); script-sole-use interpreter grant pins script path (mid-glob `Bash(python3 */check-mechanical.py *)` form); pin inexpressible (`${CLAUDE_PLUGIN_ROOT}` no-expand in frontmatter) → broad grant + inline note citing upstream limit; real tool denial = `disallowed-tools` (drops from pool, clears next user turn) — documented zero-writes (/sdd:check, /sdd:explain per §V.20) enforced via `disallowed-tools: Edit, Write`, not `allowed-tools` omission (omission only prompts) (closes §B.10).

## §V65 monitor-protocol

V65: monitor-protocol — entry paths: auto-fire deviation (consumer-repo skill deviation → capture skill, version, expected vs actual) + dispatched `mechanization-candidate` (MECHANIZE `## Next` item only, consumer repo, never auto-fire, skips backprop hand-off; issue title `<skill>: mech candidate — <pattern>`); ! redact consumer paths/code/identifiers pre-publish; dedup `gh issue list` pre-file, hit → comment not new issue; AskUserQuestion gate every gh write (§V.23) surfacing resolved `--repo` target; gh-write target = manifest `.repository` (§V.41), asserted == resolved `--repo` immediately pre-write — repo named in deviation excerpt never bleeds into `<target>`; deviation path cwd = plugin repo → backprop hand-off (§V.27), no issue filed (closes §B.11).

## §V66 mechanize-scan

V66: mechanize-scan — user-invocable recipe ({design, spec, build, check, explain, condense, reorganize}) ends w/ MECHANIZE probe — canonical verbatim block per SKILL.md, sentinel `MECHANIZE` grep-sweepable; auto-fire sub-skills excluded; candidate = ≥ 2 same-shape deterministic calls (identical command modulo args) | LLM-side join/sort/count/dedup over script-emittable data | multi-step parse collapsible to one emit mode | fresh regex paraphrase (§V.40 class); hit → exactly one `## Next` item carrying observed pattern + proposed script mode, none → no item; never self-implement mid-run (§V.22, §V.20); routing: dev repo → /sdd:spec → §T row; consumer plugin-target → monitor dispatched path (§V.65); consumer repo-local → consumer /sdd:spec → extras row.
