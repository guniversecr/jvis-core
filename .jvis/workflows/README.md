# JVIS Workflows

Predefined development workflows for different project types and scenarios.

## Available Workflows (6 files)

### Greenfield (New Projects)

| Workflow | Description |
|----------|-------------|
| `greenfield-fullstack.yaml` | Full-stack app (backend + frontend) |
| `greenfield-service.yaml` | Backend service/API only |
| `greenfield-ui.yaml` | Frontend application only |

### Brownfield (Existing Projects)

| Workflow | Description |
|----------|-------------|
| `brownfield-fullstack.yaml` | Enhance existing full-stack |
| `brownfield-service.yaml` | Modify existing backend |
| `brownfield-ui.yaml` | Update existing frontend |

## Workflow Structure

Each workflow defines:

```yaml
phases:
  - name: "Planning"
    agents: [analyst, pm, architect]
    outputs: [prd.md, architecture.md]

  - name: "Development"
    agents: [sm, dev, qa]
    outputs: [stories/, code/]

  - name: "Review"
    agents: [qa, devsecops]
    outputs: [gates/, audits/]
```

## Selection Logic

The appropriate workflow is selected based on:

1. Project type detection (has `server/`, `client/`, etc.)
2. State detection (empty, has_code, has_aicore)
3. User confirmation

## Usage

Workflows are automatically triggered by:
- `jvis new` (greenfield)
- `jvis add` (brownfield)
- `/journey:start` command
