"""Basic unit tests for Joulyzer."""

from datetime import datetime
import math
import os
import sys
from pathlib import Path

# Allow running from the repo root without install.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from joulyzer import load_journal, compute_metrics, render_text_report, to_json
from joulyzer.parser import JournalLoadError, Trade

SAMPLE = Path(__file__).resolve().parents[1] / "examples" / "sample_journal.csv"


def test_load_sample():
    trades = load_journal(SAMPLE)
    assert len(trades) >= 5
    assert all(t.symbol for t in trades)


def test_metrics_shape():
    trades = load_journal(SAMPLE)
    r = compute_metrics(trades)
    assert r.trade_count == len([t for t in trades if not t.is_open])
    assert 0.0 <= r.win_rate <= 1.0
    assert math.isfinite(r.profit_factor) or r.profit_factor == float("inf")
    assert isinstance(r.by_symbol, list) and r.by_symbol
    j = to_json(r)
    assert "net_pnl" in j


def test_text_report_contains_key_lines():
    trades = load_journal(SAMPLE)
    r = compute_metrics(trades)
    out = render_text_report(r)
    assert "Joulyzer Report" in out
    assert "Net PnL" in out
    assert "By symbol" in out


def test_trade_helpers():
    t = Trade(
        symbol="BTCUSDT", side="long",
        entry_time=datetime(2025, 1, 1, 10, 0),
        exit_time=datetime(2025, 1, 1, 11, 0),
        entry_price=100, exit_price=110, size=1, pnl=10,
    )
    assert t.is_win
    assert t.hold_minutes == 60.0


def test_load_missing_file():
    try:
        load_journal("/nope/does/not/exist.csv")
    except JournalLoadError:
        return
    assert False, "expected JournalLoadError"
