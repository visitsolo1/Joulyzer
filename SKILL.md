---
name: joulyzer
description: Analyze a trader's exported trade journal (CSV) and produce structured performance analytics — win rate, profit factor, expectancy, drawdown, MAE/MFE, time-of-day edge, symbol and tag breakdowns. Use when the user provides a trade journal file or asks for trade performance review, edge detection, journaling insights, or post-trade analytics.
---

# Joulyzer — AI Trade Journal Analyzer

Joulyzer ingests a trader's exported trade journal and returns structured
analytics an AI agent can summarize, compare, or feed into further reasoning.

## What it computes

- **Headline metrics**: trade count, win rate, net PnL, gross profit/loss,
  profit factor, average win / average loss, expectancy per trade.
- **Risk**: max drawdown, best / worst trade, average hold time.
- **Breakdowns**: by symbol, by hour-of-entry, by tag (e.g. `breakout`, `fomo`,
  `scalp`, `revenge` — anything the trader labels in the journal).
- **Format**: text report, JSON dict, or Python objects.

## When to use this skill

- User shares a CSV / Excel trade export and wants a review.
- User asks "what's my edge", "where am I losing money", "which setup pays best",
  "am I trading too much at hour X".
- User wants to compare two journals or two strategies (tag-based).
- An agent needs a deterministic analytics function instead of guessing.

## When NOT to use it

- The user has no journal yet (recommend they start one — CSV template ships in `examples/`).
- The data is not trade data (PnL column missing, instrument column missing).
- Real-time trade execution is requested — Joulyzer is post-trade analytics only.

## Function surface

```python
from joulyzer import load_journal, compute_metrics, render_text_report, to_json, to_dict

trades = load_journal("examples/sample_journal.csv")   # list[Trade]
report = compute_metrics(trades)                       # MetricsReport
print(render_text_report(report))                      # human-readable
print(to_json(report))                                 # machine-readable
```

## CLI

```bash
python -m joulyzer examples/sample_journal.csv          # text report
python -m joulyzer examples/sample_journal.csv --json   # JSON
```

## Expected CSV columns (aliases accepted)

| Canonical      | Also accepted                                     |
|----------------|---------------------------------------------------|
| `symbol`       | pair, market, instrument                          |
| `side`         | direction, action (long/short, buy/sell)          |
| `entry_time`   | open_time, opened_at, time, timestamp             |
| `exit_time`    | close_time, closed_at                             |
| `entry_price`  | open_price, price_in                              |
| `exit_price`   | close_price, price_out                            |
| `size`         | qty, quantity, amount, volume                     |
| `pnl`          | p&l, profit, net_pnl, realized_pnl                |
| `fees`         | fee, commission                                   |
| `notes`        | note, comment, reason                             |
| `tags`         | tag, category (comma- or pipe-separated)          |

Empty `exit_time` is treated as an **open position** and excluded from
win-rate / PnL metrics but counted in `open_count`.

## Testing the skill

```bash
# 1. Install (editable, no extra deps)
pip install -e .

# 2. Run unit tests (5 tests, no external services)
python -m pytest tests/ -v

# 3. Run the CLI against the bundled sample journal
python -m joulyzer examples/sample_journal.csv

# 4. Emit JSON for downstream consumption
python -m joulyzer examples/sample_journal.csv --json > report.json
```

Expected: `5 passed` from pytest, and a `================ Joulyzer Report ================`
text block ending with a `--- By tag ---` section.

## Dependencies

- Python 3.9+
- `pytest` (test only)

That's it — no pandas, no numpy. Parsing is stdlib `csv`; metrics use
`statistics.mean`. Keeping the surface tiny is the point: an agent can
call it from a sandbox without worrying about supply-chain bloat.
