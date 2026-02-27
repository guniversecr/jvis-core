# E-commerce Validation Workflow

Execute a complete e-commerce business validation before development.

## Workflow Overview

This workflow validates an e-commerce idea through 7 steps:

1. **Idea Scoring** (WPS) - Evaluate the idea's potential
2. **Market Research** - Understand the market
3. **Competitor Analysis** - Analyze competing stores
4. **SWOT Analysis** - Strengths, weaknesses, opportunities, threats
5. **Pricing & Margins** - Calculate profitability
6. **Growth Channels** - Identify acquisition channels
7. **GATE Decision** - Go/No-Go based on findings

## Instructions

Execute the task defined in `.jvis/tasks/ecommerce-validation.md`.

### Step Execution

For each step, use the appropriate agent:

```
Step 1: /strategist → *idea-score
Step 2: /strategist → *market-scan
Step 3: /strategist → *competitor-analysis
Step 4: /analyst → *swot
Step 5: /strategist → *pricing-strategy
Step 6: /strategist → *growth-channels
Step 7: Review all → Make GATE decision
```

### Key Metrics

Track these throughout the workflow:
- WPS Score (target: ≥6.0)
- Market Size (target: ≥$100M)
- Gross Margin (target: ≥50%)
- Net Margin (target: ≥20%)
- Viable acquisition channels (target: ≥2)

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
- If approved, choose platform

## Output

- Files in `docs/validation/`
- Updated `.jvis/project-composition.yaml`
- Gate decision with go/no-go recommendation

## Next Steps

If **GO**:
- For Shopify: Run `/shopify`
- For Custom: Run `/frontend` + `/api`
If **NO-GO**: Document lessons, pivot or abandon
