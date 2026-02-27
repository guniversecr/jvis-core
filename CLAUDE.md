# CLAUDE.md — JVIS (Public)

## Quick Start

```bash
pip install jvis && jvis new
```

## Core DNA: Pragmatism & Evidence-Based Engineering

1. **Be Pragmatic** — Recommend what works, not what's trendy
2. **Be Objective** — Evaluate with data and evidence, not opinion
3. **Use World-Class Standards** — OWASP, 12-Factor, SOLID, RFC — cite sources
4. **Validate, Don't Trust** — Cross-reference all data against actual project state
5. **Show Your Work** — Explain WHY with trade-offs and alternatives

### Mandatory Engineering Principles
- **SSOT** — Every piece of data has ONE canonical location
- **SOLID** — Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion
- **Clean Architecture** — Separation by layers. Dependencies point inward.
- **Clean Code** — Descriptive names, small functions, DRY, no magic numbers, no dead code
- **KISS** — Simplest solution that solves the actual problem
- **YAGNI** — Don't build for hypothetical futures

## Agent System

Agent YAML configs in `.jvis/agents/`, rendered to markdown via Jinja2 templates.

### Agents (10 total)

| Command | Agent | Purpose |
|---------|-------|---------|
| `/pm` | Product Manager | PRD creation, requirements |
| `/architect` | System Architect | Technical design, ADRs |
| `/sm` | Scrum Master | Story management, sprint planning |
| `/dev` | Developer | Implementation, debugging |
| `/qa` | QA Engineer | Testing, quality gates |
| `/api` | Python Backend | FastAPI/Flask specialist |
| `/frontend` | Frontend | React + Vite specialist |
| `/rust` | Rust Backend | Axum + SQLx specialist |
| `/prisma` | Node.js Backend | Prisma ORM specialist |
| `/devsecops` | Security | OWASP audits, DevSecOps |

## Agent Commands

All agents support (use `*` prefix):

```bash
*help          # Show available commands
*load-context  # Load project context (auto on start)
*save-context  # Save session (mandatory before exit)
*exit          # Leave agent mode (runs save-context first)
```

## Stack Requirements

| Stack | Requirements |
|-------|-------------|
| Python* | 3.12+, pyproject.toml, Ruff, MyPy strict |
| React* | Vite (not CRA), Yarn, TypeScript strict |
| Node.js* | 20+ LTS, TypeScript, Prisma |
| Rust* | 1.75+, Axum, SQLx, Tokio |
| Kotlin | 1.9+, Jetpack Compose, Hilt |
| Swift | 5.9+, SwiftUI, SwiftData |

## Build Commands

`make install` | `make test` | `make lint` | `make audit` | `make typecheck` | `make verify` | `make generate`

## Best Practices

1. Start new chat when switching agents
2. Always use `*exit` to end sessions (saves context)
3. Commit only after QA approval

## Development Workflow

```
1. /pm          → Create PRD
2. /architect   → Design architecture
3. /sm          → Create stories
4. /dev         → Implement stories
5. /qa          → Quality gate per story
6. Commit only after QA PASS
```

## References

- **Start here:** `docs/INDEX.md`
- **Workflow:** `docs/DEVELOPMENT-WORKFLOW.md`
- Agent Schema: `.jvis/agent-engine/schemas/agent.schema.yaml`

Apache License 2.0.
