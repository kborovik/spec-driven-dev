#!/usr/bin/env python3
"""check-mechanical — deterministic mechanical-audit core for the drift detector.

Owns the audit set the drift-detector skill declares "mechanical, no
LLM-judgment": SPEC-FORMAT structural rules (section catalog + order, row
grammar, column extraction, archive markers + sibling shape), monotonic IDs,
cite-DAG resolution + edge-type, history-residue patterns, pinned-invariant-header
grep, memo bookkeeping (sha / rev-parse), and token estimate. Emits the
standardized `id|verdict|evidence` pipe-table the skill merges into its REPORT.

Modes:
  audit       — read SPEC.md (+ sibling archive if present), run every mechanical
                audit, print the pipe-table. Optionally probe a REPO-LOCAL hook.
                Emits `mechanize|MISSING|…` / `mechanize|DRIFT|…` — the
                mechanize-scan invariant's pointer check: every user-invocable
                `skills/*/SKILL.md` (minus frontmatter `user-invocable: false`)
                carries a `## MECHANIZE` section that references
                `skills/_fragments/MECHANIZE` (MISSING absent/unpointed;
                DRIFT = section present but pointer missing). Canonical probe
                text lives once in the fragment — skill bodies never copy it.
                Emits `dispatch|VIOLATE|…` — the response-shape invariant's
                dispatch-target rule: no skill body slash-dispatches an auto-fire
                sub-skill (`/<plugin>:<sub-skill>` for a `user-invocable: false`
                sub-skill is never a valid dispatch target). Sub-skill set is
                derived frontmatter-only, plugin name from the manifest,
                backtick-wrapped forms exempt — realized once here so the
                drift-detector retires its hand-run skill-body slash grep.
                Emits `design-lifecycle|VIOLATE|…` / `design-lifecycle|MISSING|…`
                — the design-lifecycle invariant's post-approve contract:
                `skills/design/SKILL.md` prescribes `gh issue create` + class
                `--label` + `/sdd:spec github issue N` Next, and keeps
                `fold-design` as optional exclusion; `skills/github/SKILL.md`
                ISSUE accepts `--label`. Realized once here so the
                drift-detector retires a hand-run skill-body grep of the
                post-approve recipe.
                Emits `github-workflow|VIOLATE|…` / `github-workflow|MISSING|…`
                — the github-workflow invariant's PR-per-issue contract:
                `skills/github/SKILL.md` requires `gh issue develop`,
                `gh pr create --draft` (no review no Closes at create),
                `git push` (PUSH), load-and-run review, apply bug +
                suggestion, then `gh pr ready` (READY); bundled review
                skips on a doc-or-comment diff (`doc-or-comment` and
                `other diffs still run review` in github READY and
                POST-SPEC-CHAIN) and `load-and-run` stays required
                (review otherwise); leftover LINEAR /
                no-PR optional-track wording in that body is VIOLATE.
                No corresponding GitHub issue → no BRANCH, no PR
                (`gh pr create`) — converse of PR-per-issue.
                `skills/spec/SKILL.md` FOLD-IN github issue requires
                push default branch, issue branch (`gh issue develop`),
                one non-delta `--allow-empty` commit, then
                `gh pr create --draft` with `Related: #<issue>` before
                the spec delta (missing SPEC.md still opens the PR;
                no close trailer; no review-at-create). Spec stops
                before the chain. Chain cite is `/sdd:build` + READY
                remainder. Before-spec-delta block ! run `/sdd:build`
                or load POST-SPEC-CHAIN (numbered or not); POST-APPLY
                ! `auto-chain run` (chain once; owner = github PR).
                Non-github-issue APPLY
                requires `no github BRANCH, no github PR`.
                `skills/github/SKILL.md`
                requires `chain runs once`. `skills/github/SKILL.md`
                MERGE requires `--subject` and squash subject
                `#<issue>` (the linked issue, not merely PR);
                GitHub default `(#PR)` insufficient (closes §B.39);
                MERGE probes `gh pr checks` +
                `reviewDecision,mergeable` (closes §B.72);
                CLOSE `gh pr close --delete-branch` (closes §B.73);
                PR body `Related: #<issue>` (no Acceptance copy).
                READY remainder no wait, fold-produced Acceptance
                notes, re-run task verify, child-fail
                `gh pr comment` (closes §B.69, §B.70, §B.71,
                §B.74).
                `skills/build/SKILL.md`
                issue-linked pass
                requires github PUSH then load-and-run review-apply +
                `gh pr ready`; Next merge when approved.
                Issue-linked READY skips the green-path check hop:
                `skills/_fragments/CHAIN.md`, `skills/_fragments/NEXT.md`,
                and `skills/build/SKILL.md` require no check hop,
                Next item #1 merge phrasing, and `/sdd:check` listed
                not hopped (closes §B.66). README
                Issue-linked PR requires `gh pr create --draft`,
                `gh pr ready`, Closes only at merge, no-issue
                converse (`No corresponding GitHub issue`,
                `no git branch, no GitHub PR`), squash commit
                message `#<issue>` (closes §B.39),
                fold-produced §T ids (not post-spec
                `/sdd:build --all`; closes §B.67), and the
                doc-or-comment review skip. Acceptance-gate
                detector = issue linkage not planned close trailer;
                ALLOW @ build = evidence sufficient; close trailer
                MERGE-only (closes §B.40). Realized once
                here so the drift-detector retires a hand-run github-skill
                grep. Emits `write-serialize|VIOLATE|…` /
                `write-serialize|MISSING|…` — the write-serialize
                invariant's post-spec review spawn: `skills/github/SKILL.md`
                requires `scratch writes` and
                `uses general-purpose Agent, not read-only Explore` (closes §B.37).
                Emits `github-workflow|VIOLATE|…` for missing
                `POST-SPEC-CHILD=1` in `skills/build/SKILL.md` LOAD or
                `skills/github/SKILL.md` spawn prompt (closes §B.38).
                Emits `linear-no-pr|VIOLATE|…` — leftover LINEAR-no-PR
                wording (`LINEAR|solo linear|no PR required`) on skill
                bodies, fragments, README, CLAUDE.md (not SPEC.md — the
                sweep §T row names the pattern). Backtick-wrapped tokens
                exempt. Realized once here so the sweep cannot silently
                re-accumulate.
                Plugin-internal skill-body + plugin-README needle audits
                (design-lifecycle, github-workflow, write-serialize,
                condense-stub token, README Issue-linked PR, linear-no-pr,
                skill-effort)
                plus human-facing `symbols`/`idiom` skip when
                `plugin_dirs(repo_root)` is empty — empty
                produces no row, not MISSING/VIOLATE. A plugin repo
                still emits them (README, CLAUDE.md, manifests for
                `symbols`/`idiom`). Consumer extras-hook, cite-DAG,
                history, token-budget, and memo/scope-feed still run.
                `sembr` ADVISORY stays.
                Emits `grant|VIOLATE|…` — the tooling-preference invariant's
                grant-use rule, both directions: no frontmatter `allowed-tools`
                grant is zero-body-use (a granted tool the skill body never
                invokes); a body-prescribed catalogued tool with no grant is
                also VIOLATE (prescribed spawn/edit/write/read ! auto-run).
                Extra direction is sound by construction — flagged only on
                total body-absence (token, alias, operation verb, or
                Bash anchor). Reverse uses stricter
                prescription patterns so incidental "agent"/"edit"/"write"
                prose does not flood. `disallowed-tools` entries skip reverse.
                Spans the PUBLISHED + REPO-LOCAL skill set — realized once
                here so the drift-detector retires its hand-run allowed-tools
                grant sweep (a manual sweep misses rows).
                Emits `symbols|VIOLATE|…` — the symbol-set + human-clarity
                invariants' spell-out rule: no human-facing surface (README,
                CLAUDE.md, the plugin manifest) carries a naked `→ ≥ ≤ & ~`
                symbol outside a backtick span or fenced block. SPEC-adjacent
                telegraph keeps the set, so it is never scanned. Sound (fenced
                prose treated exempt too) — realized once here so the
                drift-detector retires its hand-run symbol grep. Skip when
                `plugin_dirs(repo_root)` is empty (closes §B.76); a plugin
                repo still emits.
                Emits `idiom|VIOLATE|…` — the human-clarity invariant's
                idiom-ban rule: no human-facing surface (README, CLAUDE.md, the
                plugin manifest) carries a banned idiom / jargon-idiom phrase from
                a curated low-false-positive subset of the steno BOUNDARIES ban
                list (multi-word idiom + hyphenated jargon-idiom only; ambiguous
                single words excluded). Backtick-span + fenced-block exempt —
                realized once here so the drift-detector retires its hand-run
                idiom grep, a fixed-pattern sweep a manual pass forgets to re-run.
                Skip when `plugin_dirs(repo_root)` is empty (closes §B.76);
                a plugin repo still emits.
                Emits `skill-effort|VIOLATE|…` — the skill-effort
                invariant: published `skills/*/SKILL.md` leave frontmatter
                `model` unset; `explain` and `check` set `effort: medium`;
                every other skill leaves `effort` unset; the README
                honored-frontmatter sentence names `effort`. Skip when
                `plugin_dirs(repo_root)` is empty (consumer-core-profile
                invariant); a plugin repo still emits.
                Emits `sembr|ADVISORY|…` — the sembr invariant's
                one-sentence-per-line rule: a prose source line in the sembr
                file set (README, CLAUDE.md, designs drafts, skill bodies)
                holds ≥ 2 sentences. Fenced blocks, `|`-table rows,
                frontmatter, blockquoted example copy, and backtick spans are
                exempt; pipe-row files never enter the set. Advisory only
                (source-format rule, never dirty) — realized once here so the
                drift-detector retires a hand-run multi-sentence line scan.
                Emits `batch|ADVISORY|recommended: <n> agents` — the
                §V-classification sub-agent count from the §V row count +
                PUBLISHED file census (batch invariant), consumed by the
                drift-detector's batch step in place of a hand-computed heuristic.
                Also emits the machine-side scope feed for the memo-driven default
                sweep: `tasks|ADVISORY|flipped-since-clean: …` (§T flipped `.`→`x`
                since the memo's clean sha), `diff|ADVISORY|touched: …` (paths
                changed since that sha), and `scope|ADVISORY|v-path-dirty: …` (§V
                rows whose body path tokens — quoted/backticked path-like strings
                — intersect that touched-set, computed script-side so the
                drift-detector never hand-greps the §V section). These plus the
                reshaped `memo|ADVISORY|… : <ids>` row carry stable comma-joined
                fields (no surrounding prose) so the drift-detector chains them
                straight into `emit-v-slices --dirty` without hand-rolling
                `git diff`.
  write-memo  — read the behavioral verdict table (§V/§I/§T classifications) on
                stdin; with --from-audit, re-run the mechanical audit internally
                and merge it (stdin = behavioral rows only, hand-merge banned).
                Validate the verdict vocab per row type, compute clean-set
                membership itself, and write the run memo (schema v3, per-row §V
                hashes, oversized-cell ack) plus the `.gitignore` guard
                (`check-state.json` + `backprop-handoff.json`) — only
                when the run is clean. The model never decides "clean". Exit
                0 = clean, 1 = dirty (memo untouched, CI-gateable), 2 = invalid
                vocab.
  emit-v-slices — read SPEC.md, print every §V row body with its source line
                range (`## V<n> SPEC.md:<start>-<end>` header + verbatim row
                text). Optional `--dirty V<n>,...` restricts to named rows
                (default is all). Sources the §V-classification slice for the
                drift-detector's single-agent and sub-agent batch paths without a
                whole-file Read (large SPEC exceeds the Read token cap).
                Resolves condense stub redirects (`→ .spec/check-extras.md §Vn`)
                by inlining the live body from `.spec/check-extras.md` when
                present (extras-hook invariant) so consumers never hand-resolve
                body files.
  emit-check-agent-prompt — print the canonical §V-classification sub-agent
                prompt block (single source with skills/_fragments/
                CHECK-AGENT-PROMPT.md).
  emit-superseded — read SPEC.md, print the condenser's prong-2 SUPERSEDED
                candidate set: every closed §T whose §V cite resolves only into
                the archived §V.retired block (absent from live §V). Live-only
                resolution, distinct from the cite-DAG audit's live+archive
                scope. Prints a `tid|superseded_v|original_cites` table the
                condenser consumes in place of by-hand per-cite resolution.
  emit-fold-seeds — read SPEC.md, print the condenser's prong-1 fold-candidate
                seed set: clusters of live §V rows that share a citer (a §T
                whose cites or a §B whose fix names ≥ 2 live §V rows co-cites
                them). Connected components over the co-citation graph. Prints a
                `cluster_members|co_citers` table — an advisory seed only; the
                operator confirms each fold at the condense CONFIRM gate (never
                auto-applied) per the fold-first-authoring invariant.
  emit-v-weights — read SPEC.md, print the condenser's prong-6 per-§V-row
                byte/token weight ranking plus the heavy-row set (top non-stub
                rows whose cumulative weight first reaches ≥ 50% of the
                non-stub §V section; stable tie-break descending weight then
                ascending id so run-stable). Already-stubbed rows
                (`→ .spec/check-extras.md §Vn`) are never heavy (stub =
                extraction-complete; re-extract no-op). Prints a
                `v_row|bytes|tokens|cum_pct|heavy` table sorted heaviest
                first — the condenser extracts the heavy rows' audit recipes
                without a by-inspection guess. All-stub fixture → empty
                heavy set.
  emit-row-ids — read SPEC.md, print the canonical live id-set skeleton: every
                live §V + §I + §T id as a verdict-table row. Default is blank
                verdict and evidence (`id||`). With --from-audit, pre-fill from
                the same memo + scope-feed sources audit emits: HOLD-SINCE-CLEAN
                for clean §V/§T, blank verdict for §I (full sweep), dirty §V
                and flipped §T. The drift-detector fills only the remaining
                blanks; write-memo rejects any blank typed row (exit 2)
                instead of joining advisory ids by hand. A live row can't be
                silently dropped from the verdict table (omitted-row
                undercoverage class). §I ids derive from kind-prefixed
                interface rows (`- api: POST /x → …` → `I.api`).
  emit-overview — read SPEC.md, print the LOAD-step spec overview: §G/§C/§I/§T/§B
                headers + bodies verbatim plus the §V id list only (no §V row
                bodies). The drift-detector loads this in place of a whole-file
                Read per the single-load invariant; §V bodies arrive via
                emit-v-slices, so loading them here too would double-load SPEC.md
                and re-hit the Read token cap on a large spec. The id list lets
                the consumer size the classification batch from the row count.
  emit-residue — read SPEC.md, print the condenser's prong-4 history-residue
                candidate set: every live §V/§T/§B row hit by the shared HR_*
                patterns (or oversized §T task / §B cause cells), after the
                same pre-filters as audit_history_residue. Prints a
                `section|id|pattern|line` table the condenser consumes in place
                of a per-run LLM regex paraphrase. Empty body (header only) =
                no residue = prong 4 skip. Single source with the audit path —
                never a second spelling of the freshness-contract pattern set.
  emit-archive-window — read SPEC.md, print the condenser's prong-3
                window-vs-archive decision: closed §T (status `x`) vs
                ARCHIVE_CLOSED_T (single source; never hardcode in skill body).
                Prints `action|tid_lo|tid_hi|count|marker` with action in
                {archive, keep, skip}. Closed count ≤ threshold → one skip row
                (prong 3 no-ops). Over threshold → archive older closed rows
                id-asc + keep newest N live; archive row's marker cell is the
                SPEC-FORMAT §T archive-marker H2. Condense consumes this table
                only — no hand-count of closed §T.
  emit-condense-propose — read SPEC.md, print the condenser's five PROPOSE seed
                tables in one invocation (fold-seeds, superseded,
                archive-window, residue, v-weights). Each table keeps its
                standalone columns; blocks labeled `## <name>` so PROPOSE
                splits by exact name (archive-marker `## archived: …` is not a
                block). /sdd:condense PROPOSE consumes this emit instead of
                five separate emit-* calls (mechanize-scan: ≥ 2 same-shape
                deterministic calls collapsed). Standalone modes remain.
  fix-sembr   — rewrite flagged multi-sentence prose lines one sentence per
                line, in place, over the sembr file set (`--files <comma-list>`
                overrides discovery). Shares the audit scan's exemption walk +
                boundary splitter — single source, no re-derived splitter — so
                fix and scan can never disagree on a line. A per-line
                rejoin-equivalence guard (whitespace-normalized join of the
                rewrite must equal the source line) leaves any failing line
                untouched, prints an UNVERIFIABLE row, and exits 1. Dry-run by
                default, `--write` applies. The sembr-advisory remediation and
                sweep-class tasks consume this instead of a scratchpad splitter.
  --self-test — run inline fixtures; exit 0 iff every assertion holds.

Parametric per the published-tooling invariant: reads SPEC-FORMAT conventions and
scope sets as input (PUBLISHED scope discovered from the marketplace manifest;
REPO-LOCAL scope from conventional paths or override). Repo-specific recipes stay
in a probed REPO-LOCAL hook, never here. Single-file, stdlib-only python3 per the
tooling-preference invariant — `re` is codepoint-based and platform-identical;
`hashlib` / `json` cover memo + self-test with zero deps.

Source discipline: this file ships in PUBLISHED scope, where a sibling audit greps
for pinned spec citations (a section letter directly followed by a number). To
avoid self-tripping that grep, the source never writes a literal section-letter
immediately followed by a literal digit: regexes use the `\\d` class, fixtures
interpolate `{n}`, and invariants are named, not numbered.
"""

import sys
import os
import re
import json
import hashlib
import subprocess
import argparse
import datetime
import tempfile

# --- verdict vocab (drift-verdict-vocab invariant) ---------------------------
# Per-row-type admissibility: §V (invariant), §I (interface), §T (task) rows each
# carry only the verdicts valid for their type, so the LLM can't silently remap
# an out-of-type verdict (closes §B.8). MATCH is the §I-clean verdict, admissible
# on §I rows only. Pseudo-id rows (mechanical findings: format/cite/history/… )
# are unrestricted — script-emitted, already trusted.

SILENT_CLEAN = {"HOLD", "HOLD-SINCE-CLEAN", "SCOPE-EMPTY", "LATENT"}   # no body row
SURFACED_CLEAN = {"VIOLATE-CAPTURED"}                                  # clean, surfaced
CLEAN_VERDICTS = SILENT_CLEAN | SURFACED_CLEAN
DIRTY_VERDICTS = {"VIOLATE", "UNVERIFIABLE", "UNRESOLVED", "TYPE-MISMATCH",
                  "DRIFT", "MISSING", "STALE", "EXTRA"}
# per-row-type admissible verdicts in the merged table
V_VOCAB = CLEAN_VERDICTS | {"VIOLATE", "UNVERIFIABLE"}
I_VOCAB = {"MATCH", "DRIFT", "MISSING", "EXTRA"}      # MATCH = §I-clean (§I rows only)
T_VOCAB = SILENT_CLEAN | {"STALE"}
ADVISORY = "ADVISORY"

TOKEN_BUDGET = 20000       # token-budget invariant advisory threshold
TOKEN_RATIO = 3.4          # bytes-per-token for telegraph register (token-budget invariant)
SKILL_TOKEN_BUDGET = 5000  # token-budget invariant per-skill-body advisory threshold
ARCHIVE_CLOSED_T = 50      # closed-§T window-vs-archive split (token-budget; condense prong 3)
# check-dispatch invariant — single source for skill §I + V47 arg set
CHECK_DISPATCH_ARGS = frozenset({"", "--full", "--no-chain", "--full --no-chain"})
OVERSIZE_CELL = 300        # history-residue oversized-cell advisory (chars)
MEMO_SCHEMA = 3            # memo schema version (memo invariant)
HISTORY_AGGREGATE_THRESHOLD = 10  # per-section body-row aggregation (drift-verdict-vocab invariant)
BATCH_ROW_DIVISOR = 15     # batch invariant: base agent count = ceil(|V| / 15)
BATCH_MAX_AGENTS = 4       # batch invariant: clamp ceil to [1, BATCH_MAX_AGENTS]

# --- structural patterns (note source discipline above) ----------------------

SECTION_HDR = re.compile(r'^## §([GCIVTB]) ')
V_ROW = re.compile(r'^(V\d+):\s?(.*)$')
T_ROW = re.compile(r'^(T\d+)\|')
B_ROW = re.compile(r'^(B\d+)\|')
# §I interface id derives from the row's kind prefix (`- api: POST /x → …`
# → `I.api`), bullet optional; kind charset matches CITE_TOKEN's I-token
# grammar so every emitted id is citable from §T.cites. Prose lines without
# a kind opener carry no id.
I_KIND = re.compile(r'^\s*(?:-\s+)?([a-z_][a-z0-9_]*):\s')
ID_NUM = re.compile(r'^([VTB])(\d+)$')
CITE_TOKEN = re.compile(r'^(V\d+|T\d+|B\d+|I\.[a-z_][a-z0-9_]*|-)$')
FIX_TOKEN = re.compile(r'^(V\d+|-)$')
TYPED_CITE = re.compile(r'§([VTB])\.(\d+)')
PINNED_HDR = re.compile(r'^#{2,}\s+[VTB]\d+\b')
ARCHIVE_MARK_ANY = re.compile(r'^## archived: ')
ARCHIVE_MARK_TB = re.compile(
    r'^## archived: §([TB])\.\d+\.\.§([TB])\.\d+ → SPEC\.archive\.md \(\d+ rows\)$')
ARCHIVE_MARK_V = re.compile(
    r'^## archived: §V\.retired → SPEC\.archive\.md \(\d+ retired rows\)$')
ARCHIVE_V_BLOCK = re.compile(r'^## §V\.retired\b')

# §B date cell shape (ISO-8601)
B_DATE = re.compile(r'^\d{4}-\d{2}-\d{2}$')

# history-residue / write-time-prune pattern set (freshness-contract +
# mechanical-realization invariants) — sole member source. Prose consumers
# (spec write-time prune, condense prong 4, reorganize ARCHIVE-RETIRED) cite
# the set name + `emit-prune-patterns`, never restate members. Roles:
#   residue    — audit-detect here; drop @ spec write / condense trim
#   fold       — write-time rewrite rule; folded form is the clean state,
#                so never audit-flagged
#   pre-filter — match exempts a row/span before the residue scan
PRUNE_PATTERNS = [
    {"id": "amendment-counter", "role": "residue",
     "pattern": r'\(∆+\)',
     "action": "drop — clean current state carries no edit tally"},
    {"id": "dated-retirement", "role": "residue",
     "pattern": r'\bretired \d{4}-\d{2}-\d{2}\b',
     "action": "drop — wholesale-retired row is reorganize archival job"},
    {"id": "supersession-narration", "role": "residue",
     "pattern": r'\bpre-amend\b|prior .{0,40}\b(?:retired|dropped|superseded)\b',
     "action": "drop — incl. recurrence-class lineage + surfaced-by prose "
               "past regex reach"},
    {"id": "closes-fold", "role": "fold",
     "pattern": r'\bCloses §B\.\d+\b',
     "action": "standalone sentence → `(closes §B.<n>)` suffix on prior clause"},
    {"id": "backtick-span", "role": "pre-filter",
     "pattern": r'`[^`]*`',
     "action": "exempt — verbatim-preservation; pattern-def rows never "
               "self-flag"},
    {"id": "cite-modifier", "role": "pre-filter",
     "pattern": r'§V\.\d+\(∆+\)',
     "action": "exempt — ∆-on-citation marks amended cross-ref, not retired "
               "value"},
    {"id": "retired-in-place", "role": "pre-filter",
     "pattern": r'^V\d+:\s+retired\s+\d{4}-\d{2}-\d{2}\b',
     "action": "exempt — §V row pending reorganize ARCHIVE-RETIRED migration"},
]
_PRUNE_RE = {p["id"]: re.compile(p["pattern"]) for p in PRUNE_PATTERNS}
# compiled aliases consumed by the audits — same objects as the emitted set
# (single source; HR_ = residue detectors, PF_ = pre-filters)
HR_AMEND = _PRUNE_RE["amendment-counter"]
HR_DATED = _PRUNE_RE["dated-retirement"]
HR_SUPERSEDE = _PRUNE_RE["supersession-narration"]
PF_BACKTICK = _PRUNE_RE["backtick-span"]
PF_CITE_MOD = _PRUNE_RE["cite-modifier"]
PF_RETIRED_INPLACE = _PRUNE_RE["retired-in-place"]

CANONICAL_ORDER = ["G", "C", "I", "V", "T", "B"]
SECTION_NAME = {"G": "GOAL", "C": "CONSTRAINTS", "I": "INTERFACES",
                "V": "INVARIANTS", "T": "TASKS", "B": "BUGS"}


# --- parsing -----------------------------------------------------------------

def parse_sections(text):
    """Return {letter: [(lineno, line), ...]} and the observed section order."""
    sections = {}
    order = []
    cur = None
    for i, line in enumerate(text.splitlines(), start=1):
        m = SECTION_HDR.match(line)
        if m:
            cur = m.group(1)
            sections[cur] = []
            order.append(cur)
        elif cur is not None:
            sections[cur].append((i, line))
    return sections, order


def split_cols(line):
    """SPEC-FORMAT column extraction: id is first `|`-segment, last column is
    rightmost `|`-segment. Body cells (between) preserve backtick-code `|`
    verbatim — never naïve all-`|` split."""
    first = line.find('|')
    last = line.rfind('|')
    if first == -1:
        return line, None, None
    row_id = line[:first]
    last_col = line[last + 1:]
    body = line[first + 1:last]
    return row_id, body, last_col


def parse_v_rows(sections):
    rows = []
    for lineno, line in sections.get("V", []):
        m = V_ROW.match(line)
        if m:
            rows.append({"id": m.group(1), "body": m.group(2),
                         "line": lineno, "full": line})
    return rows


def parse_i_ids(sections):
    """Derive the live §I interface id set. The §I section is prose/bullets
    (no pipe-rows); each kind-prefixed row (`- <kind>: <name> → <shape>`,
    bullet optional) yields id `I.<kind>` — the auditable interface contract.
    Preamble prose without a kind opener carries no id. Duplicate kinds dedup
    to one id (first occurrence), source order preserved."""
    ids = []
    seen = set()
    for lineno, line in sections.get("I", []):
        m = I_KIND.match(line)
        if m:
            iid = "I." + m.group(1)
            if iid not in seen:
                seen.add(iid)
                ids.append({"id": iid, "line": lineno})
    return ids


def emit_row_ids(v_rows, i_ids, t_rows):
    """Canonical live id-set skeleton (memo invariant): every live §V + §I + §T
    id, in section order. Returned as a flat id list; the caller renders one
    verdict-table row per id. The drift-detector fills verdicts against this
    script-emitted skeleton instead of hand-enumerating the live row set,
    closing the omitted-row silent-undercoverage class — the skeleton
    enumerates exactly the set the script already parses/hashes."""
    return ([r["id"] for r in v_rows]
            + [r["id"] for r in i_ids]
            + [r["id"] for r in t_rows])


def dirty_v_ids(v_rows, memo, touched, full=False):
    """Live §V ids that need behavioral classification (scope-feed + memo).

    full or unusable memo (None / bad schema) → every live V id.
    Else union of v_row_shas drift and v_path_dirty(touched).
    Reachable-sha gate is the caller's: pass memo=None when last_clean_sha
    is unreachable so this stays git-free and unit-testable.
    """
    if full or not memo or memo.get("schema_version") != MEMO_SCHEMA:
        return [r["id"] for r in v_rows]
    stored = memo.get("v_row_shas", {})
    cur = compute_v_row_shas(v_rows)
    sha_dirty = [rid for rid, h in cur.items() if stored.get(rid) != h]
    return sorted(set(sha_dirty) | set(v_path_dirty(v_rows, touched)),
                  key=lambda x: int(x[1:]))


def prefill_verdicts(ids, dirty_v, flipped_t):
    """Pre-fill emit-row-ids --from-audit table (memo + mechanical-realization).

    Clean §V/§T → HOLD-SINCE-CLEAN; dirty §V + flipped §T → blank; §I → blank
    (§I full-sweeps every run, so its verdict always comes from classification).
    Evidence cells stay blank — the drift-detector fills remaining blanks.
    """
    dirty = set(dirty_v)
    flipped = set(flipped_t)
    out = []
    for rid in ids:
        if ID_NUM.match(rid) and rid[0] == "V":
            v = "" if rid in dirty else "HOLD-SINCE-CLEAN"
        elif rid.startswith("I."):
            v = ""
        elif ID_NUM.match(rid) and rid[0] == "T":
            v = "" if rid in flipped else "HOLD-SINCE-CLEAN"
        else:
            v = ""
        out.append((rid, v, ""))
    return out


def emit_row_id_scope(v_rows, t_rows, memo, repo_root, spec_path="SPEC.md",
                      full=False):
    """Dirty §V + flipped §T from the same sources audit emits (scope-feed).

    Unusable memo → all live V dirty; flipped = flipped_since([], t_rows)
    (every current `x`, same as first-run). Usable memo → dirty_v_ids +
    flipped_since(spec at last_clean_sha, t_rows). --full with a usable
    memo still re-classifies every V; flipped set stays the real delta.
    """
    unusable = (not memo or memo.get("schema_version") != MEMO_SCHEMA
                or not git_sha_reachable(memo.get("last_clean_sha", "")))
    if unusable:
        return [r["id"] for r in v_rows], flipped_since([], t_rows)
    sha = memo.get("last_clean_sha", "")
    old_t = spec_t_rows_at(repo_root, sha, spec_path)
    touched = exclude_spec_paths(git_touched_paths(repo_root, sha), spec_path)
    return (dirty_v_ids(v_rows, memo, touched, full=full),
            flipped_since(old_t, t_rows))


# Condense prong-6 stub: body redirects to `.spec/check-extras.md §Vn`
V_STUB_RE = re.compile(
    r'→\s*`?\.spec/check-extras\.md\s+§(V\d+)`?',
    re.IGNORECASE,
)


def load_check_extras_bodies(repo_root):
    """Parse `.spec/check-extras.md` into {V<n>: body text under ## §Vn header}.
    Empty dict when file absent. Used by emit-v-slices to resolve stub redirects."""
    path = os.path.join(repo_root, ".spec", "check-extras.md")
    if not os.path.isfile(path):
        return {}
    try:
        text = read_text(path)
    except OSError:
        return {}
    bodies = {}
    cur_id = None
    cur_lines = []
    hdr = re.compile(r'^##\s+§?(V\d+)\b')
    for line in text.splitlines():
        m = hdr.match(line)
        if m:
            if cur_id is not None:
                bodies[cur_id] = "\n".join(cur_lines).strip()
            cur_id = m.group(1)
            cur_lines = []
            continue
        if cur_id is not None:
            cur_lines.append(line)
    if cur_id is not None:
        bodies[cur_id] = "\n".join(cur_lines).strip()
    return bodies


def collect_v_slices(sections, repo_root=None):
    """Return [{id, line_start, line_end, text, source}] every §V row — each row
    body with its source line span. Rows are normally single-line; the span
    captures any continuation lines up to the next row opener (trailing blanks
    trimmed) so a wrapped body stays faithful. Feeds the §V-classification slice
    per the batch invariant (script slice not whole-file Read).

    When repo_root is set, condense stub redirects
    (`→ .spec/check-extras.md §Vn`) resolve to the live body in check-extras.md
    (source field notes the body file). Unresolved stubs keep the stub text."""
    extras = load_check_extras_bodies(repo_root) if repo_root else {}
    extras_lines = {}
    if extras:
        try:
            for n, line in enumerate(read_text(os.path.join(
                    repo_root, ".spec", "check-extras.md")).splitlines(), 1):
                m = V_ROW.match(line)
                if m and m.group(1) not in extras_lines:
                    extras_lines[m.group(1)] = n
        except OSError:
            pass
    v_lines = sections.get("V", [])
    openers = [idx for idx, (_, line) in enumerate(v_lines) if V_ROW.match(line)]
    slices = []
    for k, idx in enumerate(openers):
        nxt = openers[k + 1] if k + 1 < len(openers) else len(v_lines)
        block = v_lines[idx:nxt]
        while block and block[-1][1].strip() == "":
            block = block[:-1]
        m = V_ROW.match(block[0][1])
        vid = m.group(1)
        text = "\n".join(b[1] for b in block)
        source = "SPEC.md"
        line_start, line_end = block[0][0], block[-1][0]
        stub = V_STUB_RE.search(text)
        if stub and extras:
            # Prefer the id named in the stub; fall back to the row id.
            body_id = stub.group(1)
            resolved = extras.get(body_id) or extras.get(vid)
            if resolved:
                # Keep opener line for identity; replace redirected body.
                text = f"{vid}: {resolved}" if not resolved.lstrip().startswith(vid) else resolved
                source = ".spec/check-extras.md"
                body_line = extras_lines.get(body_id) or extras_lines.get(vid)
                if body_line:
                    line_start = line_end = body_line
        slices.append({"id": vid,
                       "line_start": line_start,
                       "line_end": line_end,
                       "text": text,
                       "source": source})
    return slices


def collect_overview(sections, order):
    """Render the LOAD-step overview: §G/§C/§I/§T/§B headers + bodies verbatim,
    but §V as its id list only (no row bodies). Feeds the drift-detector's spec
    load in place of a whole-file Read per the single-load invariant — §V bodies
    arrive via emit-v-slices, so re-loading them here would double-load SPEC.md
    and re-hit the Read pagination cap on a large spec. Sections render in
    observed order; the §V id list lets the consumer size the classification
    batch (row count) without the bodies."""
    out = []
    v_ids = [r["id"] for r in parse_v_rows(sections)]
    for letter in order:
        if letter not in CANONICAL_ORDER:
            continue
        out.append(f"## §{letter} {SECTION_NAME[letter]}")
        if letter == "V":
            out.append(",".join(v_ids))
        else:
            out.extend(line for _, line in sections.get(letter, []))
    return "\n".join(out)


def emit_superseded_candidates(v_rows, t_rows):
    """Prong-2 SUPERSEDED candidate set (token-budget-condense invariant): each
    closed §T (status `x`) whose §V cite is absent from the live §V section →
    candidate — the cited invariant was amended away or folded (resolution lands
    only in the archived §V.retired block, or nowhere). Live-§V-only resolution,
    distinct from the cite-DAG audit's live+archive scope (where an archived
    cite holds resolved). Returns [{id, unresolved:[V<n>,...], cites}] — the
    condenser builds `SUPERSEDED — §V.<m> amend` markers from it without by-hand
    per-cite resolution (operator confirms each because content-amend-away not
    cite-detectable)."""
    live_v = {r["id"] for r in v_rows}
    out = []
    for r in t_rows:
        body = r["body"] or ""
        status = body.split('|', 1)[0].strip()
        if status != "x":
            continue
        cites = r["last"]
        if cites is None:
            continue
        unresolved = []
        for tok in cites.split(','):
            tok = tok.strip()
            m = ID_NUM.match(tok)
            if m and m.group(1) == "V" and tok not in live_v:
                unresolved.append(tok)
        if unresolved:
            out.append({"id": r["id"], "unresolved": unresolved, "cites": cites})
    return out


def emit_archive_window(t_rows, threshold=None):
    """Prong-3 window-vs-archive split (token-budget + archive-semantics +
    mechanical-realization): closed §T (status `x`) ordered id ascending.
    threshold defaults to ARCHIVE_CLOSED_T — single source; skill bodies never
    hardcode the number. Closed count ≤ threshold → one skip row (condense
    prong 3 no-ops). Over threshold → archive older (count − N) closed rows
    id-asc, keep newest N live; archive row carries the SPEC-FORMAT §T
    archive-marker H2 in `marker`. Returns [{action, tid_lo, tid_hi, count,
    marker}] with action in {archive, keep, skip}. Open (`.`) §T never count."""
    if threshold is None:
        threshold = ARCHIVE_CLOSED_T
    closed = []
    for r in t_rows:
        status = (r.get("body") or "").split('|', 1)[0].strip()
        if status == "x":
            closed.append(r["id"])
    closed.sort(key=lambda tid: int(tid[1:]))
    n = len(closed)
    if n <= threshold:
        return [{"action": "skip", "tid_lo": "", "tid_hi": "",
                 "count": 0, "marker": ""}]
    archive_ids = closed[: n - threshold]
    keep_ids = closed[n - threshold:]
    a_lo, a_hi = archive_ids[0], archive_ids[-1]
    a_n = len(archive_ids)
    # marker built from numeric tails so source never holds letter+digit pin
    lo_n, hi_n = a_lo[1:], a_hi[1:]
    marker = (f"## archived: §T.{lo_n}..§T.{hi_n} "
              f"→ SPEC.archive.md ({a_n} rows)")
    k_lo, k_hi = keep_ids[0], keep_ids[-1]
    return [
        {"action": "archive", "tid_lo": a_lo, "tid_hi": a_hi,
         "count": a_n, "marker": marker},
        {"action": "keep", "tid_lo": k_lo, "tid_hi": k_hi,
         "count": len(keep_ids), "marker": ""},
    ]


def _live_v_cites(cites, live_v):
    """Distinct live §V tokens named in a `cites`/`fix` cell, order preserved."""
    out, seen = [], set()
    for tok in cites.split(','):
        tok = tok.strip()
        m = ID_NUM.match(tok)
        if m and m.group(1) == "V" and tok in live_v and tok not in seen:
            seen.add(tok)
            out.append(tok)
    return out


