---
name: build
description: |
  Plan-then-execute impl vs SPEC.md. Triggers when user asks to build,
  implement, or execute spec or specific §T task. Phrasings: "build §T.<n>",
  "build --next", "implement next task", "run the build", "does the
  implementation run?", "is §T.<n> done?".
allowed-tools: Read, Edit, Write, Bash, Skill
model: opus
---

# build — implement spec

Single-thread native plan→execute. You are main Claude. No swarm.

## LOAD

1. Read `SPEC.md`. If missing → tell user to invoke the spec skill first. Stop.
2. Parse invocation args:
   - `§T.n` → that task only
   - `--next` or empty → lowest-numbered row with status `.`
   - `--all` → every `.` row in §T order

## PLAN

Native plan mode. For chosen task(s):

1. Cite every §V invariant that applies. Plan must respect all.
2. Cite every §I interface touched. Plan must preserve shape.
3. List files to create / edit.
4. List tests to add or update (one per invariant touched).
5. Name verification command (test, build, lint).

Emit plan inline every task — transparency, not wait-state — then proceed to EXECUTE.

## EXECUTE

Per task in order (status flips `.` → `x` direct):

1. Edit code per plan.
2. Run verification command.
2'. On staged diff touching PUBLISHED, probe `.claude/check-extras.md` and run audit recipes it ships; bail per recipe message every surviving match, not commit until match-free. Probe not match → no-op.
3. **Pass** (verification exits 0 and tests added per plan and not §V regressed via full-suite re-run) → flip §T.n status `.` → `x`; auto-commit. Surface `/sdd:check` as Next-block item #1 per §V.<n> (cascade scan; not silent close). Next task.
4. **Fail** → invoke backprop skill. Do NOT retry blindly. Status stays `.`.

## FAIL → BACKPROP

On test/build failure:

1. Read failure output.
2. Classify failure: (a) code bug → step 3, (b) spec wrong → step 4, (c) unspec edge → step 4. Confident → proceed direct. Low-confidence (ambiguous or multiple plausible) → AskUserQuestion per decision-gate invariant w/ 3 options keyed (a)/(b)/(c), labels is action descriptions ("Code bug — fix and re-run", "Spec wrong — /sdd:spec bug:", "Unspec edge — /sdd:spec bug:"), header `Verify-fail class`.
3. (a) → fix code, re-run. No spec change.
4. (b) or (c) → invoke spec skill with `bug: <cause>` first, let it update §V and §B, then resume build against updated spec.

Rule: never silently fix root-cause without considering backprop. §B records bug-class precedent so recurrence-class blocked.

## WRITE POLICY

- Only flip §T status. No other SPEC.md edits from build.
- Other spec edits → invoke spec skill.
- Auto-commit on `.` → `x` per §T row; not user prompt. Message: `T<n>: <goal line>` + §V cites.
- Stage explicit `git add <listed-paths>` per plan; not `git add -A` — pre-existing dirty working-tree state not bundled.
- `/sdd:build --all` chains plan-once → every §T row {edit → verify → commit} autonomously.
- FAIL → not commit; FAIL→BACKPROP runs first.

## OUTPUT — "Next" block

Heading `## Next`; 1–5 atomic items (one sentence each, no `Reply` prefix); positional dispatch (`run <int>` or `run /<plugin>:<cmd> [args]`). Optional `## Hint` (≤ 3 lines) precedes when item selection needs hidden state. PLAN not wait-state so not execute/revise/abort items; EXECUTE-pass auto-commits so Next leads w/ `/sdd:check` post-§T-close cascade; after backlog cleared, swap `/sdd:build --next` for `/sdd:spec` seed.

Canonical example after EXECUTE pass (commit already auto-fired):

```
## Next

1. /sdd:check — cascade scan over the just-closed §T row
2. /sdd:build --next — start the next pending §T row
3. /sdd:spec amend §T.<n> — re-scope before continuing
```

Variant: backlog cleared (terminal state) → swap item 2 for `/sdd:spec` (seed new row), drop item 3.

## NON-GOALS

- No progress dashboards. `cat SPEC.md | grep §T` is the dashboard.
- No speculative work beyond chosen task scope.
