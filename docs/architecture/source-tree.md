# Source Tree - JVIS Framework

> **Current state & metrics:** `docs/STATUS.md` (SSOT)

## Root Structure

```
.
├── .jvis/                 # Framework core (agents, tasks, templates)
├── .claude/               # Claude Code integration (commands, skills, hooks)
├── src/jvis/              # Python CLI source (Click + Jinja2 + PyYAML)
├── docs/                  # Project documentation
├── tests/                 # Test suite (unit, integration, smoke)
├── CLAUDE.md              # Claude Code instructions
├── CHANGELOG.md           # Version history
├── pyproject.toml         # Python package config (hatchling)
└── Makefile               # Build commands
```

## .jvis/ - Framework Core

```
.jvis/
├── agents/                # Agent YAML definitions (see STATUS.md for counts)
│   ├── core/              # Core development agents
│   ├── security/          # Security agents
│   ├── specialty/         # Specialty agents
│   └── marketing/         # Marketing agents
│
├── agent-engine/          # Generator: engine.py, templates/, schemas/
│   ├── engine.py          # Renders YAML → markdown commands
│   ├── templates/         # Jinja2 templates (claude.md, cursor.md)
│   └── schemas/           # agent.schema.yaml
│
├── tasks/                 # Executable task workflows
│   ├── load-context.md    # Load project context (auto)
│   ├── save-context.md    # Save session context
│   ├── create-doc.md      # Document creation
│   └── ...                # Per-agent tasks
│
├── templates/             # Document + scaffold templates
│   ├── prd-tmpl.yaml      # PRD template
│   ├── story-tmpl.yaml    # User story template
│   ├── qa-gate-tmpl.yaml  # QA gate template
│   ├── solutions/         # Pre-sales templates
│   ├── legal/             # Legal document templates
│   └── pentest/           # Security audit templates
│
├── checklists/            # Validation checklists
├── data/                  # Knowledge base, technical preferences
├── platform/claude/       # Platform-specific extras (4 files)
├── core-config.yaml       # Framework configuration
├── VERSION.yaml           # Version tracking
└── version                # Canonical version string (SSOT)
```

## src/jvis/ - Python Package

```
src/jvis/
├── __init__.py            # Package init, __version__
├── cli.py                 # Click CLI (8 commands)
├── main.py                # Entry point
├── scaffold/              # Project scaffolding
│   ├── scaffolder.py      # Stack scaffold engine
│   └── shared_files.py    # Framework file installer
├── utils/                 # Utilities
│   ├── config.py          # Version, paths, config
│   └── ...
├── licensing/             # Tier gate system
└── data/stacks/           # Stack manifests + Jinja2 templates
    ├── python-fastapi/
    ├── nodejs-express/
    ├── react-vite/
    └── ...                # See STATUS.md for full list
```

## .claude/ - Claude Code Integration

```
.claude/
├── commands/              # Generated slash commands (DO NOT EDIT)
│   ├── dev.md
│   ├── qa.md
│   ├── architect.md
│   ├── workflows/         # Workflow commands
│   └── ...
├── skills/                # Domain knowledge
│   ├── agents/SKILL.md    # Agent system guide
│   ├── python/SKILL.md    # Python conventions
│   └── testing/SKILL.md   # Testing practices
├── hooks/                 # Quality automation
└── settings.json          # Claude Code settings
```

## docs/ - Documentation

```
docs/
├── STATUS.md              # SSOT for all project state
├── INDEX.md               # Navigation hub
├── architecture/          # Architecture docs
├── adr/                   # Architecture Decision Records
├── notes/                 # Inter-agent communication
│   ├── project-log.md     # Activity history
│   ├── next-action.md     # Priority actions
│   ├── lessons-learned.md # Permanent lessons
│   └── from-*.md          # Agent notes
├── plans/                 # Execution plans (ADR-005)
├── planning/              # Strategic planning docs
└── manuals/               # User-facing documentation
```

## Key Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Instructions for Claude Code |
| `pyproject.toml` | Python package configuration |
| `.jvis/core-config.yaml` | Framework configuration |
| `.jvis/version` | Canonical version (SSOT) |
| `docs/STATUS.md` | Project state (SSOT) |
