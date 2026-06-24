# Joulyzer — Live Usage Record

- **Session ID**: `5505302ea0df`
- **Started**: 2026-06-24T19:50:31.823589+00:00
- **Ended**: 2026-06-24T19:50:33.605024+00:00
- **Duration**: 1.781 seconds
- **Total recorded events**: 33

## Summary

- CLI subprocess calls (`python -m joulyzer <journal> [--json]`): **10** (ok 9, errors 1, mean 84.65 ms, p50 74.65 ms)
- In-process Python function calls (`joulyzer.analyze_journal`): **11** (ok 9, errors 2, mean 2.18 ms, p50 1.96 ms)
- JSON-RPC MCP subprocess calls (`python -m joulyzer.agent --mcp`): **9** (ok 9, errors 0, mean 3.60 ms, p50 2.34 ms)
- Live Bitget public API calls (`api.bitget.com`): **3** (ok 3, errors 0, mean 285.21 ms, p50 259.27 ms)

## Timeline

### 1. [2026-06-24T19:50:31.829600+00:00] CLI: analyze_journal text

**Request**

```json
{
  "method": "subprocess.run",
  "cmd": [
    "/usr/bin/python",
    "-m",
    "joulyzer",
    "/run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/joulyzer-inspect/examples/sample_journal.csv"
  ],
  "cwd": ".",
  "csv_path": "examples/sample_journal.csv",
  "format": "text"
}
```

**Response**

```json
{
  "status": "ok",
  "returncode": 0,
  "body_kind": "text",
  "body": "================ Joulyzer Report ================\nTrades (closed): 7   Wins: 5   Losses: 2   Open: 1\nWin rate:        71.4%\nNet PnL:         279.00\nGross profit:    419.00   Gross loss: 140.00\nProfit factor:   2.99\nAvg win:         83.80   Avg loss: -70.00\nExpectancy:      39.86 per trade\nMax drawdown:    100.00\nAvg hold (min):  77.4\nBest trade:      275.00   Worst: -100.00\n\n--- By symbol ---\n  BT... <673 more chars>"
}
```

### 2. [2026-06-24T19:50:31.994630+00:00] function: analyze_journal text

**Request**

```json
{
  "module": "joulyzer",
  "fn": "analyze_journal",
  "args": {
    "csv_path": "examples/sample_journal.csv",
    "format": "text"
  }
}
```

**Response**

```json
{
  "status": "ok",
  "body_kind": "text",
  "body": "================ Joulyzer Report ================\nTrades (closed): 7   Wins: 5   Losses: 2   Open: 1\nWin rate:        71.4%\nNet PnL:         279.00\nGross profit:    419.00   Gross loss: 140.00\nProfit factor:   2.99\nAvg win:         83.80   Avg loss: -70.00\nExpectancy:      39.86 per trade\nMax drawdown:    100.00\nAvg hold (min):  77.4\nBest trade:      275.00   Worst: -100.00\n\n--- By symbol ---\n  BT... <672 more chars>"
}
```

### 3. [2026-06-24T19:50:31.996851+00:00] MCP: tools/call analyze_journal text

**Request**

```json
{
  "method": "stdio JSON-RPC",
  "server": "python -m joulyzer.agent --mcp",
  "payload": {
    "jsonrpc": "2.0",
    "id": 1000,
    "method": "tools/call",
    "params": {
      "name": "analyze_journal",
      "arguments": {
        "csv_path": "/run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/joulyzer-inspect/examples/sample_journal.csv",
        "format": "text"
      }
    }
  },
  "csv_path": "examples/sample_journal.csv",
  "format": "text"
}
```

**Response**

```json
{
  "status": "ok",
  "body_kind": "text",
  "body": "================ Joulyzer Report ================\nTrades (closed): 7   Wins: 5   Losses: 2   Open: 1\nWin rate:        71.4%\nNet PnL:         279.00\nGross profit:    419.00   Gross loss: 140.00\nProfit factor:   2.99\nAvg win:         83.80   Avg loss: -70.00\nExpectancy:      39.86 per trade\nMax drawdown:    100.00\nAvg hold (min):  77.4\nBest trade:      275.00   Worst: -100.00\n\n--- By symbol ---\n  BT... <672 more chars>"
}
```

### 4. [2026-06-24T19:50:32.001606+00:00] CLI: analyze_journal json

**Request**

