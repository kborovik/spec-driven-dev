---
name: steno
description: |
  Human-facing terse-prose register for non-author reviewers.
  Triggers: write/edit human-facing terse prose for review; user says
  "steno", "shorthand", "tighten this", "make this shorter".
allowed-tools: [Skill]
disable-model-invocation: true
---

# steno — human-facing terse text

Audience: human reviewer scanning prose for facts — not a token-optimised model. Plain words and readable symbols; math glyphs belong to the `glyph` skill (`sdd` plugin).

## SKIM TEST

Top criterion: a reviewer scans the text and the fact appears in the first sentence or bold-lead bullet of each block. Skim fails → rewrite the first clause; not retain dense form, not cut further words.

Self-check every paragraph or bullet:

- First clause states the fact (subject + verb ≤ 8 words).
- Subject and verb both visible — symbol-chain fragments fail the test.
- Anti-test: cover everything after the first clause; the core fact remains readable.

Compression subordinate to this test — a word that aids the skim stays.

## SCOPE

Criterion: human-facing terse prose for non-author reviewers — readers scan facts, benefit from compression w/o math-glyph load.

Common applications (not exhaustive):

- GitHub issues and PRs — titles, bodies (incl. PR desc refresh on merge).
- PR squash/merge commit message bodies (release-note section).
- Insights comments emitted by gh skills.
- READMEs and user-facing docs where compression aids scan.

not apply to:

- Code, snippets, backticked text.
- Conventional Commits title prefix (`type(area):`) — fixed format.
- Error strings, log lines.
- External-facing copy (marketing, landing pages).

## SENTENCE SHAPE

Four rules every prose sentence or bullet body:

1. **Lead-first** — subject + verb open the sentence; topic-shift and qualifier clauses move to the tail. Subject delayed past the first clause → skim test fails.
2. **Visible subject-verb** — subject explicit or imperative form (subject implicit in imperative OK, e.g. `Add X.`, `Refactor Y.`). Symbol-only fragments out: `⊥ skip flag` → `No skip flag.`
3. **No hidden copulas** — `is`/`are` elided only when the fragment intent is unambiguous. Drop the copula in `X — Y` form only when `Y` reads as predicate not apposition (apposition ambiguity slows the reader).
4. **No nested participial phrases** — at most one participial phrase per sentence. Nested form (e.g. `system, having validated the token after refreshing the session, returns ...`) prevents first-clause readability.

Verb-headed fragments fine. Lists > paragraphs. One idea per line in lists. Break long sentences before cutting words.

## SYMBOLS

Safe for GitHub readers:

```
→   leads to / becomes / produces
≥   at least
≤   at most
&   and
|   or (in lists, not prose)
§   spec citation (e.g. `§V.<n>`, `§T.<n>`) — only for refs into SPEC.md
```

Avoid — write the word instead; mirrors the `glyph` skill retired set:

```
⊥ ¬ ≠ ∈ ∉ ≡ ∴ ∀ ∃ ∧ ∨
```

## PRESERVE VERBATIM

not compress:

- Code blocks, snippets, backticked text.
- Paths: `src/auth/mw.go`.
- URLs and `#123` issue/PR refs.
- Identifiers: function names, var names, env vars, flags.
- Numbers, versions, dates, SHAs.
- Error message strings.
- SQL, regex, JSON, YAML.
- Quoted user-facing copy.
- `Resolves #N` / `Fixes #N` / `Closes #N` trailers — exact form.

## SHAPES

**Bullet > paragraph** when listing > 2 items.

**Definition list** for term/explanation pairs:

```
- `--dry-run` — print actions, do not execute.
- `--force` — skip confirmation prompts.
```

**Table** for comparing options on same axes:

```
| flag        | scope    | reversible |
|-------------|----------|------------|
| --soft      | local    | yes        |
| --hard      | working  | no         |
```

**Headers + fragments** > full sentences in issue/PR bodies:

```
## Summary
JWT replaces session cookies. Tokens expire 1h. Refresh via `/auth/refresh`.

## Changes
- Add JWT generation & validation
- New `/auth/refresh` endpoint
- Middleware validates `Authorization: Bearer <jwt>`

## Breaking
- Session cookies dropped. Clients must send `Authorization` header.
```

## EXAMPLES

Three pairs. every pair: **Good** passes SKIM TEST (first sentence or bullet states the fact); **Anti** fails on a named shape rule.

---

**Issue body**

Anti (44 words — fails rule 1: lead-first):

> When a user tries to log in with an email address that contains uppercase letters, the system fails to find their account because the lookup is being done in a case-sensitive manner, which is not the expected behavior for email addresses.

Skim failure: opening clause `When a user tries to log in...` not name the fact. The reader scans 14 words before reaching `fails to find their account`.

Good (15 words):

> Login fails when email has uppercase letters. Lookup is case-sensitive — should be case-insensitive for emails.

Skim pass: first sentence states the fact (login fails, under what condition). Second sentence states cause + fix direction.

---

**PR body**

Anti (fails SKIM TEST — filler precedes the fact):

> This pull request basically just adds some additional logging to the auth middleware so that we can debug issues more easily in production environments. It also includes a small refactor of the token validation logic.

Skim failure: 8 words of filler (`This pull request basically just adds some additional`) precede the fact. The takeaway sits past mid-sentence.

Good:

> ## Summary
>
> Add auth middleware logging for prod debugging. Refactor token validation.
>
> ## Changes
>
> - Log `userId`, `path`, `latency` on every authed request
> - Extract `validateToken()` from middleware into `auth/token.go`

Skim pass: first-sentence fragment states both items (logging + refactor). Each bullet opens with a verb (`Log`, `Extract`).

---

**Release commit body**

Anti (fails rule 4: nested participials; passive obscures the fact):

> ## Summary
>
> This change implements a new authentication system using JWT tokens which replaces the previous session-based authentication that was being used. Users will now be able to log in and receive a token that they can use to make authenticated requests, and these tokens will expire after a period of 24 hours.

Skim failure: 47 words before the fact `tokens expire after a period of 24 hours`. The two key facts (replacement, expiry) sit in tail clauses; nested relative clauses (`which replaces ... that was being used`) prevent first-clause readability.

Good:

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

Skim pass: first sentence is 4 words and states the replacement; second sentence is 3 words and states the constraint.

## BOUNDARIES

Steno register is literal phrasing w/ readable symbols (per SCOPE). Reviewers parse facts fast — idiom adds parsing cost and ambiguity. Within scope:

- not idiom (e.g. "moves the needle", "low-hanging fruit", "boil the ocean").
- not metaphor at the word level (e.g. "earns its keep", "bite", "smell").
- not colloquialism (e.g. "gotcha", "ish", "yeah", "kinda").
- not culture-loaded shorthand (sports, military, film references).

Exclusions (preserved verbatim):

- Colloquial sentence structure — allowed where it aids reviewer flow; register applies at the word level.
- Domain-load-bearing named ops (`backprop`, `glyph-encode`, `socratic`, `steno`).
- Established tech vocabulary that doubles as metaphor (`drift`, `bottleneck`, `leak`) — allowed when it is the standard term in context.

## WHEN SKIM TRIPS

Fact missing from the first sentence → rewrite the first clause to state it directly; not cut further words. Reviewer would slow down on a symbol → use the word. Compression preserves fact.
