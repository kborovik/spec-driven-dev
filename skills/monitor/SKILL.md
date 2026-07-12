---
name: monitor
description: |
  Auto-fire skill-deviation capture. Fires when, mid-skill-run, an sdd skill
  misbehaves: instruction ambiguous or self-contradictory, a recipe loop step
  impossible as written, a prescribed tool/flag fails, or the user corrects the
  skill's behavior. Redacts, dedups, then operator-gates a GitHub issue on the
  plugin repo; a dev-repo deviation routes to backprop instead. Not for consumer
  code bugs or env breakage unrelated to an sdd skill.
allowed-tools: Bash(gh *), Bash(git *), Bash(jq *), Bash(python3 *), AskUserQuestion, Skill
user-invocable: false
---

# monitor — skill-deviation capture → plugin-repo issue

Auto-fire sub-skill, 5th member of the sub-skill-flags family (telegraph, backprop, socratic, steno, monitor).
No hook — the skills-only invariant bans runtime interception; monitor = LLM self-report, not a wrapper.
Ships PUBLISHED to every consumer → every plugin user is a data source.

Trigger lives in this frontmatter description only — zero edits to existing skill bodies (byte-identical).
Body LLM-facing → telegraph.

## WHEN — fires mid-skill-run when an sdd skill deviates:

- instruction ambiguous or self-contradictory
- recipe loop step impossible as written
- prescribed tool / flag fails
- user corrects the skill's behavior

Not: consumer-repo code bugs, env breakage unrelated to an sdd skill, operator typo.
No deviation → no fire.

## PROTOCOL — ordered, stop on bail:

1. **CAPTURE** — skill name + plugin version + expected (quoted skill-body line) vs actual + minimal excerpt.
   Version ← `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` `.version` (jq; no jq → python3 — JSON parse not script-sole → frontmatter `Bash(python3 *)` stays broad per tooling-preference invariant, no single script path to pin).
2. **REDACT** — strip consumer-repo paths, code, identifiers, URLs; only the sdd skill-body text + deviation description survive.
   Mandatory pre-publish (monitor-protocol invariant) — excerpts originate in third-party repos.
3. **ROUTE** — cwd == plugin repo? `git remote get-url origin` resolves to manifest `.repository` → dev repo → hand off to backprop (backprop-protocol invariant): §B row, no issue filed.
   Stop.
   Else consumer repo → continue.
4. **TARGET** — issue repo ← `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` `.repository`, parsed to `owner/repo` (jq).
   No hardcoded slug in this body (parametric-recipe invariant — the plugin-internal file owns the slug).
5. **DEDUP** — `gh issue list --repo <target> --search "<skill> <keywords>"`.
   Hit → comment path.
   Miss → new-issue path.
6. **GATE** — AskUserQuestion before any gh write (decision-gate invariant).
   Header `Skill deviation`, question body surfaces the resolved `--repo <target>` verbatim (operator confirms exact write destination before any publish); mutually-exclusive labels: `File issue` (miss), `Comment` (hit), `Skip`.
   No auto-file path exists.
7. **WRITE** — immediately pre-write assert resolved `--repo` == `<target>` (= manifest `.repository`, step 4); mismatch → abort, no gh write (monitor-protocol invariant). `<target>` ! derive from `.repository` only — a repo named in the deviation excerpt is never sourced as `--repo` (redaction strips it; this assertion backstops a leak).
   Then per gate selection:
   - miss + File issue → `gh issue create --repo <target> --title "<skill>: <deviation summary>" --body <steno>` (github-facing-register → steno per steno skill).
   - hit + Comment → `gh issue comment <n> --repo <target> --body <steno occurrence>` (occurrence count = signal; one issue per deviation class).
   - Skip → nothing written.

## DISPATCHED — `mechanization-candidate` entry path

Second entry path, not auto-fire (mechanize-scan invariant).
Engaged from a user-invocable recipe's MECHANIZE `## Next` item — consumer plugin-target only.
Carries the observed pattern + proposed script mode, not a deviation → no CAPTURE, no WHEN trigger.
Skips the dev-repo backprop hand-off: mechanize-scan routes a dev-repo candidate to /sdd:spec → §T row and a consumer repo-local one to the consumer's /sdd:spec → extras row; only the consumer-plugin-target case reaches here, so no ROUTE step.

Ordered, stop on bail:

1. **REDACT** — strip consumer-repo paths, code, identifiers, URLs; only the observed pattern + proposed script mode survive.
   Mandatory pre-publish (monitor-protocol invariant) — candidate originates in a third-party repo.
2. **TARGET** — issue repo ← `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` `.repository`, parsed to `owner/repo` (jq).
   Same resolve as the auto-fire path — plugin-internal file owns the slug (parametric-recipe invariant), no hardcoded slug.
3. **DEDUP** — `gh issue list --repo <target> --search "<skill> mech candidate <keywords>"`.
   Hit → comment path.
   Miss → new-issue path.
   One issue per candidate class — recurrence comments, never duplicates.
4. **GATE** — AskUserQuestion before any gh write (decision-gate invariant).
   Header `Mech candidate`, question body surfaces the resolved `--repo <target>` verbatim (operator confirms exact write destination before any publish); mutually-exclusive labels: `File issue` (miss), `Comment` (hit), `Skip`.
   No auto-file path exists.
5. **WRITE** — immediately pre-write assert resolved `--repo` == `<target>` (= manifest `.repository`, TARGET step); mismatch → abort, no gh write (monitor-protocol invariant). `<target>` ! derive from `.repository` only — a repo named in the candidate excerpt is never sourced as `--repo` (redaction strips it; this assertion backstops a leak).
   Then per gate selection:
   - miss + File issue → `gh issue create --repo <target> --title "<skill>: mech candidate — <pattern>" --body <steno>` (github-facing-register → steno per steno skill; body = observed pattern + proposed script mode).
   - hit + Comment → `gh issue comment <n> --repo <target> --body <steno occurrence>` (occurrence count = signal; one issue per candidate class).
   - Skip → nothing written.

## REDACTION — mandatory

Survives: sdd skill name + plugin version, the quoted sdd skill-body line, deviation description.
Stripped: consumer file paths, code snippets, identifiers (names, secrets, consumer repo slug), URLs.
Excerpt originates in a third-party repo → strip first, publish second.
Uncertain a token is safe → drop it.

## DEV-REPO ROUTING

cwd == plugin repo → an out-of-repo issue is the wrong channel: backprop owns dev-repo capture (§B row), and a mirrored issue duplicates that record against the freshness contract.
Hand off to backprop, file no issue.

## NON-GOALS

- no hook / runtime interception (skills-only invariant — no hooks).
- no auto-file — every gh write operator-gated; silent publish impossible (decision-gate invariant).
- no CI / scheduled filing, no telemetry, metrics, or dashboards.
- never edits SPEC.md or any skill body — existing skills stay byte-identical.
