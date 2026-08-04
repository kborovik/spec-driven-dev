# check references — audit row catalog

Conditional detail split from check SKILL.md per token-budget invariant (skill-body budget).
Telegraph register (SPEC-ADJACENT).
Read on first audit-output parse; SKILL.md MECHANICAL CORE holds the run command + merge summary.

## Row catalog — `audit` mode pipe-table `id|verdict|evidence`

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

## REPORT merge rules

Merge into REPORT verbatim: `format` / `history` / `cite` / `pinned-header` / `mechanize` / `dispatch` / `grant` / `claude-md` / `symbols` / `idiom` rows → their REPORT blocks (`mechanize` DRIFT/MISSING + `dispatch` VIOLATE + `grant` VIOLATE + `claude-md` MISSING/VIOLATE + `symbols` VIOLATE + `idiom` VIOLATE → invariant drift); `token` + `sembr` + `memo`-invalidation → `## advisory`.
Scope-feed rows (`memo` drift, `tasks` flipped-set, `diff` touched-set, `scope` v-path-dirty) carry stable comma-joined fields consumed machine-side — chained into `emit-v-slices --dirty`, never surfaced in advisory, never hand-rolled via `git diff` or a hand-grep over §V bodies. `batch|ADVISORY` likewise consumed machine-side (Batch protocol step 1), never surfaced in advisory.
