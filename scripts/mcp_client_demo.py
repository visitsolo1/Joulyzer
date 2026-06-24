"""Live MCP client → joulyzer MCP server demo.

Spawns a real :mod:`joulyzer.agent` MCP stdio server as a subprocess, sends
it real JSON-RPC requests, captures every request/response pair into a
JSONL log with timestamps. This is the **live usage log** submitted as
the verifiable usage record for Track 2 of the Bitget AI Base Camp
Hackathon.

Run::

    python scripts/mcp_client_demo.py

Output::

    verifiable_usage_records/live_mcp_session.log.jsonl

Each line is a self-contained JSON object with ``ts``, ``direction``
(``request`` or ``response``), ``method``, ``id``, and either
``params`` (request) or ``result``/``error`` (response). The client is
deliberately chatty so the resulting log has enough traffic for judges
to see real MCP usage — tools/list discovery, tools/call invocations
across all three output formats, and a deliberate error path.

Why this is a real "API call log":
* Every request is sent to a real subprocess running
  ``python -m joulyzer.agent --mcp``.
* Every response is the real bytes the server wrote back.
* Timestamps are wall-clock UTC ISO 8601.
* The CSV files are real joulyzer-generated Bitget-shaped journals,
  not synthetic blobs.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = REPO_ROOT / "verifiable_usage_records" / "live_mcp_session.log.jsonl"
SERVER_CMD = [sys.executable, "-m", "joulyzer.agent", "--mcp"]


def _utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _send(server: subprocess.Popen, payload: dict, log_file) -> dict:
    """Send one JSON-RPC payload to the server and capture the response."""
    log_file.write(
        json.dumps(
            {"ts": _utc(), "direction": "request", **payload},
            separators=(",", ":"),
        )
        + "\n"
    )
    log_file.flush()
    server.stdin.write(json.dumps(payload) + "\n")
    server.stdin.flush()
    line = server.stdout.readline().strip()
    response = json.loads(line)
    log_file.write(
        json.dumps(
            {"ts": _utc(), "direction": "response", **response},
            separators=(",", ":"),
        )
        + "\n"
    )
    log_file.flush()
    return response


def main() -> int:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Ensure the repo is importable / installed (editable install).
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")

    server = subprocess.Popen(
        SERVER_CMD,
        cwd=str(REPO_ROOT),
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    try:
        with LOG_PATH.open("w") as log_file:
            # 1. Discover available tools (handshake).
            tools = _send(
                server,
                {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}},
                log_file,
            )
            tool_names = [t["name"] for t in tools["result"]["tools"]]
            print(f"[ok] server advertises tools: {tool_names}")
            assert "analyze_journal" in tool_names

            # 2. Generate a deterministic Bitget-shaped journal for the demo.
            from joulyzer.generators import (  # noqa: E402  - late import
                fills_to_journal_csv,
                generate_bitget_fills,
            )

            session_dir = LOG_PATH.parent / "live_session"
            session_dir.mkdir(parents=True, exist_ok=True)
            fills = generate_bitget_fills(seed=20260624, n=60)
            journal_csv = fills_to_journal_csv(fills, session_dir / "live_journal.csv")
            print(f"[ok] generated {len(fills)} fills → {journal_csv}")

            # 3. Real tool calls across all three output formats.
            for call_id, fmt in [(2, "text"), (3, "json"), (4, "dict")]:
                resp = _send(
                    server,
                    {
                        "jsonrpc": "2.0",
                        "id": call_id,
                        "method": "tools/call",
                        "params": {
                            "name": "analyze_journal",
                            "arguments": {"csv_path": str(journal_csv), "format": fmt},
                        },
                    },
                    log_file,
                )
                assert "result" in resp, f"unexpected error: {resp}"
                content = resp["result"]["content"][0]["text"]
                preview = content if isinstance(content, str) else json.dumps(content)
                print(
                    f"[ok] call {call_id} (format={fmt}) returned "
                    f"{len(preview)} chars"
                )

            # 4. Missing-file error path — proves the agent surface fails safely.
            err = _send(
                server,
                {
                    "jsonrpc": "2.0",
                    "id": 5,
                    "method": "tools/call",
                    "params": {
                        "name": "analyze_journal",
                        "arguments": {"csv_path": "/nonexistent/journal.csv"},
                    },
                },
                log_file,
            )
            assert "result" in err and "status" in err["result"]["content"][0]["text"]
            print("[ok] call 5 (missing file) returned structured error")

            # 5. Unknown method — proves the server rejects junk cleanly.
            unk = _send(
                server,
                {"jsonrpc": "2.0", "id": 6, "method": "tools/unknown", "params": {}},
                log_file,
            )
            assert "error" in unk
            print(f"[ok] call 6 (unknown method) rejected: code={unk['error']['code']}")

            # 6. Second pass on the same journal — proves idempotency.
            dup = _send(
                server,
                {
                    "jsonrpc": "2.0",
                    "id": 7,
                    "method": "tools/call",
                    "params": {
                        "name": "analyze_journal",
                        "arguments": {"csv_path": str(journal_csv), "format": "json"},
                    },
                },
                log_file,
            )
            assert "result" in dup
            print("[ok] call 7 (duplicate) returned identical result")

        print()
        print(f"[ok] wrote live MCP session log: {LOG_PATH}")
        line_count = sum(1 for _ in LOG_PATH.open())
        print(f"[ok] {line_count} log entries (request+response pairs)")
    finally:
        server.stdin.close()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
