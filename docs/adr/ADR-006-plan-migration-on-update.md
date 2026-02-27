# ADR-006: Plan System Migration on JVIS Update

**Status:** Approved
**Date:** 2026-02-21
**Author:** Winston — System Architect | JVIS Framework
**Triggered by:** ADR-005 introduced the plan system, but existing projects have no way to adopt it when JVIS is updated. Need a migration path.
**Scope:** Workflow infrastructure. New task files and conventions. No changes to Python CLI source code.
**Depends on:** ADR-005 (Executable Development Plans)

---

## Context

### Problem Statement

ADR-005 introduced the Executable Development Plans system (plan file, gate matrix, step reports, checkpoints). This works for **new** projects that start with the plan system from day one. But JVIS is already installed in existing projects (e.g., GAIAA) that have:

- PRDs already written
- Stories already created
- Work already completed (with QA gates)
- `core-config.yaml` without the `plans` section

When these projects update JVIS (`update-project.sh` or future `jvis update`), they need:

1. **Plan infrastructure deployed** — New task files, templates, directories
2. **Config migrated** — `plans` section added to `core-config.yaml`
3. **Existing work recognized** — A retroactive plan generated from PRD/stories/QA gates with correct status (`done` for completed work, `pending` for future work)

Without this, existing projects must either:
- Manually create `active-plan.yaml` (error-prone, tedious)
- Ignore the plan system entirely (lose the benefits of ADR-005)
- Start a new plan that doesn't reflect their history (lose traceability)

### Current Update Mechanisms

| Mechanism | Behavior | Plan-Awareness |
|-----------|----------|----------------|
| `update-project.sh` (bash) | Replaces `.jvis/` dirs, preserves `core-config.yaml`, backs up first | None — tasks/templates deploy automatically (dir copy), but config section is lost (backup restore) |
| `install_framework()` (Python) | Merges `.jvis/` dirs (`dirs_exist_ok=True`), overwrites config files | None — same as above but overwrites config instead of preserving |

**Key insight:** The task files and templates WILL deploy automatically because `update-project.sh` replaces the entire `.jvis/tasks/` and `.jvis/templates/` directories. The problem is specifically:
1. `core-config.yaml` — the `plans` section is not merged (bash restores backup, Python overwrites)
2. `docs/plans/` directory structure — not created automatically
3. No retroactive plan generation

---

## Decision

### Three-layer migration via task files (no Python code)

All migration logic lives in JVIS task files (`.jvis/tasks/*.md`) executed by agents. This is consistent with ADR-005's approach: workflow/convention changes, not product code.

### Layer 1: Config Migration Task

**File:** `.jvis/tasks/migrate-config.md`

**Purpose:** Detect and fix missing sections in `core-config.yaml` after a JVIS update.

**Workflow:**

```
1. Read `core-config.yaml`
2. Check for `plans` section
3. If missing:
   a. Read the reference config from the JVIS source (`.jvis/core-config.yaml` in repo)
   b. Extract the `plans` section
   c. Append to project's `core-config.yaml` (preserve existing content)
   d. Report: "Added `plans` section to core-config.yaml"
4. If present: verify all required keys exist (plansLocation, activePlan, gateMatrix, etc.)
   - If keys missing: add defaults
   - If all present: "Config is current"
5. Create missing directories:
   - docs/plans/
   - docs/plans/reports/
   - docs/plans/checkpoints/
   - docs/plans/archive/
```

**Trigger:** Automatically executed by `resume-session.md` on session start (added as a pre-check), OR manually via `/sm *migrate-config`.

### Layer 2: Plan Detection Task

**File:** `.jvis/tasks/detect-plan-state.md`

**Purpose:** Analyze project to determine plan migration readiness and current state.

**Workflow:**

```
1. Check if `active-plan.yaml` already exists
   - If exists AND status is pending/in_progress: "Plan already exists. No migration needed."
   - If exists AND status is completed/abandoned: "Archived plan found. Migration can create new plan."
   - If not exists: proceed to detection

2. Detect available inputs:
   a. PRD: Read core-config → prd.prdFile → check if file exists
   b. Stories: Glob docs/stories/*.md → list found stories
   c. QA Gates: Glob docs/qa/gates/*.yml → list found gates
   d. Project Log: Read last 5 entries from project-log.md

3. Categorize project state:

   | State | PRD | Stories | QA Gates | Recommended Action |
   |-------|-----|---------|----------|-------------------|
   | pristine | No | No | No | "No plan inputs found. Start with /pm *create-prd" |
   | prd-only | Yes | No | No | "PRD found. Create stories first: /sm *draft, then generate plan" |
   | stories-ready | Yes | Yes | No | "PRD + stories found. Ready to generate plan: /sm *generate-plan" |
   | partially-done | Yes | Yes | Some | "Work in progress detected. Ready for retroactive migration." |
   | fully-done | Yes | Yes | All | "All work appears complete. Generate archival plan." |

4. Present findings to user with recommended action
```

