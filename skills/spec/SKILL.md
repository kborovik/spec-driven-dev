---
name: spec
description: |
  Sole semantic author of SPEC.md @ repo root — create, amend, fold designs,
  fold GitHub issues, or backprop bugs (§T status-flip → build, archive →
  condense, §V renumber → reorganize; those carve-outs not authoring paths).
  Triggers when user asks to write spec, start new spec, distill spec from
  code, add invariants, amend a section, record a bug, fold a design plan, or
  fold a GitHub issue. Common phrasings: "write the spec for...", "new spec",
  "distill spec from code", "spec this idea", "import existing repo",
  "pull invariants out of code", "this bug keeps biting", "post-mortem on Y",
  "fold-design", "github issue N".
allowed-tools: AskUserQuestion, Read, Edit, Write, Grep, Bash(git *), Bash(grep *), Bash(gh *), Agent, Skill(sdd:*)
argument-hint: "<intent | fold-design [N] | github issue N>"
---

# spec — spec mutator

`telegraph` skill applies to all writes here.
Carve-outs, not authoring paths: §T status-flip → /sdd:build; archive → /sdd:condense; §V renumber → /sdd:reorganize.

## DISPATCH

**Step 0a (precondition):** porcelain state injected below (`!` preprocessing; `disableSkillShellExecution` consumers see a disabled-by-policy marker → run `git status --porcelain SPEC.md` manually):

!`git status --porcelain SPEC.md`

Empty output → continue; else bail w/ "SPEC.md has uncommitted changes; commit or stash first" (auto-commit assumes clean baseline; porcelain catches staged + untracked, which `git diff --quiet` misses).
**Step 0b (post-resolution, AMEND only):** after AMEND resolves body file, if body file is not SPEC.md → `git status --porcelain <body-file>` empty → continue; else bail w/ "<body-file> has uncommitted changes; commit or stash first" (stub-redirected §V write must not leak into path-scoped commit).

**Step 1 (fold-in shortcut):** any of:
- `$ARGUMENTS` matches `mechanization-candidate <pattern>` / free-form candidate report → engage `sdd:monitor` dispatched mechanization-candidate path; stop.
- `$ARGUMENTS` is `fold-design [N]` / `fold the design plan` / free-form fold of current approved design plan → FOLD-IN from approved session plan (design skill; retains issue N linkage when issue present; issue N → **Before spec delta** once, then the fold).
- `$ARGUMENTS` matches `designs/*.md`, file exists → FOLD-IN from legacy design draft.
- `$ARGUMENTS` matches `github issue <N>` / free-form "fold issue N" → **Before spec delta** once, then FOLD-IN from GitHub issue (see FOLD-IN — github issue).
`github issue N` or fold-design with issue N: missing SPEC.md does not skip the pull request.
**Before spec delta** runs once, before any draft.
Do not run it again from FOLD-IN.
Other fold-in: SPEC.md must exist @ repo root else bail w/ "fold-in needs SPEC.md; init via NEW or DISTILL first".
Else → gate.

Engage `sdd:socratic` gate w/ `$ARGUMENTS` as intent.
Single-question loop until convergence triple matches one mode:

- **NEW** — goal + first-principle-asked + (≥ 1 invariant or ≥ 1 task)
- **DISTILL** — explicit "build from code" intent (gate exits ≤ 1 turn — walks repo, no interrogation)
- **BACKPROP** — symptom + surface + recurrence-class
- **AMEND** — §-target + delta

SPEC.md presence is the only branch (mode is gate byproduct, not user-typed prefix):

1. no SPEC.md @ repo root → gate restricted to {NEW, DISTILL}.
2. SPEC.md exists → gate ranges over {BACKPROP, AMEND, NEW}; NEW rare → require explicit re-init confirmation before overwrite.

Post-convergence → run mode procedure below.
Concrete first-turn input → gate passes ≤ 1 turn (zero-friction); vague → dialogue until convergence.
No skip flag, no prefix back-doors.

## NEW — idea → spec

Input: user idea.

1. Goal (1 line, telegraph) → §G.
2. Constraints stated or implied → §C.
3. External surfaces named → §I.
4. Initial invariants → §V (numbered V<n>).
   Gate probes first-principle (foundational claim); user may decline → converge on derived invariants only.
   Late first-principle → AMEND §V (only late-entry path, not second authoring path).
5. Goal → ordered tasks → §T pipe table, all status `.`, ids T<n>.
6. §B header row only (`id|date|cause|fix`).

