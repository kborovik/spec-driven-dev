# SPEC-FORMAT — structural format every SPEC.md

LLM-facing format reference. Loaded by `/sdd:spec` and `/sdd:check` via direct read. Single source of truth every row shape, section catalog and order, header conventions. Section semantics and enforcement live in SPEC.md §V invariants — this file binds shape only.

## SECTION CATALOG + ORDER

every SPEC.md ! contain 6 sections in canonical order:

1. `## §G GOAL`
2. `## §C CONSTRAINTS`
3. `## §I INTERFACES`
4. `## §V INVARIANTS`
5. `## §T TASKS`
6. `## §B BUGS`

Empty section permitted (heading + pipe-table header row when applicable). not reorder, not omit, not rename. When `SPEC.archive.md` sibling exists, §T and §B sections additionally contain per-section archive marker H2 directly under section heading (see ARCHIVE SIBLING) — archive marker not counts as 7th section because marker form not matches catalog audit pattern.

## SECTION SEMANTICS

Per-section meaning and enforcement is SPEC.md §V invariant row defining the section. SPEC-FORMAT.md binds shape (row schema, header line, in-section ordering); §V binds semantics (what each row asserts, when /sdd:* skills mutate it).

## ENCODING REGISTER

SPEC.md and this file is LLM-facing so telegraph register per `skills/telegraph/SKILL.md`. SPEC-ADJACENT scope per scope-set invariant. Human-facing surfaces (README.md, user-facing docs) not in scope so steno per `skills/steno/SKILL.md`.

## ROW SCHEMAS

### §I row

One line, bullet optional. Opens `<kind>:` w/ kind in `[a-z_][a-z0-9_]*`:

```
- <kind>: <name> → <shape>
```

Row id is `I.<kind>` (e.g. `api:` row → `I.api`) — the form `§T.cites` references. One row per kind preferred; duplicate kinds dedup to one id addressing the set. Preamble prose w/o kind opener permitted, carries no id.

### §V row

One line. Opens `V<n>:` w/ monotonic `<n>` (per monotonic-numbering invariant).

```
V<n>: <subject> <relation> <condition>
```

Named form permitted (preferred for cross-skill-referenced rows): `V<n>: <name> — <body>` w/ short kebab-case `<name>` label. Free-text references cite `per <name> invariant` — grep-resolvable, no pinned digit, so PUBLISHED-safe per pinned-cite ban.

### §T row

Pipe-table under `## §T TASKS` heading. Header row exactly:

```
id|status|task|cites
```

Per-row columns:

- `id` is `T<n>` w/ monotonic `<n>`.
- `status` in {`.`, `x`}. `.` is pending, `x` is done.
- `task` is one-line goal in telegraph register. One-line is shape constraint; " not inlined history" semantic and enforcement defer to freshness-contract invariant per shape/semantics split.
- `cites` is comma-list of bare-form tokens in {`V<n>`, `T<n>`, `B<n>`, `I.<key>`} or sentinel `-` every no-deps. not range form (`V<a>..V<b>`), not whitespace inside list, not trailing comma.

### §B row

Pipe-table under `## §B BUGS` heading. Header row exactly:

```
id|date|cause|fix
```

Per-row columns:

- `id` is `B<n>` w/ monotonic `<n>`.
- `date` is ISO-8601 (`YYYY-MM-DD`).
- `cause` is one-line bug-class description in telegraph register. One-line is shape constraint; " not inlined history" semantic and enforcement defer to freshness-contract invariant per shape/semantics split.
- `fix` is comma-list of `V<n>` tokens or sentinel `-` every no-invariant-added. not range form, not whitespace inside list.

### Column extraction

