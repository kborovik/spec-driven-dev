---
name: steno
description: |
  Human-facing terse-prose register for non-author reviewers.
  Triggers: write/edit human-facing terse prose for review; user says
  "steno", "shorthand", "tighten this", "make this shorter".
allowed-tools: [Skill]
user-invocable: false
---

# steno — human-facing terse text

Audience: human reviewer scanning prose for facts — not a token-optimised model. Plain words, readable symbols; LLM-facing register → `telegraph` skill (same plugin).

## SKIM TEST

Top criterion: fact appears in first sentence or bold-lead bullet of each block. Skim fails → rewrite first clause to state the fact — not retain dense form, not cut further words. Compression subordinate: a word that aids the skim stays. Reviewer would slow on a symbol → use the word.

Self-check every paragraph/bullet:

- First clause states the fact (subject + verb ≤ 8 words).
- Subject and verb both visible — symbol-chain fragments fail.
- Anti-test: cover everything after first clause; core fact still readable.

## SCOPE

Human-facing terse prose for non-author reviewers — readers scan facts, benefit from compression w/o telegraph-symbol load.

Applies (not exhaustive):

- GitHub issues & PRs — titles, bodies (incl. PR desc refresh on merge).
- PR squash/merge commit bodies (release-note section).
- READMEs & user-facing docs where compression aids scan.

Not:

- Code, snippets, backticked text.
- Conventional Commits title prefix (`type(area):`) — fixed format.
- Error strings, log lines.
- External-facing copy (marketing, landing pages).

## SENTENCE SHAPE

Every prose sentence or bullet body:

1. **Lead-first** — subject + verb open the sentence; topic-shift & qualifier clauses → tail. Subject past first clause → skim fails.
2. **Visible subject-verb** — subject explicit or imperative (`Add X.` OK). No symbol-chain fragments: `auth → mw → handler` → `Auth middleware runs before the handler.`
3. **No hidden copulas** — elide `is`/`are` only when fragment unambiguous. Drop copula in `X — Y` only when Y reads as predicate, not apposition.
4. **≤ 1 participial phrase per sentence** — nesting kills first-clause readability.

Verb-headed fragments fine. Lists > paragraphs. One idea per line in lists. Break long sentences before cutting words.

## SYMBOLS

Safe for GitHub readers:

```
→   leads to / becomes / produces
≥   at least
≤   at most
&   and
|   or (in lists, not prose)
§   spec citation (`§V.<n>`, `§T.<n>`) — refs into SPEC.md only
```

No other symbols — math operators beyond this set → write the word; mirrors `telegraph` symbol policy.

## PRESERVE VERBATIM

- Code blocks, snippets, backticked text.
- Paths, URLs, `#123` issue/PR refs.
- Identifiers: function names, vars, env vars, flags.
- Numbers, versions, dates, SHAs.
- Error strings; SQL, regex, JSON, YAML.
- Quoted user-facing copy.
- `Resolves #N` / `Fixes #N` / `Closes #N` trailers — exact form.

## SHAPES

- **Bullets > paragraph** when listing > 2 items.
- **Definition list** for term/explanation pairs: `` - `--dry-run` — print actions, do not execute. ``
- **Table** for comparing options on same axes.
- **Headers + fragments** > full sentences in issue/PR bodies (see release-commit example below).

## EXAMPLES

**Issue body** — Anti fails rule 1 (lead-first): reader scans 14 words before the fact.

> When a user tries to log in with an email address that contains uppercase letters, the system fails to find their account because the lookup is being done in a case-sensitive manner, which is not the expected behavior for email addresses.

Good — first sentence states fact + condition; second states cause + fix direction:

> Login fails when email has uppercase letters. Lookup is case-sensitive — should be case-insensitive for emails.

**PR body** — Anti fails SKIM TEST: 8 filler words precede the fact.

> This pull request basically just adds some additional logging to the auth middleware so that we can debug issues more easily in production environments. It also includes a small refactor of the token validation logic.

Good — first fragment states both items; each bullet opens with a verb:

> ## Summary
>
> Add auth middleware logging for prod debugging. Refactor token validation.
>
> ## Changes
>
> - Log `userId`, `path`, `latency` on every authed request
> - Extract `validateToken()` from middleware into `auth/token.go`

**Release commit body** — Anti fails rule 4: nested participials, 47 words before the expiry fact.

> This change implements a new authentication system using JWT tokens which replaces the previous session-based authentication that was being used. Users will now be able to log in and receive a token that they can use to make authenticated requests, and these tokens will expire after a period of 24 hours.

Good — 4-word first sentence states the replacement; 3-word second states the constraint:

> ## Summary
>
> JWT auth replaces sessions. Tokens expire 24h.
>
> ## Changes
>
> - JWT generation & validation
> - `/auth/refresh` endpoint
> - Middleware reads `Authorization: Bearer <jwt>`
>
> ## Breaking
>
> - Session cookies dropped — clients must send `Authorization` header.

## BOUNDARIES

Literal phrasing w/ readable symbols (per SCOPE) — idiom adds parsing cost & ambiguity. Within scope, not:

- idiom ("moves the needle", "low-hanging fruit", "boil the ocean").
- word-level metaphor ("earns its keep", "bite", "smell").
- colloquialism ("gotcha", "ish", "yeah", "kinda").
- culture-loaded shorthand (sports, military, film references).

Exclusions:

- Colloquial sentence structure — allowed where it aids reviewer flow; register applies at word level.
- Domain-load-bearing named ops (`backprop`, `telegraph-encode`, `socratic`, `steno`).
- Established tech vocab doubling as metaphor (`drift`, `bottleneck`, `leak`) — allowed when standard term in context.