→ APPLY.

## DISTILL — code → spec

Walk repo.
Produce §G (infer from README/package.json/main entry), §C (infer from stack), §I (enumerate public APIs/CLIs/configs), §V (derive from tests + assertions), §T (one task per known TODO or missing test), §B (empty).
Flag uncertain items w/ `?` so user can confirm.

→ APPLY.

**Second pass (required Next):** post-APPLY Next always includes `/sdd:check` then `/sdd:spec` confirm `?`-flagged rows (named AMEND batch).
DISTILL is not one-shot truth — brownfield needs check noise + confirmation.

## BACKPROP — bug → §B + §V

Input: gate triple (symptom + surface + recurrence-class).

1. Parse bug.
2. Find root cause (read code).
3. New invariant would catch recurrence? yes → draft `V<next>`.
4. Append §B row `B<next>|<date>|<cause>|<fix>` — fix cell `V<N>` when step 3 drafted, else `-` (per SPEC-FORMAT §B fix grammar).
5. Drafted → append invariant to §V.
6. Fix changes behavior → add/patch §T rows.

→ APPLY.

Rule: every bug → §B entry.
Invariant optional but preferred.

**Resume card (post-commit):** APPLY already listed `backprop-handoff.json` in `.spec/.gitignore`.
Write `.spec/backprop-handoff.json` with `{B, V, T, test_name_hint}` for the new rows (REPO-LOCAL cache, not design truth).
Next item #1 = concrete `/sdd:build §T.<n>` (never bare `--next` only).
Build LOAD consumes + deletes the card on close.

## AMEND — targeted edit

Input: gate §-target + delta.

**Resolve body file** via script when possible: `emit-v-slices --dirty V<n>` resolves check-extras stubs (extras-hook + single-load).
Fallback hand-resolve: SPEC.md stub `→ .spec/check-extras.md §V<n>` → body file `.spec/check-extras.md`; else SPEC.md. §B/§G/§C/§I/§T always SPEC.md.

### Micro-AMEND (trivial path)

Fires when all hold: single § target; delta ≤ one cell / one line; no new §V row; no sweep-§T.
Still show preview.
AskUserQuestion options lead with `Apply` (recommended); skip fold-first (no new row).
Structural multi-row / new §V / FOLD-IN / BACKPROP / NEW / DISTILL keep full APPLY gate.

### Full AMEND

Read target § from resolved body file.
Show current in steno if target in {§V, §B}; telegraph otherwise.
Ask user what changes when delta incomplete.

→ APPLY.

Never silently rewrite §s user did not name.

## FOLD-IN — design plan, legacy design draft, or github issue → §V / §T amend

Input (any of):
- approved Claude Code plan mode body from `/sdd:design` (`fold-design`)
- legacy `designs/<slug>.md`
- GitHub issue `N` via `/sdd:spec github issue N` (or free-form fold of issue N)

No socratic gate — design already enforced Open-Questions-empty (or park) pre-approve; issue fold is operator-named target.
Multi-target: one design or issue may propose new §V / §T / §I / §B rows in one apply.

**Before spec delta** (github-workflow invariant; `github issue N` or fold-design with issue N only; sole call site is DISPATCH; runs once before any draft, including when SPEC.md is missing):

Open pull request for this issue → stop early.
`gh issue develop <issue> --list` names linked branches.
`gh pr list --head <branch> --state open --json number` non-empty → `git switch <branch>` and stop.
Do not run `gh issue develop` again.
Do not make another empty commit.
Do not call `gh pr create` again.

Else the tree is clean (`git status --porcelain` empty) or the block bails before any push or commit.
`git commit --allow-empty` records a non-empty index, so porcelain must still be empty at that commit.

1. Fetch `origin`.
   Resolve `<default-base>` from `origin/HEAD`.
2. Local `<default-base>` behind `origin/<default-base>` → fast-forward (`git switch <default-base>` then `git merge --ff-only`).
   Diverged → stop and report.
   Do not force-push.
3. Local `<default-base>` ahead → `git push origin <default-base>` (named refspec; this is the push default branch step; never bare `git push`).
   Rejected → stop and report.
   Already up to date → success, not a failure.
4. Issue branch — `gh issue develop <issue> --checkout` (in-place, one branch per session).
5. One commit ahead of that base, not the spec delta: `git commit --allow-empty -m "issue <issue>: ahead of base"` only when porcelain is still empty.
   `gh pr create` rejects zero-ahead.
   The message has no close trailer.