### Layer 3: Retroactive Plan Generation Task

**File:** `.jvis/tasks/migrate-to-plans.md`

**Purpose:** Generate `active-plan.yaml` from existing PRD, stories, and QA gates, with correct status per step.

**Workflow:**

```
1. PREREQUISITES:
   - Config migration done (Layer 1)
   - Plan detection shows "stories-ready" or "partially-done" or "fully-done"
   - No active plan exists (or user confirms overwrite)

2. READ INPUTS:
   a. PRD file → extract epic numbers, story IDs, titles
   b. Story files → for each story:
      - Extract: title, complexity, technical notes, AC count
      - Assess risk using generate-plan.md heuristics (keywords → risk level)
   c. QA gate files → for each gate:
      - Extract: verdict (PASS/FAIL/CONCERNS), score, date
      - Map to story ID (from filename pattern: {epic}.{story}-{slug}.yml)

3. BUILD STEP LIST:
   For each story found in PRD order:
   a. Create step entry with:
      - id: from PRD (S{epic}.{story})
      - title: from story file
      - story_ref: path to story file
      - risk: from heuristic assessment
      - gate: from gate matrix based on risk
      - depends_on: sequential within epic (S1.1 → S1.2 → S1.3)
   b. Determine status:
      - If QA gate exists AND verdict is PASS → status: done, completed_at: gate date
      - If QA gate exists AND verdict is FAIL → status: in_progress
      - If QA gate exists AND verdict is CONCERNS → status: done (concerns noted)
      - If no QA gate → status: pending
   c. Insert review steps for high/critical (per generate-plan.md rules)
      - If the reviewed steps are already `done`, mark review as `done` too

4. BUILD CHECKPOINTS:
   - One per epic (mandatory)
   - Mark as `done` if all steps in that epic are `done`

5. DETERMINE PLAN STATUS:
   - If all steps done → status: completed
   - If any step in_progress → status: in_progress
   - If no steps started → status: pending
   - If mix of done and pending → status: in_progress

6. GENERATE YAML:
   Write docs/plans/active-plan.yaml using generate-plan.md schema

7. PRESENT SUMMARY:
   Show user:
   ```
   ## Retroactive Plan Generated: {plan name}

   **Source:** {prd_file}
   **Steps:** {total} ({done} done, {in_progress} in progress, {pending} pending)
   **Checkpoints:** {total} ({done_cp} done, {pending_cp} pending)

   ### Migration Map
   ✓ S1.1 — {title} [done] — QA gate: PASS (score)
   ✓ S1.2 — {title} [done] — QA gate: PASS (score)
   → S1.3 — {title} [pending] — Next executable step
   ○ S1.4 — {title} [pending] — Blocked by S1.3

   ### Verify
   Please review the generated plan. If any step status is incorrect,
   edit docs/plans/active-plan.yaml directly.

   Say 'continúa' to proceed with the next pending step.
   ```

8. HALT — wait for user confirmation
```

### Integration with Existing Workflows

#### resume-session.md (already updated in ADR-005)

Add a config health check before the plan fast-path:

```
### 0.5 Config Health Check (before Step 1)

- Read core-config.yaml
- If `plans` section is missing:
  - Notify: "Plan system not configured. Run *migrate-config to set up."
  - Add to Priority Tasks
- If `plans` section exists but `docs/plans/` directory missing:
  - Create directories silently
```

#### update-project.sh

Add post-update hook after core files are deployed:

```bash
# After update_core_files():
echo "Checking plan system configuration..."
if ! grep -q "^plans:" "$PROJECT_DIR/.jvis/core-config.yaml" 2>/dev/null; then
    echo "⚠ Plan system not configured. Run: /sm *migrate-config"
fi
```

This is a notification only — the actual migration is performed by agents, not bash.

#### SM agent (sm.yaml)

Add new command:

```yaml
- migrate-config: "Execute task migrate-config.md — Add plan system config to existing project"
- migrate-to-plans: "Execute task migrate-to-plans.md — Generate retroactive plan from existing PRD/stories/QA gates"
```

### Schema Versioning

The plan file has `schema: 1`. Future JVIS updates may change the schema. Migration must handle this:

```
Schema Migration Rules:
- schema: 1 → Current format (ADR-005)
- Future schema: 2 → Would add new fields or change structure

Migration task checks schema version:
1. Read active-plan.yaml
2. If schema < CURRENT_SCHEMA:
   a. Apply migration transforms (schema-specific)
   b. Update schema field
   c. Report changes to user
3. If schema == CURRENT_SCHEMA: no action
4. If schema > CURRENT_SCHEMA: HALT — "Plan was created with a newer JVIS version. Update JVIS first."
```

For now, schema is 1 and no migrations exist. The mechanism is defined for forward compatibility.

---

## Consequences

### Positive

