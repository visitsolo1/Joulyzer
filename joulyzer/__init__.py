"""Joulyzer — AI Trade Journal Analyzer.

A lightweight library that ingests a trader's exported trade journal
(CSV / Excel) and produces structured analytics: win rate, profit factor,
expectancy, drawdown, MAE/MFE, time-of-day edge, symbol-level breakdown,
and simple behavioral tagging. Designed to be consumed by an AI agent
via a small, stable function surface.
"""

from .parser import load_journal, JournalLoadError
from .metrics import compute_metrics, MetricsReport
from .report import render_text_report, to_json, to_dict

__all__ = [
    "load_journal",
    "JournalLoadError",
    "compute_metrics",
    "MetricsReport",
    "render_text_report",
    "to_json",
    "to_dict",
]

__version__ = "0.1.0"
