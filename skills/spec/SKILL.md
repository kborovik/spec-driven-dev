---
name: spec
description: |
  Sole semantic author of SPEC.md @ repo root — create, amend, fold designs,
  or backprop bugs (§T status-flip → build, archive → condense, §V renumber →
  reorganize; those carve-outs not authoring paths).
  Triggers when user asks to write spec, start new spec, distill spec from
  code, add invariants, amend a section, or record a bug. Common phrasings:
  "write the spec for...", "new spec", "distill spec from code",
  "spec this idea", "import existing repo", "pull invariants out of code",
  "this bug keeps biting", "post-mortem on Y".
allowed-tools: AskUserQuestion, Read, Edit, Write, Grep, Bash(git *), Bash(grep *), Agent, Skill
model: fable
---

# spec — spec mutator

`telegraph` skill applies to all writes here.

## DISPATCH

**Step 0 (precondition):** porcelain state injected below (`!` preprocessing; `disableSkillShellExecution` consumers see a disabled-by-policy marker → run `git status --porcelain SPEC.md` manually):

!`git status --porcelain SPEC.md`

Empty output → continue; else bail w/ "SPEC.md has uncommitted changes; commit or stash first" (auto-commit assumes clean baseline; porcelain catches staged + untracked, which `git diff --quiet` misses).

**Step 1 (fold-in shortcut):** `$ARGUMENTS` matches `designs/*.md`, file exists, SPEC.md exists @ repo root → FOLD-IN (skip socratic gate — design skill Open-Questions-empty rule already enforced convergence pre-persist).
Design path w/o SPEC.md → bail w/ "fold-in needs SPEC.md; init via NEW or DISTILL first" (design skill degrades gracefully sans SPEC.md so converged drafts can predate it).
Else → gate.

Engage `sdd:socratic` gate w/ `$ARGUMENTS` as intent.
Single-question loop until convergence triple matches one mode:

- **NEW** — goal + first-principle-asked + (≥ 1 invariant or ≥ 1 task)
- **DISTILL** — explicit "build from code" intent (gate exits ≤ 1 turn — walks repo, no interrogation)
- **BACKPROP** — symptom + surface + recurrence-class
- **AMEND** — §-target + delta

SPEC.md presence is the only branch (mode is gate byproduct, not user-typed prefix):

1. no SPEC.md @ repo root → gate restricted to {NEW, DISTILL}.
2. SPEC.md exists → gate ranges over {BACKPROP, AMEND, NEW}; NEW rare → require explicit re-init confirmation before overwrite.

Post-convergence → run mode procedure below.
Concrete first-turn input → gate passes ≤ 1 turn (zero-friction); vague → dialogue until convergence.
No skip flag, no prefix back-doors.

## NEW — idea → spec

Input: user idea.

1. Goal (1 line, telegraph) → §G.
2. Constraints stated or implied → §C.
3. External surfaces named → §I.
4. Initial invariants → §V (numbered V<n>).
   Gate probes first-principle (foundational claim); user may decline → converge on derived invariants only.
   Late first-principle → AMEND §V (only late-entry path, not second authoring path).
5. Goal → ordered tasks → §T pipe table, all status `.`, ids T<n>.
6. §B header row only (`id|date|cause|fix`).

→ APPLY.

## DISTILL — code → spec

Walk repo.
Produce §G (infer from README/package.json/main entry), §C (infer from stack), §I (enumerate public APIs/CLIs/configs), §V (derive from tests + assertions), §T (one task per known TODO or missing test), §B (empty).
Flag uncertain items w/ `?` so user can confirm.

→ APPLY.

## BACKPROP — bug → §B + §V

Input: gate triple (symptom + surface + recurrence-class).

1. Parse bug.
2. Find root cause (read code).
3. New invariant would catch recurrence? yes → draft `V<next>`.
4. Append §B row `B<next>|<date>|<cause>|<fix>` — fix cell `V<N>` when step 3 drafted, else `-` (per SPEC-FORMAT §B fix grammar).
5. Drafted → append invariant to §V.
6. Fix changes behavior → add/patch §T rows.

→ APPLY.

Rule: every bug → §B entry.
Invariant optional but preferred.

## AMEND — targeted edit

Input: gate §-target + delta.

