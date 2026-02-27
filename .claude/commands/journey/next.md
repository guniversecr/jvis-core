# Journey Next

Show and optionally execute the next checkpoint in the journey.

## Instructions

### 1. Load Journey State

Read `docs/journey/journey-state.yaml`

If not found:
```
Journey not initialized. Run `/journey:start` or `/journey:diagnose` first.
```

### 2. Find Next Checkpoint

Logic:
1. Get current phase
2. Find first checkpoint in current phase with status != "completed"
3. If all checkpoints complete, check gate status
4. If gate passed, move to next phase

### 3. Display Next Checkpoint

```markdown
# ⏭️ Next Checkpoint

**Phase:** {phase_name} {icon}
**Checkpoint:** {checkpoint_name}

## Description

{checkpoint_description}

## Criteria

- [ ] {criterion_1}
- [ ] {criterion_2}
- [ ] {criterion_3}

## How to Complete

**Agent:** `{agent}`
**Command:** `{command}`

{if manual}
This checkpoint requires manual work. After completing:
```
/journey:complete {checkpoint_id}
```
{else}
Run the agent command above. The checkpoint will be marked complete when artifacts are created.
{end}

## Expected Artifacts

- `{artifact_path_1}`
- `{artifact_path_2}`

---

*Progress: {current}/{total} in {phase_name}*
```

### 4. Handle Special Cases

#### Gate Approaching
```markdown
# ⚠️ Gate Check Required

You've completed all checkpoints in **{phase_name}**.

Before proceeding to **{next_phase}**, pass the gate:

```
/journey:gate
```
```

#### Journey Complete
```markdown
# 🎉 Journey Complete!

Congratulations! All checkpoints completed.

**Final Status:**
- Phases completed: 5/5
- Checkpoints completed: 35/35
- Gates passed: 5/5

Your product has followed the complete journey from ideation to production.

## Recommended Next Steps

1. Continue monitoring PMF metrics
2. Plan next iteration based on user feedback
3. Consider scaling if PMF > 40%

Run `/strategist` with `*pmf-check` for ongoing measurement.
```

## Options

- `--execute`: After showing next checkpoint, offer to execute the recommended command
- `--skip`: Show how to skip the current checkpoint

## Success Criteria

- [ ] Next checkpoint identified
- [ ] Clear instructions provided
- [ ] Agent and command specified
- [ ] Expected artifacts listed
- [ ] Progress shown
