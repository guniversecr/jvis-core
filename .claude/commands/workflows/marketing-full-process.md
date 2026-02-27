---
description: Complete marketing process from consulting to campaign execution
---

# Marketing Suite: Proceso Completo

You are now executing the **Full Marketing Process** workflow from the Marketing & Strategy Suite.

## Your Mission

Guide the complete cycle from initial consulting through strategy development to marketing campaign execution.

## Process Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                      PROCESO COMPLETO                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  FASE 1          FASE 2           FASE 3          FASE 4            │
│  ────────        ────────         ────────        ────────          │
│  Discovery  →    Research    →    Strategy   →    Execution         │
│  /solutions      /strategist      /strategist     /marketing        │
│                                   /marketing                        │
│                                                                      │
│  Semana 1-2      Semana 2-3       Semana 3-4      Ongoing           │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Phase 1: Discovery & Consulting (Week 1-2)

### Agent: `/solutions`

```bash
/solutions
*init-project
```

### 1.1 Stakeholder Mapping

Identify key stakeholders:
- Decision makers
- Influencers
- End users
- Budget holders

### 1.2 Discovery Workshop

```bash
*generate-workshop discovery
```

**Key Questions:**
1. Business objectives (1, 3, 5 years)
2. Current marketing efforts
3. Past successes and failures
4. Competitive landscape perception
5. Budget constraints
6. Internal capabilities

### 1.3 Process Transcript

After workshop:

```bash
*process-transcript docs/consulting/transcripts/discovery.md
```

### 1.4 Gap Analysis

```bash
*gap-analysis
```

**Document:**
- AS-IS state
- TO-BE state
- Gaps to bridge

### 1.5 Proposal

```bash
*draft-proposal
```

**Deliverables:**
- Scope of work
- Timeline
- Budget
- Expected outcomes
- Terms

**Save to:** `docs/consulting/proposals/`

### Phase 1 Gate

- [ ] Discovery completed
- [ ] Findings consolidated
- [ ] Proposal approved
- [ ] Contract signed
- [ ] Kickoff scheduled

---

## Phase 2: Research & Analysis (Week 2-3)

### Agent: `/strategist`

```bash
/strategist
```

### 2.1 Market Research

```bash
*market-research <industry>
```

**Analyze:**
- Market size and trends
- Growth opportunities
- Regulatory environment
- Technology impact

### 2.2 Competitor Analysis

```bash
*competitor-analysis
```

**Map:**
- Direct competitors
- Indirect competitors
- Their positioning
- Their channels
- Their messaging

### 2.3 Audience Research

Define personas:

```markdown
## Persona: [Name]

**Demographics:**
- Age:
- Gender:
- Location:
- Income:
- Education:

**Psychographics:**
- Values:
- Interests:
- Behaviors:
- Pain points:

**Media Consumption:**
- Channels:
- Content types:
- Influencers followed:

**Decision Journey:**
- Awareness triggers:
- Research behavior:
- Purchase drivers:
- Objections:
```

### 2.4 SEO/SEM Baseline (if applicable)

```bash
/marketing
*seo-audit <client-url>
```

### Phase 2 Gate

- [ ] Market research complete
- [ ] Competitor analysis done
- [ ] Personas defined
- [ ] Current state baseline documented

---

## Phase 3: Strategy Development (Week 3-4)

### Agents: `/strategist` + `/strategist`

### 3.1 Positioning Strategy

```bash
/strategist
*positioning-strategy
```

**Define:**
- Target market
- Frame of reference
- Points of difference
- Reasons to believe

### 3.2 Go-to-Market Plan

```bash
*gtm-plan
```

**Components:**
- Value proposition
- Pricing strategy
- Channel strategy
- Launch timeline

### 3.3 Marketing Strategy

```bash
/marketing
*campaign-plan
```

**Strategic Decisions:**
- Objectives (SMART)
- Target audiences (priority)
- Channels (mix)
- Budget allocation
- Timeline

### 3.4 Content Strategy

```bash
*content-calendar
```

**Plan:**
- Content pillars
- Content types
- Publishing cadence
- Distribution channels

### Phase 3 Gate

- [ ] Strategy presentation done
- [ ] Client approval received
- [ ] KPIs agreed
- [ ] Budget confirmed

---

## Phase 4: Execution (Ongoing)

### Agent: `/strategist`

### 4.1 Campaign Setup

For each channel:

**Google Ads:**
- [ ] Account structure
- [ ] Campaigns created
- [ ] Ad groups defined
- [ ] Keywords added
- [ ] Ads written
- [ ] Tracking setup

**Meta Ads:**
- [ ] Pixel installed
- [ ] Audiences created
- [ ] Campaigns structured
- [ ] Creatives uploaded
- [ ] Tracking verified

**Email:**
- [ ] Lists segmented
- [ ] Templates created
- [ ] Automations built
- [ ] Tests scheduled

### 4.2 Content Production

Track in content calendar:

| Asset | Status | Due Date | Owner |
|-------|--------|----------|-------|
| [Asset] | [Status] | [Date] | [Who] |

### 4.3 A/B Testing

```bash
*ab-test
```

**Active Tests:**
| Test | Start | End | Winner |
|------|-------|-----|--------|
| [Test] | [Date] | [Date] | [TBD] |

### 4.4 Optimization

**Weekly Review:**
- Performance metrics
- Budget pacing
- Winning/losing elements
- Optimization actions

### 4.5 Reporting

**Weekly:** Quick performance update
**Monthly:** Full analysis + recommendations
**Quarterly:** Strategic review + adjustments

---

## Documentation Structure

```
docs/
├── consulting/
│   ├── workshops/
│   │   └── discovery-{date}.md
│   ├── transcripts/
│   │   └── workshop-{date}.md
│   └── proposals/
│       └── proposal-{client}-{date}.md
├── research/
│   ├── market-analysis-{date}.md
│   ├── competitor-analysis-{date}.md
│   └── personas-{date}.md
├── campaigns/
│   ├── strategy-{name}.md
│   ├── content-calendar-{month}.md
│   └── reports/
│       └── monthly-{month}-{year}.md
└── seo-audits/
    └── audit-{domain}-{date}.md
```

## Handoff Points

### Consulting → Strategy
```bash
/solutions
*to-development
```

This generates:
- PRD (if product development)
- Brief (if marketing only)

### Strategy → Execution
Ensure:
- Strategy document approved
- Creative briefs ready
- Budgets allocated
- Timeline confirmed

## Success Metrics by Phase

| Phase | Success Metric |
|-------|----------------|
| Discovery | Client brief approved |
| Research | Insights documented |
| Strategy | Plan approved, budget confirmed |
| Execution | KPIs met or exceeded |

## Begin

Start by asking: "Is this a new client or do you have previous discovery information?"

- **Cliente nuevo:** Begin with Phase 1 (Discovery)
- **Discovery existente:** Skip to Phase 2 (Research)
- **Approved strategy:** Skip to Phase 4 (Execution)