def emit_fold_seeds(v_rows, t_rows, b_rows):
    """Prong-1 fold-candidate seed (token-budget-condense invariant): cluster live
    §V rows that share a citer — a §T whose `cites` or a §B whose `fix` names ≥ 2
    live §V rows co-cites them so they are fold-candidate siblings. Edges run
    between every pair of live §V rows a single citer names; clusters is connected
    components over that co-citation graph. Live-§V-only — an archived or folded
    cite forms no edge. Returns [{members:[V<n>,...], citers:[T<n>|B<n>,...]}]
    sorted by lowest member id; an advisory seed only — the operator confirms
    each fold at the condense CONFIRM gate (never auto-applied) per the
    fold-first-authoring invariant."""
    live_v = {r["id"] for r in v_rows}
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    citers = []  # (citer_id, [live §V tokens]) for citers naming ≥ 2 live §V
    for r in t_rows + b_rows:
        if r["last"] is None:
            continue
        vs = _live_v_cites(r["last"], live_v)
        if len(vs) >= 2:
            citers.append((r["id"], vs))
            for v in vs[1:]:
                union(vs[0], v)

    comps = {}
    for v in parent:
        comps.setdefault(find(v), set()).add(v)

    def id_num(tok):
        return int(tok[1:])

    def citer_key(cid):
        return (cid[0], int(cid[1:]))

    out = []
    for root, members in comps.items():
        if len(members) < 2:
            continue
        member_list = sorted(members, key=id_num)
        cl_citers = sorted((cid for cid, vs in citers if find(vs[0]) == root),
                           key=citer_key)
        out.append({"members": member_list, "citers": cl_citers})
    out.sort(key=lambda d: id_num(d["members"][0]))
    return out


def emit_v_weights(v_rows):
    """Prong-6 per-§V-row weight ranking (token-budget-condense invariant): byte
    weight is utf-8 length of the full row line, token weight is byte/TOKEN_RATIO
    per the token-budget invariant. Ranks rows descending weight, tie-break
    ascending id so run-stable; the heavy set is the prefix of non-stub rows
    whose cumulative weight first reaches ≥ 50% of the non-stub §V-section
    total. Already-stubbed rows (`→ .spec/check-extras.md §Vn`) are never
    heavy (stub = extraction-complete; re-extract no-op). Returns
    (ranked, total_bytes) where each ranked entry is {id, bytes, tokens,
    cum_pct, heavy}. The condenser extracts heavy rows' audit recipes
    without a by-inspection guess."""
    weights = []
    for r in v_rows:
        full = r["full"]
        b = len(full.encode("utf-8"))
        weights.append({"id": r["id"], "bytes": b,
                        "tokens": int(b / TOKEN_RATIO),
                        "stub": bool(V_STUB_RE.search(full))})
    ranked = sorted(weights, key=lambda w: (-w["bytes"], int(w["id"][1:])))
    total = sum(w["bytes"] for w in ranked)
    live_total = sum(w["bytes"] for w in ranked if not w["stub"])
    half = live_total / 2
    cum = 0
    live_cum = 0
    heavy_done = False
    for w in ranked:
        cum += w["bytes"]
        w["cum_pct"] = round(100 * cum / total, 1) if total else 0.0
        if w["stub"]:
            w["heavy"] = False
            continue
        if heavy_done or live_total == 0:
            w["heavy"] = False
        else:
            live_cum += w["bytes"]
            w["heavy"] = True
            if live_cum >= half:
                heavy_done = True
    return ranked, total


# Condense PROPOSE seed tables (mechanize-scan: five same-shape emit-* calls
# collapsed). Order + names are the consume contract; columns stay those of the
# standalone modes (mechanical-realization — formatters shared, not restated).
CONDENSE_PROPOSE_TABLES = (
    "fold-seeds", "superseded", "archive-window", "residue", "v-weights",
)
CONDENSE_PROPOSE_HEAD = re.compile(
    r"^## (" + "|".join(re.escape(n) for n in CONDENSE_PROPOSE_TABLES) + r")$",
    re.M,
)


def format_fold_seeds_table(seeds):
    lines = ["cluster_members|co_citers"]
    for s in seeds:
        lines.append(f"{','.join(s['members'])}|{','.join(s['citers'])}")
    return "\n".join(lines)


def format_superseded_table(candidates):
    lines = ["tid|superseded_v|original_cites"]
    for c in candidates:
        lines.append(f"{c['id']}|{','.join(c['unresolved'])}|{c['cites']}")
    return "\n".join(lines)


def format_archive_window_table(rows):
    lines = ["action|tid_lo|tid_hi|count|marker"]
    for r in rows:
        lines.append(f"{r['action']}|{r['tid_lo']}|{r['tid_hi']}|{r['count']}|"
                     f"{r['marker']}")
    return "\n".join(lines)


def format_residue_table(rows):
    lines = ["section|id|pattern|line"]
    for r in rows:
        lines.append(f"{r['section']}|{r['id']}|{r['pattern']}|{r['line']}")
    return "\n".join(lines)


def format_v_weights_table(ranked):
    lines = ["v_row|bytes|tokens|cum_pct|heavy"]
    for w in ranked:
        lines.append(f"{w['id']}|{w['bytes']}|{w['tokens']}|{w['cum_pct']}|"
                     f"{'yes' if w['heavy'] else 'no'}")
    return "\n".join(lines)


def collect_condense_propose(v_rows, t_rows, b_rows):
    """Five PROPOSE seed tables, columns unchanged vs standalone emit modes.
    Returns [(name, table_text), ...] in CONDENSE_PROPOSE_TABLES order."""
    ranked, _ = emit_v_weights(v_rows) if v_rows else ([], 0)
    return [
        ("fold-seeds",
         format_fold_seeds_table(emit_fold_seeds(v_rows, t_rows, b_rows))),
        ("superseded",
         format_superseded_table(emit_superseded_candidates(v_rows, t_rows))),
        ("archive-window",
         format_archive_window_table(emit_archive_window(t_rows))),
        ("residue",
         format_residue_table(collect_residue_rows(v_rows, t_rows, b_rows))),
        ("v-weights", format_v_weights_table(ranked)),
    ]


def format_condense_propose(tables):
    """Labeled `## <name>` blocks so PROPOSE splits by exact name.
    Archive-marker `## archived: …` lives inside a pipe cell, not a block."""
    return "\n\n".join(f"## {name}\n{table}" for name, table in tables)


def parse_condense_propose(text):
    """Split labeled ## <name> blocks. Exact-name only so an archive-marker
    line-cell never starts a block. Returns {name: table_text}."""
    matches = list(CONDENSE_PROPOSE_HEAD.finditer(text))
    out = {}
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        out[m.group(1)] = text[start:end].strip("\n")
    return out


def parse_pipe_rows(sections, letter, pat):
    rows = []
    for lineno, line in sections.get(letter, []):
        if pat.match(line):
            rid, body, last = split_cols(line)
            rows.append({"id": rid, "body": body, "last": last,
                         "line": lineno, "full": line})
    return rows


# --- format audits -----------------------------------------------------------

def audit_section_catalog(order):
    out = []
    seen = [s for s in order if s in CANONICAL_ORDER]
    for letter in CANONICAL_ORDER:
        if letter not in seen:
            out.append(("format", "VIOLATE",
                        f"format: section §{letter} {SECTION_NAME[letter]} absent"))
    # order check over the sections that are present
    expected = [s for s in CANONICAL_ORDER if s in seen]
    if seen != expected:
        for idx, letter in enumerate(expected):
            if idx >= len(seen) or seen[idx] != letter:
                out.append(("format", "VIOLATE",
                            f"format: section §{letter} out-of-order "
                            f"(expected position {idx + 1})"))
                break
    return out


def audit_cites_grammar(t_rows):
    out = []
    for r in t_rows:
        cites = r["last"]
        if cites is None:
            continue
        for tok in cites.split(','):
            if not CITE_TOKEN.match(tok):
                out.append(("format", "VIOLATE",
                            f"format: §T.{r['id']} cites token \"{tok}\" "
                            f" not in comma-list grammar @ SPEC.md:{r['line']}"))
    return out


def audit_fix_grammar(b_rows):
    out = []
    for r in b_rows:
        fix = r["last"]
        if fix is None:
            continue
        for tok in fix.split(','):
            if not FIX_TOKEN.match(tok):
                out.append(("format", "VIOLATE",
                            f"format: §B.{r['id']} fix token \"{tok}\" "
                            f" not in comma-list grammar @ SPEC.md:{r['line']}"))
    return out


def audit_monotonic(rows, letter):
    out = []
    prev = None
    for r in rows:
        m = ID_NUM.match(r["id"])
        if not m:
            continue
        n = int(m.group(2))
        if prev is not None and n <= prev:
            out.append(("format", "VIOLATE",
                        f"format: §{letter}.{r['id']} ID reuse or out-of-order "
                        f"@ SPEC.md:{r['line']}"))
        prev = n
    return out


def audit_status_cells(t_rows):
    """§T status cell ! in {`.`, `x`} (SPEC-FORMAT row schema)."""
    out = []
    for r in t_rows:
        status = (r["body"] or "").split('|', 1)[0].strip()
        if status not in (".", "x"):
            out.append(("format", "VIOLATE",
                        f"format: §T.{r['id']} status \"{status}\" not in "
                        f"{{., x}} @ SPEC.md:{r['line']}"))
    return out


def audit_bug_dates(b_rows):
    """§B date cell ! ISO-8601 `YYYY-MM-DD` (SPEC-FORMAT row schema)."""
    out = []
    for r in b_rows:
        date = (r["body"] or "").split('|', 1)[0].strip()
        if not B_DATE.match(date):
            out.append(("format", "VIOLATE",
                        f"format: §B.{r['id']} date \"{date}\" not ISO-8601 "
                        f"(YYYY-MM-DD) @ SPEC.md:{r['line']}"))
    return out


def audit_archive_markers(sections, archive_present, archive_has_vretired,
                          arch_ids=None):
    """Archive marker shape under §T/§B (and §V when a retired block exists).
    With `arch_ids` (per-letter archived id sets), a §T/§B marker is required
    only when that section has archived rows, and its range + count must match
    those rows; a marker over zero archived rows is VIOLATE."""
    out = []
    found = {"T": False, "B": False, "V": False}
    for letter in ("T", "B", "V"):
        for lineno, line in sections.get(letter, []):
            if ARCHIVE_MARK_ANY.match(line):
                found[letter] = True
                if letter in ("T", "B"):
                    m = ARCHIVE_MARK_TB.match(line)
                    if not m:
                        out.append(("format", "VIOLATE",
                                    f"format: §{letter} archive marker malformed "
                                    f"@ SPEC.md:{lineno}"))
                    elif arch_ids is not None:
                        out += _archive_marker_range(letter, line, lineno,
                                                     arch_ids.get(letter, set()))
                else:
                    if not ARCHIVE_MARK_V.match(line):
                        out.append(("format", "VIOLATE",
                                    f"format: §V archive marker malformed "
                                    f"@ SPEC.md:{lineno}"))
    if archive_present:
        for letter in ("T", "B"):
            needed = (arch_ids is None) or bool(arch_ids.get(letter))
            if needed and not found[letter]:
                out.append(("format", "VIOLATE",
                            f"format: §{letter} missing archive marker "
                            f"(SPEC.archive.md has archived §{letter} rows)"))
        if archive_has_vretired and not found["V"]:
            out.append(("format", "VIOLATE",
                        "format: §V missing §V.retired archive marker "
                        "(archive contains §V.retired)"))
    return out


ARCHIVE_MARK_NUMS = re.compile(r'§[TB]\.(\d+)\.\.§[TB]\.(\d+) .*\((\d+) rows\)')


def _archive_marker_range(letter, line, lineno, ids):
    """Marker `lo..hi (n rows)` must match the archived §<letter> id set."""
    m = ARCHIVE_MARK_NUMS.search(line)
    nums = sorted(int(i[1:]) for i in ids)
    if not nums:
        return [("format", "VIOLATE",
                 f"format: §{letter} archive marker @ SPEC.md:{lineno} claims "
                 f"archived rows but SPEC.archive.md has none")]
    if m and (int(m.group(1)), int(m.group(2)), int(m.group(3))) != \
            (nums[0], nums[-1], len(nums)):
        return [("format", "VIOLATE",
                 f"format: §{letter} archive marker @ SPEC.md:{lineno} range/count "
                 f"≠ archived rows ({letter}{nums[0]}..{letter}{nums[-1]}, "
                 f"{len(nums)} rows)")]
    return []


def audit_archive_sibling(archive_text):
    """When SPEC.archive.md exists, it carries §T then §B H2 sections (canonical
    order) + optional §V.retired block."""
    out = []
    heads = [l for l in archive_text.splitlines() if l.startswith("## ")]
    seq = []
    for h in heads:
        if re.match(r'^## §T TASKS\b', h):
            seq.append("T")
        elif re.match(r'^## §B BUGS\b', h):
            seq.append("B")
        elif ARCHIVE_V_BLOCK.match(h):
            seq.append("Vret")
    core = [s for s in seq if s in ("T", "B")]
    if core != ["T", "B"]:
        out.append(("format", "VIOLATE",
                    f"format: SPEC.archive.md section order {core} differs [T, B]"))
    return out


def archive_has_vretired(archive_text):
    return any(ARCHIVE_V_BLOCK.match(l) for l in archive_text.splitlines())


# --- cite-DAG ----------------------------------------------------------------

def strip_backticks(s):
    return PF_BACKTICK.sub('', s)


def audit_cite_dag(v_rows, t_rows, b_rows, sections, arch_ids, repo_local_files,
                   i_ids):
    """Resolve typed cites to existing rows of the expected edge type.
    Emits UNRESOLVED / TYPE-MISMATCH only (HOLD silent)."""
    out = []
    i_set = {r["id"] for r in i_ids}
    live = {"V": {r["id"] for r in v_rows},
            "T": {r["id"] for r in t_rows},
            "B": {r["id"] for r in b_rows}}
    allids = {"V": live["V"] | arch_ids["V"],
              "T": live["T"] | arch_ids["T"],
              "B": live["B"] | arch_ids["B"]}

    def resolve(letter, num, citer, expect=None):
        rid = f"{letter}{num}"
        if rid not in allids[letter]:
            out.append(("cite", "UNRESOLVED",
                        f"{citer} {rid} UNRESOLVED: row absent from §{letter}"))
            return
        if expect and letter != expect:
            out.append(("cite", "TYPE-MISMATCH",
                        f"{citer} {rid} TYPE-MISMATCH: §{letter} row, "
                        f"expected §{expect}"))

    # §T.cites → resolve each token to its section (task-addresses-invariant)
    for r in t_rows:
        if r["last"] is None:
            continue
        for tok in r["last"].split(','):
            if tok == '-':
                continue
            if tok.startswith('I.'):
                if tok not in i_set:
                    out.append(("cite", "UNRESOLVED",
                                f"§T.{r['id']}.cites {tok} UNRESOLVED: "
                                f"kind absent from §I"))
                continue
            m = ID_NUM.match(tok)
            if m:
                resolve(m.group(1), m.group(2), f"§T.{r['id']}.cites")
    # §B.fix → §V (bug-catches-invariant-gap)
    for r in b_rows:
        if r["last"] is None:
            continue
        for tok in r["last"].split(','):
            if tok == '-':
                continue
            m = ID_NUM.match(tok)
            if m:
                resolve(m.group(1), m.group(2), f"§B.{r['id']}.fix", expect="V")
    # inline typed cites in §V/§C/§I bodies → cross-reference (backtick-stripped)
    for letter in ("G", "C", "I", "V"):
        for lineno, line in sections.get(letter, []):
            for m in TYPED_CITE.finditer(strip_backticks(line)):
                resolve(m.group(1), m.group(2), f"SPEC.md:{lineno}")
    # REPO-LOCAL pinned cites → SPEC.md row (project-local), backtick-filtered
    for path in repo_local_files:
        try:
            txt = read_text(path)
        except OSError:
            continue
        for i, line in enumerate(txt.splitlines(), start=1):
            for m in TYPED_CITE.finditer(strip_backticks(line)):
                resolve(m.group(1), m.group(2), f"{path}:{i}")
    return out


# --- history-residue ---------------------------------------------------------

def collect_oversized_cells(t_rows, b_rows):
    """Cell-ids whose §T `task` or §B `cause` body exceeds OVERSIZE_CELL chars —
    the oversized-cell smell set. §V rows exempt (no length advisory). §T order
    then §B order; the ack sha sorts the set so emission order is immaterial."""
    out = []
    for r in t_rows + b_rows:
        if len(r["body"] or "") > OVERSIZE_CELL:
            out.append(r["id"])
    return out


def oversized_cell_sha(cell_ids):
    """sha256 over the sorted oversized cell-id set (memo invariant) — the ack
    key. Order-independent so stable while the set is unchanged; a new oversized
    cell shifts the set so shifts the sha so re-fires the suppressed advisory."""
    return hashlib.sha256(",".join(sorted(set(cell_ids))).encode("utf-8")).hexdigest()


# pattern names shared by audit + emit-residue (freshness-contract invariant)
HR_PATTERN_ORDER = ("amendment-counter", "dated-retirement", "supersession-narration")
HR_PATTERN_FUNCS = (
    ("amendment-counter", HR_AMEND),
    ("dated-retirement", HR_DATED),
    ("supersession-narration", HR_SUPERSEDE),
)
OVERSIZE_PATTERN = "oversized-cell"


def collect_residue_rows(v_rows, t_rows, b_rows):
    """Per-row residue hits — single source for audit_history_residue +
    emit-residue. Returns list of dicts {section, id, pattern, line}.
    Pre-filters: retired-in-place §V, backtick-wrapped tokens, cite-modifier
    `§V.<n>(∆)`. Oversized §T/§B cells use pattern oversized-cell."""
    out = []

    def scan(rid, body, line, kind):
        # retired-in-place §V row exempt (pending reorganize archival)
        if kind == "V" and PF_RETIRED_INPLACE.match(f"{rid}: {body}"):
            return
        residue = PF_CITE_MOD.sub('', strip_backticks(body))
        for name, rx in HR_PATTERN_FUNCS:
            if rx.search(residue):
                out.append({"section": kind, "id": rid,
                            "pattern": name, "line": line})

    for r in v_rows:
        scan(r["id"], r["body"] or "", r["line"], "V")
    for r in t_rows:
        scan(r["id"], r["body"] or "", r["line"], "T")
    for r in b_rows:
        scan(r["id"], r["body"] or "", r["line"], "B")

    for r in t_rows + b_rows:
        if len(r["body"] or "") > OVERSIZE_CELL:
            kind = "T" if r["id"].startswith("T") else "B"
            out.append({"section": kind, "id": r["id"],
                        "pattern": OVERSIZE_PATTERN, "line": r["line"]})
    return out


def audit_history_residue(v_rows, t_rows, b_rows, full=False, oversized_ack=None):
    """Verdict-table form of residue hits. Consumes collect_residue_rows so
    pattern set + pre-filters stay byte-shared with emit-residue."""
    hits = collect_residue_rows(v_rows, t_rows, b_rows)
    by_section = {"V": [], "T": [], "B": []}
    for h in hits:
        if h["pattern"] == OVERSIZE_PATTERN:
            continue
        by_section[h["section"]].append((h["pattern"], h["id"], h["line"]))

    out = []
    for kind in ("V", "T", "B"):
        items = by_section[kind]
        if not items:
            continue
        if not full and len(items) > HISTORY_AGGREGATE_THRESHOLD:
            counts = {}
            for pattern, _, _ in items:
                counts[pattern] = counts.get(pattern, 0) + 1
            breakdown = ", ".join(f"{counts[p]} {p}"
                                  for p in HR_PATTERN_ORDER if p in counts)
            out.append(("history", "VIOLATE",
                        f"§{kind}: {len(items)} rows ({breakdown}) "
                        f"→ /sdd:condense body-trim"))
        else:
            for pattern, rid, line in items:
                out.append(("history", "VIOLATE",
                            f"§{kind}.{rid} VIOLATE: history: {pattern} "
                            f"@ SPEC.md:{line}"))

    advisories = collect_oversized_cells(t_rows, b_rows)
    if advisories and oversized_cell_sha(advisories) != oversized_ack:
        out.append(("history", ADVISORY,
                    "history: oversized cells (smell): "
                    + ", ".join(advisories) + " — consider /sdd:condense body-trim"))
    return out


# --- pinned-invariant-header -------------------------------------------------

def audit_pinned_header(published_md):
    out = []
    for path in published_md:
        try:
            txt = read_text(path)
        except OSError:
            continue
        for i, line in enumerate(txt.splitlines(), start=1):
            if PINNED_HDR.match(line):
                out.append(("pinned-header", "VIOLATE",
                            f"pinned-header VIOLATE: {path}:{i} pins invariant "
                            f"number in header"))
    return out


# --- human-facing naked-symbol audit -----------------------------------------
# symbol-set + human-clarity invariants: human-facing prose spells out the
# `→ ≥ ≤ & ~` set; SPEC-adjacent telegraph KEEPS it. Realized once here
# (mechanical-realization invariant) so the drift-detector retires the hand-run
# `grep` symbol sweep a manual pass misses (the bug this guards).

HUMAN_SYMBOLS = re.compile(r'[→≥≤&~]')
FENCE_LINE = re.compile(r'^\s*(?:```|~~~)')


def scan_human_symbols(path, text):
    """Flag naked spell-out-set symbols in one human-facing surface — outside
    inline backtick spans and fenced code blocks. Backtick-wrapped tokens,
    fenced telegraph-examples, and ASCII-diagram rows are verbatim-exempt
    (verbatim-preservation invariant). Sound, not complete: fenced *prose* (a
    file-manifest block) is treated exempt too, so the check catches the
    regular-prose recurrence class it mechanizes without false-flagging the
    telegraph-format demo blocks. One VIOLATE row per offending line; clean → no
    row (silent, sibling convention)."""
    out = []
    in_fence = False
    for i, line in enumerate(text.splitlines(), start=1):
        if FENCE_LINE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        hits = sorted(set(HUMAN_SYMBOLS.findall(strip_backticks(line))))
        if hits:
            out.append(("symbols", "VIOLATE",
                        f"symbols VIOLATE: {path}:{i} naked {' '.join(hits)} "
                        f"in human-facing prose — spell out per symbol-set + "
                        f"human-clarity invariants"))
    return out


def audit_human_symbols(human_files):
    """File-reading wrapper (symbol-set + human-clarity invariants). Asserts no
    human-facing surface carries a non-exempt naked symbol — realized once here,
    retiring the hand-run symbol grep a manual sweep misses."""
    out = []
    for path in human_files:
        try:
            txt = read_text(path)
        except OSError:
            continue
        out += scan_human_symbols(path, txt)
    return out


# --- human-facing banned-idiom audit -----------------------------------------
# human-clarity invariant: human-facing prose (README, CLAUDE.md, manifest) carries
# no banned idiom / jargon-idiom. The phrase set is a CURATED low-false-positive
# subset of the steno BOUNDARIES ban list — multi-word idiom + hyphenated
# jargon-idiom exact phrases only. Ambiguous single words ("smell", "bite") are
# deliberately excluded so legit technical prose never false-trips (the accepted
# cost is a false negative on a bare single-word metaphor). Realized once here
# (mechanical-realization invariant) so the drift-detector retires the hand-run
# idiom grep — a fixed-pattern sweep a manual pass forgets to re-run (the recurrence
# class this guards). Backtick-span + fenced-block exempt (verbatim-preservation
# invariant): a code-span or fenced example naming a banned phrase (CLAUDE.md
# enumerates the ban list) is fine; a live non-exempt prose use is VIOLATE.

BANNED_IDIOM = [
    "load-bearing", "by-construction", "hand-rolled", "clean-slate",
    "prior-art", "carry-cost",                       # jargon-idiom (hyphenated)
    "moves the needle", "low-hanging fruit", "boil the ocean",  # multi-word idiom
    "earns its", "smells like",                      # multi-word metaphor (B22 class)
]


def scan_human_idiom(path, text):
    """Flag a banned idiom / jargon-idiom phrase in one human-facing surface —
    outside inline backtick spans and fenced code blocks. Match is a
    case-insensitive substring over the backtick-stripped line; the curated
    BANNED_IDIOM set is multi-word / hyphenated only so the substring test stays
    low-false-positive. Backtick-wrapped tokens, fenced examples, and fenced
    prose are verbatim-exempt (verbatim-preservation invariant). One VIOLATE row
    per offending line, listing the matched phrases in set order (run-stable);
    clean → no row (silent, sibling convention)."""
    out = []
    in_fence = False
    for i, line in enumerate(text.splitlines(), start=1):
        if FENCE_LINE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        bare = strip_backticks(line).lower()
        hits = [p for p in BANNED_IDIOM if p in bare]
        if hits:
            out.append(("idiom", "VIOLATE",
                        f"idiom VIOLATE: {path}:{i} banned idiom "
                        f"{', '.join(hits)} in human-facing prose — write the "
                        f"literal meaning per human-clarity invariant"))
    return out


def audit_human_idiom(human_files):
    """File-reading wrapper (human-clarity invariant). Asserts no human-facing
    surface carries a banned exact-phrase idiom / jargon-idiom — realized once
    here, retiring the hand-run idiom grep a manual sweep forgets to re-run."""
    out = []
    for path in human_files:
        try:
            txt = read_text(path)
        except OSError:
            continue
        out += scan_human_idiom(path, txt)
    return out


# --- sembr multi-sentence-line advisory ---------------------------------------
# sembr invariant: repo `.md` prose source lines break per sentence (semantic
# line breaks) — one sentence per line, clause-boundary break OK. Source-format
# only, so a breach is ADVISORY (never dirty, CI-unaffected): a prose line
# holding ≥ 2 sentences. A sentence boundary = terminator (+ optional bold /
# quote / paren closers) then space then a capital, outside a backtick span,
# not after an abbreviation (`e.g.`, `vs.`, an ellipsis), and not the leading
# list marker itself. Fenced blocks, `|`-table rows, YAML frontmatter, and
# blockquoted example copy (verbatim-preservation invariant) are exempt;
# pipe-row files never enter the file set. Realized once here per the
# mechanical-realization invariant so the drift-detector retires a hand-run
# multi-sentence line scan.

SEMBR_BOUNDARY = re.compile(r'[.!?](?:\*\*|["\')\]])* +(?=[A-Z])')
SEMBR_ABBREV = re.compile(r'(?:\b(?:e\.g|i\.e|etc|vs|cf|incl|approx)|\.)\.$')
SEMBR_MARKER = re.compile(r'^\s*(?:[-*+]|\d+\.)\s+')


def iter_sembr_lines(text):
    """Yield (lineno, line) for sembr-eligible prose lines. The exemption walk
    per the sembr invariant + verbatim-preservation — frontmatter, fenced
    blocks, `|`-table rows, blockquotes — realized once here and shared by
    scan_sembr (flag) + fix-sembr (rewrite), so the two modes can never
    disagree on scope."""
    in_fence = False
    in_front = False
    for i, line in enumerate(text.splitlines(), start=1):
        if i == 1 and line.strip() == "---":
            in_front = True
            continue
        if in_front:
            if line.strip() == "---":
                in_front = False
            continue
        if FENCE_LINE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        ls = line.lstrip()
        if ls.startswith("|") or ls.startswith(">"):
            continue
        yield i, line


def sembr_split_points(line):
    """Sentence-boundary offsets into the ORIGINAL line (each = the index of
    the next sentence's first char). The single splitter shared by scan_sembr
    + fix-sembr per the mechanical-realization invariant — no re-derived
    splitter. Backtick spans are masked length-preserving (offsets stay
    original-line-valid, span content can't fire a boundary); a boundary
    inside the leading list marker or after an abbreviation / ellipsis is
    skipped."""
    masked = PF_BACKTICK.sub(lambda m: ' ' * len(m.group(0)), line)
    mm = SEMBR_MARKER.match(line)
    lead = mm.end() if mm else len(line) - len(line.lstrip())
    points = []
    for m in SEMBR_BOUNDARY.finditer(masked):
        if m.start() < lead:
            continue
        if SEMBR_ABBREV.search(masked[:m.start() + 1]):
            continue
        points.append(m.end())
    return points


def scan_sembr(path, text):
    """Flag multi-sentence prose source lines in one sembr-scoped file — one
    ADVISORY row per offending line; clean → no row (silent, sibling
    convention). Exemptions per the sembr invariant + verbatim-preservation:
    frontmatter, fenced blocks, `|`-table rows, blockquotes, backtick spans."""
    out = []
    for i, line in iter_sembr_lines(text):
        if sembr_split_points(line):
            out.append(("sembr", ADVISORY,
                        f"sembr ADVISORY: {path}:{i} multi-sentence source "
                        f"line — break one sentence per line per sembr "
                        f"invariant"))
    return out


def split_sembr_line(line):
    """Rewrite one flagged line into its sembr form: slice the original line
    at its split points, continuation lines indented to the list-marker width
    (repo convention: text column) or the line's own indent. Returns the new
    line list, None when the line has no boundary (nothing to do), or [] when
    the per-line rejoin-equivalence guard trips — the whitespace-normalized
    join of the rewrite must equal the whitespace-normalized source line, so
    a rewrite can never drop or alter non-space content."""
    points = sembr_split_points(line)
    if not points:
        return None
    mm = SEMBR_MARKER.match(line)
    indent = ' ' * (mm.end() if mm else len(line) - len(line.lstrip()))
    cuts = [0] + points + [len(line)]
    segs = [line[a:b].rstrip() for a, b in zip(cuts, cuts[1:])]
    out = [segs[0]] + [indent + s for s in segs[1:]]
    if ' '.join(' '.join(out).split()) != ' '.join(line.split()):
        return []
    return out


def fix_sembr_text(text):
    """Pure rewrite core for fix-sembr (sembr invariant): split every eligible
    multi-sentence prose line one sentence per line. Returns (new_text,
    rewrites, guard_trips) — rewrites maps source lineno → replacement lines,
    guard_trips lists linenos left untouched by the rejoin-equivalence guard.
    Trailing-newline presence is preserved; exempt lines pass through
    byte-identical."""
    rewrites = {}
    guard_trips = []
    for i, line in iter_sembr_lines(text):
        new = split_sembr_line(line)
        if new is None:
            continue
        if not new:
            guard_trips.append(i)
            continue
        rewrites[i] = new
    if not rewrites:
        return text, rewrites, guard_trips
    out = []
    for i, line in enumerate(text.splitlines(), start=1):
        out.extend(rewrites.get(i, [line]))
    new_text = "\n".join(out) + ("\n" if text.endswith("\n") else "")
    return new_text, rewrites, guard_trips


def audit_sembr(sembr_files):
    """File-reading wrapper (sembr invariant). Emits the multi-sentence-line
    advisory over the sembr-scoped prose file set — realized once here,
    retiring the hand-run line scan."""
    out = []
    for path in sembr_files:
        try:
            txt = read_text(path)
        except OSError:
            continue
        out += scan_sembr(path, txt)
    return out


# --- CLAUDE.md presence + direct-instruction marker block --------------------
# human-clarity invariant: repo-root CLAUDE.md carries the plain-imperative
# restatement of the clarity standard governing chat + human-facing output,
# wrapped in a stable marker block. Symbol-cleanliness rides the human-facing
# scan (CLAUDE.md is in discover_human_facing), realized once per
# mechanical-realization invariant — never re-checked here.

CLAUDE_MD = "CLAUDE.md"
CLAUDE_MARKER_BEGIN = "<!-- sdd:direct-instruction:begin -->"
CLAUDE_MARKER_END = "<!-- sdd:direct-instruction:end -->"


def classify_claude_md(text):
    """CLAUDE.md presence + marker-block audit core (human-clarity invariant) —
    pure, unit-testable without the filesystem. `text` is the file content, or
    None when the file is absent @ repo root. Emits one row: MISSING when the
    carrier is absent, VIOLATE when present but the begin/end marker block is
    absent or mis-ordered (the block the audit anchors on). Present + well-formed
    block → no row (silent, sibling convention). Symbol-cleanliness is NOT
    re-checked — CLAUDE.md rides the human-facing symbol scan
    (mechanical-realization invariant), so a naked symbol surfaces as a `symbols`
    row, not here."""
    if text is None:
        return [("claude-md", "MISSING",
                 f"claude-md MISSING: {CLAUDE_MD} absent @ repo root — "
                 f"human-clarity invariant requires the plain-imperative "
                 f"restatement carrier")]
    b = text.find(CLAUDE_MARKER_BEGIN)
    e = text.find(CLAUDE_MARKER_END)
    if b < 0 or e < 0 or e <= b:
        return [("claude-md", "VIOLATE",
                 f"claude-md VIOLATE: {CLAUDE_MD} missing direct-instruction "
                 f"marker block ({CLAUDE_MARKER_BEGIN} ... {CLAUDE_MARKER_END})")]
    return []


def audit_claude_md(repo_root):
    """File-reading wrapper for the CLAUDE.md presence + marker-block audit
    (human-clarity invariant). Reads repo-root CLAUDE.md (None when absent) and
    delegates to the pure classifier."""
    path = os.path.join(repo_root, CLAUDE_MD)
    text = read_text(path) if os.path.isfile(path) else None
    return classify_claude_md(text)


# --- mechanize pointer -------------------------------------------------------

MECHANIZE_HDR = re.compile(r'^## MECHANIZE\b')
H2_HDR = re.compile(r'^## ')
UI_FALSE = re.compile(r'^user-invocable:\s*false\s*$', re.MULTILINE)
# Pointer must name the shared fragment (path form flexible: plugin-root,
# relative skills/, or bare _fragments/MECHANIZE).
MECHANIZE_PTR = re.compile(r'_fragments/MECHANIZE')


def parse_frontmatter(text):
    """Return the YAML frontmatter block (between the leading `---` fences), or
    '' when absent. Shallow — the audits need only line-presence checks, so the
    flag scan stays scoped to the frontmatter, never a body mention."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return ""
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i])
    return ""


def is_user_invocable(text):
    """A SKILL.md is user-invocable unless its frontmatter declares
    `user-invocable: false` (sub-skill-flags invariant — auto-fire sub-skills are
    flagged false). Frontmatter-only so a body mention of the flag never flips
    the verdict."""
    return UI_FALSE.search(parse_frontmatter(text)) is None


def extract_mechanize_block(text):
    """MECHANIZE section: the `## MECHANIZE` header line through the line before
    the next H2 (or EOF), trailing blank lines trimmed. Returns None when the
    sentinel is absent."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if MECHANIZE_HDR.match(line):
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if H2_HDR.match(lines[j]):
            end = j
            break
    block = lines[start:end]
    while block and block[-1].strip() == "":
        block = block[:-1]
    return "\n".join(block)


def classify_mechanize_blocks(skill_texts):
    """Mechanize-pointer audit core over {path: text} — pure, unit-testable
    without the filesystem (mechanize-scan invariant). User-invocable set =
    input minus frontmatter `user-invocable: false`. Each skill must carry a
    `## MECHANIZE` section that references `skills/_fragments/MECHANIZE`
    (canonical probe text lives once in the fragment). MISSING = no section;
    DRIFT = section present but pointer absent. No multi-file byte-identity."""
    out = []
    for path in sorted(skill_texts):
        txt = skill_texts[path]
        if not is_user_invocable(txt):
            continue
        block = extract_mechanize_block(txt)
        if block is None:
            out.append(("mechanize", "MISSING",
                        f"mechanize MISSING: {path} user-invocable, "
                        f"no MECHANIZE section"))
            continue
        if not MECHANIZE_PTR.search(block):
            out.append(("mechanize", "DRIFT",
                        f"mechanize DRIFT: {path} MECHANIZE section missing "
                        f"pointer to skills/_fragments/MECHANIZE"))
    return out


def audit_mechanize_block(skill_md):
    """File-reading wrapper around classify_mechanize_blocks (mechanize-scan
    invariant). Asserts every user-invocable `skills/*/SKILL.md` points at the
    shared MECHANIZE fragment — realized once here."""
    texts = {}
    for path in skill_md:
        try:
            texts[path] = read_text(path)
        except OSError:
            continue
    return classify_mechanize_blocks(texts)


# --- design-lifecycle post-approve audit --------------------------------------

# Needles the design skill body must carry (design-lifecycle invariant):
# post-approve ! hand-off to github ISSUE (github owns create + --label);
# Next leads `/sdd:spec github issue N`; `fold-design` stays as optional exclusion.
SHAPE_POST_APPROVE_NEEDLES = (
    ("github ISSUE", "hand-off to github ISSUE"),
    ("--label", "class --label hand-off"),
    ("github issue", "/sdd:spec github issue N Next"),
    ("fold-design", "fold-design optional exclusion"),
    ("Effect on in-flight", "ISSUE body Effect"),
    ("Out of scope", "ISSUE body Out of scope"),
    ("Unresolved when present", "ISSUE body Unresolved when present"),
)


def classify_design_post_approve(design_text, github_text=None):
    """design-lifecycle post-approve contract — pure, unit-testable without the
    filesystem. `design_text` is `skills/design/SKILL.md`; empty/unreadable →
    MISSING. Each required needle absent → VIOLATE (one row per miss).
    `github_text` is `skills/github/SKILL.md` ISSUE governor; when passed,
    empty → MISSING and missing `--label` → VIOLATE so the governor cannot
    strip the class label. `github_text is None` skips the governor check
    (design-only fixtures)."""
    out = []
    if not design_text:
        out.append(("design-lifecycle", "MISSING",
                    "design-lifecycle MISSING: skills/design/SKILL.md unreadable"))
    else:
        for needle, what in SHAPE_POST_APPROVE_NEEDLES:
            if needle not in design_text:
                out.append(("design-lifecycle", "VIOLATE",
                            "design-lifecycle VIOLATE: skills/design/SKILL.md "
                            f"missing {what}"))
    if github_text is not None:
        if not github_text:
            out.append(("design-lifecycle", "MISSING",
                        "design-lifecycle MISSING: skills/github/SKILL.md "
                        "unreadable"))
        elif "--label" not in github_text:
            out.append(("design-lifecycle", "VIOLATE",
                        "design-lifecycle VIOLATE: skills/github/SKILL.md "
                        "ISSUE missing --label"))
    return out


