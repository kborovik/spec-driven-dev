---
name: github
description: |
  Auto-fire gh-CLI workflow governor. Fires when an sdd skill or the operator
  runs a GitHub issue or pull-request operation — open an issue, start work on
  one, open a PR, push an issue-linked branch with an open PR, mark a PR ready,
  merge a PR, or close one unmerged. Shapes the gh workflow:
  generic issue/PR structures, per-PR issue-linked branch,
  spec-fold draft PR before the spec delta, then post-spec-commit chain (`${CLAUDE_SKILL_DIR}/../_fragments/POST-SPEC-CHAIN.md`),
  operator-run code complete then review-apply then `gh pr ready` once per run,
  squash-merge with branch cleanup, `Closes #<issue>` at merge.
  No corresponding GitHub issue → no git branch, no GitHub PR
  (work stays on current branch).
  Not for plain git ops (commit, or push with no issue/PR) nor `gh release`
  — the release skill owns version tag + release notes.
allowed-tools: Read, Edit, Write, Agent, Bash(gh *), Bash(git *)
user-invocable: false
---

# github — gh-CLI workflow governor (auto-fire)

Auto-fire sub-skill per the sub-skill-flags invariant (`user-invocable: false`, never `disable-model-invocation` — that hides the skill from model auto-invocation).
No hook — the skills-only invariant bans runtime interception; github = LLM-applied workflow shape on each gh issue/PR op, not a wrapper.
Ships PUBLISHED to every consumer → governs the consuming repo's own gh workflow.

Trigger lives in this frontmatter description only — fires on a GitHub issue or PR op, applies the gh-CLI shape per the github-workflow invariant.
Body LLM-facing → telegraph.

Repo-agnostic per the parametric-recipe invariant: every gh + git command runs against the cwd repo — no hardcoded `owner/repo` slug, no `--repo` flag, no repo-literal path. github-facing bodies (issue, PR) = steno per the github-facing-register invariant; commit subjects = fixed templates, verbatim.

## ENGAGE LOG

When this skill fires, emit one telegraph line before the op recipe: `engaged sdd:github — <ISSUE|BRANCH|PR|PUSH|READY|MERGE|CLOSE>`.
Operator must see the governor (auto-fire visibility).

## WHEN — fires on a gh issue/PR op:

- new issue requested → ISSUE
- start work on an issue (issue-linked branch) → BRANCH
- open a PR w/ corresponding GitHub issue → PR (`--draft`; no review; no Closes); spec-fold PR continues post-spec-commit chain
- open a PR or start a branch w/ no corresponding GitHub issue → no BRANCH, no PR (work stays current branch)
- issue-linked `git push` w/ open PR → PUSH
- operator-run issue-linked code complete → READY
- post-spec-commit remainder (review already ran as sub-agent, or doc-or-comment skip) → READY remainder
- merge a PR (operator says "merge the PR" / "merge PR `<pr>`" when review approves) → MERGE
- close a PR unmerged → CLOSE

Not: plain git ops (commit, push with no issue/PR), `gh release` (release skill owns version tag + notes).
No gh issue/PR op → no fire.

Every worked GitHub issue ! one issue-linked PR.
`/sdd:spec github issue N` or fold-design with issue N runs the before-delta block once, before any draft.
An open pull request for that issue → `git switch` its branch and stop.
Do not run `gh issue develop` again.
Do not make another empty commit.
Do not call `gh pr create` again.
Else: fetch, fast-forward `<default-base>` when behind, then push default branch with `git push origin <default-base>` only when ahead (named refspec; never bare `git push`; rejected → stop and report; already up to date → success; no force), then issue branch `gh issue develop <issue> --checkout`, then one non-delta commit `git commit --allow-empty` on a clean tree (not the spec delta), then `gh pr create --draft` with `Related: #<issue>` before the spec delta.
No close trailer.
No review-at-create.
A missing SPEC.md does not skip the pull request.
SPEC.md present → draft, commit, and PUSH on that branch.
SPEC.md missing → do not write a delta and do not invent SPEC.md.
Later NEW, DISTILL, AMEND, and build commits PUSH the open PR (`git push`).
Do not open a second pull request.
No corresponding GitHub issue → no BRANCH, no PR (`gh pr create`).
Missing issue → bail: no `gh issue develop`, no `git checkout -b`, no `gh pr create`.
Work stays on current branch; plain git commit still in scope.
chain runs once after the spec commit on the open PR.
Spec stops before the chain.
The chain load is the PR section after the spec commit, not this open.
After operator-run issue-linked code complete → READY once per run.
Close → MERGE (ACCEPTANCE-GATE then add Closes then squash).

## ISSUE — `gh issue create`

`gh issue create --title "<summary>" --body <steno> [--label <class>]` against the cwd repo (no `--repo` slug per the parametric-recipe invariant).
Title = one-line summary; body = steno per the github-facing-register invariant.
Body shape: problem statement + `## Acceptance` checklist (`- [ ]` bullets).
`--label` optional.
Caller-named class in {enhancement, bug, documentation} → pass `--label <class>`.
Missing label in cwd repo → `gh label create <class>` then retry.
No fixed template scaffold beyond that heading.
Shape POST-APPROVE hands title + body + Acceptance + class here (github owns create).

## BRANCH — issue-linked branch

Corresponding GitHub issue `<issue>` required (`gh issue view <issue>` succeeds).
Missing → bail; no `gh issue develop`, no `git checkout -b`, no `git switch -c`.
Work stays on current branch.

