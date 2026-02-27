# Tutorial 2: Your First Agent Session

## Objective

Understand how JVIS agents work by running one simple session with the PM agent.

## Prerequisites

- [ ] JVIS project created (Tutorial 1)
- [ ] Claude Code open in the project

## Estimated time: 10 minutes

---

## What Are Agents?

JVIS agents are **specialized AI personas** — not generic code generators. Each agent has:

- **A role** — PM thinks about product, Architect thinks about systems, Dev writes code
- **Commands** — Each agent has specific commands prefixed with `*` (e.g., `*create-prd`)
- **Memory** — Agents read and write files in `docs/notes/` to pass context between sessions
- **Handoffs** — Each agent produces artifacts the next agent needs

Think of them as team members who communicate through documents.

## The Workflow (and Why It Matters)

```
/pm → /architect → /sm → /dev → /qa → commit
```

**Why not just run `/dev`?** Because context. The Dev agent needs stories to implement. Stories need architecture decisions. Architecture needs a PRD defining what to build. Skipping steps means the agent has to guess — and guesses lead to rework.

Each agent builds on the previous one's output:

| Agent | Reads | Produces |
|-------|-------|----------|
| `/pm` | Your idea | PRD (`docs/prd.md`) |
| `/architect` | PRD | Architecture doc (`docs/architecture.md`) |
| `/sm` | PRD + Architecture | Stories + execution plan (`docs/plans/`) |
| `/dev` | Stories + plan | Code + step reports |
| `/qa` | Code + stories | Quality verdict (PASS / CONCERNS / FAIL) |

---

## Step 1: Activate the PM Agent

In Claude Code, type:

```bash
/pm
```

You will see the agent's greeting with its role and available commands. The agent is now "loaded" — Claude is acting as a Product Manager.

## Step 2: Explore Available Commands

```bash
*help
```

This shows all commands the PM agent supports. Every JVIS agent responds to these universal commands:

| Command | Purpose |
|---------|---------|
| `*help` | List available commands |
| `*load-context` | Load project context (runs automatically on start) |
| `*save-context` | Save session state to `docs/notes/` |
| `*exit` | Save context and leave agent mode |

The PM also has specific commands like `*create-prd`, `*create-brief`, and others.

## Step 3: Create a Quick PRD

```bash
*create-prd
```

The PM agent will ask you questions about your product:
- What problem are you solving?
- Who are the users?
- What are the core features?

Answer naturally — the agent will structure your answers into a professional PRD document at `docs/prd.md`.

> **Tip:** You don't need a detailed vision yet. Even "I want a task management API with CRUD operations" is enough to get started.

## Step 4: Save and Exit

```bash
*exit
```

This does two things:
1. **Saves context** — writes a summary to `docs/notes/from-pm.md` so other agents can pick up where PM left off
2. **Exits agent mode** — returns Claude to normal operation

## Step 5: Verify What Was Created

Check the files the PM agent generated:

```bash
ls docs/
```

You should see:
- `docs/prd.md` — the PRD document
- `docs/notes/from-pm.md` — the inter-agent handoff note

The handoff note is how agents communicate. When you later run `/architect`, it will read `from-pm.md` to understand what PM decided.

---

## Key Takeaways

1. **Agents are personas, not tools** — they think within their role's scope
2. **`*` commands are universal** — `*help`, `*exit`, `*save-context` work in every agent
3. **`docs/notes/` is the shared memory** — agents read each other's notes for continuity
4. **The workflow order matters** — PM → Architect → SM → Dev → QA, each building on the last

---

## Next Step

Continue with [Tutorial 3: Complete Development Cycle](03-development-cycle.md) to walk through the full PM → Architect → Dev → QA cycle and commit your first feature.
