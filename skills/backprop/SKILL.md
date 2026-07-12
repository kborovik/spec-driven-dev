---
name: backprop
description: |
  Bug → spec protocol: trace cause, decide if a new §V invariant catches the
  recurrence class, append §B. Not user-invoked — engaged from /sdd:spec
  BACKPROP mode (bug → spec user route = `/sdd:spec <intent>`). Not for
  mechanical typo or one-off fix w/ no recurrence class — pure code fix only.
allowed-tools: Read, Grep
user-invocable: false
---

# backprop — bug → spec

Plan-then-execute fixes code, forgets.
SDD fixes code AND edits spec so recurrence impossible.
That edit = backprop.

Analysis protocol — writes nothing itself (read-only grants).
Consumers: spec skill BACKPROP mode (records §B/§V, commits SPEC.md) + /sdd:build resume (test + fix, commits code).
See HANDOFF.

## WHEN

- Test fail at `/sdd:build` verification.
- User bug report.
- Post-mortem after production incident.
- `/sdd:check` flags VIOLATE w/ root cause found.

## THREE STEPS

1. **TRACE** — read failure output / report.
   Find exact file:line of wrong behavior.
   Name root cause, one telegraph sentence.
2. **ANALYZE** — three questions: new §V catches bug class? (most common: yes). §I wrong — spec claims shape code can't deliver? (sometimes). §T wrong — built wrong thing? (rare but real).
3. **PROPOSE** — draft spec change.
   Never skip §B; §V/§I/§T case-by-case.
   ```
   §B row: B<next>|<date>|<root cause>|V<N>
   §V line: V<N>: <testable rule that would have caught it>
   ```

## HANDOFF — two commits, cross-cited

Protocol output = drafted delta.
Writes split per write-ownership (spec = sole SPEC.md mutator; build = code writer):

1. **Spec commit** — spec skill BACKPROP mode applies §B (+ §V, §T) → auto-commit `backprop §B.<n>(+) + §V.<N>(+): <one-line cause>`.
   SPEC.md only.
   Record lands even when fix deferred.
2. **Code commit** — /sdd:build (resume or operator-dispatched): invariant w/o test = lie → add failing test first, name cites invariant (`TestV<N>_RefundIdempotent`), watch fail.
   Fix code.
   New test ! pass; full suite ! no regression.
   Commit `T<n>: <goal>` citing new §B/§V.

## WORKED EXAMPLE

Input: `refund job double-charged customer on retry`

1. TRACE: payment service retried on 5xx, no idempotency key → charge reversed twice.
   Cause: `refund(ctx, amount)` not check prior charge state.
2. ANALYZE: recurrence class? yes — every retry-able money-mutation in payment service exposed; future endpoints hit same trap → new §V.
3. PROPOSE:
   ```
   §B row: B<n>|2026-04-20|refund retry double-charged, no idempotency check|V<N>
   §V line: V<N>: every refund ! idempotency key check before charge reversal
   ```
4. HANDOFF spec commit: `backprop §B.<n>(+) + §V.<N>(+): refund retry double-charge` (SPEC.md only).
5. HANDOFF code commit via /sdd:build: `TestV<N>_RefundIdempotent` — refund twice w/ same key → ≤ 1 reversal posted; watch fail.
   Add idempotency-key column; check before `charge.reverse()`.
   Test pass, suite no regression → commit `T<n>: refund idempotency` citing §B.<n> + §V.<N>.

## GOOD INVARIANT

- Testable in code (grep-able or assert-able).
- Scoped to behavior, not file.
- Positive where possible (`! hold` over `not forbid`).
- Cites §I surface where applies.

Bad: `V<N>: code should be correct.`
Good: `V<N>: every pg_query ! params via driver, not string concat.`

## WHEN NOT §V

- Mechanical typo, no class (`i++` vs `i--` in throwaway).
- One-time migration fix.
- Root cause external dep → upgrade dep, note in §C.

Still append §B — records failure mode considered.
Future same-class bug → §B grep shows precedent.

## OUTPUT

§B entry (always) + §V (usually) drafted for spec skill; test + code fix land via /sdd:build.
Two commits, cross-cited: spec commit names §B/§V, code commit cites them.
No dashboards, no log files — SPEC.md + git = full history.
