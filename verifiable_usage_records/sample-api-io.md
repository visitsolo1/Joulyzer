# Sample API I/O — Joulyzer

_Five focused request/response pairs showing joulyzer's real wire formats for each caller + one live Bitget call._

## 1. CLI: analyze_journal json

- **Session ID**: `55053e8f5a19`
- **Timestamp**: 2026-06-24T19:54:33.253849+00:00
- **Duration**: 88.602 ms

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
    "gross_profit": 419.0,
    "gross_loss": 140.0,
    "profit_factor": 2.992857142857143,
    "avg_win": 83.8,
    "avg_loss": -70.0,
    "expectancy": 39.857142857142854,
    "max_drawdown": 100.0,
    "avg_hold_minutes": 77.42857142857143,
    "best_trade": 275.0,
    "worst_trade": -100.0,
    "by_symbol": [
      {
        "symbol": "BTCUSDT",
        "trades": 3,
        "wins": 2,
        "losses": 1,
        "net_pnl": 185.0,
        "win_rate": 0.6666666666666666
      },
      {
        "symbol": "ETHUSDT",
        "trades": 2,
        "wins": 1,
        "losses": 1,
        "net_pnl": 70.0,
        "win_rate": 0.5
      },
      {
        "symbol": "SOLUSDT",
        "trades": 2,
        "wins": 2,
        "losses": 0,
        "net_pnl": 24.0,
        "win_rate": 1.0
      }
    ],
    "by_hour": {
      "9": {
        "trades": 1,
        "net_pnl": 275.0
      },
      "14": {
        "trades": 1,
        "net_pnl": 10.0
      },
      "11": {
        "trades": 1,
        "net_pnl": -40.0
      },
      "13": {
        "trades": 1,
        "net_pnl": 110.0
      },
      "8": {
        "trades": 1,
        "net_pnl": 6.0
      },
      "15": {
        "trades": 1,
        "net_pnl": 18.0
      },
      "10": {
        "trades": 1,
        "net_pnl": -100.0
      }
    },
    "by_tag": {
      "breakout": {
        "trades": 2,
        "net_pnl": 385.0
      },
      "scalp": {
        "trades": 3,
        "net_pnl": 34.0
      },
      "fomo": {
        "trades": 1,
        "net_pnl": -40.0
      },
      "revenge": {
        "trades": 1,
        "net_pnl": -100.0
      }
    }
  }
}
```

## 2. function: analyze_journal json

- **Session ID**: `55053e8f5a19`
- **Timestamp**: 2026-06-24T19:54:33.342583+00:00
- **Duration**: 1.252 ms

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
    "gross_profit": 419.0,
    "gross_loss": 140.0,
    "profit_factor": 2.992857142857143,
    "avg_win": 83.8,
    "avg_loss": -70.0,
    "expectancy": 39.857142857142854,
    "max_drawdown": 100.0,
    "avg_hold_minutes": 77.42857142857143,
    "best_trade": 275.0,
    "worst_trade": -100.0,
    "by_symbol": [
      {
        "symbol": "BTCUSDT",
        "trades": 3,
        "wins": 2,
        "losses": 1,
        "net_pnl": 185.0,
        "win_rate": 0.6666666666666666
      },
      {
        "symbol": "ETHUSDT",
        "trades": 2,
        "wins": 1,
        "losses": 1,
        "net_pnl": 70.0,
        "win_rate": 0.5
      },
      {
        "symbol": "SOLUSDT",
        "trades": 2,
        "wins": 2,
        "losses": 0,
        "net_pnl": 24.0,
        "win_rate": 1.0
      }
    ],
    "by_hour": {
      "9": {
        "trades": 1,
        "net_pnl": 275.0
      },
      "14": {
        "trades": 1,
        "net_pnl": 10.0
      },
      "11": {
        "trades": 1,
        "net_pnl": -40.0
      },
      "13": {
        "trades": 1,
        "net_pnl": 110.0
      },
      "8": {
        "trades": 1,
        "net_pnl": 6.0
      },
      "15": {
        "trades": 1,
        "net_pnl": 18.0
      },
      "10": {
        "trades": 1,
        "net_pnl": -100.0
      }
    },
    "by_tag": {
      "breakout": {
        "trades": 2,
        "net_pnl": 385.0
      },
      "scalp": {
        "trades": 3,
        "net_pnl": 34.0
      },
      "fomo": {
        "trades": 1,
        "net_pnl": -40.0
      },
      "revenge": {
        "trades": 1,
        "net_pnl": -100.0
      }
    }
  }
}
```

