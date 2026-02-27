# JVIS Agents

This directory contains the **YAML configuration files** for all 15 JVIS agents, organized by pack.

## Architecture: Single Source of Truth

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AGENT FLOW                                   │
│                                                                      │
│   .jvis/agents/{pack}/*.yaml    ──►    engine.py    ──►    .jvis/generated/*.md
│   (SOURCE - edit these)              (generates)         (USED by commands)
│                                                                      │
│                                                           ▼          │
│                                                  .claude/commands/   │
│                                                  (loads generated)   │
└─────────────────────────────────────────────────────────────────────┘
```

**Important:**
- **Edit YAML files** in this directory to modify agents
- **Never edit** files in `.jvis/generated/` directly
- After editing YAML, run `make generate`

## Directory Structure

```
agents/
├── core/           # 11 agents (dev, qa, architect, pm, sm, api, prisma, master, analyst, frontend, rust)
├── marketing/      # 1 agent (strategist)
├── security/       # 2 agents (devsecops, pentest)
└── specialty/      # 1 agent (po)
```

## Agent YAML Schema

Each agent is defined with:

```yaml
id: agent-id           # Unique identifier (used in /command)
name: AgentName        # Display name
title: Job Title       # Role title
icon: "🤖"             # Emoji icon
whenToUse: "..."       # When to invoke this agent

pack: core|marketing|... # Which pack this belongs to
enabled: true          # Whether agent is active

persona:
  role: "..."          # Primary function
  style: "..."         # Communication style
  identity: "..."      # How the agent sees itself
  focus: "..."         # What the agent prioritizes
  core_principles:     # Operating guidelines
    - "Principle 1"
    - "Principle 2"

commands:              # Agent-specific commands
  - command-name: "description"

dependencies:          # Required files
  checklists: []
  tasks: []
  templates: []

inter_agent:           # Communication with other agents
  writes_to: "path"
  reads_from: []
  handoff: []
```

## Regenerating Agents

```bash
# Generate all agents
make generate

# Generate single agent
python .jvis/agent-engine/engine.py generate dev

# Validate agent config
python .jvis/agent-engine/engine.py validate dev

# List all agents
python .jvis/agent-engine/engine.py list
```

## Adding a New Agent

1. Create YAML file in appropriate pack directory
2. Follow schema in `.jvis/agent-engine/schemas/agent.schema.yaml`
3. Add task files for all custom commands in `.jvis/tasks/`
4. Run `make generate`
5. Verify the agent works end-to-end before merging

## Pack Summary

| Pack | Agents | Description |
|------|--------|-------------|
| core | 11 | Development cycle essentials |
| security | 2 | Security & compliance |
| specialty | 1 | Domain experts |
| marketing | 1 | Strategy & planning |
