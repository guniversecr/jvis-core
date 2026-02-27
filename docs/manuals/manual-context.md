# Context Management Manual

How agents maintain and share information between sessions.

---

## Concept

AI agents do not have persistent memory. The context system provides file-based notes that agents can save and load manually using `*load-context` and `*save-context` commands. This is convention-based — if the commands are skipped, context is lost.

---

## Context Commands

| Command | When it runs | What it does |
|---------|-------------------|----------|
| `*load-context` | Automatically when starting an agent | Loads project state |
| `*save-context` | Automatically with `*exit` | Saves session progress |

---

## Automatic Flow

```
Start agent (/dev, /qa, etc.)
         |
         v
   *load-context (automatic)
   - Reads project-log.md
   - Reads relevant notes
   - Shows summary
         |
         v
   [Your normal work]
         |
         v
   *exit (your command)
         |
         v
   *save-context (automatic)
   - Updates project-log.md
   - Writes notes for other agents
   - Records decisions
```

---

## File Structure

```
docs/notes/
├── project-log.md       # Central state (TTL 7 days)
├── lessons-learned.md   # Permanent lessons
├── next-action.md       # Next priority action
├── from-analyst.md      # Analyst notes
├── from-pm.md           # PM notes
├── from-architect.md    # Architect notes
├── from-dev.md          # Developer notes
├── from-qa.md           # QA notes
├── from-devsecops.md    # Security notes
├── from-sm.md           # Scrum master notes
├── from-po.md           # Product owner notes
└── from-ux.md           # UX expert notes
```

---

## project-log.md

Central file with project state:

```markdown
# Project Log

## Current State
- Phase: Development
- Active Story: 1.2 - JWT Authentication
- Last agent: /dev

## Recent History
### 2025-01-15
- [dev] Implemented login endpoint
- [qa] Pending test review

## Decisions
- Use bcrypt for passwords
- JWT expires in 24h
```

---

## from-*.md (Agent Notes)

Each agent writes notes for others:

```markdown
# Notes from Dev -> Other Agents

## For QA
- Integration tests pending in /auth
- DB mock configured

## For Architect
- Found inconsistency in sequence diagram
```

---

## lessons-learned.md

Permanent lessons (do not expire):

```markdown
# Lessons Learned

## Technical
- Use transactions for multi-table operations
- Validate input in controller, not in service

## Process
- Make small PRs, easy to review
```

---

## Best Practices

1. **Always use `*exit`** - Never close without saving context
2. **Read the notes** - When starting, review what other agents left behind
3. **Write for others** - Document what the next agent needs to know
4. **Use lessons-learned** - For recurring patterns

---

## Recovering Lost Context

If you forgot to use `*exit`:

```bash
/Custom:project-resume
```

This command reconstructs the context from existing files.

---

See manual-agentes.md and manual-workflows.md for more information.
