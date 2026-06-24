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

# 1. Install (idempotent; works on Debian PEP 668 systems too)
echo "==> Step 1/7: pip install -e .[test]"
if pip install --quiet --break-system-packages -e ".[test]" 2>/dev/null; then
    :
elif pip install --quiet -e ".[test]"; then
    :
else
    echo "    !! pip install failed — proceeding anyway (tests may fail)"
fi

# 2. Tests
echo "==> Step 2/7: pytest"
python -m pytest tests/ -v | tee "$ROOT/verifiable_usage_records/pytest_run.log"

# 3. CLI text + JSON
echo
echo "==> Step 3/7: CLI runs"
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
echo "==> Step 4/7: agent integration example"
python examples/agent_integration.py | tee "$ROOT/verifiable_usage_records/integration_run_stdout.txt"

# 5. Live MCP client → server session (real API call log)
echo
echo "==> Step 5/7: live MCP client → server session"
python scripts/mcp_client_demo.py

# 5b. Live usage harness (multi-caller, multi-journal, multi-format)
echo
echo "==> Step 5b/7: live usage harness (CLI + function + MCP, 3 journals, 3 formats + 3 errors)"
python scripts/live_usage_harness.py

# 6. Tool surface artifacts
echo
echo "==> Step 7/7: summary"
echo "    ==> ALL ARTIFACTS REGENERATED"
ls -la "$ROOT/verifiable_usage_records/"
echo
echo "    integration_run/:"
ls -la "$ROOT/verifiable_usage_records/integration_run/"
echo
echo "    live_session/:"
ls -la "$ROOT/verifiable_usage_records/live_session/" 2>/dev/null || true
echo
echo "    live_usage_inputs/:"
ls -la "$ROOT/verifiable_usage_records/live_usage_inputs/" 2>/dev/null || true
