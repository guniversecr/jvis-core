# JVIS Templates

This directory contains **160+ document templates** organized by category.

**Last Updated:** v2.9.1 (2026-01-25)

## Template Naming Convention

All templates follow the pattern: `{name}-tmpl.{yaml|md}`

- `.yaml` - Structured data templates (PRD, stories, configs)
- `.md` - Document templates (reports, proposals, plans)

## Root Templates (6 files)

Core templates used across multiple agents:

| Template | Purpose | Used By |
|----------|---------|---------|
| `prd-tmpl.yaml` | Product Requirements Document | PM, PO |
| `brownfield-prd-tmpl.yaml` | PRD for existing projects | PM |
| `architecture-tmpl.yaml` | System architecture | Architect |
| `brownfield-architecture-tmpl.yaml` | Architecture for existing | Architect |
| `front-end-architecture-tmpl.yaml` | Frontend architecture | Architect, Frontend |
| `front-end-spec-tmpl.yaml` | Frontend specifications | Frontend |

### Relocated Templates

The following templates have been moved to appropriate subdirectories:

| Template | New Location | Used By |
|----------|--------------|---------|
| `story-tmpl.yaml` | `project-mgmt/` | SM |
| `qa-gate-tmpl.yaml` | `quality/` | QA |
| `project-brief-tmpl.yaml` | `solutions/` | Analyst |
| `brainstorming-output-tmpl.yaml` | `solutions/` | Analyst |
| `business-model-canvas-tmpl.yaml` | `solutions/` | Strategist |
| `mvp-scope-tmpl.yaml` | `solutions/` | PM, Strategist |
| `fullstack-architecture-tmpl.yaml` | `fullstack/` | Architect |
| `core-config-fullstack-tmpl.yaml` | `fullstack/` | Setup |

## Template Subdirectories

### amazon-connect/ (93 templates)

Amazon Connect-specific templates for contact center operations:

```
amazon-connect/
├── cases/           # 20 case templates
├── views/           # 15 UI views
├── data_tables/     # 8 data table configs
├── routing/         # 15 routing profiles
├── profiles/        # 5 customer profiles
├── campaigns/       # 5 outbound campaigns
├── contact-flows/   # 15 IVR flows
├── evaluation-forms/# 6 agent evaluation
├── guides/          # 6 agent assist guides
├── users/           # 3 user/security profiles
└── iac/             # 1 CloudFormation template
```

### marketing/ (51 templates)

Full marketing operations:

| Category | Templates |
|----------|-----------|
| Strategy | `market-research-tmpl.yaml`, `competitive-analysis-tmpl.yaml`, `gtm-plan-tmpl.yaml` |
| Analytics | `marketing-kpis-tmpl.yaml`, `attribution-model-tmpl.yaml`, `funnel-analysis-tmpl.yaml` |
| Content | `content-strategy-tmpl.yaml`, `content-calendar-tmpl.yaml`, `content-brief-tmpl.yaml` |
| Email | `email-strategy-tmpl.yaml`, `email-campaign-tmpl.yaml`, `email-automation-tmpl.yaml` |
| Social | `social-media-plan-tmpl.yaml`, `social-ads-strategy-tmpl.yaml` |
| SEM/SEO | `sem-campaign-structure-tmpl.yaml`, `seo-content-plan-tmpl.yaml` |
| Product | `winning-product-score-tmpl.yaml`, `pmf-scorecard-tmpl.yaml`, `unit-economics-tmpl.yaml` |

### finance/ (8 templates)

Financial management:

| Template | Purpose |
|----------|---------|
| `rate-card-tmpl.yaml` | Service rates |
| `budget-tmpl.yaml` | Project budget |
| `timesheet-tmpl.md` | Time tracking |
| `invoice-tmpl.md` | Invoice generation |
| `budget-report-tmpl.md` | Budget reporting |
| `profitability-tmpl.md` | Profitability analysis |

### solutions/ (12 templates)

Pre-sales and consulting:

| Template | Purpose |
|----------|---------|
| `discovery-workshop-tmpl.yaml` | Workshop questions |
| `proposal-tmpl.md` | Technical proposal |
| `quotation-tmpl.yaml` | Pricing quotation |
| `gap-analysis-tmpl.yaml` | AS-IS vs TO-BE |

### legal/ (4 templates)

Legal documents:

| Template | Purpose |
|----------|---------|
| `nda-tmpl.md` | Non-disclosure agreement |
| `msa-tmpl.md` | Master service agreement |
| `sow-tmpl.md` | Statement of work |
| `terms-conditions-tmpl.md` | Terms and conditions |

