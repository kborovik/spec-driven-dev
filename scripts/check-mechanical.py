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
                Emits `mechanize|DRIFT|…` / `mechanize|MISSING|…` — the
                mechanize-scan invariant's verbatim-block check: every
                user-invocable `skills/*/SKILL.md` (minus frontmatter
                `user-invocable: false`) carries the byte-identical canonical
                MECHANIZE block (DRIFT divergent, MISSING absent), realized once
                here so the drift-detector retires its hand-run `awk|md5|uniq`.
                Emits `dispatch|VIOLATE|…` — the response-shape invariant's
                dispatch-target rule: no skill body slash-dispatches an auto-fire
                sub-skill (`/<plugin>:<sub-skill>` for a `user-invocable: false`
                sub-skill is never a valid dispatch target). Sub-skill set is
                derived frontmatter-only, plugin name from the manifest,
                backtick-wrapped forms exempt — realized once here so the
                drift-detector retires its hand-run skill-body slash grep.
                Emits `grant|VIOLATE|…` — the tooling-preference invariant's
                grant-use rule: no frontmatter `allowed-tools` grant is
                zero-body-use (a granted tool the skill body never invokes).
                Sound by construction — flagged only on total body-absence
                (token, alias, operation verb, or Bash command anchor), spanning
                the PUBLISHED + REPO-LOCAL skill set — realized once here so the
                drift-detector retires its hand-run allowed-tools grant sweep
                (a manual sweep misses rows).
                Emits `symbols|VIOLATE|…` — the symbol-set + human-clarity
                invariants' spell-out rule: no human-facing surface (README,
                CLAUDE.md, the plugin manifest) carries a naked `→ ≥ ≤ & ~`
                symbol outside a backtick span or fenced block. SPEC-adjacent
                telegraph keeps the set, so it is never scanned. Sound (fenced
                prose treated exempt too) — realized once here so the
                drift-detector retires its hand-run symbol grep.
                Emits `idiom|VIOLATE|…` — the human-clarity invariant's
                idiom-ban rule: no human-facing surface (README, CLAUDE.md, the
                plugin manifest) carries a banned idiom / jargon-idiom phrase from
                a curated low-false-positive subset of the steno BOUNDARIES ban
                list (multi-word idiom + hyphenated jargon-idiom only; ambiguous
                single words excluded). Backtick-span + fenced-block exempt —
                realized once here so the drift-detector retires its hand-run
                idiom grep, a fixed-pattern sweep a manual pass forgets to re-run.
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
                hashes, oversized-cell ack) plus the `.gitignore` guard — only
                when the run is clean. The model never decides "clean". Exit
                0 = clean, 1 = dirty (memo untouched, CI-gateable), 2 = invalid
                vocab.
  emit-v-slices — read SPEC.md, print every §V row body with its source line
                range (`## V<n> SPEC.md:<start>-<end>` header + verbatim row
                text). Optional `--dirty V<n>,...` restricts to named rows
                (default is all). Sources the §V-classification slice for the
                drift-detector's single-agent and sub-agent batch paths without a
                whole-file Read (large SPEC exceeds the Read token cap).
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
                byte/token weight ranking plus the heavy-row set (top rows whose
                cumulative weight first reaches ≥ 50% of the §V section; stable
                tie-break descending weight then ascending id so run-stable).
                Prints a `v_row|bytes|tokens|cum_pct|heavy` table sorted heaviest
                first — the condenser extracts the heavy rows' audit recipes
                without a by-inspection guess.
  emit-row-ids — read SPEC.md, print the canonical live id-set skeleton: every
                live §V + §I + §T id as a verdict-table row with blank verdict
                and evidence cells (`id||`). The drift-detector fills verdicts
                against this skeleton instead of hand-enumerating the live row
                set, so a live row can't be silently dropped from the verdict
                table (omitted-row undercoverage class). §I ids derive from
                kind-prefixed interface rows (`- api: POST /x → …` → `I.api`).
  emit-overview — read SPEC.md, print the LOAD-step spec overview: §G/§C/§I/§T/§B
                headers + bodies verbatim plus the §V id list only (no §V row
                bodies). The drift-detector loads this in place of a whole-file
                Read per the single-load invariant; §V bodies arrive via
                emit-v-slices, so loading them here too would double-load SPEC.md
                and re-hit the Read token cap on a large spec. The id list lets
                the consumer size the classification batch from the row count.
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

