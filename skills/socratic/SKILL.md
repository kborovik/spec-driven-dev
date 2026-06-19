---
name: socratic
description: |
  Parameterized single-question intent-sharpening gate. Not user-invoked — engaged from consumer cmd pre-apply gate (e.g. /sdd:spec).
allowed-tools: AskUserQuestion, Read, Grep
user-invocable: false
---

# socratic — parameterized intent gate

## CALLER CONTRACT

caller passes:

1. **mode-decision space** — mode names skill may return. e.g. `{file}`; `{NEW, DISTILL, BACKPROP, AMEND}`.
2. **convergence triple per mode** — `mode → required facts`. e.g. `BACKPROP → {symptom, surface, recurrence-class}`; `AMEND → {§-target, delta}`.
3. **intent string** — user's free-form input (typically `$ARGUMENTS`).

skill returns `(converged-mode, facts)` — data only; not file, not commit, not write artifact. skill owns question selection, convergence check, escape hatch, teach overlay. caller owns draft, file-write, git ops, root-cause analysis. skill not know caller's artifact shape — checks fact presence per triple, not meaning.

## LOOP

1. ask 1 question
2. wait for answer
3. pick next question from pool or converge
4. converge → return `(mode, facts)`

every turn: 1 question. not batched. not checklist tone. not re-ask facts already supplied.

## QUESTION POOL

- `clarify` — symptom vague → "what specifically — input → observed vs expected?"
- `scope` — ask epic-shaped → "smallest change that removes the pain?"
- `boundary` — unclear what stays untouched → "what works today that must keep working?"
- `success` — no acceptance criterion → "how do we know it's fixed without re-asking you?"
- `frame` — user names fix, not problem → "is that the problem, or your current guess at the solution?"
- `first-principle` — mode NEW and no foundational claim stated → "name ≥ 1 foundational claim other invariants derive from — what is this artifact, fundamentally?"

pick by what's most missing.

NEW mode: fire first-principle probe explicitly, once — not buried under clarify. user may decline → converge on remaining triple facts. record `first-principle-asked` in returned facts regardless of answer.

## TONE

interrogate problem, not user. probe statement, not judgment. not "are you sure?" → "what would falsify this?"

## CODE READS

reactive only. not grep repo pre-questions to "find the bug" — undermines dialogue, duplicates caller's investigation. user cites `file:line`/symbol/path → read that target. user claims breakage w/o data → spot-check before next question.

shape: "looking at `<file>:<line>`, [observable fact] — given that, [next question]". model verifies, user diagnoses. ≤ 2 reads/turn; broader sweep needed → stop dialogue, return control to caller.

## TEACH

overlay, not phase. answer reveals gap → surface distinction in 1–2 sentences, then next question. not lecture.

- fix named as problem → symptom vs cause vs solution
- unfalsifiable success crit → verifiable = observable + bounded
- scope conflated w/ ambition → smallest-change seam vs total redesign
- breakage assumed w/o data → observed vs expected vs assumed

## CONVERGENCE

converged iff some mode's triple fully present in dialogue history. ≥ 3 turns w/o convergence → AskUserQuestion per decision-gate invariant (selection drives same-turn return-vs-resume; prose `or keep going?` form not allowed). header `Converge?`, mutually-exclusive labels: `Return now` (stop dialogue → return `(mode, partial-facts)` + `unmet-criteria` per ESCAPE HATCH) / `Keep going` (resume LOOP).

## ESCAPE HATCH

"just file it" / "skip the questions" / "I know what I want" → stop dialogue, not bypass gate: audit facts vs triples. gaps → ask once for missing piece or return `(mode, partial-facts)` + explicit `unmet-criteria` list so caller surfaces gaps in artifact (e.g. `## Unresolved` callout). gaps stay visible; user's "done thinking" honored.