6. `gh pr create --draft` with `Related: #<issue>` before the spec delta (generic structure; steno body per github-facing-register invariant; no close trailer; no review-at-create).

Missing SPEC.md does not skip the pull request; the pull request is open before the spec delta.
SPEC.md present → return to the fold on that branch: draft, then on OK write, path-scoped commit, PUSH.
SPEC.md missing → stay on the issue branch; no delta, no invented SPEC.md; next NEW or DISTILL on this branch creates SPEC.md and PUSHes.
Never rerun this block; never a second pull request; spec stops before the chain.
No GitHub issue → skip this block.

1. Read plan, draft, or issue; parse proposed amendments.
2. Draft each in telegraph (target §s + delta text).

→ APPLY.

Rule: fold-in mutates SPEC.md only.
Plan file stays in session; legacy design file stays in working tree (no auto `rm`).
Provenance: slug, "fold-design", or `github-issue-<N>` in commit msg.
When `fold-design` runs with an issue N created during design (or `$ARGUMENTS` supplies issue N), treat as issue-linked fold: record `github-issue-<N>` in commit body.
Dispatch already ran **Before spec delta** once.
Do not run it again.

### FOLD-IN — github issue

Draft PR already open (DISPATCH ran **Before spec delta** once).
SPEC.md missing → stop per that block (no LOAD, no delta).
SPEC.md present → ordered steps below.

Ordered:

1. **LOAD** — `gh issue view <N> --json number,title,body,labels` against the cwd repo (no `--repo` slug).
2. **MAP** — problem / body prose → candidate §V / §T rows (telegraph); title → short task goal when one §T fits.
3. **Acceptance** — if body has `## Acceptance` checklist, fold open bullets into §T goals or task notes so `/sdd:build` can prove them; if no `## Acceptance` → surface **ADVISORY** in the preview (not silent-verified; github-workflow invariant) and continue fold without inventing bullets.
4. **Link** — record issue number in commit body (`github-issue-<N>`); do not auto-close the issue from this fold.

→ APPLY show-user (step 3) on the issue branch, after **Before spec delta**.
On OK → write delta, path-scoped commit, then PUSH.
Spec stops before the chain.

## APPLY (all modes, post-delta)

Five steps in order; audits fire on condition, not mode authorship.
All audits run pre-show-user, mechanical pattern-match not LLM-judgment per mechanical-not-LLM-judgment invariant.

**Step 0 — write-time prune** (delta-rewrite stage, ordered ahead of audit table so every audit sees final-form delta):

- delta patches pre-existing §V row → §V-row residue prune per `references/write-time-prune.md` (Read on match — pattern set + pre-filters live there).
- delta adds or rewrites §B `cause` cell → one-line trim per same file.
- pruned content → commit-msg body (step 4); step 3 shows post-prune form.

**Step 1 — audit table** (on-fail column names owning sub-recipe — bail strings + grep sub-recipe detail live in `references/audit-recipes.md`, Read @ first fire):

```
audit | fires when delta is | on fail
sweep-scope | contains sweep-§T row (§V-violation remediation) | bail → SWEEP-§T SCOPE AUDIT
pinned-cite | touches PUBLISHED (a) or SPEC.md narrative (b) | bail → PINNED-CITE AUDIT, matching sub-recipe
next-block  | touches user-typeable SKILL.md | bail → NEXT-BLOCK-SECTION AUDIT
fold-first  | adds §V row to pre-existing §V section, mode not FOLD-IN | AskUserQuestion gate → FOLD-FIRST AUDIT
```

Table uses named-invariant + placeholder cite form only (`per <named> invariant`, `§V.<n>`) — `skills/**` in PUBLISHED where pinned §-digit cites banned per sub-recipe (a); body pinned-cite count is 0, stays 0.

**Step 2 — render-split**: §V + §B content rows → steno per steno skill (audience: user reviewing proposal); all else → telegraph (§T/§I pipe forms already legible, §G/§C targets, header-only §B row).

**Step 3 — show-user**: render diff preview; await user OK.

