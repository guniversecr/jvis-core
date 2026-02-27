# ADR-005: Executable Development Plans with Iterative Quality Gates

**Status:** Approved
**Date:** 2026-02-21
**Author:** Winston — System Architect | JVIS Framework
**Triggered by:** User observation: agents lose execution state between sessions; QA reviews only happen at the end; no step-by-step tracking; no per-step reporting
**Scope:** Workflow infrastructure. New files and conventions. No changes to Python CLI source code.

---

## Context

### Problem Statement

The current JVIS development workflow has three structural deficiencies:

**1. No Executable State**

When PM creates a PRD and SM creates stories, the output is markdown documents. There is no machine-readable artifact that tracks:
- Which step is current
- Which steps are complete
- What comes next

When the user says "continúa" (continue), the agent must read `project-log.md`, `next-action.md`, `from-architect.md`, and infer state. This is slow, error-prone, and non-deterministic — two agents reading the same files may reach different conclusions about what's next.

**Evidence:** The `resume-session.md` task reads 6 files to reconstruct state. The `/dev` agent's `*develop-story` command has no way to know which story is "next" without the user specifying it.

**2. Quality Gates Are Terminal, Not Iterative**

The current workflow is linear:

```
PM → Architect → SM → Dev → Dev → Dev → ... → QA
```

QA reviews happen after all development is done. The Architect reviews architecture once (before development). DevSecOps reviews security once (after audit). This means:

- Technical debt accumulates across multiple stories before detection
- Security issues compound — a bad pattern in Story 1 gets copy-pasted to Stories 2-5
- Architecture drift goes unnoticed until the final review
- Cost of fixing grows exponentially with delay

**Evidence:** In Epics 8-10 (quality hardening), QA reviewed 10 stories in a single batch. Stories 8.3-8.5 were all PASS (88-95), but if 8.3 had introduced a structural problem, it would have propagated through 8.4 and 8.5 before detection.

**3. No Per-Step Reporting**

When Dev completes a story, the only artifacts are:
- The git commit
- The story file with ACs checked off
- An optional update to `project-log.md`

There is no structured report answering: What changed? What decisions were made? What risks exist? QA must perform archaeology — reading git diffs, inferring intent, cross-referencing ACs — instead of reviewing a prepared report.

**Evidence:** QA gate files (`docs/qa/gates/*.yml`) contain `evidence.trace` but these are written by QA after review, not by Dev at completion time.

### What the User Proposed

1. A step-by-step execution plan where each step can be marked complete
2. Iterative UAT, Architect, and DevSecOps reviews (not just at the end)
3. Per-step reports for reviewers

### Industry Precedents

| Practice | Source | Relevance |
|----------|--------|-----------|
| Definition of Done checklists | Scrum Guide | Each increment has verifiable completion criteria |
| Shift-Left Testing | DORA/Google DevOps | Find defects early, when cost to fix is lowest |
| Risk-based review gates | SAFe, ISO 27001 | Review intensity proportional to risk, not uniform |
| Build logs / step reports | CI/CD (GitHub Actions, Jenkins) | Each step produces structured output for later analysis |
| Executable specifications | BDD (Cucumber, SpecFlow) | Specs that are both human-readable and machine-executable |

---

## Decision

### Component 1: Plan File (Executable State)

Introduce a **plan file** as the single source of truth for execution state. Located at `docs/plans/active-plan.yaml`.

**Format:**

```yaml
schema: 1
plan: "JVIS v4.0.0 Launch Readiness"
prd_ref: "docs/prd.md"
created: "2026-02-21"
updated: "2026-02-21"
status: in_progress  # pending | in_progress | completed | abandoned

steps:
  - id: S1.1
    title: "Fix install_framework() — 5 brownfield bugs"
    epic: 1
    story_ref: "docs/stories/S1.1.story.md"
    agent: dev
    status: pending  # pending | in_progress | done | blocked | skipped
    gate: qa  # single reviewer
    risk: high  # low | medium | high | critical
    depends_on: []
    report: null  # filled after completion: "docs/plans/reports/S1.1-report.md"
    started_at: null
    completed_at: null

  - id: S1.2
    title: "Hatchling force-include for wheel packaging"
    epic: 1
    story_ref: "docs/stories/S1.2.story.md"
    agent: dev
    status: pending
    gate: [qa, architect]  # multiple reviewers
    risk: high
    depends_on: [S1.1]
    report: null
    started_at: null
    completed_at: null

  - id: S1.2-review
    title: "Architect review: wheel packaging approach"
    epic: 1
    agent: architect
    status: pending
    gate: null  # review steps don't have their own gate
    risk: low
    depends_on: [S1.2]
    report: null
    type: review  # differentiates from implementation steps
    review_scope: [S1.1, S1.2]  # what this review covers
    started_at: null
    completed_at: null

checkpoints:
  - id: CP1
    title: "Architecture + Security checkpoint: Epic 1 complete"
    after_steps: [S1.1, S1.2, S1.3, S1.4]
    reviewers: [architect, devsecops]
    status: pending
    report: null
    scope: "Holistic review of brownfield fix, wheel packaging, E2E test, and publish pipeline"
```

