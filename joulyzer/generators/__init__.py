"""Generators: synthetic data sources joulyzer can ingest.

The :mod:`joulyzer.generators.bitget_paper` module produces trade ledgers that
match the JSON shape of Bitget's order-history endpoints (``/api/v2/mix/order/*``
and ``/api/v2/spot/trade/fills``), so a paper-trading session or backtest can be
exported straight into joulyzer's ``load_journal`` and analyzed end-to-end.

This module exists so that:

* Anyone can generate a deterministic, reproducible sample trade ledger
  without needing live API credentials or capital.
* An AI Agent that integrates with Bitget Agent Hub or Bitget Playbook can
  pipe its own fills through the same generator for offline backtesting.
* Submission to Bitget AI Base Camp Hackathon Track 2 (Trading Infra) is
  backed by a verifiable usage record: API call log + reproducible
  sample input/output. See ``verifiable_usage_records/`` in this repo.
"""

from .bitget_paper import (
    BitgetFill,
    generate_bitget_fills,
    fills_to_api_log,
    fills_to_csv,
    fills_to_journal_csv,
    DEFAULT_SYMBOLS,
)

__all__ = [
    "BitgetFill",
    "generate_bitget_fills",
    "fills_to_api_log",
    "fills_to_csv",
    "fills_to_journal_csv",
    "DEFAULT_SYMBOLS",
]
