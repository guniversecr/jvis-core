# Checkpoint: {checkpoint_id} — {title}

**Reviewers:** {reviewers}
**Date:** {date}
**Steps Covered:** {steps_covered}
**Triggered By:** {trigger}

---

## Architecture Health

- [ ] No architecture drift from original design
- [ ] Dependencies point inward (Clean Architecture)
- [ ] No new SSOT violations
- [ ] No unplanned coupling between modules
- [ ] File structure follows project conventions

## Security Health

- [ ] No new attack surfaces introduced
- [ ] Input validation on all new boundaries
- [ ] No hardcoded secrets or credentials
- [ ] Dependencies have no known CVEs
- [ ] Jinja2 SandboxedEnvironment used everywhere

## Code Quality

- [ ] All tests passing
- [ ] 0 Ruff violations
- [ ] No dead code introduced
- [ ] No magic numbers without documentation
- [ ] Clean Code principles followed

## Technical Debt Assessment

| Debt Item | Severity | Introduced In | Recommended Action |
|-----------|----------|---------------|-------------------|
| {description} | {low/med/high} | {step-id} | {fix now / next sprint / accept} |

## Accumulated Metrics

- **Tests:** {total passing}
- **Source LOC delta:** {+/-}
- **Coverage:** {%}
- **Lint violations:** {count}

## Verdict

<!-- One of: Continue | Continue with corrections | Stop and fix -->
**Verdict:** Continue

## Corrections Required

<!-- If verdict is "Continue with corrections" or "Stop and fix" -->
None.

<!-- Use this format if corrections exist:
1. **Correction** — Must be fixed before next step. Assigned to: {agent}.
-->

---

*Checkpoint reviewed by {reviewers} | JVIS Framework*
