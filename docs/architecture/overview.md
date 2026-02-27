# JVIS Architecture Overview

> **Current state & metrics:** `docs/STATUS.md` (SSOT)

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     JVIS Framework                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │    Agents    │  │   Templates  │  │    Stacks    │      │
│  │   (YAML)    │  │  (Jinja2)    │  │  (manifest)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                 │                 │               │
│         └─────────────────┼─────────────────┘               │
│                           │                                 │
│  ┌────────────────────────▼────────────────────────┐       │
│  │              Core Configuration                  │       │
│  │          (.jvis/core-config.yaml)                │       │
│  └──────────────────────────────────────────────────┘       │
│                           │                                 │
│  ┌────────────────────────▼────────────────────────┐       │
│  │              Python CLI (Click)                   │       │
│  │          (src/jvis/cli.py)                        │       │
│  └──────────────────────────────────────────────────┘       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

See `docs/architecture/source-tree.md` for detailed tree.

## Key Design Principles

### 1. Single Source of Truth

- Agents: `.jvis/agents/` only (YAML configs)
- Templates: `.jvis/templates/` only
- Commands: `.claude/commands/` only (generated — DO NOT EDIT)
- Stacks: `src/jvis/data/stacks/` only
- Project state: `docs/STATUS.md` only

### 2. Agent Standardization

All agents follow YAML-first format, rendered to markdown via Jinja2:

```yaml
activation-instructions:
  - Step 1: Read entire file
  - Step 2: Adopt persona
  - Step 3: Load config
  - Step 4: Greet user
agent:
  name: AgentName
  id: agent-id
  title: Full Title
  tier: free|pro
persona:
  role: Description
  style: Communication style
commands:
  - help: Show commands
  - task: Do something
dependencies:
  tasks: [...]
  templates: [...]
```

### 3. Inter-Agent Communication

Agents communicate through shared notes:

```
docs/notes/
├── project-log.md       # Activity history (TTL 7 days)
├── lessons-learned.md   # Permanent lessons
├── from-dev.md          # Dev -> other agents
├── from-qa.md           # QA -> other agents
└── from-architect.md    # Architect -> other agents
```

## Data Flow

```
User Request
     │
     ▼
┌─────────┐     ┌──────────┐     ┌──────────┐
│  Agent  │────>│ Templates│────>│  Output  │
└─────────┘     └──────────┘     └──────────┘
     │                                 │
     ▼                                 ▼
┌─────────┐                      ┌──────────┐
│  Notes  │<────────────────────│  Docs    │
└─────────┘                      └──────────┘
```

## Quality Assurance

```
┌─────────────────────────────────────────┐
│            CI/CD Pipeline               │
├─────────────────────────────────────────┤
│  Unit Tests │ Integration │  Lint/Type  │
│  (pytest)   │  (scaffold) │  (Ruff/MyPy)│
└─────────────────────────────────────────┘
```
