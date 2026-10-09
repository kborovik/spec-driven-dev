---
name: build
description: |
  Plan-then-execute impl vs SPEC.md §T tasks. Triggers when user asks to build,
  implement, or execute spec or specific §T task. Phrasings: "build §T.<n>",
  "build --next", "implement next task", "run the build", "does the
  implementation run?", "is §T.<n> done?". Single-thread main agent; no swarm.
  Exclusion: github post-spec-commit write-capable child (`POST-SPEC-CHILD=1`).
allowed-tools: AskUserQuestion, Read, Edit, Write, Bash, Skill(sdd:*), TaskCreate, TaskUpdate
argument-hint: "[§T.n | §T.a,§T.b,… | --next | --all | --no-chain]"
---

# build — implement spec

Single-thread native plan→execute.
You are main Claude.
No swarm.
Exclusion: github post-spec-commit write-capable child (write-serialize + github-workflow invariants); this child ! spawn further build children.

## LOAD

1. Spec overview via `python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-mechanical.py emit-overview` — §G/§C/§I/§T/§B bodies + §V id list; not whole-file Read per single-load invariant.
   Script error "SPEC.md not found" → tell user run spec skill first; bail.
   Status-cell flip later reads SPEC.md only for the write path (not a second census load).
2. Parse `$ARGUMENTS`:
   - `§T.n` → that task only
   - comma-joined `§T.a,§T.b,…` (optional spaces) → those rows only, in §T order (post-spec fold path)
   - `--next` or empty → lowest-numbered `.` row
   - `--all` → every `.` row in §T order — plan once, then chain {edit → verify → commit} per row autonomously
   - `--no-chain` → disable green-path check hop after pass
3. §V bodies for the chosen rows' cites via `python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-mechanical.py emit-v-slices --dirty V<a>,V<b>` (comma-list from §T `cites`); resolves check-extras stubs.
4. If `.spec/backprop-handoff.json` exists → treat as resume card (see FAIL → BACKPROP); prefer its `T` id when args empty/`--next`.
5. If prompt or env token `POST-SPEC-CHILD=1` set → post-spec child per `${CLAUDE_SKILL_DIR}/../_fragments/POST-SPEC-CHAIN.md`.
   Prefer comma-joined ids from spawn prompt over bare `--all`.

## PLAN

Emit plan inline, per chosen task(s) — never enter plan mode (wait-state breaks `--all`):

1. Cite every applicable §V invariant.
2. Cite every §I interface touched.
3. List files to init / patch.
4. List tests to add or patch (one per invariant touched).
5. Name verification cmd (test, build, lint).

Emit plan inline → EXECUTE.

## PROGRESS

`--all` or multi-id list = multi-phase per `${CLAUDE_SKILL_DIR}/../_fragments/PROGRESS.md` (TaskCreate, TaskUpdate).
FAIL → BACKPROP (status stays `.`) → task stays `in_progress`.

## UPSTREAM-FR (plugin-meta only)

When §T goal matches `upstream FR` (case-insensitive) **and** cwd is plugin dev repo (origin resolves to manifest `.repository`) → load `${CLAUDE_SKILL_DIR}/../_fragments/UPSTREAM-FR.md` and run it.
Consumer repos: skip this section entirely (consumer-core-profile invariant).

## EXECUTE

Per task in order:

0. UPSTREAM-FR trigger + plugin repo → run fragment first; else skip.
1. Edit code per plan.
   Stage explicit paths for step-3 probe; commit path-scoped (see `${CLAUDE_SKILL_DIR}/../_fragments/PATH-SCOPED-COMMIT.md`).
