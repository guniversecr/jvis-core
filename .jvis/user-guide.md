# JVIS - User Guide

AI-powered specialized agent system for agile development.

---

## Quick Start

```bash
# 1. Navigate to project and start Claude CLI
cd my-project
claude
```

Inside Claude:
```
# 2. Initialize documentation
/Custom:doc-init

# 3. Activate an agent
/dev              # Developer
/qa               # Testing
/architect        # Architecture

# 4. View agent commands
*help

# 5. Exit (saves context)
*exit
```

> The `/` and `*` commands only work inside Claude CLI.

---

## Available Agents

### Core Agents (Agile Methodology)

| Command | Agent | Function |
|---------|-------|----------|
| `/analyst` | Mary | Requirements analysis |
| `/pm` | John | PRD and backlog |
| `/architect` | Winston | Technical architecture |
| `/po` | - | Validation and sharding |
| `/sm` | Bob | User stories |
| `/dev` | James | Implementation |
| `/qa` | Quinn | Testing and quality gates |
| `/ux-expert` | - | UX design |
| `/devsecops` | SecOps | OWASP security |
| `/master` | - | General orchestrator |

### Specialized Agents (Stacks)

| Command | Stack | Function |
|---------|-------|----------|
| `/api` | Python FastAPI/Flask | REST API backend |
| `/prisma` | Node.js + Prisma | Backend with ORM |
| `/frontend` | React + Vite + TS | Modern frontend |
| `/eas` | Expo/React Native | Mobile apps + OTA |
| `/infra` | Terraform | Multi-cloud IaC |
| `/kotlin` | Android + Jetpack | Native Android apps |
| `/swift` | iOS + SwiftUI | Native iOS apps |
| `/unity` | Unity + C# | Games and XR |
| `/rust` | Rust + Axum | High-performance backend |
| `/voip` | Asterisk/Kamailio | VoIP telephony |
| `/migrate` | - | Stack migration |

### Strategy and Marketing Agents

| Command | Agent | Function |
|---------|-------|----------|
| `/strategist` | Alex | Market research, product strategy |
| `/marketing` | Maya | Campaigns, SEO/SEM, social ads, email marketing |
| `/solutions` | Sofia | Pre-sales consulting, workshops, proposals |

### Cloud Agents

| Command | Provider | Function |
|---------|----------|----------|
| `/aws` | AWS | EC2, S3, RDS, Lambda, CloudWatch |
| `/azure` | Azure | VMs, Storage, App Service, AVD |
| `/gcp` | GCP | Compute, GCS, Cloud SQL, GKE, Cloud Run |
| `/oci` | Oracle | Compute, Object Storage, Autonomous DB, OKE |

See `docs/manuals/manual-agents.md` and `docs/cloud-agents.md` for details.

---

## Workflows

| Command | Function |
|---------|----------|
| `/Custom:doc-init` | Initialize docs |
| `/Custom:doc-daily` | Daily checkpoint |
| `/Custom:project-resume` | Recover context |
| `/Custom:security-audit` | Security audit |

See `docs/manuals/manual-workflows.md` for details.

---

## Context Management

Agents maintain context automatically:

- **On start:** Load project state
- **On exit (`*exit`):** Save progress

See `docs/manuals/manual-context.md` for details.

---

## Development Flow

### New Project (Greenfield)
```
init-project -> /analyst -> /pm -> /architect -> /po -> [development]
```

### Existing Project (Brownfield)
```
add-to-project -> /architect (*document-project) -> /analyst -> /pm -> [development]
```

### Development (per story)
```
/sm -> /dev -> /qa -> commit
```

### Daily Cycle
```
/Custom:project-resume    # At start
[work...]
/Custom:doc-daily         # At end
```

See `docs/manuals/manual-workflows.md` for detailed guide.

---

## File Structure

```
.jvis/
├── agents/          # Agent definitions
├── tasks/           # Executable tasks
├── templates/       # Templates
└── checklists/      # Validation checklists

.claude/commands/
├── dev.md, qa.md... # Agent slash commands
└── workflows/       # Workflow commands

docs/
├── notes/           # Inter-agent communication
├── security/        # Security documentation
└── stories/         # User stories
```

---

## Specific Manuals

All manuals are in `docs/manuals/`:

| Manual | Content |
|--------|---------|
| `manual-workflows.md` | Greenfield and brownfield workflows |
| `manual-agents.md` | Reference for all agents |
| `manual-workflows.md` | /Custom:* commands |
| `manual-context.md` | Context management |
| `manual-configuration.md` | System configuration |
| `manual-new-project.md` | Creating new projects |
| `manual-existing-integration.md` | Adding to existing projects |
| `manual-stacks.md` | Adding development stacks |

See also `CLAUDE.md` for complete technical reference.

---

## Brownfield (Existing Projects)

To add JVIS to an existing project:

```bash
# From the JVIS directory
./add-to-project.sh /path/to/my-project
```

Then inside the project:
```bash
cd my-project
claude

/Custom:doc-init         # Initialize documentation
/architect
*document-project        # Document existing codebase
```

See `docs/manuals/manual-existing-integration.md` for complete guide.
