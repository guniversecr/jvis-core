"""JVIS CLI UI helpers — colors and formatted output."""

from __future__ import annotations

import logging
import os
import sys
from collections.abc import Callable

logger = logging.getLogger(__name__)

# Detect color support
_NO_COLOR = os.environ.get("NO_COLOR") is not None
_FORCE_COLOR = os.environ.get("FORCE_COLOR") is not None
_IS_TTY = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
USE_COLORS = (_IS_TTY or _FORCE_COLOR) and not _NO_COLOR

# ANSI codes
_RESET = "\033[0m"
_BOLD = "\033[1m"
_RED = "\033[31m"
_GREEN = "\033[32m"
_YELLOW = "\033[33m"
_BLUE = "\033[34m"
_MAGENTA = "\033[35m"
_CYAN = "\033[36m"


def _wrap(code: str, text: str) -> str:
    if not USE_COLORS:
        return text
    return f"{code}{text}{_RESET}"


def red(text: str) -> str:
    return _wrap(_RED, text)


def green(text: str) -> str:
    return _wrap(_GREEN, text)


def yellow(text: str) -> str:
    return _wrap(_YELLOW, text)


def blue(text: str) -> str:
    return _wrap(_BLUE, text)


def magenta(text: str) -> str:
    return _wrap(_MAGENTA, text)


def cyan(text: str) -> str:
    return _wrap(_CYAN, text)


def bold(text: str) -> str:
    return _wrap(_BOLD, text)


def header(title: str) -> str:
    """Return a boxed header line."""
    bar = cyan("=" * 72)
    return f"\n{bar}\n  {title}\n{bar}\n"


def error(message: str) -> str:
    return f"{red('Error:')} {message}"


def prompt_choice[T](
    items: list[T],
    label: str,
    display_fn: Callable[[T], str] | None = None,
    detail_fn: Callable[[T], str] | None = None,
) -> T:
    """Prompt user to select from a numbered list.

    Auto-selects if only one item. Retries on invalid input.
    """
    import click

    if not items:
        raise ValueError("prompt_choice requires at least one item")

    _display = display_fn or str

    if len(items) == 1:
        selected = items[0]
        click.echo(f"  {green('✓')} {label.capitalize()}: {_display(selected)}")
        return selected

    click.echo("")
    click.echo(f"  {cyan(f'Select {label}:')}")
    click.echo("")
    for i, item in enumerate(items, 1):
        click.echo(f"    {i}) {bold(_display(item))}")
        if detail_fn:
            click.echo(f"       {detail_fn(item)}")
    click.echo("")

    while True:
        choice = click.prompt(f"  Select {label}", default="1", show_default=True)
        try:
            # Users see 1-indexed menu; convert to 0-indexed list access
            idx = int(choice) - 1
            if 0 <= idx < len(items):
                selected = items[idx]
                click.echo(f"  {green('✓')} {label.capitalize()}: {_display(selected)}")
                return selected
        except ValueError:
            pass
        click.echo(f"  {red('Invalid')}. Enter 1-{len(items)}.")
