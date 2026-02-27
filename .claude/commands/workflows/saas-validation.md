# SaaS Validation Workflow

Execute a complete SaaS product validation before development.

## Workflow Overview

This workflow validates a SaaS idea through 8 steps:

1. **Idea Scoring** (WPS) - Evaluate the idea's potential
2. **Market Research** - TAM/SAM/SOM analysis
3. **Competitor Analysis** - Analyze competing products
4. **SWOT Analysis** - Strengths, weaknesses, opportunities, threats
5. **Pricing Strategy** - Define pricing model
6. **Unit Economics** - Calculate LTV, CAC, margins
7. **Interview Guide** - Prepare for customer discovery
8. **GATE Decision** - Go/No-Go based on findings

## Instructions

Execute the task defined in `.jvis/tasks/saas-validation.md`.

### Step Execution

For each step, use the appropriate agent:

```
Step 1: /strategist → *idea-score
Step 2: /strategist → *market-scan
Step 3: /strategist → *competitor-analysis
Step 4: /analyst → *swot
Step 5: /strategist → *pricing-strategy
Step 6: /strategist → *unit-economics
Step 7: /strategist → *interview-guide
Step 8: Review all → Make GATE decision
```

### Key Metrics

Track these throughout the workflow:
- WPS Score (target: ≥6.0)
- TAM (target: ≥$1B)
- LTV:CAC ratio (target: ≥3:1)
- Problem validation rate (target: ≥70%)
- Willingness to pay rate (target: ≥50%)

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

If **GO**: Run `/pm *create-prd` then select stack for development
If **NO-GO**: Document lessons, pivot or abandon