```json
{
  "method": "subprocess.run",
  "cmd": [
    "/usr/bin/python",
    "-m",
    "joulyzer",
    "/run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/joulyzer-inspect/examples/sample_journal.csv",
    "--json"
  ],
  "cwd": ".",
  "csv_path": "examples/sample_journal.csv",
  "format": "json"
}
```

**Response**

```json
{
  "status": "ok",
  "returncode": 0,
  "body": {
    "trade_count": 7,
    "win_count": 5,
    "loss_count": 2,
    "open_count": 1,
    "win_rate": 0.7142857142857143,
    "net_pnl": 279.0,
    "...": "<13 more keys>"
  }
}
```

### 5. [2026-06-24T19:50:32.083472+00:00] function: analyze_journal json

**Request**

```json
{
  "module": "joulyzer",
  "fn": "analyze_journal",
  "args": {
    "csv_path": "examples/sample_journal.csv",
    "format": "json"
  }
}
```

**Response**

```json
{
  "status": "ok",
  "body": {
    "trade_count": 7,
    "win_count": 5,
    "loss_count": 2,
    "open_count": 1,
    "win_rate": 0.7142857142857143,
    "net_pnl": 279.0,
    "...": "<13 more keys>"
  }
}
```

### 6. [2026-06-24T19:50:32.084752+00:00] MCP: tools/call analyze_journal json

**Request**

```json
{
  "method": "stdio JSON-RPC",
  "server": "python -m joulyzer.agent --mcp",
  "payload": {
    "jsonrpc": "2.0",
    "id": 1001,
    "method": "tools/call",
    "params": {
      "name": "analyze_journal",
      "arguments": {
        "csv_path": "/run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/joulyzer-inspect/examples/sample_journal.csv",
        "format": "json"
      }
    }
  },
  "csv_path": "examples/sample_journal.csv",
  "format": "json"
}
```

**Response**

```json
{
  "status": "ok",
  "body": {
    "trade_count": 7,
    "win_count": 5,
    "loss_count": 2,
    "open_count": 1,
    "win_rate": 0.7142857142857143,
    "net_pnl": 279.0,
    "...": "<13 more keys>"
  }
}
```

### 7. [2026-06-24T19:50:32.086286+00:00] CLI: analyze_journal dict

**Request**

```json
{
  "method": "subprocess.run",
  "cmd": [
    "/usr/bin/python",
    "-m",
    "joulyzer",
    "/run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/joulyzer-inspect/examples/sample_journal.csv"
  ],
  "cwd": ".",
  "csv_path": "examples/sample_journal.csv",
  "format": "dict"
}
```

**Response**

```json
{
  "status": "ok",
  "returncode": 0,
  "body_kind": "text",
  "body": "================ Joulyzer Report ================\nTrades (closed): 7   Wins: 5   Losses: 2   Open: 1\nWin rate:        71.4%\nNet PnL:         279.00\nGross profit:    419.00   Gross loss: 140.00\nProfit factor:   2.99\nAvg win:         83.80   Avg loss: -70.00\nExpectancy:      39.86 per trade\nMax drawdown:    100.00\nAvg hold (min):  77.4\nBest trade:      275.00   Worst: -100.00\n\n--- By symbol ---\n  BT... <673 more chars>"
}
```

### 8. [2026-06-24T19:50:32.159766+00:00] function: analyze_journal dict

**Request**

```json
{
  "module": "joulyzer",
  "fn": "analyze_journal",
  "args": {
    "csv_path": "examples/sample_journal.csv",
    "format": "dict"
  }
}
```

**Response**

```json
{
  "status": "ok",
  "body": {
    "trade_count": 7,
    "win_count": 5,
    "loss_count": 2,
    "open_count": 1,
    "win_rate": 0.7142857142857143,
    "net_pnl": 279.0,
    "...": "<13 more keys>"
  }
}
```

### 9. [2026-06-24T19:50:32.160854+00:00] MCP: tools/call analyze_journal dict

**Request**

```json
{
  "method": "stdio JSON-RPC",
  "server": "python -m joulyzer.agent --mcp",
  "payload": {
    "jsonrpc": "2.0",
    "id": 1002,
    "method": "tools/call",
    "params": {
      "name": "analyze_journal",
      "arguments": {
        "csv_path": "/run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/joulyzer-inspect/examples/sample_journal.csv",
        "format": "dict"
      }
    }
  },
  "csv_path": "examples/sample_journal.csv",
  "format": "dict"
}
```

