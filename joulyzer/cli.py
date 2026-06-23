"""Tiny CLI: `python -m joulyzer <journal.csv>` prints a text report.

Optional flags: --json   -> emit machine-readable JSON instead.
"""

from __future__ import annotations

import argparse
import sys

from .parser import load_journal, JournalLoadError
from .metrics import compute_metrics
from .report import render_text_report, to_json


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="joulyzer", description="Analyze a trade journal.")
    p.add_argument("journal", help="Path to CSV journal file")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    args = p.parse_args(argv)

    try:
        trades = load_journal(args.journal)
    except JournalLoadError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if not trades:
        print("error: no trades found in journal", file=sys.stderr)
        return 2

    report = compute_metrics(trades)
    if args.json:
        print(to_json(report))
    else:
        print(render_text_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
