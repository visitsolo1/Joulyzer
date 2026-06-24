"""Live usage harness — drive joulyzer as third-party infra.

This script is the canonical "live usage record" for the Track 2
submission. It exercises joulyzer from three independent angles
(CLI subprocess, in-process function call, JSON-RPC MCP subprocess),
drives the live Bitget public API as a real-world smoke test of the
infra talking to the world, and writes everything to:

    verifiable_usage_records/
        live-usage-<ISO-timestamp>.json     full session JSON
        live-usage-<ISO-timestamp>.md       human-readable timeline
        live-usage-latest.json             copy of the most recent run
        live-usage-latest.md               copy of the most recent run
        live_usage_inputs/                 real CSV journals consumed

Pattern is intentionally the same as ``hasbunallah01/quant-copilot``
(another Bitget AI Base Camp Hackathon S1 submission) so judges can
read it the same way:

* Per-session header: ``session_id``, ``started_at``, ``ended_at``,
  ``duration_seconds``, ``total_records``.
* Per-record: ``ts`` (UTC ISO 8601 microsecond), ``kind`` (human
  label), ``request`` (input JSON), ``response`` (output JSON).
* Per-caller summary: count by caller (CLI / function / MCP),
  plus a separate counter for live Bitget public-API calls.
* Per-record numbered timeline in the markdown, with ``Request``
  and ``Response`` JSON blocks.

Run::

    python scripts/live_usage_harness.py [--seed 20260624] [--calls 12]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import subprocess
import sys
import time
import urllib.request
import urllib.error
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
USAGE_DIR = REPO_ROOT / "verifiable_usage_records"
USAGE_INPUTS = USAGE_DIR / "live_usage_inputs"

# Pattern after hasbunallah01/quant-copilot/logs/live-usage-*.{json,md}
# timestamp uses '-' instead of ':' for filesystem safety.
TS_TOKEN = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
LATEST_JSON = USAGE_DIR / "live-usage-latest.json"
LATEST_MD = USAGE_DIR / "live-usage-latest.md"
TIMESTAMPED_JSON = USAGE_DIR / f"live-usage-{TS_TOKEN}.json"
TIMESTAMPED_MD = USAGE_DIR / f"live-usage-{TS_TOKEN}.md"


# ---------- record schema ----------


@dataclass
class UsageRecord:
    ts: str
    kind: str
    request: dict
    response: dict
    duration_ms: float = 0.0
    caller: str = "internal"


# ---------- clock + id helpers ----------


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _utc_iso(dt: datetime) -> str:
    """ISO 8601 with microseconds and explicit +00:00 — matches reference."""
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")


def _session_id() -> str:
    """Short hex session id from the wall clock + microseconds."""
    return f"{int(time.time() * 1_000_000):x}"[-12:]


# ---------- live inputs ----------


def _ensure_inputs(seed: int) -> list[Path]:
    """Materialize real CSV journals under live_usage_inputs/."""
    USAGE_INPUTS.mkdir(parents=True, exist_ok=True)
    from joulyzer.generators import fills_to_journal_csv, generate_bitget_fills

    inputs: list[Path] = []
    specs = [
        ("bundled_sample.csv", None, 0),
        ("generated_small.csv", seed, 25),
        ("generated_medium.csv", seed + 1, 80),
    ]
    for name, s, n in specs:
        if name == "bundled_sample.csv":
            src = REPO_ROOT / "examples" / "sample_journal.csv"
        else:
            fills = generate_bitget_fills(seed=s, n=n)
            out = USAGE_INPUTS / name
            fills_to_journal_csv(fills, out)
            src = out
        inputs.append(src)
    return inputs


def _relpath(p: Path) -> str:
    """Render paths relative to the repo root so committed logs are portable."""
    try:
        return str(p.relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


# ---------- Caller 1: CLI subprocess ----------


def _call_cli(journal: Path, fmt: str) -> UsageRecord:
    cmd = [sys.executable, "-m", "joulyzer", str(journal)]
    if fmt == "json":
        cmd.append("--json")
    kind = f"CLI: analyze_journal {fmt}"
    request = {
        "method": "subprocess.run",
        "cmd": cmd,
        "cwd": _relpath(REPO_ROOT),
        "csv_path": _relpath(journal),
        "format": fmt,
    }
    start = _utc_now()
    t0 = time.perf_counter()
    proc = subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
        capture_output=True,
        text=True,
        timeout=30,
    )
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    end = _utc_now()
    if proc.returncode == 0:
        try:
            parsed = json.loads(proc.stdout)
            response: dict = {"status": "ok", "returncode": 0, "body": parsed}
        except json.JSONDecodeError:
            response = {
                "status": "ok",
                "returncode": 0,
                "body_kind": "text",
                "body": proc.stdout,
            }
    else:
        response = {
            "status": "error",
            "returncode": proc.returncode,
            "stderr": (proc.stderr or "").strip(),
        }
    return UsageRecord(
        ts=_utc_iso(start),
        kind=kind,
        request=request,
        response=response,
        duration_ms=round(elapsed_ms, 3),
        caller="cli",
    )


# ---------- Caller 2: in-process function ----------


def _call_function(journal: Path, fmt: str) -> UsageRecord:
    from joulyzer import analyze_journal

    kind = f"function: analyze_journal {fmt}"
    request = {
        "module": "joulyzer",
        "fn": "analyze_journal",
        "args": {"csv_path": _relpath(journal), "format": fmt},
    }
    start = _utc_now()
    t0 = time.perf_counter()
    try:
        result = analyze_journal(str(journal), format=fmt)  # type: ignore[arg-type]
    except Exception as e:  # noqa: BLE001
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        return UsageRecord(
            ts=_utc_iso(start),
            kind=kind,
            request=request,
            response={"status": "error", "error": f"{type(e).__name__}: {e}"},
            duration_ms=round(elapsed_ms, 3),
            caller="function",
        )
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    if isinstance(result, dict) and result.get("status") == "failed":
        response = {"status": "error", "error": result.get("error", "unknown")}
    elif isinstance(result, str):
        try:
            response = {"status": "ok", "body": json.loads(result)}
        except json.JSONDecodeError:
            response = {"status": "ok", "body_kind": "text", "body": result}
    else:
        response = {"status": "ok", "body": result}
    return UsageRecord(
        ts=_utc_iso(start),
        kind=kind,
        request=request,
        response=response,
        duration_ms=round(elapsed_ms, 3),
        caller="function",
    )


# ---------- Caller 3: MCP subprocess ----------


def _call_mcp(journal: Path, fmt: str, server: subprocess.Popen, call_id: int) -> UsageRecord:
    payload = {
        "jsonrpc": "2.0",
        "id": call_id,
        "method": "tools/call",
        "params": {
            "name": "analyze_journal",
            "arguments": {"csv_path": str(journal), "format": fmt},
        },
    }
    kind = f"MCP: tools/call analyze_journal {fmt}"
    request = {
        "method": "stdio JSON-RPC",
        "server": "python -m joulyzer.agent --mcp",
        "payload": payload,
        "csv_path": _relpath(journal),
        "format": fmt,
    }
    start = _utc_now()
    t0 = time.perf_counter()
    server.stdin.write(json.dumps(payload) + "\n")
    server.stdin.flush()
    line = server.stdout.readline().strip()
    response = json.loads(line)
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    # Pull out the inner content text if present.
    if "result" in response:
        content = response["result"].get("content", [])
        text = content[0]["text"] if content else ""
        if text.startswith("{") and '"status": "failed"' in text:
            response = {"status": "error", "raw": text}
        else:
            try:
                response = {"status": "ok", "body": json.loads(text)}
            except json.JSONDecodeError:
                response = {"status": "ok", "body_kind": "text", "body": text}
    else:
        response = {"status": "error", "error": response.get("error")}
    return UsageRecord(
        ts=_utc_iso(start),
        kind=kind,
        request=request,
        response=response,
        duration_ms=round(elapsed_ms, 3),
        caller="mcp",
    )


# ---------- Live Bitget public-API section ----------


_BITGET_ENDPOINTS = (
    ("/api/v2/public/time", "GET /api/v2/public/time"),
    ("/api/v2/spot/market/tickers?symbol=BTCUSDT", "GET /api/v2/spot/market/tickers?symbol=BTCUSDT"),
    ("/api/v2/spot/market/candles?symbol=BTCUSDT&granularity=1min&limit=2",
     "GET /api/v2/spot/market/candles?symbol=BTCUSDT&granularity=1min&limit=2"),
)


def _call_bitget_live() -> list[UsageRecord]:
    """Hit the real Bitget public REST endpoints.

    These are public, unauthenticated endpoints. Captures real network
    traffic with measured latency so the live usage log proves joulyzer's
    infra can stand next to a live exchange API. A failure here (no
    network, 5xx, etc.) is recorded as an honest error record rather
    than aborted — judges see exactly what happened.
    """
    records: list[UsageRecord] = []
    for endpoint, label in _BITGET_ENDPOINTS:
        url = f"https://api.bitget.com{endpoint}"
        kind = f"Bitget live call: {label}"
        request = {"method": "GET", "url": url, "endpoint": endpoint}
        start = _utc_now()
        t0 = time.perf_counter()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "joulyzer-live-usage/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:  # noqa: S310
                raw = resp.read()
                status = resp.status
                content_type = resp.headers.get("Content-Type", "")
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            try:
                parsed = json.loads(raw)
                sample: Any
                # Bitget wraps responses in {"code","msg","requestTime","data":...}
                # Unwrap to the interesting payload so judges see real data.
                if isinstance(parsed, dict) and "data" in parsed and isinstance(parsed["data"], (list, dict)):
                    inner = parsed["data"]
                    if isinstance(inner, list):
                        sample = inner[:2]
                    else:
                        inner_keys = list(inner.keys())[:3]
                        sample = {k: inner[k] for k in inner_keys} if inner_keys else inner
                elif isinstance(parsed, dict):
                    sample = {k: parsed[k] for k in list(parsed.keys())[:3]} if parsed else parsed
                elif isinstance(parsed, list):
                    sample = parsed[:2]
                else:
                    sample = parsed
                response = {
                    "status": "ok",
                    "http_status": status,
                    "latency_ms": round(elapsed_ms, 2),
                    "data_sample": sample,
                    "data_len": len(parsed) if isinstance(parsed, (list, dict)) else "n/a",
                    "content_type": content_type,
                }
            except json.JSONDecodeError:
                snippet = raw[:120].decode("utf-8", errors="replace")
                response = {
                    "status": "ok",
                    "http_status": status,
                    "latency_ms": round(elapsed_ms, 2),
                    "body_kind": "text",
                    "snippet": snippet,
                }
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            response = {
                "status": "error",
                "error": f"{type(e).__name__}: {e}",
                "latency_ms": round(elapsed_ms, 2),
            }
        records.append(
            UsageRecord(
                ts=_utc_iso(start),
                kind=kind,
                request=request,
                response=response,
                duration_ms=round(elapsed_ms, 3),
                caller="bitget_live",
            )
        )
    return records


# ---------- build the call plan ----------


def _build_call_plan(journals: list[Path]) -> list[tuple[str, Path, str]]:
    """3 journals x 3 formats x 3 callers, plus 3 deliberate error paths."""
    plan: list[tuple[str, Path, str]] = []
    for j in journals:
        for fmt in ("text", "json", "dict"):
            plan.append(("cli", j, fmt))
            plan.append(("function", j, fmt))
            plan.append(("mcp", j, fmt))
    bogus = USAGE_INPUTS / "bogus_no_pnl_or_price.csv"
    if not bogus.exists():
        bogus.write_text("foo,bar\n1,2\n")
    plan.append(("function", bogus, "text"))
    plan.append(("cli", Path("/nonexistent/journal.csv"), "text"))
    plan.append(("function", Path("/nonexistent/journal.csv"), "json"))
    return plan


# ---------- summarize ----------


def _summarize(records: list[UsageRecord]) -> dict[str, Any]:
    by_caller: dict[str, list[UsageRecord]] = {}
    for r in records:
        by_caller.setdefault(r.caller, []).append(r)

    summary: dict[str, Any] = {
        "total_records": len(records),
        "by_caller": {},
        "by_kind": {},
    }
    for caller, rs in by_caller.items():
        lats = [r.duration_ms for r in rs]
        ok = sum(1 for r in rs if r["response"]["status"] == "ok") if isinstance(rs[0], dict) else sum(1 for r in rs if r.response["status"] == "ok")
        err = len(rs) - ok
        summary["by_caller"][caller] = {
            "calls": len(rs),
            "ok": ok,
            "errors": err,
            "mean_latency_ms": round(statistics.mean(lats), 3) if lats else 0.0,
            "p50_latency_ms": round(statistics.median(lats), 3) if lats else 0.0,
        }
    for r in records:
        summary["by_kind"][r.kind] = summary["by_kind"].get(r.kind, 0) + 1
    return summary


# ---------- markdown rendering ----------


def _render_markdown(session: dict[str, Any], records: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Joulyzer — Live Usage Record")
    lines.append("")
    lines.append(f"- **Session ID**: `{session['session_id']}`")
    lines.append(f"- **Started**: {session['started_at']}")
    lines.append(f"- **Ended**: {session['ended_at']}")
    lines.append(f"- **Duration**: {session['duration_seconds']} seconds")
    lines.append(f"- **Total recorded events**: {summary['total_records']}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")

    # Use the caller names from the schema for the headline bullets.
    for caller, stats in summary["by_caller"].items():
        label = {
            "cli": "CLI subprocess calls (`python -m joulyzer <journal> [--json]`)",
            "function": "In-process Python function calls (`joulyzer.analyze_journal`)",
            "mcp": "JSON-RPC MCP subprocess calls (`python -m joulyzer.agent --mcp`)",
            "bitget_live": "Live Bitget public API calls (`api.bitget.com`)",
        }.get(caller, f"`{caller}` calls")
        lines.append(
            f"- {label}: **{stats['calls']}** (ok {stats['ok']}, errors {stats['errors']}, "
            f"mean {stats['mean_latency_ms']:.2f} ms, p50 {stats['p50_latency_ms']:.2f} ms)"
        )
    lines.append("")
    lines.append("## Timeline")
    lines.append("")

    for i, r in enumerate(records, 1):
        lines.append(f"### {i}. [{r['ts']}] {r['kind']}")
        lines.append("")
        lines.append("**Request**")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps(r["request"], indent=2, default=str))
        lines.append("```")
        lines.append("")
        # Trim very large bodies in the markdown to keep the file readable;
        # the full data lives in the JSON sibling.
        resp_for_md = _trim_response(r["response"])
        lines.append("**Response**")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps(resp_for_md, indent=2, default=str))
        lines.append("```")
        lines.append("")
    return "\n".join(lines) + "\n"


def _trim_response(response: dict, max_str: int = 400) -> dict:
    """Trim long string bodies to keep the markdown readable."""
    out: dict = {}
    for k, v in response.items():
        if isinstance(v, str) and len(v) > max_str:
            out[k] = v[:max_str] + f"... <{len(v) - max_str} more chars>"
        elif isinstance(v, list) and len(v) > 3:
            out[k] = v[:3] + [f"... <{len(v) - 3} more items>"]
        elif isinstance(v, dict) and len(v) > 6:
            keys = list(v.keys())[:6]
            out[k] = {k2: v[k2] for k2 in keys}
            out[k]["..."] = f"<{len(v) - 6} more keys>"
        else:
            out[k] = v
    return out


# ---------- orchestration ----------


def _record_to_dict(r: UsageRecord) -> dict[str, Any]:
    return asdict(r)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=20260624)
    args = p.parse_args()

    USAGE_DIR.mkdir(parents=True, exist_ok=True)
    journals = _ensure_inputs(args.seed)
    plan = _build_call_plan(journals)

    session_id = _session_id()
    started_at = _utc_now()
    records: list[UsageRecord] = []

    # Spin up the MCP server once and reuse it for all mcp:* calls.
    mcp_server = subprocess.Popen(
        [sys.executable, "-m", "joulyzer.agent", "--mcp"],
        cwd=str(REPO_ROOT),
        env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    try:
        mcp_call_id = 1000
        for caller, journal, fmt in plan:
            if caller == "cli":
                rec = _call_cli(journal, fmt)
            elif caller == "function":
                rec = _call_function(journal, fmt)
            else:
                rec = _call_mcp(journal, fmt, mcp_server, mcp_call_id)
                mcp_call_id += 1
            records.append(rec)
            print(
                f"[{len(records):>2}/{len(plan)}] {rec.caller:<12} {rec.kind:<46} "
                f"{rec.response.get('status', '?'):<5} {rec.duration_ms:>7.2f} ms"
            )

        # Live Bitget public-API smoke section.
        print()
        print("    -- live api --")
        for rec in _call_bitget_live():
            records.append(rec)
            print(
                f"[{len(records):>2}/{len(plan)+3}] {rec.caller:<12} {rec.kind:<46} "
                f"{rec.response.get('status', '?'):<5} {rec.duration_ms:>7.2f} ms"
            )
    finally:
        mcp_server.stdin.close()
        try:
            mcp_server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            mcp_server.kill()

    ended_at = _utc_now()
    duration_seconds = round((ended_at - started_at).total_seconds(), 3)
    summary = _summarize(records)

    record_dicts = [_record_to_dict(r) for r in records]
    session_payload = {
        "session_id": session_id,
        "started_at": _utc_iso(started_at),
        "ended_at": _utc_iso(ended_at),
        "duration_seconds": duration_seconds,
        "summary": {
            "total_records": summary["total_records"],
            **{caller: stats["calls"] for caller, stats in summary["by_caller"].items()},
        },
        "by_caller": summary["by_caller"],
        "by_kind": summary["by_kind"],
        "records": record_dicts,
    }

    # Write timestamped + latest copies (matches reference pattern).
    TIMESTAMPED_JSON.write_text(json.dumps(session_payload, indent=2))
    TIMESTAMPED_MD.write_text(_render_markdown(session_payload, record_dicts, summary))
    LATEST_JSON.write_text(json.dumps(session_payload, indent=2))
    LATEST_MD.write_text(_render_markdown(session_payload, record_dicts, summary))

    # Best-effort cleanup of older timestamped files so the directory
    # doesn't grow unboundedly across re-runs. Keep the latest 5.
    _prune_old_logs(keep=5)

    print()
    print(f"[ok] session_id : {session_id}")
    print(f"[ok] duration   : {duration_seconds} s")
    print(f"[ok] records    : {summary['total_records']}")
    print(f"[ok] wrote      : {TIMESTAMPED_JSON.name}")
    print(f"[ok] wrote      : {TIMESTAMPED_MD.name}")
    print(f"[ok] wrote      : {LATEST_JSON.name}")
    print(f"[ok] wrote      : {LATEST_MD.name}")
    return 0


def _prune_old_logs(keep: int) -> None:
    pattern = re.compile(r"^live-usage-\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}Z\.(json|md)$")
    files = sorted(
        (p for p in USAGE_DIR.glob("live-usage-*.json") if pattern.match(p.name)),
        key=lambda p: p.name,
        reverse=True,
    )
    extras = files[keep:]
    for p in extras:
        try:
            p.unlink()
        except OSError:
            pass
        md = p.with_suffix(".md")
        if md.exists():
            try:
                md.unlink()
            except OSError:
                pass


if __name__ == "__main__":
    raise SystemExit(main())
