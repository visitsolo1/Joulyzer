# Contributing to Joulyzer

Thanks for the interest. Joulyzer is intentionally tiny — the
maintainer bar is "any change has to keep the dependency surface
empty and the public function surface stable."

## Development setup

```bash
git clone https://github.com/visitsolo1/Joulyzer.git
cd Joulyzer
pip install -e ".[test]"
```

## Running tests

```bash
python -m pytest tests/ -v
```

All 16 tests should pass with no warnings. CI runs against
Python 3.9, 3.10, 3.11, 3.12 (see `.github/workflows/tests.yml`).

## Adding a metric

1. Add the field to `MetricsReport` in `joulyzer/metrics.py`.
2. Compute it in `compute_metrics()`.
3. Add it to `MetricsReport.to_dict()` (so JSON serialization keeps
   working) **and** to `render_text_report()` in `joulyzer/report.py`.
4. Add an assertion in `tests/test_joulyzer.py`.
5. Update `SKILL.md` if the metric is part of the agent-facing surface.

## Adding a CSV column alias

Add the alias to `COLUMN_ALIASES` in `joulyzer/parser.py`. Existing
tests should still pass — `test_load_sample` checks every trade
parses.

## Adding a new agent tool

1. Add the function in `joulyzer/agent.py`.
2. Add a matching entry in `_MCP_DISPATCH`.
3. Add the schema to `TOOL_SCHEMA`.
4. Add the manifest entry in `mcp_manifest()`.
5. Add tests in `tests/test_agent_and_generator.py`.

## Coding style

- Python 3.9+ compatible (no walrus-only patterns in lib code).
- No third-party deps in `joulyzer/` — stdlib only.
- Test deps (pytest) live under `[project.optional-dependencies].test`.
- Public API surface lives in `joulyzer/__init__.py` — keep it small.

## Pull request process

1. Branch from `main`.
2. `python -m pytest tests/ -v` passes locally.
3. Update `README.md` / `SKILL.md` / `PROJECT_DESCRIPTION.md` if the
   change is user-visible.
4. Open the PR with a one-paragraph summary of what changed and why.

## Reporting issues

Open a GitHub issue. Include:

- joulyzer version (`python -c "import joulyzer; print(joulyzer.__version__)"`).
- Python version.
- Minimal CSV + command that reproduces the bug.
