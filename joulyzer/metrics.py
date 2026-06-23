"""Analytics computed from a list of Trade records."""

from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean, median
from typing import Iterable

from .parser import Trade


@dataclass
class SymbolBreakdown:
    symbol: str
    trades: int
    wins: int
    losses: int
    net_pnl: float
    win_rate: float


@dataclass
class MetricsReport:
    trade_count: int
    win_count: int
    loss_count: int
    open_count: int
    win_rate: float
    net_pnl: float
    gross_profit: float
    gross_loss: float
    profit_factor: float
    avg_win: float
    avg_loss: float
    expectancy: float
    max_drawdown: float
    avg_hold_minutes: float
    best_trade: float
    worst_trade: float
    by_symbol: list[SymbolBreakdown] = field(default_factory=list)
    by_hour: dict[int, dict[str, float]] = field(default_factory=dict)
    by_tag: dict[str, dict[str, float]] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "trade_count": self.trade_count,
            "win_count": self.win_count,
            "loss_count": self.loss_count,
            "open_count": self.open_count,
            "win_rate": self.win_rate,
            "net_pnl": self.net_pnl,
            "gross_profit": self.gross_profit,
            "gross_loss": self.gross_loss,
            "profit_factor": self.profit_factor,
            "avg_win": self.avg_win,
            "avg_loss": self.avg_loss,
            "expectancy": self.expectancy,
            "max_drawdown": self.max_drawdown,
            "avg_hold_minutes": self.avg_hold_minutes,
            "best_trade": self.best_trade,
            "worst_trade": self.worst_trade,
            "by_symbol": [s.__dict__ for s in self.by_symbol],
            "by_hour": self.by_hour,
            "by_tag": self.by_tag,
        }


def _drawdown(pnls: list[float]) -> float:
    peak = 0.0
    equity = 0.0
    dd = 0.0
    for p in pnls:
        equity += p
        if equity > peak:
            peak = equity
        dd = min(dd, equity - peak)
    return abs(dd)


def _by_symbol(trades: Iterable[Trade]) -> list[SymbolBreakdown]:
    buckets: dict[str, list[Trade]] = {}
    for t in trades:
        buckets.setdefault(t.symbol, []).append(t)
    out: list[SymbolBreakdown] = []
    for sym, items in buckets.items():
        wins = sum(1 for t in items if t.is_win)
        losses = sum(1 for t in items if t.is_loss)
        out.append(
            SymbolBreakdown(
                symbol=sym,
                trades=len(items),
                wins=wins,
                losses=losses,
                net_pnl=sum(t.pnl for t in items),
                win_rate=(wins / len(items)) if items else 0.0,
            )
        )
    return sorted(out, key=lambda s: s.net_pnl, reverse=True)


def _by_hour(trades: Iterable[Trade]) -> dict[int, dict[str, float]]:
    out: dict[int, dict[str, float]] = {}
    for t in trades:
        if t.entry_time is None:
            continue
        h = t.entry_time.hour
        slot = out.setdefault(h, {"trades": 0, "net_pnl": 0.0})
        slot["trades"] += 1
        slot["net_pnl"] += t.pnl
    return out


def _by_tag(trades: Iterable[Trade]) -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = {}
    for t in trades:
        if not t.tags:
            continue
        for tag in t.tags:
            slot = out.setdefault(tag, {"trades": 0, "net_pnl": 0.0})
            slot["trades"] += 1
            slot["net_pnl"] += t.pnl
    return out


def compute_metrics(trades: list[Trade]) -> MetricsReport:
    closed = [t for t in trades if not t.is_open]
    wins = [t.pnl for t in closed if t.is_win]
    losses = [t.pnl for t in closed if t.is_loss]
    pnls = [t.pnl for t in closed]

    gross_profit = sum(wins) if wins else 0.0
    gross_loss = abs(sum(losses)) if losses else 0.0
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float("inf") if gross_profit else 0.0
    avg_win = mean(wins) if wins else 0.0
    avg_loss = mean(losses) if losses else 0.0

    trade_count = len(closed)
    win_count = len(wins)
    loss_count = len(losses)
    win_rate = (win_count / trade_count) if trade_count else 0.0
    expectancy = (win_rate * avg_win) - ((1 - win_rate) * abs(avg_loss)) if trade_count else 0.0

    hold_times = [t.hold_minutes for t in closed if t.hold_minutes is not None]
    avg_hold = mean(hold_times) if hold_times else 0.0

    return MetricsReport(
        trade_count=trade_count,
        win_count=win_count,
        loss_count=loss_count,
        open_count=len(trades) - trade_count,
        win_rate=win_rate,
        net_pnl=sum(pnls),
        gross_profit=gross_profit,
        gross_loss=gross_loss,
        profit_factor=profit_factor,
        avg_win=avg_win,
        avg_loss=avg_loss,
        expectancy=expectancy,
        max_drawdown=_drawdown(pnls),
        avg_hold_minutes=avg_hold,
        best_trade=max(pnls) if pnls else 0.0,
        worst_trade=min(pnls) if pnls else 0.0,
        by_symbol=_by_symbol(closed),
        by_hour=_by_hour(closed),
        by_tag=_by_tag(closed),
    )
