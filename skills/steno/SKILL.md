---
name: steno
description: |
  Simple technical language for human readers — terse-prose register for
  non-author reviewers.
  Triggers: write/edit human-facing terse prose for review; user says
  "steno", "shorthand", "tighten this", "make this shorter".
user-invocable: false
---

# steno — simple technical language

Audience: human reviewer scanning prose for facts — not a token-optimised model.
Anchor: simple technical language — clarity primary, compression subordinate; a word that aids the skim stays.
LLM-facing register → `telegraph` skill (same plugin).

## SCOPE

Human-facing terse prose for non-author reviewers — readers scan facts, benefit from compression w/o telegraph-symbol load.

Applies (not exhaustive):

- GitHub issues & PRs — titles, bodies (incl. PR desc refresh on merge).
- Commit-message bodies, incl. PR squash/merge release-note sections (subjects = per-skill fixed templates, preserve verbatim).
- READMEs & user-facing docs where compression aids scan.

Not:

- Code, snippets, backticked text.
- Conventional Commits title prefix (`type(area):`) — fixed format.
- Error strings, log lines.
- External-facing copy (marketing, landing pages).

## CORE — lead-first, one idea per sentence

Top criterion: fact appears in first sentence or bold-lead bullet of each block.
Skim fails → rewrite first clause to state the fact — not retain dense form, not cut further words.
Reviewer would slow on a symbol → use the word.

Every prose sentence or bullet body:

1. **Lead-first** — subject + verb open the sentence; topic-shift & qualifier clauses → tail.
   Subject past first clause → skim fails.
2. **One idea per sentence** — short sentences; break a long sentence before cutting words from it.
   One idea per line in lists.
3. **Visible subject-verb** — subject explicit or imperative (`Add X.` OK).
   No symbol-chain fragments: `auth → mw → handler` → `Auth middleware runs before the handler.`
4. **No hidden copulas** — elide `is`/`are` only when fragment unambiguous.
   Drop copula in `X — Y` only when Y reads as predicate, not apposition.
5. **≤ 1 participial phrase per sentence** — nesting kills first-clause readability.
6. **Expand an acronym on first use** — first mention spells the term, acronym in parens: `spec-driven development (SDD)`.
   Common web/protocol acronyms (`API`, `URL`, `JSON`, `HTTP`, `JWT`) exempt.
   Mirrors the define-term-on-first-use clarity rule.
7. **Cite rides the tail** — `§V.<n>` / `§T.<n>` / `#123` closes the sentence, never opens or carries it: `§V.<n> says spell out symbols` → `Spell out symbols per §V.<n>`.
   Subject + verb lead; the cite is reference, not subject.

Self-check every paragraph/bullet:

- First clause states the fact (subject + verb ≤ 8 words).
- Subject and verb both visible — symbol-chain fragments fail.
- Anti-test: cover everything after first clause; core fact still readable.

Shape defaults:

- Verb-headed fragments fine.
- **Bullets > paragraph** when listing > 2 items.
- **Definition list** for term/explanation pairs: `` - `--dry-run` — print actions, do not execute. ``
- **Headers + fragments** > full sentences in issue/PR bodies.
- `|`-table only for keyed fixed-schema data rows per table-use invariant; option comparison or concept set → bullet list.

## QUESTION SHAPE

Claude asks the operator to decide (AskUserQuestion prose, per decision-gate invariant):

1. **State the choice first** — one sentence naming the decision.
2. **List the options plainly** — one line each, mutually exclusive, no idiom.
3. **Recommend** — one sentence: the default and why.

Cite rides the tail (per CORE).
No prose `or keep going?` escape — a same-turn choice is a gate, not a sentence.

## SYMBOLS

Two raw symbols safe for GitHub readers:

```
|   or (in lists, not prose)
§   spec citation (`§V.<n>`, `§T.<n>`) — refs into SPEC.md only
```

Spell out everything else as words: `→` as "leads to" / "becomes" / "produces", `≥` as "at least", `≤` as "at most", `&` as "and".
No other symbols; a math operator beyond `|` and `§` → write the word.
Diverges from `telegraph` (the LLM-facing register keeps `→ ≥ ≤`): a human reader slows on a symbol, so the word wins.

## PRESERVE VERBATIM

- Code blocks, snippets, backticked text.
- Paths, URLs, `#123` issue/PR refs.
- Identifiers: function names, vars, env vars, flags.
- Numbers, versions, dates, SHAs.
- Error strings; SQL, regex, JSON, YAML.
- Quoted user-facing copy.
- `Resolves #N` / `Fixes #N` / `Closes #N` trailers — exact form.

## EXAMPLES

**Issue body** — Anti fails CORE rule 1 (lead-first): reader scans 14 words before the fact.

> When a user tries to log in with an email address that contains uppercase letters, the system fails to find their account because the lookup is being done in a case-sensitive manner, which is not the expected behavior for email addresses.

Good — first sentence states fact + condition; second states cause + fix direction:

> Login fails when email has uppercase letters. Lookup is case-sensitive — should be case-insensitive for emails.

**PR body** — Anti fails the skim test: 8 filler words precede the fact.

> This pull request basically just adds some additional logging to the auth middleware so that we can debug issues more easily in production environments. It also includes a small refactor of the token validation logic.

Good — first fragment states both items; each bullet opens with a verb:

> ## Summary
>
> Add auth middleware logging for production debugging. Refactor token validation.
>
> ## Changes
>
> - Log `userId`, `path`, `latency` on every authed request
> - Extract `validateToken()` from middleware into `auth/token.go`

## BOUNDARIES

Literal phrasing w/ the two raw symbols (per SCOPE); idiom adds parsing cost and ambiguity.
Within scope, not:

- idiom ("moves the needle", "low-hanging fruit", "boil the ocean").
- word-level metaphor ("earns its keep", "bite", "smell").
- colloquialism ("gotcha", "ish", "yeah", "kinda").
- culture-loaded shorthand (sports, military, film references).
- jargon-idiom ("load-bearing", "by-construction", "hand-rolled", "clean-slate", "prior-art", "carry-cost") — observed in spec prose; write the literal meaning.

Exclusions:

- Colloquial sentence structure — allowed where it aids reviewer flow; register applies at word level.
- Named domain operations (`backprop`, `telegraph-encode`, `socratic`, `steno`).
- Established tech vocab — closed allowlist only: `drift`, `bottleneck`, `leak`.
  A term off the list → plain word.