**Step 4 — write + commit**: on OK → write delta to its resolved body file(s) (telegraph) + auto-commit path-scoped per `${CLAUDE_SKILL_DIR}/../_fragments/PATH-SCOPED-COMMIT.md`: `git commit -m <subject> [-m <body>] -- <body-file(s)>`.
github-issue fold (and fold-design with issue N): draft PR already open per **Before spec delta**; write delta on that branch + path-scoped commit, then PUSH; spec stops before the chain.
Non-github-issue APPLY: no github BRANCH, no github PR (do not open one).
Current branch already has an open pull request (`gh pr view --json state` is OPEN) → after the path-scoped commit, PUSH.
That covers NEW, DISTILL, AMEND, and BACKPROP on the issue branch; never a second pull request.
No open pull request → the commit stays on the current branch; no push.
Body file(s) = SPEC.md every mode + target, except a stub-redirected §V AMEND → `.spec/check-extras.md` per AMEND § resolution + extras-hook invariant (the SPEC.md stub row stays untouched, so check-extras.md is the sole path-scope; mixed delta touching both an inline §V/other § and a stub-redirected §V → path list = the union).
No commit prompt (uniform every mode).
NEW / DISTILL / BACKPROP: first `.spec/` write (NEW/DISTILL init or first BACKPROP, whichever first) → grep `^backprop-handoff.json$` in `.spec/.gitignore`; missing → init or append that line (backprop-resume-card invariant); path-scope `.spec/.gitignore` when created or patched.
Resume-card JSON stays untracked (post-commit BACKPROP write).
Msg per mode:

```
NEW      → init SPEC.md (V<1>..V<n>, T<1>..T<m>)
DISTILL  → init SPEC.md from code
BACKPROP → backprop §B.<n>(+) + §V.<N>(+): <one-line cause>   (trimmed forensics → msg body, from step 0)
AMEND    → amend §<S>.<n>(+): <one-line>                       (pruned history → msg body, from step 0)
FOLD-IN  → fold-in §V.<n>(+) and §T.<n>(+): <slug|fold-design>  (omit absent §s)
```

**Re-entry**: any stage rewriting delta after step 0 — concretely fold-first's fold-into reroute (new §V row → existing-row amend) — re-enters APPLY @ step 0; rewritten delta newly satisfies §V-row prune and prior audits saw a delta that no longer exists.

APPLY ends @ commit (github-issue fold: PUSH the open pull request, then POST-APPLY). `## POST-APPLY` fires after.

## AUDIT SUB-RECIPES + PRUNE PATTERNS — references/

Conditional detail one level deep per token-budget invariant (skill-body budget); Read each file only @ its load moment:

- `references/audit-recipes.md` — SWEEP-§T SCOPE, PINNED-CITE, NEXT-BLOCK-SECTION, FOLD-FIRST bodies + bail strings; Read @ first audit fire per APPLY step 1.
- `references/write-time-prune.md` — §V-row residue prune + §B cause trim; Read @ APPLY step 0 on match.

## POST-APPLY

Default: surface `/sdd:check` as Next item #1 (cascade over just-applied delta).
Exceptions:
- **BACKPROP** → item #1 = concrete `/sdd:build §T.<n>` (resume card); item #2 = `/sdd:check`.
- **DISTILL** → item #1 = `/sdd:check`; item #2 = `/sdd:spec` confirm `?`-flagged rows.
- **FOLD-IN github issue** and **fold-design with issue N** → spec stops before the chain; load `${CLAUDE_SKILL_DIR}/../_fragments/POST-SPEC-CHAIN.md` (`/sdd:build`; READY remainder); Next merge when approved — say "merge the PR".
- Green-path: not default-chained from spec (operator or explicit Next).

Not silent commit-then-done.

## OUTPUT RULES

Defer to `${CLAUDE_PLUGIN_ROOT}/SPEC-FORMAT.md` — row shape, section catalog, citation forms, header conventions.

## MECHANIZE

Load `${CLAUDE_SKILL_DIR}/../_fragments/MECHANIZE.md`.

## OUTPUT — "Next" block

Per `${CLAUDE_SKILL_DIR}/../_fragments/NEXT.md`.
Show-user → apply + revise lead.
Post-commit → POST-APPLY leads (BACKPROP concrete build; DISTILL check + confirm-?; FOLD-IN github issue or fold-design+issue N merge when approved — say "merge the PR"; else check then build).

## NON-GOALS

- Writes serialize on main thread; reads delegable to Agent sub-agents (BACKPROP root-cause + NEW/DISTILL code-walk).
- No dashboards.
  Cache files (`.spec/backprop-handoff.json`, check memo) are not design truth.
- No auto-build after non-BACKPROP spec except github PR recipe post-spec-commit chain per `${CLAUDE_SKILL_DIR}/../_fragments/POST-SPEC-CHAIN.md`.
