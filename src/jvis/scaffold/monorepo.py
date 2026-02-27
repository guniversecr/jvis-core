"""Create monorepo root files for fullstack projects (docker-compose, Makefile)."""

from __future__ import annotations

import logging
from pathlib import Path

from jvis.stacks.registry import StackInfo
from jvis.utils.fs import mkdir_p, write_file
from jvis.utils.validation import _NAME_RE

logger = logging.getLogger(__name__)


def create_monorepo_root(
    project_dir: Path,
    project_name: str,
    backend_stack: StackInfo | None,
    frontend_stack: StackInfo | None,
    database: str = "postgresql",
    mobile_stack: StackInfo | None = None,
) -> None:
    """Create root-level monorepo files (docker-compose.yaml, Makefile, README section)."""
    if not _NAME_RE.match(project_name):
        raise ValueError(f"Invalid project name for scaffold: {project_name!r}")
    mkdir_p(project_dir / "server")
    mkdir_p(project_dir / "client")
    if mobile_stack:
        mkdir_p(project_dir / "mobile")

    _write_docker_compose(project_dir, project_name, backend_stack, frontend_stack, database, mobile_stack)
    _write_makefile(project_dir, project_name, mobile_stack)


def _write_docker_compose(
    project_dir: Path,
    project_name: str,
    backend_stack: StackInfo | None,
    frontend_stack: StackInfo | None,
    database: str,
    mobile_stack: StackInfo | None,
) -> None:
    db_service = _db_service_block(database, project_name)
    backend_port = str(backend_stack.dev_port) if backend_stack else "8000"
    backend_cmd = (
        backend_stack.dev_command
        if backend_stack and backend_stack.dev_command
        else "echo 'Configure dev command for your stack'"
    )

    # Docker Compose v3.8: minimum for features like configs/secrets in Swarm mode.
    # Still compatible with standalone `docker compose` (v2 CLI) which ignores the field.
    content = f"""\
version: "3.8"

services:
  server:
    build:
      context: ./server
      dockerfile: Dockerfile
    ports:
      - "{backend_port}:{backend_port}"
    environment:
      - DATABASE_URL=${{DATABASE_URL:-postgresql://postgres:${{POSTGRES_PASSWORD:?Set POSTGRES_PASSWORD in .env}}@db:5432/{project_name}}}
      - APP_ENV=development
    volumes:
      - ./server:/app
    depends_on:
      - db
    command: {backend_cmd}

  client:
    build:
      context: ./client
      dockerfile: Dockerfile
    ports:
      - "3000:3000"  # Standard Vite/Next.js/Nuxt dev server port
    environment:
      - VITE_API_URL=http://localhost:{backend_port}
    volumes:
      - ./client:/app
      - /app/node_modules
    command: npm run dev -- --host 0.0.0.0

{db_service}

volumes:
  db-data:
"""
    write_file(project_dir / "docker-compose.yaml", content)


def _db_service_block(database: str, project_name: str) -> str:
    if database == "mysql":
        return f"""\
  db:
    image: mysql:8  # MySQL 8.x is current GA release with JSON, CTEs, window functions
    environment:
      MYSQL_ROOT_PASSWORD: ${{MYSQL_ROOT_PASSWORD:?Set MYSQL_ROOT_PASSWORD in .env}}
      MYSQL_DATABASE: {project_name}
    ports:
      - "3306:3306"
    volumes:
      - db-data:/var/lib/mysql"""
    # Default: postgresql
    return f"""\
  db:
    image: postgres:16-alpine  # Alpine variant for smaller image; 16 is current LTS
    environment:
      POSTGRES_DB: {project_name}
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${{POSTGRES_PASSWORD:?Set POSTGRES_PASSWORD in .env}}
    ports:
      - "5432:5432"
    volumes:
      - db-data:/var/lib/postgresql/data"""


def _write_makefile(project_dir: Path, project_name: str, mobile_stack: StackInfo | None) -> None:
    mobile_targets = ""
    if mobile_stack:
        mobile_targets = """
.PHONY: dev-mobile
dev-mobile:  ## Start mobile development server
\tcd mobile && npm start
"""

    content = f"""\
.DEFAULT_GOAL := help

.PHONY: help
help:  ## Show available commands
\t@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \\
\t\tawk 'BEGIN {{FS = ":.*?## "}}; {{printf "\\033[36m%-20s\\033[0m %s\\n", $$1, $$2}}'

.PHONY: up
up:  ## Start all services with Docker Compose
\tdocker compose up --build

.PHONY: down
down:  ## Stop all services
\tdocker compose down

.PHONY: dev-server
dev-server:  ## Start backend in development mode
\tcd server && make dev 2>/dev/null || echo "Configure: cd server && <dev command>"

.PHONY: dev-client
dev-client:  ## Start frontend in development mode
\tcd client && npm run dev

.PHONY: test
test:  ## Run all tests
\tcd server && make test 2>/dev/null || echo "Configure server tests"
\tcd client && npm test 2>/dev/null || echo "Configure client tests"

.PHONY: lint
lint:  ## Run linters
\tcd server && make lint 2>/dev/null || echo "Configure server linter"
\tcd client && npm run lint 2>/dev/null || echo "Configure client linter"

.PHONY: clean
clean:  ## Remove build artifacts
\tdocker compose down -v --remove-orphans
{mobile_targets}"""
    write_file(project_dir / "Makefile", content)