**Response**

```json
{
  "status": "ok",
  "body": {
    "trade_count": 7,
    "win_count": 5,
    "loss_count": 2,
    "open_count": 1,
    "win_rate": 0.7142857142857143,
    "net_pnl": 279.0,
    "...": "<13 more keys>"
  }
}
```

### 10. [2026-06-24T19:50:32.162238+00:00] CLI: analyze_journal text

**Request**

```json
{
  "method": "subprocess.run",
  "cmd": [
    "/usr/bin/python",
    "-m",
    "joulyzer",
    "/run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/joulyzer-inspect/verifiable_usage_records/live_usage_inputs/generated_small.csv"
  ],
  "cwd": ".",
  "csv_path": "verifiable_usage_records/live_usage_inputs/generated_small.csv",
  "format": "text"
}
```

**Response**

```json
{
  "status": "ok",
  "returncode": 0,
  "body_kind": "text",
  "body": "================ Joulyzer Report ================\nTrades (closed): 25   Wins: 20   Losses: 5   Open: 0\nWin rate:        80.0%\nNet PnL:         965.61\nGross profit:    1,296.54   Gross loss: 330.93\nProfit factor:   3.92\nAvg win:         64.83   Avg loss: -66.19\nExpectancy:      38.62 per trade\nMax drawdown:    246.63\nAvg hold (min):  41.7\nBest trade:      567.22   Worst: -246.63\n\n--- By symbol ---\n... <1243 more chars>"
}
```

### 11. [2026-06-24T19:50:32.234192+00:00] function: analyze_journal text

**Request**

```json
{
  "module": "joulyzer",
  "fn": "analyze_journal",
  "args": {
    "csv_path": "verifiable_usage_records/live_usage_inputs/generated_small.csv",
    "format": "text"
  }
}
```

**Response**

```json
{
  "status": "ok",
  "body_kind": "text",
  "body": "================ Joulyzer Report ================\nTrades (closed): 25   Wins: 20   Losses: 5   Open: 0\nWin rate:        80.0%\nNet PnL:         965.61\nGross profit:    1,296.54   Gross loss: 330.93\nProfit factor:   3.92\nAvg win:         64.83   Avg loss: -66.19\nExpectancy:      38.62 per trade\nMax drawdown:    246.63\nAvg hold (min):  41.7\nBest trade:      567.22   Worst: -246.63\n\n--- By symbol ---\n... <1242 more chars>"
}
```

### 12. [2026-06-24T19:50:32.236052+00:00] MCP: tools/call analyze_journal text

**Request**

```json
{
  "method": "stdio JSON-RPC",
  "server": "python -m joulyzer.agent --mcp",
  "payload": {
    "jsonrpc": "2.0",
    "id": 1003,
    "method": "tools/call",
    "params": {
      "name": "analyze_journal",
      "arguments": {
        "csv_path": "/run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/joulyzer-inspect/verifiable_usage_records/live_usage_inputs/generated_small.csv",
        "format": "text"
      }
    }
  },
  "csv_path": "verifiable_usage_records/live_usage_inputs/generated_small.csv",
  "format": "text"
}
```

**Response**

```json
{
  "status": "ok",
  "body_kind": "text",
  "body": "================ Joulyzer Report ================\nTrades (closed): 25   Wins: 20   Losses: 5   Open: 0\nWin rate:        80.0%\nNet PnL:         965.61\nGross profit:    1,296.54   Gross loss: 330.93\nProfit factor:   3.92\nAvg win:         64.83   Avg loss: -66.19\nExpectancy:      38.62 per trade\nMax drawdown:    246.63\nAvg hold (min):  41.7\nBest trade:      567.22   Worst: -246.63\n\n--- By symbol ---\n... <1242 more chars>"
}
```

### 13. [2026-06-24T19:50:32.238057+00:00] CLI: analyze_journal json

**Request**

```json
{
  "method": "subprocess.run",
  "cmd": [
    "/usr/bin/python",
    "-m",
    "joulyzer",
    "/run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/joulyzer-inspect/verifiable_usage_records/live_usage_inputs/generated_small.csv",
    "--json"
  ],
  "cwd": ".",
  "csv_path": "verifiable_usage_records/live_usage_inputs/generated_small.csv",
  "format": "json"
}
```

**Response**