# history-residue (freshness-contract invariant)
HR_AMEND = re.compile(r'\(∆+\)')
HR_DATED = re.compile(r'\bretired \d{4}-\d{2}-\d{2}\b')
HR_SUPERSEDE = re.compile(r'\bpre-amend\b|prior .{0,40}\b(?:retired|dropped|superseded)\b')
# pre-filters
PF_BACKTICK = re.compile(r'`[^`]*`')
PF_CITE_MOD = re.compile(r'§V\.\d+\(∆+\)')
PF_RETIRED_INPLACE = re.compile(r'^V\d+: retired \d{4}-\d{2}-\d{2}')

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
    blank-verdict verdict-table row per id (`id||`). The drift-detector fills
    verdicts against this script-emitted skeleton instead of hand-enumerating
    the live row set, closing the omitted-row silent-undercoverage class — the
    skeleton enumerates exactly the set the script already parses/hashes."""
    return ([r["id"] for r in v_rows]
            + [r["id"] for r in i_ids]
            + [r["id"] for r in t_rows])


def collect_v_slices(sections):
    """Return [{id, line_start, line_end, text}] every §V row — each row body with
    its source line span. Rows are normally single-line; the span captures any
    continuation lines up to the next row opener (trailing blanks trimmed) so a
    wrapped body stays faithful. Feeds the §V-classification slice per the batch
    invariant (script slice not whole-file Read)."""
    v_lines = sections.get("V", [])
    openers = [idx for idx, (_, line) in enumerate(v_lines) if V_ROW.match(line)]
    slices = []
    for k, idx in enumerate(openers):
        nxt = openers[k + 1] if k + 1 < len(openers) else len(v_lines)
        block = v_lines[idx:nxt]
        while block and block[-1][1].strip() == "":
            block = block[:-1]
        m = V_ROW.match(block[0][1])
        slices.append({"id": m.group(1),
                       "line_start": block[0][0],
                       "line_end": block[-1][0],
                       "text": "\n".join(b[1] for b in block)})
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
    ascending id so run-stable; the heavy set is the prefix whose cumulative weight
    first reaches ≥ 50% of the §V-section total. Returns (ranked, total_bytes)
    where each ranked entry is {id, bytes, tokens, cum_pct, heavy}. The condenser
    extracts heavy rows' audit recipes without a by-inspection guess."""
    weights = []
    for r in v_rows:
        b = len(r["full"].encode("utf-8"))
        weights.append({"id": r["id"], "bytes": b, "tokens": int(b / TOKEN_RATIO)})
    total = sum(w["bytes"] for w in weights)
    ranked = sorted(weights, key=lambda w: (-w["bytes"], int(w["id"][1:])))
    half = total / 2
    cum = 0
    heavy_done = False
    for w in ranked:
        cum += w["bytes"]
        w["cum_pct"] = round(100 * cum / total, 1) if total else 0.0
        if heavy_done:
            w["heavy"] = False
        else:
            w["heavy"] = True
            if cum >= half:
                heavy_done = True
    return ranked, total


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


def audit_archive_markers(sections, archive_present, archive_has_vretired):
    """Archive marker shape under §T/§B (and §V when a retired block exists)."""
    out = []
    found = {"T": False, "B": False, "V": False}
    for letter in ("T", "B", "V"):
        for lineno, line in sections.get(letter, []):
            if ARCHIVE_MARK_ANY.match(line):
                found[letter] = True
                if letter in ("T", "B"):
                    if not ARCHIVE_MARK_TB.match(line):
                        out.append(("format", "VIOLATE",
                                    f"format: §{letter} archive marker malformed "
                                    f"@ SPEC.md:{lineno}"))
                else:
                    if not ARCHIVE_MARK_V.match(line):
                        out.append(("format", "VIOLATE",
                                    f"format: §V archive marker malformed "
                                    f"@ SPEC.md:{lineno}"))
    if archive_present:
        for letter in ("T", "B"):
            if not found[letter]:
                out.append(("format", "VIOLATE",
                            f"format: §{letter} missing archive marker "
                            f"(SPEC.archive.md exists)"))
        if archive_has_vretired and not found["V"]:
            out.append(("format", "VIOLATE",
                        "format: §V missing §V.retired archive marker "
                        "(archive contains §V.retired)"))
    return out


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


