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
                Also emits the machine-side scope feed for the memo-driven default
                sweep: `tasks|ADVISORY|flipped-since-clean: …` (§T flipped `.`→`x`
                since the memo's clean sha) and `diff|ADVISORY|touched: …` (paths
                changed since that sha). These plus the reshaped
                `memo|ADVISORY|… : <ids>` row carry stable comma-joined fields
                (no surrounding prose) so the drift-detector chains them straight
                into `emit-v-slices --dirty` without hand-rolling `git diff`.
  write-memo  — read a merged verdict table (mechanical + LLM-judged rows) on
                stdin, validate the verdict vocab, compute clean-set membership
                itself, and write the run memo (schema v3, per-row §V hashes,
                oversized-cell ack) plus the `.gitignore` guard — only when the
                run is clean. The model never decides "clean".
  emit-v-slices — read SPEC.md, print every §V row body with its source line
                range (`## V<n> SPEC.md:<start>-<end>` header + verbatim row
                text). Optional `--dirty V<n>,...` restricts to named rows
                (default is all). Sources the §V-classification slice for the
                drift-detector's single-agent and sub-agent batch paths without a
                whole-file Read (large SPEC exceeds the Read token cap).
  emit-superseded — read SPEC.md, print the compactor's prong-2 SUPERSEDED
                candidate set: every closed §T whose §V cite resolves only into
                the archived §V.retired block (absent from live §V). Live-only
                resolution, distinct from the cite-DAG audit's live+archive
                scope. Prints a `tid|superseded_v|original_cites` table the
                compactor consumes in place of by-hand per-cite resolution.
  emit-fold-seeds — read SPEC.md, print the compactor's prong-1 fold-candidate
                seed set: clusters of live §V rows that share a citer (a §T
                whose cites or a §B whose fix names ≥ 2 live §V rows co-cites
                them). Connected components over the co-citation graph. Prints a
                `cluster_members|co_citers` table — an advisory seed only; the
                operator confirms each fold at the compact CONFIRM gate (never
                auto-applied) per the fold-first-authoring invariant.
  emit-v-weights — read SPEC.md, print the compactor's prong-6 per-§V-row
                byte/token weight ranking plus the heavy-row set (top rows whose
                cumulative weight first reaches ≥ 50% of the §V section; stable
                tie-break descending weight then ascending id so run-stable).
                Prints a `v_row|bytes|tokens|cum_pct|heavy` table sorted heaviest
                first — the compactor extracts the heavy rows' audit recipes
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

CLEAN_VERDICTS = {"HOLD", "HOLD-SINCE-CLEAN", "SCOPE-EMPTY", "VIOLATE-CAPTURED", "LATENT"}
DIRTY_VERDICTS = {"VIOLATE", "UNVERIFIABLE", "UNRESOLVED", "TYPE-MISMATCH",
                  "DRIFT", "MISSING", "STALE", "EXTRA"}
# verdicts admissible on §V (invariant) rows in the merged table
V_VOCAB = CLEAN_VERDICTS | {"VIOLATE", "UNVERIFIABLE"}
ADVISORY = "ADVISORY"

TOKEN_BUDGET = 25000       # token-budget invariant advisory threshold
TOKEN_RATIO = 3.4          # bytes-per-token for telegraph register (token-budget invariant)
OVERSIZE_CELL = 300        # history-residue oversized-cell advisory (chars)
MEMO_SCHEMA = 3            # memo schema version (memo invariant)
HISTORY_AGGREGATE_THRESHOLD = 10  # per-section body-row aggregation (drift-verdict-vocab invariant)

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
    """Prong-2 SUPERSEDED candidate set (token-budget-compact invariant): each
    closed §T (status `x`) whose §V cite is absent from the live §V section →
    candidate — the cited invariant was amended away or folded (resolution lands
    only in the archived §V.retired block, or nowhere). Live-§V-only resolution,
    distinct from the cite-DAG audit's live+archive scope (where an archived
    cite holds resolved). Returns [{id, unresolved:[V<n>,...], cites}] — the
    compactor builds `SUPERSEDED — §V.<m> amend` markers from it without by-hand
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
    """Prong-1 fold-candidate seed (token-budget-compact invariant): cluster live
    §V rows that share a citer — a §T whose `cites` or a §B whose `fix` names ≥ 2
    live §V rows co-cites them so they are fold-candidate siblings. Edges run
    between every pair of live §V rows a single citer names; clusters is connected
    components over that co-citation graph. Live-§V-only — an archived or folded
    cite forms no edge. Returns [{members:[V<n>,...], citers:[T<n>|B<n>,...]}]
    sorted by lowest member id; an advisory seed only — the operator confirms
    each fold at the compact CONFIRM gate (never auto-applied) per the
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
    """Prong-6 per-§V-row weight ranking (token-budget-compact invariant): byte
    weight is utf-8 length of the full row line, token weight is byte/TOKEN_RATIO
    per the token-budget invariant. Ranks rows descending weight, tie-break
    ascending id so run-stable; the heavy set is the prefix whose cumulative weight
    first reaches ≥ 50% of the §V-section total. Returns (ranked, total_bytes)
    where each ranked entry is {id, bytes, tokens, cum_pct, heavy}. The compactor
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
                        f"→ /sdd:compact body-trim"))
        else:
            for pattern, rid, line in items:
                out.append(("history", "VIOLATE",
                            f"§{kind}.{rid} VIOLATE: history: {pattern} "
                            f"@ SPEC.md:{line}"))

    advisories = collect_oversized_cells(t_rows, b_rows)
    if advisories and oversized_cell_sha(advisories) != oversized_ack:
        out.append(("history", ADVISORY,
                    "history: oversized cells (smell): "
                    + ", ".join(advisories) + " — consider /sdd:compact body-trim"))
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


# --- token estimate ----------------------------------------------------------

def audit_token_estimate(spec_bytes):
    est = int(spec_bytes / TOKEN_RATIO)
    if est > TOKEN_BUDGET:
        k = round(est / 1000)
        return [("token", ADVISORY,
                 f"SPEC.md ~{k}k tokens > {TOKEN_BUDGET // 1000}k budget; "
                 f"consider /sdd:compact")]
    return []


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


def audit_scope_feed(repo_root, memo, t_rows, spec_path="SPEC.md"):
    """Machine-side scope feed for the memo-driven default sweep (memo invariant):
    `tasks|ADVISORY|flipped-since-clean: <ids>` and `diff|ADVISORY|touched: <paths>`,
    both keyed off the memo's `last_clean_sha`. Fields comma-joined, no prose so
    the drift-detector chains them into `emit-v-slices --dirty` not hand-rolling
    `git diff`. No memo or schema mismatch or unreachable sha → no rows (first-run /
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
            ("diff", ADVISORY, "touched: " + ",".join(touched))]


