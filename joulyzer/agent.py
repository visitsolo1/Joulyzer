"""Agent-framework adapter — expose joulyzer as a callable tool.

This module is what makes Joulyzer "agent-grade" trading infra: any
LLM-driven agent (Claude Code, Cursor, Qwen, a LangChain ReAct agent,
a CrewAI crew, etc.) can call :func:`analyze_journal` with two strings
(``csv_path``, ``format``) and get back a deterministic report.

Two surfaces are provided:

1. :func:`analyze_journal` — plain Python function with a stable signature,
   suitable for any tool-calling framework.
2. :func:`tool_schema` — a JSON-Schema tool definition (OpenAI / Claude /
   Qwen-compatible). Wire this into your agent's tool registry and the
   model will be able to call joulyzer autonomously.
3. :func:`mcp_manifest` — a minimal Model Context Protocol (MCP) server
   manifest. Spawns a stdio JSON-RPC handler so any MCP-aware client
   (Claude Code, Continue, etc.) can mount joulyzer as a tool server.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Literal

from .metrics import compute_metrics
from .parser import JournalLoadError, load_journal
from .report import render_text_report, to_json


OutputFormat = Literal["text", "json", "dict"]


def analyze_journal(
    csv_path: str,
    format: OutputFormat = "text",  # noqa: A002 -- public tool signature
) -> dict[str, Any] | str:
    """Agent tool entry point: load a journal CSV and return analytics.

    Parameters
    ----------
    csv_path
        Path to the trade-journal CSV. Accepts Bitget / Binance / Bybit
        exports or any CSV matching joulyzer's alias table (see SKILL.md).
    format
        ``"text"`` returns a human-readable report; ``"json"`` returns a JSON
        string; ``"dict"`` returns the raw Python dict (only useful in-process).

    Returns
    -------
    str | dict
        The report. On error returns ``{"error": "...", "status": "failed"}``
        so the calling agent can branch on the result without parsing.

    Notes
    -----
    Designed to be safe to call from a sandboxed agent loop:

    * No network calls.
    * No third-party deps beyond Python stdlib.
    * Deterministic — same input => same output.
    * Bounded input — only reads the CSV the agent names.
    """
    try:
        trades = load_journal(csv_path)
        if not trades:
            return {
                "status": "failed",
                "error": f"No trades found in journal: {csv_path}",
            }
        report = compute_metrics(trades)
        if format == "text":
            return render_text_report(report)
        if format == "json":
            return to_json(report)
        return report.to_dict()
    except JournalLoadError as e:
        return {"status": "failed", "error": f"JournalLoadError: {e}"}
    except FileNotFoundError as e:
        return {"status": "failed", "error": f"FileNotFoundError: {e}"}
    except Exception as e:  # noqa: BLE001 -- agent surface must never raise
        return {"status": "failed", "error": f"{type(e).__name__}: {e}"}


# OpenAI / Anthropic / Qwen compatible tool schema. Wire this into the
# model's tool registry; the model will produce a tool_call like
#   {"name": "analyze_journal", "arguments": {"csv_path": "...", "format": "json"}}
# which your dispatcher hands to :func:`analyze_journal` above.
TOOL_SCHEMA: dict[str, Any] = {
    "name": "analyze_journal",
    "description": (
        "Load a CSV trade journal (Bitget / Binance / Bybit / generic export) "
        "and return structured performance analytics: win rate, profit factor, "
        "expectancy, drawdown, MAE/MFE-style metrics, symbol breakdown, "
        "time-of-day breakdown, and tag breakdown. Use this whenever the user "
        "shares a trade log or asks about their edge, win rate, best setup, "
        "or worst hour."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "csv_path": {
                "type": "string",
                "description": (
                    "Absolute or relative path to the CSV trade journal. "
                    "Headers are auto-detected (see joulyzer SKILL.md for aliases)."
                ),
            },
            "format": {
                "type": "string",
                "enum": ["text", "json", "dict"],
                "description": (
                    "Output format. 'text' = human-readable report; 'json' = "
                    "stringified JSON for piping into another tool; 'dict' = "
                    "raw dict (only usable in-process)."
                ),
                "default": "text",
            },
        },
        "required": ["csv_path"],
    },
}


def tool_schema() -> dict[str, Any]:
    """Return the tool schema. Equivalent to ``TOOL_SCHEMA`` but stable callable."""
    return TOOL_SCHEMA


def mcp_manifest() -> dict[str, Any]:
    """Minimal MCP (Model Context Protocol) server manifest.

    Spawn this with::

        python -m joulyzer.agent --mcp

    and point any MCP-aware client (Claude Code, Continue, the
    Bitget getagent CLI) at it. The server speaks JSON-RPC over stdio and
    exposes the same ``analyze_journal`` tool.
    """
    return {
        "name": "joulyzer",
        "version": "0.2.0",
        "description": (
            "Trade-journal analytics for AI agents. Ingests Bitget / Binance / "
            "Bybit CSV exports and returns deterministic performance metrics."
        ),
        "tools": [
            {
                "name": TOOL_SCHEMA["name"],
                "description": TOOL_SCHEMA["description"],
                "inputSchema": TOOL_SCHEMA["parameters"],
            }
        ],
    }


# ---------------------------------------------------------------------------
# MCP stdio handler — tiny, self-contained, no external deps.
# ---------------------------------------------------------------------------

_MCP_DISPATCH = {
    "analyze_journal": lambda args: analyze_journal(
        csv_path=args.get("csv_path", ""),
        format=args.get("format", "text"),
    ),
}


def _mcp_serve() -> int:
    """Read JSON-RPC requests from stdin, write responses to stdout."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        method = req.get("method")
        req_id = req.get("id")
        params = req.get("params", {}) or {}

        if method == "tools/list":
            resp = {"jsonrpc": "2.0", "id": req_id, "result": mcp_manifest()}
        elif method == "tools/call":
            tool_name = params.get("name")
            args = params.get("arguments", {}) or {}
            handler = _MCP_DISPATCH.get(tool_name)
            if handler is None:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"unknown tool: {tool_name}"},
                }
            else:
                try:
                    result = handler(args)
                    if isinstance(result, (dict, list)):
                        result_text = json.dumps(result, indent=2, default=str)
                    else:
                        result_text = str(result)
                    resp = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {"content": [{"type": "text", "text": result_text}]},
                    }
                except Exception as e:  # noqa: BLE001
                    resp = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {"code": -32000, "message": f"{type(e).__name__}: {e}"},
                    }
        else:
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"unknown method: {method}"},
            }

        sys.stdout.write(json.dumps(resp, default=str) + "\n")
        sys.stdout.flush()
    return 0


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if argv and argv[0] == "--mcp":
        return _mcp_serve()
    if argv and argv[0] == "--schema":
        print(json.dumps(TOOL_SCHEMA, indent=2))
        return 0
    if argv and argv[0] == "--manifest":
        print(json.dumps(mcp_manifest(), indent=2))
        return 0
    print("usage: python -m joulyzer.agent [--mcp | --schema | --manifest]", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