def audit_design_post_approve(repo_root):
    """File-reading wrapper around classify_design_post_approve (design-lifecycle
    invariant). Resolves PUBLISHED `skills/design/SKILL.md` and
    `skills/github/SKILL.md` via discover_skill_md — realized once here so the
    drift-detector retires a hand-run post-approve recipe grep."""
    by_name = {}
    for path in discover_skill_md(repo_root):
        by_name[os.path.basename(os.path.dirname(path))] = path
    shape_p = by_name.get("design")
    github_p = by_name.get("github")
    try:
        design_text = read_text(shape_p) if shape_p else ""
    except OSError:
        design_text = ""
    try:
        github_text = read_text(github_p) if github_p else ""
    except OSError:
        github_text = ""
    return classify_design_post_approve(design_text, github_text)


# --- github-workflow PR-per-issue audit --------------------------------------

# Needles the github skill body must carry (github-workflow invariant):
# every worked issue ! issue-linked PR; PR create is `--draft` (no review
# no Closes); PUSH = `git push` issue-linked branch w/ open PR; READY =
# load-and-run review, apply bug + suggestion, then `gh pr ready`.
# No corresponding GitHub issue → no BRANCH, no PR (`gh pr create`).
GITHUB_PR_PER_ISSUE_NEEDLES = (
    ("gh issue develop", "gh issue develop"),
    ("gh pr create --draft", "gh pr create --draft"),
    ("git push", "git push / PUSH"),
    ("load-and-run", "load-and-run review"),
    ("bug + suggestion", "apply bug + suggestion"),
    ("gh pr ready", "gh pr ready"),
    ("chain runs once", "chain runs once"),
    ("No corresponding GitHub issue", "no corresponding GitHub issue"),
    ("no BRANCH, no PR", "no BRANCH, no PR without issue"),
    ("no `gh pr create`", "no gh pr create without issue"),
    ("git switch", "CLOSE git switch before branch -D"),
    ("fold-produced", "post-spec builds fold-produced §T ids"),
    ("implies `--no-chain`", "POST-SPEC-CHILD implies --no-chain"),
    ("Related: #<issue>", "PR body Related: #<issue>"),
    ("push default", "push default branch"),
    ("issue branch", "issue branch"),
    ("--allow-empty", "one non-delta commit (--allow-empty)"),
    ("before the spec delta", "draft PR before the spec delta"),
    ("missing SPEC.md", "missing SPEC.md still opens PR"),
    ("no close trailer", "no close trailer @ create"),
    ("no review-at-create", "no review-at-create"),
)
# Leftover LINEAR / no-PR optional-track wording in the github skill body
# (github-workflow invariant). Substring match; any hit → VIOLATE.
GITHUB_LINEAR_NO_PR_MARKERS = (
    "Optional on the linear solo track",
    "## LINEAR",
    "solo track (no PR)",
)
# READY remainder must not cross-index into another section's numbered steps
# (github-workflow invariant).
READY_CROSS_STEP_RE = re.compile(r'remainder \(step \d+\)', re.I)


def classify_github_pr_per_issue(github_text, frag_text=""):
    """github-workflow PR-per-issue contract — pure, unit-testable without the
    filesystem. `github_text` is `skills/github/SKILL.md`; `frag_text` is
    `skills/_fragments/POST-SPEC-CHAIN.md` (chain needles may live there).
    Empty/unreadable github → MISSING. Each required needle absent from
    github+fragment hay → VIOLATE (one row per miss).
    Leftover LINEAR / no-PR optional-track markers → VIOLATE so the governor
    cannot keep a solo-push exclusion."""
    if not github_text:
        return [("github-workflow", "MISSING",
                 "github-workflow MISSING: skills/github/SKILL.md unreadable")]
    hay = github_text if not frag_text else github_text + "\n" + frag_text
    out = []
    if READY_CROSS_STEP_RE.search(github_text):
        out.append(("github-workflow", "VIOLATE",
                    "github-workflow VIOLATE: skills/github/SKILL.md "
                    "READY remainder cross-section step index"))
    for needle, what in GITHUB_PR_PER_ISSUE_NEEDLES:
        if needle not in hay:
            out.append(("github-workflow", "VIOLATE",
                        "github-workflow VIOLATE: skills/github/SKILL.md "
                        f"missing {what}"))
    for marker in GITHUB_LINEAR_NO_PR_MARKERS:
        if marker in github_text:
            out.append(("github-workflow", "VIOLATE",
                        "github-workflow VIOLATE: skills/github/SKILL.md "
                        f"leftover {marker}"))
    # CLOSE: git switch must precede git branch -D (closes §B.43)
    close_m = re.search(r'(?m)^## CLOSE\b', github_text)
    if close_m:
        close_hay = _md_block_until_h2(github_text, close_m.start())
        sw = close_hay.find("git switch")
        bd = close_hay.find("git branch -D")
        if sw < 0 or bd < 0 or sw > bd:
            out.append(("github-workflow", "VIOLATE",
                        "github-workflow VIOLATE: skills/github/SKILL.md "
                        "CLOSE git switch must precede git branch -D"))
        if not any("gh pr close" in line and "--delete-branch" in line
                   for line in close_hay.splitlines()):
            out.append(("github-workflow", "VIOLATE",
                        "github-workflow VIOLATE: skills/github/SKILL.md "
                        "CLOSE missing gh pr close --delete-branch"))
    return out


def audit_github_pr_per_issue(repo_root):
    """File-reading wrapper around classify_github_pr_per_issue
    (github-workflow invariant). Resolves PUBLISHED `skills/github/SKILL.md`
    via discover_skill_md — realized once here so the drift-detector retires
    a hand-run PR-per-issue recipe grep."""
    by_name = {}
    for path in discover_skill_md(repo_root):
        by_name[os.path.basename(os.path.dirname(path))] = path
    github_p = by_name.get("github")
    try:
        github_text = read_text(github_p) if github_p else ""
    except OSError:
        github_text = ""
    return classify_github_pr_per_issue(github_text,
                                        _read_post_spec_chain(repo_root))


# --- github-workflow bundled review skip (doc-or-comment) --------------------

# Needles the bundled-review recipe must carry (github-workflow invariant):
# skip on a doc-or-comment diff, and still load-and-run review otherwise.
# `doc-or-comment` and `other diffs still run review` must appear in both
# `skills/github/SKILL.md` and `skills/_fragments/POST-SPEC-CHAIN.md`.
# `load-and-run` must remain in the combined hay so a skip-only recipe
# is VIOLATE.
GITHUB_REVIEW_SKIP_NEEDLE = "doc-or-comment"
GITHUB_REVIEW_STILL_NEEDLE = "other diffs still run review"
GITHUB_REVIEW_OTHERWISE_NEEDLE = "load-and-run"


def classify_github_review_skip(github_text, frag_text=""):
    """github-workflow bundled review skip — pure, unit-testable
    without the filesystem. `github_text` is `skills/github/SKILL.md`;
    `frag_text` is `skills/_fragments/POST-SPEC-CHAIN.md`.
    Empty/unreadable github → MISSING. Doc-or-comment skip absent from
    github or from the fragment → VIOLATE. `other diffs still run review`
    absent from either → VIOLATE. `load-and-run` absent from the
    combined hay → VIOLATE (review otherwise). A recipe that names the
    skip and still load-and-runs review is clean."""
    if not github_text:
        return [("github-workflow", "MISSING",
                 "github-workflow MISSING: skills/github/SKILL.md unreadable")]
    out = []
    if GITHUB_REVIEW_SKIP_NEEDLE not in github_text:
        out.append(("github-workflow", "VIOLATE",
                    "github-workflow VIOLATE: skills/github/SKILL.md "
                    "missing doc-or-comment review skip"))
    if GITHUB_REVIEW_SKIP_NEEDLE not in (frag_text or ""):
        out.append(("github-workflow", "VIOLATE",
                    "github-workflow VIOLATE: "
                    "skills/_fragments/POST-SPEC-CHAIN.md "
                    "missing doc-or-comment review skip"))
    if GITHUB_REVIEW_STILL_NEEDLE not in github_text:
        out.append(("github-workflow", "VIOLATE",
                    "github-workflow VIOLATE: skills/github/SKILL.md "
                    "missing other diffs still run review"))
    if GITHUB_REVIEW_STILL_NEEDLE not in (frag_text or ""):
        out.append(("github-workflow", "VIOLATE",
                    "github-workflow VIOLATE: "
                    "skills/_fragments/POST-SPEC-CHAIN.md "
                    "missing other diffs still run review"))
    hay = github_text if not frag_text else github_text + "\n" + frag_text
    if GITHUB_REVIEW_OTHERWISE_NEEDLE not in hay:
        out.append(("github-workflow", "VIOLATE",
                    "github-workflow VIOLATE: skills/github/SKILL.md "
                    "missing load-and-run review otherwise"))
    return out


def audit_github_review_skip(repo_root):
    """File-reading wrapper around classify_github_review_skip
    (github-workflow invariant). Resolves PUBLISHED
    `skills/github/SKILL.md` via discover_skill_md — realized once here
    so the drift-detector retires a hand-run review-skip grep."""
    by_name = {}
    for path in discover_skill_md(repo_root):
        by_name[os.path.basename(os.path.dirname(path))] = path
    github_p = by_name.get("github")
    try:
        github_text = read_text(github_p) if github_p else ""
    except OSError:
        github_text = ""
    return classify_github_review_skip(github_text,
                                       _read_post_spec_chain(repo_root))


# --- github-workflow spec FOLD-IN github issue audit -------------------------

# Needles the spec skill FOLD-IN github-issue path must carry (github-workflow
# invariant): before the spec delta, push default branch, issue branch,
# one non-delta `--allow-empty` commit, then `gh pr create --draft`
# with `Related: #<issue>` (missing SPEC.md still opens the PR; no close
# trailer; no review-at-create). Spec stops before the chain. Spec-side
# cites the three-step chain (`/sdd:build` + READY remainder) not a
# two-step subset (closes §B.36). The before-spec-delta block must not
# run `/sdd:build` or load POST-SPEC-CHAIN (numbered or not);
# POST-APPLY must not `auto-chain run` (closes §B.35, §B.77).
SPEC_FOLD_GITHUB_NEEDLES = (
    ("push default", "push default branch"),
    ("gh issue develop", "issue branch via gh issue develop"),
    ("--allow-empty", "one non-delta commit (--allow-empty)"),
    ("Related: #<issue>", "draft Related: #<issue>"),
    ("before the spec delta", "draft PR before the spec delta"),
    ("missing SPEC.md", "missing SPEC.md still opens PR"),
    ("gh pr create --draft", "gh pr create --draft"),
    ("no close trailer", "no close trailer @ create"),
    ("no review-at-create", "no review-at-create"),
    ("/sdd:build", "post-spec-commit `/sdd:build` cite"),
    ("READY remainder", "three-step READY remainder cite"),
    ("stops before the chain", "spec stops before the chain"),
    ("no github BRANCH, no github PR",
     "non-issue APPLY no BRANCH no PR"),
)
SPEC_POST_APPLY_AUTOCHAIN = "auto-chain run"


def _read_post_spec_chain(repo_root):
    """Read `skills/_fragments/POST-SPEC-CHAIN.md` or '' if missing."""
    p = os.path.join(repo_root, "skills", "_fragments", "POST-SPEC-CHAIN.md")
    try:
        return read_text(p) if os.path.isfile(p) else ""
    except OSError:
        return ""


def _md_block_until_h2(text, start_idx):
    """Slice from start_idx to the next `## ` heading (exclusive)."""
    return _md_block_until_heading(text, start_idx, "## ")


def _md_block_until_h3(text, start_idx):
    """Slice from start_idx to the next `# `, `## `, or `### ` heading."""
    return _md_block_until_heading(text, start_idx, ("# ", "## ", "### "))


def _md_block_until_heading(text, start_idx, prefixes):
    """Slice from start_idx to the next heading with one of `prefixes`."""
    if isinstance(prefixes, str):
        prefixes = (prefixes,)
    rest = text[start_idx:]
    lines = rest.splitlines()
    if not lines:
        return ""
    out = [lines[0]]
    for line in lines[1:]:
        if line.startswith(prefixes):
            break
        out.append(line)
    return "\n".join(out)


def classify_spec_fold_github(spec_text):
    """github-workflow spec FOLD-IN github-issue contract — pure,
    unit-testable without the filesystem. `spec_text` is
    `skills/spec/SKILL.md`; empty/unreadable → MISSING. Each required
    needle absent → VIOLATE (one row per miss). Before spec delta
    `/sdd:build` or `POST-SPEC-CHAIN.md` (numbered or not) or
    POST-APPLY `auto-chain run` → VIOLATE so the chain cannot run
    twice (closes §B.35, §B.77)."""
    if not spec_text:
        return [("github-workflow", "MISSING",
                 "github-workflow MISSING: skills/spec/SKILL.md unreadable")]
    out = []
    for needle, what in SPEC_FOLD_GITHUB_NEEDLES:
        if needle not in spec_text:
            out.append(("github-workflow", "VIOLATE",
                        "github-workflow VIOLATE: skills/spec/SKILL.md "
                        f"missing {what}"))
    before_m = re.search(
        r'(?m)^\*\*(?:Before spec delta|After OK)\*\*', spec_text)
    if before_m:
        # Stop at the next heading (# through ###). A later ### list may
        # name `/sdd:build` without running it (Acceptance fold note).
        before = _md_block_until_h3(spec_text, before_m.start())
        for line in before.splitlines():
            if "/sdd:build" in line or "POST-SPEC-CHAIN.md" in line:
                out.append(("github-workflow", "VIOLATE",
                            "github-workflow VIOLATE: skills/spec/SKILL.md "
                            "Before spec delta runs the post-spec chain "
                            "(spec stops before the chain)"))
                break
    post_m = re.search(r'(?m)^## POST-APPLY\b', spec_text)
    if post_m:
        post_apply = _md_block_until_h2(spec_text, post_m.start())
        if SPEC_POST_APPLY_AUTOCHAIN in post_apply:
            out.append(("github-workflow", "VIOLATE",
                        "github-workflow VIOLATE: skills/spec/SKILL.md "
                        "POST-APPLY auto-chain run "
                        "(chain must run once)"))
    return out


def audit_spec_fold_github(repo_root):
    """File-reading wrapper around classify_spec_fold_github
    (github-workflow invariant). Resolves PUBLISHED `skills/spec/SKILL.md`
    via discover_skill_md — realized once here so the drift-detector retires
    a hand-run spec-fold recipe grep."""
    by_name = {}
    for path in discover_skill_md(repo_root):
        by_name[os.path.basename(os.path.dirname(path))] = path
    spec_p = by_name.get("spec")
    try:
        spec_text = read_text(spec_p) if spec_p else ""
    except OSError:
        spec_text = ""
    return classify_spec_fold_github(spec_text)


# --- github-workflow build issue-linked pass audit ---------------------------

# Needles the build skill issue-linked pass must carry (github-workflow
# invariant): github PUSH then load-and-run review-apply + `gh pr ready`;
# Next merge when approved. Close trailer stays off the build commit.
# Acceptance-gate detector = issue linkage not planned close trailer;
# ALLOW @ build = evidence sufficient (closes B37).
BUILD_ISSUE_LINKED_NEEDLES = (
    ("github PUSH", "github PUSH"),
    ("load-and-run", "load-and-run review-apply"),
    ("gh pr ready", "gh pr ready"),
    ("merge when approved", "Next merge when approved"),
    ("issue linkage", "acceptance-gate detector issue linkage"),
    ("evidence sufficient", "ALLOW @ build = evidence sufficient"),
)


def classify_build_issue_linked(build_text):
    """github-workflow build issue-linked pass contract — pure,
    unit-testable without the filesystem. `build_text` is
    `skills/build/SKILL.md`; empty/unreadable → MISSING. Each required
    needle absent → VIOLATE (one row per miss)."""
    if not build_text:
        return [("github-workflow", "MISSING",
                 "github-workflow MISSING: skills/build/SKILL.md unreadable")]
    out = []
    for needle, what in BUILD_ISSUE_LINKED_NEEDLES:
        if needle not in build_text:
            out.append(("github-workflow", "VIOLATE",
                        "github-workflow VIOLATE: skills/build/SKILL.md "
                        f"missing {what}"))
    return out


def audit_build_issue_linked(repo_root):
    """File-reading wrapper around classify_build_issue_linked
    (github-workflow invariant). Resolves PUBLISHED `skills/build/SKILL.md`
    via discover_skill_md — realized once here so the drift-detector retires
    a hand-run build issue-linked recipe grep."""
    by_name = {}
    for path in discover_skill_md(repo_root):
        by_name[os.path.basename(os.path.dirname(path))] = path
    build_p = by_name.get("build")
    try:
        build_text = read_text(build_p) if build_p else ""
    except OSError:
        build_text = ""
    return classify_build_issue_linked(build_text)


# Needles CHAIN + NEXT + build must carry for issue-linked READY
# (recipe-step-no-dispatch + response-shape + github-workflow;
# closes B63): no check hop; Next item #1 = merge phrasing;
# `/sdd:check` listed not hopped.
CHAIN_ISSUE_LINKED_READY_NEEDLES = (
    ("issue-linked READY", "issue-linked READY"),
    ("no check hop", "no check hop"),
    ("listed not hopped", "/sdd:check listed not hopped"),
)
NEXT_ISSUE_LINKED_READY_NEEDLES = (
    ("item #1", "Next item #1 = merge phrasing"),
    ("listed not hopped", "/sdd:check listed not hopped"),
)
BUILD_ISSUE_LINKED_READY_CHAIN_NEEDLES = (
    ("issue-linked READY", "issue-linked READY skips check hop"),
    ("no check hop", "no check hop"),
    ("listed not hopped", "/sdd:check listed not hopped"),
)


def classify_issue_linked_ready_chain(chain_text, next_text, build_text):
    """issue-linked READY skips green-path check hop — pure,
    unit-testable without the filesystem (closes B63).
    `chain_text` is `skills/_fragments/CHAIN.md`; `next_text` is
    `skills/_fragments/NEXT.md`; `build_text` is
    `skills/build/SKILL.md`. Empty/unreadable → MISSING. Each
    required needle absent → VIOLATE (one row per miss)."""
    out = []
    if not chain_text:
        out.append(("github-workflow", "MISSING",
                    "github-workflow MISSING: "
                    "skills/_fragments/CHAIN.md unreadable"))
    else:
        for needle, what in CHAIN_ISSUE_LINKED_READY_NEEDLES:
            if needle not in chain_text:
                out.append(("github-workflow", "VIOLATE",
                            "github-workflow VIOLATE: "
                            "skills/_fragments/CHAIN.md "
                            f"missing {what}"))
    if not next_text:
        out.append(("github-workflow", "MISSING",
                    "github-workflow MISSING: "
                    "skills/_fragments/NEXT.md unreadable"))
    else:
        for needle, what in NEXT_ISSUE_LINKED_READY_NEEDLES:
            if needle not in next_text:
                out.append(("github-workflow", "VIOLATE",
                            "github-workflow VIOLATE: "
                            "skills/_fragments/NEXT.md "
                            f"missing {what}"))
    if not build_text:
        out.append(("github-workflow", "MISSING",
                    "github-workflow MISSING: skills/build/SKILL.md "
                    "unreadable"))
    else:
        for needle, what in BUILD_ISSUE_LINKED_READY_CHAIN_NEEDLES:
            if needle not in build_text:
                out.append(("github-workflow", "VIOLATE",
                            "github-workflow VIOLATE: "
                            "skills/build/SKILL.md "
                            f"missing {what}"))
    return out


def audit_issue_linked_ready_chain(repo_root):
    """File-reading wrapper around classify_issue_linked_ready_chain
    (github-workflow invariant; closes B63). Resolves PUBLISHED
    CHAIN + NEXT fragments and `skills/build/SKILL.md` — realized
    once here so the drift-detector retires a hand-run hop-skip grep."""
    chain_p = os.path.join(repo_root, "skills", "_fragments", "CHAIN.md")
    next_p = os.path.join(repo_root, "skills", "_fragments", "NEXT.md")
    try:
        chain_text = read_text(chain_p) if os.path.isfile(chain_p) else ""
    except OSError:
        chain_text = ""
    try:
        next_text = read_text(next_p) if os.path.isfile(next_p) else ""
    except OSError:
        next_text = ""
    by_name = {}
    for path in discover_skill_md(repo_root):
        by_name[os.path.basename(os.path.dirname(path))] = path
    build_p = by_name.get("build")
    try:
        build_text = read_text(build_p) if build_p else ""
    except OSError:
        build_text = ""
    return classify_issue_linked_ready_chain(chain_text, next_text,
                                             build_text)


# Needles the ACCEPTANCE-GATE fragment + github skill must carry with build
# (github-workflow invariant; closes B37): detector = issue linkage not
# planned close trailer; ALLOW @ build = evidence sufficient; close trailer
# MERGE-only.
ACCEPTANCE_GATE_DETECT_NEEDLES = (
    ("issue linkage", "detector issue linkage not close trailer"),
    ("evidence sufficient", "ALLOW @ build = evidence sufficient"),
    ("MERGE-only", "close trailer MERGE-only"),
)


GITHUB_ACCEPTANCE_GATE_PTR = "ACCEPTANCE-GATE.md"


def classify_acceptance_gate_detect(frag_text, github_text):
    """github-workflow acceptance-gate detector contract — pure,
    unit-testable without the filesystem (closes B37). `frag_text` is
    `skills/_fragments/ACCEPTANCE-GATE.md` (needles live here);
    `github_text` is `skills/github/SKILL.md` (load-only pointer).
    Empty/unreadable → MISSING. Fragment missing a needle → VIOLATE.
    Github missing the fragment pointer → VIOLATE."""
    out = []
    if not frag_text:
        out.append(("github-workflow", "MISSING",
                    "github-workflow MISSING: "
                    "skills/_fragments/ACCEPTANCE-GATE.md unreadable"))
    else:
        for needle, what in ACCEPTANCE_GATE_DETECT_NEEDLES:
            if needle not in frag_text:
                out.append(("github-workflow", "VIOLATE",
                            "github-workflow VIOLATE: "
                            "skills/_fragments/ACCEPTANCE-GATE.md "
                            f"missing {what}"))
    if not github_text:
        out.append(("github-workflow", "MISSING",
                    "github-workflow MISSING: skills/github/SKILL.md "
                    "unreadable"))
    elif GITHUB_ACCEPTANCE_GATE_PTR not in github_text:
        out.append(("github-workflow", "VIOLATE",
                    "github-workflow VIOLATE: "
                    "skills/github/SKILL.md "
                    "missing ACCEPTANCE-GATE.md pointer"))
    return out


def audit_acceptance_gate_detect(repo_root):
    """File-reading wrapper around classify_acceptance_gate_detect
    (github-workflow invariant). Resolves PUBLISHED fragment + github
    skill — realized once here so the drift-detector retires a hand-run
    acceptance-gate detector grep."""
    frag_p = os.path.join(repo_root, "skills", "_fragments",
                          "ACCEPTANCE-GATE.md")
    try:
        frag_text = read_text(frag_p) if os.path.isfile(frag_p) else ""
    except OSError:
        frag_text = ""
    by_name = {}
    for path in discover_skill_md(repo_root):
        by_name[os.path.basename(os.path.dirname(path))] = path
    github_p = by_name.get("github")
    try:
        github_text = read_text(github_p) if github_p else ""
    except OSError:
        github_text = ""
    return classify_acceptance_gate_detect(frag_text, github_text)


# Needles condense prong 6 must carry (token-budget invariant): consume
# stub-skip from the v-weights table; no re-extract of already-stubbed rows.
CONDENSE_PRONG6_NEEDLES = (
    ("stub-skip", "consume stub-skip from table"),
    ("no re-extract", "no re-extract already-stubbed rows"),
)


def classify_condense_stub_skip(condense_text):
    """token-budget condense prong-6 stub-skip contract — pure,
    unit-testable without the filesystem. `condense_text` is
    `skills/condense/SKILL.md`; empty/unreadable → MISSING. Each
    required needle absent → VIOLATE (one row per miss)."""
    if not condense_text:
        return [("token", "MISSING",
                 "token MISSING: skills/condense/SKILL.md unreadable")]
    out = []
    for needle, what in CONDENSE_PRONG6_NEEDLES:
        if needle not in condense_text:
            out.append(("token", "VIOLATE",
                        "token VIOLATE: skills/condense/SKILL.md "
                        f"missing {what}"))
    return out


def audit_condense_stub_skip(repo_root):
    """File-reading wrapper around classify_condense_stub_skip
    (token-budget invariant). Resolves PUBLISHED
    `skills/condense/SKILL.md` via discover_skill_md — realized once
    here so the drift-detector retires a hand-run prong-6 consume grep."""
    by_name = {}
    for path in discover_skill_md(repo_root):
        by_name[os.path.basename(os.path.dirname(path))] = path
    condense_p = by_name.get("condense")
    try:
        condense_text = read_text(condense_p) if condense_p else ""
    except OSError:
        condense_text = ""
    return classify_condense_stub_skip(condense_text)


# --- write-serialize review scratch-write audit (closes §B.37) ---------------

# Needles the github post-spec review spawn must carry (write-serialize
# invariant): scratch writes only, no repo edits; spawn uses a
# general-purpose Agent, not read-only Explore, so the bundled review child
# can write its scratch file.
REVIEW_SCRATCH_NEEDLES = (
    ("scratch writes", "review scratch writes"),
    ("general-purpose Agent, not read-only Explore",
     "spawn general-purpose Agent, not read-only Explore"),
)


def classify_review_scratch_write(github_text, frag_text=""):
    """write-serialize post-spec review spawn contract — pure,
    unit-testable without the filesystem. `github_text` is
    `skills/github/SKILL.md`; `frag_text` is
    `skills/_fragments/POST-SPEC-CHAIN.md` (spawn recipe may live
    there). Empty/unreadable github → MISSING. Each required
    needle absent from github+fragment hay → VIOLATE (one row per
    miss). Closes §B.37."""
    if not github_text:
        return [("write-serialize", "MISSING",
                 "write-serialize MISSING: skills/github/SKILL.md unreadable")]
    out = []
    combined = github_text if not frag_text else github_text + "\n" + frag_text
    hay = combined.lower()
    for needle, what in REVIEW_SCRATCH_NEEDLES:
        if needle.lower() not in hay:
            out.append(("write-serialize", "VIOLATE",
                        "write-serialize VIOLATE: skills/github/SKILL.md "
                        f"missing {what}"))
    return out


def audit_review_scratch_write(repo_root):
    """File-reading wrapper around classify_review_scratch_write
    (write-serialize invariant). Resolves PUBLISHED `skills/github/SKILL.md`
    via discover_skill_md — realized once here so the drift-detector retires
    a hand-run review-spawn grep."""
    by_name = {}
    for path in discover_skill_md(repo_root):
        by_name[os.path.basename(os.path.dirname(path))] = path
    github_p = by_name.get("github")
    try:
        github_text = read_text(github_p) if github_p else ""
    except OSError:
        github_text = ""
    return classify_review_scratch_write(github_text,
                                         _read_post_spec_chain(repo_root))


# --- github-workflow POST-SPEC-CHILD discriminator (closes §B.38) ------------

# Needles the post-spec build child must carry (github-workflow +
# write-serialize): spawn prompt sets `POST-SPEC-CHILD=1`; build LOAD
# treats that token as the child discriminator → PUSH only, drop READY.
POST_SPEC_CHILD_TOKEN = "POST-SPEC-CHILD=1"


def classify_post_spec_child(build_text, github_text, frag_text=""):
    """POST-SPEC-CHILD=1 discriminator contract — pure, unit-testable
    without the filesystem (github-workflow + write-serialize; closes
    §B.38). `build_text` is `skills/build/SKILL.md`; `github_text` is
    `skills/github/SKILL.md`; `frag_text` is
    `skills/_fragments/POST-SPEC-CHAIN.md` (spawn token may live
    there). Empty/unreadable file → MISSING. Token absent from
    build, or from github+fragment hay → VIOLATE."""
    out = []
    if not build_text:
        out.append(("github-workflow", "MISSING",
                    "github-workflow MISSING: skills/build/SKILL.md "
                    "unreadable"))
    elif POST_SPEC_CHILD_TOKEN not in build_text:
        out.append(("github-workflow", "VIOLATE",
                    "github-workflow VIOLATE: skills/build/SKILL.md "
                    "missing POST-SPEC-CHILD=1"))
    gh_hay = github_text if not frag_text else github_text + "\n" + frag_text
    if not github_text:
        out.append(("github-workflow", "MISSING",
                    "github-workflow MISSING: skills/github/SKILL.md "
                    "unreadable"))
    elif POST_SPEC_CHILD_TOKEN not in gh_hay:
        out.append(("github-workflow", "VIOLATE",
                    "github-workflow VIOLATE: skills/github/SKILL.md "
                    "missing POST-SPEC-CHILD=1"))
    return out


def audit_post_spec_child(repo_root):
    """File-reading wrapper around classify_post_spec_child
    (github-workflow invariant). Resolves PUBLISHED build + github
    skill bodies via discover_skill_md — realized once here so the
    drift-detector retires a hand-run POST-SPEC-CHILD grep."""
    by_name = {}
    for path in discover_skill_md(repo_root):
        by_name[os.path.basename(os.path.dirname(path))] = path
    build_p = by_name.get("build")
    github_p = by_name.get("github")
    try:
        build_text = read_text(build_p) if build_p else ""
    except OSError:
        build_text = ""
    try:
        github_text = read_text(github_p) if github_p else ""
    except OSError:
        github_text = ""
    return classify_post_spec_child(build_text, github_text,
                                    _read_post_spec_chain(repo_root))


# --- github-workflow README Issue-linked PR audit ----------------------------

# Needles the README Issue-linked PR section must carry (github-workflow +
# github-facing-register invariants): branch then spec commit then draft PR;
# build then review-apply then `gh pr ready`; Closes only at merge after
# acceptance-gate; squash commit message holds `#<issue>` (closes §B.39);
# doc-or-comment review skip.
README_ISSUE_LINKED_NEEDLES = (
    ("gh pr create --draft", "branch then spec commit then draft PR"),
    ("gh pr ready", "review-apply then gh pr ready"),
    ("only at merge", "Closes only at merge after acceptance-gate"),
    ("No corresponding GitHub issue",
     "no corresponding GitHub issue → no branch/PR"),
    ("no git branch, no GitHub PR", "no git branch, no GitHub PR"),
    ("#<issue>", "squash commit message holds #<issue>"),
    ("fold-produced", "post-spec fold-produced §T ids"),
    ("doc-or-comment", "doc-or-comment review skip"),
)
README_POST_SPEC_ALL_BAN = "/sdd:build --all"


def classify_readme_issue_linked(readme_text):
    """github-workflow README Issue-linked PR contract — pure,
    unit-testable without the filesystem. `readme_text` is README.md;
    empty/unreadable → MISSING. Each required needle absent → VIOLATE
    (one row per miss)."""
    if not readme_text:
        return [("github-workflow", "MISSING",
                 "github-workflow MISSING: README.md unreadable")]
    out = []
    for needle, what in README_ISSUE_LINKED_NEEDLES:
        if needle not in readme_text:
            out.append(("github-workflow", "VIOLATE",
                        "github-workflow VIOLATE: README.md "
                        f"missing {what}"))
    if README_POST_SPEC_ALL_BAN in readme_text:
        out.append(("github-workflow", "VIOLATE",
                    "github-workflow VIOLATE: README.md "
                    "post-spec `/sdd:build --all` "
                    "(fold-produced §T ids only)"))
    return out


def audit_readme_issue_linked(repo_root):
    """File-reading wrapper around classify_readme_issue_linked
    (github-workflow invariant). Resolves REPO-LOCAL README.md —
    realized once here so the drift-detector retires a hand-run
    README Issue-linked PR grep."""
    path = os.path.join(repo_root, "README.md")
    try:
        text = read_text(path) if os.path.isfile(path) else ""
    except OSError:
        text = ""
    return classify_readme_issue_linked(text)


# --- github-workflow MERGE squash subject (closes §B.39) ---------------------

# Needles the github MERGE recipe must carry (github-workflow invariant):
# `gh pr merge --squash --subject` and the subject holds `#<issue>` (the
# linked issue, not merely PR). GitHub default subject PR title `(#PR)`
# is insufficient — `Closes #<issue>` on the PR body does not put the
# issue number in the squash commit subject (closes §B.39).
GITHUB_MERGE_SUBJECT_NEEDLE = "--subject"
GITHUB_MERGE_ISSUE_NEEDLE = "#<issue>"


def classify_github_merge_subject(github_text):
    """github-workflow MERGE squash subject contract — pure, unit-testable
    without the filesystem (closes §B.39). `github_text` is
    `skills/github/SKILL.md`; empty/unreadable → MISSING. MERGE block
    (else whole body) must carry `--subject`. The `--subject` line must
    also carry `#<issue>` so a `(#PR)`-only subject is VIOLATE even when
    `Closes #<issue>` sits on another line."""
    if not github_text:
        return [("github-workflow", "MISSING",
                 "github-workflow MISSING: skills/github/SKILL.md unreadable")]
    merge_m = re.search(r'(?m)^## MERGE\b', github_text)
    hay = (_md_block_until_h2(github_text, merge_m.start())
           if merge_m else github_text)
    out = []
    if GITHUB_MERGE_SUBJECT_NEEDLE not in hay:
        out.append(("github-workflow", "VIOLATE",
                    "github-workflow VIOLATE: skills/github/SKILL.md "
                    "MERGE missing --subject"))
    elif not any(GITHUB_MERGE_SUBJECT_NEEDLE in line
                 and GITHUB_MERGE_ISSUE_NEEDLE in line
                 for line in hay.splitlines()):
        out.append(("github-workflow", "VIOLATE",
                    "github-workflow VIOLATE: skills/github/SKILL.md "
                    "MERGE squash subject holds #<issue> (not merely PR)"))
    return out


# MERGE check-probe needles (github-workflow invariant; closes §B.72):
# `gh pr checks` + `reviewDecision,mergeable` in the MERGE block.
GITHUB_MERGE_PROBE_NEEDLES = (
    ("gh pr checks", "MERGE gh pr checks probe"),
    ("reviewDecision,mergeable", "MERGE reviewDecision,mergeable probe"),
)


def classify_github_merge_probe(github_text):
    """github-workflow MERGE check-probe contract — pure, unit-testable
    without the filesystem (closes §B.72). `github_text` is
    `skills/github/SKILL.md`; empty/unreadable → MISSING. MERGE block
    (else whole body) must carry `gh pr checks` and
    `reviewDecision,mergeable`."""
    if not github_text:
        return [("github-workflow", "MISSING",
                 "github-workflow MISSING: skills/github/SKILL.md unreadable")]
    merge_m = re.search(r'(?m)^## MERGE\b', github_text)
    hay = (_md_block_until_h2(github_text, merge_m.start())
           if merge_m else github_text)
    out = []
    for needle, what in GITHUB_MERGE_PROBE_NEEDLES:
        if needle not in hay:
            out.append(("github-workflow", "VIOLATE",
                        "github-workflow VIOLATE: skills/github/SKILL.md "
                        f"missing {what}"))
    return out


def audit_github_merge_probe(repo_root):
    """File-reading wrapper around classify_github_merge_probe
    (github-workflow invariant). Resolves PUBLISHED
    `skills/github/SKILL.md` via discover_skill_md — realized once here
    so the drift-detector retires a hand-run MERGE-probe grep."""
    by_name = {}
    for path in discover_skill_md(repo_root):
        by_name[os.path.basename(os.path.dirname(path))] = path
    github_p = by_name.get("github")
    try:
        github_text = read_text(github_p) if github_p else ""
    except OSError:
        github_text = ""
    return classify_github_merge_probe(github_text)


def audit_github_merge_subject(repo_root):
    """File-reading wrapper around classify_github_merge_subject
    (github-workflow invariant). Resolves PUBLISHED
    `skills/github/SKILL.md` via discover_skill_md — realized once here
    so the drift-detector retires a hand-run MERGE-subject grep."""
    by_name = {}
    for path in discover_skill_md(repo_root):
        by_name[os.path.basename(os.path.dirname(path))] = path
    github_p = by_name.get("github")
    try:
        github_text = read_text(github_p) if github_p else ""
    except OSError:
        github_text = ""
    return classify_github_merge_subject(github_text)


# --- github-workflow READY remainder + fold ids (closes §B.69–§B.71, §B.74)

# Needles the github skill must carry (github-workflow invariant):
# post-spec READY remainder no wait; fold-produced ids include existing
# `.` rows that received Acceptance notes; READY re-runs task verify
# before `gh pr ready`; child-fail posts `gh pr comment`.
GITHUB_READY_REMAINDER_NEEDLES = (
    ("no wait", "READY remainder no wait"),
    ("Acceptance notes", "fold-produced Acceptance notes"),
    ("re-run task verify", "READY re-run task verify"),
    ("gh pr comment", "child-fail gh pr comment"),
)


def classify_github_ready_remainder(github_text, frag_text=""):
    """github-workflow READY remainder + fold-produced Acceptance-notes
    contract — pure, unit-testable without the filesystem (closes
    §B.69, §B.70, §B.71, §B.74). `github_text` is
    `skills/github/SKILL.md`; `frag_text` is
    `skills/_fragments/POST-SPEC-CHAIN.md` (fold-produced Acceptance
    notes + `gh pr comment` may live there). Empty/unreadable github →
    MISSING. Each required needle absent from github+fragment hay →
    VIOLATE (one row per miss)."""
    if not github_text:
        return [("github-workflow", "MISSING",
                 "github-workflow MISSING: skills/github/SKILL.md unreadable")]
    hay = github_text if not frag_text else github_text + "\n" + frag_text
    out = []
    for needle, what in GITHUB_READY_REMAINDER_NEEDLES:
        if needle not in hay:
            out.append(("github-workflow", "VIOLATE",
                        "github-workflow VIOLATE: skills/github/SKILL.md "
                        f"missing {what}"))
    return out


