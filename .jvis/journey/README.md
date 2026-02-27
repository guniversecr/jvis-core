# JVIS Journey System

Guides projects from idea to production through 5 phases with 35 checkpoints.

## Files

| File | Purpose |
|------|---------|
| `phases.yaml` | Phase and checkpoint definitions |
| `state-template.yaml` | Template for project journey state |

## Journey Phases

```
Ideation (5) → Validation (6) → Planning (8) → Development (7) → Production (7)
```

### Phase Details

| Phase | Checkpoints | Gate Requirement |
|-------|-------------|------------------|
| Ideation | 5 | WPS score >= 6, competitors analyzed |
| Validation | 6 | Problem validated (70%+), solution validated |
| Planning | 8 | PRD, architecture, documents sharded |
| Development | 7 | QA passed, security audited |
| Production | 7 | Deployed, monitoring active, PMF measured |

## Commands

```bash
/journey:start      # Initialize tracking
/journey:diagnose   # Detect state from artifacts
/journey:status     # Show progress
/journey:next       # Work on next checkpoint
/journey:complete   # Mark checkpoint done
/journey:gate       # Validate gate requirements
```

## Project State

Project journey state is stored in:
```
docs/journey/journey-state.yaml
```

## Brownfield Projects

For existing projects, `/journey:diagnose` scans artifacts to detect completed checkpoints and recommends next steps.