def audit_history_residue(v_rows, t_rows, b_rows, full=False, oversized_ack=None):
    by_section = {"V": [], "T": [], "B": []}

    def scan(rid, body, line, kind):
        # retired-in-place §V row exempt (pending reorganize archival)
        if kind == "V" and PF_RETIRED_INPLACE.match(f"{rid}: {body}"):
            return
        residue = PF_CITE_MOD.sub('', strip_backticks(body))
        if HR_AMEND.search(residue):
            by_section[kind].append(("amendment-counter", rid, line))
        if HR_DATED.search(residue):
            by_section[kind].append(("dated-retirement", rid, line))
        if HR_SUPERSEDE.search(residue):
            by_section[kind].append(("supersession-narration", rid, line))

    for r in v_rows:
        scan(r["id"], r["body"], r["line"], "V")
    for r in t_rows:
        scan(r["id"], r["body"] or "", r["line"], "T")
    for r in b_rows:
        scan(r["id"], r["body"] or "", r["line"], "B")

    out = []
    pattern_order = ("amendment-counter", "dated-retirement", "supersession-narration")
    for kind in ("V", "T", "B"):
        items = by_section[kind]
        if not items:
            continue
        if not full and len(items) > HISTORY_AGGREGATE_THRESHOLD:
            counts = {}
            for pattern, _, _ in items:
                counts[pattern] = counts.get(pattern, 0) + 1
            breakdown = ", ".join(f"{counts[p]} {p}"
                                  for p in pattern_order if p in counts)
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


# --- mechanize-block identity ------------------------------------------------

MECHANIZE_HDR = re.compile(r'^## MECHANIZE\b')
H2_HDR = re.compile(r'^## ')
UI_FALSE = re.compile(r'^user-invocable:\s*false\s*$', re.MULTILINE)


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
    """Canonical MECHANIZE block: the `## MECHANIZE` header line through the line
    before the next H2 (or EOF), trailing blank lines trimmed. Returns None when
    the sentinel is absent. Trailing-blank trim canonicalizes the inter-section
    gap so byte-identity reflects block content, not the blank-line count before
    the following section."""
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
    """Mechanize-block audit core over {path: text} — pure, unit-testable without
    the filesystem (mechanize-scan + mechanical-realization invariants). The
    user-invocable set is the input minus frontmatter `user-invocable: false`
    (auto-fire sub-skills). Emits MISSING for a user-invocable skill lacking the
    MECHANIZE sentinel, DRIFT for a block diverging from the set's canonical
    (majority) md5. Uniform set → no rows (clean, silent). < 2 blocks → no
    comparison possible, no rows."""
    out = []
    blocks = {}
    for path in sorted(skill_texts):
        txt = skill_texts[path]
        if not is_user_invocable(txt):
            continue
        block = extract_mechanize_block(txt)
        if block is None:
            out.append(("mechanize", "MISSING",
                        f"mechanize MISSING: {path} user-invocable, "
                        f"no MECHANIZE block"))
            continue
        blocks[path] = block
    if len(blocks) < 2:
        return out
    by_hash = {}
    for path in sorted(blocks):
        h = hashlib.md5(blocks[path].encode("utf-8")).hexdigest()
        by_hash.setdefault(h, []).append(path)
    if len(by_hash) == 1:
        return out
    # canonical = most-populated md5; ties → lexicographically smallest hash
    # (sorted iteration + max-by-count is deterministic, run-stable).
    canonical = max(sorted(by_hash), key=lambda h: len(by_hash[h]))
    for h in sorted(by_hash):
        if h == canonical:
            continue
        for path in by_hash[h]:
            out.append(("mechanize", "DRIFT",
                        f"mechanize DRIFT: {path} MECHANIZE block diverges from "
                        f"canonical (md5 {h[:8]} != {canonical[:8]})"))
    return out


