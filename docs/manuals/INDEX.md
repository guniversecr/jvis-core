# JVIS - Documentation Index

> **Current state & metrics:** `docs/STATUS.md` (SSOT)

---

## Tutorials

| Tutorial | Objective |
|----------|-----------|
| [01-create-project.md](tutorials/01-create-project.md) | Create a project from scratch |
| [02-first-agent-session.md](tutorials/02-first-agent-session.md) | Your first agent session |
| [03-development-cycle.md](tutorials/03-development-cycle.md) | Complete cycle PM -> Dev -> QA |

---

## Topic Manuals

| Manual | Topic |
|--------|-------|
| [manual-templates.md](manual-templates.md) | Template system |
| [manual-context.md](manual-context.md) | Context management |

---

## Quick Reference

### CLI Commands
```bash
jvis new              # Create project
jvis add <path>       # Add to existing project
jvis update <path>    # Update existing project
jvis bump patch       # Bump version
jvis version          # Show version
jvis pipeline         # CI/CD templates
jvis hooks            # List hooks
```

### Core Agents
```bash
/pm          # Product Manager — PRDs, requirements
/architect   # System Architect — technical design, ADRs
/sm          # Scrum Master — stories, sprint planning
/dev         # Developer — implementation
/qa          # QA Architect — testing, quality gates
```

### Stack Specialist Agents
```bash
/api         # Python backend specialist
/frontend    # React/Vue/Angular specialist
/prisma      # Node.js + Prisma specialist
/rust        # Rust + Axum specialist
```

### Security Agent
```bash
/devsecops   # Security planning, OWASP audits
```

### Agent Commands
```bash
*help        # Show help
*load-context # Load project context
*save-context # Save session
*exit        # Exit (saves context first)
```

---

## Support

- **Issues:** https://github.com/your-org/jvis/issues
- **Project state:** `docs/STATUS.md`