def audit_github_ready_remainder(repo_root):
    """File-reading wrapper around classify_github_ready_remainder
    (github-workflow invariant). Resolves PUBLISHED
    `skills/github/SKILL.md` via discover_skill_md — realized once here
    so the drift-detector retires a hand-run READY-remainder grep."""
    by_name = {}
    for path in discover_skill_md(repo_root):
        by_name[os.path.basename(os.path.dirname(path))] = path
    github_p = by_name.get("github")
    try:
        github_text = read_text(github_p) if github_p else ""
    except OSError:
        github_text = ""
    return classify_github_ready_remainder(github_text,
                                           _read_post_spec_chain(repo_root))


# --- leftover LINEAR-no-PR wording audit -------------------------------------

# Sweep-scope grep from §T.73 (github-workflow invariant): remaining
# LINEAR / solo-linear / no-PR-required wording on human + skill surfaces.
LINEAR_NO_PR_RE = re.compile(r"LINEAR|solo linear|no PR required")


def classify_linear_no_pr(texts):
    """Leftover LINEAR-no-PR wording — pure, unit-testable without the
    filesystem (github-workflow invariant). `texts` is {path: text} over
    skill bodies, fragments, README, CLAUDE.md. SPEC.md excluded (the sweep
    §T row names the pattern). Backtick-wrapped tokens exempt per the
    verbatim-preservation invariant. One VIOLATE row per matching line."""
    out = []
    for path in sorted(texts):
        for i, line in enumerate(texts[path].splitlines(), start=1):
            if LINEAR_NO_PR_RE.search(strip_backticks(line)):
                out.append(("linear-no-pr", "VIOLATE",
                            f"linear-no-pr VIOLATE: {path}:{i} leftover "
                            f"LINEAR-no-PR wording"))
    return out


def audit_linear_no_pr(repo_root):
    """File-reading wrapper around classify_linear_no_pr (github-workflow
    invariant). Scope = PUBLISHED skill bodies + `_fragments` + README +
    CLAUDE.md — realized once here so the sweep-scope grep cannot silently
    re-accumulate. SPEC.md is out of scope (the live §T row documents the
    pattern)."""
    texts = {}
    paths = list(discover_skill_md(repo_root))
    paths += discover_sembr_fragments(repo_root)
    for name in ("README.md", "CLAUDE.md"):
        p = os.path.join(repo_root, name)
        if os.path.isfile(p):
            paths.append(p)
    for path in paths:
        try:
            texts[path] = read_text(path)
        except OSError:
            continue
    return classify_linear_no_pr(texts)


# --- dispatch-target audit ---------------------------------------------------


def classify_dispatch_targets(skill_texts, plugins, subskills):
    """Dispatch-target audit core over {path: text} — pure, unit-testable
    without the filesystem (response-shape + sub-skill-flags invariants, closes
    §B.14). No skill body may slash-dispatch an auto-fire sub-skill: the slash
    form `/<plugin>:<sub-skill>` names a dispatch target, but auto-fire
    sub-skills are `user-invocable: false` so are never a valid dispatch (the
    bug→spec route is `/<plugin>:spec <intent>`, never the sub-skill slash form).
    `plugins` = manifest plugin names (plugin-shape invariant — never assumed
    equal to a dir name), `subskills` = auto-fire sub-skill dir names
    (frontmatter `user-invocable: false`). Backtick-wrapped tokens exempt per the
    verbatim-preservation invariant — code-span prose documenting the banned form
    is fine; a live non-backtick slash form is VIOLATE, one row per hit,
    line-numbered. Empty plugin or sub-skill set → no audit (nothing to match)."""
    out = []
    if not plugins or not subskills:
        return out
    pat = re.compile(r'/(?:' + '|'.join(re.escape(p) for p in sorted(plugins))
                     + r'):(?:'
                     + '|'.join(re.escape(s) for s in sorted(subskills))
                     + r')\b')
    for path in sorted(skill_texts):
        for i, line in enumerate(skill_texts[path].splitlines(), start=1):
            for m in pat.finditer(strip_backticks(line)):
                out.append(("dispatch", "VIOLATE",
                            f"dispatch VIOLATE: {path}:{i} slash-dispatches "
                            f"auto-fire sub-skill {m.group(0)} "
                            f"(never user-invocable)"))
    return out


def classify_dispatch_targets_from_texts(skill_texts, plugins):
    """Derive the auto-fire sub-skill set from {path: text} then run the
    dispatch-target audit — pure, unit-testable without the filesystem. The
    sub-skill set is the skills whose frontmatter declares `user-invocable: false`
    (frontmatter-only — a body prose mention of the flag never enrolls a
    user-invocable skill); the dir name (`skills/<name>/SKILL.md`) is the banned
    dispatch target."""
    subskills = {os.path.basename(os.path.dirname(p))
                 for p, t in skill_texts.items() if not is_user_invocable(t)}
    return classify_dispatch_targets(skill_texts, plugins, subskills)


def audit_dispatch_targets(skill_md, plugins):
    """File-reading wrapper around classify_dispatch_targets_from_texts
    (response-shape + sub-skill-flags invariants, closes §B.14). Realized once
    here so the drift-detector retires its hand-run skill-body slash grep — the
    sub-skill set is derived frontmatter-only and the plugin name from the
    manifest, where a hand grep would over-match a prose mention of the flag."""
    texts = {}
    for path in skill_md:
        try:
            texts[path] = read_text(path)
        except OSError:
            continue
    return classify_dispatch_targets_from_texts(texts, plugins)


# --- allowed-tools grant-use audit -------------------------------------------

# Per-tool body-reference set (tooling-preference invariant: a frontmatter grant
# pre-approves a body-prescribed tool invocation, so a granted tool the body never
# invokes is banned — nothing to pre-approve). SOUND by construction: a grant is
# flagged only when the body carries NO reference of any kind — the canonical
# token, an alias (Explore for the sub-agent spawner), the operation verb a body
# uses in place of the tool name (skills name operations: "rewrite" for the editor,
# "spawn" for the agent), or (Bash) a command anchor. Generous sets never
# false-positive a genuine use; the accepted cost is a false negative on a tool
# whose reference word saturates every body (the skill-dispatcher — "skill" is
# ubiquitous). The wildcard-pattern tool matches case-sensitively so wildcard prose
# ("mid-glob") never masks a missing grant for it.

GRANT_REFERENCE = {
    "Read": [(r'\bread|\bload\b', re.I)],
    "Edit": [(r'\bedit|\brewrite|\bpatch\b|\bprune|\btrim|\brenumber|\boverwrite',
              re.I)],
    "Write": [(r'\bwrite', re.I)],
    "Grep": [(r'\bgrep', re.I)],
    "Glob": [(r'\bGlob\b', 0)],                         # case-sensitive: prose-safe
    "Agent": [(r'\bagent|\bExplore\b|subagent', re.I)],
    "Skill": [(r'\bskill', re.I)],                       # generous (accepted limit)
    "TaskCreate": [(r'TaskCreate', 0)],
    "TaskUpdate": [(r'TaskUpdate', 0)],
    "AskUserQuestion": [(r'AskUserQuestion|\bask\b|\bquestion', re.I)],
    "EnterPlanMode": [(r'EnterPlanMode', 0)],
    "ExitPlanMode": [(r'ExitPlanMode', 0)],
}
# bare `Bash` grant pre-approves any command — body
# prescribes a command (fenced block or a known command token).
BARE_BASH_CMD = re.compile(r'```|\b(?:git|python3|gh|jq|grep|rg|npm|make|cargo'
                           r'|sed|awk|cat|test)\b')
ALLOWED_TOOLS_LINE = re.compile(r'^allowed-tools:\s*(.*)$')
DISALLOWED_TOOLS_LINE = re.compile(r'^disallowed-tools:\s*(.*)$')

# Reverse (missing-grant) prescription patterns — stricter than GRANT_REFERENCE
# so incidental "agent"/"edit"/"write" prose does not flood. Catalog covers
# prescribed spawn/edit/write/read (tooling-preference invariant). `skill`
# omitted — saturates every body (same accepted FN as extra-grant).
GRANT_MISSING_REFERENCE = {
    "Agent": [(r'\bAgent\b', 0), (r'\bsub-agents?\b|\bsubagent\b', re.I)],
    "Edit": [(r'\bEdit\b', 0), (r'\brewrite\b', re.I)],
    "Write": [(r'\bwrite (?:delta|the plan file)\b|\bpatch the plan file\b',
               re.I)],
    "Read": [(r'(?:^|\n)\s*(?:\d+\.\s+)?(?:Read|Load)\s+`', re.I)],
}


def split_grant_tokens(value):
    """Split an `allowed-tools` value into grant tokens on top-level commas only —
    paren-depth-aware so a `Bash(...)` arg pattern keeps any inner comma and stays
    a single token."""
    toks, depth, cur = [], 0, ""
    for ch in value:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            toks.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        toks.append(cur.strip())
    return [t for t in toks if t]


def find_allowed_tools(text):
    """Locate the frontmatter `allowed-tools:` line: return (grant tokens, 1-based
    line number), or (None, None) when absent. Scans only the frontmatter region
    (between the leading `---` fences) so a body mention never registers."""
    return _find_frontmatter_tools(text, ALLOWED_TOOLS_LINE)


def find_disallowed_tools(text):
    """Locate the frontmatter `disallowed-tools:` line: return (tokens, 1-based
    line number), or (None, None) when absent. Reverse missing-grant skips
    these — documented denial is not a missing grant."""
    return _find_frontmatter_tools(text, DISALLOWED_TOOLS_LINE)


def _find_frontmatter_tools(text, line_re):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            break
        m = line_re.match(lines[i])
        if m:
            return split_grant_tokens(m.group(1)), i + 1
    return None, None


def body_after_frontmatter(text):
    """Text after the closing frontmatter `---` fence (the skill body) — grant use
    is a body claim, so the grant's own frontmatter line never self-satisfies it."""
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return "\n".join(lines[i + 1:])
    return text


def grant_used(token, body):
    """True when the skill body prescribes an invocation of the granted tool
    (tooling-preference invariant). `Bash(<pattern>)` → any literal command anchor
    of the pattern is present; bare `Bash` → any command token / fenced block;
    a catalogued tool → its body-reference set; an uncatalogued tool → its bare
    token (case-insensitive, so a never-mentioned future grant still flags)."""
    base = token.split("(", 1)[0].strip()
    if base == "Bash":
        inner = token[token.find("(") + 1:token.rfind(")")] if "(" in token else ""
        if not inner.strip():
            return bool(BARE_BASH_CMD.search(body))
        anchors = [a for a in re.split(r'[*\s]', inner) if a]
        return any(a in body for a in anchors)
    pats = GRANT_REFERENCE.get(base, [(r'\b' + re.escape(base) + r'\b', re.I)])
    return any(re.search(p, body, f) for p, f in pats)


def grant_prescribed(tool, body):
    """True when the skill body prescribes `tool` at reverse-audit confidence
    (tooling-preference invariant). Stricter than grant_used — incidental
    "agent"/"edit"/"write" prose does not count as a missing-grant hit."""
    pats = GRANT_MISSING_REFERENCE.get(tool)
    if not pats:
        return False
    return any(re.search(p, body, f) for p, f in pats)


def classify_grants(skill_texts):
    """Grant-use audit core over {path: text} — pure, unit-testable without the
    filesystem (tooling-preference invariant). Both directions: extra grant
    (frontmatter `allowed-tools` token the body never invokes) → VIOLATE;
    missing grant (body prescribes a catalogued tool with no grant and not
    in `disallowed-tools`) → VIOLATE. Skills without an `allowed-tools` line
    carry no grants → no rows. Realized once here so the drift-detector
    retires its hand-run grant sweep — a manual sweep misses rows, the
    recurrence class this closes."""
    out = []
    for path in sorted(skill_texts):
        text = skill_texts[path]
        tokens, lineno = find_allowed_tools(text)
        if not tokens:
            continue
        disallowed, _ = find_disallowed_tools(text)
        disallowed_bases = {t.split("(", 1)[0].strip()
                            for t in (disallowed or [])}
        body = body_after_frontmatter(text)
        granted_bases = set()
        for tok in tokens:
            granted_bases.add(tok.split("(", 1)[0].strip())
            if not grant_used(tok, body):
                out.append(("grant", "VIOLATE",
                            f"grant VIOLATE: {path}:{lineno} grants {tok} "
                            f"zero body use (drop per tooling-preference "
                            f"invariant)"))
        loc = lineno
        for tool in GRANT_MISSING_REFERENCE:
            if tool in granted_bases or tool in disallowed_bases:
                continue
            if grant_prescribed(tool, body):
                out.append(("grant", "VIOLATE",
                            f"grant VIOLATE: {path}:{loc} body prescribes "
                            f"{tool} missing grant (add per "
                            f"tooling-preference invariant)"))
    return out


def audit_grants(skill_md):
    """File-reading wrapper around classify_grants (tooling-preference invariant).
    Asserts no frontmatter `allowed-tools` grant is zero-body-use across the
    PUBLISHED + REPO-LOCAL skill set — realized once here so the drift-detector
    retires its hand-run allowed-tools grant sweep, where a manual sweep misses
    rows (the recurrence class this closes)."""
    texts = {}
    for path in skill_md:
        try:
            texts[path] = read_text(path)
        except OSError:
            continue
    return classify_grants(texts)


# --- token estimate ----------------------------------------------------------

def estimate_tokens(spec_bytes):
    """Token estimate = bytes / TOKEN_RATIO (token-budget invariant). Single
    realization of the divisor: both the audit advisory and the
    emit-token-estimate mode consume this, so /sdd:condense LOAD baseline +
    /sdd:check stop hand-running `wc -c` + division (mechanical-realization
    invariant)."""
    return int(spec_bytes / TOKEN_RATIO)


def audit_token_estimate(spec_bytes):
    est = estimate_tokens(spec_bytes)
    if est > TOKEN_BUDGET:
        k = round(est / 1000)
        return [("token", ADVISORY,
                 f"SPEC.md ~{k}k tokens > {TOKEN_BUDGET // 1000}k budget; "
                 f"consider /sdd:condense")]
    return []


def skill_token_rows(sizes):
    """Per-skill-body token advisory core over [(path, bytes)] — pure,
    unit-testable without the filesystem (token-budget invariant). A published
    SKILL.md body whose estimate (bytes / TOKEN_RATIO) exceeds
    SKILL_TOKEN_BUDGET emits `skill-token|ADVISORY|<path> ~<n>k > 5k …`;
    remediation = split conditional detail to references/ one level deep.
    Realized once here so the drift-detector retires its hand-run size check
    (mechanical-realization invariant)."""
    out = []
    for path, nbytes in sizes:
        est = int(nbytes / TOKEN_RATIO)
        if est > SKILL_TOKEN_BUDGET:
            k = round(est / 1000, 1)
            out.append(("skill-token", ADVISORY,
                        f"{path} ~{k}k tokens > "
                        f"{SKILL_TOKEN_BUDGET // 1000}k skill-body budget; "
                        f"split conditional detail to references/"))
    return out


def audit_skill_tokens(skill_md, repo_root):
    """File-reading wrapper around skill_token_rows (token-budget invariant)
    over the PUBLISHED skill set (discover_skill_md); paths reported
    repo-relative."""
    sizes = []
    for path in skill_md:
        try:
            nbytes = os.path.getsize(path)
        except OSError:
            continue
        sizes.append((os.path.relpath(path, repo_root), nbytes))
    return skill_token_rows(sizes)


# --- batch-sizing advisory ---------------------------------------------------

def recommend_batch_count(v_count, published_census):
    """§V-classification sub-agent count (batch invariant). Base =
    ceil(|V| / BATCH_ROW_DIVISOR) clamped [1, BATCH_MAX_AGENTS]. Narrow-scope
    override: PUBLISHED file census < ceil(|V| / 2) → 1 agent regardless — a
    narrow file set means cross-cutting greps amortize (one in-thread `rg` sweep
    beats per-agent spawn cost). Census is the deterministic PUBLISHED markdown
    file count, not an LLM-eyeballed repo-file proxy (closes §B.7)."""
    if v_count <= 0:
        return 1
    base = (v_count + BATCH_ROW_DIVISOR - 1) // BATCH_ROW_DIVISOR
    base = max(1, min(BATCH_MAX_AGENTS, base))
    if published_census < (v_count + 1) // 2:   # census < ceil(|V| / 2)
        return 1
    return base


def audit_batch_advisory(v_rows, published_md):
    """Emit the batch-sizing advisory (batch invariant):
    `batch|ADVISORY|recommended: <n> agents` from the live §V row count +
    PUBLISHED file census. The drift-detector consumes this row for its
    Batch-protocol agent count instead of hand-computing the heuristic
    (closes §B.7)."""
    n = recommend_batch_count(len(v_rows), len(published_md))
    return [("batch", ADVISORY, f"recommended: {n} agents")]


# --- memo bookkeeping --------------------------------------------------------

def row_body_sha(body):
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def compute_v_row_shas(v_rows):
    return {r["id"]: row_body_sha(r["body"]) for r in v_rows}


def git_sha_reachable(sha):
    try:
        subprocess.run(["git", "rev-parse", "--verify", "--quiet", f"{sha}^{{commit}}"],
                       check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, OSError):
        return False


def audit_memo(memo_path, v_rows):
    """Emit memo invalidation advisories (sha / rev-parse bookkeeping)."""
    out = []
    if not os.path.exists(memo_path):
        out.append(("memo", ADVISORY, "memo absent — first-run, full sweep"))
        return out
    try:
        memo = json.loads(read_text(memo_path))
    except (OSError, ValueError):
        out.append(("memo", ADVISORY, "memo unreadable — dropped, full sweep"))
        return out
    if memo.get("schema_version") != MEMO_SCHEMA:
        out.append(("memo", ADVISORY,
                    "memo schema_version mismatch — memo dropped, full sweep"))
        return out
    if not git_sha_reachable(memo.get("last_clean_sha", "")):
        out.append(("memo", ADVISORY,
                    "last_clean_sha unreachable — memo dropped, full sweep"))
        return out
    cur = compute_v_row_shas(v_rows)
    stored = memo.get("v_row_shas", {})
    dirty = sorted((rid for rid, h in cur.items() if stored.get(rid) != h),
                   key=lambda x: int(x[1:]))
    if dirty:
        # comma-joined field, no surrounding prose (memo invariant) so the
        # drift-detector chains it into `emit-v-slices --dirty`.
        out.append(("memo", ADVISORY, "v_row_shas drift: " + ",".join(dirty)))
    return out


def load_memo(memo_path):
    """Parse the memo dict, or None when absent or unreadable (the audit_memo
    advisory feed reports the why; this loader feeds the ack and scope helpers)."""
    if not os.path.exists(memo_path):
        return None
    try:
        return json.loads(read_text(memo_path))
    except (OSError, ValueError):
        return None


def flipped_since(old_t_rows, cur_t_rows):
    """§T ids flipped `.`→`x` since the clean baseline: status `x` now and not `x`
    (absent or `.`) before. Pure over parsed rows so unit-testable without git."""
    old = {r["id"]: (r["body"] or "").split('|', 1)[0].strip() for r in old_t_rows}
    flipped = [r["id"] for r in cur_t_rows
               if (r["body"] or "").split('|', 1)[0].strip() == "x"
               and old.get(r["id"]) != "x"]
    flipped.sort(key=lambda x: int(x[1:]))
    return flipped


def spec_t_rows_at(repo_root, sha, spec_path="SPEC.md"):
    """Parse SPEC.md §T rows as of <sha> via `git show` (empty on git failure)."""
    try:
        old = subprocess.run(["git", "show", f"{sha}:{spec_path}"], cwd=repo_root,
                             check=True, capture_output=True, text=True).stdout
    except (subprocess.CalledProcessError, OSError):
        return []
    secs, _ = parse_sections(old)
    return parse_pipe_rows(secs, "T", T_ROW)


def git_touched_paths(repo_root, sha):
    """Paths changed `<sha>..HEAD` (empty on git failure)."""
    try:
        res = subprocess.run(["git", "diff", "--name-only", f"{sha}..HEAD"],
                             cwd=repo_root, check=True, capture_output=True, text=True)
    except (subprocess.CalledProcessError, OSError):
        return []
    return [p for p in res.stdout.splitlines() if p.strip()]


def exclude_spec_paths(paths, spec_path="SPEC.md"):
    """Scope-feed rule: drop SPEC.md + its SPEC.archive.md sibling from the
    touched set. Structural SPEC audits are owned mechanically by this script
    and per-row `v_row_shas` is the precise spec-edit signal, so a SPEC-only
    edit not collapse the §V dirty set to a near-full sweep via ubiquitous
    SPEC.md body-refs."""
    archive = (spec_path[:-3] if spec_path.endswith(".md") else spec_path) + ".archive.md"
    excl = {spec_path, archive}
    return [p for p in paths if p not in excl]


# --- §V body path-token dirty scope (scope-feed + mechanical-realization) -----
# The check SCOPE step's "§V dirty" set includes rows whose body path tokens
# (quoted/backticked path-like strings) intersect the touched set. Mechanized
# here so the drift-detector consumes a script row instead of hand-grepping the
# §V section per run. Over-inclusion is safe (a spuriously dirty row
# re-classifies to a clean hold); a missed row is the real risk, so extraction
# leans inclusive — every quoted/backticked path-like token counts, `*`/`**`
# globs and `<...>` placeholders act as wildcards.

SPAN = re.compile(r'`([^`]*)`|"([^"]*)"|\'([^\']*)\'')
PATHISH = re.compile(r'^[\w./*<>-]+$')
HAS_EXT = re.compile(r'\.[A-Za-z][A-Za-z0-9]*$')


def path_tokens(body):
    """Path-like tokens inside quoted/backticked spans of a §V body. Each span's
    whitespace-delimited words are kept when path-like — a `/` or a filename
    extension; surrounding prose punctuation trimmed. Non-path spans (flag names,
    verdict words) yield nothing."""
    tokens = []
    for m in SPAN.finditer(body or ""):
        span = m.group(1) or m.group(2) or m.group(3) or ""
        for word in span.split():
            w = word.strip("(),;:")
            if w and PATHISH.match(w) and ('/' in w or HAS_EXT.search(w)):
                tokens.append(w)
    return tokens


def glob_to_re(tok):
    """Compile a path token to an anchored regex. `*` matches within a path
    segment, `**` spans segments, `<...>` placeholders match a single segment;
    `.` is literal. The token charset is restricted to `[\\w./*<>-]` by PATHISH,
    so the builder escapes only `.` and needs no general re.escape."""
    out = ["^"]
    i, n = 0, len(tok)
    while i < n:
        c = tok[i]
        if c == '*':
            if i + 1 < n and tok[i + 1] == '*':
                out.append('.*'); i += 2
            else:
                out.append('[^/]*'); i += 1
        elif c == '<':
            j = tok.find('>', i)
            if j != -1:
                out.append('[^/]*'); i = j + 1
            else:
                out.append('<'); i += 1
        elif c == '.':
            out.append(r'\.'); i += 1
        else:
            out.append(c); i += 1
    out.append("$")
    return re.compile("".join(out))


def tok_matches(tok, path):
    """A path token intersects a touched path when its glob matches the full path,
    or (for a bare filename, no `/`) the path's basename."""
    rx = glob_to_re(tok)
    if rx.match(path):
        return True
    return '/' not in tok and rx.match(path.rsplit('/', 1)[-1]) is not None


def v_path_dirty(v_rows, touched):
    """§V rows whose body path tokens intersect the touched set (scope-feed +
    mechanical-realization invariants). Pure over parsed rows + the touched list
    so unit-testable without git. Returns the dirty V-id list, ascending."""
    dirty = [r["id"] for r in v_rows
             if any(tok_matches(t, p)
                    for t in path_tokens(r["body"]) for p in touched)]
    dirty.sort(key=lambda x: int(x[1:]))
    return dirty


def audit_scope_feed(repo_root, memo, t_rows, v_rows, spec_path="SPEC.md"):
    """Machine-side scope feed for the memo-driven default sweep (memo invariant):
    `tasks|ADVISORY|flipped-since-clean: <ids>`, `diff|ADVISORY|touched: <paths>`,
    and `scope|ADVISORY|v-path-dirty: <ids>` (§V rows whose body path tokens
    intersect the touched-set), all keyed off the memo's `last_clean_sha`. Fields
    comma-joined, no prose so the drift-detector chains them into
    `emit-v-slices --dirty` not hand-rolling `git diff` or a hand-grep over §V
    bodies. No memo or schema mismatch or unreachable sha → no rows (first-run /
    invalidated → full sweep, nothing to scope — mirrors the memo advisory gate).
    Touched-set drops SPEC.md + SPEC.archive.md per `exclude_spec_paths`."""
    if not memo or memo.get("schema_version") != MEMO_SCHEMA:
        return []
    sha = memo.get("last_clean_sha", "")
    if not sha or not git_sha_reachable(sha):
        return []
    flipped = flipped_since(spec_t_rows_at(repo_root, sha, spec_path), t_rows)
    touched = exclude_spec_paths(git_touched_paths(repo_root, sha), spec_path)
    return [("tasks", ADVISORY, "flipped-since-clean: " + ",".join(flipped)),
            ("diff", ADVISORY, "touched: " + ",".join(touched)),
            ("scope", ADVISORY,
             "v-path-dirty: " + ",".join(v_path_dirty(v_rows, touched)))]


# --- REPO-LOCAL hook probe ---------------------------------------------------

def probe_extras_hook(repo_root):
    """Run `.spec/scripts/check-extras.sh` if present + executable; append its
    pipe-table rows. Language-agnostic contract per the parametric invariant."""
    out = []
    hook = os.path.join(repo_root, ".spec", "scripts", "check-extras.sh")
    if not (os.path.isfile(hook) and os.access(hook, os.X_OK)):
        return out
    try:
        res = subprocess.run([hook], cwd=repo_root, capture_output=True,
                             text=True, timeout=120)
    except (OSError, subprocess.SubprocessError) as e:
        out.append(("extras-hook", ADVISORY, f"hook error: {e}"))
        return out
    for line in res.stdout.splitlines():
        if line.count('|') == 2 and not line.startswith("id|"):
            rid, verdict, evidence = line.split('|', 2)
            out.append((rid.strip(), verdict.strip(), evidence.strip()))
    return out


# --- scope discovery (parametric) --------------------------------------------

def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def plugin_source_dirs(repo_root, plugins):
    """Resolve marketplace `plugins[].source` values to absolute plugin dirs.
    `./` (root-source plugin) resolves to the repo root — a naive
    `lstrip("./")` empties it and silently drops the plugin from PUBLISHED
    scope. Missing/empty source is skipped."""
    dirs = []
    for p in plugins:
        raw = p.get("source", "")
        if not raw:
            continue
        src = os.path.normpath(raw)
        dirs.append(repo_root if src == "." else os.path.join(repo_root, src))
    return dirs


def _manifest_paths(repo_root):
    """Return (marketplace.json path or None, plugin.json path or None).
    Claude Code `.claude-plugin/` only."""
    base = ".claude-plugin"
    mp = os.path.join(repo_root, base, "marketplace.json")
    pj = os.path.join(repo_root, base, "plugin.json")
    return (mp if os.path.exists(mp) else None,
            pj if os.path.exists(pj) else None)


SDD_PLUGIN_NAME = "sdd"     # sdd-only needle audits gate on this manifest name


def plugin_dirs(repo_root):
    """PUBLISHED plugin source dirs from `.claude-plugin/marketplace.json`
    (`plugins[].source`, root `./` → repo root), else single
    `.claude-plugin/plugin.json` → repo root, else empty."""
    mp, pj = _manifest_paths(repo_root)
    if mp:
        try:
            data = json.loads(read_text(mp))
            return plugin_source_dirs(repo_root, data.get("plugins", []))
        except (OSError, ValueError):
            return []
    if pj:
        return [repo_root]
    return []


def plugin_names(repo_root):
    """PUBLISHED plugin names from `.claude-plugin/` marketplace or plugin.json."""
    mp, pj = _manifest_paths(repo_root)
    if mp:
        try:
            data = json.loads(read_text(mp))
            return [p["name"] for p in data.get("plugins", []) if p.get("name")]
        except (OSError, ValueError):
            return []
    if pj:
        try:
            data = json.loads(read_text(pj))
            return [data["name"]] if data.get("name") else []
        except (OSError, ValueError):
            return []
    return []


def discover_published_md(repo_root):
    """PUBLISHED markdown bodies — every `.md` under a plugin source dir.
    Repo-agnostic."""
    md = []
    for d in plugin_dirs(repo_root):
        for root, _, files in os.walk(d):
            for fn in files:
                if fn.endswith(".md"):
                    md.append(os.path.join(root, fn))
    return sorted(md)


def discover_skill_md(repo_root):
    """PUBLISHED skill bodies — `<plugin-source>/skills/*/SKILL.md` for each
    plugin source dir. Conventional `skills/` under the plugin root.
    REPO-LOCAL `.claude/skills/**` excluded by construction. Feeds the
    mechanize-block audit's user-invocable set."""
    out = []
    for d in plugin_dirs(repo_root):
        skills_dir = os.path.join(d, "skills")
        if not os.path.isdir(skills_dir):
            continue
        for name in sorted(os.listdir(skills_dir)):
            p = os.path.join(skills_dir, name, "SKILL.md")
            if os.path.isfile(p):
                out.append(p)
    return sorted(out)


def discover_grant_skills(repo_root):
    """SKILL.md set for grant-use audit: PUBLISHED skills plus REPO-LOCAL
    `.claude/skills`."""
    paths = list(discover_skill_md(repo_root))
    local = os.path.join(repo_root, ".claude", "skills")
    if os.path.isdir(local):
        for name in sorted(os.listdir(local)):
            p = os.path.join(local, name, "SKILL.md")
            if os.path.isfile(p):
                paths.append(p)
    return sorted(set(paths))


def discover_repo_local(repo_root):
    """REPO-LOCAL files holding pinned cites — the cite-DAG repo-local file
    set (scope-set invariant: `.spec/**` + `.claude/**` + README.md +
    CLAUDE.md; membership synced with the invariant row same commit)."""
    files = []
    for dirname in (".spec", ".claude"):
        d = os.path.join(repo_root, dirname)
        if not os.path.isdir(d):
            continue
        for root, _, fns in os.walk(d):
            for fn in fns:
                if fn.endswith(".md"):
                    files.append(os.path.join(root, fn))
    for name in ("README.md", "CLAUDE.md"):
        p = os.path.join(repo_root, name)
        if os.path.exists(p):
            files.append(p)
    return sorted(files)


def discover_human_facing(repo_root):
    """Human-facing prose surfaces (symbol-set + human-clarity invariants):
    repo-root README.md + CLAUDE.md plus plugin manifests.
    Excludes SPEC-adjacent telegraph."""
    out = []
    for name in ("README.md", "CLAUDE.md"):
        p = os.path.join(repo_root, name)
        if os.path.isfile(p):
            out.append(p)
    for d in plugin_dirs(repo_root):
        mani = os.path.join(d, ".claude-plugin", "plugin.json")
        if os.path.isfile(mani):
            out.append(mani)
    return sorted(set(out))


def discover_sembr_fragments(repo_root):
    """Shared recipe fragments under each plugin's `skills/_fragments/**`
    (sembr invariant scope — closes §B.29). Separate helper so self-tests
    assert fragment inclusion without requiring a full skill tree."""
    out = []
    for d in plugin_dirs(repo_root):
        frag = os.path.join(d, "skills", "_fragments")
        if not os.path.isdir(frag):
            continue
        for root, _, files in os.walk(frag):
            for fn in sorted(files):
                if fn.endswith(".md"):
                    out.append(os.path.join(root, fn))
    return sorted(out)


def discover_sembr_files(repo_root):
    """Sembr-invariant prose file set: repo-root README.md + CLAUDE.md,
    `designs/*.md` drafts, PUBLISHED skill bodies, and
    `skills/_fragments/**` (shared recipe text — closes §B.29)."""
    out = []
    for name in ("README.md", "CLAUDE.md"):
        p = os.path.join(repo_root, name)
        if os.path.isfile(p):
            out.append(p)
    designs = os.path.join(repo_root, "designs")
    if os.path.isdir(designs):
        for fn in sorted(os.listdir(designs)):
            if fn.endswith(".md"):
                out.append(os.path.join(designs, fn))
    out += discover_skill_md(repo_root)
    out += discover_sembr_fragments(repo_root)
    return sorted(set(out))


# --- modes -------------------------------------------------------------------

def load_spec(repo_root, spec_path):
    spec = os.path.join(repo_root, spec_path)
    if not os.path.exists(spec):
        sys.stderr.write(f"check-mechanical: {spec_path} not found in "
                         f"{repo_root} — nothing to audit\n")
        sys.exit(2)
    text = read_text(spec)
    spec_bytes = os.path.getsize(spec)
    arch_path = os.path.join(repo_root, "SPEC.archive.md")
    arch_text = read_text(arch_path) if os.path.exists(arch_path) else None
    return text, spec_bytes, arch_text


def parse_archive_ids(arch_text):
    ids = {"V": set(), "T": set(), "B": set()}
    if not arch_text:
        return ids
    secs, _ = parse_sections(arch_text)
    for _, line in secs.get("T", []):
        m = T_ROW.match(line)
        if m:
            ids["T"].add(m.group(1))
    for _, line in secs.get("B", []):
        m = B_ROW.match(line)
        if m:
            ids["B"].add(m.group(1))
    for line in arch_text.splitlines():
        m = re.match(r'^(V\d+):', line)
        if m:
            ids["V"].add(m.group(1))
    return ids



def audit_reorganize_advisory(v_rows):
    """ADVISORY when live §V ids look sparse (renumber / cluster debt smell).
    Heuristic: span of ids / count ≥ 3 and span − count ≥ 15 → suggest reorganize.
    Not dirty. Operator discoverability for reorganize vs condense."""
    if len(v_rows) < 8:
        return []
    ids = []
    for r in v_rows:
        m = re.match(r'V(\d+)', r["id"])
        if m:
            ids.append(int(m.group(1)))
    if not ids:
        return []
    lo, hi = min(ids), max(ids)
    span = hi - lo + 1
    n = len(ids)
    if span >= 3 * n and (span - n) >= 15:
        return [("reorganize", ADVISORY,
                 f"§V id span {lo}..{hi} ({span} slots for {n} live rows) — "
                 f"consider /sdd:reorganize for cluster + renumber clarity")]
    return []


# --- skill-effort ------------------------------------------------------------

# Published skills leave frontmatter `model` unset. `explain` and `check`
# pin `effort: medium`. Every other skill leaves `effort` unset. The README
# honored-frontmatter sentence names `effort` (skill-effort invariant).
SKILL_EFFORT_PIN = {"check": "medium", "explain": "medium"}
_FM_MODEL_KEY = re.compile(r'(?m)^model\s*:')
_FM_EFFORT_KEY = re.compile(r'(?m)^effort\s*:\s*(.*?)\s*$')
_HONORED_FRONTMATTER = "frontmatter is honored"


def _effort_scalar(raw):
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in ("'", '"'):
        return raw[1:-1]
    return raw


def classify_skill_effort(skill_texts, readme_text):
    """skill-effort invariant — pure, unit-testable without the filesystem.

    `skill_texts` maps skill directory name → SKILL.md text. A frontmatter
    `model:` key on any skill is VIOLATE. `explain` and `check` must set
    `effort: medium`; a missing key or any other value is VIOLATE. Any
    other skill with an `effort:` key is VIOLATE. A missing `explain` or
    `check` skill is VIOLATE. The README line that says frontmatter is
    honored must name `effort`.
    """
    out = []
    seen = set()
    for name in sorted(skill_texts):
        fm = parse_frontmatter(skill_texts[name])
        if _FM_MODEL_KEY.search(fm):
            out.append(("skill-effort", "VIOLATE",
                        f"skill-effort VIOLATE: skills/{name}/SKILL.md "
                        f"frontmatter sets model"))
        effort_m = _FM_EFFORT_KEY.search(fm)
        if name in SKILL_EFFORT_PIN:
            want = SKILL_EFFORT_PIN[name]
            got = _effort_scalar(effort_m.group(1)) if effort_m else None
            if got != want:
                shown = got if got is not None else "unset"
                out.append(("skill-effort", "VIOLATE",
                            f"skill-effort VIOLATE: skills/{name}/SKILL.md "
                            f"effort {shown} (want {want})"))
        elif effort_m:
            out.append(("skill-effort", "VIOLATE",
                        f"skill-effort VIOLATE: skills/{name}/SKILL.md "
                        f"frontmatter sets effort"))
        seen.add(name)
    for name in sorted(SKILL_EFFORT_PIN):
        if name not in seen:
            want = SKILL_EFFORT_PIN[name]
            out.append(("skill-effort", "VIOLATE",
                        f"skill-effort VIOLATE: skills/{name}/SKILL.md "
                        f"missing (effort want {want})"))
    honored = None
    for line in (readme_text or "").splitlines():
        if _HONORED_FRONTMATTER in line:
            honored = line
            break
    if honored is None:
        out.append(("skill-effort", "VIOLATE",
                    "skill-effort VIOLATE: README honored-frontmatter "
                    "sentence missing"))
    elif re.search(r'\beffort\b', honored) is None:
        out.append(("skill-effort", "VIOLATE",
                    "skill-effort VIOLATE: README honored-frontmatter "
                    "sentence does not name effort"))
    return out