`cites` in §T row and `fix` in §B row is last `|`-delimited segment (rightmost-`|` split); `id` is first `|`-delimited segment. Cells preceding the final delimiter preserve backtick-code `|` verbatim per telegraph verbatim-preservation rule so not `\|`-escape required inside `task` or `cause` body. Naïve all-`|` split (`awk -F'|'` or `IFS='|' read`) over-splits when body cells contain unescaped `|` (e.g. argument-hint `[§T.n|--next|--all]` in backtick code) so forbidden. The extraction rule is implemented once — see REFERENCE IMPLEMENTATION below; this file states the rule, not restates parser pseudo-code.

## CITATION FORMS

Bare-form (`V<n>`, `T<n>`, `B<n>`, `I.<key>`) valid only in SPEC.md typed columns (`§T.cites`, `§B.fix`) — column type unambiguously names target section so `§` prefix redundant.

Free-text contexts (SPEC.md §V/§C/§I/§G prose and REPO-LOCAL cites) ! use prefixed form: `§V.<n>`, `§T.<n>`, `§B.<n>`, `§I.<key>`.

Cite range form (`V<a>..V<b>`, `§V.<a>..§V.<b>`) not allowed every contexts — comma-list only. LLM-agent parses comma-list w/o expansion step so closes range-ambiguity recurrence class.

PUBLISHED scope per scope-set invariant not allows pinned numeric cites — placeholder form (`§V.<n>`, `§T.<n>`, `§B.<n>`) or inline rule embedding required.

Cite-DAG edge types per cite-resolution invariant: `§T.cites → §V`, `§B.fix → §V`, inline `§V.<n>` in §V/§C/§I body → §V (cross-ref). `/sdd:check` audits resolution + edge-type match; `/sdd:spec` mutation sweeps citers via edge-type traversal.

## HEADER LINES

- File opens w/ H1 title line (any text).
- Per-section H2 heading is `## §<S> <NAME>` exact form (e.g. `## §V INVARIANTS`).
- not H3+ subsections inside §-bodies (pipe-table or one-liner-per-row form per row schema).
- Exception: §T and §B sections MAY contain archive marker H2 directly under section heading per ARCHIVE SIBLING (sole permitted H2 inside §-body).

## ONE-FILE RULE

SPEC.md @ repo root is sole live spec file (per sole-source-of-truth invariant). not split, not docs/ tree, not JSON sidecars. Token-budget overflow → condense via archive sibling per token-budget condense mechanism (see ARCHIVE SIBLING) — archive is separate artifact carrying immutable historical rows, not split in canonical sense.

## ARCHIVE SIBLING

Optional `SPEC.archive.md` @ repo root is sibling file carrying verbatim archived §T and §B rows per token-budget condense mechanism and verbatim retired §V rows per reorganize archive-retired phase. Rows sorted by id ascending within each section/block. Sibling form not 7th section in SPEC.md — archive is separate artifact, not embedded.

### Archive marker

When `SPEC.archive.md` exists, SPEC.md §T and §B sections ! contain per-section archive marker H2 line directly under section heading:

```
## archived: §<S>.<a>..§<S>.<b> → SPEC.archive.md (<n> rows)
```

Where `<S>` in {`T`, `B`}, `<a>` is lowest archived id, `<b>` is highest archived id, `<n>` is row count.

When `SPEC.archive.md` contains `## §V.retired` block, SPEC.md §V section ! contain archive marker H2 line directly under section heading:

```
## archived: §V.retired → SPEC.archive.md (<n> retired rows)
```

Where `<n>` is retired row count. not id-range form because retired §V ids non-contiguous (carved by per-row retirement, not contiguous window split).

Section-catalog audit pattern `^## §[GCIVTB] ` not matches either archive marker form so marker not violates 6-section catalog invariant.

### Archive file shape

`SPEC.archive.md` opens w/ H1 title line + 2 sibling H2 sections (`## §T TASKS` and `## §B BUGS`) and optional `## §V.retired` block (sibling H2). Each §T and §B section contains pipe-table header row + archived rows verbatim per ROW SCHEMAS, sorted by id ascending. not §G / §C / §I content — archive scope is §T and §B and §V.retired only. Archived rows remain cite-DAG targets (resolution behavior governed by check skill).