```json
{
  "status": "ok",
  "returncode": 0,
  "body": {
    "trade_count": 25,
    "win_count": 20,
    "loss_count": 5,
    "open_count": 0,
    "win_rate": 0.8,
    "net_pnl": 965.6083000000002,
    "...": "<13 more keys>"
  }
}
```

### 14. [2026-06-24T19:50:32.311995+00:00] function: analyze_journal json

**Request**

```json
{
  "module": "joulyzer",
  "fn": "analyze_journal",
  "args": {
    "csv_path": "verifiable_usage_records/live_usage_inputs/generated_small.csv",
    "format": "json"
  }
}
```

**Response**

```json
{
  "status": "ok",
  "body": {
    "trade_count": 25,
    "win_count": 20,
    "loss_count": 5,
    "open_count": 0,
    "win_rate": 0.8,
    "net_pnl": 965.6083000000002,
    "...": "<13 more keys>"
  }
}
```

### 15. [2026-06-24T19:50:32.314259+00:00] MCP: tools/call analyze_journal json

**Request**

```json
{
  "method": "stdio JSON-RPC",
  "server": "python -m joulyzer.agent --mcp",
  "payload": {
    "jsonrpc": "2.0",
    "id": 1004,
    "method": "tools/call",
    "params": {
      "name": "analyze_journal",
      "arguments": {
        "csv_path": "/run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/joulyzer-inspect/verifiable_usage_records/live_usage_inputs/generated_small.csv",
        "format": "json"
      }
    }
  },
  "csv_path": "verifiable_usage_records/live_usage_inputs/generated_small.csv",
  "format": "json"
}
```

**Response**

```json
{
  "status": "ok",
  "body": {
    "trade_count": 25,
    "win_count": 20,
    "loss_count": 5,
    "open_count": 0,
    "win_rate": 0.8,
    "net_pnl": 965.6083000000002,
    "...": "<13 more keys>"
  }
}
```

### 16. [2026-06-24T19:50:32.316704+00:00] CLI: analyze_journal dict

**Request**

```json
{
  "method": "subprocess.run",
  "cmd": [
    "/usr/bin/python",
    "-m",
    "joulyzer",
    "/run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/joulyzer-inspect/verifiable_usage_records/live_usage_inputs/generated_small.csv"
  ],
  "cwd": ".",
  "csv_path": "verifiable_usage_records/live_usage_inputs/generated_small.csv",
  "format": "dict"
}
```

**Response**

```json
{
  "status": "ok",
  "returncode": 0,
  "body_kind": "text",
  "body": "================ Joulyzer Report ================\nTrades (closed): 25   Wins: 20   Losses: 5   Open: 0\nWin rate:        80.0%\nNet PnL:         965.61\nGross profit:    1,296.54   Gross loss: 330.93\nProfit factor:   3.92\nAvg win:         64.83   Avg loss: -66.19\nExpectancy:      38.62 per trade\nMax drawdown:    246.63\nAvg hold (min):  41.7\nBest trade:      567.22   Worst: -246.63\n\n--- By symbol ---\n... <1243 more chars>"
}
```

### 17. [2026-06-24T19:50:32.389793+00:00] function: analyze_journal dict

**Request**

```json
{
  "module": "joulyzer",
  "fn": "analyze_journal",
  "args": {
    "csv_path": "verifiable_usage_records/live_usage_inputs/generated_small.csv",
    "format": "dict"
  }
}
```

**Response**

```json
{
  "status": "ok",
  "body": {
    "trade_count": 25,
    "win_count": 20,
    "loss_count": 5,
    "open_count": 0,
    "win_rate": 0.8,
    "net_pnl": 965.6083000000002,
    "...": "<13 more keys>"
  }
}
```

### 18. [2026-06-24T19:50:32.391815+00:00] MCP: tools/call analyze_journal dict

**Request**

```json
{
  "method": "stdio JSON-RPC",
  "server": "python -m joulyzer.agent --mcp",
  "payload": {
    "jsonrpc": "2.0",
    "id": 1005,
    "method": "tools/call",
    "params": {
      "name": "analyze_journal",
      "arguments": {
        "csv_path": "/run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/joulyzer-inspect/verifiable_usage_records/live_usage_inputs/generated_small.csv",
        "format": "dict"
      }
    }
  },
  "csv_path": "verifiable_usage_records/live_usage_inputs/generated_small.csv",
  "format": "dict"
}
```

**Response**

