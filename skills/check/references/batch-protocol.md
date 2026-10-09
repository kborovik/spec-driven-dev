# check references — batch protocol

Conditional detail split from check SKILL.md per token-budget invariant (skill-body budget).
Telegraph register (SPEC-ADJACENT).
Read before spawning §V batches; loaded only when the audit's `batch|ADVISORY` row recommends > 1 agent.

## Batch protocol (parallel invariant audit)

Invariant audit MAY parallelize via Explore sub-agents:

1. **Batch count** = the audit's `batch|ADVISORY|recommended: <n> agents` row — script-computed from §V row count + PUBLISHED file census; formula owned by the script per mechanical-realization invariant, never re-derived here. `n` = 1 → main-thread single-agent path.
   Narrow-scope collapse (PUBLISHED census small vs §V count → fewer agents amortize cross-cutting greps better) folds into the row already, closing the eyeballed-file-count proxy class (§B.7).
2. **Partition** = contiguous V<n> spans per batch (cite locality → shared file reads).
3. **Prompt** = `python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-mechanical.py emit-check-agent-prompt` output (single source = `skills/_fragments/CHECK-AGENT-PROMPT.md`), fill only `{...}` placeholders — no paraphrase, no per-call schema improvisation. `{V_SLICE}` + `{LINE_START}`/`{LINE_END}` filled from `emit-v-slices` output (batch = contiguous span; line bounds from the `## V<n> SPEC.md:<start>-<end>` headers), never re-Read SPEC.md.
   Single-agent path sources same slice in-thread.
4. **Aggregate** — main thread concatenates per-batch tables → REPORT invariant drift block.
5. **Failure** — agent error or timeout → re-run that range serially (strict fallback, not retry); other batch results retained.

Cite-DAG, format, history, pinned-header, mechanize-block, dispatch-target, grant-use stay w/ the script — never delegated to §V batches.
