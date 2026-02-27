# Gaming Validation Workflow

Execute a complete gaming idea validation before development.

## Workflow Overview

This workflow validates a game idea through 7 steps:

1. **Idea Scoring** (WPS) - Evaluate the idea's potential
2. **Market Research** - Understand the gaming market
3. **Competitor Analysis** - Analyze competing games
4. **SWOT Analysis** - Strengths, weaknesses, opportunities, threats
5. **Timing Analysis** - Why now is the right time
6. **Monetization Strategy** - How to make money
7. **GATE Decision** - Go/No-Go based on findings

## Instructions

Execute the task defined in `.jvis/tasks/gaming-validation.md`.

### Step Execution

For each step, use the appropriate agent:

```
Step 1: /strategist → *idea-score
Step 2: /strategist → *market-scan
Step 3: /strategist → *competitor-analysis
Step 4: /analyst → *swot
Step 5: /strategist → *timing-analysis
Step 6: /strategist → *monetization
Step 7: Review all → Make GATE decision
```

### State Tracking

After each step, update the composition file:
- Mark step as completed
- Increment current_step
- Save output to docs/validation/

### Gate Decision

When all steps complete:
- Calculate overall score
- Compare against thresholds
- Document decision
- If approved, prepare for PRD creation

## Output

- Files in `docs/validation/`
- Updated `.jvis/project-composition.yaml`
- Gate decision with go/no-go recommendation

## Next Steps

If **GO**: Run `/pm *create-prd` then `/unity`
If **NO-GO**: Document lessons, pivot or abandon
