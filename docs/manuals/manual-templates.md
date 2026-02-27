# Manual: Template Catalog

Complete guide to all available templates in JVIS Framework.

---

## Summary

| Metric | Value |
|---------|-------|
| **Total Templates** | 105 |
| **Categories** | 19 |
| **Formats** | Markdown (.md) and YAML (.yaml) |
| **Location** | `.jvis/templates/` |

---

## Template Categories

### 1. client-comm/ - Client Communication

Templates for reports and presentations to clients.

| Template | Description | Format |
|----------|-------------|---------|
| `status-update-tmpl.md` | Weekly project status report | MD |
| `steering-committee-tmpl.md` | Presentation for steering committee | MD |

**Typical use:** PM generates weekly reports, monthly presentations to executives.

---

### 2. data/ - Data Migration

Templates for data migration planning.

| Template | Description | Format |
|----------|-------------|---------|
| `data-migration-plan-tmpl.md` | Complete data migration plan | MD |

**Typical use:** Legacy system migration projects, database changes.

---

### 3. devops/ - DevOps and Deployment

Templates for CI/CD, deployment, and operations.

| Template | Description | Format |
|----------|-------------|---------|
| `ci-cd-pipeline-tmpl.yaml` | CI/CD pipeline configuration | YAML |
| `blue-green-deploy-tmpl.md` | Blue-green deployment plan | MD |
| `rollback-procedure-tmpl.md` | Rollback procedure | MD |
| `monitoring-strategy-tmpl.yaml` | Monitoring and observability strategy | YAML |
| `slo-sla-tmpl.md` | SLO/SLA definition | MD |
| `disaster-recovery-plan-tmpl.md` | Disaster recovery plan | MD |
| `backup-strategy-tmpl.yaml` | Backup strategy | YAML |
| `deployment-checklist-tmpl.md` | Deployment checklist | MD |
| `release-notes-tmpl.md` | Release notes | MD |

**Typical use:** Set up pipelines, prepare deployments, define SLAs.

---

### 4. docs/ - Technical Documentation

Templates for architecture documentation.

| Template | Description | Format |
|----------|-------------|---------|
| `architecture/adr-template.md` | Architecture Decision Record | MD |
| (others per project) | Technical documentation | MD |

**Typical use:** Document architectural decisions.

---

### 5. finance/ - Project Finance

Templates for project financial management.

| Template | Description | Format |
|----------|-------------|---------|
| `rate-card-tmpl.yaml` | Rate card by role | YAML |
| `budget-tmpl.yaml` | Project budget | YAML |
| `timesheet-tmpl.md` | Weekly time log | MD |
| `invoice-tmpl.md` | Client invoice | MD |
| `budget-report-tmpl.md` | Budget status report | MD |
| `profitability-tmpl.md` | Profitability analysis | MD |
| `cost-optimization-tmpl.md` | Cloud cost optimization | MD |
| `infrastructure-rightsizing-tmpl.yaml` | Infrastructure right-sizing | YAML |

**Typical use:** Financial tracking, invoicing, profitability analysis.

---

### 6. handoff/ - Transition and Delivery

Templates for project transitions.

| Template | Description | Format |
|----------|-------------|---------|
| `ops-handoff-tmpl.md` | Handoff to operations team | MD |
| `knowledge-transfer-tmpl.md` | Knowledge transfer plan | MD |

**Typical use:** End of project, dev-to-ops transition, team changes.

---

### 7. integrations/ - Integrations

Templates for integration specifications.

| Template | Description | Format |
|----------|-------------|---------|
| `api-integration-spec-tmpl.md` | API integration specification | MD |
| `webhook-spec-tmpl.md` | Webhook specification | MD |

**Typical use:** Document third-party integrations.

---

### 8. knowledge/ - Knowledge Base

Templates for knowledge management.

| Template | Description | Format |
|----------|-------------|---------|
| `adr-tmpl.md` | Architecture Decision Record | MD |
| `technical-spec-tmpl.md` | Technical specification | MD |
| `lessons-learned-tmpl.md` | Lessons learned | MD |

**Typical use:** Document decisions, specifications, lessons.

---

### 9. legal/ - Legal Documents