```json
{
  "status": "ok",
  "body": {
    "trade_count": 25,
    "win_count": 20,
    "loss_count": 5,
    "open_count": 0,
    "win_rate": 0.8,
    "net_pnl": 965.6083000000002,
    "...": "<13 more keys>"
  }
}
```

### 19. [2026-06-24T19:50:32.394159+00:00] CLI: analyze_journal text

**Request**

```json
{
  "method": "subprocess.run",
  "cmd": [
    "/usr/bin/python",
    "-m",
    "joulyzer",
    "/run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/joulyzer-inspect/verifiable_usage_records/live_usage_inputs/generated_medium.csv"
  ],
  "cwd": ".",
  "csv_path": "verifiable_usage_records/live_usage_inputs/generated_medium.csv",
  "format": "text"
}
```

**Response**

```json
{
  "status": "ok",
  "returncode": 0,
  "body_kind": "text",
  "body": "================ Joulyzer Report ================\nTrades (closed): 80   Wins: 34   Losses: 46   Open: 0\nWin rate:        42.5%\nNet PnL:         -6,072.90\nGross profit:    9,171.01   Gross loss: 15,243.91\nProfit factor:   0.60\nAvg win:         269.74   Avg loss: -331.39\nExpectancy:      -75.91 per trade\nMax drawdown:    13,594.44\nAvg hold (min):  46.9\nBest trade:      3,573.56   Worst: -2,457.95\n\n-... <1402 more chars>"
}
```

### 20. [2026-06-24T19:50:32.476170+00:00] function: analyze_journal text

**Request**

```json
{
  "module": "joulyzer",
  "fn": "analyze_journal",
  "args": {
    "csv_path": "verifiable_usage_records/live_usage_inputs/generated_medium.csv",
    "format": "text"
  }
}
```

**Response**

```json
{
  "status": "ok",
  "body_kind": "text",
  "body": "================ Joulyzer Report ================\nTrades (closed): 80   Wins: 34   Losses: 46   Open: 0\nWin rate:        42.5%\nNet PnL:         -6,072.90\nGross profit:    9,171.01   Gross loss: 15,243.91\nProfit factor:   0.60\nAvg win:         269.74   Avg loss: -331.39\nExpectancy:      -75.91 per trade\nMax drawdown:    13,594.44\nAvg hold (min):  46.9\nBest trade:      3,573.56   Worst: -2,457.95\n\n-... <1401 more chars>"
}
```

### 21. [2026-06-24T19:50:32.481899+00:00] MCP: tools/call analyze_journal text

**Request**

```json
{
  "method": "stdio JSON-RPC",
  "server": "python -m joulyzer.agent --mcp",
  "payload": {
    "jsonrpc": "2.0",
    "id": 1006,
    "method": "tools/call",
    "params": {
      "name": "analyze_journal",
      "arguments": {
        "csv_path": "/run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/joulyzer-inspect/verifiable_usage_records/live_usage_inputs/generated_medium.csv",
        "format": "text"
      }
    }
  },
  "csv_path": "verifiable_usage_records/live_usage_inputs/generated_medium.csv",
  "format": "text"
}
```

**Response**

```json
{
  "status": "ok",
  "body_kind": "text",
  "body": "================ Joulyzer Report ================\nTrades (closed): 80   Wins: 34   Losses: 46   Open: 0\nWin rate:        42.5%\nNet PnL:         -6,072.90\nGross profit:    9,171.01   Gross loss: 15,243.91\nProfit factor:   0.60\nAvg win:         269.74   Avg loss: -331.39\nExpectancy:      -75.91 per trade\nMax drawdown:    13,594.44\nAvg hold (min):  46.9\nBest trade:      3,573.56   Worst: -2,457.95\n\n-... <1401 more chars>"
}
```

### 22. [2026-06-24T19:50:32.492390+00:00] CLI: analyze_journal json

**Request**

```json
{
  "method": "subprocess.run",
  "cmd": [
    "/usr/bin/python",
    "-m",
    "joulyzer",
    "/run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/joulyzer-inspect/verifiable_usage_records/live_usage_inputs/generated_medium.csv",
    "--json"
  ],
  "cwd": ".",
  "csv_path": "verifiable_usage_records/live_usage_inputs/generated_medium.csv",
  "format": "json"
}
```

**Response**

```json
{
  "status": "ok",
  "returncode": 0,
  "body": {
    "trade_count": 80,
    "win_count": 34,
    "loss_count": 46,
    "open_count": 0,
    "win_rate": 0.425,
    "net_pnl": -6072.904500000006,
    "...": "<13 more keys>"
  }
}
```

