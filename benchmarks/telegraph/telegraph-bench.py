#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""telegraph-bench — measure telegraph compression of SPEC.md rows under two decoders.

Corpus: first 10 rows ∀ section {§V, §T, §B} in repo-root SPEC.md (30 rows total).

Per row, two decoders run:
  minimal   — naive expand-to-prose system msg (compression-vs-naive baseline)
  canonical — /sdd:explain invocation (production-decoder + legibility check)

Pipeline per row:
  n_glyph             = count_tokens(body)
  prose_minimal       = decode(body, MINIMAL_SYSTEM)
  prose_canonical     = decode(<SPEC.md attached> + §<S>.<n>, /sdd:explain SKILL.md)
  n_prose_{m,c}       = count_tokens(prose_{m,c})
  reduction_{m,c}     = 1 - n_glyph / n_prose_{m,c}

Per-sample record: {id, section, body, n_glyph,
                    prose_minimal, n_prose_minimal, reduction_minimal,
                    prose_canonical, n_prose_canonical, reduction_canonical}

Summary: per-section × per-decoder + grand-total {mean, median, p25, p75, n}.

Append record to benchmarks/telegraph/telegraph-bench-results.json (tracked in git).
Stats-over-time block schema-aware: incompatible prior record → skip w/ 1-line note.

Run:
  ./telegraph-bench.py
  uv run benchmarks/telegraph/telegraph-bench.py
  BENCH_MODEL=claude-opus-4-8 uv run benchmarks/telegraph/telegraph-bench.py

Model:
  Default claude-opus-4-7. Override w/ $BENCH_MODEL (recorded per result record →
  cross-model runs stay comparable; same JSON, one record per run).

