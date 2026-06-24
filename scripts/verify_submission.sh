#!/usr/bin/env bash
# Verifier — regenerates every artifact in verifiable_usage_records/
# so judges (or the maintainer) can prove the submission is reproducible.
#
# Usage:  bash scripts/verify_submission.sh
#
# Exits non-zero on any failure. Writes a final summary to stdout.

set -euo pipefail

cd "$(dirname "$0")/.."
ROOT="$(pwd)"

echo "==> Joulyzer submission verifier"
echo "    root: $ROOT"
echo

# 1. Install (idempotent)
echo "==> Step 1/5: pip install -e .[test]"
pip install --quiet --break-system-packages -e ".[test]" 2>/dev/null || \
    pip install --quiet -e ".[test]"

# 2. Tests
echo "==> Step 2/5: pytest"
python -m pytest tests/ -v | tee "$ROOT/verifiable_usage_records/pytest_run.log"

# 3. CLI text + JSON
echo
echo "==> Step 3/5: CLI runs"
python -m joulyzer examples/sample_journal.csv > /tmp/_text.txt
python -m joulyzer examples/sample_journal.csv --json > /tmp/_json.json
{
  echo "=== joulyzer CLI on examples/sample_journal.csv (text) ==="
  cat /tmp/_text.txt
  echo
  echo "=== joulyzer CLI on examples/sample_journal.csv (JSON) ==="
  cat /tmp/_json.json
} > "$ROOT/verifiable_usage_records/cli_text_run.txt"
echo "    wrote verifiable_usage_records/cli_text_run.txt"

# 4. End-to-end agent integration
echo
echo "==> Step 4/5: agent integration example"
python examples/agent_integration.py | tee "$ROOT/verifiable_usage_records/integration_run_stdout.txt"

# 5. Tool surface artifacts
echo
echo "==> Step 5/5: tool schema + MCP manifest"
python -m joulyzer.agent --schema  > "$ROOT/verifiable_usage_records/tool_schema.json"
python -m joulyzer.agent --manifest > "$ROOT/verifiable_usage_records/mcp_manifest.json"
echo "    wrote tool_schema.json + mcp_manifest.json"

echo
echo "==> ALL ARTIFACTS REGENERATED"
ls -la "$ROOT/verifiable_usage_records/"
ls -la "$ROOT/verifiable_usage_records/integration_run/"