**Rules:**
- Only ONE active plan at a time (`active-plan.yaml`)
- Completed plans move to `docs/plans/archive/{plan-name}-{date}.yaml`
- The plan is the SSOT for execution state — `project-log.md` is a human-readable journal, not state
- Any agent can read the plan; only the assigned agent or SM updates step status

### Component 2: Gate Matrix (Risk-Based Reviews)

Not every step needs every reviewer. Define review intensity by **risk level** and **change type**:

**Gate Matrix:**

| Risk | Change Type | Required Gate | Example |
|------|-------------|---------------|---------|
| Critical | Security, auth, data model | QA + Architect + DevSecOps | Add auth middleware |
| High | New module, API change, infra | QA + Architect | New API endpoint, CI pipeline |
| Medium | Feature with business logic | QA | CRUD implementation |
| Low | Refactor, docs, config | Self-review (tests pass) | Rename variable, update README |

**Assignment rules:**
- Risk level is set by the SM when creating the plan (based on story complexity and type)
- Architect can escalate any step's risk level
- DevSecOps is auto-included when step touches: auth, crypto, user input handling, CI/CD, dependencies
- QA is always included for `medium` risk and above

**Checkpoint triggers:**
- After every epic completion (mandatory) — full 4-phase protocol (Architect → DevSecOps → Architect consolidation → PM prioritization)
- After every 5 implementation steps (if no epic boundary crossed)
- When Architect or DevSecOps explicitly requests one

### Component 3: Step Reports (Structured Post-Completion Output)

When an agent completes a step, it writes a **step report** to `docs/plans/reports/{step-id}-report.md`.

**Template:**

```markdown
# Step Report: {step-id} — {title}

**Agent:** {agent}
**Date:** {YYYY-MM-DD}
**Duration:** {estimated time spent}
**Status:** Done

## Changes

| File | Action | Lines Changed |
|------|--------|---------------|
| `src/jvis/scaffold/framework.py` | Modified | +45 / -32 |
| `tests/test_framework.py` | Created | +120 |

## Decisions Made

1. **{Decision}** — {Rationale}. Alternative considered: {alternative}. Rejected because: {reason}.

## Tests

- **New:** {count} tests added
- **Modified:** {count} tests changed
- **Total passing:** {count}
- **Coverage delta:** {+/-}%

## Risks & Debt

- [ ] {Risk description} — Severity: {low/medium/high}. Mitigation: {description}.
- None identified (if clean)

## Notes for Reviewers

- {Specific things QA/Architect/DevSecOps should verify}

## Ready For

- [x] QA review
- [ ] Architect review (if gate requires)
- [ ] DevSecOps review (if gate requires)
```

**Rules:**
- Reports are written by the implementing agent (Dev, Infra, etc.) — not by QA
- Reports are mandatory for `medium` risk and above
- Reports for `low` risk steps are optional (a commit message suffices)
- Reviewers annotate the report with their findings (append a `## Review: {agent}` section)

### Component 4: Auto-Continue Protocol

When the user says "continúa" (or "continue", "next", "proceed"):

```
1. Read `docs/plans/active-plan.yaml`
2. Find the first step with status: pending AND all depends_on steps are "done"
3. If the step has type: review → notify user which agent to invoke
4. If the step has type: implementation (default) → execute
5. Before executing: set step status to "in_progress", update started_at
6. After completing: set step status to "done", update completed_at, write report
7. Check if this triggers a checkpoint → notify user
```

If no executable step exists (all pending steps are blocked), report the blockage clearly:

```
No executable steps. Blocked:
- S1.3 is blocked by S1.2 (status: in_progress)
- S1.4 is blocked by S1.3 (status: pending)

Next action: Complete S1.2 or unblock manually.
```

