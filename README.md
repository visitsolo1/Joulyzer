# Joulyzer

> An AI trade journal analyzer. Point it at a CSV of your trades, get back
> win rate, profit factor, expectancy, drawdown, and breakdowns by symbol,
> time-of-day, and tag.

Joulyzer is intentionally tiny: a parser, a metrics engine, and a renderer —
no pandas, no numpy, no broker SDK. That makes it cheap to run inside an
agent loop and easy to embed in any Python toolchain.

## Quick start

```bash
# 1. install
pip install -e .

# 2. analyze the bundled sample journal
python -m joulyzer examples/sample_journal.csv
```

You should see a report that starts with
`================ Joulyzer Report ================`.

## Programmatic use

```python
from joulyzer import load_journal, compute_metrics, render_text_report, to_json

trades = load_journal("examples/sample_journal.csv")
report = compute_metrics(trades)

print(render_text_report(report))   # human-readable
print(to_json(report))              # machine-readable
```

## How to test

The project ships with a sample journal and a small test suite.

```bash
# Run the test suite (5 tests, no network, no external services)
python -m pytest tests/ -v

# Try the CLI on the sample data
python -m joulyzer examples/sample_journal.csv

# Get a JSON report (handy for piping into other tools or an LLM)
python -m joulyzer examples/sample_journal.csv --json > report.json
```

Expected:

- `5 passed` from pytest.
- A text report that lists headline metrics, then `--- By symbol ---`,
  `--- By hour (entry) ---`, and `--- By tag ---` sections.
- A JSON object on stdout with keys like `net_pnl`, `win_rate`, `profit_factor`,
  `by_symbol`, `by_hour`, `by_tag`.

## CSV format

Joulyzer accepts a wide range of column names. See [`SKILL.md`](./SKILL.md)
for the full alias table. A working minimum:

```
symbol,side,entry_time,exit_time,entry_price,exit_price,size,pnl,fees,tags,notes
BTCUSDT,long,2025-01-02 09:15:00,2025-01-02 10:42:00,42000,42550,0.5,275.00,4.10,breakout,clean breakout above range high
```

Empty `exit_time` is treated as an open position and excluded from
win-rate / PnL metrics, but counted in `open_count`.

## Project layout

```
joulyzer/
  __init__.py        # public API
  __main__.py        # enables `python -m joulyzer`
  cli.py             # argument parsing
  parser.py          # CSV → list[Trade]
  metrics.py         # list[Trade] → MetricsReport
  report.py          # MetricsReport → text / JSON
tests/
  test_joulyzer.py   # 5 unit tests
examples/
  sample_journal.csv # 8 trades, mix of wins/losses/open
SKILL.md             # agent-facing description of the tool
README.md            # you are here
```

## License

MIT — see `LICENSE`.