def audit_skill_effort(repo_root):
    """File-reading wrapper around classify_skill_effort (skill-effort
    invariant). Published `skills/*/SKILL.md` plus repo-root README.md.
    Caller skips this when `plugin_dirs` is empty (consumer-core-profile
    invariant)."""
    texts = {}
    for path in discover_skill_md(repo_root):
        name = os.path.basename(os.path.dirname(path))
        try:
            texts[name] = read_text(path)
        except OSError:
            texts[name] = ""
    readme_p = os.path.join(repo_root, "README.md")
    try:
        readme = read_text(readme_p) if os.path.isfile(readme_p) else ""
    except OSError:
        readme = ""
    return classify_skill_effort(texts, readme)


def run_audit(repo_root, spec_path, run_hook=True, full=False):
    text, spec_bytes, arch_text = load_spec(repo_root, spec_path)
    sections, order = parse_sections(text)
    v_rows = parse_v_rows(sections)
    t_rows = parse_pipe_rows(sections, "T", T_ROW)
    b_rows = parse_pipe_rows(sections, "B", B_ROW)
    arch_present = arch_text is not None
    arch_vret = archive_has_vretired(arch_text) if arch_text else False
    arch_ids = parse_archive_ids(arch_text)

    memo_path = os.path.join(repo_root, ".spec", "check-state.json")
    memo = load_memo(memo_path)
    oversized_ack = (memo.get("oversized_cell_ack")
                     if memo and memo.get("schema_version") == MEMO_SCHEMA else None)

    findings = []
    findings += audit_section_catalog(order)
    findings += audit_archive_markers(sections, arch_present, arch_vret,
                                      arch_ids)
    if arch_text:
        findings += audit_archive_sibling(arch_text)
    findings += audit_cites_grammar(t_rows)
    findings += audit_fix_grammar(b_rows)
    findings += audit_status_cells(t_rows)
    findings += audit_bug_dates(b_rows)
    findings += audit_monotonic(v_rows, "V")
    findings += audit_monotonic(t_rows, "T")
    findings += audit_monotonic(b_rows, "B")
    findings += audit_cite_dag(v_rows, t_rows, b_rows, sections, arch_ids,
                               discover_repo_local(repo_root),
                               parse_i_ids(sections))
    findings += audit_history_residue(v_rows, t_rows, b_rows, full=full,
                                      oversized_ack=oversized_ack)
    published_md = discover_published_md(repo_root)
    findings += audit_pinned_header(published_md)
    skill_md = discover_skill_md(repo_root)
    findings += audit_mechanize_block(skill_md)
    # empty plugin_dirs → no row, not MISSING/VIOLATE; sdd-only needle audits
    # fire only in the sdd plugin repo itself (consumer-core-profile invariant)
    if plugin_dirs(repo_root) and SDD_PLUGIN_NAME in plugin_names(repo_root):
        findings += audit_design_post_approve(repo_root)
        findings += audit_github_pr_per_issue(repo_root)
        findings += audit_github_review_skip(repo_root)
        findings += audit_github_merge_subject(repo_root)
        findings += audit_github_merge_probe(repo_root)
        findings += audit_github_ready_remainder(repo_root)
        findings += audit_spec_fold_github(repo_root)
        findings += audit_build_issue_linked(repo_root)
        findings += audit_issue_linked_ready_chain(repo_root)
        findings += audit_acceptance_gate_detect(repo_root)
        findings += audit_condense_stub_skip(repo_root)
        findings += audit_review_scratch_write(repo_root)
        findings += audit_post_spec_child(repo_root)
        findings += audit_readme_issue_linked(repo_root)
        findings += audit_linear_no_pr(repo_root)
        findings += audit_skill_effort(repo_root)
        findings += audit_claude_md(repo_root)
    if plugin_dirs(repo_root):
        findings += audit_human_symbols(discover_human_facing(repo_root))
        findings += audit_human_idiom(discover_human_facing(repo_root))
    findings += audit_dispatch_targets(skill_md, plugin_names(repo_root))
    findings += audit_grants(discover_grant_skills(repo_root))
    findings += audit_sembr(discover_sembr_files(repo_root))
    findings += audit_batch_advisory(v_rows, published_md)
    findings += audit_token_estimate(spec_bytes)
    findings += audit_skill_tokens(skill_md, repo_root)
    findings += audit_reorganize_advisory(v_rows)
    findings += audit_memo(memo_path, v_rows)
    findings += audit_scope_feed(repo_root, memo, t_rows, v_rows, spec_path)
    if run_hook:
        findings += probe_extras_hook(repo_root)
    return findings


def cmd_audit(args):
    findings = run_audit(args.repo_root, args.spec,
                         run_hook=not args.no_hook, full=args.full)
    print("id|verdict|evidence")
    for rid, verdict, evidence in findings:
        print(f"{rid}|{verdict}|{evidence}")
    return 0


def cmd_emit_v_slices(args):
    text, _, _ = load_spec(args.repo_root, args.spec)
    sections, _ = parse_sections(text)
    slices = collect_v_slices(sections, repo_root=args.repo_root)
    if args.dirty:
        wanted = {t.strip() for t in args.dirty.split(',') if t.strip()}
        slices = [s for s in slices if s["id"] in wanted]
    for s in slices:
        src = s.get("source") or "SPEC.md"
        print(f"## {s['id']} {src}:{s['line_start']}-{s['line_end']}")
        print(s["text"])
        print()
    return 0


def cmd_emit_check_agent_prompt(args):
    """Emit the canonical §V-classification sub-agent prompt. Sole source =
    skills/_fragments/CHECK-AGENT-PROMPT.md (shared-fragments invariant); no
    second copy lives in this script, so the two can never drift."""
    here = os.path.dirname(os.path.abspath(__file__))
    frag = os.path.normpath(
        os.path.join(here, "..", "skills", "_fragments", "CHECK-AGENT-PROMPT.md")
    )
    try:
        body = read_text(frag)
    except OSError:
        sys.stderr.write(f"emit-check-agent-prompt: {frag} unreadable\n")
        return 2
    sys.stdout.write(body if body.endswith("\n") else body + "\n")
    return 0


def cmd_emit_superseded(args):
    text, _, _ = load_spec(args.repo_root, args.spec)
    sections, _ = parse_sections(text)
    v_rows = parse_v_rows(sections)
    t_rows = parse_pipe_rows(sections, "T", T_ROW)
    candidates = emit_superseded_candidates(v_rows, t_rows)
    print(format_superseded_table(candidates))
    return 0


def cmd_emit_fold_seeds(args):
    text, _, _ = load_spec(args.repo_root, args.spec)
    sections, _ = parse_sections(text)
    v_rows = parse_v_rows(sections)
    t_rows = parse_pipe_rows(sections, "T", T_ROW)
    b_rows = parse_pipe_rows(sections, "B", B_ROW)
    seeds = emit_fold_seeds(v_rows, t_rows, b_rows)
    print(format_fold_seeds_table(seeds))
    return 0


def cmd_emit_v_weights(args):
    text, _, _ = load_spec(args.repo_root, args.spec)
    sections, _ = parse_sections(text)
    v_rows = parse_v_rows(sections)
    ranked, _ = emit_v_weights(v_rows)
    print(format_v_weights_table(ranked))
    return 0


def cmd_emit_row_ids(args):
    text, _, _ = load_spec(args.repo_root, args.spec)
    sections, _ = parse_sections(text)
    v_rows = parse_v_rows(sections)
    i_ids = parse_i_ids(sections)
    t_rows = parse_pipe_rows(sections, "T", T_ROW)
    ids = emit_row_ids(v_rows, i_ids, t_rows)
    print("id|verdict|evidence")
    if args.from_audit:
        memo = load_memo(os.path.join(args.repo_root, ".spec", "check-state.json"))
        dirty, flipped = emit_row_id_scope(
            v_rows, t_rows, memo, args.repo_root, args.spec, full=args.full)
        for rid, v, e in prefill_verdicts(ids, dirty, flipped):
            print(f"{rid}|{v}|{e}")
    else:
        for rid in ids:
            print(f"{rid}||")
    return 0


def cmd_emit_overview(args):
    text, _, _ = load_spec(args.repo_root, args.spec)
    sections, order = parse_sections(text)
    print(collect_overview(sections, order))
    return 0


def cmd_emit_token_estimate(args):
    """Single-line `bytes / TOKEN_RATIO` token estimate from SPEC.md
    (token-budget invariant). /sdd:condense LOAD baseline + post-sweep estimate
    consume this instead of hand-running `wc -c` + division."""
    _, spec_bytes, _ = load_spec(args.repo_root, args.spec)
    print(estimate_tokens(spec_bytes))
    return 0


def cmd_emit_prune_patterns(args):
    """History-residue / write-time-prune member set (freshness-contract +
    mechanical-realization invariants). Consumers: spec write-time prune,
    condense prong 4, reorganize ARCHIVE-RETIRED flagged-set grep — prose
    surfaces cite this mode instead of restating members. Spec-independent:
    emits the set without loading SPEC.md."""
    print("id|role|pattern|action")
    for p in PRUNE_PATTERNS:
        print(f"{p['id']}|{p['role']}|{p['pattern']}|{p['action']}")
    return 0


def cmd_emit_residue(args):
    """emit-residue mode (freshness-contract + mechanical-realization): print
    section|id|pattern|line for every residue hit. Condense prong 4 consumes
    this table; empty body (header only) means skip. Shares collect_residue_rows
    with audit_history_residue — no second pattern spelling."""
    text, _, _ = load_spec(args.repo_root, args.spec)
    sections, _ = parse_sections(text)
    v_rows = parse_v_rows(sections)
    t_rows = parse_pipe_rows(sections, "T", T_ROW)
    b_rows = parse_pipe_rows(sections, "B", B_ROW)
    rows = collect_residue_rows(v_rows, t_rows, b_rows)
    print(format_residue_table(rows))
    return 0


def cmd_emit_archive_window(args):
    """emit-archive-window mode (token-budget + archive-semantics +
    mechanical-realization): print action|tid_lo|tid_hi|count|marker for the
    prong-3 window split. Condense consumes this table only; skip → no archive.
    ARCHIVE_CLOSED_T is the sole threshold source."""
    text, _, _ = load_spec(args.repo_root, args.spec)
    sections, _ = parse_sections(text)
    t_rows = parse_pipe_rows(sections, "T", T_ROW)
    rows = emit_archive_window(t_rows)
    print(format_archive_window_table(rows))
    return 0


def cmd_emit_condense_propose(args):
    """emit-condense-propose mode (mechanical-realization + mechanize-scan +
    token-budget): print the five PROPOSE seed tables in one invocation.
    Columns unchanged vs standalone emit-* modes. Condense PROPOSE consumes
    this emit; never five separate calls."""
    text, _, _ = load_spec(args.repo_root, args.spec)
    sections, _ = parse_sections(text)
    v_rows = parse_v_rows(sections)
    t_rows = parse_pipe_rows(sections, "T", T_ROW)
    b_rows = parse_pipe_rows(sections, "B", B_ROW)
    print(format_condense_propose(collect_condense_propose(v_rows, t_rows, b_rows)))
    return 0


def cmd_fix_sembr(args):
    """fix-sembr mode (sembr + mechanical-realization invariants): rewrite
    flagged multi-sentence prose lines one sentence per line, in place, over
    the discovered sembr file set (--files comma-list overrides). Dry-run by
    default — --write applies. Shares the scan's exemption walk + splitter;
    a rejoin-equivalence guard trip leaves the line untouched, prints an
    UNVERIFIABLE row, and exits 1."""
    if args.files:
        files = [f if os.path.isabs(f) else os.path.join(args.repo_root, f)
                 for f in (t.strip() for t in args.files.split(',')) if f]
    else:
        files = discover_sembr_files(args.repo_root)
    verb = "split" if args.write else "would split (dry-run; --write applies)"
    rewrote = 0
    tripped = 0
    print("id|verdict|evidence")
    for path in files:
        try:
            text = read_text(path)
        except OSError:
            continue
        rel = os.path.relpath(path, args.repo_root)
        new_text, rewrites, guard_trips = fix_sembr_text(text)
        for i in sorted(rewrites):
            print(f"sembr-fix|ADVISORY|{rel}:{i} {verb} into "
                  f"{len(rewrites[i])} lines")
        for i in guard_trips:
            print(f"sembr-fix|UNVERIFIABLE|{rel}:{i} rejoin-equivalence "
                  f"guard tripped — line left untouched")
        rewrote += len(rewrites)
        tripped += len(guard_trips)
        if args.write and rewrites:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_text)
    sys.stderr.write(f"fix-sembr: {rewrote} line(s) "
                     f"{'rewritten' if args.write else 'flagged (dry-run)'}, "
                     f"{tripped} guard trip(s)\n")
    return 1 if tripped else 0


def parse_table(text):
    rows = []
    for line in text.splitlines():
        line = line.rstrip("\n")
        if not line or line.startswith("id|"):
            continue
        if line.count('|') < 2:
            continue
        rid, verdict, evidence = line.split('|', 2)
        rows.append((rid.strip(), verdict.strip(), evidence.strip()))
    return rows


def compute_clean(rows):
    """Clean iff no row carries a dirty verdict. Returns (clean, offenders)."""
    offenders = [(rid, v) for rid, v, _ in rows if v in DIRTY_VERDICTS]
    return (len(offenders) == 0), offenders


def row_type_vocab(rid):
    """Admissible verdict set for a merged-table row id, by row type
    (drift-verdict-vocab invariant): §V → V_VOCAB, §I → I_VOCAB (incl. MATCH),
    §T → T_VOCAB. Pseudo-id rows (mechanical findings) + §B ids return None =
    unrestricted (never classified rows)."""
    m = ID_NUM.match(rid)
    if m:
        if m.group(1) == "V":
            return V_VOCAB
        if m.group(1) == "T":
            return T_VOCAB
        return None
    if rid.startswith("I."):
        return I_VOCAB
    return None


def validate_vocab(rows):
    """Per-row-type verdict admissibility (drift-verdict-vocab invariant): each
    classified row carries only a verdict valid for its type — MATCH is §I-only,
    V-vocab §V-only, STALE §T-only — so the LLM can't silently remap an
    out-of-type verdict (closes §B.8). Pseudo-id rows are unrestricted; a blank
    verdict on a typed §V/§I/§T row (unfilled skeleton row) is a complaint, so
    an unclassified dirty row can never advance the memo. Returns list of
    complaints."""
    bad = []
    for rid, v, _ in rows:
        vocab = row_type_vocab(rid)
        if not v:
            if vocab is not None:
                bad.append(f"{rid} verdict blank — unfilled skeleton row")
            continue
        if vocab is not None and v not in vocab:
            bad.append(f"{rid} verdict {v} not in row-type vocab")
    return bad


def memo_exit_code(rows):
    """write-memo decision (memo invariant), no side effects so unit-testable
    without git/filesystem: 2 = invalid vocab, 1 = dirty run (memo untouched,
    CI-gateable), 0 = clean (caller writes the memo). Vocab failure outranks
    dirtiness. Returns (code, detail) — detail is the vocab complaints (code 2),
    the dirty offenders (code 1), or None (code 0)."""
    bad = validate_vocab(rows)
    if bad:
        return 2, bad
    clean, offenders = compute_clean(rows)
    if not clean:
        return 1, offenders
    return 0, None


# Cache filenames the `.spec/.gitignore` guard must list (memo + resume card).
SPEC_GITIGNORE_CACHE = ("check-state.json", "backprop-handoff.json")


def ensure_gitignore_guard(repo_root):
    """Append missing SPEC_GITIGNORE_CACHE lines to `.spec/.gitignore`.

    First `.spec/` write (write-memo, or spec NEW/DISTILL/BACKPROP recipe)
    lists `backprop-handoff.json` so the resume card stays untracked
    (backprop-resume-card invariant).
    """
    path = os.path.join(repo_root, ".spec", ".gitignore")
    existing = ""
    if os.path.exists(path):
        existing = read_text(path)
    present = {l.strip() for l in existing.splitlines()}
    missing = [name for name in SPEC_GITIGNORE_CACHE if name not in present]
    if not missing:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        if existing and not existing.endswith("\n"):
            f.write("\n")
        for name in missing:
            f.write(name + "\n")


def cmd_write_memo(args):
    behavioral = parse_table(sys.stdin.read())
    if args.from_audit:
        # script owns both ends (memo invariant): re-run the mechanical audit
        # internally + merge it with the behavioral rows, so stdin carries
        # behavioral verdicts only and hand-merging the audit table is banned.
        mechanical = run_audit(args.repo_root, args.spec,
                               run_hook=not args.no_hook, full=args.full)
        rows = mechanical + behavioral
    else:
        rows = behavioral
    code, detail = memo_exit_code(rows)
    if code == 2:
        sys.stderr.write("write-memo: invalid verdicts: " + "; ".join(detail) + "\n")
        return 2
    if code == 1:
        sys.stderr.write("write-memo: run not clean (" + ", ".join(
            f"{r}:{v}" for r, v in detail[:8]) + ") — memo untouched (exit 1)\n")
        return 1
    text, _, _ = load_spec(args.repo_root, args.spec)
    sections, _ = parse_sections(text)
    v_rows = parse_v_rows(sections)
    t_rows = parse_pipe_rows(sections, "T", T_ROW)
    b_rows = parse_pipe_rows(sections, "B", B_ROW)
    try:
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=args.repo_root,
                              check=True, capture_output=True, text=True).stdout.strip()
    except (subprocess.CalledProcessError, OSError):
        head = ""
    classifications = {rid: v for rid, v, _ in rows
                       if ID_NUM.match(rid) and rid[0] == "V"}
    memo = {
        "schema_version": MEMO_SCHEMA,
        "last_clean_sha": head,
        "v_row_shas": compute_v_row_shas(v_rows),
        "last_run_at": datetime.datetime.now(datetime.timezone.utc)
                       .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "last_v_classifications": classifications,
        "oversized_cell_ack": oversized_cell_sha(
            collect_oversized_cells(t_rows, b_rows)),
    }
    ensure_gitignore_guard(args.repo_root)
    memo_path = os.path.join(args.repo_root, ".spec", "check-state.json")
    os.makedirs(os.path.dirname(memo_path), exist_ok=True)
    with open(memo_path, "w", encoding="utf-8") as f:
        json.dump(memo, f, indent=2)
        f.write("\n")
    sys.stderr.write(f"write-memo: clean — memo @ {head[:7]} "
                     f"({len(memo['v_row_shas'])} §V rows hashed)\n")
    return 0


# --- acceptance-gate (github-workflow; closes §B.34) --------------------------
# Pure parse + verdict helpers for the ACCEPTANCE-GATE fragment.
# LLM still maps open bullets to evidence; script owns section/bullet parse and
# the BLOCK/ALLOW/ADVISORY decision so unproven close cannot silent-pass.

_ACCEPTANCE_HEADING = re.compile(r"^##\s+Acceptance\s*$", re.MULTILINE | re.I)
_ACCEPTANCE_BULLET = re.compile(
    r"^[\t ]*[-*]\s+\[([ xX])\]\s+(.+?)\s*$", re.MULTILINE
)
# Next ATX heading ends the Acceptance section (## or deeper).
_NEXT_HEADING = re.compile(r"^#{1,6}\s+\S", re.MULTILINE)


def parse_acceptance_bullets(body):
    """Parse `## Acceptance` checklist bullets from an issue body.

    Returns:
      None  — no `## Acceptance` heading (ADVISORY path)
      list of {"text": str, "checked": bool} — possibly empty
    """
    if body is None:
        return None
    m = _ACCEPTANCE_HEADING.search(body)
    if not m:
        return None
    rest = body[m.end():]
    end = _NEXT_HEADING.search(rest)
    section = rest[: end.start()] if end else rest
    out = []
    for bm in _ACCEPTANCE_BULLET.finditer(section):
        mark, text = bm.group(1), bm.group(2).strip()
        out.append({"text": text, "checked": mark.lower() == "x"})
    return out


def acceptance_gate_verdict(bullets, proven):
    """Decide ACCEPTANCE-GATE verdict.

    bullets: None (no section) or list from parse_acceptance_bullets.
    proven:  iterable of bullet texts (or indices) the caller has evidence for.
             Only open bullets require proof; checked bullets are already done.

    Returns: "ADVISORY" | "BLOCK" | "ALLOW"
    """
    if bullets is None:
        return "ADVISORY"
    proven_set = set(proven) if proven is not None else set()
    for i, b in enumerate(bullets):
        if b.get("checked"):
            continue
        text = b.get("text", "")
        if text in proven_set or i in proven_set:
            continue
        return "BLOCK"
    return "ALLOW"


# --- self-test ---------------------------------------------------------------

def _vrow(n, body):
    return f"V{n}: {body}"


