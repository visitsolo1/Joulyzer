# Project Description — Joulyzer

> **Submission:** Bitget AI Base Camp Hackathon S1 — Track 2 (Trading Infra)
> **Author:** Joulyzer Contributors
> **Repo:** https://github.com/visitsolo1/Joulyzer
> **Hackathon submission form:** https://forms.gle/CEGB6fRtuobD3bCj8

This document follows the **four-part structure** required by the
hackathon submission form. It is the canonical project description
that should be pasted into the form. The README expands each section
with code, diagrams, and verifiable artifacts.

---

## Part 1 — Problem & Motivation

The first generation of autonomous trading agents is being written
right now. Bitget Agent Hub exposes 58 trading APIs; Bitget Playbook
turns a plain-language strategy idea into a live strategy. The agents
are coming.

What's missing is the **post-trade analytics loop**. Today a strategy
either prints "submitted order: OK" and walks away, or asks the user
to paste a CSV into a Google Sheet and eyeball their PnL. No agent —
and no user — gets a deterministic answer to:

* "What is my actual edge?"
* "Where am I losing money?"
* "Which setup pays best, which hour kills me?"
* "Am I revenge-trading after losses?"

Every broker exports a slightly different CSV column set. Existing
analytics libraries drag in pandas / numpy / Jupyter (200MB+ install)
and have no agent-friendly function surface. **There is no tiny,
dependency-free, agent-callable tool that closes the journal → analytics
→ feedback loop.** Joulyzer fills that gap.

## Part 2 — Solution

Joulyzer is a **trade-journal → analytics → agent-tool** pipeline in
one Python package with **zero required dependencies**:

* **Standard-library CSV parser** with a wide column-alias table
  (`symbol` / `pair` / `market`; `pnl` / `profit` / `net_pnl`; etc.) —
  any broker's export "just works".
* **Deterministic metrics engine**: win rate, profit factor,
  expectancy, max drawdown, breakdowns by symbol / hour / tag.
* **Three output formats**: human-readable text, JSON string, raw dict.
* **Tool surface for agents**:
  * `joulyzer.analyze_journal(csv_path, format)` — single stable
    function the agent calls.
  * `joulyzer.TOOL_SCHEMA` — OpenAI / Anthropic / Qwen
    function-calling JSON schema.
  * `python -m joulyzer.agent --mcp` — a minimal Model Context
    Protocol (MCP) stdio server so Claude Code, Continue, or Bitget's
    `getagent` CLI can mount joulyzer as a tool.
* **Bitget-shaped paper-trade generator** —
  `joulyzer.generators.bitget_paper` produces a deterministic
  synthetic fill stream that mirrors Bitget's order-history API JSON,
  so agents can be developed and tested offline without credentials
  or capital, and so submission to Track 2 is backed by a
  **verifiable API call log + reproducible sample input/output**.

## Part 3 — Architecture & Tech Choices

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

**Tech**: Python 3.9+ stdlib only (no numpy / pandas / broker SDK);
`pytest` as a dev-only test dep. The MCP server is a 60-line stdlib
JSON-RPC loop. The paper-trade generator uses only `random` + `csv` +
`json` from stdlib.

**Why stdlib only?** Two reasons. (1) An agent running in a sandbox
can't depend on a 200MB scientific stack being present. (2) Every
dependency is a version-pinning liability for a project that lives
inside an agent's tool loop. The codebase is small enough that
hand-writing the parser is cheaper than wiring pandas.

**Determinism.** Every generator call takes a `seed=`. Every metric
is a pure function of the input list. Same input → same output, byte
for byte. This is what makes the `verifiable_usage_records/` artifacts
trustworthy: a judge can rerun the exact same command and get the
exact same report.

**Sandbox safety.** `analyze_journal` reads only the file the agent
names. It does not network, exec, or import agent-controlled code.
Errors return structured dicts (`{"status": "failed", "error": "..."}`)
so the calling model can branch on the result without `try/except`.

## Part 4 — Our Take on AI Trading

The next 12 months will be defined by *how well agents close the
feedback loop* — not by who can call the order endpoint. The
interesting questions are not "can the agent place a trade" (yes,
trivially — Bitget's APIs are well-documented). The interesting
questions are:

1. **Does the agent know when its edge has decayed?** — rolling
   win-rate, profit factor, Sharpe on its own fills.
2. **Can the agent explain to its user why a strategy is failing?**
   — per-symbol, per-hour, per-tag breakdowns.
3. **Can the agent compare two strategies head-to-head without
   humans?** — deterministic, machine-readable reports.

Joulyzer is the smallest thing that does all three. The hard work
(regime classification, MAE/MFE, expectation curves, multi-strategy
blending) is a straightforward extension on the same `MetricsReport`
shape. We chose to ship a tiny, correct, agent-grade v0.2 today
rather than a pandas-bound monster that breaks every time a column
moves.

If joulyzer sees adoption in the Base Camp community, the next step
is an optional `joulyzer-live` companion that pipes Bitget Agent
Hub's fill stream directly into joulyzer's parser — same code path,
live data, no schema change for the agent.

The bet: **AI Trading will be won by infra that lets agents
self-critique cheaply**, not by infra that lets them place orders
faster. Joulyzer is one piece of that.

---

## Submission materials checklist (Track 2)

| Material                                            | Where it lives in this repo                                                      |
|-----------------------------------------------------|-----------------------------------------------------------------------------------|
| **Project description** (this file)                 | `PROJECT_DESCRIPTION.md`                                                         |
| **Public GitHub repo**                              | https://github.com/visitsolo1/Joulyzer                                            |
| **README** with install / integration / usage       | `README.md`                                                                       |
| **INSTALL** — 3-command zero-to-running guide       | `INSTALL.md`                                                                      |
| **Verifiable usage record #1 — test logs**         | `verifiable_usage_records/pytest_run.log` (16/16 passed)                          |
| **Verifiable usage record #2 — sample I/O**        | `verifiable_usage_records/cli_text_run.txt` + `integration_run/agent_tool_call_result.json` |
| **Verifiable usage record #3 — simulated API log** | `verifiable_usage_records/integration_run/bitget_api_call_log.jsonl` (240 simulated Bitget calls with timestamps) |
| **Verifiable usage record #4 — LIVE API call log** | `verifiable_usage_records/live_mcp_session.log.jsonl` (real JSON-RPC traffic between a client subprocess and the joulyzer MCP server) |
| **Verifiable usage record #5 — integration example** | `examples/agent_integration.py` + `scripts/mcp_client_demo.py` (another developer can run them via `bash scripts/verify_submission.sh`) |
| **Demo video** (optional)                           | _Not submitted — repo is self-runnable, judges can `python -m pytest tests/ -v` immediately_ |
| **Deployment link** (optional)                      | _Not submitted — joulyzer is a library, not a hosted service_                     |

Reproducing the verifiable artifacts (no API keys, no network):

```bash
git clone https://github.com/visitsolo1/Joulyzer.git
cd Joulyzer
pip install -e ".[test]"
bash scripts/verify_submission.sh     # regenerates every artifact
```

`verify_submission.sh` runs the test suite, regenerates the simulated
Bitget API log, regenerates the live MCP usage log against a real MCP
server subprocess, and re-emits the tool schema + MCP manifest. Every
artifact is byte-stable on rerun.
