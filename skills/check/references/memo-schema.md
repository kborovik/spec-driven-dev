# check references — memo schema

Conditional detail split from check SKILL.md per token-budget invariant (skill-body budget).
Telegraph register (SPEC-ADJACENT).
Read only when memo field shapes needed; SKILL.md MEMO § holds the read/write contract.

`.spec/check-state.json`, schema v3:

```json
{
  "schema_version": 3,
  "last_clean_sha": "<git HEAD @ last clean run>",
  "v_row_shas": { "V<n>": "<sha256 of §V row body>" },
  "last_run_at": "<ISO-8601 timestamp>",
  "last_v_classifications": { "V<n>": "HOLD|HOLD-SINCE-CLEAN|SCOPE-EMPTY|VIOLATE-CAPTURED|LATENT" },
  "oversized_cell_ack": "<sha256 over sorted oversized cell-id set>"
}
```
