"""Logging configuration for the JVIS CLI.

Provides a single ``setup_logging`` function called early in the CLI
entrypoint.  All modules use ``logging.getLogger(__name__)`` — the
hierarchy roots at ``jvis`` so a single handler on that logger captures
everything.
"""

from __future__ import annotations

import logging
import sys


def setup_logging(*, verbose: bool = False) -> None:
    """Configure the ``jvis`` logger hierarchy.

    Parameters
    ----------
    verbose:
        When *True*, set the level to DEBUG and emit to stderr.
        When *False* (default), only WARNING and above are shown.
    """
    level = logging.DEBUG if verbose else logging.WARNING
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(levelname)s [%(name)s] %(message)s"))

    root = logging.getLogger("jvis")
    root.setLevel(level)
    # Avoid duplicate handlers on repeated calls (e.g., in tests)
    if not root.handlers:
        root.addHandler(handler)