`gh issue develop <issue> --checkout` — creates + checks out the issue-linked branch in place (native gh linkage; branch named by gh, never hand-named).
One branch per session.
Required when starting work on an issue.
No corresponding GitHub issue → no BRANCH.

## PR — `gh pr create --draft`

Fires when opening a PR for a worked GitHub issue.
Spec fold fires before the spec delta, after push default branch, the issue branch, and one `git commit --allow-empty` (not the spec delta), including when SPEC.md is missing.
Corresponding GitHub issue required (branch from `gh issue develop <issue>`, or explicit `<issue>`).
Missing → bail; no `gh pr create`.
Create has no review-at-create.
Never `Closes`/`Fixes`/`Resolves` trailer @ create.
No close trailer.

`gh pr create --draft --title "<summary>" --body <steno>` from the linked branch.
Body = steno per the github-facing-register invariant.
Body includes `Related: #<issue>` line.
No Acceptance copy.
No secondary Closes @ create.
Generic structure: change summary; no close trailer; no fixed template.

**After the spec commit on this open PR:** load `${CLAUDE_SKILL_DIR}/../_fragments/POST-SPEC-CHAIN.md`.
Do not wait to open the PR until the spec commit exists.
An open pull request for the issue already exists → do not create another.

## PUSH — `git push` issue-linked branch w/ open PR

Fires on later issue-linked commits while a PR is open.
Later spec commits and build commits PUSH to the open PR.
NEW, DISTILL, AMEND, and BACKPROP on a branch that already has an open pull request PUSH after the commit.
They do not open a pull request.
`git push` the issue branch.
Plain git push w/ no issue/PR still out of scope — no fire.

## READY — review-apply then `gh pr ready`

Required after issue-linked code complete (once per operator-run build, not per task).
Never skip READY.
Post-spec-commit path already ran `code-review` as sub-agent → skip review; continue at remainder.

**Review** — load-and-run bundled `code-review` skill on the issue-linked branch vs default base (not slash-dispatch `/code-review`; recipe-step-no-dispatch invariant).
Skip when post-spec-commit already ran `code-review` as sub-agent.
Skip when the diff matches the github-workflow review skip (doc-or-comment diff).
Doc-or-comment: every changed path is in {`SPEC.md`, `SPEC.archive.md`, `.spec/check-extras.md`, `SPEC-FORMAT.md`, `README.md`, `CLAUDE.md`, `designs/**`}.
Or every changed line outside that set is comment or whitespace.
`skills/**`, any script, or any other non-comment line → other diffs still run review.
Diff = `git diff <default-base>...HEAD` plus `git diff -U0 <default-base>...HEAD` for lines outside the doc set.
Skip continues READY remainder (no findings).
Scratch writes only, no repo edits; spawn general-purpose Agent, not read-only Explore.
Operator `/code-review` unchanged.

**Remainder** — parse findings.
Post-spec: apply open bug + suggestion; list nits; no wait.
Operator-run: apply open bug + suggestion; list nits; ? wait nits (apply unless operator declines).
re-run task verify.
Fail → no `gh pr ready`.
Pass → `git push` (PUSH); `gh pr ready`.
Post Acceptance-evidence comment once per issue-linked run when ALLOW evidence collected (ACCEPTANCE-GATE fragment).
Recipe pauses (Next: merge when approved — say "merge the PR" / "merge PR `<pr>`"; auto-fires github MERGE).

## MERGE — ACCEPTANCE-GATE then add Closes then squash

Run ACCEPTANCE-GATE first (full evidence for every open Acceptance bullet).
BLOCK → do not add close trailer; do not merge.
Probe `gh pr checks <pr>` + `gh pr view <pr> --json reviewDecision,mergeable`.
Empty checks skip.
Required reviews missing or CHANGES_REQUESTED or unmergeable → BLOCK, no merge.
ALLOW → add `Closes #<issue>` to PR body then `gh pr merge <pr> --squash --delete-branch --subject "<title> (#<issue>)" --body "Closes #<issue>"` (commits squashed, remote branch deleted); post evidence comment per fragment if not already posted.
Squash subject ! `#<issue>` the linked issue not merely PR; GitHub default `(#PR)` insufficient.
ADVISORY → surface advisory, then add Closes + merge only after the advisory is stated.

`Closes #<issue>` in the PR body auto-closes the linked issue on merge → no separate `gh issue close`.
Squash commit subject and body carry `#<issue>` → git log recovers closed issue.

## CLOSE — unmerged

PR abandoned, not merged → cleanup only, no squash:

1. `gh pr close <pr> --delete-branch` — closes the PR and deletes the remote branch; no merge commit.
2. `git switch <default-base>` — leave the issue-linked branch before deleting it (git refuses to delete the checked-out branch).
3. `git branch -D <branch>` — local branch cleanup.

No squash.
Remote delete via `gh pr close --delete-branch`, not merge.
The linked issue stays open — nothing merged to close it.
Unmerged PR close does not run ACCEPTANCE-GATE (issue not closed).

## ACCEPTANCE-GATE

Load `${CLAUDE_SKILL_DIR}/../_fragments/ACCEPTANCE-GATE.md`.

## NON-GOALS

- no `gh release` — the release skill (REPO-LOCAL) owns version tag + release notes.
- no hardcoded repo slug, no `--repo` flag — every op runs against the cwd repo (parametric-recipe invariant).
- never writes or edits SPEC.md or any skill body.
- no close of a worked issue without an issue-linked PR.
- no git branch, no GitHub PR without corresponding GitHub issue.
