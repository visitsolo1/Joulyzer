# Installing Joulyzer

> Zero-to-running in **under 2 minutes** for judges. Three commands, no
> API keys, no network. Python 3.9+ required, everything else is stdlib.

---

## TL;DR — three commands

```bash
git clone https://github.com/visitsolo1/Joulyzer.git
cd Joulyzer
pip install -e ".[test]"
```

You now have a working `joulyzer` install, the `python -m joulyzer` CLI,
the `python -m joulyzer.agent` MCP server, and a `pytest` test suite
with 16 tests.

Verify it works:

```bash
python -m pytest tests/ -v
# expected: 16 passed

python -m joulyzer examples/sample_journal.csv
# expected: prints "================ Joulyzer Report ================" ...
```

That's the whole install. The rest of this document is for edge cases,
verifiable-artifact regeneration, and CI integration.

---

## Prerequisites

| Requirement | Minimum | Notes                                                          |
|-------------|---------|----------------------------------------------------------------|
| Python      | 3.9+    | Tested on 3.9, 3.10, 3.11, 3.12 (see CI matrix)                |
| pip         | 21+     | Bundled with modern Python; only needed for the `[test]` extra |
| git         | any     | Only if cloning — `pip install` from a tarball also works       |
| OS          | any     | Linux, macOS, Windows, WSL — all stdlib-only, no native deps   |

Joulyzer has **zero runtime dependencies**. The only "extra" is `pytest`
for the test suite, and that's only required if you want to run the
tests yourself.

---

## Install paths

### A. Editable install (recommended for judges / contributors)

```bash
# from a clean clone
git clone https://github.com/visitsolo1/Joulyzer.git
cd Joulyzer
pip install -e ".[test]"
```

Editable means: changes to the source are picked up immediately without
re-installing. Best for reading the code, running the tests, or hacking
on the package.

### B. Non-editable install (recommended for AI agents / production)

```bash
pip install "git+https://github.com/visitsolo1/Joulyzer.git"
```

The package lands in `site-packages`. No source directory is created.
Best for embedding joulyzer inside another tool.

### C. Tarball install (air-gapped environments)

```bash
# On a machine with internet:
pip download "git+https://github.com/visitsolo1/Joulyzer.git" --no-deps -d ./joulyzer-dl
# Copy ./joulyzer-dl/ to the air-gapped machine, then:
pip install --no-index --find-links=./joulyzer-dl joulyzer
```

### D. Just drop the source in your project

```bash
# Copy joulyzer/ into your project, then:
pip install -e ".[test]"   # still works; you just don't need to clone the repo
```

This is what most agent-framework integrations do — they vendor the
`joulyzer/` package directly.

---

## Run the full demo (30 seconds)

After install, copy-paste this single block to see every feature
joulyzer ships:

```bash
# 1. Tests (16/16 should pass)
python -m pytest tests/ -v

# 2. CLI text report on the bundled sample
python -m joulyzer examples/sample_journal.csv

# 3. CLI JSON report (pipe into another tool or an LLM)
python -m joulyzer examples/sample_journal.csv --json

# 4. End-to-end agent integration: generate Bitget-shaped fills,
#    convert to a journal, dispatch a model tool_call, persist result.
python examples/agent_integration.py

# 5. Print the tool schema any LLM/agent will see
python -m joulyzer.agent --schema

# 6. Print the MCP server manifest
python -m joulyzer.agent --manifest

# 7. Regenerate every artifact in verifiable_usage_records/
bash scripts/verify_submission.sh
```

Expected output: `16 passed`, a text report, a JSON report, a success
message from the integration example, two JSON blobs (tool schema + MCP
manifest), and a verifier summary listing every artifact.

---

## Use joulyzer as a tool inside your AI agent

Pick whichever surface matches your stack. All three are zero-dep.

### A. Direct function call (simplest)

```python
from joulyzer import analyze_journal
result = analyze_journal("path/to/journal.csv", format="json")
```

### B. OpenAI / Anthropic / Qwen function-calling

```python
from joulyzer import TOOL_SCHEMA
# Register TOOL_SCHEMA with your model. It will produce:
#   {"name": "analyze_journal",
#    "arguments": {"csv_path": "...", "format": "json"}}
# Dispatch those into joulyzer.analyze_journal(**arguments).
```

### C. MCP server (Claude Code, Continue, Bitget getagent, any MCP client)

```bash
# Start the server (talks JSON-RPC over stdio)
python -m joulyzer.agent --mcp
```

Point any MCP-aware client at the spawned stdio process and it will
discover `analyze_journal` automatically. See `scripts/mcp_client_demo.py`
for a working end-to-end client → server → log capture.

---

## Run the MCP server in a separate process and drive it

If you want to see what real MCP traffic looks like, there's a
self-contained demo:

```bash
# Capture a live JSON-RPC session: client → MCP server → joulyzer
python scripts/mcp_client_demo.py
# Output:
#   verifiable_usage_records/live_mcp_session.log.jsonl
```

This is the **live usage log** submitted as the Track-2 verifiable
usage record. Every line is a real request sent to a real joulyzer
MCP server process and the real response that came back.

---

## Verifying the install (for hackathon judges)

Two commands. Both should "just work" with no configuration.

```bash
# 1. Functional check — 16 unit tests must pass.
python -m pytest tests/ -v

# 2. Reproducible artifact check — regenerates all verifiable files.
bash scripts/verify_submission.sh
```

If either fails, open an issue with the output:
https://github.com/visitsolo1/Joulyzer/issues

---

## Uninstalling

```bash
pip uninstall joulyzer
```

The `joulyzer.egg-info/` left in the clone directory is harmless and
will be ignored by git. Delete the clone directory if you want a fully
clean state.

---

## Troubleshooting

### `python: command not found`

You have Python installed but `python` isn't on PATH. Try `python3`
instead, or install Python 3.9+ from https://python.org.

### `pip: command not found`

Use `python -m pip` instead of bare `pip`. Modern Python always has pip
bundled; it's just not always on PATH.

### `externally-managed-environment` (PEP 668) on Debian/Ubuntu

Use a virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
```

Or, for a one-off inspection, override:

```bash
pip install --break-system-packages -e ".[test]"
```

### `ModuleNotFoundError: No module named 'joulyzer' after install`

You're probably running `python` from a different venv than the one you
installed into. Either `source .venv/bin/activate` first, or use
`python -m pip install` so pip targets the same interpreter.

### Tests fail on Python < 3.9

Joulyzer targets 3.9+ as a hard floor (it uses `from __future__ import
annotations`, PEP 604 union syntax is avoided). Upgrade Python.

### Want to use it from a Jupyter notebook

Joulyzer is stdlib-only, so it works in any Python environment that has
`import csv`. Just `pip install -e .` (no `[test]` needed in a notebook)
and `from joulyzer import analyze_journal`.

---

## Where to next

- **`README.md`** — what joulyzer is, four-part architecture, AI-trading take
- **`SKILL.md`** — agent-facing description of the tool
- **`PROJECT_DESCRIPTION.md`** — the four-part submission write-up for
  the Bitget AI Base Camp Hackathon S1 form
- **`docs/github-actions-tests.yml`** — drop this into
  `.github/workflows/tests.yml` to enable CI on your fork
- **`verifiable_usage_records/`** — every artifact referenced in the
  submission, all regenerable via `bash scripts/verify_submission.sh`
- **`CONTRIBUTING.md`** — how to add a metric, CSV alias, or new tool
