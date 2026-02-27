# JVIS Update

Update the JVIS framework in this project to the latest version and reconcile all project artifacts.

## Instructions

Execute the task defined in `.jvis/tasks/update-aicore.md`.

## Full Process

This workflow performs a **complete update cycle**, not just file copying:

1. **Version check** — Compare current vs source JVIS version
2. **File update** — Run `update-project.sh` to copy new framework files
3. **Post-update summary** — Show what changed (CHANGELOG / VERSION.yaml)
4. **Project reconciliation** (task: `post-update-reconciliation.md`):
   - Regenerate slash commands (`make generate`)
   - Validate `core-config.yaml` against new schema
   - Check `active-plan.yaml` compatibility (if plan exists)
   - Verify stack compatibility
   - Validate custom agent schemas
   - Run tests to catch regressions
   - Create actionable next steps in `docs/notes/next-action.md`

## After the Update

The reconciliation step creates specific next steps in `next-action.md`. Follow those.

For a deeper analysis of new capabilities available:
- `/workflows:project-upgrade` — Full upgrade analysis with agent recommendations
- `/workflows:post-upgrade` — Analyze project using newly installed capabilities

## Manual Alternative

If you prefer to run the update manually:

```bash
# From the JVIS source directory
./update-project.sh /path/to/this/project

# Then reconcile manually:
make generate          # Regenerate commands
make test              # Verify nothing broke
```