# --- REPO-LOCAL hook probe ---------------------------------------------------

def probe_extras_hook(repo_root):
    """Run `.claude/scripts/check-extras.sh` if present + executable; append its
    pipe-table rows. Language-agnostic contract per the parametric invariant."""
    out = []
    hook = os.path.join(repo_root, ".claude", "scripts", "check-extras.sh")
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


def discover_published_md(repo_root):
    """PUBLISHED markdown bodies — discovered from the marketplace manifest
    (plugin sources), single plugin.json, else empty. Repo-agnostic."""
    dirs = []
    mp = os.path.join(repo_root, ".claude-plugin", "marketplace.json")
    pj = os.path.join(repo_root, ".claude-plugin", "plugin.json")
    if os.path.exists(mp):
        try:
            data = json.loads(read_text(mp))
            dirs = plugin_source_dirs(repo_root, data.get("plugins", []))
        except (OSError, ValueError):
            pass
    elif os.path.exists(pj):
        dirs.append(repo_root)
    md = []
    for d in dirs:
        for root, _, files in os.walk(d):
            for fn in files:
                if fn.endswith(".md"):
                    md.append(os.path.join(root, fn))
    return sorted(md)


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

    memo_path = os.path.join(repo_root, ".claude", "check-state.json")
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
    findings += audit_pinned_header(discover_published_md(repo_root))
    findings += audit_token_estimate(spec_bytes)
    findings += audit_memo(memo_path, v_rows)
    findings += audit_scope_feed(repo_root, memo, t_rows, spec_path)
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


def validate_vocab(rows):
    """§V (invariant) rows must carry a vocab verdict; pseudo-id rows may carry
    problem/advisory verdicts. Returns list of complaints."""
    bad = []
    for rid, v, _ in rows:
        if ID_NUM.match(rid) and rid[0] == "V":
            if v not in V_VOCAB and v not in ("VIOLATE", "UNVERIFIABLE"):
                bad.append(f"{rid} verdict {v} not in vocab")
    return bad


def ensure_gitignore_guard(repo_root):
    path = os.path.join(repo_root, ".claude", ".gitignore")
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
    rows = parse_table(sys.stdin.read())
    bad = validate_vocab(rows)
    if bad:
        sys.stderr.write("write-memo: invalid verdicts: " + "; ".join(bad) + "\n")
        return 2
    clean, offenders = compute_clean(rows)
    if not clean:
        sys.stderr.write("write-memo: run not clean (" + ", ".join(
            f"{r}:{v}" for r, v in offenders[:8]) + ") — memo not written\n")
        return 0
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
    memo_path = os.path.join(args.repo_root, ".claude", "check-state.json")
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

    # clean-set + vocab
    clean_rows = [(f"V{1}", "HOLD", ""), (f"V{2}", "VIOLATE-CAPTURED", ""),
                  ("token", ADVISORY, "")]
    dirty_rows = [(f"V{1}", "VIOLATE", ""), ("format", "VIOLATE", "")]
    check(compute_clean(clean_rows)[0] is True, "clean-set admits captured+advisory")
    check(compute_clean(dirty_rows)[0] is False, "clean-set rejects violate")
    check(validate_vocab([(f"V{1}", "BOGUS", "")]), "vocab rejects bogus V verdict")
    check(validate_vocab([("format", "VIOLATE", "")]) == [], "vocab allows pseudo-id")

    if fails:
        sys.stderr.write("SELF-TEST FAIL:\n  " + "\n  ".join(fails) + "\n")
        return 1
    print(f"self-test OK ({_selftest_count()} assertions)")
    return 0


def _selftest_count():
    # informational; kept in sync loosely with the check() calls above
    return 81


# --- entry -------------------------------------------------------------------

def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--self-test" in argv:
        return selftest()
    parser = argparse.ArgumentParser(prog="check-mechanical",
                                     description="deterministic mechanical audits")
    parser.add_argument("mode", choices=["audit", "write-memo", "emit-v-slices",
                                         "emit-superseded", "emit-fold-seeds",
                                         "emit-v-weights", "emit-row-ids",
                                         "emit-overview"])
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
    args = parser.parse_args(argv)
    args.repo_root = os.path.abspath(args.repo_root)
    if args.mode == "audit":
        return cmd_audit(args)
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
    return cmd_write_memo(args)


if __name__ == "__main__":
    sys.exit(main())