Templates for contracts and agreements.

| Template | Description | Format |
|----------|-------------|---------|
| `nda-tmpl.md` | Non-Disclosure Agreement | MD |
| `msa-tmpl.md` | Master Service Agreement | MD |
| `sow-tmpl.md` | Statement of Work | MD |
| `terms-conditions-tmpl.md` | Terms and conditions | MD |

**Typical use:** Pre-sales, contract formalization.

---

### 10. migration/ - Code Migration

Templates for system migration.

| Template | Description | Format |
|----------|-------------|---------|
| `migration-plan-tmpl.md` | Code migration plan | MD |
| `migration-analysis-tmpl.md` | Legacy system analysis | MD |
| `migration-checklist-tmpl.md` | Migration checklist | MD |

**Typical use:** Migrate from Laravel/Express to FastAPI/Flask.

---

### 11. onboarding/ - Onboarding

Templates for onboarding people and clients.

| Template | Description | Format |
|----------|-------------|---------|
| `client-onboarding-tmpl.md` | New client onboarding | MD |
| `developer-onboarding-tmpl.md` | Developer onboarding | MD |
| `training-plan-tmpl.md` | Training plan | MD |

**Typical use:** New clients, new team members.

---

### 12. operations/ - Operations

Templates for operations management.

| Template | Description | Format |
|----------|-------------|---------|
| `runbook-tmpl.md` | Operational runbook | MD |
| `incident-response-plan-tmpl.md` | Incident response plan | MD |
| `postmortem-tmpl.md` | Post-mortem analysis | MD |
| `escalation-procedures-tmpl.md` | Escalation procedures | MD |

**Typical use:** Daily operations, incident management.

---

### 13. pre-sales/ - Pre-Sales

Templates for the pre-sales process.

| Template | Description | Format |
|----------|-------------|---------|
| `discovery-workshop-tmpl.md` | Discovery workshop | MD |
| `proposal-tmpl.md` | Commercial proposal | MD |

**Typical use:** Sales process, client workshops.

---

### 14. project-mgmt/ - Project Management

Templates for Agile project management.

| Template | Description | Format |
|----------|-------------|---------|
| `project-kickoff-tmpl.md` | Kickoff document | MD |
| `sprint-retrospective-tmpl.md` | Sprint retrospective | MD |
| `meeting-minutes-tmpl.md` | Meeting minutes | MD |
| `status-report-tmpl.md` | Internal status report | MD |
| `risk-register-tmpl.md` | Risk register | MD |
| `change-request-tmpl.md` | Change request | MD |
| `project-closure-tmpl.md` | Project closure | MD |

**Typical use:** Project lifecycle management.

---

### 15. quality/ - Quality

Templates for quality management.

| Template | Description | Format |
|----------|-------------|---------|
| `technical-debt-tmpl.md` | Technical debt register | MD |

**Typical use:** Technical debt tracking and management.

---

### 16. reporting/ - Reports

Templates for executive reports.

| Template | Description | Format |
|----------|-------------|---------|
| `kpi-dashboard-tmpl.md` | KPI dashboard | MD |
| `project-health-tmpl.md` | Project health | MD |
| `resource-utilization-tmpl.md` | Resource utilization | MD |

**Typical use:** Reports to management, metrics analysis.

---

### 17. solutions/ - Solution Architecture

Templates for solution design.

| Template | Description | Format |
|----------|-------------|---------|
| `quotation-tmpl.yaml` | Detailed quotation | YAML |
| `solution-architecture-tmpl.md` | Solution architecture | MD |
| `gap-analysis-tmpl.md` | Gap analysis | MD |
| `workshop-questions-tmpl.md` | Workshop questions | MD |
| `findings-tmpl.md` | Discovery findings | MD |

**Typical use:** Pre-sales, solution design.

---

### 18. testing/ - Testing

Templates for test planning.

| Template | Description | Format |
|----------|-------------|---------|
| `test-plan-tmpl.md` | Test plan | MD |
| `uat-protocol-tmpl.md` | UAT protocol | MD |
| `load-test-plan-tmpl.md` | Load test plan | MD |
| `performance-benchmark-tmpl.md` | Performance benchmark | MD |
| `capacity-planning-tmpl.md` | Capacity planning | MD |

