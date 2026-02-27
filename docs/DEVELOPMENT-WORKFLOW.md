# JVIS Development Workflow

Complete guide for the story-to-deployment development cycle using JVIS agents.

## Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         JVIS DEVELOPMENT WORKFLOW                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│   │   /pm    │───►│/architect│───►│   /sm    │───►│  /dev    │             │
│   │  (John)  │    │(Winston) │    │  (Bob)   │    │ (James)  │             │
│   └──────────┘    └──────────┘    └──────────┘    └────┬─────┘             │
│       │                                                │                    │
│       │ PRD              Architecture         Stories  │ Code              │
│       ▼                       ▼                   ▼    ▼                    │
│   ┌──────────────────────────────────────────────────────┐                 │
│   │                  docs/product/                        │                 │
│   │   prd.md → architecture.md → stories/{epic}/story.md  │                 │
│   └──────────────────────────────────────────────────────┘                 │
│                                                    │                        │
│                                                    ▼                        │
│                                            ┌──────────┐                     │
│                                            │   /qa    │                     │
│                                            │ (Quinn)  │                     │
│                                            └────┬─────┘                     │
│                                                 │                           │
│                              ┌──────────────────┼──────────────────┐       │
│                              ▼                  ▼                  ▼       │
│                           PASS             CONCERNS              FAIL      │
│                              │                  │                  │       │
│                              ▼                  ▼                  ▼       │
│                           Deploy          Fix + Re-review      Major Fix   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Workflow Phases

### Phase 1: Requirements (PM)

**Agent:** `/pm` (John)
**Purpose:** Create Product Requirements Document (PRD)

**Commands:**
```bash
/pm                          # Activate PM agent
*create-prd                  # Create new PRD from requirements
*create-brownfield-prd       # Create PRD for existing project
*shard-prd                   # Break PRD into epics
```

**Output:** `docs/product/prd.md`

**Handoff:** PRD ready → `/architect`

---

### Phase 2: Architecture (Architect)

**Agent:** `/architect` (Winston)
**Purpose:** Design system architecture based on PRD

**Commands:**
```bash
/architect                        # Activate Architect agent
*create-backend-architecture      # Backend-only architecture
*create-front-end-architecture    # Frontend-only architecture
*create-full-stack-architecture   # Full-stack architecture
*create-brownfield-architecture   # For existing projects
*shard-prd                        # Shard into technical components
```

**Output:** `docs/product/architecture.md`

**Handoff:** Architecture ready → `/sm`

---

### Phase 3: Story Creation + Plan (Scrum Master)

**Agent:** `/sm` (Bob)
**Purpose:** Create detailed, actionable stories from PRD and architecture, generate execution plan

**Commands:**
```bash
/sm                          # Activate SM agent
*draft                       # Create next story + update plan YAML
*draft-fullstack             # Create story with backend/frontend context
*story-checklist             # Validate story completeness
*assign-backend              # Assign to backend agent (fullstack)
*assign-frontend             # Assign to frontend agent (fullstack)
```

**Output:**
- `docs/product/stories/{epic}/story-{id}.md`
- `docs/plans/active-plan.yaml` (updated with new steps, risk levels, gate assignments)

**Story Structure:**
```markdown
# Story {id}: {title}

## Status: Draft | Ready | In Progress | Ready for Review | Done

## Story
As a {user}, I want {feature}, so that {benefit}.

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Tasks
- [ ] Task 1
  - [ ] Subtask 1.1
  - [ ] Subtask 1.2
- [ ] Task 2

## Dev Notes
{Implementation guidance from architect}

## Testing
{Required test scenarios}

## Dev Agent Record
### Debug Log
### Completion Notes
### File List
### Change Log
```

**Handoff:** Story ready → `/dev`

---

### Phase 4: Development (Developer)

**Agent:** `/dev` (James)
**Purpose:** Implement stories following the task sequence

**Commands:**
```bash
/dev                         # Activate Dev agent
*develop-story               # Implement current story
*run-tests                   # Execute linting and tests
*explain                     # Explain implementation decisions
*review-qa                   # Apply QA feedback fixes
```

**Development Protocol:**
1. Read plan file (`docs/plans/active-plan.yaml`) to find assigned step
2. Set step status to `in_progress`
3. Read story file (contains all needed context)
4. Execute tasks sequentially
5. Write tests for each task
6. Run validations
7. Mark task checkbox `[x]` only when ALL pass
8. Write step report (`docs/plans/reports/{step-id}-report.md`)
9. Set step status to `done` in plan file
10. Update File List section
11. Set story status: `Ready for Review`

**What Dev CAN Update:**
- Tasks/Subtasks checkboxes
- Dev Agent Record section
- Debug Log
- Completion Notes
- File List
- Change Log
- Status (to Ready for Review)

