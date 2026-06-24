"""Example: an AI agent uses joulyzer as a tool to review a paper-trade session.

Run::

    python examples/agent_integration.py

This script is the canonical "another developer can integrate it" example
referenced in the README and the Track 2 submission. It shows the full
loop end-to-end:

  1. Generate a deterministic Bitget-shaped paper-trade session.
  2. Convert fills -> joulyzer journal CSV (same code path an Agent would use).
  3. Wire joulyzer into a tool-calling dispatcher (mimics Claude Code /
     LangChain ReAct / Qwen tool registry).
  4. Dispatch a fake model tool-call into joulyzer and print the result.

A separate, near-identical pattern works with LangChain's
``StructuredTool.from_function`` — see the README for the snippet.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Make the repo importable when run as `python examples/agent_integration.py`.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from joulyzer import (
    TOOL_SCHEMA,
    analyze_journal,
)
from joulyzer.generators import (
    fills_to_api_log,
    fills_to_journal_csv,
    generate_bitget_fills,
)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    out_dir = repo_root / "verifiable_usage_records" / "integration_run"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: generate deterministic Bitget paper-trade ledger.
    fills = generate_bitget_fills(seed=20260624, n=120)
    api_log_path = fills_to_api_log(fills, out_dir / "bitget_api_call_log.jsonl")

    # Step 2: convert to joulyzer's flat journal CSV (what an Agent would export).
    journal_csv = fills_to_journal_csv(fills, out_dir / "agent_session_journal.csv")

    # Step 3+4: pretend the model just produced this tool_call:
    tool_call = {
        "name": TOOL_SCHEMA["name"],
        "arguments": {"csv_path": str(journal_csv), "format": "json"},
    }

    # In a real agent loop this would be done by the tool dispatcher.
    result = analyze_journal(**tool_call["arguments"])

    # Persist the result for judges.
    out_path = out_dir / "agent_tool_call_result.json"
    with out_path.open("w") as f:
        json.dump(
            {
                "tool_call": tool_call,
                "tool_schema_name": TOOL_SCHEMA["name"],
                "result_type": type(result).__name__,
                "result_preview": (
                    json.loads(result) if isinstance(result, str) else result
                ),
            },
            f,
            indent=2,
            default=str,
        )

    print(f"[ok] fills generated         : {len(fills)} (open+close pairs)")
    print(f"[ok] api call log written    : {api_log_path}")
    print(f"[ok] journal csv written     : {journal_csv}")
    print(f"[ok] agent tool call result  : {out_path}")
    print()
    if isinstance(result, str):
        # Already JSON-formatted
        parsed = json.loads(result)
        print(
            f"[ok] analyzed {parsed['trade_count']} closed trades, "
            f"net PnL {parsed['net_pnl']:,.2f}, "
            f"win rate {parsed['win_rate']*100:.1f}%, "
            f"profit factor {parsed['profit_factor']:.2f}"
        )
    else:
        print(f"[ok] result: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
