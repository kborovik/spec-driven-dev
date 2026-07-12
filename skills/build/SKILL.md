---
name: build
description: |
  Plan-then-execute impl vs SPEC.md. Triggers when user asks to build,
  implement, or execute spec or specific §T task. Phrasings: "build §T.<n>",
  "build --next", "implement next task", "run the build", "does the
  implementation run?", "is §T.<n> done?".
allowed-tools: Read, Edit, Write, Bash, Skill, TaskCreate, TaskUpdate
model: opus
---

# build — implement spec

Single-thread native plan→execute.
You are main Claude.
No swarm.

## LOAD

1. Read `SPEC.md`.
   Missing → tell user run spec skill first; bail.
2. Parse `$ARGUMENTS`: `§T.n` → that task only; `--next` or empty → lowest-numbered `.` row; `--all` → every `.` row in §T order — plan once, then chain {edit → verify → commit} per row autonomously.

## PLAN

Emit plan inline, per chosen task(s) — never enter plan mode (a wait-state breaks the `--all` autonomous chain):

1. Cite every applicable §V invariant — plan respects all.
2. Cite every §I interface touched — plan preserves shape.
3. List files to init / patch.
4. List tests to add or patch (one per invariant touched).
5. Name verification cmd (test, build, lint).

Emit plan inline every task (transparency, not wait-state) → EXECUTE.

## PROGRESS

`--all` autonomous chain = multi-phase run per response-shape invariant → emit live harness checklist (single `§T.n` / `--next` = one row, no checklist).
TaskCreate one task per chosen `.` §T row @ plan start, subject `T<n>: <goal line>`.
TaskUpdate `in_progress` @ that row's {edit → verify → commit} entry → `completed` @ its auto-commit.
FAIL → BACKPROP (status stays `.`) → task stays `in_progress`, never `completed`.
Checklist = ephemeral harness UI: never repo state (§T cells stay the dashboard per NON-GOALS), never substitutes the `## Next` block.

## EXECUTE

Per task in order:

1. Edit code per plan.
   Stage explicit `git add <listed-paths>` (feeds step-3 staged-diff probe); step-4 commit path-scoped so pre-existing dirty tree never bundled (write-ownership invariant).
2. Run verification cmd.
   Frontmatter `Bash` grant stays broad — verification cmd is consumer-defined per repo (`<test>` / `<build>` / `<lint>`), unpinnable; broad grant = prompt-control + intent-doc only per tooling-preference invariant, never an access boundary (real tool denial = `disallowed-tools`).
3. Staged diff touches PUBLISHED → probe `.spec/check-extras.md`; exists → run its audit recipes, bail per recipe msg every surviving match, no commit until match-free.
   No file → no-op.
4. **Pass** (cmd exits 0 + planned tests added + full-suite re-run shows no §V regress) → flip §T.n `.` → `x`; auto-commit path-scoped `git commit -m <subject> [-m <body>] -- <listed-paths> SPEC.md` (`-m` flags ! precede `--`), no prompt, msg `T<n>: <goal line>` + §V cites.
   Next task.
5. **Fail** → FAIL → BACKPROP.
   No blind retry, no commit, status stays `.`.

## FAIL → BACKPROP

1. Read failure output.
2. Classify: (a) code bug, (b) spec wrong, (c) unspec edge.
   Confident → proceed direct.
   Low-confidence (ambiguous or multiple plausible) → AskUserQuestion per decision-gate invariant, header `Verify-fail class`, 3 action-labels keyed (a)/(b)/(c): "Code bug — fix and re-run" / "Spec wrong — route cause to /sdd:spec" / "Unspec edge — route cause to /sdd:spec".
3. (a) → fix code, retry.
   No spec change.
4. (b)/(c) → run spec skill w/ the cause as free-form intent (gate routes to BACKPROP); it records §B (+ §V) and commits SPEC.md.
   Resume build vs updated spec per backprop HANDOFF: failing test first, then fix; commit cites the new §B/§V.

Rule: never silently fix root-cause w/o considering backprop — §B records bug-class precedent so recurrence-class blocked.

Mid-loop spec dispatch here is the sole exclusion from the operator-dispatch rule (slash-cmd dispatch is otherwise operator-turn only); without it every verify-fail costs an operator round-trip.

## WRITE POLICY

Build flips §T status cells only.
Every other SPEC.md edit → spec skill.

## MECHANIZE — script-candidate scan

Recipe end → before the `## Next` block, scan this run for a mechanization candidate.
Candidate = any of:

- ≥ 2 same-shape deterministic calls this run (identical command modulo args)
- LLM-side join / sort / count / dedup over script-emittable data
- multi-step parse collapsible to one script emit mode
- fresh regex paraphrase of an existing mechanical rule (mechanical-realization invariant class)

Hit → emit exactly one `## Next` item naming the observed pattern + proposed script mode; none → no item.
Never self-implement the mechanization mid-run (recipe-step-no-dispatch + write-ownership invariants).
Route by cwd:

- dev repo (this plugin) → /sdd:spec → new §T row
- consumer repo, plugin-target → monitor dispatched `mechanization-candidate` path (monitor-protocol invariant)
- consumer repo-local → consumer /sdd:spec → `.spec/check-extras` row

## OUTPUT — "Next" block

Heading `## Next`; 1–5 atomic items (one sentence each, no `Reply` prefix); positional dispatch (`run <int>` or `run /<plugin>:<cmd> [args]`).
Optional `## Hint` (≤ 3 lines) precedes when item selection needs hidden state.
PLAN not wait-state → no execute/revise/abort items.
Pass auto-commits → `/sdd:check` leads (cascade scan over just-closed §T row; not silent close):

```
## Next

1. /sdd:check — cascade scan over the just-closed §T row
2. /sdd:build --next — start the next pending §T row
3. /sdd:spec amend §T.<n> — re-scope before continuing
```

Backlog cleared (terminal state) → swap item 2 for `/sdd:spec` (seed new row), drop item 3.

## NON-GOALS

- No progress dashboards — `grep §T SPEC.md` is the dashboard.
- No speculative work beyond chosen task scope.
