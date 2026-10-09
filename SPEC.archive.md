# SPEC.archive — archived rows

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

## §B BUGS

id|date|cause|fix
