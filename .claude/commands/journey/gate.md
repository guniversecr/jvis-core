# Journey Gate

Check gate requirements and transition to next phase.

## Usage

```
/journey:gate                    # Check current phase gate
/journey:gate --phase ideation   # Check specific phase gate
/journey:gate --waive --reason "..." # Waive gate (requires reason)
```

## Instructions

### 1. Load Gate Definition

From `.jvis/journey/phases.yaml`, get gate requirements for current phase.

### 2. Evaluate Requirements

For each requirement:
1. Check if referenced checkpoint is complete
2. Verify any conditions (e.g., score >= 6)
3. Track pass/fail status

### 3. Display Gate Status

```markdown
# 🚪 {Phase} Gate Check

**Phase:** {phase_name}
**Gate Status:** {PASS | PENDING | BLOCKED}

## Requirements

| Requirement | Status | Details |
|-------------|--------|---------|
| wps_scored (score >= 6) | ✅ PASS | Score: 7/10 |
| idea_documented | ✅ PASS | Completed 2024-01-15 |
| competitors_analyzed | ❌ PENDING | Not completed |

## Summary

- **Passed:** {X}/{Y}
- **Pending:** {X}
- **Blocked:** {X}

{if all passed}
## ✅ Gate Passed!

You can now proceed to **{next_phase}**.

Transition to next phase?
1. Yes - Move to {next_phase}
2. No - Stay in {current_phase} for refinement
{else}
## ⏳ Gate Not Ready

Complete the following before proceeding:

1. **{checkpoint}** - {how_to_complete}
   Agent: `{agent}` Command: `{command}`

{if has_blockers}
### ⚠️ Blockers

- {checkpoint}: {blocking_reason}
  This must be resolved before gate can pass.
{end}
{end}
```

### 4. Handle Gate Transition

If all requirements pass and user confirms:

1. Update current phase:
```yaml
phases:
  {current_phase}:
    status: "completed"
    completed: "{today}"
    gate:
      status: "passed"
      decision: "approved"
      decision_date: "{today}"
```

2. Update next phase:
```yaml
phases:
  {next_phase}:
    status: "in_progress"
    started: "{today}"
```

3. Update current_phase in state:
```yaml
current_phase: "{next_phase}"
```

4. Add history entry:
```yaml
history:
  - date: "{today}"
    action: "gate_passed"
    phase: "{current_phase}"
    notes: "Transitioned to {next_phase}"
```

### 5. Display Transition Confirmation

```markdown
# 🎉 Phase Transition Complete!

**From:** {current_phase} → **To:** {next_phase}

## {Next Phase} Overview

{phase_description}

### Checkpoints in this Phase

1. [ ] {checkpoint_1} - {description}
2. [ ] {checkpoint_2} - {description}
...

## First Checkpoint

**{first_checkpoint_name}**

{description}

Agent: `{agent}`
Command: `{command}`

---

Run `/journey:next` to start working on the first checkpoint.
```

### 6. Handle Gate Waiver

If `--waive` is used:

```yaml
phases:
  {current_phase}:
    gate:
      status: "waived"
      decision: "waived"
      decision_date: "{today}"
      decision_by: "user"
      notes: "{reason}"
```

Display warning:
```markdown
# ⚠️ Gate Waived

**Phase:** {phase_name}
**Reason:** {reason}

The following requirements were not met:
- {requirement_1}
- {requirement_2}

Proceeding to **{next_phase}** despite incomplete gate.

**Recommendation:** Document the rationale and consider completing
the skipped requirements later if possible.
```

## Gate Definitions by Phase

| Phase | Key Requirements | Blocker Checkpoints |
|-------|------------------|---------------------|
| Ideation | WPS >= 6, Idea documented, Competitors analyzed | wps_scored |
| Validation | Problem validated, Solution validated, 5+ interviews | problem_validated, solution_validated |
| Planning | PRD, Architecture, Documents sharded, Sprint planned | All required |
| Development | QA passed, Security audit, Integration tested | qa_passed, security_audited |
| Production | Deployed, Monitoring, PMF measured | All required |

## Success Criteria

- [ ] Gate requirements evaluated
- [ ] Clear pass/fail status shown
- [ ] Missing requirements listed with next steps
- [ ] Blockers highlighted
- [ ] Transition handled if approved
- [ ] Waiver documented if used
