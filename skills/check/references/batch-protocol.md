# check references — batch protocol + canonical agent prompt block

Conditional detail split from check SKILL.md per token-budget invariant (skill-body budget).
Telegraph register (SPEC-ADJACENT).
Read before spawning §V batches; loaded only when the audit's `batch|ADVISORY` row recommends > 1 agent.

## Batch protocol (parallel invariant audit)

Invariant audit MAY parallelize via Explore sub-agents:

1. **Batch count** = the audit's `batch|ADVISORY|recommended: <n> agents` row — script-computed from §V row count + PUBLISHED file census; formula owned by the script per mechanical-realization invariant, never re-derived here. `n` = 1 → main-thread single-agent path.
   Narrow-scope collapse (PUBLISHED census small vs §V count → fewer agents amortize cross-cutting greps better) folds into the row already, closing the eyeballed-file-count proxy class (§B.7).
2. **Partition** = contiguous V<n> spans per batch (cite locality → shared file reads).
3. **Prompt** = canonical block below, copied verbatim per batch, fill only `{...}` placeholders — no paraphrase, no per-call schema improvisation. `{V_SLICE}` + `{LINE_START}`/`{LINE_END}` filled from `emit-v-slices` output (batch = contiguous span; line bounds from the `## V<n> SPEC.md:<start>-<end>` headers), never re-Read SPEC.md.
   Single-agent path sources same slice in-thread.
4. **Aggregate** — main thread concatenates per-batch tables → REPORT invariant drift block.
5. **Failure** — agent error or timeout → re-run that range serially (strict fallback, not retry); other batch results retained.

Cite-DAG, format, history, pinned-header, mechanize-block, dispatch-target, grant-use stay w/ the script — never delegated to §V batches.

## Canonical agent prompt block

```
You are an invariants audit sub-agent. Read-only tools (Explore-class palette). No edits, no commits.

INPUT — SPEC.md invariants slice (lines {LINE_START}–{LINE_END}):

{V_SLICE}

INPUT — audit recipe (CHECK invariants step 5 behavioral-claim classification + judgment-class REPO-LOCAL extras from `.spec/check-extras.md`, verbatim):

{RECIPE_EXCERPT}

INPUT — scope sets (per scope-set invariant in SPEC.md):

PUBLISHED = {PUBLISHED_PATHS}
REPO-LOCAL = {REPO_LOCAL_PATHS}
SPEC-ADJACENT = {SPEC_ADJACENT_PATHS}
GITHUB-FACING = {GITHUB_FACING_PATHS}

OUTPUT — pipe-table only. Columns: `id|verdict|evidence`.

- `id` is invariant row identifier (`V<n>`).
- `verdict` in {HOLD, VIOLATE, VIOLATE-CAPTURED, UNVERIFIABLE, SCOPE-EMPTY, HOLD-SINCE-CLEAN, LATENT}.
- `evidence` ≤ 1 line, one of `file:line` or `no test covers …` or `scope-touch overlap empty` or `HOLD-since-clean @ <sha>` or `<file:line>; see §B.<n>` (VIOLATE-CAPTURED form) or `<trigger-condition-absent reason>` (LATENT form).

No prose preamble before the table. No trailing summary after the table. No commentary between rows. Pipe-table only — first line is header `id|verdict|evidence`, subsequent lines one row per assigned V<n>.
```

Block = single source of truth for sub-agent input + output shape; verbatim-copy contract closes the dispatcher-improvisation class.
