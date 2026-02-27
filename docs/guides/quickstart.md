# JVIS Quick Start Guide

Get started with JVIS in 5 minutes.

## Installation

### 1. Clone or Download JVIS

```bash
git clone https://github.com/your-org/jvis.git
cd jvis
```

### 2. Make CLI Available Globally

```bash
# macOS/Linux
sudo ln -sf $(pwd)/jvis /usr/local/bin/jvis

# Verify
jvis version
```

## Creating a New Project

### Option 1: Interactive Menu

```bash
jvis new
```

Follow the prompts to select:
- Project type (Backend, Frontend, Full-Stack, Mobile, etc.)
- Stack (FastAPI, React, Kotlin, etc.)
- Database (PostgreSQL, MySQL, etc.)

### Option 2: Direct Commands

```bash
# Backend only
jvis new --stack python-fastapi --name my-api

# Full-stack
jvis new --stack fullstack --backend python-fastapi --frontend react-vite
```

## Adding JVIS to Existing Project

```bash
cd /path/to/your/project
jvis add .
```

JVIS will:
1. Detect your current stack
2. Create `.jvis/` directory
3. Add appropriate agents
4. Set up documentation structure

## Your First Agent Session

### 1. Start an Agent

```bash
# In your project directory with Claude Code
/dev
```

### 2. Load Context

The agent automatically loads context on start. Or manually:

```bash
*load-context
```

### 3. Work

Ask the agent to help:

```
Help me implement user authentication
```

### 4. Save and Exit

```bash
*exit
```

This saves your context for the next session.

## Common Workflows

### New Feature Development

```
1. /pm           # Create PRD
2. /architect    # Design solution
3. /sm           # Create stories
4. /dev          # Implement
5. /qa           # Review
6. Commit
```

### Bug Fix

```
1. /dev          # Investigate and fix
2. /qa           # Verify fix
3. Commit
```

### Security Audit

```
1. /devsecops    # Run audit
2. *audit        # Generate report
```

## Key Commands

| Command | Purpose |
|---------|---------|
| `jvis new` | Create new project |
| `jvis add <path>` | Add to existing project |
| `jvis update <path>` | Update JVIS |
| `jvis helper` | Interactive help |
| `/helper` | In-session help agent |

## Getting Help

- Run `/helper` for interactive guidance
- See `docs/manual.md` for full documentation
- Check `.jvis/agents/` for agent details

## Next Steps

1. Explore available agents: `docs/agents/index.md`
2. Learn the development cycle: `docs/guides/development.md`
3. Configure your stack: `.jvis/core-config.yaml`