**Resolve body file** (§V target — condense relocates heavy §V bodies, SPEC.md row left a stub): read the target's SPEC.md §V row.
Row body redirects to `.spec/check-extras.md §V<n>` (condense prong-6 stub) → live body lives there under `## §V<n>` header; body file = `.spec/check-extras.md` (multi-target AMEND → one resolved body file per §V target, stub-redirected rows collapse to the same file).
Else inline-body row → body file = SPEC.md. §B/§G/§C/§I/§T targets always SPEC.md.
Resolved body file feeds APPLY step 4 write + commit path-scope per extras-hook invariant.

Read target § from its resolved body file.
Show current in steno per steno skill if target in {§V, §B} (audience: user reviewing proposal); telegraph otherwise.
Ask user what changes.

→ APPLY.

Never silently rewrite §s user did not name.

## FOLD-IN — design draft → §V or §T amend

Input: `designs/<slug>.md` (converged per design skill Open-Questions-empty rule).

No socratic gate — design skill enforced convergence pre-persist so /sdd:spec trusts content.
Multi-target: one design may propose new §V row(s), §T row(s), §I edit(s), §B row(s) in one apply.

1. Read draft; parse proposed amendments.
2. Draft each in telegraph (target §s + delta text).

→ APPLY.

Rule: fold-in mutates SPEC.md only; design file persists in working tree post-apply (no `git rm`, `git add`, or `rm`) per design-file lifecycle invariant — APPLY write step SPEC.md-only so structurally enforced.
User removes or preserves manually.
Provenance: slug in SPEC.md commit msg + git history.

## APPLY (all modes, post-delta)

Five steps in order; audits fire on condition, not mode authorship.
All audits run pre-show-user, mechanical pattern-match not LLM-judgment per mechanical-not-LLM-judgment invariant.

**Step 0 — write-time prune** (delta-rewrite stage, ordered ahead of audit table so every audit sees final-form delta):

- delta patches pre-existing §V row → §V-row residue prune per `references/write-time-prune.md` (Read on match — pattern set + pre-filters live there).
- delta adds or rewrites §B `cause` cell → one-line trim per same file.
- pruned content → commit-msg body (step 4); step 3 shows post-prune form.

**Step 1 — audit table** (on-fail column names owning sub-recipe — bail strings + grep sub-recipe detail live in `references/audit-recipes.md`, Read @ first fire):

```
audit | fires when delta is | on fail
sweep-scope | contains sweep-§T row (§V-violation remediation) | bail → SWEEP-§T SCOPE AUDIT
pinned-cite | touches PUBLISHED (a) or SPEC.md narrative (b) | bail → PINNED-CITE AUDIT, matching sub-recipe
next-block  | touches user-typeable SKILL.md | bail → NEXT-BLOCK-SECTION AUDIT
fold-first  | adds §V row to pre-existing §V section, mode not FOLD-IN | AskUserQuestion gate → FOLD-FIRST AUDIT
```

pinned-cite (a) + next-block rows structurally no-op while step 4 writes SPEC.md only — retained defensive (fire only if future mode widens write set).

Table uses named-invariant + placeholder cite form only (`per <named> invariant`, `§V.<n>`) — `skills/**` in PUBLISHED where pinned §-digit cites banned per sub-recipe (a); body pinned-cite count is 0, stays 0.

**Step 2 — render-split**: §V + §B content rows → steno per steno skill (audience: user reviewing proposal); all else → telegraph (§T/§I pipe forms already legible, §G/§C targets, header-only §B row).

**Step 3 — show-user**: render diff preview; await user OK.

**Step 4 — write + commit**: on OK → write delta to its resolved body file(s) (telegraph) + auto-commit path-scoped `git commit -m <subject> [-m <body>] -- <body-file(s)>` (write-ownership invariant — scopes to the owned file set, pre-staged files never leak).
Body file(s) = SPEC.md every mode + target, except a stub-redirected §V AMEND → `.spec/check-extras.md` per AMEND § resolution + extras-hook invariant (the SPEC.md stub row stays untouched, so check-extras.md is the sole path-scope; mixed delta touching both an inline §V/other § and a stub-redirected §V → path list = the union). `-m` flags ! precede `--` — message tokens after `--` parse as pathspecs, commit fails; no commit prompt (uniform every mode).
Msg per mode:

