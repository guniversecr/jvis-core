# JVIS

[![Tests](https://github.com/guniversecr/jvis/actions/workflows/tests.yml/badge.svg)](https://github.com/guniversecr/jvis/actions/workflows/tests.yml)
[![Coverage](https://img.shields.io/badge/coverage-87%25-brightgreen)](docs/STATUS.md)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)](https://python.org)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)

**The best way to start an AI-assisted project.**

Scaffold production-ready projects across 17 stacks and give your AI coding assistant a structured development workflow with 10 specialized agent prompts.

## Quick Start

```bash
pip install jvis
```

New project:

```bash
jvis new                                    # interactive
jvis new -n my-api -s python-fastapi -p . -y  # scripted
```

Existing project:

```bash
cd my-existing-project
jvis add .
```

Then open with your AI assistant:

```bash
claude          # or open in Cursor
/dev            # activate the Developer agent prompt
```

## See It In Action

```
$ jvis new

  Project name: my-api
  Project type:
    1) Single-Stack
    2) Full-Stack
    3) Full-Stack + Mobile
    4) SaaS Platform
  Select type [1]: 1

  Select stack:
    1) python-fastapi    — FastAPI + SQLAlchemy
    2) python-django     — Django + DRF
    3) react-vite        — React + Vite + TypeScript
    ...17 stacks available

  Select database:
    1) PostgreSQL
    2) MySQL / MariaDB
    3) DynamoDB

  ✓ Created my-api/
  ✓ Scaffolded python-fastapi (Item CRUD, tests, service layer)
  ✓ Installed 10 agent prompts
  ✓ Ready — open with `claude` or Cursor
```

## What JVIS Does

### 1. Project Scaffolding

`jvis new` generates a working CRUD application with domain models, service layer, routes, and tests. You get running code, not an empty directory.

17 stacks available:

| Stack | Framework | What You Get |
|-------|-----------|-------------|
| `python-fastapi` | FastAPI + SQLAlchemy | Clean Architecture, Pydantic models |
| `python-django` | Django + DRF | ViewSets, UUID models, admin panel |
| `python-flask` | Flask + SQLAlchemy | Blueprints, service layer |
| `nodejs-express` | Express + Prisma | TypeScript, Zod validation |
| `nodejs-nestjs` | NestJS + Prisma | Modules, class-validator |
| `nextjs` | Next.js + Prisma | App Router, React Server Components |
| `react-vite` | React + Vite | TypeScript strict, React Router |
| `vue-vite` | Vue + Vite | Pinia, Vue Router, Composition API |
| `angular` | Angular | Standalone components, signals |
| `php-laravel` | Laravel | Eloquent, HasUuids, API Resources |
| `rust-axum` | Axum + SQLx | Clean Architecture, Tokio async |

Plus `nodejs-fastify`, `nuxt`, `svelte-kit`, `astro`, `php-symfony`, and `custom` (pure Python stdlib).

### 2. Agent Prompt Configurations

JVIS installs 10 specialized agent prompts as slash commands for your AI assistant. Each "agent" is a structured prompt with a defined role, principles, and workflow.

When you type `/dev` in Claude Code, your assistant receives instructions to act as a developer with coding standards, a pre-QA checklist, and story-scoped permissions. JVIS gives your AI better context — it still does the work.

| Command | Role | Purpose |
|---------|------|---------|
| `/pm` | Product Manager | PRD creation, requirements |
| `/architect` | System Architect | Technical design, ADRs |
| `/sm` | Scrum Master | Stories, sprint planning |
| `/dev` | Developer | Implementation, debugging |
| `/qa` | QA Engineer | Testing, quality gates |
| `/api` | Python Backend | FastAPI/Flask specialist |
| `/frontend` | Frontend | React + Vite specialist |
| `/rust` | Rust Backend | Axum + SQLx specialist |
| `/prisma` | Node.js Backend | Prisma ORM specialist |
| `/devsecops` | Security | OWASP audits, DevSecOps |

### 3. Persistent Notes

Agents write structured notes to `docs/notes/` that survive between sessions. Each agent prompt instructs the AI to load context on start and save context on exit. The persistence is a convention enforced by prompts, not by code.

### 4. Quality Workflow

A defined review process: QA reviews code before commits, with risk-based severity levels (PASS/CONCERNS/FAIL). Low-risk changes need self-review, high-risk changes need QA + Architect review.

## How It Compares

| Feature | cookiecutter | create-t3-app | JVIS |
|---------|-------------|---------------|------|
| Project scaffolding | 1 template/repo | T3 only | 17 functional stacks |
| Agent prompts | No | No | 10 role-specific prompts |
| Persistent notes | No | No | File-based, between sessions |
| Quality workflow | No | No | Risk-based review levels |

JVIS adds structure to how you use AI coding assistants. It doesn't replace them.

## Supported Platforms

| Platform | Format | Status |
|----------|--------|--------|
| Claude Code | `.claude/commands/*.md` | Stable |
| Cursor | `.cursor/rules/*.mdc` | Stable |
| Kiro | `.kiro/steering/*.md` | Beta |

## Installation

```bash
pip install jvis
```

Requires **Python 3.12+** and **Git**.

## Documentation

- **[docs/INDEX.md](docs/INDEX.md)** — Navigation hub
- **[docs/STATUS.md](docs/STATUS.md)** — Project state with verified numbers
- **[docs/DEVELOPMENT-WORKFLOW.md](docs/DEVELOPMENT-WORKFLOW.md)** — Agent workflow + plan system

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

Apache License 2.0. See [LICENSE](LICENSE).
