"""Tests for the Bitget generator + agent adapter.

Verifies:

* Generator is deterministic for a given seed (reproducibility requirement).
* Round-trip fills parse cleanly back into trades via ``load_journal``.
* Bitget-fill -> journal conversion preserves trade count.
* Agent tool entry point returns a parseable report on a valid journal.
* Agent tool entry point returns a structured error on a missing file
  (sandbox-safe failure mode).
* Tool schema is valid JSON-Schema-ish (has name, description, parameters).
* MCP manifest has a tool list.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from joulyzer import (
    TOOL_SCHEMA,
    analyze_journal,
    compute_metrics,
    load_journal,
    mcp_manifest,
    tool_schema,
)
from joulyzer.generators import (
    fills_to_journal_csv,
    generate_bitget_fills,
)
from joulyzer.generators.bitget_paper import fills_to_api_log


def test_generator_is_deterministic():
    a = generate_bitget_fills(seed=7, n=20)
    b = generate_bitget_fills(seed=7, n=20)
    assert a == b, "same seed must yield identical fills"
    # 2 fills per round-trip (open + close)
    assert len(a) == 40


def test_generator_different_seeds_diverge():
    a = generate_bitget_fills(seed=1, n=20)
    b = generate_bitget_fills(seed=2, n=20)
    assert a != b


def test_fills_have_bitget_shape():
    fills = generate_bitget_fills(seed=42, n=10)
    for f in fills:
        assert f.orderId.startswith("bg-")
        assert f.symbol.endswith("USDT")
        assert f.side in ("buy", "sell")
        assert f.tradeSide in ("open", "close")
        assert f.price > 0
        assert f.size > 0
        assert f.cTime.endswith("Z")  # ISO 8601 UTC


def test_journal_round_trip(tmp_path: Path):
    fills = generate_bitget_fills(seed=99, n=40)
    csv_path = fills_to_journal_csv(fills, tmp_path / "session.csv")
    trades = load_journal(csv_path)
    # Each round-trip produces one Trade.
    assert len(trades) == 40
    # Metrics should run without error.
    r = compute_metrics(trades)
    assert r.trade_count == len(trades)


def test_api_log_jsonl_shape(tmp_path: Path):
    fills = generate_bitget_fills(seed=11, n=8)
    log_path = fills_to_api_log(fills, tmp_path / "calls.jsonl")
    lines = log_path.read_text().strip().split("\n")
    assert len(lines) == len(fills)
    first = json.loads(lines[0])
    for key in ("ts", "endpoint", "params", "response_code", "latency_ms"):
        assert key in first


def test_agent_text_format(tmp_path: Path):
    fills = generate_bitget_fills(seed=5, n=20)
    csv_path = fills_to_journal_csv(fills, tmp_path / "j.csv")
    out = analyze_journal(str(csv_path), format="text")
    assert isinstance(out, str)
    assert "Joulyzer Report" in out
    assert "Net PnL" in out


def test_agent_json_format(tmp_path: Path):
    fills = generate_bitget_fills(seed=6, n=15)
    csv_path = fills_to_journal_csv(fills, tmp_path / "j.csv")
    out = analyze_journal(str(csv_path), format="json")
    assert isinstance(out, str)
    parsed = json.loads(out)
    assert "net_pnl" in parsed
    assert "by_symbol" in parsed


def test_agent_dict_format(tmp_path: Path):
    fills = generate_bitget_fills(seed=8, n=12)
    csv_path = fills_to_journal_csv(fills, tmp_path / "j.csv")
    out = analyze_journal(str(csv_path), format="dict")
    assert isinstance(out, dict)
    assert "win_rate" in out


def test_agent_missing_file_returns_structured_error(tmp_path: Path):
    out = analyze_journal(str(tmp_path / "does_not_exist.csv"))
    assert isinstance(out, dict)
    assert out.get("status") == "failed"
    assert "error" in out


def test_tool_schema_shape():
    s = tool_schema()
    assert s["name"] == "analyze_journal"
    assert "description" in s and len(s["description"]) > 20
    assert s["parameters"]["type"] == "object"
    assert "csv_path" in s["parameters"]["properties"]
    assert "csv_path" in s["parameters"]["required"]


def test_mcp_manifest_has_tool():
    m = mcp_manifest()
    assert m["name"] == "joulyzer"
    assert any(t["name"] == "analyze_journal" for t in m["tools"])


def test_live_usage_harness_artifact_shape(tmp_path: Path):
    """The live_usage harness writes JSONL + summary JSON + summary MD.

    We don't run the full harness here (it spawns subprocesses); we just
    check the schema is what we documented. Run ``scripts/live_usage_harness.py``
    (or ``bash scripts/verify_submission.sh``) to actually populate it.
    """
    import json as _json

    expected_keys = {
        "ts",
        "ts_end",
        "latency_ms",
        "caller",
        "operation",
        "input_journal",
        "input_format",
        "status",
        "exit_code",
        "error",
        "output_size_bytes",
        "output_preview",
    }
    sample_record = {
        "ts": "2026-06-24T19:38:19.848595Z",
        "ts_end": "2026-06-24T19:38:19.860439Z",
        "latency_ms": 11.844,
        "caller": "cli",
        "operation": "cli:text",
        "input_journal": "/tmp/example.csv",
        "input_format": "text",
        "status": "ok",
        "exit_code": 0,
        "error": None,
        "output_size_bytes": 1073,
        "output_preview": "================ Joulyzer Report",
    }
    assert expected_keys.issubset(sample_record.keys())

    # If the harness has been run, the on-disk JSONL must conform.
    repo_root = Path(__file__).resolve().parents[1]
    usage_log = repo_root / "verifiable_usage_records" / "live_usage.jsonl"
    if usage_log.exists():
        with usage_log.open() as f:
            for i, line in enumerate(f):
                if not line.strip():
                    continue
                rec = _json.loads(line)
                assert expected_keys.issubset(rec.keys()), f"line {i} missing keys"
                assert rec["caller"] in {"cli", "function", "mcp"}
                assert rec["status"] in {"ok", "error"}
                assert isinstance(rec["latency_ms"], (int, float))