### Component 4b: Plan Dynamics (Mutability Rules)

The plan is a **living document** — it adapts as the project evolves. Steps can be added, reordered, re-assigned, or removed during execution. Checkpoints are **immutable** — they must always execute at epic boundaries.

**What CAN change:**

| Mutation | When | Who |
|----------|------|-----|
| Add steps | During execution, when new work is discovered (e.g., frontend work blocking dev) | Any agent, validated by SM |
| Remove steps | When work is no longer needed (requirements changed) | SM or PM |
| Re-assign agent | When a step requires a different specialist than originally planned | Any agent |
| Change dependencies | When execution order needs adjustment | SM |
| Change risk level | When implementation reveals higher/lower risk than estimated | Architect can escalate; SM can adjust |
| Change status | Normal execution flow (pending → in_progress → done) | Assigned agent |
| Add fix steps | After review findings (e.g., S1.2-FIX-1) | Review agent + SM |

**What CANNOT change:**

| Immutable | Why |
|-----------|-----|
| Checkpoints | Epic-level validation is mandatory. Checkpoints can be updated with findings but never deleted or skipped. |
| Checkpoint reviewers | Architect + DevSecOps review at every epic boundary is non-negotiable |
| Completed step status | A `done` step cannot revert to `pending` (create a new fix step instead) |
| Step reports | Once written, reports are append-only (reviewers add sections, never delete) |

**Auto-continue with plan mutation:**

When the auto-continue protocol detects all pending steps are blocked, it MUST NOT just report the blockage — it must **propose plan mutations** to unblock:

```
1. Read active-plan.yaml
2. Find first step with status: pending AND all depends_on are "done"
3. If found → execute normally (Component 4)
4. If NOT found (all blocked):
   a. Identify the blocking chain (what's blocking what)
   b. Determine if the blockage is:
      - AGENT MISMATCH: Step assigned to wrong agent → propose re-assignment
      - MISSING STEP: Required work not in plan → propose new step(s)
      - DEPENDENCY ERROR: Circular or incorrect dependency → propose fix
   c. Present mutation proposal to user:
      "No executable steps. Proposed plan update:
       + Add S9.1 (frontend): Build component library [NEW]
       + Add S9.2 (frontend): Implement page templates [NEW]
       ~ S11.1 (dev): Change depends_on from [S1.3] to [S9.2]
       Checkpoints CP1, CP9 preserved (immutable).
       Approve? [yes/edit/reject]"
   d. If approved → mutate plan, update `updated` timestamp
   e. If rejected → halt and wait for manual intervention
5. After any mutation: re-run step 2 to find next executable step
```

**Post-review reconciliation:**

After a review step produces findings, the plan MUST be updated:

```
1. Review agent writes findings to step report
2. If findings have severity "blocker" or "important":
   a. Create fix steps (S{id}-FIX-N) with depends_on: [review-step]
   b. Update downstream dependencies to depend on fix steps
   c. Checkpoint after_steps list is auto-extended to include fix steps
3. If all findings are "low" or "nice-to-have":
   a. Add to backlog (no plan mutation)
4. Updated timestamp on plan reflects the mutation
```

### Component 5: Epic Checkpoints

Checkpoints are holistic reviews that happen at epic boundaries. They differ from step-level gates:

| Aspect | Step Gate | Checkpoint |
|--------|-----------|------------|
| Scope | Single step | All steps in an epic |
| Reviewer | Per risk matrix | Architect + DevSecOps |
| Focus | "Did this step do what it should?" | "Is the accumulated state healthy?" |
| Output | Gate PASS/CONCERNS/FAIL | Consolidated report with prioritized action items |

**Checkpoint execution preconditions (ALL must be true):**

1. ALL steps in `after_steps` have `status: done`
2. ALL QA fix steps (type: fix, created from CONCERNS verdicts) for this epic have `status: done`
3. ALL review fix steps (type: fix, created from review findings) for this epic have `status: done`
4. NO step in this epic has a FAIL verdict pending rework

If ANY precondition is not met, the checkpoint CANNOT execute. The continue-plan protocol must report exactly which precondition is failing and what steps need to complete first.

**QA gate verdicts and their impact on checkpoints:**