**What Dev CANNOT Update:**
- Story description
- Acceptance Criteria
- Testing section
- Any other sections

**Blocking Conditions (HALT):**
- Unapproved dependencies needed
- Ambiguous requirements
- 3+ failed attempts at same task
- Missing configuration
- Failing regression tests

**Handoff:** Code ready → `/qa`

---

### Phase 5: Quality Gate (QA)

**Agent:** `/qa` (Quinn)
**Purpose:** Review code quality and make gate decision

**Commands:**
```bash
/qa                          # Activate QA agent
*review                      # Comprehensive story review
*gate                        # Write quality gate decision
*trace                       # Map requirements to tests
*risk-profile                # Generate risk assessment
*test-design                 # Create test scenarios
*nfr-assess                  # Validate non-functional requirements
```

**Gate Decisions:**

| Decision | Meaning | Action |
|----------|---------|--------|
| **PASS** | Meets quality standards | Proceed to deploy |
| **CONCERNS** | Minor issues found | Fix and re-review |
| **FAIL** | Major issues found | Significant rework needed |
| **WAIVED** | Issues accepted for now | Proceed with known debt |

**Gate Output:** `docs/qa/gates/{epic}.{story}-{slug}.yml`

**Review Scope:**
- Requirements traceability
- Test coverage
- Code quality
- Security considerations
- Performance implications
- Technical debt assessment

**Handoff:**
- PASS/WAIVED → Deploy
- CONCERNS/FAIL → `/dev`

---

### Phase 6: Deploy

After QA approval (or epic checkpoint if last story in epic):

1. **Commit code**
   ```bash
   git add .
   git commit -m "feat(epic): story description"
   ```

2. **Push to remote**
   ```bash
   git push origin feature-branch
   ```

3. **Create PR** (if using branches)
   ```bash
   gh pr create --title "Story Title" --body "Description"
   ```

4. **Deploy** (per project workflow)

---

## Inter-Agent Communication

Agents communicate via `docs/notes/from-{agent}.md` files:

| Agent | Writes To | Reads From |
|-------|-----------|------------|
| PM | from-pm.md | from-architect, from-analyst, from-strategist |
| Architect | from-architect.md | from-pm, from-dev, from-devsecops |
| SM | from-sm.md | from-pm, from-dev, from-qa |
| Dev | from-dev.md | from-architect, from-sm, from-qa |
| QA | from-qa.md | from-dev, from-devsecops, from-architect |

**Message Format:**
```markdown
## [YYYY-MM-DD] → To: {Recipient/All}

**Subject:** Brief description
**Priority:** High/Medium/Low
**Requires Action:** Yes/No

Message details...

---
```

---

## Session Management

### Starting a Session

1. Activate agent
   ```bash
   /dev
   ```

2. Agent auto-loads context:
   - Project configuration
   - Stack experience
   - Inter-agent notes
   - Current story (if any)

### Ending a Session

Always use `*exit` which:
1. Saves session context
2. Updates inter-agent notes
3. Records session metrics

**Never close without `*exit`** - context will be lost.

---

## Full-Stack Projects

For projects with separate backend and frontend:

### Configuration
In `.jvis/core-config.yaml`:
```yaml
projectType: fullstack
agentRoles:
  specialists:
    backend: api    # or prisma, rust
    frontend: frontend
```

### Story Context

Every story must specify:
- `context: backend` - Server work only
- `context: frontend` - Client work only
- `context: fullstack` - Both parts required

### Coordination

SM coordinates via `docs/notes/coordination.md`:
```markdown
## Current Sprint Status

### Backend Team
- **Agent:** /api
- **Status:** In Progress
- **Current Story:** story-1.3

### Frontend Team
- **Agent:** /frontend
- **Status:** Waiting
- **Current Story:** None
- **Blockers:** Waiting for API from story-1.3
```

---

## Quality Gates Reference

### Gate File Structure
```yaml
story: "1.3-user-authentication"
epic: "auth"
date: "2026-01-28"
reviewer: "qa"

decision: PASS  # PASS | CONCERNS | FAIL | WAIVED

summary: "Implementation meets requirements with good test coverage"

findings:
  critical: []
  major: []
  minor:
    - "Consider adding rate limiting in future iteration"

metrics:
  test_coverage: 87%
  code_quality_score: 8.5/10
  security_score: 9/10

recommendations:
  - "Add integration tests for edge cases"
```

### Gate Criteria

**PASS requires:**
- All acceptance criteria met
- Tests pass
- No critical/major findings
- Code follows standards
- Security review passed

**CONCERNS triggers:**
- Minor issues found
- Test coverage < 80%
- Minor security concerns
- Technical debt noted

**FAIL triggers:**
- Acceptance criteria not met
- Critical bugs found
- Security vulnerabilities
- Major architectural issues
- Tests failing