### §V.retired block

`## §V.retired` H2 block contains verbatim retired §V rows produced by reorganize archive-retired phase. Per-row shape: leading `V<orig-n>:` prefix preserved (original id, not post-renumber); body opens `retired YYYY-MM-DD — ...` form verbatim per telegraph verbatim-preservation rule. Rows sorted by `<orig-n>` ascending. Archived §V rows not exists as live rows in SPEC.md §V section so historical-id resolution via renumber-map chain-walk per reorganize chain-walk semantics — chain landing on `archive` sentinel emits `archived → SPEC.archive.md ## §V.retired V<n>` and not resolves to live row.

## /sdd:check VALIDATION SURFACE

`/sdd:check` ! audit format-layer every run. Per-rule contract below; mechanical, not LLM-judgment. The rules are implemented once (see REFERENCE IMPLEMENTATION) — this file states each rule, the script executes it; not duplicate pseudo-code across the two surfaces:

- **section presence + order** — grep `^## §[GCIVTB] ` in SPEC.md → 6 hits in canonical order; missing or reordered → VIOLATE.
- **§T cites parse** — split `§T.<row>.cites` on `,` → every token match `^(V[0-9]+|T[0-9]+|B[0-9]+|I\.[a-z_]+|-)$`; not match → VIOLATE.
- **§B fix parse** — split `§B.<row>.fix` on `,` → every token match `^(V[0-9]+|-)$`; not match → VIOLATE.
- **§T status cell** — status ! in {`.`, `x`}; other → VIOLATE.
- **§B date cell** — date ! match ISO-8601 `YYYY-MM-DD`; other → VIOLATE.
- **monotonic ID** — extract `V<n>`/`T<n>`/`B<n>` row IDs in document order → every section IDs ! strictly increasing; gap ? allowed (closure history), reuse not allowed.
- **cite-DAG resolution** — per cite-resolution invariant: every bare-form cite in typed column ! resolve to existing SPEC.md row of expected edge type.
- **archive marker shape** — every archive marker line in SPEC.md §T or §B section ! match `^## archived: §[TB]\.[0-9]+\.\.§[TB]\.[0-9]+ → SPEC\.archive\.md \([0-9]+ rows\)$`; every archive marker line in SPEC.md §V section ! match `^## archived: §V\.retired → SPEC\.archive\.md \([0-9]+ retired rows\)$`; not match → VIOLATE.
- **archive sibling shape** — when `SPEC.archive.md` exists, file ! contain 2 sibling H2 sections (`## §T TASKS`, `## §B BUGS`) in canonical order w/ archived rows per ROW SCHEMAS; optional `## §V.retired` block (sibling H2) containing verbatim retired §V rows w/ `V<orig-n>:` prefix preserved and body opening `retired YYYY-MM-DD — ...` form; shape violations → VIOLATE.

Format violations emit VIOLATE per drift-verdict-vocab invariant w/ evidence prefix `format:` (e.g. `§T.<row> VIOLATE: format: cites token "V12..V15" not in comma-list grammar`). not new verdict — remedy identical to VIOLATE per vocab-add rule.

## REFERENCE IMPLEMENTATION

The parse rules above (column extraction, row schemas, citation forms, section catalog + order, archive-marker + archive-sibling shape, monotonic-ID, cite-DAG resolution) is deterministic so realized as plugin-internal mechanical tooling per the published-tooling carve-out: `scripts/check-mechanical.py` (run via `${CLAUDE_PLUGIN_ROOT}/scripts/check-mechanical.py`) is the single reference implementation. Contract lives here (one statement per rule); mechanism lives there (one implementation per rule). not duplicate parser pseudo-code across this file and the script and skill bodies — a rule restated as runnable code in two places is drift vector. Consumers re-implementing the audit in another runtime ! treat this file as the rule contract and the script as the canonical realization.
