---
description: Create comprehensive marketing campaign from brief to execution plan
---

# Marketing Suite: Marketing Campaign

You are now executing the **Marketing Campaign** workflow from the Marketing & Strategy Suite.

## Your Mission

Create a comprehensive, multi-channel marketing campaign based on client brief and strategic objectives.

## Prerequisites

This workflow requires:
- Client brief (from `/solutions` discovery or provided directly)
- Clear objectives and KPIs
- Budget allocation
- Timeline

## Process Steps

### Step 1: Brief Review

If no brief exists, gather:

```
Essential Information:
1. Campaign objectives (awareness, leads, sales)
2. Target audience (demographics, psychographics)
3. Presupuesto total y por canal
4. Timeline (fechas clave)
5. Mensaje principal / USP
6. Restricciones o requisitos especiales
```

### Step 2: Strategic Framework

Use `/strategist` agent:

```bash
/strategist
*campaign-plan
```

**Define:**

| Element | Description |
|---------|-------------|
| Objective | SMART goal |
| Audience | Primary & secondary |
| Positioning | vs. competitors |
| Key Message | Core value proposition |
| Tone & Voice | Brand personality |
| Channels | Where to reach audience |
| Budget Split | % per channel |
| Timeline | Phases and milestones |

### Step 3: Channel Strategy

For each selected channel:

#### Digital Channels

| Channel | Best For | Key Metrics |
|---------|----------|-------------|
| Google Ads | Intent-based search | CTR, CPC, Conv Rate |
| Meta Ads | Awareness, targeting | CPM, Reach, Engagement |
| LinkedIn | B2B, professionals | CTR, Lead Quality |
| TikTok | Gen Z, viral content | Views, Engagement |
| Email | Nurturing, retention | Open Rate, CTR |
| Content/SEO | Long-term traffic | Rankings, Organic Traffic |

#### Traditional Channels (if applicable)
- Print, TV, Radio, OOH
- Events and sponsorships
- PR and earned media

### Step 4: Content Calendar

```bash
*content-calendar
```

**Create monthly calendar:**

```markdown
## Week 1
| Day | Channel | Content Type | Topic | Status |
|-----|---------|--------------|-------|--------|
| Mon | Instagram | Post | [Topic] | Draft |
| Tue | Blog | Article | [Topic] | Draft |
| Wed | Email | Newsletter | [Topic] | Draft |
```

### Step 5: Creative Brief

For each creative asset:

```markdown
## Creative Brief: [Asset Name]

**Format:** [Banner/Video/Email/etc.]
**Size:** [Dimensions]
**Channel:** [Where it will run]

**Objective:** [What should it achieve]
**Target Audience:** [Who will see it]
**Key Message:** [What to communicate]
**CTA:** [Desired action]
**Tone:** [How it should feel]

**Must Include:**
- Logo
- [Other mandatory elements]

**Must Avoid:**
- [Restrictions]

**Inspiration/References:**
- [Links or descriptions]
```

### Step 6: A/B Testing Plan

```bash
*ab-test
```

**Define tests:**

| Test | Variable | Variant A | Variant B | Hypothesis |
|------|----------|-----------|-----------|------------|
| 1 | Headline | [A] | [B] | [Expected outcome] |
| 2 | CTA | [A] | [B] | [Expected outcome] |

### Step 7: Budget Allocation

```markdown
## Budget Breakdown

**Total Budget:** $XX,XXX

| Channel | % | Amount | Expected Results |
|---------|---|--------|------------------|
| Google Ads | 30% | $X,XXX | X leads |
| Meta Ads | 25% | $X,XXX | X reach |
| Content | 20% | $X,XXX | X articles |
| Email | 15% | $X,XXX | X sends |
| Tools/Other | 10% | $X,XXX | - |
```

### Step 8: KPIs & Measurement

**Primary KPIs:**
| KPI | Target | Measurement |
|-----|--------|-------------|
| Leads | X | Form submissions |
| CAC | $X | Cost / Conversions |
| ROAS | X:1 | Revenue / Ad Spend |

**Secondary KPIs:**
- Impressions, Reach
- Engagement Rate
- Website Traffic
- Email Metrics

### Step 9: Reporting Structure

**Weekly Reports:**
- Performance by channel
- Budget spend vs. plan
- Top performing content
- Issues and optimizations

**Monthly Reports:**
- Full funnel analysis
- ROI calculation
- Learnings and recommendations
- Next month adjustments

### Step 10: Documentation

Save to: `docs/campaigns/campaign-{name}-{date}.md`

## Output Format

```markdown
# Marketing Campaign Plan

## Campaign: [Name]
**Client:** [Client Name]
**Period:** [Start] - [End]
**Budget:** $[Amount]

## Executive Summary
[2-3 paragraph overview]

## Objectives & KPIs

| Objective | KPI | Target |
|-----------|-----|--------|
| [Obj 1] | [KPI] | [Target] |

## Target Audience

### Primary Audience
- Demographics: [Details]
- Psychographics: [Details]
- Pain Points: [Details]

### Secondary Audience
[If applicable]

## Strategic Approach
[Positioning, messaging, differentiation]

## Channel Mix

| Channel | Role | Budget | Timeline |
|---------|------|--------|----------|
| [Channel] | [Role] | $[X] | [Dates] |

## Content Calendar
[Monthly view or link to detailed calendar]

## Creative Requirements
[List of assets needed]

## A/B Testing Plan
[Key tests to run]

## Measurement & Reporting
[How success will be tracked]

## Timeline & Milestones

| Date | Milestone |
|------|-----------|
| [Date] | [Milestone] |

## Risk Mitigation
[Potential issues and contingencies]

## Approval & Sign-off
- [ ] Client approval
- [ ] Creative approval
- [ ] Budget approval
- [ ] Launch readiness
```

## Begin

Check if there's an existing client brief in `docs/campaigns/client-brief.md`. If not, start gathering the essential information.