---

## Best Practices

### DO ✅

1. **Follow the agent sequence** - PM → Architect → SM → Dev → QA
2. **Read documentation first** - Stories contain all needed context
3. **Update only allowed sections** - Each agent has specific permissions
4. **Use inter-agent notes** - For async communication
5. **Save context before leaving** - Always use `*exit`
6. **Run tests before review** - Dev validates before QA
7. **Commit only after QA approval** - Gate must pass first

### DON'T ❌

1. **Skip agents** - Each phase is necessary
2. **Modify PRD during dev** - Go back to PM first
3. **Commit without tests** - Dev includes testing
4. **Ignore QA feedback** - Fix concerns before proceeding
5. **Close without saving** - Context will be lost
6. **Mix agent responsibilities** - Each agent has specific focus

---

## Quick Reference

### Agent Commands Summary

| Agent | Key Commands |
|-------|--------------|
| `/pm` | `*create-prd`, `*shard-prd` |
| `/architect` | `*create-full-stack-architecture`, `*shard-prd` |
| `/sm` | `*draft`, `*draft-fullstack`, `*story-checklist` |
| `/dev` | `*develop-story`, `*run-tests`, `*review-qa` |
| `/qa` | `*review`, `*gate`, `*trace` |

### Common Commands (All Agents)

| Command | Purpose |
|---------|---------|
| `*help` | Show available commands |
| `*load-context` | Load project context |
| `*save-context` | Save session context |
| `*exit` | Save and leave agent mode |

---

## Troubleshooting

### "Story has insufficient context"
→ Check that architecture.md exists and story references it

### "QA gate keeps failing"
→ Review findings, address ALL critical/major issues

### "Lost context after restart"
→ You didn't use `*exit`. Use `*load-context` to recover

### "Conflicting agent notes"
→ Check timestamps, latest entry takes precedence

### "Blocked on dependency"
→ Create blocker in `docs/notes/next-action.md`, notify SM

---

---

## Plan System (ADR-005/ADR-006)

The story workflow above is wrapped by an **execution plan system** that provides deterministic state tracking, risk-based quality gates, and auto-continue support.

### Plan File

Location: `docs/plans/active-plan.yaml` — the single source of truth for execution state.

```yaml
schema: 1
plan: "Project Name"
status: in_progress  # pending | in_progress | completed | abandoned

steps:
  - id: S1.1
    title: "Story description"
    agent: dev
    status: pending  # pending | in_progress | done | blocked | skipped
    gate: qa         # single or list: [qa, architect]
    risk: medium     # low | medium | high | critical
    depends_on: []
    report: null     # filled after completion

checkpoints:
  - id: CP1
    after_steps: [S1.1, S1.2, S1.3]
    reviewers: [architect, devsecops]
    status: pending
```

**Rules:**
- Only ONE active plan at a time
- Completed plans → `docs/plans/archive/`
- The plan is SSOT for execution state — `project-log.md` is a human journal, not state

### Risk-Based Quality Gates

Not every step needs every reviewer. Review intensity is proportional to risk:

| Risk | Required Gate | Example |
|------|---------------|---------|
| Critical | QA + Architect + DevSecOps | Auth, data model, crypto |
| High | QA + Architect | New API endpoint, CI pipeline |
| Medium | QA | CRUD, business logic |
| Low | Self-review (tests pass) | Docs, config, rename |

### Step Reports

After completing a step, the implementing agent writes a report to `docs/plans/reports/{step-id}-report.md`:

- Changes made (files, lines)
- Decisions and rationale
- Tests added/modified
- Risks and debt identified
- Notes for reviewers

Reports are mandatory for `medium` risk and above.

### Auto-Continue Protocol

When the user says "continua" / "continue" / "next":

1. Read `docs/plans/active-plan.yaml`
2. Find first step with `status: pending` AND all `depends_on` steps are `done`
3. If `type: review` → notify user which agent to invoke
4. If implementation → execute the step
5. Set `in_progress` → complete → write report → set `done`
6. Check if this triggers a checkpoint

### Epic Checkpoints

Mandatory after every epic. 4-phase protocol:

```
Phase A: /architect    → Deep review (principles, debt, logic)
Phase B: /devsecops    → Security review (attack surfaces, CVEs)
Phase C: /architect    → Consolidate findings → report for PM
Phase D: /pm           → Prioritize: blockers → stories, rest → backlog
```

**Checkpoint severity rules:**

| Severity | Action | Blocks next epic? |
|----------|--------|-------------------|
| Blocker | Fix immediately | Yes |
| Important | Story for next sprint | No |
| Nice-to-have | Backlog | No |

Reference: `docs/adr/ADR-005-executable-development-plans.md`, `docs/adr/ADR-006-plan-migration-on-update.md`

---

*JVIS Development Workflow v2.0*