def audit_mechanize_block(skill_md):
    """File-reading wrapper around classify_mechanize_blocks (mechanize-scan +
    mechanical-realization invariants). Asserts every user-invocable
    `skills/*/SKILL.md` carries the byte-identical canonical MECHANIZE block —
    realized once here, retiring the hand-run `awk|md5|uniq` verbatim check."""
    texts = {}
    for path in skill_md:
        try:
            texts[path] = read_text(path)
        except OSError:
            continue
    return classify_mechanize_blocks(texts)


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
    "Read":  [(r'\bread', re.I)],
    "Edit":  [(r'\bedit|\brewrite|\bpatch\b|\bprune|\btrim|\brenumber|\boverwrite',
               re.I)],
    "Write": [(r'\bwrite', re.I)],
    "Grep":  [(r'\bgrep', re.I)],
    "Glob":  [(r'\bGlob\b', 0)],                         # case-sensitive: prose-safe
    "Agent": [(r'\bagent|\bExplore\b', re.I)],
    "Skill": [(r'\bskill', re.I)],                       # generous (accepted limit)
    "TaskCreate": [(r'TaskCreate', 0)],
    "TaskUpdate": [(r'TaskUpdate', 0)],
    "AskUserQuestion": [(r'AskUserQuestion|\bask\b|\bquestion', re.I)],
}
# bare `Bash` grant (no arg pattern) pre-approves any command — used when the body
# prescribes a command (fenced block or a known command token).
BARE_BASH_CMD = re.compile(r'```|\b(?:git|python3|gh|jq|grep|rg|npm|make|cargo'
                           r'|sed|awk|cat|test)\b')
ALLOWED_TOOLS_LINE = re.compile(r'^allowed-tools:\s*(.*)$')


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
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            break
        m = ALLOWED_TOOLS_LINE.match(lines[i])
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


def classify_grants(skill_texts):
    """Grant-use audit core over {path: text} — pure, unit-testable without the
    filesystem (tooling-preference invariant). For each skill's frontmatter
    `allowed-tools` grant, emit `grant|VIOLATE|…` when the body prescribes no
    invocation of that tool (zero-body-use grant banned). Skills without an
    `allowed-tools` line carry no grants → no rows. Realized once here so the
    drift-detector retires its hand-run grant sweep — a manual sweep misses rows,
    the recurrence class this closes."""
    out = []
    for path in sorted(skill_texts):
        text = skill_texts[path]
        tokens, lineno = find_allowed_tools(text)
        if not tokens:
            continue
        body = body_after_frontmatter(text)
        for tok in tokens:
            if not grant_used(tok, body):
                out.append(("grant", "VIOLATE",
                            f"grant VIOLATE: {path}:{lineno} grants {tok} "
                            f"zero body use (drop per tooling-preference invariant)"))
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


def plugin_dirs(repo_root):
    """PUBLISHED plugin source dirs — from the marketplace manifest
    (`plugins[].source`, root `./` → repo root), else a single plugin.json repo
    root, else empty. Repo-agnostic; shared by the published-md + skill-md
    discovery so the PUBLISHED-scope root is resolved once."""
    mp = os.path.join(repo_root, ".claude-plugin", "marketplace.json")
    pj = os.path.join(repo_root, ".claude-plugin", "plugin.json")
    if os.path.exists(mp):
        try:
            data = json.loads(read_text(mp))
            return plugin_source_dirs(repo_root, data.get("plugins", []))
        except (OSError, ValueError):
            return []
    if os.path.exists(pj):
        return [repo_root]
    return []


def plugin_names(repo_root):
    """PUBLISHED plugin names — from the marketplace manifest
    (`plugins[].name`), else the single `plugin.json` `name`, else empty
    (plugin-shape invariant — name from the manifest, never assumed equal to a
    dir name). The dispatch-target audit builds the `/<plugin>:<sub-skill>`
    slash form from these."""
    mp = os.path.join(repo_root, ".claude-plugin", "marketplace.json")
    pj = os.path.join(repo_root, ".claude-plugin", "plugin.json")
    if os.path.exists(mp):
        try:
            data = json.loads(read_text(mp))
            return [p["name"] for p in data.get("plugins", []) if p.get("name")]
        except (OSError, ValueError):
            return []
    if os.path.exists(pj):
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
    plugin source dir. The plugin skills dir is conventionally `skills/` (Claude
    Code plugin layout), so REPO-LOCAL `.claude/skills/**` is excluded by
    construction — it is not a plugin source skills dir. Repo-agnostic; feeds the
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
    """SKILL.md set the grant-use audit spans: PUBLISHED `<src>/skills/*/SKILL.md`
    (discover_skill_md) plus REPO-LOCAL `.claude/skills/*/SKILL.md` — a REPO-LOCAL
    skill (e.g. release) carries `allowed-tools` grants too, so the grant-use
    audit covers it. Repo-agnostic."""
    paths = list(discover_skill_md(repo_root))
    local = os.path.join(repo_root, ".claude", "skills")
    if os.path.isdir(local):
        for name in sorted(os.listdir(local)):
            p = os.path.join(local, name, "SKILL.md")
            if os.path.isfile(p):
                paths.append(p)
    return sorted(set(paths))