### 23. [2026-06-24T19:50:32.574960+00:00] function: analyze_journal json

**Request**

```json
{
  "module": "joulyzer",
  "fn": "analyze_journal",
  "args": {
    "csv_path": "verifiable_usage_records/live_usage_inputs/generated_medium.csv",
    "format": "json"
  }
}
```

**Response**

```json
{
  "status": "ok",
  "body": {
    "trade_count": 80,
    "win_count": 34,
    "loss_count": 46,
    "open_count": 0,
    "win_rate": 0.425,
    "net_pnl": -6072.904500000006,
    "...": "<13 more keys>"
  }
}
```

### 24. [2026-06-24T19:50:32.578871+00:00] MCP: tools/call analyze_journal json

**Request**

```json
{
  "method": "stdio JSON-RPC",
  "server": "python -m joulyzer.agent --mcp",
  "payload": {
    "jsonrpc": "2.0",
    "id": 1007,
    "method": "tools/call",
    "params": {
      "name": "analyze_journal",
      "arguments": {
        "csv_path": "/run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/joulyzer-inspect/verifiable_usage_records/live_usage_inputs/generated_medium.csv",
        "format": "json"
      }
    }
  },
  "csv_path": "verifiable_usage_records/live_usage_inputs/generated_medium.csv",
  "format": "json"
}
```

**Response**

```json
{
  "status": "ok",
  "body": {
    "trade_count": 80,
    "win_count": 34,
    "loss_count": 46,
    "open_count": 0,
    "win_rate": 0.425,
    "net_pnl": -6072.904500000006,
    "...": "<13 more keys>"
  }
}
```

### 25. [2026-06-24T19:50:32.583236+00:00] CLI: analyze_journal dict

**Request**

```json
{
  "method": "subprocess.run",
  "cmd": [
    "/usr/bin/python",
    "-m",
    "joulyzer",
    "/run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/joulyzer-inspect/verifiable_usage_records/live_usage_inputs/generated_medium.csv"
  ],
  "cwd": ".",
  "csv_path": "verifiable_usage_records/live_usage_inputs/generated_medium.csv",
  "format": "dict"
}
```

**Response**

```json
{
  "status": "ok",
  "returncode": 0,
  "body_kind": "text",
  "body": "================ Joulyzer Report ================\nTrades (closed): 80   Wins: 34   Losses: 46   Open: 0\nWin rate:        42.5%\nNet PnL:         -6,072.90\nGross profit:    9,171.01   Gross loss: 15,243.91\nProfit factor:   0.60\nAvg win:         269.74   Avg loss: -331.39\nExpectancy:      -75.91 per trade\nMax drawdown:    13,594.44\nAvg hold (min):  46.9\nBest trade:      3,573.56   Worst: -2,457.95\n\n-... <1402 more chars>"
}
```

### 26. [2026-06-24T19:50:32.658867+00:00] function: analyze_journal dict

**Request**

```json
{
  "module": "joulyzer",
  "fn": "analyze_journal",
  "args": {
    "csv_path": "verifiable_usage_records/live_usage_inputs/generated_medium.csv",
    "format": "dict"
  }
}
```

**Response**

```json
{
  "status": "ok",
  "body": {
    "trade_count": 80,
    "win_count": 34,
    "loss_count": 46,
    "open_count": 0,
    "win_rate": 0.425,
    "net_pnl": -6072.904500000006,
    "...": "<13 more keys>"
  }
}
```

### 27. [2026-06-24T19:50:32.662634+00:00] MCP: tools/call analyze_journal dict

**Request**

```json
{
  "method": "stdio JSON-RPC",
  "server": "python -m joulyzer.agent --mcp",
  "payload": {
    "jsonrpc": "2.0",
    "id": 1008,
    "method": "tools/call",
    "params": {
      "name": "analyze_journal",
      "arguments": {
        "csv_path": "/run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/joulyzer-inspect/verifiable_usage_records/live_usage_inputs/generated_medium.csv",
        "format": "dict"
      }
    }
  },
  "csv_path": "verifiable_usage_records/live_usage_inputs/generated_medium.csv",
  "format": "dict"
}
```

**Response**

```json
{
  "status": "ok",
  "body": {
    "trade_count": 80,
    "win_count": 34,
    "loss_count": 46,
    "open_count": 0,
    "win_rate": 0.425,
    "net_pnl": -6072.904500000006,
    "...": "<13 more keys>"
  }
}
```