Requires:
  uv (https://docs.astral.sh/uv/) — self-bootstraps python via the PEP 723 block above.
  Anthropic API key in $ANTHROPIC_API_KEY or ~/.anthropic-api-key.
"""

import datetime
import json
import os
import re
import statistics
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

MODEL = os.environ.get("BENCH_MODEL", "claude-opus-4-7")
MINIMAL_SYSTEM = (
    "Expand to plain English. Preserve every fact. Output prose only, no preamble."
)
SECTIONS = ("V", "T", "B")
SECTION_LIMIT = 10
TREND_WINDOW = 5
MAX_TOKENS = 8192
HTTP_TIMEOUT_S = 180

SECTION_BOUNDS = {
    "V": (r"## §V INVARIANTS\n", r"\n## §T TASKS"),
    "T": (r"## §T TASKS\n", r"\n## §B BUGS"),
    "B": (r"## §B BUGS\n", r"\Z"),
}

SECTION_ROW_RE = {
    "V": re.compile(r"(?m)^V(\d+):\s*(.*?)(?=\n(?:V\d+:|## )|\Z)", re.S),
    "T": re.compile(r"(?m)^T(\d+)\|(.*?)$"),
    "B": re.compile(r"(?m)^B(\d+)\|(.*?)$"),
}


def resolve_api_key() -> str:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key
    path = Path.home() / ".anthropic-api-key"
    if path.is_file():
        return path.read_text().strip()
    sys.exit("bail: ANTHROPIC_API_KEY unset and ~/.anthropic-api-key absent")


def extract_corpus(spec_md: Path) -> list[tuple[str, str, str]]:
    """Return (id, section, body) tuples; first SECTION_LIMIT rows per section."""
    txt = spec_md.read_text()
    rows: list[tuple[str, str, str]] = []
    for section in SECTIONS:
        start_pat, end_pat = SECTION_BOUNDS[section]
        m = re.search(start_pat + r"(.*?)" + end_pat, txt, re.S)
        if not m:
            sys.exit(f"bail: §{section} section not found in SPEC.md")
        body_region = m.group(1) + "\n## "
        section_rows = [
            (f"{section}{mm.group(1)}", section, mm.group(2).strip())
            for mm in SECTION_ROW_RE[section].finditer(body_region)
        ]
        if not section_rows:
            sys.exit(f"bail: no §{section} rows extracted")
        rows.extend(section_rows[:SECTION_LIMIT])
    return rows


def api_post(path: str, payload: dict, api_key: str) -> dict:
    req = urllib.request.Request(
        f"https://api.anthropic.com{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_S) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:500]
        sys.exit(f"bail: {path} -> HTTP {e.code}: {body}")
    except urllib.error.URLError as e:
        sys.exit(f"bail: {path} -> URLError: {e.reason}")


def count_tokens(text: str, api_key: str) -> int:
    out = api_post(
        "/v1/messages/count_tokens",
        {"model": MODEL, "messages": [{"role": "user", "content": text}]},
        api_key,
    )
    return out["input_tokens"]


def decode(system_prompt: str, user_content: str, api_key: str) -> str:
    out = api_post(
        "/v1/messages",
        {
            "model": MODEL,
            "max_tokens": MAX_TOKENS,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_content}],
        },
        api_key,
    )
    return out["content"][0]["text"]


def canonical_user_msg(spec_md_text: str, section: str, rid_num: str) -> str:
    return (
        "SPEC.md content (provided inline — no filesystem access in this evaluation):\n\n"
        f"<SPEC.md>\n{spec_md_text}\n</SPEC.md>\n\n"
        f"$ARGUMENTS: §{section}.{rid_num}"
    )


def load_prior_records(results_json: Path) -> list[dict]:
    if not results_json.exists():
        return []
    try:
        data = json.loads(results_json.read_text())
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def compute_section_stats(values: list[float]) -> dict:
    n = len(values)
    if n == 0:
        return {"mean": 0.0, "median": 0.0, "p25": 0.0, "p75": 0.0, "n": 0}
    if n >= 2:
        q = statistics.quantiles(values, n=4, method="inclusive")
        p25, p75 = q[0], q[2]
    else:
        p25 = p75 = values[0]
    return {
        "mean": round(statistics.fmean(values), 4),
        "median": round(statistics.median(values), 4),
        "p25": round(p25, 4),
        "p75": round(p75, 4),
        "n": n,
    }


def compute_summary(per_sample: list[dict]) -> dict:
    summary: dict[str, dict[str, dict]] = {}
    decoders = ("minimal", "canonical")
    for section in SECTIONS + ("all",):
        summary[section] = {}
        rows = (
            per_sample
            if section == "all"
            else [s for s in per_sample if s["section"] == section]
        )
        for d in decoders:
            vals = [s[f"reduction_{d}"] for s in rows]
            summary[section][d] = compute_section_stats(vals)
    return summary


def schema_compatible(prior: dict) -> bool:
    if not prior.get("per_sample"):
        return False
    sample = prior["per_sample"][0]
    required = {
        "id", "section", "body", "n_glyph",
        "prose_minimal", "n_prose_minimal", "reduction_minimal",
        "prose_canonical", "n_prose_canonical", "reduction_canonical",
    }
    return required.issubset(sample.keys())


def emit_trend(prior: list[dict], current: dict) -> None:
    compatible_prior = [p for p in prior if schema_compatible(p)]
    if not compatible_prior:
        if prior:
            print(
                "\nstats-over-time: skipped — prior records use single-decoder schema, "
                "incompatible w/ two-decoder format; trend resumes after next compatible run",
                flush=True,
            )
        return
    last = compatible_prior[-1]
    for d in ("minimal", "canonical"):
        cur_s = current["summary"]["all"][d]
        last_s = last["summary"]["all"][d]
        print(
            f"\ndelta vs last [{d}]: "
            f"Δmean {cur_s['mean'] - last_s['mean']:+.4f} | "
            f"Δmedian {cur_s['median'] - last_s['median']:+.4f} | "
            f"Δn {cur_s['n'] - last_s['n']:+d}",
            flush=True,
        )
        means = [
            r["summary"]["all"][d]["mean"]
            for r in (compatible_prior + [current])[-TREND_WINDOW:]
        ]
        print(
            f"last-{len(means)} mean trend [{d}]: "
            + " -> ".join(f"{m:.4f}" for m in means),
            flush=True,
        )
    print(
        f"\ncommit shift: {last['commit_sha'][:8]} -> {current['commit_sha'][:8]}",
        flush=True,
    )


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent.parent
    spec_md = repo_root / "SPEC.md"
    explain_skill_md = repo_root / "skills" / "explain" / "SKILL.md"
    results_json = script_dir / "telegraph-bench-results.json"

    api_key = resolve_api_key()
    rows = extract_corpus(spec_md)
    explain_system = explain_skill_md.read_text()
    spec_md_text = spec_md.read_text()

    print(
        "| id  | sec | n_glyph | n_pmin | red_min | n_pcan | red_can |",
        flush=True,
    )
    print(
        "|-----|-----|---------|--------|---------|--------|---------|",
        flush=True,
    )
    per_sample = []
    for rid, section, body in rows:
        rid_num = rid[1:]
        n_g = count_tokens(body, api_key)
        prose_m = decode(MINIMAL_SYSTEM, body, api_key)
        n_pm = count_tokens(prose_m, api_key)
        red_m = round(1 - n_g / n_pm, 4) if n_pm > 0 else 0.0
        canonical_input = canonical_user_msg(spec_md_text, section, rid_num)
        prose_c = decode(explain_system, canonical_input, api_key)
        n_pc = count_tokens(prose_c, api_key)
        red_c = round(1 - n_g / n_pc, 4) if n_pc > 0 else 0.0
        per_sample.append(
            {
                "id": rid,
                "section": section,
                "body": body,
                "n_glyph": n_g,
                "prose_minimal": prose_m,
                "n_prose_minimal": n_pm,
                "reduction_minimal": red_m,
                "prose_canonical": prose_c,
                "n_prose_canonical": n_pc,
                "reduction_canonical": red_c,
            }
        )
        print(
            f"| {rid:<3} | {section}   | {n_g:>7} | {n_pm:>6} | {red_m:>+.4f} | {n_pc:>6} | {red_c:>+.4f} |",
            flush=True,
        )

    summary = compute_summary(per_sample)
    print("", flush=True)
    print("| section | decoder   | mean    | median  | p25     | p75     | n  |", flush=True)
    print("|---------|-----------|---------|---------|---------|---------|----|", flush=True)
    for section in SECTIONS + ("all",):
        for d in ("minimal", "canonical"):
            s = summary[section][d]
            print(
                f"| {section:<7} | {d:<9} | {s['mean']:>+.4f} | {s['median']:>+.4f} | "
                f"{s['p25']:>+.4f} | {s['p75']:>+.4f} | {s['n']:>2} |",
                flush=True,
            )

    commit_sha = (
        subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo_root)
        .decode()
        .strip()
    )
    record = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
        "commit_sha": commit_sha,
        "model": MODEL,
        "per_sample": per_sample,
        "summary": summary,
    }

    prior = load_prior_records(results_json)
    emit_trend(prior, record)
    prior.append(record)
    results_json.write_text(json.dumps(prior, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
