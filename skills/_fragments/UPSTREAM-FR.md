# UPSTREAM-FR — Claude Code product feedback (plugin-meta)

Load only when: (1) chosen §T goal matches `upstream FR` (case-insensitive), and (2) cwd is the plugin dev repo (origin URL resolves to manifest `.repository`).
Consumer repos never load this fragment.

Class = platform-limit product request (e.g. env no-expand in frontmatter), never a plugin-repo GitHub issue.

Ordered; stop on bail:

1. **DRAFT** — steno FR body: problem + ask + acceptance + context (plugin `.version`, `claude --version` when cheap).
   Preserve verbatim env names + grant patterns.
2. **PROBE** — channel reachable iff the agent tool palette exposes a feedback-submit tool (name contains `feedback`) or a documented CLI submit path is invocable from the recipe.
   Else channel = unavailable.
3. **GATE** — AskUserQuestion per decision-gate invariant.
   Header `Upstream FR`.
   Question surfaces one-line FR summary + `channel: reachable` or `channel: unavailable (paste fallback)`.
   Labels (mutually exclusive):
   - `Send` — only when channel reachable; recipe auto-submits DRAFT via the feedback tool/CLI.
   - `Already sent` — operator confirms prior submit; treat as pass (no re-send).
   - `I will paste /feedback` — channel unavailable path; recipe emits DRAFT as a paste block; wait for operator `sent` confirm before pass.
   - `Skip` — leave §T `.`, bail this task (continue next `.` row under `--all` if any).
4. **SEND** — `Send` + reachable → invoke feedback tool/CLI w/ DRAFT; exit 0 / success ack → pass.
   Non-zero / no ack → FAIL (code-bug class retry once; still failing → BACKPROP unspec edge: channel broken).
5. **FALLBACK** — `I will paste /feedback` → emit full DRAFT in a fenced block labeled for `/feedback`; no silent close.
   Operator confirms `sent` → pass.
   No confirm this turn → status stays `.`, next task under `--all` or stop.
6. **VERIFY** — pass criterion = FR submitted (`Send` success, or `Already sent`, or paste-path `sent` confirm).
   FR-only tasks list no code files; edit is no-op; flip + commit `SPEC.md` only.

Never file a plugin-repo GitHub issue for this class (monitor / github own those).
Never auto-send without GATE.
