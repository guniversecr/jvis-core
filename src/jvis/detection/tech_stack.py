"""Detect the technology stack of an existing project and recommend agents."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class StackDetection:
    """Result of tech-stack detection."""

    languages: list[str] = field(default_factory=list)
    frameworks: list[str] = field(default_factory=list)
    databases: list[str] = field(default_factory=list)
    recommended_agents: list[str] = field(default_factory=list)

    @property
    def summary(self) -> str:
        parts = self.languages + self.frameworks
        return ", ".join(parts) if parts else "unknown"


# Mapping: (file-to-check, language/framework label, stack-type)
_FILE_INDICATORS: list[tuple[str, str, str]] = [
    # Python
    ("pyproject.toml", "python", "lang"),
    ("setup.py", "python", "lang"),
    ("requirements.txt", "python", "lang"),
    ("Pipfile", "python", "lang"),
    # Node.js
    ("package.json", "node", "lang"),
    ("yarn.lock", "node", "lang"),
    ("pnpm-lock.yaml", "node", "lang"),
    # Rust
    ("Cargo.toml", "rust", "lang"),
    # Go
    ("go.mod", "go", "lang"),
    # Ruby
    ("Gemfile", "ruby", "lang"),
    # PHP
    ("composer.json", "php", "lang"),
    # Java/Kotlin
    ("pom.xml", "java", "lang"),
    ("build.gradle", "java", "lang"),
    ("build.gradle.kts", "kotlin", "lang"),
    # Swift
    ("Package.swift", "swift", "lang"),
    # Docker
    ("Dockerfile", "docker", "tool"),
    ("docker-compose.yml", "docker", "tool"),
    ("docker-compose.yaml", "docker", "tool"),
    # Terraform
    ("main.tf", "terraform", "tool"),
]

# Content-based framework detection (file, substring, framework)
_CONTENT_INDICATORS: list[tuple[str, str, str]] = [
    ("pyproject.toml", "fastapi", "fastapi"),
    ("pyproject.toml", "flask", "flask"),
    ("pyproject.toml", "django", "django"),
    ("requirements.txt", "fastapi", "fastapi"),
    ("requirements.txt", "flask", "flask"),
    ("requirements.txt", "django", "django"),
    ("package.json", "react", "react"),
    ("package.json", "vue", "vue"),
    ("package.json", "angular", "angular"),
    ("package.json", "next", "nextjs"),
    ("package.json", "express", "express"),
    ("package.json", "prisma", "prisma"),
    ("package.json", "expo", "expo"),
    ("Cargo.toml", "axum", "axum"),
    ("Cargo.toml", "actix", "actix"),
]

# Database detection (file, substring, database name)
_DB_INDICATORS: list[tuple[str, str, str]] = [
    ("docker-compose.yml", "postgres", "postgresql"),
    ("docker-compose.yaml", "postgres", "postgresql"),
    ("docker-compose.yml", "mysql", "mysql"),
    ("docker-compose.yaml", "mysql", "mysql"),
    ("docker-compose.yml", "mongo", "mongodb"),
    ("docker-compose.yaml", "mongo", "mongodb"),
    ("docker-compose.yml", "redis", "redis"),
    ("docker-compose.yaml", "redis", "redis"),
    (".env", "DATABASE_URL", "detected"),
    ("prisma/schema.prisma", "postgresql", "postgresql"),
    ("prisma/schema.prisma", "mysql", "mysql"),
    ("prisma/schema.prisma", "sqlite", "sqlite"),
]

# Agent recommendations by detected tech
_AGENT_MAP: dict[str, list[str]] = {
    "python": ["api", "dev", "qa"],
    "fastapi": ["api"],
    "flask": ["api"],
    "node": ["prisma", "dev", "qa"],
    "express": ["prisma"],
    "prisma": ["prisma"],
    "react": ["frontend"],
    "vue": ["frontend"],
    "angular": ["frontend"],
    "nextjs": ["frontend"],
    "rust": ["rust", "dev", "qa"],
    "axum": ["rust"],
    "kotlin": ["dev"],
    "swift": ["dev"],
    "docker": ["docker"],
    "terraform": ["infra"],
    "expo": ["dev"],
}

# Always recommended (core workflow agents)
_CORE_AGENTS = ["pm", "architect", "sm", "dev", "qa", "devsecops", "master"]


def _scan_directory(
    directory: Path,
    result: StackDetection,
    seen: set[str],
    db_seen: set[str],
) -> None:
    """Scan a single directory for tech-stack indicators."""
    # File-based detection
    for filename, label, kind in _FILE_INDICATORS:
        if (directory / filename).is_file() and label not in seen:
            seen.add(label)
            if kind == "lang":
                result.languages.append(label)
            else:
                result.frameworks.append(label)

    # Content-based framework detection
    for filename, substring, framework in _CONTENT_INDICATORS:
        filepath = directory / filename
        if filepath.is_file() and framework not in seen:
            try:
                content = filepath.read_text(errors="ignore").lower()
                if substring in content:
                    seen.add(framework)
                    result.frameworks.append(framework)
            except (PermissionError, OSError) as exc:
                logger.debug("Cannot read %s for framework detection: %s", filepath, exc)
                continue

    # Database detection
    for filename, substring, db_name in _DB_INDICATORS:
        filepath = directory / filename
        if filepath.is_file() and db_name not in db_seen:
            try:
                content = filepath.read_text(errors="ignore").lower()
                if substring.lower() in content:
                    db_seen.add(db_name)
                    result.databases.append(db_name)
            except (PermissionError, OSError) as exc:
                logger.debug("Cannot read %s for database detection: %s", filepath, exc)
                continue


def detect_tech_stack(target: Path) -> StackDetection:
    """Analyze a project directory and return detected technologies.

    Scans the root directory and immediate subdirectories (1 level deep)
    to support monorepo layouts like ``backend/pyproject.toml``.
    """
    result = StackDetection()
    seen: set[str] = set()
    db_seen: set[str] = set()

    # Check root directory
    _scan_directory(target, result, seen, db_seen)

    # Check immediate subdirectories (monorepo support)
    try:
        subdirs = sorted(target.iterdir())
    except (PermissionError, OSError):
        subdirs = []
    for subdir in subdirs:
        if subdir.is_dir() and not subdir.name.startswith("."):
            _scan_directory(subdir, result, seen, db_seen)

    # Build agent recommendations
    agent_set: set[str] = set(_CORE_AGENTS)
    for tech in seen:
        for agent in _AGENT_MAP.get(tech, []):
            agent_set.add(agent)
    result.recommended_agents = sorted(agent_set)

    return result


def detect_project_type(target: Path) -> str:
    """Detect project type from directory structure.

    Returns: single, fullstack, fullstack-mobile, or saas-platform.
    Recognizes both server/client and backend/frontend naming conventions.
    """
    has_server = (target / "server").is_dir() or (target / "backend").is_dir()
    has_client = (target / "client").is_dir() or (target / "frontend").is_dir()
    has_mobile = (target / "mobile").is_dir()
    has_infra = (target / "infra").is_dir() or (target / "infrastructure").is_dir()

    if has_server and has_client and has_mobile:
        return "fullstack-mobile"
    if has_server and has_client and has_infra:
        return "saas-platform"
    if has_server and has_client:
        return "fullstack"
    return "single"
