---
name: glyph
description: |
  Math-glyph encoding — LLM-facing compression for SPEC.md and spec-adjacent
  writes. Loaded by /sdd:spec, /sdd:build, /sdd:check. Triggers on any
  write to SPEC.md or user says "math-glyph", "glyph", "compress this",
  "be brief".
allowed-tools: [Skill]
disable-model-invocation: true
---

# glyph — LLM-facing math-glyph encoding

Audience: the LLM re-reading SPEC.md into context. SPEC.md is LLM-facing — Claude does every read/write; humans operate via /sdd:* cmds, and /sdd:explain decodes glyph → prose. Compression comes from terse grammar — dropped articles/aux/filler, fragments, unpadded pipe tables — cutting tokens on every re-load. Symbol set is curated for parse clarity, not token savings: heavy math operators cost 2–4 tokens vs a 1-token word, so a glyph stays only where it reads clearer than the word.

"Math-glyph" is not "glyph". Generic glyphs are any printable symbol (status markers `.` `x`, bullets); math-glyphs are math operators. This skill keeps a curated low-token subset (→ ≥ ≤ ! ? § |) and retires heavy multi-token operators to ASCII words (see SYMBOLS). Glyph vs steno split is grammar aggression, not symbol set: glyph drops articles/aux/filler and runs in fragments; steno keeps grammar intact for GitHub reviewers.

Applies to SPEC.md writes, spec-referencing prose, backprop entries.
Does NOT apply to code, error strings, commit messages, PR descriptions, or anything a human reviewer reads on GitHub (use the `core:steno` skill for that).

## GRAMMAR

- Drop articles (a, an, the).
- Drop filler (just, really, basically, simply, actually).
- Drop aux verbs where fragment works (is, are, was, were, being).
- Drop pleasantries.
- No hedging (skip "might", "perhaps", "could be worth").
- Fragments fine.
- Short synonyms per `## VERBS` (canonical verbs + `avoid` column).
- Pipe tables compact: not alignment padding, not separator row. Header row + data rows, bare `|cell|cell|` (escape literal `|` as `\|`).

## SYMBOLS

Keep set — low-token and parse-clear, prefer over the word:

```
→   leads to / becomes / on <x>
≥   at least
≤   at most
!   must / required
?   may / optional / unknown
§   section reference
|   pipe-table delimiter (no semantic meaning)
```

Retired set — heavy multi-token operators (2–4 tokens each, measured). Write the ASCII word; sweep tasks swap surviving prose occurrences:

```
⊥ ¬ ≠ ∈ ∉ ≡ ∴ ∀ ∃ ∧ ∨
```

Retired for token cost, not banned for meaning — /sdd:explain still decodes legacy occurrences; all read as standard math except `⊥`, which reads no / not / never / nil by context. For "or" write `or` — never `∨`, never bare `|` (table delimiter only).

## VERBS

Canonical action-verb vocab every math-glyph artifacts. Use canonical form; not use synonyms in `avoid` column. Exclusions same as SYMBOLS — backticks, verbatim trigger phrases, domain-load-bearing named ops (e.g. `backprop`, `glyph-encode`).

**Write / edit ops**

|canonical|meaning|avoid|
|`add`|place new entity inside existing container|introduce, insert|
|`init`|bring new container into existence (file, §)|create, generate, scaffold|
|`drop`|remove entity|remove, delete, erase|
|`swap`|exchange one for another, in place|replace, substitute, switch|
|`fix`|repair broken behavior|implement (when fixing), correct|
|`patch`|targeted change to existing entity|mutate, modify, change, alter, update|
|`sweep`|apply same edit every matching sites|refactor (when mechanical)|
|`sync`|reconcile two surfaces back to agreement|update (when reconciling)|
|`append`|add at end of ordered seq (log, table, list)|push, attach|
|`strip`|drop substructure (prefix, whitespace, tokens)|trim, clean|
|`extend`|enlarge existing structure (additive change)|expand, augment, grow|
|`tighten`|sharpen wording, scope unchanged|refine, improve, polish|

**Read / check ops**

|canonical|meaning|avoid|
|`read`|load file/section into context|inspect, view, examine, look at|
|`cite`|reference §V/§I/§T row|reference, mention, point to|
|`grep`|scan text for pattern, return matches|search, scan (when pattern-match)|
|`diff`|compare two surfaces, return delta|compare (when surface-vs-surface)|
|`audit`|systematic rule-check, return pass/fail|review, verify (when ruleful)|
|`parse`|structured read of formal input|interpret, decode|
|`trace`|follow chain (cause→effect, caller→callee)|track, follow|

