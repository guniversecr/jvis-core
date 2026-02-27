"""Tests for jvis.log_config — structured logging setup."""

from __future__ import annotations

import logging

from jvis.log_config import setup_logging


class TestSetupLogging:
    """Verify setup_logging configures the jvis logger hierarchy."""

    def test_default_level_is_warning(self) -> None:
        setup_logging(verbose=False)
        root = logging.getLogger("jvis")
        assert root.level == logging.WARNING

    def test_verbose_level_is_debug(self) -> None:
        setup_logging(verbose=True)
        root = logging.getLogger("jvis")
        assert root.level == logging.DEBUG

    def test_handler_writes_to_stderr(self) -> None:
        setup_logging(verbose=False)
        root = logging.getLogger("jvis")
        assert len(root.handlers) >= 1
        handler = root.handlers[0]
        assert isinstance(handler, logging.StreamHandler)

    def test_format_includes_levelname_and_module(self) -> None:
        setup_logging(verbose=False)
        root = logging.getLogger("jvis")
        handler = root.handlers[0]
        fmt = handler.formatter
        assert fmt is not None
        assert "%(levelname)s" in fmt._fmt
        assert "%(name)s" in fmt._fmt

    def test_child_logger_inherits(self) -> None:
        setup_logging(verbose=True)
        child = logging.getLogger("jvis.stacks.registry")
        assert child.getEffectiveLevel() == logging.DEBUG

    def test_no_duplicate_handlers_on_repeated_calls(self) -> None:
        # Reset handlers for clean test
        root = logging.getLogger("jvis")
        root.handlers.clear()

        setup_logging(verbose=False)
        setup_logging(verbose=True)
        assert len(root.handlers) == 1
