"""Create shared project files — .editorconfig, .gitignore, README, etc."""

from __future__ import annotations

import logging
from datetime import date
from pathlib import Path

from jvis.stacks.registry import StackInfo
from jvis.utils.config import read_version
from jvis.utils.fs import write_file

logger = logging.getLogger(__name__)

# EditorConfig conventions:
# - 4-space indent: Python (PEP 8), PHP (PSR-12), Rust (rustfmt default)
# - 2-space indent: JS/TS (Prettier default, Airbnb styleguide), JSON, YAML, HTML, CSS
# - Markdown: trailing whitespace is significant (line break = two trailing spaces)
# - Makefile: requires tabs per POSIX make specification
_EDITORCONFIG = """\
root = true

[*]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.{js,jsx,ts,tsx,json,yml,yaml,css,html}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
"""

_ENV_EXAMPLE = """\
# Environment Variables
# Copy this file to .env and fill in the values

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Application
APP_ENV=development
APP_PORT=8000
APP_SECRET=change-me-in-production
"""

_SECURITY_MD = """\
# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do NOT** open a public issue
2. Email security concerns to the project maintainers
3. Include steps to reproduce the vulnerability
4. Allow reasonable time for a fix before disclosure

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest  | Yes       |
"""

_CONTRIBUTING_MD = """\
# Contributing

## Development Setup

1. Clone the repository
2. Install dependencies
3. Run tests to verify setup

## Pull Request Process

1. Create a feature branch from `main`
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation if needed
5. Submit a pull request

## Code Style

Follow the project's established conventions. Run the linter before submitting.
"""

_CHANGELOG_MD = """\
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added
- Initial project setup with JVIS framework
"""


def create_shared_files(
    project_dir: Path,
    project_name: str,
    project_description: str = "",
    stack: StackInfo | None = None,
) -> None:
    """Create common project files (.editorconfig, README, etc.)."""
    write_file(project_dir / ".editorconfig", _EDITORCONFIG)
    write_file(project_dir / ".env.example", _ENV_EXAMPLE)
    write_file(project_dir / "SECURITY.md", _SECURITY_MD)
    write_file(project_dir / "CONTRIBUTING.md", _CONTRIBUTING_MD)
    write_file(project_dir / "CHANGELOG.md", _CHANGELOG_MD)

    readme = _build_readme(project_name, project_description, stack)
    write_file(project_dir / "README.md", readme)


def _build_readme(name: str, description: str, stack: StackInfo | None = None) -> str:
    desc_line = f"\n{description}\n" if description else ""
    getting_started = _getting_started_section(stack)
    return f"""\
# {name}
{desc_line}
{getting_started}

## Development

This project uses [JVIS](https://github.com/guniversecr/jvis) for AI-assisted development.

### Recommended Workflow

1. `/pm` — Create PRD
2. `/architect` — Design architecture
3. `/sm` — Create stories
4. `/dev` — Implement
5. `/qa` — Review and quality gates

## License

See [LICENSE](LICENSE) for details.

---

Created on {date.today().isoformat()} with JVIS v{read_version()}
"""


def _getting_started_section(stack: StackInfo | None) -> str:
    """Build Getting Started markdown from stack manifest data."""
    _FALLBACK = """\
## Getting Started

```bash
# Install dependencies and start development server
make dev
```"""
    if not stack or not stack.getting_started:
        return _FALLBACK

    gs = stack.getting_started
    prerequisites = gs.get("prerequisites", "")
    commands: list[str] = gs.get("commands", [])

    parts: list[str] = []
    if prerequisites:
        parts.append(f"## Prerequisites\n\n- **{prerequisites}** is required.")
    if commands:
        cmd_block = "\n".join(commands)
        parts.append(f"## Getting Started\n\n```bash\n{cmd_block}\n```")

    return "\n\n".join(parts) if parts else _FALLBACK
