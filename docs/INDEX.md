# Documentation Index

Start here. This page routes you to the right document based on what you need.

## If you are...

### A new user
1. [README.md](../README.md) — What JVIS is, quick start, installation
2. [QUICKSTART.md](QUICKSTART.md) — Step-by-step first project

### A contributor
1. [CONTRIBUTING.md](../CONTRIBUTING.md) — How to contribute
2. [DEVELOPMENT-WORKFLOW.md](DEVELOPMENT-WORKFLOW.md) — Agent sequence, plan system, quality gates
3. [STATUS.md](STATUS.md) — Honest project state, what's done, what's not
4. [notes/lessons-learned.md](notes/lessons-learned.md) — Solved problems (read before debugging)

### An AI agent working on this repo
1. [../CLAUDE.md](../CLAUDE.md) — Principles, agents, stacks, plan system, build commands
2. [DEVELOPMENT-WORKFLOW.md](DEVELOPMENT-WORKFLOW.md) — Full workflow with plan system (ADR-005/006)

---

## Document Map

### Root files
| File | Purpose |
|------|---------|
| [README.md](../README.md) | Project overview, quick start |
| [CLAUDE.md](../CLAUDE.md) | Instructions for AI agents (principles, workflow, stacks) |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | Contribution guidelines |
| [SECURITY.md](../SECURITY.md) | Security policy |
| [CHANGELOG.md](../CHANGELOG.md) | Version history |

### Core docs (`docs/`)
| File | Purpose | Audience |
|------|---------|----------|
| [STATUS.md](STATUS.md) | Honest maturity assessment with verified numbers | Everyone |
| [DEVELOPMENT-WORKFLOW.md](DEVELOPMENT-WORKFLOW.md) | Agent workflow + plan system | Contributors, agents |
| [QUICKSTART.md](QUICKSTART.md) | First project walkthrough | New users |
| [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md) | Release process | Maintainers |
| [PYPI-PUBLISH-GUIDE.md](PYPI-PUBLISH-GUIDE.md) | PyPI publishing | Maintainers |

### Architecture Decisions (`docs/adr/`)
| ADR | Decision |
|-----|----------|
| [ADR-001](adr/ADR-001-core-principles-and-agent-improvements.md) | Core principles: honesty, SSOT, SOLID, Clean Architecture |
| [ADR-002](adr/ADR-002-functional-stack-scaffolding.md) | Functional stack scaffolding (Python stacks) |
| [ADR-003](adr/ADR-003-functional-scaffolds-nodejs-react.md) | Functional scaffolds (Node.js, React, PHP, Rust) |
| [ADR-004](adr/ADR-004-quality-hardening-architecture.md) | Quality hardening architecture |
| [ADR-005](adr/ADR-005-executable-development-plans.md) | Plan system: executable plans, risk-based gates |
| [ADR-006](adr/ADR-006-plan-migration-on-update.md) | Plan migration on JVIS update |
| [ADR-007](adr/ADR-007-version-management.md) | Version management: mandatory bumps, 3-tier SSOT |

### Notes (`docs/notes/`)
| File | Purpose |
|------|---------|
| [lessons-learned.md](notes/lessons-learned.md) | Permanent knowledge base of solved problems |
| [project-log.md](notes/project-log.md) | Timeline of decisions and events |

### Templates
| File | Status |
|------|--------|
| [prd.md](prd.md) | Template stub (populated by `/pm` agent) |
| [architecture.md](architecture.md) | Template stub (populated by `/architect` agent) |
