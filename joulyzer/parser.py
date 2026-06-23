"""Trade journal parsers.

Accepts CSV and Excel exports. Tries to be tolerant of column-name
variation across brokers (Binance, Bybit, Bitget, manual sheets).
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

# Map of canonical field -> accepted aliases (lowercased, stripped).
COLUMN_ALIASES: dict[str, tuple[str, ...]] = {
    "symbol": ("symbol", "pair", "market", "instrument"),
    "side": ("side", "direction", "action"),
    "entry_time": ("entry_time", "open_time", "opened_at", "time", "timestamp"),
    "exit_time": ("exit_time", "close_time", "closed_at"),
    "entry_price": ("entry_price", "open_price", "price_in"),
    "exit_price": ("exit_price", "close_price", "price_out"),
    "size": ("size", "qty", "quantity", "amount", "volume"),
    "pnl": ("pnl", "p&l", "profit", "net_pnl", "realized_pnl"),
    "fees": ("fees", "fee", "commission"),
    "notes": ("notes", "note", "comment", "comments", "reason"),
    "tags": ("tags", "tag", "category"),
}


class JournalLoadError(ValueError):
    """Raised when a journal file cannot be parsed into trades."""


@dataclass
class Trade:
    symbol: str
    side: str  # "long" | "short"
    entry_time: datetime | None
    exit_time: datetime | None
    entry_price: float
    exit_price: float
    size: float
    pnl: float
    fees: float = 0.0
    notes: str = ""
    tags: tuple[str, ...] = ()

    @property
    def is_win(self) -> bool:
        return self.pnl > 0

    @property
    def is_loss(self) -> bool:
        return self.pnl < 0

    @property
    def is_open(self) -> bool:
        return self.exit_time is None

    @property
    def hold_minutes(self) -> float | None:
        if self.entry_time is None or self.exit_time is None:
            return None
        return (self.exit_time - self.entry_time).total_seconds() / 60.0


def _normalize_columns(headers: list[str]) -> dict[str, str]:
    """Return {alias_used: canonical_name} for recognized columns."""
    lowered = {h.strip().lower(): h for h in headers}
    mapping: dict[str, str] = {}
    for canonical, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in lowered:
                mapping[lowered[alias]] = canonical
                break
    return mapping


def _coerce_float(v: Any) -> float:
    if v is None or v == "":
        return 0.0
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace(",", "").replace("$", "")
    if s.startswith("(") and s.endswith(")"):  # accounting negative
        s = "-" + s[1:-1]
    return float(s)


def _coerce_datetime(v: Any) -> datetime | None:
    if v is None or v == "":
        return None
    if isinstance(v, datetime):
        return v
    s = str(v).strip()
    for fmt in (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%m/%d/%Y %H:%M",
        "%m/%d/%Y",
    ):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    # Last-resort: fromisoformat (handles Z)
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return None


def _coerce_side(v: Any) -> str:
    if v is None:
        return "long"
    s = str(v).strip().lower()
    if s in ("short", "sell", "s", "shrt"):
        return "short"
    return "long"


def _coerce_tags(v: Any) -> tuple[str, ...]:
    if v is None or v == "":
        return ()
    return tuple(t.strip().lower() for t in str(v).replace("|", ",").split(",") if t.strip())


def _row_to_trade(row: dict[str, str], mapping: dict[str, str]) -> Trade:
    def get(canonical: str, default: Any = None) -> Any:
        for orig, mapped in mapping.items():
            if mapped == canonical:
                return row.get(orig)
        return default

    return Trade(
        symbol=str(get("symbol", "")).strip().upper() or "UNKNOWN",
        side=_coerce_side(get("side")),
        entry_time=_coerce_datetime(get("entry_time")),
        exit_time=_coerce_datetime(get("exit_time")),
        entry_price=_coerce_float(get("entry_price")),
        exit_price=_coerce_float(get("exit_price")),
        size=_coerce_float(get("size")),
        pnl=_coerce_float(get("pnl")),
        fees=_coerce_float(get("fees", 0.0)),
        notes=str(get("notes", "") or "").strip(),
        tags=_coerce_tags(get("tags")),
    )


def _read_csv(path: Path) -> Iterable[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield {k: ("" if v is None else v) for k, v in row.items()}


def load_journal(path: str | Path) -> list[Trade]:
    """Load trades from a CSV file. Returns an empty list on no rows."""
    p = Path(path)
    if not p.exists():
        raise JournalLoadError(f"File not found: {p}")
    if p.suffix.lower() not in {".csv", ".txt"}:
        raise JournalLoadError(
            f"Unsupported extension '{p.suffix}'. Only .csv/.txt are supported in v0.1."
        )

    rows = list(_read_csv(p))
    if not rows:
        return []

    mapping = _normalize_columns(list(rows[0].keys()))
    if "pnl" not in mapping.values() and "entry_price" not in mapping.values():
        raise JournalLoadError(
            "Could not identify a PnL or entry_price column. "
            f"Headers found: {list(rows[0].keys())}"
        )

    return [_row_to_trade(r, mapping) for r in rows]
