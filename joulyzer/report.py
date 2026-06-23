"""Render MetricsReport as text or JSON."""

from __future__ import annotations

import json
from typing import Any

from .metrics import MetricsReport


def to_dict(report: MetricsReport) -> dict[str, Any]:
    return report.to_dict()


def to_json(report: MetricsReport, indent: int = 2) -> str:
    return json.dumps(to_dict(report), indent=indent, default=str)


def render_text_report(report: MetricsReport) -> str:
    pf = "∞" if report.profit_factor == float("inf") else f"{report.profit_factor:.2f}"
    lines = [
        "================ Joulyzer Report ================",
        f"Trades (closed): {report.trade_count}   Wins: {report.win_count}   "
        f"Losses: {report.loss_count}   Open: {report.open_count}",
        f"Win rate:        {report.win_rate * 100:.1f}%",
        f"Net PnL:         {report.net_pnl:,.2f}",
        f"Gross profit:    {report.gross_profit:,.2f}   Gross loss: {report.gross_loss:,.2f}",
        f"Profit factor:   {pf}",
        f"Avg win:         {report.avg_win:,.2f}   Avg loss: {report.avg_loss:,.2f}",
        f"Expectancy:      {report.expectancy:,.2f} per trade",
        f"Max drawdown:    {report.max_drawdown:,.2f}",
        f"Avg hold (min):  {report.avg_hold_minutes:.1f}",
        f"Best trade:      {report.best_trade:,.2f}   Worst: {report.worst_trade:,.2f}",
        "",
        "--- By symbol ---",
    ]
    if not report.by_symbol:
        lines.append("  (no data)")
    for s in report.by_symbol:
        lines.append(
            f"  {s.symbol:<10} trades={s.trades:<4} wins={s.wins:<4} losses={s.losses:<4} "
            f"WR={s.win_rate*100:5.1f}%  net={s.net_pnl:,.2f}"
        )
    lines.append("")
    lines.append("--- By hour (entry) ---")
    if not report.by_hour:
        lines.append("  (no data)")
    else:
        for h in sorted(report.by_hour):
            slot = report.by_hour[h]
            lines.append(f"  {h:02d}:00  trades={int(slot['trades']):<4} net={slot['net_pnl']:,.2f}")
    lines.append("")
    lines.append("--- By tag ---")
    if not report.by_tag:
        lines.append("  (no data)")
    else:
        for tag, slot in sorted(report.by_tag.items(), key=lambda kv: -kv[1]["net_pnl"]):
            lines.append(f"  {tag:<14} trades={int(slot['trades']):<4} net={slot['net_pnl']:,.2f}")
    lines.append("=================================================")
    return "\n".join(lines)
