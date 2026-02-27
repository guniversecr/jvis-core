"""Root conftest — ensures src/jvis is importable for all tests."""

from __future__ import annotations

import sys
from pathlib import Path

# Add src/ to path so 'from jvis.cli import cli' works without pip install -e
src_dir = str(Path(__file__).parent.parent / "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