### quality/ (6 templates)

Quality assurance:

| Template | Purpose |
|----------|---------|
| `test-plan-tmpl.yaml` | Test planning |
| `test-case-tmpl.yaml` | Test case definition |
| `qa-assessment-tmpl.md` | QA assessment |

### pentest/ (67 templates)

Penetration testing:

```
pentest/
├── engagement/      # 8 scope, ROE, authorization
├── scans/           # 15 Nmap, Nuclei, ZAP configs
├── reports/         # 18 executive, technical
├── payloads/        # 6 XSS, SQLi, SSTI, XXE
├── checklists/      # 12 OWASP WSTG, ASVS
└── configs/         # 8 tool configurations
```

### docs/ (15 templates)

Documentation templates:

```
docs/
├── architecture/    # ADR, API reference, coding standards
├── guides/          # User guides, setup guides
└── specs/           # Technical specifications
```

### Other Subdirectories

| Directory | Count | Purpose |
|-----------|-------|---------|
| `backlog-export/` | 6 | Export to Jira, Azure, Trello, etc. |
| `bitrix24/` | 5 | Bitrix24 integration |
| `client-comm/` | 4 | Client communication |
| `data/` | 3 | Data models |
| `devops/` | 6 | CI/CD, deployments |
| `fullstack/` | 3 | Full-stack configs |
| `handoff/` | 3 | Agent handoff docs |
| `integrations/` | 4 | Third-party integrations |
| `knowledge/` | 5 | Knowledge base |
| `migration/` | 8 | Migration planning |
| `onboarding/` | 3 | Developer onboarding |
| `operations/` | 4 | Operations runbooks |
| `pipelines/` | 9 | CI/CD pipeline configs |
| `pre-sales/` | 4 | Pre-sales materials |
| `project-mgmt/` | 5 | Project management |
| `reporting/` | 4 | Report templates |
| `testing/` | 5 | Testing templates |
| `vendor/` | 3 | Vendor management |

### sync/ (4 templates) - NEW in v2.9.x

Synchronization system templates:

| Template | Purpose |
|----------|---------|
| `team-state-tmpl.yaml` | Team synchronization state |
| `sync-state-tmpl.json` | Session sync state |
| `local-overrides-tmpl.yaml` | Local knowledge overrides |
| `README.md` | Sync system documentation |

### launch/ (5 templates) - NEW in v2.8.9

Product launch templates:

| Template | Purpose |
|----------|---------|
| `product-brief-tmpl.md` | Product brief |
| `swot-analysis-tmpl.md` | SWOT analysis |
| `gtm-strategy-tmpl.md` | Go-to-market strategy |
| `launch-checklist-tmpl.md` | Launch checklist |
| `launch-timeline-tmpl.md` | Launch timeline |

### brand/ (3 templates) - NEW in v2.8.9

Brand identity templates:

| Template | Purpose |
|----------|---------|
| `brand-identity-tmpl.md` | Brand identity |
| `messaging-framework-tmpl.md` | Messaging framework |
| `visual-guidelines-tmpl.md` | Visual guidelines |

### Root Templates - NEW in v2.9.0

| Template | Purpose |
|----------|---------|
| `project-composition-tmpl.yaml` | Project composition configuration |

## Using Templates

### In Agents

Agents reference templates using paths:

```yaml
template: .jvis/templates/prd-tmpl.yaml
```

### Template Variables

Templates use placeholder patterns:

- `{project_name}` - Project name
- `{date}` - Current date
- `{version}` - Version number
- `[PLACEHOLDER]` - Manual input required

## Adding New Templates

1. Create template in appropriate subdirectory
2. Follow naming convention: `{name}-tmpl.{yaml|md}`
3. Include metadata header if applicable
4. Add to this README in appropriate category
5. Reference from relevant agents/tasks

## Template Structure

### YAML Templates

```yaml
# Template metadata
_meta:
  name: "Template Name"
  version: "1.0.0"
  description: "What this template is for"

# Template content
field1: "{placeholder}"
field2: "[Manual input]"
```

### Markdown Templates

```markdown
# Document Title

## Section 1
{content}

## Section 2
[PLACEHOLDER: Description of what goes here]
```

## Best Practices

1. **Use consistent naming** - Always use `-tmpl` suffix
2. **Include metadata** - Version and description
3. **Use clear placeholders** - `{variable}` or `[DESCRIPTION]`
4. **Organize by domain** - Keep templates in appropriate subdirectories
5. **Document usage** - Add to this README when creating new templates