**Runtime ops**

|canonical|meaning|avoid|
|`run`|execute cmd / skill / task|execute, invoke, trigger (when running), tackle (when applied to task)|
|`retry`|re-run after failure|redo, reattempt|
|`bail`|exit early w/ nothing done|abort, halt, quit, give up|
|`fire`|dispatch event / hook|trigger (when dispatching), send|
|`emit`|produce output (stdout, file, channel)|output, print, write (when emitting)|
|`render`|format for display (table, prose, diagram)|format, display, show, generate|
|`ask`|prompt user for input / decision|prompt, query, request|

**State ops**

|canonical|meaning|avoid|
|`set`|assign value to a field|assign, configure|
|`mark`|transition state field to known value (`mark T<n> x`)|tag (when stateful), flag|
|`flag`|raise attention / categorize as violation|warn, alert, note|
|`open`|create new tracked entity w/ initial status|start, begin, file (when opening)|
|`close`|transition entity to terminal state|finish, complete, resolve|

Domain-load-bearing verbs override (`backprop` as bug-protocol noun, `glyph-encode` as named encoding op). Canonical form distorts domain semantic → keep domain verb. Verb canonicalization is compression every LLM reader, not paraphrase.

## NOUNS

Canonical noun vocab every math-glyph artifacts. Use canonical form; not use synonyms in `avoid` column. Same exclusions as SYMBOLS and VERBS — backticks, verbatim trigger phrases, domain-load-bearing named ops (e.g. `backprop`, `glyph-encode`, `socratic`, `steno`).

|canonical|meaning|avoid|
|`exclusion`|permitted divergence from default rule; named exception|carve-out, exemption, escape hatch|
|`require` (modal `!`)|obligation; mandate|earn (when subject not animate)|
|`record` or `ledger`|persisted bug-class store|memory (when used metaphorically for §B)|

Extend as new pairs surface — idioms and metaphors caught by sweep tasks land as noun rows here so future writes default to canonical form.

## PRESERVE VERBATIM

Never compress:

- Code blocks, snippets, one-liners with backticks.
- Paths: `src/auth/mw.go`.
- URLs.
- Identifiers: function names, variable names, env vars.
- Numbers and versions.
- Error message strings.
- SQL, regex, JSON, YAML.
- Quoted strings.

## SHAPES

**Invariant**:

```
V<n>: <subject> <relation> <condition>
V<n>: every req → auth check before handler
V<n>: token expiry ≤ current_time → reject
```

**Bug row** (pipe table under §B):

```
id|date|cause|fix
B<n>|2026-04-20|token `<` not `≤`|V<n>
```

**Task row** (pipe table under §T):

```
id|status|task|cites
T<n>|x|add auth mw|V<n>,I.api
```

Status: `x` done, `.` todo. Escape literal `|` as `\|`.

**Interface**:

```
<kind>: <name> → <shape>
api: POST /x → 200 {id:string}
cmd: `foo bar <arg>` → stdout JSON
env: FOO_KEY ! set
```

## ADDRESSING

`§<S>.<n>` is section.item ref (e.g. `§V.<n>` is invariants §, item n). Cmd args, commits, PRs cite by § → zero ambiguity.

## ONE FILE RULE

Big project → more §s, not more files. grep ceremony kills agent speed. SPEC.md > 500 lines → compact §B (drop oldest bugs) before split.

## EXAMPLES

**Bad**:

> The system should ensure that every incoming request is properly authenticated before being forwarded to its corresponding handler function.

**Good**:

> V<n>: every req → auth check before handler

**Bad**:

> We discovered that the token expiration check in the middleware was using a strict less-than comparison operator, which meant tokens were being rejected at the exact moment of their expiry.

**Good**:

> B<n>: token `<` not `≤` → reject @ expiry boundary.

**Bad**:

> The POST endpoint at /x accepts a JSON body and returns a 200 response with an object containing the created id.

**Good**:

> api: POST /x → 200 {id}

## BOUNDARIES

- User asks for prose explanation → switch to normal English.
- Spec documents for external review (RFC, pitch) → normal English.
- Commit message → normal English (git readers expect it).
- Diff comment in code → normal English.

## WHEN UNSURE

If cutting a word loses a fact, keep it. Math-glyph encoding is compression, not amputation.
