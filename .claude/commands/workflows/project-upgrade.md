---
description: Analyze and upgrade JVIS installation in this project
---

# Project Upgrade Workflow

You are now executing the **Project Upgrade Analysis** workflow.

## Your Mission

Analyze the current project's JVIS installation, identify upgrade opportunities, recommend new agents based on the technology stack, and provide a clear upgrade path with next steps.

## Workflow Steps

### Step 1: Version Check

1. Read `.jvis/version` to get current version
2. Note if version file is missing (legacy installation)
3. Compare with latest version features

### Step 2: Component Inventory

Scan and report on existing components:

```
.jvis/
├── agents/          # Count installed agent definitions
├── tasks/           # Available tasks
├── templates/       # Document templates
├── checklists/      # Validation checklists
└── data/            # Knowledge base

.claude/commands/    # Slash commands (count agents)

.mcp/                # MCP servers
├── aws-server/
├── azure-server/
├── gcp-server/
└── oci-server/
```

### Step 3: Technology Stack Detection

Analyze the project to detect technologies:

**Check for:**
- `package.json` → Node.js, React, Expo, Express, Prisma, Vite
- `requirements.txt` / `pyproject.toml` → Python, FastAPI, Flask, Django
- `Cargo.toml` → Rust
- `build.gradle` → Kotlin/Android
- `Package.swift` / `*.xcodeproj` → Swift/iOS
- `Assets/` + `ProjectSettings/` → Unity
- `*.tf` files → Terraform
- `Dockerfile` / `docker-compose.yml` → Docker
- `.github/workflows/` → CI/CD

### Step 4: Agent Recommendations

Based on detected stack, recommend agents:

| If Detected | Recommend Agent | Why |
|-------------|-----------------|-----|
| React/Vite | `/frontend` | React + Vite specialist |
| Expo | `/eas` | EAS builds, OTA updates |
| Express + Prisma | `/prisma` | Node.js + Prisma ORM |
| FastAPI/Flask | `/api` | Python backend specialist |
| Kotlin/Android | `/kotlin` | Android native development |
| Swift/iOS | `/swift` | iOS native development |
| Unity | `/unity` | Game development |
| Rust | `/rust` | High-performance backend |
| Terraform | `/devsecops` | Infrastructure as Code |
| Any cloud | `/aws`, `/azure`, `/gcp`, `/oci` | Cloud operations |
| Any project | `/devsecops` | Security audits |

### Step 5: MCP Server Status

For each MCP server directory found:
1. Check if `package.json` exists
2. Check if `dist/index.js` exists (needs build?)
3. Check if configured in `.claude/mcp.json`

### Step 6: Generate Report

Create a comprehensive report with:

1. **Current State Summary**
2. **Available Upgrades**
3. **Recommended Agents** (with rationale)
4. **Action Items** (prioritized)
5. **Next Steps** (specific commands)

## Output Format

Present findings as:

```markdown
# JVIS Upgrade Analysis

## Current Installation
- **Version:** [version or "legacy"]
- **Agents Installed:** [count] of 28
- **MCP Servers:** [list]
- **Cloud Templates:** [list]

## Detected Technology Stack
- [Technology 1]
- [Technology 2]
- ...

## Recommendations

### Agents to Add
| Agent | Stack | Benefit |
|-------|-------|---------|
| `/frontend` | React + Vite | Modern web development |
| ... | ... | ... |

### MCP Servers to Configure
| Server | Status | Action Needed |
|--------|--------|---------------|
| aws-server | Installed, not built | Run `npm run build` |
| ... | ... | ... |

## Upgrade Commands

### From Terminal (JVIS directory):
```bash
# Analyze (already done)
./update-project.sh /path/to/this/project

# Apply core updates
./update-project.sh --apply /path/to/this/project

# Add recommended agents
./add-to-project.sh /path/to/this/project --agents frontend,infra,aws
```

### From Claude Code (this project):
```
# After upgrade, use these workflows:
/Custom:project-resume    # Start sessions with context
/Custom:security-audit    # Security review
/Custom:doc-daily         # Daily checkpoints
```

## Leveraging New Features

### 1. Cloud Operations
Use cloud agents to manage infrastructure directly:
```
/aws
*status          # Check AWS identity
*ec2-list        # List instances
*costs           # View costs
*tf-plan         # Terraform plan
```

### 2. Enhanced Security
Run security audits with DevSecOps:
```
/devsecops
*audit           # Full security audit
*owasp-check     # OWASP Top 10 review
*dependency-scan # Check vulnerabilities
```

### 3. Stack-Specific Development
Use specialized agents for your stack:
```
/frontend        # React + Vite development
/api             # Python FastAPI backend
/prisma          # Node.js + Prisma
```

### 4. Context Persistence
Maintain context across sessions:
```
/Custom:project-resume   # At session start
*save-context            # Before ending (automatic with *exit)
```
```

## Execution

Now analyze this project and generate the upgrade report.

1. First, scan the project structure
2. Detect the technology stack
3. Compare installed vs available components
4. Generate prioritized recommendations
5. Provide specific upgrade commands
6. Suggest how to leverage new features for this specific project
