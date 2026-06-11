---
name: backprop
description: |
  Bug → spec protocol. On bug found or test fail → trace cause, decide if new
  §V invariant catches recurrence, append to §B. Triggers: test failure, bug
  report, post-mortem, explicit user ask. Phrasings: "X broke", "we got bit
  by", "post-mortem on Y", "this should never recur", "add a §V for". not for
  mechanical typo or one-off fix w/ not recurrence class — pure code fix only.
allowed-tools: Read, Grep, Glob, Skill
disable-model-invocation: true
---

# backprop — bug → spec

Plan-then-execute fixes the code and forgets.
SDD fixes the code AND edits spec so recurrence is impossible.
That edit is backprop.

## WHEN TO BACKPROP

- Test failed at `/sdd:build` verification.
- User reports bug.
- Post-mortem after production incident.
- `/sdd:check` flags VIOLATE with root cause found.

## SIX STEPS

### 1. TRACE
Read failure output / bug report.
Find exact file:line of wrong behavior.
Name root cause in one telegraph sentence.

### 2. ANALYZE
Ask three questions:
- Would a new §V invariant catch this class of bug? (most common: yes)
- Is §I wrong — did spec claim shape the code cannot deliver? (sometimes)
- Is §T wrong — did we build the wrong thing? (rare but real)

### 3. PROPOSE
Draft the spec change. Never skip §B; §V/§I/§T are case-by-case.

Template:
```
§B row: B<next>|<date>|<root cause>|V<N>
§V line: V<next>: <testable rule that would have caught it>
```

Example:
```
§B row: B<n>|<date>|refund job ran twice on retry|V<N>
§V line: V<N>: every refund → idempotency key check before charge reversal
```

### 4. GENERATE TEST
New invariant without test = lie. Add failing test first.
Name test so it cites the invariant: `TestV<N>_RefundIdempotent`.

### 5. VERIFY
Fix code. Run test. Must pass. Run full suite. Must not regress.

### 6. LOG
Commit spec edit + test + code fix together.
Commit msg: `backprop §B.<n> + §V.<N>: <one-line cause>`.

## WORKED EXAMPLE

Walks the six steps end-to-end on one bug. Numbers fictional; demonstrates judgment.

**Input**: `bug: refund job double-charged customer on retry`

1. **TRACE**: payment service retried on 5xx; not idempotency key → charge reversed twice. cause: `refund(ctx, amount)` not check prior charge state.
2. **ANALYZE**: recurrence class? yes — every retry-able money-mutation in payment service exposed; future endpoints will hit same trap. → new §V warranted.
3. **PROPOSE**:
   ```
   §B row: B<n>|2026-04-20|refund retry double-charged because no idempotency check|V<N>
   §V line: V<N>: every refund ! idempotency key check before charge reversal
   ```
4. **GENERATE TEST**: `TestV<N>_RefundIdempotent` — invoke refund twice w/ same key → expect ≤ 1 reversal posted.
5. **VERIFY**: add idempotency-key column to refunds table; check before `charge.reverse()`. Run new test → pass. Run full suite → not regression.
6. **LOG**: commit code + test + spec edit. msg: `backprop §B.<n>(+) + §V.<N>(+): refund retry double-charge`.

## WHAT MAKES A GOOD INVARIANT

- Testable in code (grep-able or assert-able).
- Scoped to a behavior, not a file.
- Stated positively when possible (`! hold` over `not forbid`).
- References §I surface where it applies.

**Bad**: V<N>: code should be correct.
**Good**: V<N>: every pg_query ! params interpolated via driver, not string concat.

## WHEN NOT TO ADD §V

- Bug was purely mechanical typo with no class (`i++` vs `i--` in throwaway).
- Fix is a one-time migration.
- Root cause is external dep (upgrade deps instead, note in §C).

Still append §B entry — record that this failure mode was considered. Future bug in same class → §B search shows precedent.

## OUTPUT SHAPE

Every backprop run produces:
1. §B entry (always).
2. §V entry (usually).
3. Test file (when §V added).
4. Code fix.
5. One commit.

No dashboards. No log files. SPEC.md + git is the full history.
