# Tutorial 1: Create a Project From Scratch

## Objective

Create a new project with JVIS, including the entire structure needed for professional development.

## Prerequisites

- [ ] JVIS installed globally (`jvis version` works)
- [ ] Git installed
- [ ] Claude Code installed
- [ ] (Optional) Docker for database

## Estimated time: 5 minutes

---

## Step 1: Start the Wizard

```bash
jvis new
```

You will see the stack selection menu with 17 available stacks:

```
╔═══════════════════════════════════════════════════════════╗
║            JVIS - New Project                            ║
╠═══════════════════════════════════════════════════════════╣
║  Select the stack:                                        ║
║                                                           ║
║  Python Backend:                                          ║
║    1) python-fastapi    - FastAPI + SQLAlchemy            ║
║    2) python-django     - Django + DRF                    ║
║    3) python-flask      - Flask + SQLAlchemy              ║
║                                                           ║
║  Node.js Backend:                                         ║
║    4) nodejs-express    - Express + Prisma                ║
║    5) nodejs-nestjs     - NestJS + Prisma                 ║
║    6) nodejs-fastify    - Fastify + Prisma                ║
║                                                           ║
║  Full-Stack:                                              ║
║    7) nextjs            - Next.js + Prisma                ║
║    8) nuxt              - Nuxt + Vue                      ║
║                                                           ║
║  Frontend:                                                ║
║    9) react-vite        - React + Vite                    ║
║   10) vue-vite          - Vue + Vite                      ║
║   11) angular           - Angular standalone              ║
║   12) svelte-kit        - SvelteKit                       ║
║   13) astro             - Astro                           ║
║                                                           ║
║  Other:                                                   ║
║   14) php-laravel       - Laravel + Eloquent              ║
║   15) php-symfony       - Symfony                         ║
║   16) rust-axum         - Axum + SQLx + Tokio             ║
║   17) custom            - Pure Python stdlib              ║
╚═══════════════════════════════════════════════════════════╝
```

## Step 2: Configure the Project

Answer the prompts:

```
Project name: my-api
Selected stack: 1 (python-fastapi)
Database: 1 (PostgreSQL)
Initialize Git: y
```

## Step 3: Verify the Created Structure

```bash
cd my-api
tree -L 2
```

You should see:

```
my-api/
├── .jvis/
│   ├── agents/
│   ├── templates/
│   ├── tasks/
│   └── core-config.yaml
├── .claude/
│   └── commands/
├── .cursor/
│   └── rules/
├── docs/
│   ├── notes/
│   ├── prd.md
│   └── architecture.md
├── src/
│   ├── domain/
│   ├── application/
│   └── infrastructure/
├── tests/
├── pyproject.toml
└── README.md
```

## Step 4: Start the Database (Optional)

If you selected PostgreSQL:

```bash
docker-compose up -d db
```

## Step 5: Verify Available Agents

```bash
# Open Claude Code
claude

# Verify that commands are available
> /pm --help
> /dev --help
> /qa --help
```

---

## Verification

- [ ] Project directory created
- [ ] `.jvis/` structure present
- [ ] Slash commands working in Claude Code
- [ ] Git initialized (`git status` shows a clean repo)

## Common Problems

### "jvis: command not found"

```bash
# Install from PyPI
pip install jvis

# Or if you installed in a virtual environment, make sure it's activated
source .venv/bin/activate
```

### "No module named jvis"

```bash
# Ensure Python 3.12+ is installed
python3 --version

# Reinstall
pip install --upgrade jvis
```

---

## Next Step

Continue with [Tutorial 2: Your First Agent Session](02-first-agent-session.md) to understand how agents work before diving into a full cycle.