2. Run verification cmd.
3. Staged diff touches PUBLISHED → probe `.spec/check-extras.md` judgment recipes when present.
4. **Acceptance-gate (task-scoped)** — when issue-linked (open PR, `github-issue-N` cite, `gh issue develop` branch); detector = issue linkage not planned close trailer:
   load `${CLAUDE_SKILL_DIR}/../_fragments/ACCEPTANCE-GATE.md` and run the gate (github-workflow invariant).
   - **BLOCK** → verify FAIL; no close trailer; status stays `.`; go FAIL → BACKPROP only if class (b)/(c), else fix evidence and re-run gate.
   - **ADVISORY** (no `## Acceptance`) → surface advisory (not silent-verified); continue only after the advisory is stated.
   - **ALLOW** → evidence sufficient (no close trailer); **collect** bullet→evidence map for this task; do **not** post comment here (post once @ READY / MERGE per fragment).
   Build commit never carries `Closes`/`Fixes`/`Resolves` — close trailer MERGE-only (github MERGE after ACCEPTANCE-GATE).
   No issue linkage → skip.
5. **Pass** → flip §T.n `.`→`x`; path-scoped commit `T<n>: <goal line>` + §V cites on listed paths + SPEC.md.
   Clear `.spec/backprop-handoff.json` if present.
   Issue-linked open PR: github PUSH after each passed task (keep remote current).
   Do **not** run READY inside the per-task loop.
6. **Fail** → FAIL → BACKPROP.
   No blind retry.
   Status stays `.`.

## POST-LOOP (issue-linked only)

After the last chosen row closes (single task, last of multi-id list, or last of `--all`):

- operator-run `/sdd:build`: load-and-run github READY once (review-apply + push + `gh pr ready`; not slash-dispatch `/code-review` per recipe-step-no-dispatch invariant).
  Post Acceptance-evidence comment once if ALLOW evidence collected.
  Issue-linked READY implies no check hop.
  Next item #1: merge when approved — say "merge the PR" (auto-fires github MERGE).
  `/sdd:check` listed not hopped.
- post-spec-commit child (`POST-SPEC-CHILD=1`): per `${CLAUDE_SKILL_DIR}/../_fragments/POST-SPEC-CHAIN.md`.

## FAIL → BACKPROP

Post-spec-commit child (`POST-SPEC-CHILD=1`): child cannot prompt interactively or mutate SPEC.md; halt execution on fail, keep status `.`, emit failure report to parent session (class a/b/c when known).
Parent posts `gh pr comment` steno on the draft PR (§T, class, Next); Next leads `/sdd:build` resume; when class b/c also `/sdd:spec <cause>` BACKPROP (write-serialize + backprop-protocol invariants).
Otherwise (operator-run build):

1. Read failure output.
2. Classify: (a) code bug, (b) spec wrong, (c) unspec edge.
   Low confidence → AskUserQuestion: Code bug / Spec wrong / Unspec edge.
3. (a) → fix code, retry.
   No spec change.
4. (b)/(c) → run spec skill with cause as free-form intent (BACKPROP).
   Spec commits §B (+ §V, §T).
   Resume: failing test first, then fix; commit cites new §B/§V.

Mid-loop spec dispatch = sole mandatory exclusion from operator-only dispatch (plus green-path chain).

## CHAIN (default-on)

Per `${CLAUDE_SKILL_DIR}/../_fragments/CHAIN.md`.
issue-linked READY implies no check hop — Next merge phrasing leads; `/sdd:check` listed not hopped.

## WRITE POLICY

Build flips §T status cells only.
Every other SPEC.md edit → spec skill.

## MECHANIZE

Load `${CLAUDE_SKILL_DIR}/../_fragments/MECHANIZE.md`.

## OUTPUT — "Next" block

Per `${CLAUDE_SKILL_DIR}/../_fragments/NEXT.md`.
Pass (chain off) → check leads, then build --next.
Issue-linked operator-run pass → merge when approved (say "merge the PR"; github MERGE auto-fire) leads; `/sdd:check` listed not hopped.
Post-spec-commit child → `${CLAUDE_SKILL_DIR}/../_fragments/POST-SPEC-CHAIN.md`; on fail include BACKPROP Next when class b/c.
Backlog clear → `/sdd:spec` seed.

## NON-GOALS

- No progress dashboards — `grep §T SPEC.md` is the dashboard.
- No speculative work beyond chosen task scope.
