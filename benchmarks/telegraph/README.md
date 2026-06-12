# telegraph-bench — telegraph compression benchmark

Measures how many tokens the `telegraph` skill's encoding actually saves, by
decoding real `SPEC.md` rows back to prose and comparing token counts. This is
the evidence behind the README's headline claim that telegraph encoding cuts
tokens **~40% vs Claude prose for the same content**.

The benchmark lives next to the spec it measures on purpose: the corpus is this
repo's own `SPEC.md`, so the number tracks the actual artifact, not a synthetic
sample.

## TL;DR

Reference run (model `claude-opus-4-7`, n=30 rows, commit `26b5ef8`) — the same
corpus has also been run on `claude-opus-4-8` and `claude-sonnet-4-6`, see
[Cross-model](#cross-model):

| metric                                  | minimal decoder | canonical decoder |
| --------------------------------------- | --------------- | ----------------- |
| per-row reduction — **mean**            | **41.4%**       | 92.0%             |
| per-row reduction — median              | 38.9%           | 91.9%             |
| per-row reduction — p25 / p75           | 34.2% / 51.3%   | 91.3% / 92.5%     |
| token-weighted corpus reduction         | 45.0%           | 92.0%             |

The **minimal** decoder is the apples-to-apples figure — same content, just
decompressed — and is what backs the "~40%" claim. Inverted: prose costs about
**1.7x** the tokens of the telegraph form for the same facts (per-row mean;
1.8x token-weighted).

The **canonical** decoder is not a same-content comparison — see
[Two decoders](#two-decoders) below.

## What "reduction" means

For each spec row, `reduction = 1 - n_glyph / n_prose`, where:

- `n_glyph` — tokens in the telegraph-encoded row as it sits in `SPEC.md`.
- `n_prose` — tokens in the decoded prose.

A reduction of 0.41 means the telegraph row is 41% smaller than the prose that
carries the same content. Token counts come from the Anthropic
`/v1/messages/count_tokens` endpoint, so they are real model tokens, not a
character or word heuristic.

## Two decoders

Each row is decoded two ways, because "what prose costs" depends on who writes
the prose:

### `minimal` — naive expand-to-prose (the baseline)

System prompt: *"Expand to plain English. Preserve every fact. Output prose
only, no preamble."* Nothing else — no spec context, no cross-references. The
output is the same facts, written as full sentences instead of telegraph.

This is the honest, same-content comparison. It answers: *if you had written
this row as ordinary prose instead of telegraph, how many more tokens would it
cost?* Answer: **~41%** more compact in telegraph (per-row mean).

### `canonical` — the real `/sdd:explain` decoder

Feeds the **entire `SPEC.md`** plus `$ARGUMENTS: §<S>.<n>` through the actual
[`skills/explain/SKILL.md`](../../skills/explain/SKILL.md) as the system prompt
— the same skill an operator runs as `/sdd:explain §V.1`.

This is **not** a same-content comparison, and its ~92% reduction should not be
read as "telegraph saves 92%." `/sdd:explain` deliberately produces *more* than
the row: it pulls in cited siblings (the §V/§I a task cites, the §B bugs an
invariant guards), restates in full sentences, then appends `Bottom line`,
`Hint`, and `Next` blocks. The output is a reader-facing explainer, not a
1:1 decoding.

The canonical decoder earns its place as two things:

1. **A legibility check.** It runs the production decoder against every sampled
   row and confirms `/sdd:explain` returns sane, non-empty prose for all of
   them — a smoke test of the skill across the live corpus.
2. **An upper bound on read cost.** It quantifies how much a human pays, in
   tokens, to fully decompress a row with its cited context — the cost the
   telegraph form defers until someone actually asks for it.

## Corpus

The first 10 rows of each of `§V INVARIANTS`, `§T TASKS`, and `§B BUGS` in the
repo-root `SPEC.md` — **30 rows total**. `§G`/`§C`/`§I` are excluded: they're
prose-shaped sections, not the dense numbered rows telegraph targets.

Row extraction is regex-driven (`SECTION_BOUNDS` + `SECTION_ROW_RE` in the
script). If a section is missing or yields no rows, the script bails loudly
rather than silently shrinking the sample.

## Pipeline (per row)

```
n_glyph         = count_tokens(body)
prose_minimal   = decode(body, MINIMAL_SYSTEM)
prose_canonical = decode(<SPEC.md inline> + "§<S>.<n>", explain SKILL.md)
n_prose_{m,c}   = count_tokens(prose_{m,c})
reduction_{m,c} = 1 - n_glyph / n_prose_{m,c}
```

That's 5 API calls per row (1 count + 2 decode + 2 count) × 30 rows ≈ 150 calls
per run. Decodes use `max_tokens=8192`.

### Worked example — §V.1

Telegraph row as stored (91 tokens):

```
spec-adjacent-register — SPEC.md, `skills/**/SKILL.md`, SPEC-FORMAT.md, spec-referencing prose ! telegraph per telegraph skill; /sdd:explain decodes on demand.
```

`minimal` decode (226 tokens, reduction **0.5973**) opens:

> The skill named "spec-adjacent-register" applies to several categories of
> documents and content: the SPEC.md file, every SKILL.md file located anywhere
> within the skills directory tree, the SPEC-FORMAT.md file, and any prose that
> references specifications…

`canonical` decode (977 tokens, reduction **0.9069**) opens with the citation
header, restates in prose, then adds cited siblings and `Bottom line`/`Next`
scaffolding — far more than the row alone, which is why its reduction reads so
high.

## Results

Reference run (`claude-opus-4-7`) — per row:

| id  | sec | n_glyph | n_prose_min | red_min | n_prose_can | red_can |
| --- | --- | ------- | ----------- | ------- | ----------- | ------- |
| V1  | V   |      91 |         226 | +0.5973 |         977 | +0.9069 |
| V2  | V   |      66 |         166 | +0.6024 |         862 | +0.9234 |
| V3  | V   |      98 |         178 | +0.4494 |         978 | +0.8998 |
| V4  | V   |      66 |         117 | +0.4359 |         962 | +0.9314 |
| V10 | V   |      76 |         115 | +0.3391 |         868 | +0.9124 |
| V11 | V   |      71 |         121 | +0.4132 |         755 | +0.9060 |
| V12 | V   |      79 |         180 | +0.5611 |         982 | +0.9196 |
| V13 | V   |      97 |         148 | +0.3446 |         967 | +0.8997 |
| V14 | V   |      98 |         107 | +0.0841 |        1228 | +0.9202 |
| V15 | V   |      86 |         280 | +0.6929 |        1126 | +0.9236 |
| T1  | T   |      45 |         149 | +0.6980 |         799 | +0.9437 |
| T2  | T   |      43 |          52 | +0.1731 |         458 | +0.9061 |
| T3  | T   |     100 |         156 | +0.3590 |         998 | +0.8998 |
| T4  | T   |      85 |         212 | +0.5991 |        1031 | +0.9176 |
| T5  | T   |     117 |         154 | +0.2403 |        1233 | +0.9051 |
| T6  | T   |      70 |         118 | +0.4068 |         821 | +0.9147 |
| T7  | T   |      79 |         131 | +0.3969 |         926 | +0.9147 |
| T8  | T   |      54 |          72 | +0.2500 |        1027 | +0.9474 |
| T9  | T   |      78 |         123 | +0.3659 |        1038 | +0.9249 |
| T10 | T   |      58 |         150 | +0.6133 |         931 | +0.9377 |
| B1  | B   |      65 |         105 | +0.3810 |         751 | +0.9134 |
| B2  | B   |      56 |          85 | +0.3412 |         644 | +0.9130 |
| B3  | B   |      64 |         127 | +0.4961 |         749 | +0.9146 |
| B4  | B   |      53 |         103 | +0.4854 |         675 | +0.9215 |
| B5  | B   |      51 |         106 | +0.5189 |         627 | +0.9187 |
| B6  | B   |      84 |         134 | +0.3731 |        1128 | +0.9255 |
| B7  | B   |      62 |          84 | +0.2619 |         885 | +0.9299 |
| B8  | B   |      71 |         110 | +0.3545 |        1080 | +0.9343 |
| B9  | B   |      55 |          69 | +0.2029 |         924 | +0.9405 |
| B10 | B   |     111 |         178 | +0.3764 |        1360 | +0.9184 |

Summary (per-section × decoder + grand total):

| section | decoder   | mean    | median  | p25     | p75     | n  |
| ------- | --------- | ------- | ------- | ------- | ------- | -- |
| V       | minimal   | +0.4520 | +0.4426 | +0.3618 | +0.5883 | 10 |
| V       | canonical | +0.9143 | +0.9160 | +0.9062 | +0.9226 | 10 |
| T       | minimal   | +0.4102 | +0.3814 | +0.2772 | +0.5510 | 10 |
| T       | canonical | +0.9212 | +0.9162 | +0.9083 | +0.9345 | 10 |
| B       | minimal   | +0.3791 | +0.3748 | +0.3445 | +0.4593 | 10 |
| B       | canonical | +0.9230 | +0.9201 | +0.9155 | +0.9288 | 10 |
| all     | minimal   | +0.4138 | +0.3890 | +0.3421 | +0.5132 | 30 |
| all     | canonical | +0.9195 | +0.9185 | +0.9125 | +0.9254 | 30 |

### Reading the spread

- **`§V` compresses best** (mean 45%). Invariants are the densest rows —
  symbol-heavy, every word load-bearing — so prose has the most to add back.
- **`§B` compresses least** (mean 38%). Bug rows are already short and contain
  more verbatim-preserved content (dates, identifiers, error fragments) that
  telegraph can't touch.
- **The low outlier, V14 (+0.08)**, is a row that was already near-prose with
  little to drop — telegraph wins least where the source isn't compressible.
  The high outlier, T1 (+0.70), is a terse task line that prose has to unpack
  heavily.

## Cross-model

The same 30-row corpus was run through three models. Grand totals (all sections,
n=30 each):

| model               | minimal mean | minimal median | canonical mean | canonical median | Σ glyph | Σ prose_min |
| ------------------- | ------------ | -------------- | -------------- | ---------------- | ------- | ----------- |
| `claude-opus-4-7`   | +0.4138      | +0.3890        | +0.9195        | +0.9185          | 2229    | 4056        |
| `claude-opus-4-8`   | +0.4172      | +0.4094        | +0.9107        | +0.9112          | 2069    | 3672        |
| `claude-sonnet-4-6` | +0.7303      | +0.7650        | +0.9375        | +0.9402          | 1537    | 20201       |

Two things to read off this table.

### The `canonical` decoder is model-stable; the `minimal` decoder is not

Canonical reduction lands in a tight band — **0.911 / 0.920 / 0.938** — across all
three models. That's the headline robustness result: when the decoder is handed
the **full `SPEC.md` as context** (the production `/sdd:explain` path), the
measured expansion barely moves with the model, because the model is grounding
its prose in the spec rather than guessing.

Minimal reduction does *not* hold steady: Opus 4.7 and 4.8 agree closely (0.41
each), but Sonnet jumps to 0.73. **That jump is a decoder artifact, not a real
compression gain** — see below. It is exactly the
[decoder-dependence caveat](#caveats) in the extreme.

### Why Sonnet's `minimal` number is an artifact

The `minimal` decoder gives the model a single terse row and no context. Opus
expands it tersely and faithfully. **Sonnet balloons — and on some rows,
confabulates.** The `Σ prose_min` column is the tell: Opus expanded all 30 rows
to ~3.7–4.1k prose tokens total; **Sonnet produced 20,201** — roughly 5× — and
14 of the 30 rows blew past 400 prose tokens (vs a typical Opus row of ~120).

The clearest case is **§V.2**. The row defines the github-facing writing
register:

```
github-facing-register — README, issues, PRs, commit-msg bodies ! steno per steno skill; commit subjects = per-skill fixed templates, verbatim.
```

With no context, Sonnet misread "steno" as **stenography** and emitted a
**15,349-character fictional README about learning shorthand skills one at a
time** — 3753 prose tokens, reduction +0.988. The reduction looks enormous only
because the denominator hallucinated. It measures Sonnet's verbosity, not the
telegraph encoding.

### Takeaways

- **Headline stays on Opus `minimal` (~40%)** — the honest, same-content
  baseline. Opus 4.7 → 4.8 confirms it is stable across the model bump.
- **`canonical` is the model-robust cross-model measure** (~0.91–0.94 for every
  model tested). When you need one number that doesn't depend on decoder
  temperament, this is it.
- **Do not quote Sonnet's `minimal` 0.73 as a compression figure.** It reflects a
  context-free decoder over-expanding (and on terse rows, hallucinating), which
  is the opposite of what the benchmark is trying to isolate. The record is kept
  in the results JSON for transparency, flagged here.
- **Token counts are tokenizer-specific.** `Σ glyph` for the identical 30 rows is
  2229 / 2069 / 1537 across the three models — Opus and Sonnet tokenize the same
  bytes differently, so absolute counts are only comparable *within* a model.

## Reproduce

```bash
# from repo root
uv run benchmarks/telegraph/telegraph-bench.py
# or, executable directly (PEP 723 self-bootstraps Python via uv)
./benchmarks/telegraph/telegraph-bench.py
```

Requires:

- [`uv`](https://docs.astral.sh/uv/) — the script's PEP 723 header pins
  `requires-python >=3.11` and zero dependencies; `uv` bootstraps the
  interpreter. No virtualenv to manage.
- An Anthropic API key in `$ANTHROPIC_API_KEY`, or a `~/.anthropic-api-key`
  file. The script bails if neither is present.

A run reads the live `SPEC.md`, so re-running after the spec changes re-measures
against the current rows — the number stays honest as the spec evolves.

## Results file & trend tracking

Every run appends one record to
[`telegraph-bench-results.json`](telegraph-bench-results.json) (tracked in git).
Each record carries:

```jsonc
{
  "timestamp":  "2026-06-12T03:08:31Z",
  "commit_sha": "<HEAD at run time>",
  "model":      "claude-opus-4-7",
  "per_sample": [ { "id", "section", "body",
                    "n_glyph",
                    "prose_minimal",   "n_prose_minimal",   "reduction_minimal",
                    "prose_canonical", "n_prose_canonical", "reduction_canonical" }, … ],
  "summary":    { "<section>": { "<decoder>": { "mean", "median", "p25", "p75", "n" } } }
}
```

On each run the script prints a **stats-over-time** block: Δmean / Δmedian / Δn
vs the last compatible record, the last-5 mean trend per decoder, and the
commit shift. Records whose schema predates the two-decoder format are skipped
with a one-line note rather than crashing the trend — so the history survives
format changes.

> Note on the `n_glyph` column name: "glyph" refers to the low-token symbol set
> (`→ ≥ ≤ § …`) telegraph uses — it names the *encoded quantity*, not the
> benchmark. The benchmark itself is `telegraph-bench`. The column name is kept
> stable so the schema check and historical records stay valid.

## Caveats

- **Decoder-dependent.** "Reduction vs prose" is only as meaningful as the prose
  you compare against. The `minimal` decoder is a deliberately plain,
  fact-preserving expansion; a chattier or terser writer would move the number.
  We report `minimal` as the headline precisely because it's the least
  flattering, most defensible baseline. [Cross-model](#cross-model) shows how far
  this can swing — Sonnet's context-free `minimal` decode balloons ~5× and drags
  its reduction to an artifactual 0.73.
- **Model-pinned.** Token counts and decodings come from the run's model (default
  `claude-opus-4-7`, overridable via `$BENCH_MODEL`). A different model shifts
  both the counts and the prose length; tokenizers differ, so absolute counts are
  only comparable within a model. The model id is recorded in every result record.
  The `canonical` decoder proves the most model-robust — see [Cross-model](#cross-model).
- **Sample = 30 rows** from one repo's spec. It measures *this* spec's
  compressibility, which is the point — it is not a universal constant for all
  telegraph text.
