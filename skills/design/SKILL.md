---
name: design
description: |
  SDD structural design: propose-then-critique via Claude Code plan mode →
  approved plan opens a GitHub issue (class label) then stops. Later fold via
  `/sdd:spec github issue N`. Exhausts structural Open Questions (distinct from
  socratic "enough"). Use when user wants to design a structural change, weigh
  tradeoffs between named alternatives, propose an architecture, or shape a
  subsystem before implementation. Triggers: "/sdd:design", "design the X",
  "shape the X subsystem", "tradeoffs between A and B", "how should we
  structure", "propose an architecture for".
allowed-tools: AskUserQuestion, Read, Grep, EnterPlanMode, ExitPlanMode
argument-hint: "<topic>"
---

# design — propose-then-critique via Claude Code plan mode

Skill body SPEC-ADJACENT → telegraph.
Plan body user-reviewed pre-issue → steno: spell out arrows and inequalities as words, keep only `|` `§` raw (per steno SYMBOLS).

## POSITION IN FUNNEL

`/sdd:design` is the structural front door.
Caller wants a durable GitHub issue before `/sdd:spec` fold-in.
Layer unclear → ≤ 2 questions, then propose.
No auto-route — user-driven only.

## ARTIFACT — plan mode, not designs/

Primary working artifact = Claude Code session **plan file** (path named by the plan-mode harness).

1. Call `EnterPlanMode` at start (user must approve plan mode).
2. Write / patch the design proposal **only** into the plan file — plan mode owns that path (harness write; no skill `Write` grant); other writes blocked.
3. Iterate Open Questions until empty.
4. Call `ExitPlanMode` w/ the plan body to present it for approval.
5. On approve → hand issue payload to github ISSUE then stop — see POST-APPROVE.
6. No default write to `designs/<slug>.md`.
   Optional durable export only if operator asks (`designs/<slug>.md` after approval, outside plan mode).

Legacy `designs/*.md` still folds via `/sdd:spec designs/<slug>.md` for old drafts.

## LOOP

1. `EnterPlanMode` (declined → offer escape to `/sdd:spec` direct amend).
2. Read `SPEC.md` @ root (citation context only — never written this run); absent → degrade per § below.
3. Topic vague or empty → ≤ 2 questions to localize, then propose.
4. Propose design (named structures, types, key decisions) in 1 pass → write plan file.
5. Surface `## Open Questions` list at bottom of plan.
6. Wait → user critique / answers.
7. Patch plan in place; resolved Qs → `## Design decisions` w/ rationale.
8. Repeat 6–7 until `## Open Questions` empty.
9. `ExitPlanMode` → user approves plan.
10. On approve → POST-APPROVE; never mutate SPEC.md.

Never self-resolve Open Qs.
Never `ExitPlanMode` with open Qs unless escape parks them under `## Unresolved`.
Never mutate SPEC.md this run.

## DISTINCTION FROM SOCRATIC

- `socratic` — converges on "enough": 1 question/turn, sharpen intent.
- `design` — converges on "exhausted": propose design, exhaust open Qs.

Not merged. socratic = bug or small-feature framing. design = structural choice.

## OUTPUT TEMPLATE (plan body)

steno body; § citations OK when `SPEC.md` present.

```
# <title>

## Problem

[symptoms + §B/§V cites; no SPEC.md → "designing without SPEC anchor"]

## Proposal

[named structures, types, shape]

## [topic-specific sections]

## Effect on in-flight SPEC items

[§T/§V deltas described here, never applied to SPEC.md. omit if SPEC.md absent]

## Design decisions

[each resolved Q: **Decision:** ... **Why:** ...]

## Success criterion

[observable invariants]

## Class

[enhancement | bug | documentation; default enhancement]

## Out of scope

[deferred]

## Unresolved

[only if escape used]
```

## CODE READS

Reactive only — no preemptive scans.
Banned: grep repo before first proposal "for context".
OK: user cites `file:line` / symbol → read target.
Cap ≤ 2 reads/turn.

## SPEC.md DEGRADATION

`SPEC.md` absent → flag once: "designing without SPEC anchor; §V/§B/§T citations omitted".
Continue; omit Effect section.

## LONG-SESSION ESCAPE

Single Open Q ≥ 3 turns unresolved → AskUserQuestion per decision-gate invariant (selection drives same-turn park-vs-resume; prose `or keep going?` form not allowed):

- header `Open-Q escape`
- `Park Q and converge` / `Keep going`

Park → `## Unresolved` in plan.

## POST-APPROVE

On plan approve (after `ExitPlanMode`): hand off to github ISSUE (auto-fire); github owns `gh label create` and `gh issue create`.
This skill stops after the hand-off.

1. Title = plan `# <title>`.
2. Body = steno plan (Problem + Proposal + Design decisions + Effect on in-flight SPEC items + Out of scope + Unresolved when present).
   `## Acceptance` checklist (`- [ ]`) from Success criterion (each sentence or bullet → one open item).
   Empty Success criterion → one `- [ ]` bullet from the plan title.
3. Label = `## Class` when in {enhancement, bug, documentation}; missing or other → enhancement.
4. Hand title, steno body, `## Acceptance` bullets, and class to github ISSUE (auto-fire); github owns `gh label create` and `gh issue create --label`.
5. Read issue N back from the printed URL (`.../issues/N`).
6. Stop — never fold SPEC.md this run.

Next leads issue URL + `/sdd:spec github issue N`.
`/sdd:spec fold-design` = optional same-session exclusion (retains issue N linkage).

Post-approve Next:

```
## Next

1. /sdd:spec github issue N — fold <issue-url> into SPEC.md
2. /sdd:design <topic> — re-run for a revised plan
3. /sdd:spec fold-design — optional same-session fold of approved plan (retains issue N linkage)
```

## ESCAPE HATCH

"just file it" / "skip design" / "I already know" → stop; hand intent to `/sdd:spec`.

## BOUNDARY

Never mutate `SPEC.md` this skill.
Not root-cause debugging — backprop via `/sdd:spec <bug intent>`.

## MECHANIZE

Load `${CLAUDE_SKILL_DIR}/../_fragments/MECHANIZE.md`.

## OUTPUT — "Next" block

Per `${CLAUDE_SKILL_DIR}/../_fragments/NEXT.md`.
Mid-loop → Open-Q resolution items.
Post-approve → issue URL + `/sdd:spec github issue N` lead; fold-design optional exclusion.
