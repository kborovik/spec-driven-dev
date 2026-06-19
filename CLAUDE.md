# CLAUDE.md

This file governs human-facing output in the sdd plugin repo: chat replies, the
README, GitHub issues and pull requests, and commit-message bodies. SPEC.md and
the skill bodies use the compressed telegraph register instead, so these rules
do not apply there.

This is a plain restatement of the human-clarity invariant in SPEC.md. SPEC.md
stays the source of truth. When that invariant changes, this file is updated in
the same commit.

<!-- sdd:direct-instruction:begin -->

## Clarity standard for human-facing output

Write so a reviewer reads each point once and moves on.

- **Main point first.** Open each paragraph or bullet with the fact. Put
  background and qualifiers after it.
- **One idea per sentence.** Keep sentences short. Break a long sentence before
  you cut words from it.
- **Plain words.** Use literal phrasing. Do not use idiom (for example
  `moves the needle`, `low-hanging fruit`), word-level metaphor (for example
  `earns its keep`, `bite`, `smell`), colloquialism (for example `gotcha`,
  `kinda`), culture-loaded shorthand (sports, military, film), or jargon-idiom
  (for example `load-bearing`, `by-construction`, `hand-rolled`, `clean-slate`,
  `prior-art`, `carry-cost`). Write the literal meaning instead.
- **Define or avoid jargon.** Spell out a technical term the first time you use
  it, or use a plain word. Established terms `drift`, `bottleneck`, and `leak`
  are fine as is.
- **Expand an acronym on first use.** Write the full term first, with the acronym
  in parentheses: spec-driven development (SDD). Common web and protocol acronyms
  (`API`, `URL`, `JSON`, `HTTP`, `JWT`) are exempt.
- **Spell out symbols.** Write `→` as "leads to" or "becomes", `≥` as "at least",
  `≤` as "at most", `&` as "and", and a leading `~` before a number as "about".
  Keep `|` for list and table separators, and keep `§` for spec citations. Any
  other math symbol becomes its word.
- **Put the citation at the tail.** End a sentence with the spec citation; never
  open or build the sentence on it. Write "Spell out symbols per the symbol-set
  invariant", not "The symbol-set invariant says to spell out symbols". The same
  rule covers issue and pull-request references such as `#123`.
- **When the operator asks you to decide,** state the choice in one sentence,
  list the options plainly with one line each, and recommend one option in one
  sentence. Do not end with a prose "or keep going?" question; a same-turn choice
  is a gate, not a sentence.

<!-- sdd:direct-instruction:end -->
