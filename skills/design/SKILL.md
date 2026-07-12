---
name: design
description: |
  Propose-then-critique structural design loop → draft to `designs/<slug>.md`. Distinct from socratic (which sharpens vague intent). Use when user wants to design a structural change, weigh tradeoffs between named alternatives, propose an architecture, or shape a subsystem before implementation. Triggers: "/sdd:design", "design the X", "shape the X subsystem", "tradeoffs between A and B", "how should we structure", "propose an architecture for".
allowed-tools: AskUserQuestion, Read, Grep, Write
model: fable
---

# design — propose-then-critique → designs/<slug>.md draft

Skill body SPEC-ADJACENT → telegraph.
Design file body user-reviewed pre-fold → steno: spell out `→ ≥ ≤ &` as words, keep only `|` `§` raw (per steno SYMBOLS).

## POSITION IN FUNNEL

`/sdd:design` is front door — caller named the layer mentally, wants to commit a shape.
Layer / shape-space unclear → loop step 2 questions narrow.
No auto-route — user-driven only.

## LOOP

1. read `SPEC.md` @ root (citation context only — never written this run); absent → degrade per § below
2. topic vague or empty → ≤ 2 questions to localize, then propose
3. propose shape (named structures, types, key decisions) in 1 pass
4. surface `## Open Questions` list at bottom
5. wait → user critique / answers
6. patch Proposal in place; resolved Qs → `## Design decisions` w/ rationale
7. repeat 5–6 until `## Open Questions` empty
8. user confirms → persist per `## PERSIST`

never self-resolve Open Qs — resolution requires user input. never persist w/o confirmation. never collapse multiple Qs into one to fake convergence.

## DISTINCTION FROM SOCRATIC

- `socratic` — converges on "enough": 1 question/turn, sharpen intent.
- `design` — converges on "exhausted": propose shape, exhaust open Qs.

not merged. socratic = bug or small-feature framing. design = structural choice.

## OUTPUT TEMPLATE (design file body)

steno body; § citations OK when `SPEC.md` present.

```
# <title>

## Problem

[symptoms + §B/§V cites; no SPEC.md → "designing without SPEC anchor"]

## Proposal

[named structures, types, shape]

## [topic-specific §s, e.g. "Tool ownership", "Naming", "Layering"]

## Effect on in-flight SPEC items

[§T/§V deltas — superseded, narrowed, unchanged — described in THIS file, never applied to SPEC.md. omit § if SPEC.md absent]

## Design decisions

[each resolved Q: `**Decision:** ... **Why:** ...`]

## Success criterion

[observable invariants — "X cannot recur", "Y returns Z", measurable]

## Out of scope

[deferred → §T row or future issue]

## Unresolved

[only if ≥3-turn escape used — parked Qs for follow-up]
```

## CODE READS

reactive only — no preemptive scans.

- banned: grep repo before first proposal "for context". propose from user framing + `SPEC.md`.
- OK: user cites `file:line` / symbol / path → read target. user claims code behavior → spot-check before next proposal turn.

cap ≤ 2 reads/turn. broader sweep needed → stop, return control to user for codebase investigation.

## SPEC.md DEGRADATION

`SPEC.md` @ root absent → flag once: "designing without SPEC anchor; §V/§B/§T citations omitted". continue; omit `## Effect on in-flight SPEC items` from output.

## LONG-SESSION ESCAPE

single Open Q ≥ 3 turns unresolved → AskUserQuestion per decision-gate invariant (selection drives persist-shape in current turn; prose `or keep going?` form not allowed):

- **question**: `Park unresolved Q under '## Unresolved' and converge on rest?`
- **header**: `Open-Q escape`
- **options** (2, mutually exclusive):
  - `Park Q and converge` — Q → `## Unresolved`, proceed to convergence + persist
  - `Keep going` — back to step 5

park → persisted draft carries Q under `## Unresolved` — not pretend resolved.

## TITLE AND SLUG

body opens `# <title>`. conventional-commits prefix optional (`feat(<scope>): ...`) — design-ness encoded by `designs/` location, not title prefix.

slug: short kebab-case (`<noun-phrase>` or `<scope>-<noun>`), ≤ 5 words, ≤ 50 chars. ambiguous topic → ask once for confirmation. collision → append `-<n>`.

## PERSIST

write-new only — never append to existing design file. `Write` auto-creates `designs/` @ repo root (no `Bash` mkdir).

1. derive slug per § above
2. write steno body per template → `designs/<slug>.md`
3. show file path + summary

not commit — caller stages manually or runs `/sdd:spec designs/<slug>.md` fold-in (folds → SPEC.md, leaves design file in working tree per design-lifecycle invariant in SPEC.md; user removes or preserves manually post-fold).

## BOUNDARY

never mutate `SPEC.md` — output is `designs/<slug>.md` only.
SPEC amend = `/sdd:spec <designs/<slug>.md>` post-persist (gate routes to fold-in); impl = `/sdd:build` post-amend.

not root-cause debugging — backprop skill owns that (user route `/sdd:spec <bug intent>`, gate → BACKPROP). design = structural shape, not "why is this broken".

## ESCAPE HATCH

"just file it" / "skip the design" / "I already know what I want" → stop; hand verbatim intent to `/sdd:spec` (amend SPEC directly, no design draft).

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
Optional `## Hint` (≤ 3 lines) precedes when selection needs hidden state (e.g. fold-in leaves design file in working tree post-apply). mid-loop → items lead w/ Open-Q resolution (answer, park, abort); post-persist → items lead w/ `/sdd:spec <designs/<slug>.md>` fold-in + escape hatches (`/sdd:design` rework).

mid-loop example (Open Qs outstanding):

```
## Next

1. answer the next Open Question to converge the proposal
2. /sdd:design park — move unresolved Q under `## Unresolved` and persist
3. /sdd:spec <intent> — amend SPEC directly w/o design draft
```

post-persist example (terminal — `designs/<slug>.md` written):

```
## Next

1. /sdd:spec designs/<slug>.md — fold the draft into SPEC.md
2. /sdd:design <topic> — re-run for a revised draft (new file per write-new mode)
```
