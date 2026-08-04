---
name: release
description: |
  REPO-LOCAL gh release flow for the sdd plugin — bump `.claude-plugin/plugin.json`
  version, commit, tag `v<version>`, publish GitHub release w/ generated notes.
  Triggers: "/release", "cut a release", "publish a release", "bump version and tag",
  "ship a new sdd version", "gh release".
allowed-tools: Read, Edit, Bash(git *), Bash(gh *), Bash(python3 */check-mechanical.py *), AskUserQuestion
---

# release — gh release flow (REPO-LOCAL)

REPO-LOCAL operator skill, not part of the published `sdd` surface. Cuts a GitHub release: bump version → commit → tag → publish. Single source of version truth = `.claude-plugin/plugin.json` (`marketplace.json` carries no version). Body LLM-facing → telegraph.

## ARGS

`$ARGUMENTS`:
- explicit `<version>` (e.g. `1.2.0`) → used verbatim.
- bump level `major` | `minor` | `patch` → semver-bump current.
- empty or ambiguous → decision-gate (`## VERSION`).

## PREFLIGHT

Guard chain — outputs injected below (`!` preprocessing, pre-model; `disableSkillShellExecution` consumers see disabled-by-policy markers → run each guard cmd manually). Bail w/ the named reason on first fail, nothing mutated:

1. working tree clean — output empty → else bail "commit or stash first":

!`git status --porcelain`

2. on `main` — output = `main` → else bail "release from main":

!`git rev-parse --abbrev-ref HEAD`

3. self-test green — output ends `self-test OK (…)` → else bail:

!`python3 scripts/check-mechanical.py --self-test`

4. audit clean — no dirty verdict row (VIOLATE / UNVERIFIABLE / UNRESOLVED / TYPE-MISMATCH / DRIFT / MISSING / STALE / EXTRA) → else bail "resolve drift via /sdd:check first":

!`python3 scripts/check-mechanical.py audit`

5. read current version from `.claude-plugin/plugin.json`.

## VERSION

- explicit `<version>` arg → new version verbatim.
- bump level → `major` = `X+1.0.0`, `minor` = `X.Y+1.0`, `patch` = `X.Y.Z+1` over current.
- empty or ambiguous level → AskUserQuestion (decision-gate), header `Release bump`, 3 mutually-exclusive labels `major` / `minor` / `patch`, each previewing its computed `v<version>`.
- collision guard: `v<version>` must not exist locally (`git tag -l v<version>`) nor on remote (`git ls-remote --tags origin v<version>`) → collision → bail.

## EXECUTE

In order, stop on any non-zero exit:

1. Edit `.claude-plugin/plugin.json` `"version"` field → new value (sole edited field; leave the rest byte-for-byte).
2. path-scoped commit: `git commit -m "release: v<version>" -- .claude-plugin/plugin.json` — `-m` (+ any `-m` body line) ! precede `--`; flags after `--` parse as pathspecs (`error: pathspec '-m' did not match`). Subject verbatim `release: v<version>` (fixed template per github-facing-register; body steno only if a note is warranted, else subject-only). Path-scoped per write-ownership invariant — owned file only, pre-existing dirty tree never bundled.
3. annotated tag: `git tag -a v<version> -m v<version>`.
4. push commit + tag: `git push origin main --follow-tags`.
5. publish: `gh release create v<version> --verify-tag --generate-notes`.

## VERIFY

`gh release view v<version> --json url -q .url` → report the release URL. Non-zero → publish failed, surface stderr, tag + commit already pushed (operator re-runs `gh release create` only).

## NON-GOALS

- never edits `SPEC.md` or published `skills/**` — REPO-LOCAL scope only.
- no hand-authored changelog — GitHub `--generate-notes` owns release notes.
- no version in `marketplace.json` — single source is `.claude-plugin/plugin.json`.
- not a pre-release gate for spec drift — `/sdd:check` owns that; PREFLIGHT only blocks on it.

## OUTPUT — "Next" block

Heading `## Next`; 1–5 atomic items (one sentence each, no `Reply` prefix); positional dispatch. Optional `## Hint` (≤ 3 lines) precedes when an item needs hidden state (e.g. publish failed mid-flow, tag already pushed).

Published release (terminal) →

```
## Next

1. open the release URL to confirm generated notes
2. /sdd:check — confirm spec + code clean on the new tag
```

PREFLIGHT bail → lead w/ the remedy for the failed guard (commit/stash, switch to main, or `/sdd:check` to clear drift).