### 28. [2026-06-24T19:50:32.666976+00:00] function: analyze_journal text

**Request**

```json
{
  "module": "joulyzer",
  "fn": "analyze_journal",
  "args": {
    "csv_path": "verifiable_usage_records/live_usage_inputs/bogus_no_pnl_or_price.csv",
    "format": "text"
  }
}
```

**Response**

```json
{
  "status": "error",
  "error": "JournalLoadError: Could not identify a PnL or entry_price column. Headers found: ['foo', 'bar']"
}
```

### 29. [2026-06-24T19:50:32.667683+00:00] CLI: analyze_journal text

**Request**

```json
{
  "method": "subprocess.run",
  "cmd": [
    "/usr/bin/python",
    "-m",
    "joulyzer",
    "/nonexistent/journal.csv"
  ],
  "cwd": ".",
  "csv_path": "/nonexistent/journal.csv",
  "format": "text"
}
```

**Response**

```json
{
  "status": "error",
  "returncode": 2,
  "stderr": "error: File not found: /nonexistent/journal.csv"
}
```

### 30. [2026-06-24T19:50:32.736681+00:00] function: analyze_journal json

**Request**

```json
{
  "module": "joulyzer",
  "fn": "analyze_journal",
  "args": {
    "csv_path": "/nonexistent/journal.csv",
    "format": "json"
  }
}
```

**Response**

```json
{
  "status": "error",
  "error": "JournalLoadError: File not found: /nonexistent/journal.csv"
}
```

### 31. [2026-06-24T19:50:32.736742+00:00] Bitget live call: GET /api/v2/public/time

**Request**

```json
{
  "method": "GET",
  "url": "https://api.bitget.com/api/v2/public/time",
  "endpoint": "/api/v2/public/time"
}
```

**Response**

```json
{
  "status": "ok",
  "http_status": 200,
  "latency_ms": 248.0,
  "data_sample": {
    "serverTime": "1782330632899"
  },
  "data_len": 4,
  "content_type": "application/json"
}
```

### 32. [2026-06-24T19:50:32.985088+00:00] Bitget live call: GET /api/v2/spot/market/tickers?symbol=BTCUSDT

**Request**

```json
{
  "method": "GET",
  "url": "https://api.bitget.com/api/v2/spot/market/tickers?symbol=BTCUSDT",
  "endpoint": "/api/v2/spot/market/tickers?symbol=BTCUSDT"
}
```

**Response**

```json
{
  "status": "ok",
  "http_status": 200,
  "latency_ms": 348.37,
  "data_sample": [
    {
      "open": "62328.32",
      "symbol": "BTCUSDT",
      "high24h": "63407.88",
      "low24h": "59105.71",
      "lastPr": "59840.59",
      "quoteVolume": "489670767.665845",
      "baseVolume": "7981.261042",
      "usdtVolume": "489670767.66584448",
      "ts": "1782330632509",
      "bidPr": "59840.59",
      "askPr": "59840.6",
      "bidSz": "0.052759",
      "askSz": "1.0453",
      "openUtc": "62729.21",
      "changeUtc24h": "-0.04605",
      "change24h": "-0.03991"
    }
  ],
  "data_len": 4,
  "content_type": "application/json"
}
```

### 33. [2026-06-24T19:50:33.333958+00:00] Bitget live call: GET /api/v2/spot/market/candles?symbol=BTCUSDT&granularity=1min&limit=2

**Request**

```json
{
  "method": "GET",
  "url": "https://api.bitget.com/api/v2/spot/market/candles?symbol=BTCUSDT&granularity=1min&limit=2",
  "endpoint": "/api/v2/spot/market/candles?symbol=BTCUSDT&granularity=1min&limit=2"
}
```

**Response**

```json
{
  "status": "ok",
  "http_status": 200,
  "latency_ms": 259.27,
  "data_sample": [
    [
      "1782330540000",
      "59783.41",
      "59811.66",
      "59777.69",
      "59811.66",
      "3.848292",
      "230086.02340335",
      "230086.02340335"
    ],
    [
      "1782330600000",
      "59811.66",
      "59860",
      "59760.78",
      "59840.59",
      "16.828416",
      "1006501.36344313",
      "1006501.36344313"
    ]
  ],
  "data_len": 4,
  "content_type": "application/json"
}
```