| QA Verdict | Step Status | Checkpoint Impact |
|------------|-------------|-------------------|
| PASS | `done` | No impact — step counts as complete |
| CONCERNS | `done` + fix steps created | Fix steps added to checkpoint's `after_steps`. Checkpoint BLOCKED until all fix steps are `done` |
| FAIL | `in_progress` (returned to dev) | Checkpoint BLOCKED — step is not `done` |
| WAIVED | `done` + waiver documented | Checkpoint reviewers informed — may override waiver |

**Checkpoint protocol (4 phases):**

```
Phase A: /architect — Deep code review (scoped to epic changes)
  - Validate JVIS principles compliance (SSOT, SOLID, Clean Architecture, Clean Code)
  - Identify technical debt, logic errors, code quality issues
  - Check for architecture drift from original design
  - Output: Architecture health report

Phase B: /devsecops — Security review (scoped to epic changes)
  - Review attack surfaces, input validation, secrets handling
  - Check dependencies for known CVEs
  - Verify OWASP compliance on new boundaries
  - Output: Security health report

Phase C: /architect — Consolidation
  - Review and validate devsecops findings (intervene only when findings
    have architectural implications; pure security items pass through as-is)
  - Merge architecture + security findings into single checkpoint report
  - Classify each finding by severity
  - Output: Consolidated checkpoint report for PM

Phase D: /pm — Prioritization
  - Review checkpoint report
  - Classify findings into actionable work:

    | Severity | Action | Blocks next epic? |
    |----------|--------|-------------------|
    | Blocker  | Create immediate story, fix before proceeding | Yes |
    | Important | Create story for next sprint | No |
    | Nice-to-have | Add to backlog | No |

  - Update PRD/stories if needed
  - Give go/no-go for next epic
```

**Scope constraint:** Each checkpoint reviews ONLY changes since the last checkpoint. Previously reviewed and approved code is not re-audited unless a finding reveals systemic issues.

**Checkpoint report template:**

```markdown
# Checkpoint: {checkpoint-id} — {title}

**Reviewers:** Architect, DevSecOps
**Date:** {YYYY-MM-DD}
**Steps covered:** {S1.1, S1.2, S1.3, S1.4}

## Architecture Health

- [ ] No architecture drift from original design
- [ ] Dependencies point inward (Clean Architecture)
- [ ] No new SSOT violations
- [ ] No unplanned coupling between modules

## Security Health

- [ ] No new attack surfaces introduced
- [ ] Input validation on all new boundaries
- [ ] No hardcoded secrets or credentials
- [ ] Dependencies have no known CVEs

## Findings

| # | Finding | Severity | Source | Recommended Action |
|---|---------|----------|--------|-------------------|
| 1 | {description} | Blocker/Important/Nice-to-have | Architect/DevSecOps | {fix now / next sprint / backlog} |

## Verdict

**Continue:** Yes / Yes with corrections / No (stop and fix)

## Blocker Corrections (must fix before next epic)

1. {Correction} — Assigned to: {agent}
```

---

## Consequences

### Positive

1. **Deterministic "continue"** — Agent reads one file, finds next step. No inference, no ambiguity.
2. **Early defect detection** — Shift-left gates catch issues per-step, not per-project.
3. **Traceable decisions** — Every step has a report. Six months from now, you can answer "why was this done this way?"
4. **Proportional overhead** — Low-risk steps have minimal process; high-risk steps get full scrutiny.
5. **Checkpoint safety net** — Even if step-level gates miss drift, checkpoints catch it at epic boundaries.
7. **PM feedback loop** — Checkpoint findings flow back to PM for prioritization, ensuring only blockers delay progress while improvements are tracked as stories.
6. **Session-independent** — Plan state persists in YAML, not in agent memory or chat context.

### Negative

1. **More files** — Each plan generates: 1 plan YAML + N report files + M checkpoint files. Mitigated: archived after completion.
2. **Process overhead for small tasks** — A 3-line fix still requires reading/updating the plan file. Mitigated: `low` risk steps have optional reports; plan file is small and fast to parse.
3. **SM workload increases** — SM must define risk levels and gate assignments per step. Mitigated: gate matrix provides clear defaults; most assignments are mechanical.

### Neutral

1. **No Python code changes** — This is a workflow/convention change, not a product change. The plan file is consumed by agents (via prompts), not by `jvis` CLI.
2. **Backward compatible** — Existing stories and QA gates continue to work. The plan file is additive.
3. **No new dependencies** — YAML parsing already exists in every agent's toolchain.

---

## Implementation Plan

### Phase 1: Foundation (3 steps)

