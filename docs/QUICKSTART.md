# JVIS Quick Start

Get running in 5 minutes.

---

## Install

```bash
pip install jvis
```

Requires Python 3.12+ and Git.

---

## Create a New Project

```bash
# Interactive
jvis new

# Scripted
jvis new -n my-api -s python-fastapi -p . -y
```

### What You Get

A working project with domain models, service layer, routes, and tests:

```
my-api/
  src/
    domain/          # Entities, business rules
    use_cases/       # Application logic
    infrastructure/  # Database, external services
    controllers/     # REST endpoints
  tests/
  pyproject.toml
  README.md
```

---

## Add JVIS to an Existing Project

```bash
cd my-existing-project
jvis add .
```

This installs the agent system (`.jvis/`, `.claude/commands/`) without touching your code.

---

## Start Developing with AI Agents

```bash
# Open your AI assistant
claude          # or open in Cursor

# Activate an agent
/dev            # Developer agent
```

### The Development Cycle

```
/pm         → Create PRD              "What are we building?"
/architect  → Design architecture     "How do we build it?"
/sm         → Break into stories      "What are the tasks?"
/dev        → Implement               "Write the code"
/qa         → Quality gate            "Is it good enough?"
             → Commit (only after QA PASS)
```

### Agent Commands

Once inside an agent session, use `*` prefix:

```
*help           # Show available commands
*load-context   # Load project context (auto on start)
*save-context   # Save session work (mandatory before exit)
*exit           # Leave agent (runs save-context first)
```

---

## Available Stacks

### Backend

| Stack | Framework | What You Get |
|-------|-----------|-------------|
| `python-fastapi` | FastAPI + SQLAlchemy | Clean Architecture, Pydantic models |
| `python-django` | Django + DRF | ViewSets, UUID models, admin panel |
| `python-flask` | Flask + SQLAlchemy | Blueprints, service layer |
| `nodejs-express` | Express + Prisma | TypeScript, Zod validation |
| `nodejs-nestjs` | NestJS + Prisma | Modules, class-validator |
| `nodejs-fastify` | Fastify + Prisma | JSON Schema, domain entities |
| `rust-axum` | Axum + SQLx | Clean Architecture, Tokio async |
| `php-laravel` | Laravel | Eloquent, HasUuids, API Resources |
| `php-symfony` | Symfony + Doctrine | Route attributes, WebTestCase |

### Frontend

| Stack | Framework | What You Get |
|-------|-----------|-------------|
| `react-vite` | React + Vite | TypeScript strict, React Router |
| `vue-vite` | Vue + Vite | Pinia, Vue Router, Composition API |
| `angular` | Angular | Standalone components, signals |
| `svelte-kit` | SvelteKit | Svelte stores, fetch API |
| `nextjs` | Next.js + Prisma | App Router, React Server Components |
| `nuxt` | Nuxt + Prisma | Server API routes, Vue composables |
| `astro` | Astro + Preact | Content-first, islands architecture |

### Other

| Stack | Description |
|-------|-------------|
| `custom` | Minimal — JVIS agent system only, no framework |

---

## Workflows

```
/workflows:doc-init           # Initialize docs structure
/workflows:doc-update         # Update project documentation
/workflows:doc-daily          # Daily checkpoint
/workflows:project-resume     # Recover context after a break
/workflows:security-plan      # OWASP security plan
/workflows:security-audit     # Security audit
```

---

## Full Example

```bash
# 1. Create project
jvis new -n todo-api -s python-fastapi -p . -y

# 2. Set up
cd todo-api
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 3. Open AI assistant and develop
claude
/pm              # Create PRD
/architect       # Design architecture
/sm              # Create stories
/dev             # Start development
/qa              # Quality gate before commit
```

---

## Supported Platforms

| Platform | Format | Status |
|----------|--------|--------|
| Claude Code | `.claude/commands/*.md` | Stable |
| Cursor | `.cursor/rules/*.mdc` | Stable |
| Kiro | `.kiro/steering/*.md` | Beta |

---

## Tips

1. Start a new chat when switching agents
2. Always use `*exit` to end sessions (saves context)
3. Use `/workflows:project-resume` when resuming after a break
4. Commit only after QA approval

See [README.md](../README.md) for full documentation.