```
NEW      → init SPEC.md (V<1>..V<n>, T<1>..T<m>)
DISTILL  → init SPEC.md from code
BACKPROP → backprop §B.<n>(+) + §V.<N>(+): <one-line cause>   (trimmed forensics → msg body, from step 0)
AMEND    → amend §<S>.<n>(+): <one-line>                       (pruned history → msg body, from step 0)
FOLD-IN  → fold-in §V.<n>(+) and §T.<n>(+): <slug>            (omit absent §s)
```

**Re-entry**: any stage rewriting delta after step 0 — concretely fold-first's fold-into reroute (new §V row → existing-row amend) — re-enters APPLY @ step 0; rewritten delta newly satisfies §V-row prune and prior audits saw a delta that no longer exists.

APPLY ends @ commit. `## POST-APPLY` fires after, unchanged.

## AUDIT SUB-RECIPES + PRUNE PATTERNS — references/

Conditional detail one level deep per token-budget invariant (skill-body budget); Read each file only @ its load moment:

- `references/audit-recipes.md` — SWEEP-§T SCOPE (grep-pattern scope rule), PINNED-CITE (grep sub-recipes a/b + `grep -v -E` pre-filter), NEXT-BLOCK-SECTION (frontmatter Grep + heading probe), FOLD-FIRST (AskUserQuestion gate + re-entry) — full bodies + bail strings; Read @ first audit fire per APPLY step 1.
- `references/write-time-prune.md` — §V-row residue prune pattern set + pre-filters, §B cause trim rule; Read @ APPLY step 0 on match.

## POST-APPLY

Every mode post-commit ! surface `/sdd:check` as Next-block item #1 per §V.<n>; operator dispatches next turn → cascade scan over just-applied delta.
Not silent commit-then-done.
Recipe ends @ commit — slash-cmd dispatch is operator turn only.

Catches class where SPEC.md amend invalidates derivative content in `<plugin>/**` (skills, commands, READMEs) w/o manual audit.
Next-block surfacing is baseline — operator dispatch is only path to `/sdd:check`.

## OUTPUT RULES

Defer to `${CLAUDE_PLUGIN_ROOT}/SPEC-FORMAT.md` — row shape, section catalog, citation forms, header conventions.

## MECHANIZE — script-candidate scan

Recipe end → before the `## Next` block, scan this run for a mechanization candidate.
Candidate = any of:

- ≥ 2 same-shape deterministic calls this run (identical command modulo args)
- LLM-side join / sort / count / dedup over script-emittable data
- multi-step parse collapsible to one script emit mode
- fresh regex paraphrase of an existing mechanical rule (mechanical-realization invariant class)

Hit → emit exactly one `## Next` item naming the observed pattern + proposed script mode; none → no item.
Never self-implement the mechanization mid-run (recipe-step-no-dispatch + write-ownership invariants).
Route by cwd:

- dev repo (this plugin) → /sdd:spec → new §T row
- consumer repo, plugin-target → monitor dispatched `mechanization-candidate` path (monitor-protocol invariant)
- consumer repo-local → consumer /sdd:spec → `.spec/check-extras` row

## OUTPUT — "Next" block

Heading `## Next`; 1–5 atomic items (one sentence each, no `Reply` prefix); positional dispatch (`run <int>` or `run /<plugin>:<cmd> [args]`).
Optional `## Hint` (≤ 3 lines) precedes when item selection needs hidden state.
Two output moments, distinct item leads: show-user turn (diff pending) → apply + revise lead; post-commit turn → `/sdd:check` item #1 every mode per POST-APPLY, then `/sdd:build §T.n` when pending §T row exists.

Example @ show-user, diff pending (Hint skipped — items self-explanatory):

```
## Next

1. apply the diff to `SPEC.md`
2. /sdd:spec rework the V<N> invariant before building
```

Example post-commit, any mode (`/sdd:check` leads per POST-APPLY):

```
## Next

1. /sdd:check — cascade scan over the just-applied delta
2. /sdd:build T<n> — start the next pending task
```

## NON-GOALS

- Writes serialize on main thread; reads delegable to sub-agents — SPEC.md draft + apply + commit stays main-thread; BACKPROP root-cause + NEW/DISTILL code-walk reads delegable.
- No dashboards, no logs, no state files beyond SPEC.md itself.
- No auto-build after spec.
  User invokes build explicitly.
