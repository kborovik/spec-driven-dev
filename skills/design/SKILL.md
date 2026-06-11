---
name: design
description: |
  Propose-then-critique structural design loop → draft to `designs/<slug>.md`. Distinct from socratic (which sharpens vague intent). Use when user wants to design a structural change, weigh tradeoffs between named alternatives, propose an architecture, or shape a subsystem before implementation. Triggers: "/sdd:design", "design the X", "shape the X subsystem", "tradeoffs between A and B", "how should we structure", "propose an architecture for".
allowed-tools: AskUserQuestion, Read, Grep, Write, Skill
model: opus
---

# Design — propose-then-critique → designs/<slug>.md draft

## AUDIENCE

Skill body in SPEC-ADJACENT so glyph register. Design file output (`designs/<slug>.md`) is user-reviewing surface pre-spec-fold so steno register (readable symbols `→ & | §`, not heavy math glyphs `∀ ∃ ∴ ⊥ ∈ ∉`). Encoding follows audience.

## Position in funnel

`/sdd:design` is front door — caller has named the layer mentally and wants to commit a shape. Layer / shape-space unclear → loop step 2 localization questions narrow it. No auto-route — user-driven only.

## Loop

1. read `SPEC.md` in root → degrade gracefully if absent
2. topic vague or empty → ≤ 2 questions to localize, then propose
3. propose shape (named structures, types, key decisions) in 1 pass
4. surface `## Open Questions` list at bottom
5. wait → user critique / answers
6. update Proposal in place; resolved Qs → `## Design decisions` w/ rationale
7. repeat 5–6 until `## Open Questions` empty
8. on confirm → write draft to `designs/<slug>.md` (steno-encoded per template)

every turn: not self-resolve Open Questions. resolution ⊢ user input.

## Distinction from socratic

|skill|converges on|mechanism|
|socratic|"enough"|1 question/turn, sharpen intent|
|design|"exhausted"|propose shape, exhaust open Qs|

not merge. socratic = bug or small-feature framing. design = structural choice.

## Output template (design file body)

body in steno per `## AUDIENCE` (readable symbols, not heavy math glyphs). § citations OK if `SPEC.md` present.

```
# <title>

## Problem

[symptoms + §B/§V citations if SPEC.md present, else "designing without SPEC anchor"]

## Proposal

[named structures, types, shape — propose-then-critique starting point]

## [topic-specific sections, e.g. "Tool ownership", "Naming", "Layering"]

## Effect on in-flight SPEC items

[§T/§V deltas — what gets superseded, narrowed, unchanged. omit section if SPEC.md absent.]

## Design decisions

[each resolved Open Q + rationale, in `**Decision:** ... **Why:** ...` shape]

## Success criterion

[observable invariants — "X cannot recur", "Y returns Z", measurable]

## Out of scope

[deferred → §T row or future issue]

## Unresolved

[only if ≥3-turns/Q escape used — parked Qs for follow-up]
```

## Code reads

reactive only. not preemptive scans.

- not allowed: grep repo before first proposal "to find context". propose from user's framing + `SPEC.md`.
- ✓ allowed: user cites `file:line` or symbol or path → read that target. user claims behavior in code → spot-check before next proposal turn.

cap: ≤ 2 reads/turn. broader sweep needed → stop; return control to user for codebase investigation.

## SPEC.md degradation

`SPEC.md` in root absent → flag once: "designing without SPEC anchor; §V/§B/§T citations omitted". continue. omit `## Effect on in-flight SPEC items` from output.

## Long-session escape

single Open Q ≥ 3 turns w/o resolution → decision-gate per decision-gate invariant (mid-flow consequence-bearing prompt — selection drives persist-shape in current turn) → emit AskUserQuestion call:

- **question**: `Park unresolved Q under '## Unresolved' and converge on rest?`
- **options** (2 — mutually exclusive):
  - `Park Q and converge` — move Q to `## Unresolved`, proceed to convergence and persist
  - `Keep going` — return to step 5 loop
- **header**: `Open-Q escape`
- prose `or keep going?` form not allowed — selection drives `## Unresolved` shape in persisted draft.

park → persisted draft carries explicit unresolved list in `## Unresolved` section. not pretend resolved.

## Mode

write-new-design-file only. not append-to-existing.

## Title and slug

draft body opens w/ `# <title>` heading. conventional-commits prefix optional (`feat(<scope>): ...`, `refactor(<scope>): ...`) — design-ness encoded via file location (`designs/`), not title prefix duplicating it.

slug derivation:
- short kebab-case (`<noun-phrase>` or `<scope>-<noun>`); ≤ 5 words, ≤ 50 chars.
- ambiguous topic → ask user once for slug confirmation.
- collision (`designs/<slug>.md` exists) → append `-<n>` suffix.

filename: `designs/<slug>.md`.

## Persist

1. `designs/` dir @ repo root — auto-created by `Write` on draft persist (no `Bash` mkdir needed).
2. derive slug per § above.
3. write design body (steno-encoded per template) to `designs/<slug>.md`.
4. show file path + summary to user.

not commit. caller may stage manually or wait for `/sdd:spec` fold-in (folds → SPEC.md and leaves design file in working tree per design-lifecycle invariant in SPEC.md; user removes or preserves manually post-fold).

## Convergence gate

ready iff `## Open Questions` empty and user confirms.

not persist w/o confirmation. not self-resolve Qs. not collapse multiple Qs into one to fake convergence.

## Boundary

not mutate `SPEC.md`. design produces `designs/<slug>.md` draft only. SPEC amendment ⊢ caller runs `/sdd:spec <designs/<slug>.md>` after persist (gate routes to design-file fold-in per design-lifecycle invariant in SPEC.md). impl ⊢ `/sdd:build` after spec amended.

not root-cause debugging — that belongs to the backprop skill (user route is `/sdd:spec <bug intent>`, gate → BACKPROP). design = structural shape, not "why is this broken".

## Escape hatch

"just file it" or "skip the design" or "I already know what I want" → stop. hand verbatim intent to `/sdd:spec` (amend SPEC directly w/o design draft).

## OUTPUT — "Next" block

Heading `## Next`; 1–5 atomic items (one sentence each, no `Reply` prefix); positional dispatch (`run <int>` or `run /<plugin>:<cmd> [args]`). Optional `## Hint` (≤ 3 lines) precedes when item selection needs hidden state (e.g. fold-in leaves `designs/<slug>.md` in working tree post-apply so user removes or preserves manually). Design is iterative: mid-loop items lead w/ Open-Q resolution (answer, park, abort); post-persist items lead w/ `/sdd:spec <designs/<slug>.md>` fold-in and escape hatches (`/sdd:design` rework).

Example mid-loop with Open Questions outstanding:

```
## Next

1. answer the next Open Question to converge the proposal
2. /sdd:design park — move unresolved Q under `## Unresolved` and persist
3. /sdd:spec <intent> — amend SPEC directly w/o design draft
```

Example after persist (terminal — `designs/<slug>.md` written):

```
## Next

1. /sdd:spec designs/<slug>.md — fold the draft into SPEC.md
2. /sdd:design <topic> — re-run for a revised draft (new file per write-new mode)
```