## 3. MCP: tools/call analyze_journal json

- **Session ID**: `55053e8f5a19`
- **Timestamp**: 2026-06-24T19:54:33.343939+00:00
- **Duration**: 1.695 ms

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
    "gross_profit": 419.0,
    "gross_loss": 140.0,
    "profit_factor": 2.992857142857143,
    "avg_win": 83.8,
    "avg_loss": -70.0,
    "expectancy": 39.857142857142854,
    "max_drawdown": 100.0,
    "avg_hold_minutes": 77.42857142857143,
    "best_trade": 275.0,
    "worst_trade": -100.0,
    "by_symbol": [
      {
        "symbol": "BTCUSDT",
        "trades": 3,
        "wins": 2,
        "losses": 1,
        "net_pnl": 185.0,
        "win_rate": 0.6666666666666666
      },
      {
        "symbol": "ETHUSDT",
        "trades": 2,
        "wins": 1,
        "losses": 1,
        "net_pnl": 70.0,
        "win_rate": 0.5
      },
      {
        "symbol": "SOLUSDT",
        "trades": 2,
        "wins": 2,
        "losses": 0,
        "net_pnl": 24.0,
        "win_rate": 1.0
      }
    ],
    "by_hour": {
      "9": {
        "trades": 1,
        "net_pnl": 275.0
      },
      "14": {
        "trades": 1,
        "net_pnl": 10.0
      },
      "11": {
        "trades": 1,
        "net_pnl": -40.0
      },
      "13": {
        "trades": 1,
        "net_pnl": 110.0
      },
      "8": {
        "trades": 1,
        "net_pnl": 6.0
      },
      "15": {
        "trades": 1,
        "net_pnl": 18.0
      },
      "10": {
        "trades": 1,
        "net_pnl": -100.0
      }
    },
    "by_tag": {
      "breakout": {
        "trades": 2,
        "net_pnl": 385.0
      },
      "scalp": {
        "trades": 3,
        "net_pnl": 34.0
      },
      "fomo": {
        "trades": 1,
        "net_pnl": -40.0
      },
      "revenge": {
        "trades": 1,
        "net_pnl": -100.0
      }
    }
  }
}
```

## 4. demo: examples/agent_integration.py

- **Session ID**: `55053e8f5a19`
- **Timestamp**: 2026-06-24T19:54:34.035217+00:00
- **Duration**: 109.423 ms

**Request**

```json
{
  "method": "subprocess.run",
  "cmd": [
    "/usr/bin/python",
    "/run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/joulyzer-inspect/examples/agent_integration.py"
  ],
  "cwd": "."
}
```

**Response**

```json
{
  "status": "ok",
  "returncode": 0,
  "stdout": "[ok] fills generated         : 240 (open+close pairs)\n[ok] api call log written    : /run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/joulyzer-inspect/verifiable_usage_records/integration_run/bitget_api_call_log.jsonl\n[ok] journal csv written     : /run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/joulyzer-inspect/verifiable_usage_records/integration_run/agent_session_journal.csv\n[ok] agent tool call result  : /run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/joulyzer-inspect/verifiable_usage_records/integration_run/agent_tool_call_result.json\n\n[ok] analyzed 120 closed trades, net PnL 4,674.38, win rate 57.5%, profit factor 1.42\n",
  "result_summary": {
    "tool_call": {
      "name": "analyze_journal",
      "arguments": {
        "csv_path": "/run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/joulyzer-inspect/verifiable_usage_records/integration_run/agent_session_journal.csv",
        "format": "json"
      }
    },
    "result_type": "str",
    "result_preview_trade_count": 120,
    "result_preview_net_pnl": 4674.376499999999,
    "result_preview_win_rate": 0.575
  }
}
```

## 5. Bitget live call: GET /api/v2/public/time

- **Session ID**: `55053e8f5a19`
- **Timestamp**: 2026-06-24T19:54:34.146496+00:00
- **Duration**: 243.858 ms

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
  "latency_ms": 243.86,
  "data_sample": {
    "serverTime": "1782330874306"
  },
  "data_len": 4,
  "content_type": "application/json"
}
```