def selftest():
    fails = []

    def check(cond, label):
        if not cond:
            fails.append(label)

    # column extraction: `|` inside backtick body must not break id/cites split
    line = f"T{1}|x|amend `[§T.n|--next|--all]` per rule|V{2},V{3}"
    rid, body, last = split_cols(line)
    check(rid == f"T{1}", "split id")
    check(last == f"V{2},V{3}", "split rightmost cites with pipe in body")
    check(body is not None and "--next" in body, "split body keeps inner pipes")

    # section catalog: good order clean; missing + reorder flagged
    good = "\n".join(f"## §{l} {SECTION_NAME[l]}" for l in CANONICAL_ORDER)
    secs, order = parse_sections(good)
    check(audit_section_catalog(order) == [], "catalog clean")
    _, bad_order = parse_sections("## §G GOAL\n## §I INTERFACES\n## §C CONSTRAINTS"
                                  "\n## §V INVARIANTS\n## §T TASKS\n## §B BUGS")
    check(any(v == "VIOLATE" for _, v, _ in audit_section_catalog(bad_order)),
          "catalog reorder flagged")

    # cites grammar: range form rejected, comma-list accepted
    ok = [{"id": f"T{9}", "last": f"V{1},V{2},-", "line": 1}]
    rng = [{"id": f"T{9}", "last": f"V{1}..V{4}", "line": 1}]
    check(audit_cites_grammar(ok) == [], "cites comma-list ok")
    check(len(audit_cites_grammar(rng)) == 1, "cites range rejected")

    # cites grammar: I.<kind> tokens citable
    ok_i = [{"id": f"T{9}", "last": "I.api,I.check_cli", "line": 1}]
    check(audit_cites_grammar(ok_i) == [], "cites I.<kind> tokens ok")

    # fix grammar: only V-tokens / sentinel
    check(audit_fix_grammar([{"id": f"B{5}", "last": "-", "line": 1}]) == [],
          "fix sentinel ok")
    check(len(audit_fix_grammar([{"id": f"B{5}", "last": f"T{3}", "line": 1}])) == 1,
          "fix non-V rejected")

    # monotonic: increasing ok, reuse flagged
    inc = [{"id": f"V{0}", "line": 1}, {"id": f"V{5}", "line": 2}]
    reuse = [{"id": f"V{5}", "line": 1}, {"id": f"V{5}", "line": 2}]
    check(audit_monotonic(inc, "V") == [], "monotonic increasing ok")
    check(len(audit_monotonic(reuse, "V")) == 1, "monotonic reuse flagged")

    # cite-DAG: resolved silent, unresolved flagged
    vr = [{"id": f"V{1}", "body": "x", "line": 1}]
    tr = [{"id": f"T{9}", "last": f"V{1}", "line": 2}]
    tr_bad = [{"id": f"T{9}", "last": f"V{77}", "line": 2}]
    empty_ids = {"V": set(), "T": set(), "B": set()}
    check(audit_cite_dag(vr, tr, [], {}, empty_ids, [], []) == [],
          "cite resolved silent")
    bad = audit_cite_dag(vr, tr_bad, [], {}, empty_ids, [], [])
    check(any(v == "UNRESOLVED" for _, v, _ in bad), "cite unresolved flagged")
    # I.<kind> cites resolve against the live §I id set
    tr_i = [{"id": f"T{9}", "last": f"V{1},I.api", "line": 2}]
    check(audit_cite_dag(vr, tr_i, [], {}, empty_ids, [], [{"id": "I.api"}]) == [],
          "I-cite resolved silent")
    bad_i = audit_cite_dag(vr, tr_i, [], {}, empty_ids, [], [])
    check(any(v == "UNRESOLVED" and "I.api" in e for _, v, e in bad_i),
          "I-cite unresolved flagged")

    # history-residue: each pattern flagged; pre-filters exempt
    flag_v = [{"id": f"V{8}", "body": "foo retired 2026-01-02 bar", "line": 1}]
    check(any("dated-retirement" in e for _, _, e
              in audit_history_residue(flag_v, [], [])), "dated-retirement flagged")
    amend_v = [{"id": f"V{8}", "body": "clause (∆) here", "line": 1}]
    check(any("amendment-counter" in e for _, _, e
              in audit_history_residue(amend_v, [], [])), "amendment-counter flagged")
    # backtick-wrapped pattern definition exempt
    bt_v = [{"id": f"V{8}", "body": "pattern `\\bretired \\d{4}-\\d{2}-\\d{2}\\b` here",
             "line": 1}]
    check(audit_history_residue(bt_v, [], []) == [], "backtick pattern exempt")
    # cite-modifier exempt
    cm_v = [{"id": f"V{8}", "body": f"per §V.{94}(∆) amend", "line": 1}]
    check(audit_history_residue(cm_v, [], []) == [], "cite-modifier exempt")
    # retired-in-place §V row exempt
    rip_v = [{"id": f"V{95}", "body": "retired 2026-06-03 — moot", "line": 1}]
    check(audit_history_residue(rip_v, [], []) == [], "retired-in-place exempt")
    # oversized cell advisory
    big = [{"id": f"T{9}", "body": "x" * (OVERSIZE_CELL + 1), "line": 1}]
    check(any(v == ADVISORY for _, v, _ in audit_history_residue([], big, [])),
          "oversized advisory")
    # oversized-cell ack suppression (memo invariant): matching ack silences,
    # stale ack fires, a new oversized cell re-fires despite the old ack
    ack = oversized_cell_sha([f"T{9}"])
    check(not any(v == ADVISORY for _, v, _
                  in audit_history_residue([], big, [], oversized_ack=ack)),
          "oversized advisory suppressed when ack matches")
    check(any(v == ADVISORY for _, v, _
              in audit_history_residue([], big, [], oversized_ack="stale")),
          "oversized advisory fires when ack stale")
    big2 = big + [{"id": f"T{10}", "body": "y" * (OVERSIZE_CELL + 1), "line": 2}]
    check(any(v == ADVISORY for _, v, _
              in audit_history_residue([], big2, [], oversized_ack=ack)),
          "oversized advisory re-fires on new cell")
    check(oversized_cell_sha([f"T{2}", f"T{1}"])
          == oversized_cell_sha([f"T{1}", f"T{2}"]),
          "oversized ack sha order-independent")
    check(collect_oversized_cells(big, []) == [f"T{9}"]
          and collect_oversized_cells([{"id": f"T{3}", "body": "ok"}], []) == [],
          "collect_oversized_cells: only > OVERSIZE_CELL")

    # emit-residue: same hit set as audit (full) + oversized-cell rows; empty clean
    clean_res = collect_residue_rows(
        [{"id": f"V{1}", "body": "clean axiom", "line": 1}],
        [{"id": f"T{1}", "body": "x|short", "line": 2}],
        [])
    check(clean_res == [], "emit-residue: clean rows → empty table body")
    res_v = collect_residue_rows(flag_v, [], [])
    check(len(res_v) == 1 and res_v[0]["pattern"] == "dated-retirement"
          and res_v[0]["section"] == "V" and res_v[0]["id"] == f"V{8}",
          "emit-residue: dated-retirement row")
    res_mix = collect_residue_rows(amend_v + flag_v, big, [])
    res_patterns = {(r["id"], r["pattern"]) for r in res_mix}
    check((f"V{8}", "amendment-counter") in res_patterns
          and (f"V{8}", "dated-retirement") in res_patterns
          and (f"T{9}", OVERSIZE_PATTERN) in res_patterns,
          "emit-residue: HR patterns + oversized-cell")
    # emit set of (section,id,pattern) for non-oversize equals audit full VIOLATE set
    audit_full = audit_history_residue(amend_v + flag_v, big, [], full=True)
    audit_keys = set()
    for _, v, e in audit_full:
        if v != "VIOLATE":
            continue
        # evidence: §V.V8 VIOLATE: history: amendment-counter @ SPEC.md:1
        m = re.search(r'§([VTB])\.(\w+) VIOLATE: history: (\S+)', e)
        if m:
            audit_keys.add((m.group(1), m.group(2), m.group(3)))
    emit_keys = {(r["section"], r["id"], r["pattern"]) for r in res_mix
                 if r["pattern"] != OVERSIZE_PATTERN}
    check(emit_keys == audit_keys, "emit-residue: HR hits agree with audit full")
    # pre-filters: emit empty when audit empty
    check(collect_residue_rows(bt_v, [], []) == [],
          "emit-residue: backtick pre-filter")
    check(collect_residue_rows(cm_v, [], []) == [],
          "emit-residue: cite-modifier pre-filter")
    check(collect_residue_rows(rip_v, [], []) == [],
          "emit-residue: retired-in-place pre-filter")

    # §T flipped-since-clean: `x` now and not `x` before (pure over parsed rows)
    old_t = [{"id": f"T{1}", "body": ".|task"}, {"id": f"T{2}", "body": "x|done"}]
    cur_t = [{"id": f"T{1}", "body": "x|task"}, {"id": f"T{2}", "body": "x|done"},
             {"id": f"T{3}", "body": "x|new"}]
    check(flipped_since(old_t, cur_t) == [f"T{1}", f"T{3}"],
          "flipped: .→x and newly-added x flagged")
    check(flipped_since(cur_t, cur_t) == [], "flipped: stable x not flagged")
    # scope-feed rule: touched-set excludes SPEC.md + SPEC.archive.md sibling
    check(exclude_spec_paths(["SPEC.md", "SPEC.archive.md",
                              "scripts/x.py"])
          == ["scripts/x.py"],
          "touched-set excludes SPEC.md + SPEC.archive.md")
    check(exclude_spec_paths(["SPEC.md", "SPEC.archive.md"]) == [],
          "SPEC-only diff → empty touched-set")
    check(exclude_spec_paths([]) == [], "touched-set exclude: empty in → empty out")
    check(exclude_spec_paths(["sub/SPEC.md"]) == ["sub/SPEC.md"],
          "touched-set exclude: only repo-root SPEC.md, not same-basename subpath")
    # §V body path-token dirty scope (scope-feed + mechanical-realization):
    # quoted/backticked path tokens intersect the touched set, script-side, so
    # the check SCOPE step consumes a row instead of hand-grepping §V bodies.
    n_extras = 40
    vp_rows = [
        {"id": f"V{1}", "body": "reg — SPEC.md, `skills/**/SKILL.md`, prose"},
        {"id": f"V{n_extras}",
         "body": f"mech — → `.spec/check-extras.md §V{n_extras}`"},
        {"id": f"V{31}", "body": "design — writes `designs/<slug>.md` only"},
        {"id": f"V{22}", "body": "no path — `--from-audit` and `emit-v-slices`"},
    ]
    check(v_path_dirty(vp_rows, ["skills/check/SKILL.md"]) == [f"V{1}"],
          "v-path-dirty: glob token matches touched skill path")
    check(v_path_dirty(vp_rows, [".spec/check-extras.md"]) == [f"V{n_extras}"],
          "v-path-dirty: stub body path token matches touched extras")
    check(v_path_dirty(vp_rows, ["designs/foo.md"]) == [f"V{31}"],
          "v-path-dirty: placeholder token matches touched design draft")
    check(v_path_dirty(vp_rows, ["README.md"]) == [],
          "v-path-dirty: no path-token intersection yields empty")
    check(v_path_dirty(vp_rows, []) == [],
          "v-path-dirty: empty touched-set yields empty")
    check(path_tokens("no path — `--from-audit` and `emit-v-slices`") == [],
          "v-path-dirty: non-path backtick spans yield no tokens")
    check(v_path_dirty([{"id": f"V{2}", "body": "bare `SKILL.md` name"}],
                       ["skills/build/SKILL.md"]) == [f"V{2}"],
          "v-path-dirty: bare filename matches touched path basename")
    multi = [{"id": f"V{n_extras}",
              "body": f"→ `.spec/check-extras.md §V{n_extras}`"},
             {"id": f"V{3}", "body": f"→ `.spec/check-extras.md §V{3}`"}]
    check(v_path_dirty(multi, [".spec/check-extras.md"])
          == [f"V{3}", f"V{n_extras}"],
          "v-path-dirty: multiple dirty rows sorted ascending")
    # §T status + §B date cell shape
    check(audit_status_cells([{"id": f"T{1}", "body": ".|task", "line": 1}]) == [],
          "status . ok")
    check(len(audit_status_cells([{"id": f"T{1}", "body": "?|task", "line": 1}])) == 1,
          "status ? flagged")
    check(audit_bug_dates([{"id": f"B{1}", "body": "2026-06-11|cause", "line": 1}]) == [],
          "date iso ok")
    check(len(audit_bug_dates([{"id": f"B{1}", "body": "yesterday|cause", "line": 1}])) == 1,
          "date non-iso flagged")
    # marketplace source resolution: root `./` keeps the plugin in scope
    check(plugin_source_dirs("/r", [{"source": "./"}]) == ["/r"],
          "source ./ resolves to repo root")
    check(plugin_source_dirs("/r", [{"source": "./plugins/x"}])
          == [os.path.join("/r", "plugins/x")],
          "nested source resolves under root")
    check(plugin_source_dirs("/r", [{}, {"source": ""}]) == [],
          "missing/empty source skipped")
    # body-row aggregation: > threshold → single per-section summary row
    many_v = [{"id": f"V{200 + i}", "body": "foo retired 2026-01-02 bar",
               "line": i + 1}
              for i in range(HISTORY_AGGREGATE_THRESHOLD + 5)]
    agg = audit_history_residue(many_v, [], [])
    violates = [row for row in agg if row[1] == "VIOLATE"]
    check(len(violates) == 1, "history aggregated when count > threshold")
    check(any(f"{HISTORY_AGGREGATE_THRESHOLD + 5} rows" in e
              and "dated-retirement" in e
              for _, _, e in violates),
          "history aggregate row count + pattern breakdown")
    # --full → per-row regardless
    full_rows = audit_history_residue(many_v, [], [], full=True)
    check(len([r for r in full_rows if r[1] == "VIOLATE"])
          == HISTORY_AGGREGATE_THRESHOLD + 5,
          "history --full restores per-row")
    # ≤ threshold → per-row form retained
    few_v = [{"id": f"V{300 + i}", "body": "foo retired 2026-01-02 bar",
              "line": i + 1}
             for i in range(HISTORY_AGGREGATE_THRESHOLD)]
    few = audit_history_residue(few_v, [], [])
    check(len([r for r in few if r[1] == "VIOLATE"])
          == HISTORY_AGGREGATE_THRESHOLD,
          "history below threshold per-row")
    # mixed patterns → breakdown enumerates each
    mixed_t = ([{"id": f"T{400 + i}", "body": "stale (∆) clause", "line": i + 1}
                for i in range(6)]
               + [{"id": f"T{500 + i}", "body": "foo retired 2026-01-02",
                   "line": i + 1}
                  for i in range(6)])
    mix = audit_history_residue([], mixed_t, [])
    violates_mix = [row for row in mix if row[1] == "VIOLATE"]
    check(len(violates_mix) == 1, "mixed patterns aggregate to single row")
    check(any("amendment-counter" in e and "dated-retirement" in e
              for _, _, e in violates_mix),
          "mixed patterns breakdown lists both")

    # emit-v-slices: row bodies + source line ranges; --dirty filter; verbatim
    spec_v = ("## §G GOAL\n## §C CONSTRAINTS\n## §I INTERFACES\n"
              "## §V INVARIANTS\n"
              + _vrow(0, "axiom body") + "\n"
              + _vrow(1, "second invariant") + "\n"
              + _vrow(2, "third `a|b` invariant") + "\n"
              "## §T TASKS\n")
    secs_v, _ = parse_sections(spec_v)
    sl = collect_v_slices(secs_v)
    check(len(sl) == 3, "emit-v-slices: all rows")
    check(sl[0]["id"] == f"V{0}" and sl[0]["line_start"] == 5
          and sl[0]["line_end"] == 5, "emit-v-slices: single-line source range")
    check("third" in sl[2]["text"] and "a|b" in sl[2]["text"],
          "emit-v-slices: body keeps inner pipes verbatim")
    only = [s for s in sl if s["id"] in {f"V{1}"}]
    check(len(only) == 1 and only[0]["id"] == f"V{1}", "emit-v-slices: --dirty filter")

    # prong-2 SUPERSEDED candidates: live-§V-only resolution
    sv = [{"id": f"V{1}", "body": "live invariant", "line": 1}]
    t_live = [{"id": f"T{10}", "body": "x|task", "last": f"V{1}", "line": 1}]
    check(emit_superseded_candidates(sv, t_live) == [],
          "superseded: live cite not candidate")
    t_gone = [{"id": f"T{11}", "body": "x|task", "last": f"V{1},V{95}", "line": 1}]
    cand = emit_superseded_candidates(sv, t_gone)
    check(len(cand) == 1 and cand[0]["id"] == f"T{11}"
          and cand[0]["unresolved"] == [f"V{95}"],
          "superseded: archived/retired cite is candidate")
    t_open = [{"id": f"T{12}", "body": ".|task", "last": f"V{95}", "line": 1}]
    check(emit_superseded_candidates(sv, t_open) == [],
          "superseded: open §T excluded")
    t_nonv = [{"id": f"T{13}", "body": "x|task", "last": f"T{3},B{4},I.key", "line": 1}]
    check(emit_superseded_candidates(sv, t_nonv) == [],
          "superseded: non-V cites ignored")

    # prong-1 fold-candidate seeds: co-cited live §V rows cluster (transitively)
    fv = [{"id": f"V{1}", "body": "a", "line": 1, "full": f"V{1}: a"},
          {"id": f"V{2}", "body": "b", "line": 2, "full": f"V{2}: b"},
          {"id": f"V{3}", "body": "c", "line": 3, "full": f"V{3}: c"},
          {"id": f"V{9}", "body": "d", "line": 4, "full": f"V{9}: d"}]
    ft = [{"id": f"T{10}", "body": "x|t", "last": f"V{1},V{2}", "line": 1},
          {"id": f"T{11}", "body": "x|t", "last": f"V{2},V{3}", "line": 2},
          {"id": f"T{12}", "body": "x|t", "last": f"V{9}", "line": 3}]  # single → no edge
    seeds = emit_fold_seeds(fv, ft, [])
    check(len(seeds) == 1, "fold-seed: one cluster")
    check(seeds[0]["members"] == [f"V{1}", f"V{2}", f"V{3}"],
          "fold-seed: transitive co-citation cluster")
    check(f"T{10}" in seeds[0]["citers"] and f"T{11}" in seeds[0]["citers"]
          and f"T{12}" not in seeds[0]["citers"], "fold-seed: contributing citers listed")
    # §B.fix co-citation forms an edge; archived/non-live cite forms none (live-only)
    fb = [{"id": f"B{6}", "body": "x", "last": f"V{1},V{9}", "line": 1}]
    seeds_b = emit_fold_seeds(fv, [], fb)
    check(len(seeds_b) == 1 and seeds_b[0]["members"] == [f"V{1}", f"V{9}"]
          and seeds_b[0]["citers"] == [f"B{6}"], "fold-seed: §B.fix co-citation")
    fb_gone = [{"id": f"B{7}", "body": "x", "last": f"V{1},V{95}", "line": 1}]  # {95} not in live
    check(emit_fold_seeds(fv, [], fb_gone) == [],
          "fold-seed: non-live cite forms no edge")

    # prong-6 per-§V-row weights: heavy set first reaches ≥ 50%, deterministic
    wv = [{"id": f"V{1}", "body": "", "line": 1, "full": "V" + "1: " + "x" * 10},
          {"id": f"V{2}", "body": "", "line": 2, "full": "V" + "2: " + "y" * 90},
          {"id": f"V{3}", "body": "", "line": 3, "full": "V" + "3: " + "z" * 5}]
    ranked, total = emit_v_weights(wv)
    check(ranked[0]["id"] == f"V{2}", "v-weights: heaviest row ranks first")
    check([w["id"] for w in ranked if w["heavy"]] == [f"V{2}"],
          "v-weights: heavy set first reaches 50%")
    check(ranked[0]["tokens"] == int(ranked[0]["bytes"] / TOKEN_RATIO),
          "v-weights: token weight is bytes/TOKEN_RATIO")
    # equal weights → tie-break ascending id so run-stable
    tv = [{"id": f"V{2}", "body": "", "line": 1, "full": "V" + "2: " + "a" * 20},
          {"id": f"V{1}", "body": "", "line": 2, "full": "V" + "1: " + "a" * 20}]
    tied, _ = emit_v_weights(tv)
    check([w["id"] for w in tied] == [f"V{1}", f"V{2}"],
          "v-weights: tie-break ascending id")
    # stub rows never heavy; all-stub fixture → empty heavy set
    # (token-budget invariant; stub = extraction-complete).
    stub_full = (
        f"V{{n}}: name — → `.spec/check-extras.md §V{{n}}`"
    )
    sv = [{"id": f"V{n}", "body": "", "line": n,
           "full": stub_full.format(n=n)} for n in (1, 2, 3)]
    stub_ranked, _ = emit_v_weights(sv)
    check([w["id"] for w in stub_ranked if w["heavy"]] == [],
          "v-weights: all-stub fixture → empty heavy set")
    check(all(not w["heavy"] for w in stub_ranked),
          "v-weights: stub rows not heavy")
    mixed = [
        {"id": f"V{1}", "body": "", "line": 1,
         "full": stub_full.format(n=1) + "x" * 90},
        {"id": f"V{2}", "body": "", "line": 2,
         "full": "V" + "2: " + "y" * 40},
    ]
    mixed_ranked, _ = emit_v_weights(mixed)
    check(all(not w["heavy"] for w in mixed_ranked if w["id"] == f"V{1}"),
          "v-weights: stub row not heavy even when longest")
    check([w["id"] for w in mixed_ranked if w["heavy"]] == [f"V{2}"],
          "v-weights: remaining inline row still heavy")

    # emit-row-ids: §I ids from kind prefixes; skeleton is §V+§I+§T in order
    isec = ("## §I INTERFACES\n"
            "external surface — what world sees.\n"
            "- cmd: `foo bar <arg>` → stdout JSON\n"
            "api: POST /x → 200 {id}\n"
            "- api: GET /x → 200 {id}\n"
            "- `quoted` lead token → no id\n"
            "## §V INVARIANTS\n")
    isecs, _ = parse_sections(isec)
    i_ids = parse_i_ids(isecs)
    check([r["id"] for r in i_ids] == ["I.cmd", "I.api"],
          "emit-row-ids: §I ids from kind prefixes; prose, dup, backtick-lead excluded")
    skel = emit_row_ids([{"id": f"V{1}"}], i_ids,
                        [{"id": f"T{9}"}, {"id": f"T{10}"}])
    check(skel == [f"V{1}", "I.cmd", "I.api", f"T{9}", f"T{10}"],
          "emit-row-ids: skeleton is §V+§I+§T in section order")
    # skeleton rows survive write-memo's parse_table (≥ 2 pipes, header skipped)
    skel_table = "id|verdict|evidence\n" + "\n".join(f"{r}||" for r in skel)
    parsed = parse_table(skel_table)
    check([r[0] for r in parsed] == skel and all(v == "" for _, v, _ in parsed),
          "emit-row-ids: pipe-table parses for fill-verdicts hand-off")
    filled = prefill_verdicts(
        [f"V{1}", f"V{2}", "I.cmd", f"T{9}", f"T{10}"],
        dirty_v=[f"V{2}"], flipped_t=[f"T{10}"])
    check(filled == [
        (f"V{1}", "HOLD-SINCE-CLEAN", ""),
        (f"V{2}", "", ""),
        ("I.cmd", "", ""),
        (f"T{9}", "HOLD-SINCE-CLEAN", ""),
        (f"T{10}", "", ""),
    ], "emit-row-ids --from-audit: pre-fill HOLD-SINCE-CLEAN/blank")
    filled_table = "id|verdict|evidence\n" + "\n".join(
        f"{rid}|{v}|{e}" for rid, v, e in filled)
    check(parse_table(filled_table) == filled,
          "emit-row-ids --from-audit: pre-fill table parses for write-memo")
    check(validate_vocab([r for r in filled if r[1]]) == [],
          "emit-row-ids --from-audit: pre-fill verdicts in row-type vocab")
    check(memo_exit_code(filled)[0] == 2,
          "write-memo: unfilled blank dirty rows → exit 2, memo untouched")
    done = [(r, v or ("HOLD" if r.startswith("V") else
                      "MATCH" if r.startswith("I.") else "HOLD-SINCE-CLEAN"), e)
            for r, v, e in filled]
    check(memo_exit_code(done)[0] == 0,
          "write-memo: pre-filled table with blanks classified → exit 0")
    vfix = [{"id": f"V{1}", "body": "alpha"}, {"id": f"V{2}", "body": "beta"}]
    memo_ok = {"schema_version": MEMO_SCHEMA,
               "v_row_shas": {f"V{1}": row_body_sha("alpha"),
                              f"V{2}": row_body_sha("beta")}}
    check(dirty_v_ids(vfix, memo_ok, []) == [],
          "dirty-v: matching shas + no path-dirty → empty")
    memo_drift = {"schema_version": MEMO_SCHEMA,
                  "v_row_shas": {f"V{1}": row_body_sha("alpha"),
                                 f"V{2}": "deadbeef"}}
    check(dirty_v_ids(vfix, memo_drift, []) == [f"V{2}"],
          "dirty-v: v_row_shas drift → that id")
    check(dirty_v_ids(vfix, None, []) == [f"V{1}", f"V{2}"],
          "dirty-v: no memo → all V (first-run)")
    check(dirty_v_ids(vfix, memo_ok, [], full=True) == [f"V{1}", f"V{2}"],
          "dirty-v: --full → all V")
    vpath = [{"id": f"V{1}", "body": "see `skills/check/SKILL.md`"},
             {"id": f"V{2}", "body": "no path"}]
    memo_match = {"schema_version": MEMO_SCHEMA,
                  "v_row_shas": {f"V{1}": row_body_sha(vpath[0]["body"]),
                                 f"V{2}": row_body_sha(vpath[1]["body"])}}
    check(dirty_v_ids(vpath, memo_match, ["skills/check/SKILL.md"]) == [f"V{1}"],
          "dirty-v: v-path-dirty unions with sha set")
    check(flipped_since([], [{"id": f"T{1}", "body": "x|done"},
                             {"id": f"T{2}", "body": ".|open"}]) == [f"T{1}"],
          "flipped: first-run empty baseline → every current x")

    # emit-overview: non-§V sections verbatim + §V id list only (no bodies)
    spec_ov = ("## §G GOAL\n" "goal prose line\n"
               "## §C CONSTRAINTS\n" "- one constraint\n"
               "## §I INTERFACES\n" "- cmd: `foo bar` → out\n"
               "## §V INVARIANTS\n"
               "section preamble line\n"
               + _vrow(1, "first axiom body") + "\n"
               + _vrow(2, "second `a|b` body") + "\n"
               "## §T TASKS\n" "id|status|task|cites\n"
               + f"T{3}|x|do `a|b` thing|V{1}" + "\n"
               "## §B BUGS\n" "id|date|cause|fix\n")
    ov_secs, ov_order = parse_sections(spec_ov)
    ov = collect_overview(ov_secs, ov_order)
    check("goal prose line" in ov and "- one constraint" in ov,
          "emit-overview: §G/§C bodies verbatim")
    check(f"T{3}|x|do `a|b` thing|V{1}" in ov,
          "emit-overview: §T row body verbatim incl inner pipe")
    check(f"V{1},V{2}" in ov, "emit-overview: §V rendered as id list")
    check("first axiom body" not in ov and "second" not in ov
          and "section preamble line" not in ov,
          "emit-overview: no §V row bodies or preamble")
    check("## §V INVARIANTS" in ov and ov.index("## §I INTERFACES")
          < ov.index("## §V INVARIANTS") < ov.index("## §T TASKS"),
          "emit-overview: §V id list in observed section position")

    # token estimate
    check(audit_token_estimate(int(TOKEN_BUDGET * TOKEN_RATIO) + 1000), "token over fires")
    check(audit_token_estimate(100) == [], "token under silent")
    # estimate_tokens: single divisor realization, shared by audit + emit mode
    check(estimate_tokens(int(TOKEN_RATIO * 100)) == 100,
          "estimate_tokens: bytes / TOKEN_RATIO")
    check(estimate_tokens(0) == 0, "estimate_tokens: zero bytes → 0 tokens")
    check(estimate_tokens(int(TOKEN_BUDGET * TOKEN_RATIO) + 1000) > TOKEN_BUDGET,
          "estimate_tokens: over-budget bytes → est > budget")

    # per-skill-body token advisory (token-budget invariant): oversized
    # published SKILL.md body fires skill-token|ADVISORY; the drift-detector
    # consumes the row instead of hand-running the size check
    over = int(SKILL_TOKEN_BUDGET * TOKEN_RATIO) + 3400
    rows = skill_token_rows([("skills/x/SKILL.md", over)])
    check(len(rows) == 1 and rows[0][0] == "skill-token"
          and rows[0][1] == ADVISORY,
          "skill-token: over-budget body fires advisory row")
    check("skills/x/SKILL.md" in rows[0][2] and "> 5k" in rows[0][2]
          and "references/" in rows[0][2],
          "skill-token: evidence carries path, threshold, remedy")
    check(skill_token_rows([("skills/x/SKILL.md", 1000)]) == [],
          "skill-token: under-budget body silent")
    check(skill_token_rows([("skills/x/SKILL.md",
                             int(SKILL_TOKEN_BUDGET * TOKEN_RATIO))]) == [],
          "skill-token: at-budget boundary silent")
    check(len(skill_token_rows([("a/SKILL.md", over),
                                ("b/SKILL.md", over)])) == 2,
          "skill-token: one row per oversized body")

    # batch agent count (batch invariant): ceil(|V|/15) clamp [1,4]; PUBLISHED
    # census < ceil(|V|/2) → 1 regardless; census deterministic (closes §B.7)
    check(recommend_batch_count(0, 5) == 1, "batch: empty §V → 1 agent")
    check(recommend_batch_count(14, 50) == 1, "batch: <15 rows → base 1 agent")
    check(recommend_batch_count(16, 50) == 2, "batch: ceil(16/15) → 2 agents")
    check(recommend_batch_count(45, 50) == 3, "batch: ceil(45/15) → 3 agents")
    check(recommend_batch_count(60, 50) == 4, "batch: ceil(60/15) → 4 agents")
    check(recommend_batch_count(100, 50) == 4, "batch: ceil clamps at 4 agents")
    # narrow-scope override: census < ceil(|V|/2) collapses to 1 regardless
    check(recommend_batch_count(30, 14) == 1,
          "batch: census < ceil(|V|/2) → 1 agent (narrow scope)")
    check(recommend_batch_count(30, 15) == 2,
          "batch: census == ceil(|V|/2) → base count (not narrow)")
    check(recommend_batch_count(30, 50) == 2, "batch: wide census → base count")
    # audit emits the advisory row the drift-detector consumes
    bv = [{"id": f"V{i}"} for i in range(16)]
    check(audit_batch_advisory(bv, ["a.md"] * 16)
          == [("batch", ADVISORY, "recommended: 2 agents")],
          "batch: audit emits recommended-agents advisory row")
    check(audit_batch_advisory(bv, ["a.md"] * 4)
          == [("batch", ADVISORY, "recommended: 1 agents")],
          "batch: advisory honors narrow-scope override")

    # mechanize-pointer audit (mechanize-scan invariant): every user-invocable
    # SKILL.md carries a ## MECHANIZE section pointing at skills/_fragments/
    # MECHANIZE; sub-skills (user-invocable: false) excluded. No byte-identity.
    mblock = ("## MECHANIZE\n\n"
              "Load `${CLAUDE_PLUGIN_ROOT}/skills/_fragments/MECHANIZE.md`. "
              "Run probe.\n")
    mblock_nopointer = "## MECHANIZE\n\nscan body inlined — no fragment ptr\n"

    def _mk(fm_extra="", block=mblock, tail="\n## OUTPUT\n\nnext\n"):
        return ("---\nname: s\n" + fm_extra + "---\n\n# s\n\nintro\n\n"
                + block + tail)

    # frontmatter parse + user-invocable detection (frontmatter-only)
    check("user-invocable: false"
          in parse_frontmatter(_mk("user-invocable: false\n")),
          "parse_frontmatter: returns frontmatter block")
    check(parse_frontmatter("no fence\nbody") == "",
          "parse_frontmatter: absent fence → empty")
    check(is_user_invocable(_mk()) is True, "is_user_invocable: default true")
    check(is_user_invocable(_mk("user-invocable: false\n")) is False,
          "is_user_invocable: frontmatter false → false")
    body_mention = _mk(block="## MECHANIZE\n\nsets `user-invocable: "
                             "false` in prose; skills/_fragments/MECHANIZE.md\n")
    check(is_user_invocable(body_mention) is True,
          "is_user_invocable: body mention of flag ignored (frontmatter-only)")
    # block extraction: header → next H2, trailing blank trimmed; absent → None
    check(extract_mechanize_block(_mk()) == mblock.rstrip("\n"),
          "extract_mechanize_block: header to next H2, trailing blank trimmed")
    check(extract_mechanize_block(_mk(block="## NOPE\n\nx\n")) is None,
          "extract_mechanize_block: sentinel absent → None")
    check(extract_mechanize_block(_mk(tail="")) == mblock.rstrip("\n"),
          "extract_mechanize_block: block at EOF extracts")
    # pointer present → clean
    check(classify_mechanize_blocks({"a/SKILL.md": _mk(), "b/SKILL.md": _mk()})
          == [], "mechanize: pointer present → clean")
    # section present but pointer missing → DRIFT
    dr = classify_mechanize_blocks({"a/SKILL.md": _mk(),
                                    "c/SKILL.md": _mk(block=mblock_nopointer)})
    check(len(dr) == 1 and dr[0][1] == "DRIFT" and "c/SKILL.md" in dr[0][2],
          "mechanize: missing pointer flagged DRIFT")
    # user-invocable skill missing the section → MISSING
    mr = classify_mechanize_blocks({"a/SKILL.md": _mk(),
                                    "b/SKILL.md": _mk(block="## OTHER\n\nx\n")})
    check(any(v == "MISSING" and "b/SKILL.md" in e for _, v, e in mr),
          "mechanize: user-invocable skill missing section → MISSING")
    # sub-skill (user-invocable: false) without section excluded — no MISSING
    check(classify_mechanize_blocks(
        {"a/SKILL.md": _mk(),
         "sub/SKILL.md": _mk("user-invocable: false\n",
                             block="## OTHER\n\nx\n")}) == [],
          "mechanize: sub-skill without section excluded")
    # single pointed skill → clean
    check(classify_mechanize_blocks({"a/SKILL.md": _mk()}) == [],
          "mechanize: single pointed skill → clean")
    # DRIFT + MISSING make the run dirty; pseudo-id row unrestricted vocab
    check(compute_clean([("mechanize", "DRIFT", "")])[0] is False,
          "mechanize: DRIFT is dirty")
    check(compute_clean([("mechanize", "MISSING", "")])[0] is False,
          "mechanize: MISSING is dirty")
    check(validate_vocab([("mechanize", "DRIFT", "")]) == [],
          "mechanize: pseudo-id unrestricted vocab")

    # design-lifecycle post-approve: hand-off to github ISSUE + class --label
    # + Next github issue N; fold-design stays; github ISSUE accepts --label.
    sl_good = (
        "post-approve: hand title/body to github ISSUE; class --label\n"
        "Next: /sdd:spec github issue N\n"
        "fold-design optional same-session exclusion\n"
        "ISSUE body: Effect on in-flight SPEC items + Out of scope "
        "+ Unresolved when present + Acceptance\n"
    )
    sl_gh = "ISSUE: gh issue create --title t --body b --label enhancement\n"
    check(classify_design_post_approve(sl_good) == [],
          "design-lifecycle: complete recipe → clean")
    check(classify_design_post_approve(sl_good, sl_gh) == [],
          "design-lifecycle: github ISSUE --label present → clean")
    miss_cmd = classify_design_post_approve(
        "Next: /sdd:spec github issue N\nfold-design\n--label x\n")
    check(any(v == "VIOLATE" and "github ISSUE" in e
              for _, v, e in miss_cmd),
          "design-lifecycle: missing github ISSUE hand-off → VIOLATE")
    miss_label = classify_design_post_approve(
        "github ISSUE\nNext: /sdd:spec github issue N\nfold-design\n")
    check(any(v == "VIOLATE" and "--label" in e for _, v, e in miss_label),
          "design-lifecycle: missing class --label → VIOLATE")
    miss_next = classify_design_post_approve(
        "github ISSUE --label x\nfold-design\n")
    check(any(v == "VIOLATE" and "github issue" in e
              for _, v, e in miss_next),
          "design-lifecycle: missing github issue Next → VIOLATE")
    miss_fold = classify_design_post_approve(
        "github ISSUE --label x\nNext: /sdd:spec github issue N\n")
    check(any(v == "VIOLATE" and "fold-design" in e for _, v, e in miss_fold),
          "design-lifecycle: missing fold-design exclusion → VIOLATE")
    check(classify_design_post_approve("")[0][1] == "MISSING",
          "design-lifecycle: empty design body → MISSING")
    miss_effect = classify_design_post_approve(
        "github ISSUE --label x\nNext: /sdd:spec github issue N\n"
        "fold-design\nOut of scope\nUnresolved when present\n")
    check(any(v == "VIOLATE" and "Effect" in e
              for _, v, e in miss_effect),
          "design-lifecycle: missing ISSUE body Effect → VIOLATE")
    miss_oos = classify_design_post_approve(
        "github ISSUE --label x\nNext: /sdd:spec github issue N\n"
        "fold-design\nEffect on in-flight\nUnresolved when present\n")
    check(any(v == "VIOLATE" and "Out of scope" in e
              for _, v, e in miss_oos),
          "design-lifecycle: missing ISSUE body Out of scope → VIOLATE")
    miss_unres = classify_design_post_approve(
        "github ISSUE --label x\nNext: /sdd:spec github issue N\n"
        "fold-design\nEffect on in-flight\nOut of scope\n")
    check(any(v == "VIOLATE" and "Unresolved when present" in e
              for _, v, e in miss_unres),
          "design-lifecycle: missing ISSUE body Unresolved → VIOLATE")
    gh_miss = classify_design_post_approve(sl_good, "ISSUE: gh issue create\n")
    check(any(v == "VIOLATE" and "github" in e.lower() and "--label" in e
              for _, v, e in gh_miss),
          "design-lifecycle: github ISSUE missing --label → VIOLATE")
    check(classify_design_post_approve(sl_good, "")[0][1] == "MISSING"
          or any(v == "MISSING" and "github" in e.lower()
                 for _, v, e in classify_design_post_approve(sl_good, "")),
          "design-lifecycle: empty github body → MISSING")
    check(compute_clean([("design-lifecycle", "VIOLATE", "")])[0] is False,
          "design-lifecycle: VIOLATE is dirty")
    check(validate_vocab([("design-lifecycle", "VIOLATE", "")]) == [],
          "design-lifecycle: pseudo-id unrestricted vocab")

    # github-workflow PR-per-issue: gh issue develop + gh pr create --draft +
    # git push (PUSH) + load-and-run review + apply bug + suggestion +
    # gh pr ready (READY); leftover LINEAR / no-PR markers are VIOLATE
    # (github-workflow invariant).
    gw_good = (
        "BRANCH: gh issue develop n --checkout\n"
        "PR: gh pr create --draft; no review no Closes\n"
        "PUSH: git push issue-linked branch w/ open PR\n"
        "READY: load-and-run bundled review\n"
        "Apply open bug + suggestion; then gh pr ready\n"
        "chain runs once — owner = this PR three-step list\n"
        "No corresponding GitHub issue → no BRANCH, no PR "
        "(`gh pr create`).\n"
        "Missing issue → bail: no `gh issue develop`, "
        "no `git checkout -b`, no `gh pr create`.\n"
        "build fold-produced §T ids; spawn implies `--no-chain`\n"
        "Related: #<issue>\n"
        "push default branch then issue branch\n"
        "git commit --allow-empty\n"
        "before the spec delta\n"
        "missing SPEC.md still opens the PR\n"
        "no close trailer\n"
        "no review-at-create\n"
        "## CLOSE — unmerged\n"
        "1. gh pr close --delete-branch\n"
        "2. git switch <default-base>\n"
        "3. git branch -D <branch>\n"
    )
    check(classify_github_pr_per_issue(gw_good) == [],
          "github-workflow: complete PR-per-issue recipe → clean")
    gw_step = gw_good + "start at remainder (step 2).\n"
    check(any(v == "VIOLATE" and "cross-section step index" in e
              for _, v, e in classify_github_pr_per_issue(gw_step)),
          "github-workflow: READY remainder (step N) → VIOLATE")
    miss_dev = classify_github_pr_per_issue(
        "load-and-run review\nbug + suggestion\ngh pr create\n")
    check(any(v == "VIOLATE" and "gh issue develop" in e
              for _, v, e in miss_dev),
          "github-workflow: missing gh issue develop → VIOLATE")
    miss_pr = classify_github_pr_per_issue(
        "gh issue develop\nload-and-run review\nbug + suggestion\n"
        "git push\ngh pr ready\n")
    check(any(v == "VIOLATE" and "gh pr create --draft" in e
              for _, v, e in miss_pr),
          "github-workflow: missing gh pr create --draft → VIOLATE")
    miss_push = classify_github_pr_per_issue(
        "gh issue develop\ngh pr create --draft\nload-and-run review\n"
        "bug + suggestion\ngh pr ready\n")
    check(any(v == "VIOLATE" and "git push" in e for _, v, e in miss_push),
          "github-workflow: missing git push / PUSH → VIOLATE")
    miss_ready = classify_github_pr_per_issue(
        "gh issue develop\ngh pr create --draft\nload-and-run review\n"
        "bug + suggestion\ngit push\n")
    check(any(v == "VIOLATE" and "gh pr ready" in e for _, v, e in miss_ready),
          "github-workflow: missing gh pr ready → VIOLATE")
    miss_load = classify_github_pr_per_issue(
        "gh issue develop\ngh pr create\nbug + suggestion\n")
    check(any(v == "VIOLATE" and "load-and-run" in e
              for _, v, e in miss_load),
          "github-workflow: missing load-and-run review → VIOLATE")

    # github-workflow bundled review: doc-or-comment skip admitted;
    # load-and-run still required otherwise.
    # test_name_hint: doc-or-comment review skip
    grs_gh = (
        "Skip when the diff matches the github-workflow review skip "
        "(doc-or-comment diff).\n"
        "other diffs still run review\n"
        "load-and-run bundled review\n"
    )
    grs_frag = (
        "doc-or-comment diff\n"
        "other diffs still run review\n"
    )
    check(classify_github_review_skip(grs_gh, grs_frag) == [],
          "doc-or-comment review skip: skip plus load-and-run → clean")
    check(any(v == "VIOLATE" and "load-and-run review otherwise" in e
              for _, v, e in classify_github_review_skip(
                  "doc-or-comment\nother diffs still run review\n",
                  "doc-or-comment\nother diffs still run review\n")),
          "doc-or-comment review skip: skip without load-and-run → VIOLATE")
    check(any(v == "VIOLATE" and "skills/github/SKILL.md" in e
              and "doc-or-comment" in e
              for _, v, e in classify_github_review_skip(
                  "load-and-run\nother diffs still run review\n",
                  "doc-or-comment\nother diffs still run review\n")),
          "doc-or-comment review skip: github missing doc-or-comment "
          "→ VIOLATE")
    check(any(v == "VIOLATE" and "POST-SPEC-CHAIN.md" in e
              and "doc-or-comment" in e
              for _, v, e in classify_github_review_skip(
                  grs_gh, "other diffs still run review\nload-and-run\n")),
          "doc-or-comment review skip: fragment missing doc-or-comment "
          "→ VIOLATE")
    check(any(v == "VIOLATE" and "skills/github/SKILL.md" in e
              and "other diffs still run review" in e
              for _, v, e in classify_github_review_skip(
                  "doc-or-comment\nload-and-run\n",
                  "doc-or-comment\nother diffs still run review\n")),
          "doc-or-comment review skip: github missing other diffs "
          "→ VIOLATE")
    check(any(v == "VIOLATE" and "POST-SPEC-CHAIN.md" in e
              and "other diffs still run review" in e
              for _, v, e in classify_github_review_skip(
                  grs_gh, "doc-or-comment\n")),
          "doc-or-comment review skip: fragment missing other diffs "
          "→ VIOLATE")
    check(classify_github_review_skip("")[0][1] == "MISSING",
          "doc-or-comment review skip: empty github body → MISSING")

    miss_apply = classify_github_pr_per_issue(
        "gh issue develop\nload-and-run review\ngh pr create\n")
    check(any(v == "VIOLATE" and "bug + suggestion" in e
              for _, v, e in miss_apply),
          "github-workflow: missing apply bug + suggestion → VIOLATE")
    check(classify_github_pr_per_issue("")[0][1] == "MISSING",
          "github-workflow: empty github body → MISSING")
    gw_linear = gw_good + "Optional on the linear solo track (see LINEAR).\n"
    check(any(v == "VIOLATE" and "linear solo" in e.lower()
              for _, v, e in classify_github_pr_per_issue(gw_linear)),
          "github-workflow: leftover LINEAR optional-track → VIOLATE")
    check(any(v == "VIOLATE" and "## LINEAR" in e
              for _, v, e in classify_github_pr_per_issue(
                  gw_good + "## LINEAR — solo track (no PR)\n")),
          "github-workflow: leftover ## LINEAR heading → VIOLATE")
    check(compute_clean([("github-workflow", "VIOLATE", "")])[0] is False,
          "github-workflow: VIOLATE is dirty")
    check(validate_vocab([("github-workflow", "VIOLATE", "")]) == [],
          "github-workflow: pseudo-id unrestricted vocab")
    miss_no_issue = classify_github_pr_per_issue(
        "gh issue develop\ngh pr create --draft\ngit push\n"
        "load-and-run\nbug + suggestion\ngh pr ready\n"
        "chain runs once\n")
    check(any(v == "VIOLATE" and "no corresponding GitHub issue" in e
              for _, v, e in miss_no_issue),
          "github-workflow: missing no corresponding GitHub issue "
          "→ VIOLATE")
    check(any(v == "VIOLATE" and "no BRANCH, no PR" in e
              for _, v, e in miss_no_issue),
          "github-workflow: missing no BRANCH, no PR → VIOLATE")
    check(any(v == "VIOLATE" and "no gh pr create" in e
              for _, v, e in miss_no_issue),
          "github-workflow: missing no gh pr create without issue "
          "→ VIOLATE")

    # github-workflow MERGE squash subject holds #<issue> (not merely PR).
    # GitHub default (#PR) on --subject is VIOLATE even when Closes #<issue>
    # sits on another line (closes §B.39).
    # test_name_hint: github MERGE squash subject holds #<issue> (not merely PR)
    gm_good = (
        "## MERGE — squash\n"
        'ALLOW → gh pr merge --squash --subject "<title> (#<issue>)" '
        '--body "Closes #<issue>"\n'
    )
    check(classify_github_merge_subject(gm_good) == [],
          "github MERGE squash subject holds #<issue> (not merely PR): "
          "complete MERGE → clean")
    miss_gm_subject = classify_github_merge_subject(
        "## MERGE — squash\n"
        "gh pr merge --squash --delete-branch\n"
        "Closes #<issue>\n")
    check(any(v == "VIOLATE" and "--subject" in e
              for _, v, e in miss_gm_subject),
          "github MERGE: missing --subject → VIOLATE")
    miss_gm_pr_only = classify_github_merge_subject(
        "## MERGE — squash\n"
        'ALLOW → gh pr merge --squash --subject "<title> (#PR)"\n'
        "Closes #<issue> on PR body\n")
    check(any(v == "VIOLATE" and "not merely PR" in e
              for _, v, e in miss_gm_pr_only),
          "github MERGE squash subject holds #<issue> (not merely PR): "
          "--subject (#PR) without #<issue> on that line → VIOLATE")
    check(classify_github_merge_subject("")[0][1] == "MISSING",
          "github MERGE: empty github body → MISSING")

    # github-workflow MERGE check-probe (closes §B.72).
    # test_name_hint: github MERGE check-probe
    gp_good = (
        "## MERGE — ACCEPTANCE-GATE then squash\n"
        "Probe gh pr checks <pr> + "
        "gh pr view <pr> --json reviewDecision,mergeable\n"
        "Empty checks skip.\n"
    )
    check(classify_github_merge_probe(gp_good) == [],
          "github MERGE check-probe: complete MERGE → clean")
    miss_gp_checks = classify_github_merge_probe(
        "## MERGE\nreviewDecision,mergeable\n")
    check(any(v == "VIOLATE" and "gh pr checks" in e
              for _, v, e in miss_gp_checks),
          "github MERGE check-probe: missing gh pr checks → VIOLATE")
    miss_gp_json = classify_github_merge_probe(
        "## MERGE\ngh pr checks <pr>\n")
    check(any(v == "VIOLATE" and "reviewDecision,mergeable" in e
              for _, v, e in miss_gp_json),
          "github MERGE check-probe: missing reviewDecision,mergeable "
          "→ VIOLATE")
    check(classify_github_merge_probe("")[0][1] == "MISSING",
          "github MERGE check-probe: empty github body → MISSING")

    # github-workflow READY remainder no wait + fold-produced Acceptance
    # notes + re-run task verify + gh pr comment (closes §B.69, §B.70,
    # §B.71, §B.74).
    # test_name_hint: github READY remainder no-wait + fold-produced Acceptance-notes
    grr_good = (
        "Post-spec: apply open bug + suggestion; list nits; no wait.\n"
        "ids = new §T this fold + existing `.` rows that received "
        "Acceptance notes this fold\n"
        "re-run task verify. Fail → no gh pr ready.\n"
        "parent gh pr comment steno on draft PR\n"
    )
    check(classify_github_ready_remainder(grr_good) == [],
          "github READY remainder: complete recipe → clean")
    check(any(v == "VIOLATE" and "no wait" in e
              for _, v, e in classify_github_ready_remainder(
                  "Acceptance notes\nre-run task verify\ngh pr comment\n")),
          "github READY remainder: missing no wait → VIOLATE")
    check(any(v == "VIOLATE" and "Acceptance notes" in e
              for _, v, e in classify_github_ready_remainder(
                  "no wait\nre-run task verify\ngh pr comment\n")),
          "github READY remainder: missing Acceptance notes → VIOLATE")
    check(any(v == "VIOLATE" and "re-run task verify" in e
              for _, v, e in classify_github_ready_remainder(
                  "no wait\nAcceptance notes\ngh pr comment\n")),
          "github READY remainder: missing re-run task verify → VIOLATE")
    check(any(v == "VIOLATE" and "gh pr comment" in e
              for _, v, e in classify_github_ready_remainder(
                  "no wait\nAcceptance notes\nre-run task verify\n")),
          "github READY remainder: missing gh pr comment → VIOLATE")
    check(classify_github_ready_remainder("")[0][1] == "MISSING",
          "github READY remainder: empty github body → MISSING")
    check(classify_github_ready_remainder(
              "no wait\nre-run task verify\n",
              "Acceptance notes\ngh pr comment\n") == [],
          "github READY remainder: fold needles in fragment → clean")

    # github-workflow spec FOLD-IN github issue: push default, issue branch,
    # one non-delta commit, draft Related before the spec delta; missing
    # SPEC.md still opens the PR; no close trailer; no review-at-create;
    # spec stops before the chain; spec cites three-step chain
    # (READY remainder). The before-spec-delta block must not run
    # /sdd:build or load POST-SPEC-CHAIN, numbered or not.
    # POST-APPLY must not auto-chain run
    # (github-workflow invariant; closes §B.35, §B.36, §B.77).
    sf_good = (
        "**Before spec delta**\n"
        "1. push default branch\n"
        "2. issue branch: gh issue develop N --checkout\n"
        "3. git commit --allow-empty (not the spec delta)\n"
        "4. gh pr create --draft with Related: #<issue> "
        "before the spec delta; no close trailer; "
        "no review-at-create\n"
        "missing SPEC.md does not skip the pull request\n"
        "Spec stops before the chain.\n"
        "Non-github-issue APPLY: no github BRANCH, no github PR\n"
        "## APPLY\n"
        "## POST-APPLY\n"
        "post-spec-commit `/sdd:build` then READY remainder\n"
        "FOLD-IN github issue → load chain; Next merge when approved\n"
    )
    check(classify_spec_fold_github(sf_good) == [],
          "spec-fold-github: complete before-delta recipe → clean")
    sf_later = sf_good.replace(
        "## APPLY\n",
        "### FOLD-IN — github issue\n"
        "3. fold open bullets so `/sdd:build` can prove them\n"
        "## APPLY\n",
        1)
    check(classify_spec_fold_github(sf_later) == [],
          "spec-fold-github: later ### /sdd:build mention stays clean")
    miss_sf_dev = classify_spec_fold_github(
        "gh pr create --draft\nno close trailer\nno review-at-create\n"
        "/sdd:build\nREADY remainder\nstops at draft PR\n")
    check(any(v == "VIOLATE" and "gh issue develop" in e
              for _, v, e in miss_sf_dev),
          "spec-fold-github: missing gh issue develop → VIOLATE")
    miss_sf_draft = classify_spec_fold_github(
        "gh issue develop\nno close trailer\nno review-at-create\n"
        "/sdd:build\nREADY remainder\nstops at draft PR\n")
    check(any(v == "VIOLATE" and "gh pr create --draft" in e
              for _, v, e in miss_sf_draft),
          "spec-fold-github: missing gh pr create --draft → VIOLATE")
    miss_sf_trailer = classify_spec_fold_github(
        "gh issue develop\ngh pr create --draft\nno review-at-create\n"
        "/sdd:build\nREADY remainder\nstops at draft PR\n")
    check(any(v == "VIOLATE" and "no close trailer" in e
              for _, v, e in miss_sf_trailer),
          "spec-fold-github: missing no close trailer → VIOLATE")
    miss_sf_review = classify_spec_fold_github(
        "gh issue develop\ngh pr create --draft\nno close trailer\n"
        "/sdd:build\nREADY remainder\nstops at draft PR\n")
    check(any(v == "VIOLATE" and "no review-at-create" in e
              for _, v, e in miss_sf_review),
          "spec-fold-github: missing no review-at-create → VIOLATE")
    miss_sf_next = classify_spec_fold_github(
        "gh issue develop\ngh pr create --draft\nno close trailer\n"
        "no review-at-create\nREADY remainder\nstops at draft PR\n")
    check(any(v == "VIOLATE" and "/sdd:build" in e
              for _, v, e in miss_sf_next),
          "spec-fold-github: missing post-spec-commit /sdd:build cite → VIOLATE")
    miss_sf_ready = classify_spec_fold_github(
        "gh issue develop\ngh pr create --draft\nno close trailer\n"
        "no review-at-create\n/sdd:build\nstops at draft PR\n")
    check(any(v == "VIOLATE" and "READY remainder" in e
              for _, v, e in miss_sf_ready),
          "spec-fold-github: missing READY remainder cite → VIOLATE")
    miss_sf_stop = classify_spec_fold_github(
        "push default\ngh issue develop\n--allow-empty\n"
        "Related: #<issue>\nbefore the spec delta\nmissing SPEC.md\n"
        "gh pr create --draft\nno close trailer\n"
        "no review-at-create\n/sdd:build\nREADY remainder\n"
        "no github BRANCH, no github PR\n")
    check(any(v == "VIOLATE" and "stops before the chain" in e
              for _, v, e in miss_sf_stop),
          "spec-fold-github: missing spec stops before the chain "
          "→ VIOLATE")
    sf_runs = (
        "**After OK**\n"
        "1. gh issue develop N --checkout\n"
        "2. SPEC.md commit\n"
        "3. gh pr create --draft; no close trailer; no review-at-create\n"
        "4. run `/sdd:build --all` write-capable sub-agent\n"
        "Stops at draft PR.\n"
        "READY remainder\n"
        "## APPLY\n"
    )
    check(any(v == "VIOLATE" and "runs the post-spec chain" in e
              for _, v, e in classify_spec_fold_github(sf_runs)),
          "post-spec-commit chain once: Before spec delta numbered "
          "/sdd:build → VIOLATE")
    sf_unn = (
        "**Before spec delta**\n"
        "push default\ngh issue develop\n--allow-empty\n"
        "Related: #<issue>\nbefore the spec delta\nmissing SPEC.md\n"
        "gh pr create --draft\nno close trailer\nno review-at-create\n"
        "stops before the chain\n"
        "no github BRANCH, no github PR\n"
        "then run /sdd:build\n"
        "## POST-APPLY\n"
        "READY remainder\n"
    )
    check(any(v == "VIOLATE" and "runs the post-spec chain" in e
              for _, v, e in classify_spec_fold_github(sf_unn)),
          "post-spec-commit chain once: Before spec delta unnumbered "
          "/sdd:build → VIOLATE")
    sf_load = (
        "**Before spec delta**\n"
        "push default\ngh issue develop\n--allow-empty\n"
        "Related: #<issue>\nbefore the spec delta\nmissing SPEC.md\n"
        "gh pr create --draft\nno close trailer\nno review-at-create\n"
        "stops before the chain\n"
        "no github BRANCH, no github PR\n"
        "load skills/_fragments/POST-SPEC-CHAIN.md\n"
        "## POST-APPLY\n"
        "/sdd:build\nREADY remainder\n"
    )
    check(any(v == "VIOLATE" and "runs the post-spec chain" in e
              for _, v, e in classify_spec_fold_github(sf_load)),
          "post-spec-commit chain once: Before spec delta "
          "POST-SPEC-CHAIN load → VIOLATE")
    sf_dup = (
        sf_good.rsplit("## POST-APPLY", 1)[0]
        + "## POST-APPLY\n"
        "- FOLD-IN github issue → auto-chain run `/sdd:build --all`\n"
    )
    check(any(v == "VIOLATE" and "POST-APPLY auto-chain run" in e
              for _, v, e in classify_spec_fold_github(sf_dup)),
          "post-spec-commit chain once: POST-APPLY auto-chain run → VIOLATE")
    check(any(v == "VIOLATE" and "chain runs once" in e
              for _, v, e in classify_github_pr_per_issue(
                  "gh issue develop\ngh pr create --draft\ngit push\n"
                  "load-and-run\nbug + suggestion\ngh pr ready\n")),
          "post-spec-commit chain once: github missing chain runs once → VIOLATE")
    check(classify_spec_fold_github("")[0][1] == "MISSING",
          "spec-fold-github: empty spec body → MISSING")
    miss_sf_no_issue = classify_spec_fold_github(
        "gh issue develop\ngh pr create --draft\nno close trailer\n"
        "no review-at-create\n/sdd:build\nREADY remainder\n"
        "stops at draft PR\n")
    check(any(v == "VIOLATE" and "no BRANCH no PR" in e
              for _, v, e in miss_sf_no_issue),
          "spec-fold-github: missing non-issue no BRANCH no PR "
          "→ VIOLATE")
    check(any(v == "VIOLATE" and "push default" in e
              for _, v, e in classify_spec_fold_github(
                  sf_good.replace("push default", "PUSH"))),
          "spec-fold-github: missing push default → VIOLATE")
    check(any(v == "VIOLATE" and "--allow-empty" in e
              for _, v, e in classify_spec_fold_github(
                  sf_good.replace("--allow-empty", "empty-commit"))),
          "spec-fold-github: missing one non-delta commit → VIOLATE")
    check(any(v == "VIOLATE" and "before the spec delta" in e
              for _, v, e in classify_spec_fold_github(
                  sf_good.replace(
                      "before the spec delta", "after the spec commit"))),
          "spec-fold-github: missing draft before the spec delta "
          "→ VIOLATE")
    check(any(v == "VIOLATE" and "missing SPEC.md" in e
              for _, v, e in classify_spec_fold_github(
                  sf_good.replace("missing SPEC.md", "absent spec file"))),
          "spec-fold-github: missing SPEC.md still PR → VIOLATE")
    check(any(v == "VIOLATE" and "Related: #<issue>" in e
              for _, v, e in classify_spec_fold_github(
                  sf_good.replace("Related: #<issue>", "see issue"))),
          "spec-fold-github: missing Related: #<issue> → VIOLATE")
    check(any(v == "VIOLATE" and "push default" in e
              for _, v, e in classify_github_pr_per_issue(
                  gw_good.replace("push default", "PUSH"))),
          "github-workflow: missing push default → VIOLATE")
    check(any(v == "VIOLATE" and "issue branch" in e
              for _, v, e in classify_github_pr_per_issue(
                  gw_good.replace("issue branch", "linked checkout"))),
          "github-workflow: missing issue branch → VIOLATE")
    check(any(v == "VIOLATE" and "--allow-empty" in e
              for _, v, e in classify_github_pr_per_issue(
                  gw_good.replace("--allow-empty", "empty-commit"))),
          "github-workflow: missing one non-delta commit → VIOLATE")
    check(any(v == "VIOLATE" and "before the spec delta" in e
              for _, v, e in classify_github_pr_per_issue(
                  gw_good.replace(
                      "before the spec delta", "after the spec commit"))),
          "github-workflow: missing draft before the spec delta "
          "→ VIOLATE")
    check(any(v == "VIOLATE" and "missing SPEC.md" in e
              for _, v, e in classify_github_pr_per_issue(
                  gw_good.replace("missing SPEC.md", "absent spec file"))),
          "github-workflow: missing SPEC.md still PR → VIOLATE")
    check(any(v == "VIOLATE" and "no close trailer" in e
              for _, v, e in classify_github_pr_per_issue(
                  gw_good.replace("no close trailer", "trailer omitted"))),
          "github-workflow: missing no close trailer → VIOLATE")
    check(any(v == "VIOLATE" and "no review-at-create" in e
              for _, v, e in classify_github_pr_per_issue(
                  gw_good.replace(
                      "no review-at-create", "review deferred"))),
          "github-workflow: missing no review-at-create → VIOLATE")

    # write-serialize post-spec review spawn: scratch writes only; spawn
    # uses general-purpose Agent, not read-only Explore (closes §B.37).
    # test_name_hint: review scratch write
    rs_good = (
        "load-and-run bundled review as sub-agent\n"
        "Scratch writes only, no repo edits; "
        "spawn general-purpose Agent, not read-only Explore\n"
    )
    check(classify_review_scratch_write(rs_good) == [],
          "review scratch write: complete spawn recipe → clean")
    check(classify_review_scratch_write(
              "load-and-run bundled review as sub-agent\n",
              "Scratch writes only; spawn general-purpose Agent, not read-only Explore\n")
          == [],
          "review scratch write: needles in fragment → clean")
    check(any(v == "VIOLATE" and "scratch writes" in e
              for _, v, e in classify_review_scratch_write(
                  "spawn general-purpose Agent, not read-only Explore\n")),
          "review scratch write: missing scratch writes → VIOLATE")
    check(any(v == "VIOLATE" and "not read-only Explore" in e
              for _, v, e in classify_review_scratch_write(
                  "scratch writes only, no repo edits\n")),
          "review scratch write: missing uses general-purpose Agent, not read-only Explore "
          "→ VIOLATE")
    check(classify_review_scratch_write("")[0][1] == "MISSING",
          "review scratch write: empty github body → MISSING")
    check(compute_clean([("write-serialize", "VIOLATE", "")])[0] is False,
          "write-serialize: VIOLATE is dirty")
    check(validate_vocab([("write-serialize", "VIOLATE", "")]) == [],
          "write-serialize: pseudo-id unrestricted vocab")

    # POST-SPEC-CHILD=1 discriminator in build LOAD + github spawn prompt
    # (github-workflow + write-serialize; closes §B.38).
    # test_name_hint: POST-SPEC-CHILD=1
    psc_build = (
        "## LOAD\n"
        "4. If prompt or env token `POST-SPEC-CHILD=1` set → "
        "github PUSH only; drop READY\n"
    )
    psc_github = (
        "spawn prompt ! `POST-SPEC-CHILD=1`; child drops READY\n"
    )
    check(classify_post_spec_child(psc_build, psc_github) == [],
          "POST-SPEC-CHILD=1: build LOAD + github spawn → clean")
    check(classify_post_spec_child(
              psc_build, "run write-capable /sdd:build sub-agent\n",
              "spawn prompt ! `POST-SPEC-CHILD=1`\n") == [],
          "POST-SPEC-CHILD=1: github token in fragment → clean")
    check(any(v == "VIOLATE" and "build" in e and "POST-SPEC-CHILD=1" in e
              for _, v, e in classify_post_spec_child(
                  "## LOAD\nPUSH only; drop READY\n", psc_github)),
          "POST-SPEC-CHILD=1: build missing token → VIOLATE")
    check(any(v == "VIOLATE" and "github" in e and "POST-SPEC-CHILD=1" in e
              for _, v, e in classify_post_spec_child(
                  psc_build, "run write-capable /sdd:build --all sub-agent\n")),
          "POST-SPEC-CHILD=1: github missing token → VIOLATE")
    check(any(v == "MISSING" and "build" in e
              for _, v, e in classify_post_spec_child("", psc_github)),
          "POST-SPEC-CHILD=1: empty build body → MISSING")
    check(any(v == "MISSING" and "github" in e
              for _, v, e in classify_post_spec_child(psc_build, "")),
          "POST-SPEC-CHILD=1: empty github body → MISSING")

    # github-workflow build issue-linked pass: github PUSH then load-and-run
    # review-apply + gh pr ready; Next merge when approved.
    bi_good = (
        "Issue-linked pass: github PUSH then load-and-run review-apply "
        "+ push + gh pr ready. Next merge when approved.\n"
        "detector = issue linkage not planned close trailer; "
        "ALLOW @ build = evidence sufficient.\n"
    )
    check(classify_build_issue_linked(bi_good) == [],
          "build-issue-linked: complete pass recipe → clean")
    miss_bi_push = classify_build_issue_linked(
        "load-and-run review-apply\ngh pr ready\nmerge when approved\n")
    check(any(v == "VIOLATE" and "github PUSH" in e
              for _, v, e in miss_bi_push),
          "build-issue-linked: missing github PUSH → VIOLATE")
    miss_bi_load = classify_build_issue_linked(
        "github PUSH\ngh pr ready\nmerge when approved\n")
    check(any(v == "VIOLATE" and "load-and-run" in e
              for _, v, e in miss_bi_load),
          "build-issue-linked: missing load-and-run review-apply → VIOLATE")
    miss_bi_ready = classify_build_issue_linked(
        "github PUSH\nload-and-run\nmerge when approved\n")
    check(any(v == "VIOLATE" and "gh pr ready" in e
              for _, v, e in miss_bi_ready),
          "build-issue-linked: missing gh pr ready → VIOLATE")
    miss_bi_next = classify_build_issue_linked(
        "github PUSH\nload-and-run\ngh pr ready\n")
    check(any(v == "VIOLATE" and "merge when approved" in e
              for _, v, e in miss_bi_next),
          "build-issue-linked: missing Next merge when approved → VIOLATE")
    check(classify_build_issue_linked("")[0][1] == "MISSING",
          "build-issue-linked: empty build body → MISSING")
    miss_bi_link = classify_build_issue_linked(
        "github PUSH\nload-and-run\ngh pr ready\nmerge when approved\n"
        "evidence sufficient\n")
    check(any(v == "VIOLATE" and "issue linkage" in e
              for _, v, e in miss_bi_link),
          "build-issue-linked: missing issue linkage detector → VIOLATE")
    miss_bi_ev = classify_build_issue_linked(
        "github PUSH\nload-and-run\ngh pr ready\nmerge when approved\n"
        "issue linkage\n")
    check(any(v == "VIOLATE" and "evidence sufficient" in e
              for _, v, e in miss_bi_ev),
          "build-issue-linked: missing evidence sufficient → VIOLATE")

    # issue-linked READY skips check hop; Next item #1 merge phrasing;
    # /sdd:check listed not hopped (closes B63).
    # test_name_hint: issue-linked READY skips check hop
    ilrc_chain = (
        "issue-linked READY implies no check hop\n"
        "`/sdd:check` listed not hopped\n"
    )
    ilrc_next = (
        "after READY, Next item #1 names merge phrasing\n"
        "`/sdd:check` listed not hopped\n"
    )
    ilrc_build = (
        "unless issue-linked READY: hop check\n"
        "issue-linked READY implies no check hop\n"
        "`/sdd:check` listed not hopped\n"
    )
    check(classify_issue_linked_ready_chain(
              ilrc_chain, ilrc_next, ilrc_build) == [],
          "issue-linked READY chain: complete CHAIN+NEXT+build → clean")
    miss_ilrc_chain = classify_issue_linked_ready_chain(
        "POST-SPEC-CHILD never hops\n", ilrc_next, ilrc_build)
    check(any(v == "VIOLATE" and "CHAIN.md" in e
              and "issue-linked READY" in e
              for _, v, e in miss_ilrc_chain),
          "issue-linked READY chain: CHAIN missing issue-linked READY "
          "→ VIOLATE")
    miss_ilrc_hop = classify_issue_linked_ready_chain(
        "issue-linked READY\nlisted not hopped\n", ilrc_next, ilrc_build)
    check(any(v == "VIOLATE" and "CHAIN.md" in e and "no check hop" in e
              for _, v, e in miss_ilrc_hop),
          "issue-linked READY chain: CHAIN missing no check hop → VIOLATE")
    miss_ilrc_next = classify_issue_linked_ready_chain(
        ilrc_chain, "merge when approved\nlisted not hopped\n", ilrc_build)
    check(any(v == "VIOLATE" and "NEXT.md" in e and "item #1" in e
              for _, v, e in miss_ilrc_next),
          "issue-linked READY chain: NEXT missing item #1 → VIOLATE")
    miss_ilrc_listed = classify_issue_linked_ready_chain(
        ilrc_chain, "Next item #1 names merge\n", ilrc_build)
    check(any(v == "VIOLATE" and "NEXT.md" in e
              and "listed not hopped" in e
              for _, v, e in miss_ilrc_listed),
          "issue-linked READY chain: NEXT missing listed not hopped "
          "→ VIOLATE")
    miss_ilrc_build = classify_issue_linked_ready_chain(
        ilrc_chain, ilrc_next, "merge when approved\n")
    check(any(v == "VIOLATE" and "build/SKILL.md" in e
              and "issue-linked READY" in e
              for _, v, e in miss_ilrc_build),
          "issue-linked READY chain: build missing issue-linked READY "
          "→ VIOLATE")
    check(any(v == "MISSING" and "CHAIN.md" in e
              for _, v, e in classify_issue_linked_ready_chain(
                  "", ilrc_next, ilrc_build)),
          "issue-linked READY chain: empty CHAIN → MISSING")
    check(any(v == "MISSING" and "NEXT.md" in e
              for _, v, e in classify_issue_linked_ready_chain(
                  ilrc_chain, "", ilrc_build)),
          "issue-linked READY chain: empty NEXT → MISSING")
    check(any(v == "MISSING" and "build" in e
              for _, v, e in classify_issue_linked_ready_chain(
                  ilrc_chain, ilrc_next, "")),
          "issue-linked READY chain: empty build → MISSING")

    # acceptance-gate detector = issue linkage not close trailer;
    # ALLOW @ build = evidence sufficient; close trailer MERGE-only
    # (github-workflow invariant).
    # test_name_hint: acceptance-gate detector = issue linkage not close trailer
    agd_good = (
        "Fires on issue linkage, not planned close trailer.\n"
        "ALLOW @ build = evidence sufficient (no trailer).\n"
        "Close trailer MERGE-only.\n"
    )
    agd_gh = "Load skills/_fragments/ACCEPTANCE-GATE.md\n"
    check(classify_acceptance_gate_detect(agd_good, agd_gh) == [],
          "acceptance-gate detector = issue linkage not close trailer: "
          "complete fragment+github pointer → clean")
    miss_agd_frag = classify_acceptance_gate_detect(
        "evidence sufficient\nMERGE-only\n", agd_gh)
    check(any(v == "VIOLATE" and "ACCEPTANCE-GATE.md" in e
              and "issue linkage" in e for _, v, e in miss_agd_frag),
          "acceptance-gate detect: fragment missing issue linkage → VIOLATE")
    miss_agd_gh = classify_acceptance_gate_detect(
        agd_good, "issue linkage\nevidence sufficient\n")
    check(any(v == "VIOLATE" and "github/SKILL.md" in e
              and "ACCEPTANCE-GATE.md pointer" in e
              for _, v, e in miss_agd_gh),
          "acceptance-gate detect: github missing ACCEPTANCE-GATE.md "
          "pointer → VIOLATE")
    check(classify_acceptance_gate_detect("", "")[0][1] == "MISSING",
          "acceptance-gate detect: empty fragment → MISSING")

    # github-workflow README Issue-linked PR: draft PR after spec commit;
    # gh pr ready after review-apply; Closes only at merge.
    rm_good = (
        "gh issue develop then SPEC.md commit then gh pr create --draft\n"
        "build then review-apply then gh pr ready\n"
        "Closes only at merge after acceptance-gate\n"
        "No corresponding GitHub issue: no git branch, no GitHub PR\n"
        "squash commit subject holds #<issue>\n"
        "post-spec /sdd:build on fold-produced §T ids\n"
        "doc-or-comment diff skips bundled review\n"
    )
    check(classify_readme_issue_linked(rm_good) == [],
          "readme-issue-linked: complete Issue-linked PR → clean")
    miss_rm_draft = classify_readme_issue_linked(
        "gh pr ready\nonly at merge\n")
    check(any(v == "VIOLATE" and "draft PR" in e
              for _, v, e in miss_rm_draft),
          "readme-issue-linked: missing gh pr create --draft → VIOLATE")
    miss_rm_ready = classify_readme_issue_linked(
        "gh pr create --draft\nonly at merge\n")
    check(any(v == "VIOLATE" and "gh pr ready" in e
              for _, v, e in miss_rm_ready),
          "readme-issue-linked: missing gh pr ready → VIOLATE")
    miss_rm_merge = classify_readme_issue_linked(
        "gh pr create --draft\ngh pr ready\n")
    check(any(v == "VIOLATE" and "only at merge" in e
              for _, v, e in miss_rm_merge),
          "readme-issue-linked: missing Closes only at merge → VIOLATE")
    check(classify_readme_issue_linked("")[0][1] == "MISSING",
          "readme-issue-linked: empty README → MISSING")
    miss_rm_no_issue = classify_readme_issue_linked(
        "gh pr create --draft\ngh pr ready\nonly at merge\n")
    check(any(v == "VIOLATE" and "no corresponding GitHub issue" in e
              for _, v, e in miss_rm_no_issue),
          "readme-issue-linked: missing no corresponding GitHub issue "
          "→ VIOLATE")
    check(any(v == "VIOLATE" and "no git branch, no GitHub PR" in e
              for _, v, e in miss_rm_no_issue),
          "readme-issue-linked: missing no git branch, no GitHub PR "
          "→ VIOLATE")
    miss_rm_issue_subj = classify_readme_issue_linked(
        "gh pr create --draft\ngh pr ready\nonly at merge\n"
        "No corresponding GitHub issue: no git branch, no GitHub PR\n")
    check(any(v == "VIOLATE" and "#<issue>" in e
              for _, v, e in miss_rm_issue_subj),
          "readme-issue-linked: missing squash #<issue> → VIOLATE")
    miss_rm_fold = classify_readme_issue_linked(
        "gh pr create --draft\ngh pr ready\nonly at merge\n"
        "No corresponding GitHub issue: no git branch, no GitHub PR\n"
        "#<issue>\n")
    check(any(v == "VIOLATE" and "fold-produced" in e
              for _, v, e in miss_rm_fold),
          "readme-issue-linked: missing fold-produced §T ids → VIOLATE")
    miss_rm_skip = classify_readme_issue_linked(
        rm_good.replace("doc-or-comment diff skips bundled review\n", ""))
    check(any(v == "VIOLATE" and "doc-or-comment" in e
              for _, v, e in miss_rm_skip),
          "readme-issue-linked: missing doc-or-comment review skip "
          "→ VIOLATE")
    rm_all = rm_good + "then auto /sdd:build --all sub-agent\n"
    check(any(v == "VIOLATE" and "/sdd:build --all" in e
              for _, v, e in classify_readme_issue_linked(rm_all)),
          "readme-issue-linked: post-spec /sdd:build --all → VIOLATE")

    # leftover LINEAR-no-PR wording (github-workflow invariant): sweep-scope
    # grep LINEAR|solo linear|no PR required on skill/fragment/README surfaces;
    # backtick-wrapped tokens exempt; SPEC.md out of scope.
    ln_hit = classify_linear_no_pr(
        {"a.md": "keep the LINEAR heading\n"})
    check(len(ln_hit) == 1 and ln_hit[0][0] == "linear-no-pr"
          and ln_hit[0][1] == "VIOLATE" and "a.md:1" in ln_hit[0][2],
          "linear-no-pr: LINEAR heading → VIOLATE")
    check(any("solo linear" in e or "leftover" in e
              for _, _, e in classify_linear_no_pr(
                  {"b.md": "the solo linear path is gone\n"})),
          "linear-no-pr: solo linear → VIOLATE")
    check(any("no PR required" in e or "leftover" in e
              for _, _, e in classify_linear_no_pr(
                  {"c.md": "solo, no PR required\n"})),
          "linear-no-pr: no PR required → VIOLATE")
    check(classify_linear_no_pr(
              {"d.md": "every issue gets one issue-linked PR\n"}) == [],
          "linear-no-pr: PR-per-issue wording → clean")
    check(classify_linear_no_pr(
              {"e.md": "the `LINEAR` token is a historical name\n"}) == [],
          "linear-no-pr: backtick-wrapped LINEAR exempt")
    check(compute_clean([("linear-no-pr", "VIOLATE", "")])[0] is False,
          "linear-no-pr: VIOLATE is dirty")
    check(validate_vocab([("linear-no-pr", "VIOLATE", "")]) == [],
          "linear-no-pr: pseudo-id unrestricted vocab")

    # dispatch-target audit (response-shape + sub-skill-flags invariants, closes
    # §B.14): no skill body slash-dispatches an auto-fire sub-skill; the slash
    # form is never user-invocable. Plugin name from the manifest, sub-skill set
    # frontmatter-only, backtick-wrapped form exempt (verbatim-preservation).
    d_plugins = ["sdd"]
    d_subs = {"backprop", "monitor"}
    bad_d = classify_dispatch_targets(
        {"skills/build/SKILL.md": "intro\nroute cause to /sdd:backprop F5\nend\n"},
        d_plugins, d_subs)
    check(len(bad_d) == 1 and bad_d[0][0] == "dispatch" and bad_d[0][1] == "VIOLATE"
          and "skills/build/SKILL.md:2" in bad_d[0][2]
          and "/sdd:backprop" in bad_d[0][2],
          "dispatch: non-backtick slash form → VIOLATE, line-numbered")
    check(classify_dispatch_targets(
        {"a/SKILL.md": "the `/sdd:backprop` skill is read-only\n"},
        d_plugins, d_subs) == [],
          "dispatch: backtick-wrapped slash form exempt")
    check(classify_dispatch_targets(
        {"a/SKILL.md": "route through /sdd:spec then /sdd:build\n"},
        d_plugins, d_subs) == [],
          "dispatch: user-invocable slash target not flagged")
    check(classify_dispatch_targets(
        {"a/SKILL.md": "/other:backprop elsewhere\n"}, d_plugins, d_subs) == [],
          "dispatch: non-manifest plugin slash form not matched")
    check(classify_dispatch_targets(
        {"a/SKILL.md": "/sdd:backproptest is a different name\n"},
        d_plugins, d_subs) == [],
          "dispatch: word-boundary guards sub-skill-name prefix")
    check(classify_dispatch_targets(
        {"a/SKILL.md": "/sdd:backprop\n"}, [], d_subs) == [],
          "dispatch: empty plugin set → no audit")
    check(classify_dispatch_targets(
        {"a/SKILL.md": "/sdd:backprop\n"}, d_plugins, set()) == [],
          "dispatch: empty sub-skill set → no audit")
    # frontmatter-only sub-skill derivation: a user-invocable skill that mentions
    # the flag in prose stays user-invocable, and its live slash form is flagged
    fm_sub = "---\nname: backprop\nuser-invocable: false\n---\n\nbody\n"
    fm_ui = ("---\nname: build\n---\n\nmentions `user-invocable: false` in prose\n"
             "then routes to /sdd:backprop live\n")
    dd = classify_dispatch_targets_from_texts(
        {"skills/backprop/SKILL.md": fm_sub,
         "skills/build/SKILL.md": fm_ui}, d_plugins)
    check(len(dd) == 1 and "skills/build/SKILL.md" in dd[0][2],
          "dispatch: sub-skill set frontmatter-only; user-invocable body slash flagged")
    check(compute_clean([("dispatch", "VIOLATE", "")])[0] is False,
          "dispatch: VIOLATE is dirty")
    check(validate_vocab([("dispatch", "VIOLATE", "")]) == [],
          "dispatch: pseudo-id unrestricted vocab")
    # plugin name from the manifest (plugin-shape invariant)
    check(plugin_names("/no/such/repo") == [], "plugin_names: absent manifest → empty")

    # allowed-tools grant-use audit (tooling-preference invariant): a frontmatter
    # grant the body never invokes is zero-body-use → VIOLATE. Sound — flagged only
    # on total body-absence. Realized once here, retiring the hand-run grant sweep.
    def _gk(tools, body):
        return f"---\nname: s\nallowed-tools: {tools}\n---\n\n# s\n\n{body}\n"

    # token split keeps a Bash arg pattern as one token
    check(split_grant_tokens(
            "Read, Bash(python3 */check-mechanical.py *), grep")
          == ["Read", "Bash(python3 */check-mechanical.py *)",
              "grep"],
          "grant: paren-aware token split")
    toks_g, ln_g = find_allowed_tools(
        _gk("Read, grep", "allowed-tools: Edit here"))
    check(toks_g == ["Read", "grep"] and ln_g == 3,
          "grant: allowed-tools parsed w/ lineno, body line ignored")
    check(find_allowed_tools("no fence\nallowed-tools: Read\n") == (None, None),
          "grant: no frontmatter → no grants")
    check(grant_used("Read", "first Read `SPEC.md`"), "grant_used: token present")
    check(grant_used("Read", "Load `skills/_fragments/X.md`"),
          "grant_used: load → read")
    check(grant_used("grep", "we grep the files"), "grant_used: lowercase token")
    check(grant_used("Agent", "spawn Explore sub-agents"),
          "grant_used: alias Explore → agent-spawner")
    check(grant_used("Edit", "rewrite the rows in place"),
          "grant_used: operation verb rewrite → editor")
    check(not grant_used("grep", "this body never searches"),
          "grant_used: absent tool → unused")
    check(grant_used("Bash(git *)", "run `git commit -- paths`"),
          "grant_used: Bash arg anchor present")
    check(not grant_used("Bash(jq *)", "no json tooling here"),
          "grant_used: Bash arg anchor absent → unused")
    check(grant_used("Bash", "the recipe runs `python3 scripts/x.py`"),
          "grant_used: bare Bash + command token")
    check(not grant_used("Bash", "pure prose, no commands"),
          "grant_used: bare Bash, no command → unused")
    check(grant_used("skill", "follows the telegraph skill rules"),
          "grant_used: dispatcher generous (any mention)")
    rows_g = classify_grants({"skills/x/SKILL.md": _gk(
        "Read, list_dir", "Read `SPEC.md` then bail")})
    check(len(rows_g) == 1 and rows_g[0][0] == "grant" and rows_g[0][1] == "VIOLATE"
          and "list_dir" in rows_g[0][2] and "skills/x/SKILL.md:3" in rows_g[0][2],
          "classify_grants: unused grant flagged, used grant silent, line-numbered")
    check(classify_grants({"skills/y/SKILL.md": _gk("Read", "Read the file")})
          == [],
          "classify_grants: all-used → clean")
    check(classify_grants({"skills/z/SKILL.md": "# no frontmatter\nbody\n"}) == [],
          "classify_grants: no allowed-tools and no prescription → no rows")
    # reverse: body-prescribed catalogued tool with no grant → VIOLATE
    rows_miss_spawn = classify_grants({"skills/g/SKILL.md": _gk(
        "Bash(gh *)",
        "run write-capable sub-agent then `gh issue view`")})
    check(any(v == "VIOLATE" and "Agent" in e and "missing grant" in e
              for _, v, e in rows_miss_spawn),
          "classify_grants reverse: missing Agent → VIOLATE")
    rows_miss_edit = classify_grants({"skills/e/SKILL.md": _gk(
        "Grep", "rewrite the rows in place then grep files")})
    check(any(v == "VIOLATE" and "Edit" in e and "missing grant" in e
              for _, v, e in rows_miss_edit),
          "classify_grants reverse: missing Edit → VIOLATE")
    rows_miss_read = classify_grants({"skills/r/SKILL.md": _gk(
        "Grep", "Load `skills/_fragments/X.md` then grep")})
    check(any(v == "VIOLATE" and "Read" in e and "missing grant" in e
              for _, v, e in rows_miss_read),
          "classify_grants reverse: missing Read → VIOLATE")
    rows_miss_write = classify_grants({"skills/w/SKILL.md": _gk(
        "Grep", "write delta to `SPEC.md` then grep")})
    check(any(v == "VIOLATE" and "Write" in e and "missing grant" in e
              for _, v, e in rows_miss_write),
          "classify_grants reverse: missing write → VIOLATE")
    rows_miss_plan = classify_grants({"skills/design/SKILL.md": _gk(
        "Grep", "write the plan file then grep")})
    check(any(v == "VIOLATE" and "Write" in e and "missing grant" in e
              for _, v, e in rows_miss_plan),
          "classify_grants reverse: missing write (plan file) → VIOLATE")
    # disallowed-tools skip reverse (documented denial is not a missing grant)
    dis_txt = ("---\nname: s\nallowed-tools: Grep\n"
               "disallowed-tools: Edit, Write\n---\n\n"
               "# s\n\nrewrite the rows then grep files\n")
    check(classify_grants({"skills/d/SKILL.md": dis_txt}) == [],
          "classify_grants reverse: disallowed-tools skips missing grant")
    toks_d, _ = find_disallowed_tools(dis_txt)
    check(toks_d == ["Edit", "Write"],
          "grant: disallowed-tools parsed")
    both_ok = classify_grants({"skills/ok/SKILL.md": _gk(
        "Read, Edit, Write, Agent, "
        "Bash(gh *)",
        "Load `skills/_fragments/X.md` then spawn a sub-agent; "
        "rewrite the rows; write delta to `SPEC.md`; run `gh pr ready`")})
    check(both_ok == [],
          "classify_grants: extra+missing both clean when grants match body")
    # pseudo-id row: VIOLATE is dirty, unrestricted vocab
    check(compute_clean([("grant", "VIOLATE", "")])[0] is False,
          "grant: VIOLATE is dirty")
    check(validate_vocab([("grant", "VIOLATE", "")]) == [],
          "grant: pseudo-id unrestricted vocab")

    # clean-set + vocab
    clean_rows = [(f"V{1}", "HOLD", ""), (f"V{2}", "VIOLATE-CAPTURED", ""),
                  ("token", ADVISORY, "")]
    dirty_rows = [(f"V{1}", "VIOLATE", ""), ("format", "VIOLATE", "")]
    check(compute_clean(clean_rows)[0] is True, "clean-set admits captured+advisory")
    check(compute_clean(dirty_rows)[0] is False, "clean-set rejects violate")
    check(validate_vocab([(f"V{1}", "BOGUS", "")]), "vocab rejects bogus V verdict")
    check(validate_vocab([("format", "VIOLATE", "")]) == [], "vocab allows pseudo-id")
    # per-row-type vocab (drift-verdict-vocab invariant): MATCH is §I-clean, §I-only
    check(validate_vocab([("I.api", "MATCH", "")]) == [], "vocab admits MATCH on §I row")
    check(validate_vocab([("I.api", "DRIFT", "")]) == [], "vocab admits DRIFT on §I row")
    check(validate_vocab([(f"V{1}", "MATCH", "")]),
          "vocab rejects MATCH on §V row (§I-only)")
    check(validate_vocab([("I.api", "HOLD", "")]),
          "vocab rejects §V silent verdict on §I row")
    check(validate_vocab([(f"T{9}", "STALE", "")]) == [], "vocab admits STALE on §T row")
    check(validate_vocab([(f"T{9}", "MATCH", "")]), "vocab rejects MATCH on §T row")
    check(validate_vocab([("I.api", "", "")]) != [], "vocab rejects blank typed skeleton verdict")
    check(validate_vocab([("batch", "", "")]) == [], "vocab skips blank pseudo-id verdict")
    check(compute_clean([("I.api", "MATCH", "")])[0] is True, "clean-set: MATCH is clean")
    check(compute_clean([("I.api", "DRIFT", "")])[0] is False, "clean-set: DRIFT is dirty")
    # write-memo --from-audit merge (memo invariant): the mechanical audit unions
    # the behavioral rows, so a dirty mechanical finding flips an otherwise-clean
    # behavioral set — the script owns the clean decision, no hand-merge.
    behav_clean = [(f"V{1}", "HOLD", ""), ("I.api", "MATCH", "")]
    mech_dirty = [("format", "VIOLATE", "format: bad")]
    check(compute_clean(behav_clean)[0] is True, "from-audit: behavioral set alone clean")
    check(compute_clean(mech_dirty + behav_clean)[0] is False,
          "from-audit: mechanical VIOLATE flips merged set dirty")
    # write-memo exit codes (memo invariant): 2 invalid vocab, 1 dirty (memo
    # untouched, CI-gateable), 0 clean; vocab failure outranks dirtiness
    check(memo_exit_code([(f"V{1}", "BOGUS", "")])[0] == 2,
          "write-memo: invalid vocab → exit 2")
    check(memo_exit_code([(f"V{1}", "VIOLATE", "")])[0] == 1,
          "write-memo: behavioral VIOLATE → exit 1")
    check(memo_exit_code(mech_dirty + behav_clean)[0] == 1,
          "write-memo: merged mechanical VIOLATE → exit 1")
    check(memo_exit_code([(f"V{1}", "HOLD", ""), ("I.api", "MATCH", ""),
                          ("token", ADVISORY, "")])[0] == 0,
          "write-memo: clean → exit 0")
    check(memo_exit_code([(f"V{1}", "BOGUS", ""), (f"V{2}", "VIOLATE", "")])[0] == 2,
          "write-memo: invalid vocab outranks dirty → exit 2")

    # human-facing naked-symbol audit (symbol-set + human-clarity invariants):
    # naked symbol in prose flagged; backtick span + fenced block exempt; clean
    # spelled-out prose silent; multi-symbol line → one row listing each;
    # scanning resumes after a fence closes
    naked = "the loop is human → grok and a & b"
    check(any(v == "VIOLATE" for _, v, _ in scan_human_symbols("p", naked)),
          "human-symbols: naked arrow / ampersand flagged")
    bt = "the `a → b` mapping costs about 40 percent"
    check(scan_human_symbols("p", bt) == [], "human-symbols: backtick span exempt")
    fenced = "```\na → b\n```\nclean prose here"
    check(scan_human_symbols("p", fenced) == [], "human-symbols: fenced block exempt")
    clean = "spelled out: at least, at most, and, about 40 percent"
    check(scan_human_symbols("p", clean) == [], "human-symbols: spelled-out prose clean")
    multi = "x ≥ y ≤ z ~ w"
    rows = scan_human_symbols("p", multi)
    check(len(rows) == 1 and all(s in rows[0][2] for s in ("≥", "≤", "~")),
          "human-symbols: multiple symbols on a line → one row listing each")
    after_fence = "```\na → b\n```\nthen x → y in plain prose"
    check(any(v == "VIOLATE" for _, v, _ in scan_human_symbols("p", after_fence)),
          "human-symbols: scanning resumes after fence close")

    # archive markers: required only for sections w/ archived rows; range +
    # count must match the archived id set (closes empty §B.0 marker class)
    _ams = {"T": [(5, f"## archived: §T.{1}..§T.{2} → SPEC.archive.md (2 rows)")],
            "B": []}
    _aid = {"T": {f"T{1}", f"T{2}"}, "B": set(), "V": set()}
    check(audit_archive_markers(_ams, True, False, _aid) == [],
          "archive marker: §T marked, §B w/o archived rows needs no marker")
    _ams0 = dict(_ams, B=[(9, f"## archived: §B.{0}..§B.{0} → SPEC.archive.md (0 rows)")])
    check(any("claims archived rows" in e
              for _, _, e in audit_archive_markers(_ams0, True, False, _aid)),
          "archive marker: marker over zero archived rows → VIOLATE")
    _amsx = {"T": [(5, f"## archived: §T.{1}..§T.{3} → SPEC.archive.md (3 rows)")],
             "B": []}
    check(any("range/count" in e
              for _, _, e in audit_archive_markers(_amsx, True, False, _aid)),
          "archive marker: range/count mismatch → VIOLATE")
    check(any("§T missing archive marker" in e
              for _, _, e in audit_archive_markers({"T": [], "B": []}, True,
                                                   False, _aid)),
          "archive marker: archived §T rows w/o marker → VIOLATE")

    # CLAUDE.md presence + direct-instruction marker block (human-clarity
    # invariant): absent → MISSING, present-without-block → VIOLATE, present
    # with well-formed begin/end block → clean (silent); end-before-begin →
    # VIOLATE. Symbol-cleanliness rides the human-symbol scan, not re-checked.
    check(classify_claude_md(None)[0][1] == "MISSING",
          "claude-md: absent file → MISSING")
    check(classify_claude_md("# CLAUDE.md\nno marker here")[0][1] == "VIOLATE",
          "claude-md: present without marker block → VIOLATE")
    well_formed = f"intro\n{CLAUDE_MARKER_BEGIN}\nrules\n{CLAUDE_MARKER_END}\nrest"
    check(classify_claude_md(well_formed) == [],
          "claude-md: well-formed marker block → clean")
    end_first = f"{CLAUDE_MARKER_END}\nrules\n{CLAUDE_MARKER_BEGIN}"
    check(classify_claude_md(end_first)[0][1] == "VIOLATE",
          "claude-md: end-before-begin marker → VIOLATE")


    # human-facing banned-idiom audit (human-clarity invariant): a banned idiom /
    # jargon-idiom phrase in prose flagged; backtick span + fenced block exempt;
    # literal prose silent; multi-phrase line → one row listing each; ambiguous
    # single word ("smell") excluded; scanning resumes after a fence closes.
    idiom_naked = "that framing is load-bearing and earns its keep"
    ir = scan_human_idiom("p", idiom_naked)
    check(len(ir) == 1 and ir[0][0] == "idiom" and ir[0][1] == "VIOLATE"
          and "load-bearing" in ir[0][2] and "earns its" in ir[0][2],
          "human-idiom: banned phrases flagged, one row listing each")
    check(scan_human_idiom("p", "the `load-bearing` token is exempt") == [],
          "human-idiom: backtick span exempt")
    check(scan_human_idiom("p", "```\nload-bearing\n```\nclean prose here") == [],
          "human-idiom: fenced block exempt")
    check(scan_human_idiom("p", "this framing matters; the term is essential") == [],
          "human-idiom: literal prose clean")
    check(scan_human_idiom("p", "a code smell here and a small bite") == [],
          "human-idiom: ambiguous single words excluded")
    check(any("smells like" in e for _, _, e
              in scan_human_idiom("p", "this smells like under-specification")),
          "human-idiom: multi-word metaphor 'smells like' flagged")
    after_idiom = "```\nload-bearing\n```\nthen low-hanging fruit in plain prose"
    check(any(v == "VIOLATE" for _, v, _ in scan_human_idiom("p", after_idiom)),
          "human-idiom: scanning resumes after fence close")
    check(compute_clean([("idiom", "VIOLATE", "")])[0] is False,
          "human-idiom: VIOLATE is dirty")
    check(validate_vocab([("idiom", "VIOLATE", "")]) == [],
          "human-idiom: pseudo-id unrestricted vocab")

    # sembr multi-sentence-line advisory (sembr invariant): a prose line
    # holding two sentences → one ADVISORY row; single sentence clean; fence /
    # pipe-table / frontmatter / blockquote / backtick-span exempt; a list
    # marker is not a boundary; abbreviation + ellipsis guarded; ADVISORY is
    # never dirty; scanning resumes after a fence closes.
    two = "First sentence here. Second sentence follows."
    sr = scan_sembr("p", two)
    check(len(sr) == 1 and sr[0][0] == "sembr" and sr[0][1] == ADVISORY,
          "sembr: multi-sentence prose line → one ADVISORY row")
    check(scan_sembr("p", "One sentence per line stays silent.") == [],
          "sembr: single-sentence line clean")
    check(scan_sembr("p", f"```\n{two}\n```") == [],
          "sembr: fenced block exempt")
    check(scan_sembr("p", "| a. B | c. D |") == [],
          "sembr: pipe-table row exempt")
    check(scan_sembr("p", f"---\ndesc: |\n  {two}\n---") == [],
          "sembr: frontmatter exempt")
    check(scan_sembr("p", "> Quoted copy. Two sentences fine.") == [],
          "sembr: blockquote exempt")
    check(scan_sembr("p", "1. Read the file per plan.") == [],
          "sembr: list marker is not a sentence boundary")
    check(scan_sembr("p", "guard fires on e.g. Uppercase and stops... Then") == [],
          "sembr: abbreviation + ellipsis guarded")
    check(scan_sembr("p", "code span `a. B` stays exempt.") == [],
          "sembr: backtick span exempt")
    check(any(v == ADVISORY for _, v, _ in
              scan_sembr("p", f"```\n{two}\n```\n{two}")),
          "sembr: scanning resumes after fence close")
    check(compute_clean([("sembr", ADVISORY, "")])[0] is True,
          "sembr: ADVISORY never dirty")
    check(validate_vocab([("sembr", ADVISORY, "")]) == [],
          "sembr: pseudo-id unrestricted vocab")

    # fix-sembr splitter (sembr + mechanical-realization invariants): one
    # splitter shared with the scan — plain / bullet / numbered / indented
    # split shapes, marker-width continuation indent, backtick-span + abbrev
    # guards ride the shared boundary finder, rejoin-equivalence holds, the
    # pure rewrite core leaves exempt lines byte-identical, preserves the
    # trailing newline, and is idempotent.
    check(split_sembr_line(two) ==
          ["First sentence here.", "Second sentence follows."],
          "fix-sembr: plain two-sentence line splits at the boundary")
    check(split_sembr_line("- One done. Two follow.") ==
          ["- One done.", "  Two follow."],
          "fix-sembr: bullet continuation indents to the text column")
    check(split_sembr_line("2. Stop here. Then go on.") ==
          ["2. Stop here.", "   Then go on."],
          "fix-sembr: numbered-list continuation indents to the text column")
    check(split_sembr_line("   Alpha beta. Gamma delta.") ==
          ["   Alpha beta.", "   Gamma delta."],
          "fix-sembr: indented prose keeps its own indent")
    check(split_sembr_line("One sentence only stays whole.") is None,
          "fix-sembr: single-sentence line untouched (None)")
    check(split_sembr_line("span `a. B` holds tight. Next one starts.") ==
          ["span `a. B` holds tight.", "Next one starts."],
          "fix-sembr: backtick span never splits, real boundary does")
    check(split_sembr_line("see e.g. Alpha stays put. Real split lands.") ==
          ["see e.g. Alpha stays put.", "Real split lands."],
          "fix-sembr: abbreviation guard rides the shared splitter")
    check(all(bool(sembr_split_points(l)) == bool(scan_sembr("p", l))
              for l in (two, "One sentence per line stays silent.",
                        "1. Read the file per plan.")),
          "fix-sembr: scan flags exactly the lines the splitter would rewrite")
    fixture = f"```\n{two}\n```\n{two}\n"
    fixed, rewrites, trips = fix_sembr_text(fixture)
    check(fixed == f"```\n{two}\n```\nFirst sentence here.\n"
                   f"Second sentence follows.\n"
          and list(rewrites) == [4] and trips == [],
          "fix-sembr: rewrite core splits prose only, fence + newline kept")
    refixed, rerewrites, _ = fix_sembr_text(fixed)
    check(refixed == fixed and rerewrites == {},
          "fix-sembr: rewrite is idempotent")

    # discover_repo_local: cite-DAG repo-local file set walks `.spec/**` +
    # `.claude/**` + repo-root README/CLAUDE (scope-set invariant)
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, ".spec"))
        os.makedirs(os.path.join(td, ".claude", "skills"))
        for rel in (os.path.join(".spec", "check-extras.md"),
                    os.path.join(".claude", "skills", "note.md"),
                    "README.md"):
            with open(os.path.join(td, rel), "w", encoding="utf-8") as f:
                f.write("§V.1\n")
        with open(os.path.join(td, ".spec", "check-state.json"),
                  "w", encoding="utf-8") as f:
            f.write("{}\n")
        rels = {os.path.relpath(p, td) for p in discover_repo_local(td)}
        check(os.path.join(".spec", "check-extras.md") in rels,
              "discover_repo_local: .spec/check-extras.md in cite-DAG file set")
        check(os.path.join(".claude", "skills", "note.md") in rels
              and "README.md" in rels,
              "discover_repo_local: .claude/** walk + repo-root set intact")
        check(os.path.join(".spec", "check-state.json") not in rels,
              "discover_repo_local: md-only filter excludes memo json")

    # prune-pattern set: sole member source (freshness-contract +
    # mechanical-realization invariants) — emitted set == compiled detectors
    check([p["id"] for p in PRUNE_PATTERNS] ==
          ["amendment-counter", "dated-retirement", "supersession-narration",
           "closes-fold", "backtick-span", "cite-modifier",
           "retired-in-place"],
          "prune-patterns: member ids + order stable")
    roles = [p["role"] for p in PRUNE_PATTERNS]
    check(roles.count("residue") == 3 and roles.count("fold") == 1
          and roles.count("pre-filter") == 3,
          "prune-patterns: role tags residue/fold/pre-filter")
    check(HR_DATED.pattern == next(p["pattern"] for p in PRUNE_PATTERNS
                                   if p["id"] == "dated-retirement")
          and PF_RETIRED_INPLACE is _PRUNE_RE["retired-in-place"],
          "prune-patterns: audit detectors compiled from the set")
    fold_pat = next(p["pattern"] for p in PRUNE_PATTERNS
                    if p["id"] == "closes-fold")
    check(bool(re.search(fold_pat, f"row body. Closes §B.{7}.")),
          "prune-patterns: closes-fold matches standalone sentence")
    check(bool(PF_RETIRED_INPLACE.match(f"V{9}:  retired  2026-01-01 — x"))
          and bool(PF_RETIRED_INPLACE.match(f"V{9}: retired 2026-01-01 — x")),
          "prune-patterns: retired-in-place whitespace-tolerant "
          "(reorganize grep parity)")
    # discover_sembr_files includes skills/_fragments/** (sembr invariant +
    # §B.29): fragment .md paths join the prose set so multi-sentence fragment
    # lines are audited + fix-sembr-reachable.
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, ".claude-plugin"))
        with open(os.path.join(td, ".claude-plugin", "plugin.json"), "w",
                  encoding="utf-8") as f:
            f.write('{"name":"t"}\n')
        frag_dir = os.path.join(td, "skills", "_fragments")
        os.makedirs(frag_dir)
        frag_path = os.path.join(frag_dir, "X.md")
        with open(frag_path, "w", encoding="utf-8") as f:
            f.write("One line.\n")
        found = discover_sembr_files(td)
        check(frag_path in found,
              "sembr-discover: skills/_fragments/** .md in file set")
        check(frag_path in discover_sembr_fragments(td),
              "sembr-discover: fragment helper lists _fragments .md")
        empty_td = os.path.join(td, "empty-plugin")
        os.makedirs(os.path.join(empty_td, ".claude-plugin"))
        with open(os.path.join(empty_td, ".claude-plugin", "plugin.json"), "w",
                  encoding="utf-8") as f:
            f.write('{"name":"e"}\n')
        check(discover_sembr_fragments(empty_td) == [],
              "sembr-discover: missing _fragments dir → empty")

    # ARCHIVE_CLOSED_T mirrors the token-budget closed-§T archive threshold
    # (token-budget invariant + §B.32) — single source for condense prong 3.
    check(ARCHIVE_CLOSED_T == 50,
          "token-budget: ARCHIVE_CLOSED_T == 50 (condense prong 3 source)")
    check(isinstance(ARCHIVE_CLOSED_T, int) and ARCHIVE_CLOSED_T > 0,
          "token-budget: ARCHIVE_CLOSED_T positive int")
    check(CHECK_DISPATCH_ARGS == frozenset(
              {"", "--full", "--no-chain", "--full --no-chain"}),
          "check-dispatch: CHECK_DISPATCH_ARGS single-sources V47 arg set")
    # CLOSE order: switch after branch -D → VIOLATE
    gw_bad_close = gw_good.replace(
        "2. git switch <default-base>\n"
        "3. git branch -D <branch>\n",
        "2. git branch -D <branch>\n"
        "3. git switch <default-base>\n")
    check(any(v == "VIOLATE" and "git switch must precede" in e
              for _, v, e in classify_github_pr_per_issue(gw_bad_close)),
          "github-workflow: CLOSE branch -D before git switch → VIOLATE")
    gw_no_del = gw_good.replace("gh pr close --delete-branch", "gh pr close")
    check(any(v == "VIOLATE" and "CLOSE missing gh pr close --delete-branch" in e
              for _, v, e in classify_github_pr_per_issue(gw_no_del)),
          "github-workflow: CLOSE missing --delete-branch → VIOLATE")
    miss_related = classify_github_pr_per_issue(
        gw_good.replace("Related: #<issue>\n", ""))
    check(any(v == "VIOLATE" and "Related: #<issue>" in e
              for _, v, e in miss_related),
          "github-workflow: missing PR Related: #<issue> → VIOLATE")

    # emit-archive-window: skip under threshold; archive older / keep newest over
    # (token-budget + archive-semantics + mechanical-realization)
    aw_under = [{"id": f"T{i}", "body": "x|done"} for i in range(1, 6)]
    aw_skip = emit_archive_window(aw_under, threshold=10)
    check(len(aw_skip) == 1 and aw_skip[0]["action"] == "skip"
          and aw_skip[0]["count"] == 0,
          "emit-archive-window: closed ≤ threshold → skip")
    aw_exact = [{"id": f"T{i}", "body": "x|done"} for i in range(1, 11)]
    check(emit_archive_window(aw_exact, threshold=10)[0]["action"] == "skip",
          "emit-archive-window: closed == threshold → skip")
    # open §T ignored; over threshold → archive older id-asc + keep newest N
    aw_mix = ([{"id": f"T{i}", "body": "x|done"} for i in range(1, 8)]
              + [{"id": f"T{8}", "body": ".|open"},
                 {"id": f"T{9}", "body": "x|done"},
                 {"id": f"T{10}", "body": "x|done"}])
    aw_over = emit_archive_window(aw_mix, threshold=5)
    check(len(aw_over) == 2
          and aw_over[0]["action"] == "archive"
          and aw_over[1]["action"] == "keep",
          "emit-archive-window: over threshold → archive + keep rows")
    check(aw_over[0]["tid_lo"] == f"T{1}" and aw_over[0]["tid_hi"] == f"T{4}"
          and aw_over[0]["count"] == 4,
          "emit-archive-window: archive older closed id-asc (open excluded)")
    check(aw_over[1]["tid_lo"] == f"T{5}" and aw_over[1]["tid_hi"] == f"T{10}"
          and aw_over[1]["count"] == 5 and aw_over[1]["marker"] == "",
          "emit-archive-window: keep newest N closed live")
    check(ARCHIVE_MARK_TB.match(aw_over[0]["marker"]) is not None
          and f"({4} rows)" in aw_over[0]["marker"],
          "emit-archive-window: marker matches SPEC-FORMAT §T form")
    # default threshold is ARCHIVE_CLOSED_T (single source; not a skill hardcode)
    many = [{"id": f"T{i}", "body": "x|d"} for i in range(1, ARCHIVE_CLOSED_T + 3)]
    aw_def = emit_archive_window(many)
    check(aw_def[0]["action"] == "archive" and aw_def[0]["count"] == 2
          and aw_def[1]["count"] == ARCHIVE_CLOSED_T,
          "emit-archive-window: default threshold = ARCHIVE_CLOSED_T")
    check(emit_archive_window([])[0]["action"] == "skip",
          "emit-archive-window: empty §T → skip")

    # emit-condense-propose: five labeled tables, columns unchanged vs
    # standalone formatters (mechanical-realization + mechanize-scan)
    empty_cp = collect_condense_propose([], [], [])
    check([n for n, _ in empty_cp] == list(CONDENSE_PROPOSE_TABLES),
          "emit-condense-propose: five tables in named order")
    check(empty_cp[3][1] == "section|id|pattern|line",
          "emit-condense-propose: empty residue → header only")
    check(empty_cp[2][1].splitlines()[0]
          == "action|tid_lo|tid_hi|count|marker"
          and empty_cp[2][1].splitlines()[1].startswith("skip|"),
          "emit-condense-propose: empty §T → archive-window skip")
    # columns unchanged: combined tables == standalone formatters on same input
    cp_tables = [
        ("fold-seeds", format_fold_seeds_table(seeds)),
        ("superseded", format_superseded_table(cand)),
        ("archive-window", format_archive_window_table(aw_over)),
        ("residue", format_residue_table(res_mix)),
        ("v-weights", format_v_weights_table(ranked)),
    ]
    cp_blob = format_condense_propose(cp_tables)
    cp_parsed = parse_condense_propose(cp_blob)
    check(list(cp_parsed.keys()) == list(CONDENSE_PROPOSE_TABLES),
          "emit-condense-propose: parse yields five named blocks")
    check(cp_parsed["fold-seeds"] == format_fold_seeds_table(seeds),
          "emit-condense-propose: fold-seeds columns unchanged")
    check(cp_parsed["superseded"] == format_superseded_table(cand),
          "emit-condense-propose: superseded columns unchanged")
    check(cp_parsed["archive-window"] == format_archive_window_table(aw_over),
          "emit-condense-propose: archive-window columns unchanged")
    check(cp_parsed["residue"] == format_residue_table(res_mix),
          "emit-condense-propose: residue columns unchanged")
    check(cp_parsed["v-weights"] == format_v_weights_table(ranked),
          "emit-condense-propose: v-weights columns unchanged")
    check("## archived:" in cp_parsed["archive-window"]
          and cp_parsed["archive-window"].splitlines()[0]
          == "action|tid_lo|tid_hi|count|marker",
          "emit-condense-propose: archive-marker stays inside table block")
    check(cp_parsed["fold-seeds"].splitlines()[0] == "cluster_members|co_citers"
          and cp_parsed["superseded"].splitlines()[0]
          == "tid|superseded_v|original_cites"
          and cp_parsed["residue"].splitlines()[0] == "section|id|pattern|line"
          and cp_parsed["v-weights"].splitlines()[0]
          == "v_row|bytes|tokens|cum_pct|heavy",
          "emit-condense-propose: standalone headers preserved")

    # condense prong 6 consumes stub-skip from the v-weights table
    # (token-budget invariant; no re-extract).
    cp6_good = (
        "Heavy set = v-weights table.\n"
        "Consume stub-skip from table (no re-extract).\n"
    )
    check(classify_condense_stub_skip(cp6_good) == [],
          "condense prong-6: stub-skip + no re-extract → clean")
    check(any(v == "VIOLATE" and "stub-skip" in e
              for _, v, e in classify_condense_stub_skip(
                  "no re-extract of stubs\n")),
          "condense prong-6: missing stub-skip → VIOLATE")
    check(any(v == "VIOLATE" and "no re-extract" in e
              for _, v, e in classify_condense_stub_skip(
                  "consume stub-skip from table\n")),
          "condense prong-6: missing no re-extract → VIOLATE")
    check(classify_condense_stub_skip("")[0][1] == "MISSING",
          "condense prong-6: empty body → MISSING")

    # acceptance-gate parse + verdict (github-workflow invariant; closes §B.34)
    # test_name_hint: acceptance_gate_blocks_unproven_close
    ag_body = (
        "## Problem\n\nSomething broke.\n\n"
        "## Acceptance\n\n"
        "- [ ] load linked issue Acceptance\n"
        "- [x] already checked criterion\n"
        "- [ ] post evidence comment\n\n"
        "## Other\n\nIgnore me.\n"
    )
    ag_bullets = parse_acceptance_bullets(ag_body)
    check(ag_bullets is not None and len(ag_bullets) == 3,
          "acceptance-gate: parse three bullets under ## Acceptance")
    check(ag_bullets[0]["text"] == "load linked issue Acceptance"
          and ag_bullets[0]["checked"] is False,
          "acceptance-gate: first bullet open")
    check(ag_bullets[1]["checked"] is True,
          "acceptance-gate: second bullet checked")
    check(parse_acceptance_bullets("## Problem\n\nNo gate here.\n") is None,
          "acceptance-gate: missing ## Acceptance → None")
    check(parse_acceptance_bullets("## Acceptance\n\nNo bullets yet.\n") == [],
          "acceptance-gate: empty section → empty list")
    check(acceptance_gate_verdict(None, []) == "ADVISORY",
          "acceptance-gate: no section → ADVISORY (not silent-verified)")
    check(acceptance_gate_verdict(ag_bullets, []) == "BLOCK",
          "acceptance_gate_blocks_unproven_close")
    check(acceptance_gate_verdict(
              ag_bullets,
              ["load linked issue Acceptance"]) == "BLOCK",
          "acceptance-gate: partial evidence still BLOCK")
    check(acceptance_gate_verdict(
              ag_bullets,
              ["load linked issue Acceptance",
               "post evidence comment"]) == "ALLOW",
          "acceptance-gate: all open proven → ALLOW")
    check(acceptance_gate_verdict(
              [{"text": "done", "checked": True}], []) == "ALLOW",
          "acceptance-gate: only checked bullets → ALLOW")
    check(acceptance_gate_verdict(ag_bullets, [0, 2]) == "ALLOW",
          "acceptance-gate: index-based proven set → ALLOW")

    # gitignore guard: first `.spec/` write lists both cache files
    # (backprop-resume-card invariant; T85)
    with tempfile.TemporaryDirectory() as td:
        ensure_gitignore_guard(td)
        gi = os.path.join(td, ".spec", ".gitignore")
        text = read_text(gi)
        check(text.splitlines() == list(SPEC_GITIGNORE_CACHE),
              "gitignore-guard: missing file → both cache lines in order")
        ensure_gitignore_guard(td)
        check(read_text(gi) == text,
              "gitignore-guard: second call idempotent")
        partial = os.path.join(td, "partial")
        os.makedirs(os.path.join(partial, ".spec"))
        partial_gi = os.path.join(partial, ".spec", ".gitignore")
        with open(partial_gi, "w", encoding="utf-8") as f:
            f.write("check-state.json")  # no trailing newline
        ensure_gitignore_guard(partial)
        check(read_text(partial_gi).splitlines()
              == ["check-state.json", "backprop-handoff.json"],
              "gitignore-guard: appends handoff; repairs missing newline")
        extra = os.path.join(td, "extra")
        os.makedirs(os.path.join(extra, ".spec"))
        extra_gi = os.path.join(extra, ".spec", ".gitignore")
        with open(extra_gi, "w", encoding="utf-8") as f:
            f.write("# keep\nbackprop-handoff.json\n")
        ensure_gitignore_guard(extra)
        extra_lines = read_text(extra_gi).splitlines()
        check(extra_lines[0] == "# keep"
              and "backprop-handoff.json" in extra_lines
              and extra_lines[-1] == "check-state.json"
              and extra_lines.count("backprop-handoff.json") == 1,
              "gitignore-guard: preserves extra lines; appends missing memo")

    # skill-effort invariant: model unset; explain+check pin medium;
    # other skills leave effort unset; README honored sentence names effort.
    def _se(name, extra=""):
        return (f"---\nname: {name}\n{extra}---\n\n# {name}\n\n"
                "body mentions model: grok and effort: high\n")

    _se_readme = (
        "SKILL.md frontmatter is honored on dispatch: `description`, "
        "`user-invocable`, and `effort`.\n"
    )
    _se_ok = {
        "explain": _se("explain", "effort: medium\n"),
        "check": _se("check", "effort: medium\n"),
        "build": _se("build"),
    }
    check(classify_skill_effort(_se_ok, _se_readme) == [],
          "skill-effort: pins medium, others unset, README names effort "
          "→ clean; body model/effort ignored")
    _se_quoted = dict(_se_ok)
    _se_quoted["check"] = _se("check", 'effort: "medium"\n')
    check(classify_skill_effort(_se_quoted, _se_readme) == [],
          "skill-effort: quoted medium counts as medium")
    _se_model = dict(_se_ok)
    _se_model["build"] = _se("build", "model: grok\n")
    check(any(v == "VIOLATE" and "sets model" in e
              for _, v, e in classify_skill_effort(_se_model, _se_readme)),
          "skill-effort: frontmatter model → VIOLATE")
    _se_high = dict(_se_ok)
    _se_high["explain"] = _se("explain", "effort: high\n")
    check(any(v == "VIOLATE" and "explain" in e and "high" in e
              for _, v, e in classify_skill_effort(_se_high, _se_readme)),
          "skill-effort: explain effort other than medium → VIOLATE")
    _se_unset = dict(_se_ok)
    _se_unset["explain"] = _se("explain")
    check(any(v == "VIOLATE" and "explain" in e and "unset" in e
              for _, v, e in classify_skill_effort(_se_unset, _se_readme)),
          "skill-effort: explain effort unset → VIOLATE")
    _se_low = dict(_se_ok)
    _se_low["check"] = _se("check", "effort: low\n")
    check(any(v == "VIOLATE" and "check" in e and "low" in e
              for _, v, e in classify_skill_effort(_se_low, _se_readme)),
          "skill-effort: check effort other than medium → VIOLATE")
    _se_extra = dict(_se_ok)
    _se_extra["build"] = _se("build", "effort: medium\n")
    check(any(v == "VIOLATE" and "build" in e and "sets effort" in e
              for _, v, e in classify_skill_effort(_se_extra, _se_readme)),
          "skill-effort: other skill effort line → VIOLATE")
    check(any(v == "VIOLATE" and "does not name effort" in e
              for _, v, e in classify_skill_effort(
                  _se_ok,
                  "SKILL.md frontmatter is honored on dispatch: "
                  "`description` and `user-invocable`.\n")),
          "skill-effort: honored sentence omits effort → VIOLATE")
    check(any(v == "VIOLATE" and "sentence missing" in e
              for _, v, e in classify_skill_effort(
                  _se_ok, "Product readme. No honored sentence.\n")),
          "skill-effort: honored-frontmatter sentence missing → VIOLATE")
    _se_gone = dict(_se_ok)
    del _se_gone["explain"]
    check(any(v == "VIOLATE" and "explain" in e and "missing" in e
              for _, v, e in classify_skill_effort(_se_gone, _se_readme)),
          "skill-effort: missing explain skill → VIOLATE")
    _se_indent = dict(_se_ok)
    _se_indent["build"] = (
        "---\nname: build\ndescription: |\n"
        "  model: grok-x\n"
        "  effort: high\n"
        "---\n\nbody\n"
    )
    check(classify_skill_effort(_se_indent, _se_readme) == [],
          "skill-effort: indented description model/effort ignored")

    _pi_ids = ("design-lifecycle", "github-workflow", "write-serialize",
               "linear-no-pr", "symbols", "idiom", "skill-effort")

    def _pi_dirty(rows):
        out = []
        for rid, v, e in rows:
            if v not in DIRTY_VERDICTS:
                continue
            if rid in _pi_ids or (rid == "token" and v in ("MISSING", "VIOLATE")):
                out.append((rid, v, e))
        return out

    _min_spec = (
        "## §G GOAL\n" "goal\n"
        "## §C CONSTRAINTS\n" "- one\n"
        "## §I INTERFACES\n" "- cmd: `foo` → out\n"
        "## §V INVARIANTS\n"
        + _vrow(1, "first axiom") + "\n"
        "## §T TASKS\n" "id|status|task|cites\n"
        + f"T{1}|x|do thing|V{1}\n"
        "## §B BUGS\n" "id|date|cause|fix\n"
    )
    with tempfile.TemporaryDirectory() as td:
        spec_p = os.path.join(td, "SPEC.md")
        with open(spec_p, "w", encoding="utf-8") as f:
            f.write(_min_spec)
        with open(os.path.join(td, "README.md"), "w", encoding="utf-8") as f:
            f.write("Requires GNU Make ≥ 4.4. Product readme. "
                    "LINEAR track. No draft PR needles.\n")
        with open(os.path.join(td, "CLAUDE.md"), "w", encoding="utf-8") as f:
            f.write("This framing is load-bearing.\n")
        hook_dir = os.path.join(td, ".spec", "scripts")
        os.makedirs(hook_dir)
        hook = os.path.join(hook_dir, "check-extras.sh")
        with open(hook, "w", encoding="utf-8") as f:
            f.write("#!/bin/sh\necho 'hook|ADVISORY|extras-hook ran'\n")
        os.chmod(hook, 0o755)
        check(plugin_dirs(td) == [],
              "consumer-core-profile: no .claude-plugin/ → plugin_dirs empty")
        empty_rows = run_audit(td, "SPEC.md")
        check(_pi_dirty(empty_rows) == [],
              "consumer-core-profile: empty plugin_dirs → no plugin-internal "
              "MISSING/VIOLATE")
        check(not any(rid in _pi_ids for rid, _, _ in empty_rows),
              "consumer-core-profile: empty plugin_dirs → no plugin-internal "
              "rows at all")
        check(any(rid == "hook" and "extras-hook ran" in e
                  for rid, _, e in empty_rows),
              "consumer-core-profile: empty plugin_dirs → extras-hook still")
        check(any(rid == "memo" and v == ADVISORY
                  for rid, v, _ in empty_rows),
              "consumer-core-profile: empty plugin_dirs → memo still")
        check(not any(rid == "symbols" and v == "VIOLATE"
                      for rid, v, _ in empty_rows),
              "consumer-core-profile: empty plugin_dirs + README ≥ → "
              "no symbols VIOLATE")
        check(not any(rid == "idiom" and v == "VIOLATE"
                      for rid, v, _ in empty_rows),
              "consumer-core-profile: empty plugin_dirs → no idiom VIOLATE")
        check(any(rid == "sembr" and v == ADVISORY
                  for rid, v, _ in empty_rows),
              "consumer-core-profile: empty plugin_dirs → sembr ADVISORY stays")
        check(compute_clean(empty_rows)[0] is True,
              "consumer-core-profile: consumer SPEC + product README → "
              "mechanical table clean")
        pad = "x" * (int(TOKEN_BUDGET * TOKEN_RATIO) + 200)
        with open(spec_p, "w", encoding="utf-8") as f:
            f.write(_min_spec.replace("goal\n", pad + "\n").replace(
                _vrow(1, "first axiom"),
                _vrow(1, "first axiom retired 2026-01-02")).replace(
                f"T{1}|x|do thing|V{1}",
                f"T{1}|x|do thing|V{99}"))
        stay_rows = run_audit(td, "SPEC.md")
        check(any(rid == "cite" and v == "UNRESOLVED"
                  for rid, v, _ in stay_rows),
              "consumer-core-profile: empty plugin_dirs → cite-DAG still")
        check(any(rid == "history" and v == "VIOLATE"
                  for rid, v, _ in stay_rows),
              "consumer-core-profile: empty plugin_dirs → history still")
        check(any(rid == "token" and v == ADVISORY
                  for rid, v, _ in stay_rows),
              "consumer-core-profile: empty plugin_dirs → token-budget still")
        check(_pi_dirty(stay_rows) == [],
              "consumer-core-profile: stay-running rows do not add "
              "plugin-internal dirty")
        os.makedirs(os.path.join(td, ".claude-plugin"))
        with open(os.path.join(td, ".claude-plugin", "plugin.json"), "w",
                  encoding="utf-8") as f:
            f.write('{"name":"t","note":"x ≥ y"}\n')
        check(plugin_dirs(td) == [td],
              "consumer-core-profile: plugin.json → plugin_dirs non-empty")
        other_rows = run_audit(td, "SPEC.md", run_hook=False)
        check(not any(rid in ("design-lifecycle", "github-workflow",
                              "write-serialize", "skill-effort")
                      for rid, _, _ in other_rows),
              "consumer-core-profile: non-sdd plugin → no sdd-only needle rows")
        check(any(rid == "symbols" and v == "VIOLATE"
                  for rid, v, _ in other_rows),
              "consumer-core-profile: non-sdd plugin still audits symbols")
        with open(os.path.join(td, ".claude-plugin", "plugin.json"), "w",
                  encoding="utf-8") as f:
            f.write('{"name":"sdd","note":"x ≥ y"}\n')
        plugin_rows = run_audit(td, "SPEC.md", run_hook=False)
        check(any(rid == "design-lifecycle" and v in DIRTY_VERDICTS
                  for rid, v, _ in plugin_rows),
              "consumer-core-profile: non-empty plugin_dirs still audits "
              "design-lifecycle")
        check(any(rid == "github-workflow" and v in DIRTY_VERDICTS
                  for rid, v, _ in plugin_rows),
              "consumer-core-profile: non-empty plugin_dirs still audits "
              "github-workflow")
        check(any(rid == "write-serialize" and v in DIRTY_VERDICTS
                  for rid, v, _ in plugin_rows),
              "consumer-core-profile: non-empty plugin_dirs still audits "
              "write-serialize")
        check(any(rid == "token" and v in ("MISSING", "VIOLATE")
                  for rid, v, _ in plugin_rows),
              "consumer-core-profile: non-empty plugin_dirs still audits "
              "condense-stub token")
        check(any(rid == "linear-no-pr" and v in DIRTY_VERDICTS
                  for rid, v, _ in plugin_rows),
              "consumer-core-profile: non-empty plugin_dirs still audits "
              "linear-no-pr")
        check(any(rid == "skill-effort" and v in DIRTY_VERDICTS
                  for rid, v, _ in plugin_rows),
              "consumer-core-profile: non-empty plugin_dirs still audits "
              "skill-effort")
        check(any(rid == "symbols" and v == "VIOLATE" and "README.md" in e
                  for rid, v, e in plugin_rows),
              "consumer-core-profile: non-empty plugin_dirs still audits "
              "symbols vs README")
        check(any(rid == "idiom" and v == "VIOLATE" and "CLAUDE.md" in e
                  for rid, v, e in plugin_rows),
              "consumer-core-profile: non-empty plugin_dirs still audits "
              "idiom vs CLAUDE.md")
        check(any(rid == "symbols" and v == "VIOLATE" and "plugin.json" in e
                  for rid, v, e in plugin_rows),
              "consumer-core-profile: non-empty plugin_dirs still audits "
              "symbols vs manifests")

    if fails:
        sys.stderr.write("SELF-TEST FAIL:\n  " + "\n  ".join(fails) + "\n")
        return 1
    print(f"self-test OK ({_selftest_count()} assertions)")
    return 0


