# Live Usage Record — joulyzer

_Generated 2026-06-24 19:38:47 UTC_

This is the canonical verifiable usage record for the Track 2
submission. Each row in the table below is one real call into
joulyzer as third-party infrastructure, executed by the harness
in `scripts/live_usage_harness.py`.

## Summary

- **Total calls:** 30
- **OK:** 27
- **Errors:** 3 (intentional error-path coverage)
- **First call:** 2026-06-24T19:38:46.650397Z
- **Last call:** 2026-06-24T19:38:47.565091Z
- **Total wall-clock:** 909.5 ms
- **Input journals exercised:** 5
- **Output formats exercised:** dict, json, text

## By caller

| Caller | Calls | OK | Errors | Mean ms | p50 ms | Min ms | Max ms |
|--------|------:|---:|-------:|--------:|-------:|-------:|-------:|
| `cli` | 10 | 9 | 1 | 85.83 | 85.34 | 70.76 | 102.53 |
| `function` | 11 | 9 | 2 | 2.17 | 1.93 | 0.05 | 4.77 |
| `mcp` | 9 | 9 | 0 | 3.04 | 2.39 | 1.42 | 4.85 |

## Per-call detail

| # | ts | caller | operation | input_format | latency_ms | status | bytes |
|---:|---|---|---|---|---:|---|---:|
| 1 | 2026-06-24T19:38:46.650397Z | `cli` | `cli:text` | `text` | 102.53 | ok | 1073 |
| 2 | 2026-06-24T19:38:46.754101Z | `function` | `analyze_journal:text` | `text` | 2.25 | ok | 1072 |
| 3 | 2026-06-24T19:38:46.756501Z | `mcp` | `tools/call:analyze_journal:text` | `text` | 4.85 | ok | 1072 |
| 4 | 2026-06-24T19:38:46.761477Z | `cli` | `cli:--json` | `json` | 88.22 | ok | 1585 |
| 5 | 2026-06-24T19:38:46.849843Z | `function` | `analyze_journal:json` | `json` | 1.22 | ok | 1584 |
| 6 | 2026-06-24T19:38:46.851165Z | `mcp` | `tools/call:analyze_journal:json` | `json` | 1.52 | ok | 1584 |
| 7 | 2026-06-24T19:38:46.852802Z | `cli` | `cli:text` | `dict` | 99.07 | ok | 1073 |
| 8 | 2026-06-24T19:38:46.952043Z | `function` | `analyze_journal:dict` | `dict` | 1.05 | ok | 1152 |
| 9 | 2026-06-24T19:38:46.953314Z | `mcp` | `tools/call:analyze_journal:dict` | `dict` | 1.42 | ok | 1584 |
| 10 | 2026-06-24T19:38:46.954834Z | `cli` | `cli:text` | `text` | 82.08 | ok | 1643 |
| 11 | 2026-06-24T19:38:47.037071Z | `function` | `analyze_journal:text` | `text` | 1.76 | ok | 1642 |
| 12 | 2026-06-24T19:38:47.038930Z | `mcp` | `tools/call:analyze_journal:text` | `text` | 2.16 | ok | 1642 |
| 13 | 2026-06-24T19:38:47.041192Z | `cli` | `cli:--json` | `json` | 77.94 | ok | 2882 |
| 14 | 2026-06-24T19:38:47.119276Z | `function` | `analyze_journal:json` | `json` | 2.13 | ok | 2881 |
| 15 | 2026-06-24T19:38:47.121515Z | `mcp` | `tools/call:analyze_journal:json` | `json` | 2.39 | ok | 2881 |
| 16 | 2026-06-24T19:38:47.124008Z | `cli` | `cli:text` | `dict` | 79.78 | ok | 1643 |
| 17 | 2026-06-24T19:38:47.203928Z | `function` | `analyze_journal:dict` | `dict` | 1.93 | ok | 2049 |
| 18 | 2026-06-24T19:38:47.206093Z | `mcp` | `tools/call:analyze_journal:dict` | `dict` | 2.17 | ok | 2881 |
| 19 | 2026-06-24T19:38:47.208402Z | `cli` | `cli:text` | `text` | 86.50 | ok | 1802 |
| 20 | 2026-06-24T19:38:47.295069Z | `function` | `analyze_journal:text` | `text` | 4.77 | ok | 1801 |
| 21 | 2026-06-24T19:38:47.299950Z | `mcp` | `tools/call:analyze_journal:text` | `text` | 4.21 | ok | 1801 |
| 22 | 2026-06-24T19:38:47.304278Z | `cli` | `cli:--json` | `json` | 87.19 | ok | 3263 |
| 23 | 2026-06-24T19:38:47.391670Z | `function` | `analyze_journal:json` | `json` | 4.11 | ok | 3262 |
| 24 | 2026-06-24T19:38:47.395941Z | `mcp` | `tools/call:analyze_journal:json` | `json` | 4.50 | ok | 3262 |
| 25 | 2026-06-24T19:38:47.400542Z | `cli` | `cli:text` | `dict` | 84.18 | ok | 1802 |
| 26 | 2026-06-24T19:38:47.484867Z | `function` | `analyze_journal:dict` | `dict` | 3.97 | ok | 2364 |
| 27 | 2026-06-24T19:38:47.489100Z | `mcp` | `tools/call:analyze_journal:dict` | `dict` | 4.18 | ok | 3262 |
| 28 | 2026-06-24T19:38:47.493445Z | `function` | `analyze_journal:text` | `text` | 0.64 | error | 0 |
| 29 | 2026-06-24T19:38:47.494179Z | `cli` | `cli:text` | `text` | 70.76 | error | 0 |
| 30 | 2026-06-24T19:38:47.565091Z | `function` | `analyze_journal:json` | `json` | 0.05 | error | 0 |

## Reproduce

```bash
pip install -e .[test]
python scripts/live_usage_harness.py
```

Re-running overwrites this file and the sibling
`live_usage.jsonl` (one JSON record per call) and
`live_usage_summary.json` (per-caller aggregates).
