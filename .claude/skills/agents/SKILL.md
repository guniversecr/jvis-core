# Agents Skill

Knowledge for working with the JVIS parametric agent system.

## Architecture Overview

JVIS agents are **YAML configs** rendered to markdown via Jinja2 templates. The agent engine generates platform-specific output (Claude Code slash commands, Cursor rules).

```
.jvis/agents/           # 68 YAML configs (source of truth)
  core/                 # dev.yaml, qa.yaml, architect.yaml, pm.yaml, sm.yaml, ...
  marketing/            # 14 agents
  mobile/               # 5 agents
  ...
.jvis/agent-engine/
  engine.py             # Core generator (~220 lines)
  templates/
    claude.md           # Claude Code output template (Jinja2)
    cursor.md           # Cursor rules output template (Jinja2)
  schemas/
    agent.schema.yaml   # YAML schema definition

# Generated output (DO NOT EDIT):
.claude/commands/       # 68 .md files (Claude Code slash commands)
.cursor/rules/          # 68 .mdc files (Cursor rules)
```

## Agent YAML Schema

Required fields: `id`, `name`, `title`, `tier`, `pack`, `persona`, `commands`

```yaml
agent:
  id: dev                    # Lowercase, /command name
  name: James                # Persona name
  title: Full Stack Developer
  tier: free                 # free|pro|teams
  pack: core                 # Extension pack
  status: active             # active|draft

persona:
  role: "Description"
  style: "Communication style"
  identity: "Self-description"
  focus: "What agent prioritizes"
  core_principles:
    - "Principle 1"

commands:
  - help: "Show commands"
  - load-context: "Load project context (task load-context.md)"
  - custom-command: "Description"

dependencies:
  tasks:
    - load-context.md        # Maps to .jvis/tasks/load-context.md
  templates:
    - story-tmpl.yaml
  checklists:
    - story-dod-checklist.md

inter_agent:
  writes_to: docs/notes/from-dev.md
  reads_from:
    - docs/notes/project-log.md
    - docs/notes/from-qa.md
  handoff:
    - agent: /qa
      purpose: "Code ready for review"
```

See: `.jvis/agent-engine/schemas/agent.schema.yaml` for complete schema

## Agent Tiers

| Tier | Agents | Description |
|------|--------|-------------|
| **Battle-tested** (~8) | dev, qa, architect, pm, sm, api, prisma, master | Real workflows with tested tasks |
| **Functional prompts** (~12) | analyst, frontend, rust, infra, docker, devsecops, ... | Good persona, useful as prompts |
| **Config templates** (~48) | Most marketing, specialty agents | YAML defined, no tested workflows |

## Engine Workflow

Generate all agents: `python3 .jvis/agent-engine/engine.py generate-all --platform all`

1. Engine reads all `.yaml` files from `.jvis/agents/`
2. Skips `draft` status agents (unless `--include-drafts`)
3. For each agent + platform:
   - Loads YAML config
   - Renders through platform template (claude.md or cursor.md)
   - Writes output to platform directory
4. Reports generation stats

## Inter-Agent Communication Protocol

Agents communicate via markdown files in `docs/notes/`:

| File | Writer | Purpose |
|------|--------|---------|
| `from-dev.md` | /dev | Implementation notes, tech decisions |
| `from-qa.md` | /qa | Review findings, gate decisions |
| `from-architect.md` | /architect | Architecture decisions, ADRs |
| `from-pm.md` | /pm | PRD updates, epic scope |
| `from-sm.md` | /sm | Story assignments, sprint updates |
| `project-log.md` | All | Centralized project state |
| `lessons-learned.md` | All | Permanent knowledge base |

**Protocol:** Every agent runs `*load-context` on activation (reads project-log + relevant from-*.md files) and `*save-context` before exit (writes updates).

## Adding a New Agent

1. Create YAML config in `.jvis/agents/{pack}/{id}.yaml`
2. Follow schema: id, name, title, tier, pack, persona, commands
3. Set `status: active` (or `draft` for WIP)
4. Run `make generate` to render output files
5. Test: verify `.claude/commands/{id}.md` exists and renders correctly

## Common Commands (All Agents)

All agents share these base commands via the template:
- `*help` — show commands
- `*load-context` — load project context
- `*save-context` — save session state
- `*exit` — save context then exit
