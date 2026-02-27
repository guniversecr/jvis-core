# Journey Complete

Mark a checkpoint as completed.

## Usage

```
/journey:complete {checkpoint_id}
/journey:complete {checkpoint_id} --notes "Additional context"
/journey:complete {checkpoint_id} --skip --reason "Not applicable"
```

## Instructions

### 1. Parse Arguments

- `checkpoint_id`: Required - ID from phases.yaml (e.g., "idea_documented", "wps_scored")
- `--notes`: Optional - Additional notes about completion
- `--skip`: Mark as skipped instead of completed
- `--reason`: Required if using --skip

### 2. Validate Checkpoint

1. Load `docs/journey/journey-state.yaml`
2. Verify checkpoint_id exists in phases.yaml
3. Check checkpoint is not already completed

### 3. Verify Artifacts (if applicable)

For checkpoints with artifact requirements:
1. Check if expected files exist
2. Validate content if quality check defined
3. Warn if artifacts missing (allow override)

```markdown
⚠️ **Artifact Verification**

Expected: `docs/ideation/idea-brief.md`
Status: Not found

Options:
1. Create the artifact first
2. Proceed anyway (not recommended)
3. Cancel
```

### 4. Update Journey State

```yaml
phases:
  {phase}:
    checkpoints:
      {checkpoint_id}:
        status: "completed"  # or "skipped"
        completed: "{today}"
        notes: "{user_notes}"
        artifacts:
          - "{found_artifacts}"
```

### 5. Add History Entry

```yaml
history:
  - date: "{today}"
    action: "checkpoint_completed"  # or "checkpoint_skipped"
    checkpoint: "{checkpoint_id}"
    phase: "{phase}"
    notes: "{notes}"
```

### 6. Update Metrics

Recalculate:
- `metrics.completed_checkpoints`
- `metrics.progress_percentage`

### 7. Check Phase Completion

If all checkpoints in current phase are complete:
- Notify user about gate check
- Update phase status to "completed" if gate passed

### 8. Display Confirmation

```markdown
# ✅ Checkpoint Completed

**Checkpoint:** {checkpoint_name}
**Phase:** {phase_name}

## Status

- Completed: {date}
- Artifacts: {count} verified
- Notes: {notes}

## Progress

**Phase Progress:** ████████░░ {X}%
**Overall Progress:** ████░░░░░░ {X}%

## Next Steps

{if more checkpoints}
Next checkpoint: **{next_checkpoint}**
Run `/journey:next` for details.
{else if gate pending}
All checkpoints complete! Run `/journey:gate` to pass the {phase} gate.
{end}
```

## For Skipped Checkpoints

```markdown
# ⏭️ Checkpoint Skipped

**Checkpoint:** {checkpoint_name}
**Reason:** {reason}

{if gate_blocker}
⚠️ **Warning:** This checkpoint is a gate blocker.
Skipping it may prevent passing the {phase} gate.
You may need to complete it later or request a gate waiver.
{end}
```

## Success Criteria

- [ ] Checkpoint ID validated
- [ ] Artifacts verified (if applicable)
- [ ] Journey state updated
- [ ] History entry added
- [ ] Metrics recalculated
- [ ] Next steps shown