| Step | What | Agent | Effort |
|------|------|-------|--------|
| 1 | Create `docs/plans/` directory structure + `active-plan.yaml` schema | SM/Architect | 30min |
| 2 | Create step report template at `.jvis/templates/step-report-tmpl.md` | Architect | 30min |
| 3 | Create checkpoint report template at `.jvis/templates/checkpoint-report-tmpl.md` | Architect | 30min |

### Phase 2: Agent Integration (4 steps)

| Step | What | Agent | Effort |
|------|------|-------|--------|
| 4 | Update `/dev` agent: on `*develop-story`, read plan → find assigned step → set `in_progress` → write report on completion → set `done` | Dev (self-modify task) | 1h |
| 5 | Update `/qa` agent: on `*gate`, read step report + plan gate assignment → produce gate YML | QA (self-modify task) | 1h |
| 6 | Update `/sm` agent: on `*draft`, generate plan YAML alongside story files, with risk + gate assignments | SM (self-modify task) | 1h |
| 7 | Create "continue" task (`.jvis/tasks/continue-plan.md`) — the auto-continue protocol | Architect | 30min |

### Phase 3: Validation (2 steps)

| Step | What | Agent | Effort |
|------|------|-------|--------|
| 8 | Dry-run: create a plan for the current PRD (v4.0.0 launch) and execute 2 steps end-to-end | Dev + QA | 1h |
| 9 | Retrospective: evaluate overhead vs. value after the dry-run; adjust gate matrix if needed | Architect + PM | 30min |

**Total estimated effort:** ~6 hours

### Execution Order

```
1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9
         (Phase 1)  (Phase 2 — can partially parallelize 4,5,6)  (Phase 3)
```

---

## Files Affected

### New Files

| File | Purpose |
|------|---------|
| `docs/plans/active-plan.yaml` | Current execution plan (SSOT for state) |
| `docs/plans/reports/` | Step reports directory |
| `docs/plans/checkpoints/` | Checkpoint reports directory |
| `docs/plans/archive/` | Completed plans archive |
| `.jvis/templates/step-report-tmpl.md` | Step report template |
| `.jvis/templates/checkpoint-report-tmpl.md` | Checkpoint report template |
| `.jvis/tasks/continue-plan.md` | Auto-continue protocol task |

### Modified Files

| File | Change |
|------|--------|
| `.jvis/agents/core/dev.yaml` | Add plan-aware step to `*develop-story` |
| `.jvis/agents/core/qa.yaml` | Add plan-aware step to `*gate` |
| `.jvis/agents/core/sm.yaml` | Add plan generation to `*draft` |
| `.jvis/core-config.yaml` | Add `plans` section with paths |
| `docs/notes/from-architect.md` | ADR-005 announcement |

### Unchanged

- All Python source code (`src/jvis/`)
- All tests (`tests/`)
- All existing story files and QA gates

---

## Alternatives Considered

### A. Use Claude Code's built-in TodoWrite/TaskCreate

**Rejected.** TodoWrite is session-scoped — it doesn't persist across conversations. The plan file must survive session boundaries, which requires a file on disk.

### B. Embed plan state in `project-log.md`

**Rejected.** Violates SSOT — `project-log.md` is a journal for humans, not a state machine for agents. Mixing state tracking with narrative logging creates parsing ambiguity.

### C. Every step gets full Architect + DevSecOps + QA review

**Rejected.** Overhead would be ~3x the implementation time. Risk-based gating provides the same safety with proportional cost. A README update does not need a security review.

### D. No checkpoints — rely only on per-step gates

**Rejected.** Per-step gates verify individual correctness but miss systemic drift. A checkpoint catches "each step is fine individually but together they've drifted from the architecture."

---

## Open Questions

1. **Should the plan file support parallel steps?** Current design is sequential with dependencies. True parallelism (two developers working simultaneously) would require conflict resolution. **Recommendation:** Defer — JVIS is single-developer workflow for now.

2. **Should checkpoint frequency be configurable?** Current: every epic + every 5 steps. Some projects may want more or fewer. **Recommendation:** Add to `core-config.yaml` as `plans.checkpoint_frequency: 5` with a sensible default.

3. **Should step reports be generated automatically from git diff?** Possible to auto-fill the "Changes" table. **Recommendation:** Partially — auto-populate file changes, but decisions and risks must be human/agent-written.

---

*This document was generated using JVIS Framework*
*Agent: Winston — System Architect*
*Date: 2026-02-21*