def discover_repo_local(repo_root):
    """REPO-LOCAL files holding pinned cites — conventional default set."""
    files = []
    cl = os.path.join(repo_root, ".claude")
    if os.path.isdir(cl):
        for root, _, fns in os.walk(cl):
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
    repo-root README.md + CLAUDE.md (GITHUB-FACING + REPO-LOCAL human surfaces)
    plus the plugin manifest(s) (description shown in the marketplace). Excludes
    SPEC-adjacent telegraph (SPEC.md, skill bodies, `.spec/**` overflow), which
    KEEPS the symbol set, so those are never scanned. Repo-agnostic."""
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


def discover_sembr_files(repo_root):
    """Sembr-invariant prose file set: repo-root README.md + CLAUDE.md,
    `designs/*.md` drafts, and the PUBLISHED skill bodies (discover_skill_md).
    Pipe-row files (SPEC.md, the archive sibling, the extras overflow) are
    exempt by construction — never in the set. Repo-agnostic."""
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
    findings += audit_archive_markers(sections, arch_present, arch_vret)
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
    findings += audit_dispatch_targets(skill_md, plugin_names(repo_root))
    findings += audit_grants(discover_grant_skills(repo_root))
    findings += audit_human_symbols(discover_human_facing(repo_root))
    findings += audit_human_idiom(discover_human_facing(repo_root))
    findings += audit_claude_md(repo_root)
    findings += audit_sembr(discover_sembr_files(repo_root))
    findings += audit_batch_advisory(v_rows, published_md)
    findings += audit_token_estimate(spec_bytes)
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
    slices = collect_v_slices(sections)
    if args.dirty:
        wanted = {t.strip() for t in args.dirty.split(',') if t.strip()}
        slices = [s for s in slices if s["id"] in wanted]
    for s in slices:
        print(f"## {s['id']} SPEC.md:{s['line_start']}-{s['line_end']}")
        print(s["text"])
        print()
    return 0


def cmd_emit_superseded(args):
    text, _, _ = load_spec(args.repo_root, args.spec)
    sections, _ = parse_sections(text)
    v_rows = parse_v_rows(sections)
    t_rows = parse_pipe_rows(sections, "T", T_ROW)
    candidates = emit_superseded_candidates(v_rows, t_rows)
    print("tid|superseded_v|original_cites")
    for c in candidates:
        print(f"{c['id']}|{','.join(c['unresolved'])}|{c['cites']}")
    return 0


def cmd_emit_fold_seeds(args):
    text, _, _ = load_spec(args.repo_root, args.spec)
    sections, _ = parse_sections(text)
    v_rows = parse_v_rows(sections)
    t_rows = parse_pipe_rows(sections, "T", T_ROW)
    b_rows = parse_pipe_rows(sections, "B", B_ROW)
    seeds = emit_fold_seeds(v_rows, t_rows, b_rows)
    print("cluster_members|co_citers")
    for s in seeds:
        print(f"{','.join(s['members'])}|{','.join(s['citers'])}")
    return 0


def cmd_emit_v_weights(args):
    text, _, _ = load_spec(args.repo_root, args.spec)
    sections, _ = parse_sections(text)
    v_rows = parse_v_rows(sections)
    ranked, _ = emit_v_weights(v_rows)
    print("v_row|bytes|tokens|cum_pct|heavy")
    for w in ranked:
        print(f"{w['id']}|{w['bytes']}|{w['tokens']}|{w['cum_pct']}|"
              f"{'yes' if w['heavy'] else 'no'}")
    return 0


def cmd_emit_row_ids(args):
    text, _, _ = load_spec(args.repo_root, args.spec)
    sections, _ = parse_sections(text)
    v_rows = parse_v_rows(sections)
    i_ids = parse_i_ids(sections)
    t_rows = parse_pipe_rows(sections, "T", T_ROW)
    print("id|verdict|evidence")
    for rid in emit_row_ids(v_rows, i_ids, t_rows):
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
    verdict (unfilled skeleton row) is skipped. Returns list of complaints."""
    bad = []
    for rid, v, _ in rows:
        if not v:
            continue
        vocab = row_type_vocab(rid)
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