def _selftest_count():
    # informational; kept in sync loosely with the check() calls above
    return 414


# --- entry -------------------------------------------------------------------

def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--self-test" in argv:
        return selftest()
    parser = argparse.ArgumentParser(prog="check-mechanical",
                                     description="deterministic mechanical audits")
    parser.add_argument("mode", choices=["audit", "write-memo", "fix-sembr",
                                         "emit-v-slices", "emit-superseded",
                                         "emit-fold-seeds", "emit-v-weights",
                                         "emit-row-ids", "emit-overview",
                                         "emit-token-estimate",
                                         "emit-prune-patterns", "emit-residue",
                                         "emit-archive-window",
                                         "emit-condense-propose",
                                         "emit-check-agent-prompt"])
    parser.add_argument("--repo-root", default=os.environ.get("CHECK_REPO_ROOT", "."))
    parser.add_argument("--spec", default="SPEC.md")
    parser.add_argument("--no-hook", action="store_true",
                        help="skip the REPO-LOCAL check-extras.sh probe")
    parser.add_argument("--no-chain", action="store_true",
                        help="check-dispatch: green-path hop flag, accepted "
                             "and ignored so the check skill can pass its "
                             "arguments through to audit")
    parser.add_argument("--full", action="store_true",
                        help="restore per-row history listing "
                             "(skip body-row aggregation)")
    parser.add_argument("--dirty", default="",
                        help="emit-v-slices: comma-list of V<n> to restrict to "
                             "(default is all rows)")
    parser.add_argument("--from-audit", action="store_true",
                        help="write-memo: re-run the mechanical audit internally "
                             "and merge it with the behavioral verdicts on stdin "
                             "(stdin = behavioral rows only; hand-merge banned). "
                             "emit-row-ids: pre-fill HOLD-SINCE-CLEAN / MATCH / "
                             "blank from the same memo + scope-feed sources")
    parser.add_argument("--files", default="",
                        help="fix-sembr: comma-list of files to rewrite "
                             "(default: the discovered sembr file set)")
    parser.add_argument("--write", action="store_true",
                        help="fix-sembr: apply rewrites in place "
                             "(default is dry-run)")
    args = parser.parse_args(argv)
    args.repo_root = os.path.abspath(args.repo_root)
    if args.mode == "audit":
        return cmd_audit(args)
    if args.mode == "fix-sembr":
        return cmd_fix_sembr(args)
    if args.mode == "emit-v-slices":
        return cmd_emit_v_slices(args)
    if args.mode == "emit-superseded":
        return cmd_emit_superseded(args)
    if args.mode == "emit-fold-seeds":
        return cmd_emit_fold_seeds(args)
    if args.mode == "emit-v-weights":
        return cmd_emit_v_weights(args)
    if args.mode == "emit-row-ids":
        return cmd_emit_row_ids(args)
    if args.mode == "emit-overview":
        return cmd_emit_overview(args)
    if args.mode == "emit-token-estimate":
        return cmd_emit_token_estimate(args)
    if args.mode == "emit-prune-patterns":
        return cmd_emit_prune_patterns(args)
    if args.mode == "emit-residue":
        return cmd_emit_residue(args)
    if args.mode == "emit-archive-window":
        return cmd_emit_archive_window(args)
    if args.mode == "emit-condense-propose":
        return cmd_emit_condense_propose(args)
    if args.mode == "emit-check-agent-prompt":
        return cmd_emit_check_agent_prompt(args)
    return cmd_write_memo(args)


if __name__ == "__main__":
    sys.exit(main())