1. **Existing projects can adopt plan system** — Zero manual YAML writing required
2. **History preserved** — Completed work is recognized via QA gates, not lost
3. **Non-destructive** — Detection-first approach means no changes until user confirms
4. **Consistent with ADR-005** — Task files, no Python code, agent-executed
5. **Schema-forward** — Versioning built in from day one
6. **Incremental adoption** — Projects can run Layer 1 only (config), Layer 2 (detection), or full Layer 3 (migration) as needed

### Negative

1. **Agent-dependent accuracy** — Migration quality depends on agent correctly parsing PRD, stories, and gates. No programmatic guarantees.
2. **QA gate filename convention required** — Retroactive status detection relies on gate files following `{epic}.{story}-{slug}.yml` naming. If gates don't follow this, status can't be inferred.
3. **Manual verification needed** — User must review generated plan for accuracy. This is a feature (human-in-the-loop) but adds a step.

### Neutral

1. **No Python code** — Consistent approach but means we can't write tests for the migration logic. Quality depends on task file clarity.
2. **SM owns migration** — Consistent with SM owning plan generation (ADR-005), but adds SM workload.

---

## Implementation Plan

| Step | What | Agent | Effort |
|------|------|-------|--------|
| 1 | Create `.jvis/tasks/migrate-config.md` | Architect | 30min |
| 2 | Create `.jvis/tasks/detect-plan-state.md` | Architect | 30min |
| 3 | Create `.jvis/tasks/migrate-to-plans.md` | Architect | 1h |
| 4 | Add `migrate-config` and `migrate-to-plans` commands to SM agent | Dev | 15min |
| 5 | Add config health check to `resume-session.md` (Step 0.5) | Dev | 15min |
| 6 | Add post-update notification to `update-project.sh` | Dev | 15min |
| 7 | Dry-run: test migration on GAIAA project | Dev + QA | 1h |

**Total estimated effort:** ~3.5 hours

### Execution Order

```
1 → 2 → 3 → 4 → 5 → 6 → 7
(Task files)  (Integration)  (Validation)
```

---

## Files Affected

### New Files

| File | Purpose |
|------|---------|
| `.jvis/tasks/migrate-config.md` | Config migration task (Layer 1) |
| `.jvis/tasks/detect-plan-state.md` | Plan state detection task (Layer 2) |
| `.jvis/tasks/migrate-to-plans.md` | Retroactive plan generation task (Layer 3) |

### Modified Files

| File | Change |
|------|--------|
| `.jvis/agents/core/sm.yaml` | Add `migrate-config`, `migrate-to-plans` commands + dependencies |
| `.jvis/tasks/resume-session.md` | Add config health check (Step 0.5) |
| `update-project.sh` | Add post-update notification for plan system |

### Unchanged

- All Python source code (`src/jvis/`)
- All tests (`tests/`)
- `active-plan.yaml` (migration creates it, not modifies it)
- ADR-005 (this ADR extends, not modifies)

---

## Alternatives Considered

### A. Python CLI command (`jvis migrate-plans`)

**Rejected.** Adds Python source LOC, requires tests, increases maintenance surface. The migration is a one-time workflow per project — task file instructions are sufficient and consistent with ADR-005's "no code changes" principle.

### B. Automatic migration on update (no user confirmation)

**Rejected.** Generating a plan retroactively involves interpreting PRD structure, story content, and QA gate results. These are heuristic — errors are possible. The user MUST review the generated plan before it becomes the execution SSOT. Silent auto-generation could create an incorrect plan that blocks development.

### C. Extend update-project.sh with full migration logic

**Rejected.** The bash script is already 4,700 lines. Adding YAML parsing, PRD reading, and plan generation in bash would be fragile and hard to maintain. Agent-executed task files leverage the LLM's ability to parse markdown/YAML and make judgment calls (risk assessment, status inference).

### D. Do nothing — let users create plans manually

**Rejected.** Manual YAML creation is error-prone and tedious. Users who update JVIS should get the plan system benefits without becoming YAML experts. The whole point of ADR-005 is reducing manual state management.

---

## Open Questions

1. **Should migrate-config run automatically on every session resume?** Currently proposed as a notification in resume-session.md. Auto-running could be convenient but adds overhead to every session. **Recommendation:** Notify only; user runs manually.

2. **What if PRD structure doesn't follow JVIS conventions?** The migration task assumes PRD has epics with numbered stories. Freeform PRDs can't be parsed reliably. **Recommendation:** HALT with guidance — "PRD doesn't follow JVIS epic/story structure. Use `/pm *create-prd` to restructure, or create `active-plan.yaml` manually."

3. **Should the migration support partial plans?** e.g., migrate only Epic 1 (done) and leave Epic 2-3 as pending placeholders without story files. **Recommendation:** Yes — steps without story files get `story_ref: null` and status `pending`, same as ADR-005's current plan.

---

*This document was generated using JVIS Framework*
*Agent: Winston — System Architect*
*Date: 2026-02-21*