def ensure_gitignore_guard(repo_root):
    path = os.path.join(repo_root, ".spec", ".gitignore")
    line = "check-state.json"
    existing = ""
    if os.path.exists(path):
        existing = read_text(path)
        if any(l.strip() == line for l in existing.splitlines()):
            return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        if existing and not existing.endswith("\n"):
            f.write("\n")
        f.write(line + "\n")


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

    # mechanize-block audit (mechanize-scan + mechanical-realization invariants):
    # every user-invocable SKILL.md carries the byte-identical canonical block;
    # sub-skills (user-invocable: false) excluded. Replaces hand-run awk|md5|uniq.
    mblock = "## MECHANIZE — scan\n\nscan body\n\n- rule a\n- rule b\n"
    mblock2 = "## MECHANIZE — scan\n\nscan body\n\n- rule a\n- rule DIFFERENT\n"

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
    body_mention = _mk(block="## MECHANIZE — scan\n\nsets `user-invocable: "
                             "false` in prose\n\n- rule a\n- rule b\n")
    check(is_user_invocable(body_mention) is True,
          "is_user_invocable: body mention of flag ignored (frontmatter-only)")
    # block extraction: header → next H2, trailing blank trimmed; absent → None
    check(extract_mechanize_block(_mk()) == mblock.rstrip("\n"),
          "extract_mechanize_block: header to next H2, trailing blank trimmed")
    check(extract_mechanize_block(_mk(block="## NOPE\n\nx\n")) is None,
          "extract_mechanize_block: sentinel absent → None")
    check(extract_mechanize_block(_mk(tail="")) == mblock.rstrip("\n"),
          "extract_mechanize_block: block at EOF extracts")
    # uniform set → clean (silent)
    check(classify_mechanize_blocks({"a/SKILL.md": _mk(), "b/SKILL.md": _mk()})
          == [], "mechanize: uniform blocks → clean")
    # divergent block → DRIFT on the minority only
    dr = classify_mechanize_blocks({"a/SKILL.md": _mk(), "b/SKILL.md": _mk(),
                                    "c/SKILL.md": _mk(block=mblock2)})
    check(len(dr) == 1 and dr[0][1] == "DRIFT" and "c/SKILL.md" in dr[0][2],
          "mechanize: divergent block flagged DRIFT on minority")
    # user-invocable skill missing the block → MISSING
    mr = classify_mechanize_blocks({"a/SKILL.md": _mk(),
                                    "b/SKILL.md": _mk(block="## OTHER\n\nx\n")})
    check(any(v == "MISSING" and "b/SKILL.md" in e for _, v, e in mr),
          "mechanize: user-invocable skill missing block → MISSING")
    # sub-skill (user-invocable: false) without block excluded — no MISSING
    check(classify_mechanize_blocks(
        {"a/SKILL.md": _mk(), "b/SKILL.md": _mk(),
         "sub/SKILL.md": _mk("user-invocable: false\n",
                             block="## OTHER\n\nx\n")}) == [],
          "mechanize: sub-skill without block excluded")
    # single user-invocable block → no comparison possible, clean
    check(classify_mechanize_blocks({"a/SKILL.md": _mk()}) == [],
          "mechanize: single block → no divergence possible")
    # DRIFT + MISSING make the run dirty; pseudo-id row unrestricted vocab
    check(compute_clean([("mechanize", "DRIFT", "")])[0] is False,
          "mechanize: DRIFT is dirty")
    check(compute_clean([("mechanize", "MISSING", "")])[0] is False,
          "mechanize: MISSING is dirty")
    check(validate_vocab([("mechanize", "DRIFT", "")]) == [],
          "mechanize: pseudo-id unrestricted vocab")

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

    # token split keeps a Bash arg pattern (commas inside parens) as one token
    check(split_grant_tokens("Read, Bash(python3 */check-mechanical.py *), Grep")
          == ["Read", "Bash(python3 */check-mechanical.py *)", "Grep"],
          "grant: paren-aware token split")
    # find_allowed_tools: frontmatter-only, with line number; body line ignored
    toks_g, ln_g = find_allowed_tools(_gk("Read, Grep", "allowed-tools: Edit here"))
    check(toks_g == ["Read", "Grep"] and ln_g == 3,
          "grant: allowed-tools parsed w/ lineno, body line ignored")
    check(find_allowed_tools("no fence\nallowed-tools: Read\n") == (None, None),
          "grant: no frontmatter → no grants")
    # grant_used: token / lowercase token / alias / operation verb / absence
    check(grant_used("Read", "first Read `SPEC.md`"), "grant_used: token present")
    check(grant_used("Grep", "we grep the files"), "grant_used: lowercase token")
    check(grant_used("Agent", "spawn Explore sub-agents"),
          "grant_used: alias Explore → agent-spawner")
    check(grant_used("Edit", "rewrite the rows in place"),
          "grant_used: operation verb rewrite → editor")
    check(not grant_used("Grep", "this body never searches"),
          "grant_used: absent tool → unused")
    # wildcard-pattern tool matches case-sensitively: 'mid-glob' prose never masks
    check(not grant_used("Glob", "the mid-glob `Bash(python3 *)` form"),
          "grant_used: wildcard prose does not mask a missing pattern-lister grant")
    check(grant_used("Glob", "the Glob tool lists files"),
          "grant_used: PascalCase pattern-lister counts")
    # Bash: arg-pattern anchor vs bare-Bash command presence
    check(grant_used("Bash(git *)", "run `git commit -- paths`"),
          "grant_used: Bash arg anchor present")
    check(not grant_used("Bash(jq *)", "no json tooling here"),
          "grant_used: Bash arg anchor absent → unused")
    check(grant_used("Bash", "the recipe runs `python3 scripts/x.py`"),
          "grant_used: bare Bash + command token")
    check(not grant_used("Bash", "pure prose, no commands"),
          "grant_used: bare Bash, no command → unused")
    # dispatcher reference word is ubiquitous → generous (accepted false-negative)
    check(grant_used("Skill", "follows the telegraph skill rules"),
          "grant_used: dispatcher generous (any mention)")
    # classify_grants: VIOLATE on the unused grant only, line-numbered
    rows_g = classify_grants({"skills/x/SKILL.md": _gk("Read, Glob",
                                                       "Read `SPEC.md` then bail")})
    check(len(rows_g) == 1 and rows_g[0][0] == "grant" and rows_g[0][1] == "VIOLATE"
          and "Glob" in rows_g[0][2] and "skills/x/SKILL.md:3" in rows_g[0][2],
          "classify_grants: unused grant flagged, used grant silent, line-numbered")
    check(classify_grants({"skills/y/SKILL.md": _gk("Read", "Read the file")}) == [],
          "classify_grants: all-used → clean")
    check(classify_grants({"skills/z/SKILL.md": "# no frontmatter\nbody\n"}) == [],
          "classify_grants: no allowed-tools → no rows")
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
    check(validate_vocab([("I.api", "", "")]) == [], "vocab skips blank skeleton verdict")
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
    naked = "the loop is human → claude and a & b"
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

    if fails:
        sys.stderr.write("SELF-TEST FAIL:\n  " + "\n  ".join(fails) + "\n")
        return 1
    print(f"self-test OK ({_selftest_count()} assertions)")
    return 0


def _selftest_count():
    # informational; kept in sync loosely with the check() calls above
    return 203


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
                                         "emit-token-estimate"])
    parser.add_argument("--repo-root", default=os.environ.get("CHECK_REPO_ROOT", "."))
    parser.add_argument("--spec", default="SPEC.md")
    parser.add_argument("--no-hook", action="store_true",
                        help="skip the REPO-LOCAL check-extras.sh probe")
    parser.add_argument("--full", action="store_true",
                        help="restore per-row history listing "
                             "(skip body-row aggregation)")
    parser.add_argument("--dirty", default="",
                        help="emit-v-slices: comma-list of V<n> to restrict to "
                             "(default is all rows)")
    parser.add_argument("--from-audit", action="store_true",
                        help="write-memo: re-run the mechanical audit internally "
                             "and merge it with the behavioral verdicts on stdin "
                             "(stdin = behavioral rows only; hand-merge banned)")
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
    return cmd_write_memo(args)


if __name__ == "__main__":
    sys.exit(main())
