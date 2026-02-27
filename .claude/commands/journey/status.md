# Journey Status

Show current project journey status and progress.

## Instructions

Execute the journey status task to display:
1. Overall progress percentage
2. Current phase and checkpoint
3. Completed vs pending items
4. Next recommended action

Load and execute: `.jvis/tasks/journey-status.md`

If `docs/journey/journey-state.yaml` doesn't exist, suggest running `/journey:diagnose` first.

## Quick Reference

```
/journey:status           # Full status
/journey:status --compact # One-line summary
/journey:status --phase development  # Specific phase
```
