"""Enable `python -m joulyzer <file.csv>`.

For the agent adapter (`python -m joulyzer.agent --mcp/--schema/--manifest`),
see ``joulyzer/agent.py``.
"""

from .cli import main

raise SystemExit(main())