**Typical use:** QA, performance testing, capacity planning.

---

### 19. vendor/ - Vendor Management

Templates for vendor evaluation.

| Template | Description | Format |
|----------|-------------|---------|
| `rfp-comparison-matrix.yaml` | RFP comparison matrix | YAML |

**Typical use:** Vendor evaluation, supplier selection.

---

## Root Templates

In addition to categories, there are templates at the root for common cases:

| Template | Description | Format |
|----------|-------------|---------|
| `prd-tmpl.yaml` | Product Requirements Document | YAML |
| `brownfield-prd-tmpl.yaml` | PRD for brownfield projects | YAML |
| `story-tmpl.yaml` | User Story | YAML |
| `qa-gate-tmpl.yaml` | Quality Gate | YAML |
| `architecture-tmpl.yaml` | Architecture document | YAML |
| `brownfield-architecture-tmpl.yaml` | Brownfield architecture | YAML |
| `fullstack-architecture-tmpl.yaml` | Fullstack architecture | YAML |
| `front-end-architecture-tmpl.yaml` | Frontend architecture | YAML |
| `front-end-spec-tmpl.yaml` | Frontend specification | YAML |
| `project-brief-tmpl.yaml` | Project brief | YAML |
| `user-persona-tmpl.yaml` | User persona | YAML |
| ... | (marketing, strategy templates, etc.) | YAML |

---

## How to Use the Templates

### 1. Copy Template

```bash
cp .jvis/templates/project-mgmt/project-kickoff-tmpl.md docs/project-kickoff.md
```

### 2. Use with an Agent

Agents use templates automatically:

```bash
/pm          # Uses prd-tmpl.yaml
/sm          # Uses story-tmpl.yaml
/qa          # Uses qa-gate-tmpl.yaml
/solutions   # Uses quotation-tmpl.yaml
/finance     # Uses budget-tmpl.yaml, invoice-tmpl.md
```

### 3. Agent Commands

```bash
# /solutions
*draft-proposal    # Uses proposal templates
*create-quotation  # Uses quotation-tmpl.yaml

# /finance
*generate-invoice  # Uses invoice-tmpl.md
*budget-status     # Uses budget-report-tmpl.md

# /sm
*draft             # Uses story-tmpl.yaml

# /qa
*gate              # Uses qa-gate-tmpl.yaml
```

---

## Customization

### Modify Templates

1. Edit the template in `.jvis/templates/`
2. Changes apply to all new projects

### Add New Templates

1. Create the file in the appropriate category
2. Follow the naming convention: `{name}-tmpl.{md|yaml}`
3. Document in this manual

---

## Templates by Workflow

### Pre-Sales -> Development

```
pre-sales/discovery-workshop-tmpl.md
    ↓
solutions/gap-analysis-tmpl.md
    ↓
solutions/quotation-tmpl.yaml
    ↓
legal/msa-tmpl.md + legal/sow-tmpl.md
    ↓
project-mgmt/project-kickoff-tmpl.md
    ↓
(root templates) prd-tmpl.yaml
    ↓
(root templates) story-tmpl.yaml
```

### Development -> Production

```
testing/test-plan-tmpl.md
    ↓
devops/ci-cd-pipeline-tmpl.yaml
    ↓
devops/blue-green-deploy-tmpl.md
    ↓
devops/monitoring-strategy-tmpl.yaml
    ↓
operations/runbook-tmpl.md
```

### Operations -> Closure

```
operations/incident-response-plan-tmpl.md
    ↓
operations/postmortem-tmpl.md
    ↓
handoff/ops-handoff-tmpl.md
    ↓
handoff/knowledge-transfer-tmpl.md
    ↓
project-mgmt/project-closure-tmpl.md
```

---

## Updates

| Date | Changes |
|-------|---------|
| 2024-12-21 | Initial documentation with 105 templates |

---

## See Also

- [JVIS Manual](manual-jvis.md) - Unified manager
- [Agents Manual](manual-agentes.md) - Agent reference
- [Consulting Manual](manual-consulting.md) - Consulting workflow
- [Finance Manual](manual-finance.md) - Financial management
