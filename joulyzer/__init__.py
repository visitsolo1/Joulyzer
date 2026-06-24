"""Joulyzer — AI Trade Journal Analyzer + Agent Tool.

A lightweight library that ingests a trader's exported trade journal
(CSV from Bitget / Binance / Bybit / generic exports) and produces
structured analytics: win rate, profit factor, expectancy, drawdown,
symbol breakdown, time-of-day edge, and tag breakdown. Designed to be
consumed by an AI agent via a small, stable tool surface.

Built for Bitget AI Base Camp Hackathon S1, Track 2 (Trading Infra).
"""

from .parser import load_journal, JournalLoadError
from .metrics import compute_metrics, MetricsReport
from .report import render_text_report, to_json, to_dict

__all__ = [
    # Core analytics
    "load_journal",
    "JournalLoadError",
    "compute_metrics",
    "MetricsReport",
    "render_text_report",
    "to_json",
    "to_dict",
    # Agent surface (lazy via __getattr__)
    "analyze_journal",
    "tool_schema",
    "mcp_manifest",
    "TOOL_SCHEMA",
]

__version__ = "0.2.0"


def __getattr__(name: str):
    """Lazily import the agent adapter so ``python -m joulyzer.agent`` is warning-free."""
    if name in {"analyze_journal", "tool_schema", "mcp_manifest", "TOOL_SCHEMA"}:
        from . import agent as _agent
        value = getattr(_agent, name)
        globals()[name] = value  # cache for next access
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
