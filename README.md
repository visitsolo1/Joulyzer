# Joulyzer — AI Trade Journal Analyzer & Agent Tool

> A deterministic, agent-grade analytics layer for crypto trade journals.
> Drop-in tool for AI agents (Claude Code, Qwen, Cursor, LangChain ReAct, MCP clients).
> Built for the **Bitget AI Base Camp Hackathon S1 — Track 2 (Trading Infra)**.

[![tests](https://img.shields.io/badge/tests-16%20passed-brightgreen)]()
[![python](https://img.shields.io/badge/python-3.9%2B-blue)]()
[![license](https://img.shields.io/badge/license-MIT-green)]()
[![hackathon](https://img.shields.io/badge/Bitget-AI%20Base%20Camp%20S1-orange)]()

Joulyzer ingests a trader's exported trade journal (CSV from Bitget, Binance,
Bybit, or any broker whose columns joulyzer can alias — see [`SKILL.md`](./SKILL.md))
and returns **structured performance analytics** an AI agent can summarize,
compare, or feed into further reasoning:

* **Headline metrics**: trade count, win rate, net PnL, gross profit / loss,
  profit factor, average win / average loss, expectancy per trade.
* **Risk**: max drawdown, best / worst trade, average hold time.
* **Breakdowns**: by symbol, by hour-of-entry, by tag (`breakout`, `fomo`,
  `scalp`, `revenge` — whatever the trader labels).

Joulyzer is **intentionally tiny**: parser + metrics + renderer + a tool
adapter. No pandas, no numpy, no broker SDK. That's the point — an agent
can call it from a sandbox without worrying about supply-chain bloat.

---

## Table of contents

1. [Why (the problem joulyzer solves)](#1-why)
2. [Solution (what joulyzer delivers)](#2-solution)
3. [Architecture (how it's put together)](#3-architecture)
4. [AI-Trading take (where this is going)](#4-ai-trading-take)
5. [Quick start](#quick-start)
6. [Agent integration](#agent-integration)
7. [Project layout](#project-layout)
8. [Testing](#testing)
9. [License](#license)

---

## 1. Why

AI Trading Agents are about to ship at scale. Bitget Agent Hub exposes
**58 trading APIs**; Bitget Playbook can take a strategy idea in plain
language and ship it as a backtest + live strategy. The agents are
coming.

What's missing is the **post-trade analytics loop**. Right now a
strategy either prints "submitted order: OK" and walks away, or asks
the user to paste a CSV into a Google Sheet and eyeball their PnL.
Nobody — neither the agent, nor the user — gets a deterministic
answer to:

> *"What is my actual edge? Where am I losing money? Which setup pays
> best, which hour kills me, am I revenge-trading after losses?"*

Every broker exports a slightly different CSV column set. No single
tool does "load journal → return structured analytics → give that
back to the agent in a format it can reason over" without dragging
in pandas, numpy, jupyter, and a 200MB install.

That gap is what joulyzer fills.

## 2. Solution

Joulyzer is a **trade-journal → analytics → agent-tool** pipeline in
one Python package with no required dependencies:

* **Standard library CSV parser** with a wide column-alias table
  (`symbol` / `pair` / `market`; `pnl` / `profit` / `net_pnl`; etc.)
  so any broker's export "just works".
* **Deterministic metrics engine**: win rate, profit factor,
  expectancy, max drawdown, breakdowns by symbol / hour / tag.
* **Three output formats**: human-readable text, JSON string, raw dict.
* **Tool surface for agents**:
  * :func:`joulyzer.analyze_journal` — the function an agent calls.
  * :data:`joulyzer.TOOL_SCHEMA` — OpenAI / Anthropic / Qwen
    function-calling JSON schema.
  * :func:`joulyzer.mcp_manifest` + ``python -m joulyzer.agent --mcp``
    — a minimal MCP (Model Context Protocol) stdio server so any
    MCP-aware client (Claude Code, Continue, Bitget getagent) can mount
    joulyzer as a tool.
* **Bitget-shaped paper-trade generator** —
  :mod:`joulyzer.generators.bitget_paper` produces a deterministic
  synthetic fill stream that mirrors Bitget's order-history API JSON,
  so agents can be developed and tested offline without credentials
  or capital.

Everything an agent needs to go from "I just exported my trades" to
"here's your win rate, profit factor, worst setup, and what to fix
next" lives in one Python file.

## 3. Architecture

```
                       ┌────────────────────────────────────────┐
                       │  AI Agent (Claude Code / Qwen / MCP)   │
                       └───────────────┬────────────────────────┘
                                       │ tool_call: analyze_journal
                                       ▼
   ┌─────────────────┐         ┌─────────────────────┐
   │ Bitget / Binance│  CSV    │  joulyzer.parser    │
   │ / Bybit export  │────────▶│  (stdlib csv +      │
   └─────────────────┘         │   column aliases)   │
                               └──────────┬──────────┘
                                          │ list[Trade]
                                          ▼
                               ┌─────────────────────┐
                               │ joulyzer.metrics    │
                               │ win rate, PF, DD,   │
                               │ by sym/hour/tag     │
                               └──────────┬──────────┘
                                          │ MetricsReport
                                          ▼
                               ┌─────────────────────┐
                               │ joulyzer.report     │
                               │ text / JSON / dict  │
                               └──────────┬──────────┘
                                          │
                                          ▼
                                agent continues reasoning
```

### Module map

| Module                                | Purpose                                                            |
|---------------------------------------|--------------------------------------------------------------------|
| `joulyzer.parser`                     | CSV → `list[Trade]`, alias-aware                                    |
| `joulyzer.metrics`                    | `list[Trade]` → `MetricsReport` (deterministic)                    |
| `joulyzer.report`                     | `MetricsReport` → text / JSON / dict                               |
| `joulyzer.cli`                        | `python -m joulyzer <journal.csv>` entry point                     |
| `joulyzer.agent`                      | Tool surface: `analyze_journal`, `tool_schema`, MCP stdio server   |
| `joulyzer.generators.bitget_paper`    | Deterministic Bitget-shaped fill generator + API-call-log emitter   |

### Design choices

- **Stdlib only** for the core parser / metrics / report — no supply-chain
  risk, no version churn, ships in any sandbox.
- **One stable tool signature** (`analyze_journal(csv_path, format)`) so
  the agent contract doesn't move when internals change.
- **Errors return structured dicts**, not exceptions — the calling agent
  can branch on `result["status"]` without `try/except`.
- **Deterministic generator** (`seed=` arg) so every integration test
  and every verifiable artifact is byte-identical on rerun.
- **MCP server** is a 60-line stdlib JSON-RPC loop, no extra deps —
  anyone running an MCP-aware coding agent can mount joulyzer with
  `python -m joulyzer.agent --mcp`.

## 4. AI-Trading take

The next 12 months are going to be defined by *how well agents close the
loop* — not by who can call the order endpoint. The interesting
questions aren't "can the agent place a trade" (yes, trivially, the Bitget
APIs are well-documented). The interesting questions are:

1. **Does the agent know when its edge has decayed?** — running rolling
   win-rate, profit factor, and Sharpe on its own fills.
2. **Can the agent explain to its user why a strategy is failing?** —
   per-symbol, per-hour, per-tag breakdowns.
3. **Can the agent compare two strategies head-to-head without
   humans?** — deterministic, machine-readable reports.

Joulyzer is the smallest thing that does all three. The hard work
above (regime classification, MAE/MFE, expectation curves) is a
straightforward extension on the same `MetricsReport` shape. We'd
rather ship a tiny, correct, agent-grade v0.2 today than a
pandas-bound monster that breaks every time a column moves.

If joulyzer sees adoption in the Base Camp community, the next step
is an optional `joulyzer-live` companion that pipes Bitget Agent Hub's
fill stream directly into joulyzer's parser — same code path, live
data, no schema change for the agent.

---

## Quick start

> **Install in 3 commands.** Full step-by-step (incl. PEP 668 / Termux / air-gapped
> variants) lives in [`INSTALL.md`](./INSTALL.md).

```bash
git clone https://github.com/visitsolo1/Joulyzer.git
cd Joulyzer
pip install -e ".[test]"
```

Then:

```bash
# 1. Run on the bundled sample journal
python -m joulyzer examples/sample_journal.csv

# 2. JSON output (pipe into another tool or an LLM)
python -m joulyzer examples/sample_journal.csv --json > report.json

# 3. Run the full test suite (16 tests, no network, no external services)
python -m pytest tests/ -v
```

Expected:

* A text report starting with `================ Joulyzer Report ================`
  and containing `Net PnL`, `By symbol`, `By hour (entry)`, `By tag` sections.
* JSON with keys like `net_pnl`, `win_rate`, `profit_factor`, `by_symbol`.
* `16 passed` from pytest.

## Programmatic use

```python
from joulyzer import load_journal, compute_metrics, render_text_report, to_json

trades = load_journal("examples/sample_journal.csv")
report = compute_metrics(trades)

print(render_text_report(report))   # human-readable
print(to_json(report))              # machine-readable
```

## Agent integration

Joulyzer's value to an AI agent is that it can be called as a tool
with one stable signature. Pick whichever surface matches your stack:

### A. Direct function call (simplest)

```python
from joulyzer import analyze_journal
result = analyze_journal("path/to/journal.csv", format="json")
# result is a JSON string you can hand back to the model.
```

### B. OpenAI / Anthropic / Qwen function-calling

```python
from joulyzer import TOOL_SCHEMA

# Register TOOL_SCHEMA with your model. The model will produce:
#   {"name": "analyze_journal",
#    "arguments": {"csv_path": "journal.csv", "format": "json"}}
# Dispatch that into joulyzer.analyze_journal(**arguments).
```

### C. MCP server (Claude Code, Continue, Bitget getagent)

```bash
python -m joulyzer.agent --mcp
```

Point any MCP-aware client at the spawned stdio process — they will
discover `analyze_journal` and route calls to joulyzer.

### D. End-to-end working example

```bash
python examples/agent_integration.py
```

This runs the full loop (generate fills → export journal → dispatch
a fake model tool call → persist the result) and is the canonical
"another developer can integrate it" reference. The artifacts it
writes live under `verifiable_usage_records/integration_run/`.

### D. Live usage record (multi-caller, multi-journal)

`scripts/live_usage_harness.py` drives joulyzer as third-party
infrastructure from three independent angles — a CLI subprocess,
an in-process Python function call, and a JSON-RPC MCP subprocess
— across three real input journals and all three output formats,
plus three deliberate error paths. Every call is captured with a
UTC timestamp and wall-clock latency into
[`verifiable_usage_records/live_usage.jsonl`](./verifiable_usage_records/live_usage.jsonl).
A human-readable summary lives at
[`live_usage_summary.md`](./verifiable_usage_records/live_usage_summary.md)
and a machine-readable one at
[`live_usage_summary.json`](./verifiable_usage_records/live_usage_summary.json).

```bash
python scripts/live_usage_harness.py     # ~30 calls, <1s wall-clock
# or include in the one-shot:
bash scripts/verify_submission.sh
```

A second, narrower live trace focused on MCP wire-format detail
(`tools/list` discovery + `tools/call` envelopes) lives at
[`verifiable_usage_records/live_mcp_session.log.jsonl`](./verifiable_usage_records/live_mcp_session.log.jsonl)
and is regenerated by `scripts/mcp_client_demo.py`.

## Project layout

```
joulyzer/
  __init__.py              # public API (lazy agent import)
  __main__.py              # enables `python -m joulyzer`
  cli.py                   # argument parsing
  parser.py                # CSV → list[Trade]
  metrics.py               # list[Trade] → MetricsReport
  report.py                # MetricsReport → text / JSON
  agent.py                 # tool surface + MCP stdio server
  generators/
    __init__.py
    bitget_paper.py        # deterministic Bitget-shaped fill generator
tests/
  test_joulyzer.py                 # core parser/metrics tests (5)
  test_agent_and_generator.py      # agent + generator tests (11)
examples/
  sample_journal.csv               # 8-trade sample for CLI demo
  agent_integration.py             # end-to-end agent tool-call example
scripts/
  verify_submission.sh             # regenerates every artifact end-to-end
  mcp_client_demo.py               # live MCP client → server demo (logs wire traffic)
  live_usage_harness.py            # multi-caller live usage harness (CLI + function + MCP)
verifiable_usage_records/
  pytest_run.log                   # full test log
  cli_text_run.txt                  # CLI text + JSON output
  integration_run/
    bitget_api_call_log.jsonl       # 240 simulated Bitget API calls
    agent_session_journal.csv       # resulting joulyzer journal
    agent_tool_call_result.json     # what the agent "received"
  live_usage.jsonl                 # live usage record (30 calls, 3 callers, 3 journals, 3 formats + errors)
  live_usage_summary.json           # per-caller aggregates (machine-readable)
  live_usage_summary.md             # per-caller aggregates (human-readable table)
  live_usage_inputs/                # real CSVs the live harness consumed
  live_mcp_session.log.jsonl        # narrower MCP wire-traffic log
  live_session/
    live_journal.csv                # journal used by the live MCP session
  tool_schema.json                  # JSON-Schema tool definition
  mcp_manifest.json                 # MCP server manifest
.github/workflows/tests.yml        # (CI config in docs/github-actions-tests.yml; user enables via GitHub UI since PAT lacks workflow scope)
docs/github-actions-tests.yml       # CI workflow config (copy to .github/workflows/ to enable)
LICENSE                             # MIT
README.md                           # you are here
INSTALL.md                          # 3-command install + every install variant
SKILL.md                            # agent-facing description
PROJECT_DESCRIPTION.md              # 4-part submission blurb
```

## Testing

```bash
# Full suite (16 tests, stdlib + pytest only)
python -m pytest tests/ -v

# Just the agent + generator tests
python -m pytest tests/test_agent_and_generator.py -v
```

Expected: `16 passed`.

## CSV format

Joulyzer accepts a wide range of column names. See [`SKILL.md`](./SKILL.md)
for the full alias table. A working minimum:

```
symbol,side,entry_time,exit_time,entry_price,exit_price,size,pnl,fees,tags,notes
BTCUSDT,long,2025-01-02 09:15:00,2025-01-02 10:42:00,42000,42550,0.5,275.00,4.10,breakout,clean breakout above range high
```

Empty `exit_time` is treated as an open position and excluded from
win-rate / PnL metrics, but counted in `open_count`.

## License

MIT — see [`LICENSE`](./LICENSE).
