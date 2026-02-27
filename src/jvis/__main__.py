"""Allow running JVIS via `python -m jvis`."""

import sys

MINIMUM_PYTHON = (3, 12)
if sys.version_info < MINIMUM_PYTHON:
    sys.exit(
        f"Error: JVIS requires Python {MINIMUM_PYTHON[0]}.{MINIMUM_PYTHON[1]}+. "
        f"Current: Python {sys.version_info.major}.{sys.version_info.minor}.\n"
        f"Install Python 3.12+ from https://python.org"
    )

from jvis.cli import main

main()
