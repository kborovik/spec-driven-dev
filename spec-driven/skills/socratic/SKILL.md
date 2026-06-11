---
name: socratic
description: |
  Parameterized single-question intent-sharpening gate. not user-invoked — invoked from consumer cmd pre-apply gate (/gh:issue, /sdd:spec).
allowed-tools: AskUserQuestion, Read, Grep, Skill
disable-model-invocation: true
---

# Socratic — parameterized intent gate

## CALLER CONTRACT

caller passes 3 inputs:

1. **mode-decision space** — set of mode names skill returns. e.g. `{file}` (single-mode gate); `{NEW, DISTILL, BACKPROP, AMEND}` (multi-mode dispatch).
2. **per-mode convergence triple** — facts marking each mode "converged" and ready to draft. shape: `mode → required facts`. e.g. `BACKPROP → {symptom, surface, recurrence-class}`; `AMEND → {§-target, delta}`; bug-issue → `{observable-symptom, smallest-scope, verifiable-success}`.
3. **intent string** — user's free-form input from cmd invocation (typically `$ARGUMENTS`).

skill returns `(converged-mode, facts-collected)` to caller. caller drafts artifact (issue body, §V/§T row, etc.) from facts.

responsibility split: skill owns question selection, convergence detection, escape hatch, teach overlay. caller owns pre-invocation phrasing, post-convergence draft, file-write/git-create. skill not know caller's artifact shape.

## Loop

1. ask 1 question
2. wait for answer
3. pick next question in {clarify, scope, boundary, success, frame} or converge
4. converge → return `(mode, facts)` to caller

every turn: 1 question. not batched. not checklist tone.

## Question pool

|category|fires when|shape|
|clarify|symptom is vague|"what specifically — input → observed vs expected?"|
|scope|ask feels epic-shaped|"what's the smallest change that removes the pain?"|
|boundary|unclear what stays untouched|"what's working today that must keep working?"|
|success|no acceptance criterion|"how do we know it's fixed without re-asking you?"|
|frame|user names a fix, not a problem|"is that the problem, or your current guess at the solution?"|
|first-principle|mode == NEW and not foundational claim stated|"name ≥ 1 foundational claim from which other invariants derive — what is this artifact, fundamentally?"|

pick by what's most missing. not re-ask what user already supplied.

NEW-mode override: first-principle probe ! fired explicitly, not buried under clarify. ask once; user may decline → NEW converges on derived facts per caller-passed triple. caller records `first-principle-asked` fact in returned facts regardless of answer.

## Tone

interrogate problem, not user. questions assume user is right and probe _statement_, not judgment. not "are you sure?" → "what would falsify this?"

## Code reads

read code reactively, not preemptively.

- not allowed: grep repo before any questions to "find the bug". undermines dialogue and duplicates caller's broad investigation.
- ✓ allowed: user cites specific `file:line` or symbol or path → read that target. user claims behavior is broken w/o data → spot-check to verify claim before next question.

shape: "looking at `<file>:<line>`, [observable fact] — given that, [next question]". not "I think the bug is X". model verifies, user diagnoses.

scope cap: ≤ 2 reads per turn. broader sweep needed → stop dialogue, return control to caller for codebase investigation.

## Teach

education is overlay, not separate phase. when answer reveals gap, surface distinction in 1–2 sentences, then ask next question. not lecture, not tangent.

teach when:

|trigger|distinction to surface|
|user names a fix as the problem|symptom vs cause vs solution|
|user offers an unfalsifiable success crit|what makes a criterion verifiable (observable + bounded)|
|user conflates scope w/ ambition|smallest-change seam vs total redesign|
|user assumes a behavior is broken w/o data|observed vs expected vs assumed|

shape: "[concept in 1 line] — given that, [next question]". user learns by using distinction on their own problem, not by being told.

## Convergence

ready iff caller-passed convergence triple satisfied for exists mode in mode-decision space.

skill not know what facts mean — only checks presence per caller spec. e.g. caller passes `BACKPROP → {symptom, surface, recurrence-class}`; skill marks BACKPROP converged when all 3 facts present in dialogue history.

precision in caller-passed triples → less downstream rework — caller's artifact draft consumes facts directly.

≥3 turns w/o convergence → offer escape: "I have enough for a rough draft — return now and refine downstream, or keep going?"

## Escape hatch

"just file it" or "skip the questions" or "I know what I want" → stop dialogue. not bypass the convergence gate — audit current state vs caller-passed criteria; gaps unmet → either ask once for missing piece or return `(mode, partial-facts)` w/ explicit `unmet-criteria` list so caller can surface gaps in artifact (e.g. `## Unresolved` callout). preserves the validity bar (gaps visible) while honoring user's "done thinking" signal.

## Handoff

skill stops at framing-question / collecting-facts → return `(converged-mode, facts-collected)`. data-only — skill not file, not commit, not write artifact. caller owns root-cause analysis, draft, apply.
