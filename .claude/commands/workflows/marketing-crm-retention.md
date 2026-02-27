---
description: CRM and customer retention workflow
---

# Marketing Suite: CRM & Retention Workflow

You are now executing the **CRM & Retention** workflow from the Marketing Suite.

## Your Mission

Build and execute a comprehensive CRM and retention strategy to maximize customer lifetime value.

## Process Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          CRM & RETENTION WORKFLOW                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  FOUNDATION      SEGMENTATION    AUTOMATION      RETENTION      GROWTH          │
│  ──────────      ────────────    ──────────      ─────────      ──────          │
│                                                                                  │
│  /crm            /crm            /crm            /crm           /marketing      │
│  /marketing      /marketing      /copywriter     /community     /crm            │
│                                  /ux-expert                     /community      │
│                                                                                  │
│  Week 1-2        Week 2-3        Week 3-5        Ongoing        Ongoing         │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: CRM Foundation (Week 1-2)

### Agents: `/crm` → `/strategist`

### 1.1 CRM Strategy

```bash
/crm
*strategy            # CRM strategy
*journey-map         # Customer journey mapping
```

**Define:**

| Element | Definition |
|---------|------------|
| Objectives | Retention rate, LTV, NPS targets |
| Customer Lifecycle | Stages and triggers |
| Communication Strategy | Channels, frequency, personalization |
| Data Requirements | What data to collect |
| Success Metrics | KPIs to track |

### 1.2 Customer Journey Mapping

```bash
/crm
*journey-map         # Full journey map
```

**Lifecycle Stages:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CUSTOMER LIFECYCLE                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ACQUIRE    ONBOARD     ENGAGE      RETAIN      EXPAND     ADVOCATE    │
│    │           │           │           │           │           │        │
│    ▼           ▼           ▼           ▼           ▼           ▼        │
│  Lead      New User    Active     At-Risk    Loyal     Champion        │
│  Prospect  First Use   Regular    Declining  Repeat    Referrer        │
│                        User       Usage      Buyer                      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.3 Data & Infrastructure

```bash
/crm
*data-audit          # Data assessment
```

**Data Requirements:**

| Category | Data Points | Source |
|----------|-------------|--------|
| Identity | Name, email, phone | Registration |
| Demographics | Age, location, industry | Profile |
| Behavioral | Logins, features used | Product |
| Transactional | Purchases, revenue | Payments |
| Engagement | Email opens, clicks | Email |
| Support | Tickets, NPS scores | Support |

### 1.4 CRM Metrics Setup

```bash
/crm
*metrics             # Define metrics
```

```bash
/marketing
*analytics-goals     # Goals setup
```

**Core Metrics:**

| Metric | Definition | Target |
|--------|------------|--------|
| Retention Rate | % customers retained period over period | >X% |
| Churn Rate | % customers lost | <X% |
| LTV | Customer lifetime value | $X |
| CAC:LTV Ratio | Acquisition efficiency | >3:1 |
| NPS | Net Promoter Score | >X |
| Email Engagement | Open rate, CTR | >X% |

### Phase 1 Gate

- [ ] CRM strategy approved
- [ ] Customer journey mapped
- [ ] Data requirements defined
- [ ] Metrics established

---

## Phase 2: Segmentation (Week 2-3)

### Agents: `/crm` → `/strategist`

### 2.1 RFM Analysis

```bash
/crm
*rfm-analysis        # RFM segmentation
```

**RFM Model:**

| Dimension | Score 1 (Low) | Score 5 (High) |
|-----------|---------------|----------------|
| Recency | >90 days | <7 days |
| Frequency | 1 purchase | 10+ purchases |
| Monetary | Bottom 20% | Top 20% |

**RFM Segments:**

| Segment | RFM Score | Strategy |
|---------|-----------|----------|
| Champions | 555, 554, 545 | Reward, upsell |
| Loyal | 445, 454, 544 | Loyalty program |
| Potential Loyalists | 534, 443, 434 | Nurture to loyal |
| New Customers | 511, 512, 521 | Onboard well |
| Promising | 413, 414, 431 | Engage more |
| Need Attention | 333, 332, 323 | Re-engage |
| About to Sleep | 233, 232, 223 | Win-back |
| At Risk | 244, 234, 143 | Urgent retention |
| Hibernating | 122, 123, 132 | Reactivation |
| Lost | 111, 112, 121 | Let go or deep win-back |

### 2.2 Behavioral Segmentation

```bash
/crm
*segment             # Advanced segmentation
```

**Behavioral Segments:**

| Segment | Criteria | Size | Priority |
|---------|----------|------|----------|
| Power Users | >X logins/week, all features | X% | High |
| Regular Users | X-Y logins/week | X% | Medium |
| Casual Users | <X logins/week | X% | Medium |
| Dormant | No login >30 days | X% | High |
| Feature A Users | Uses Feature A | X% | Varies |

### 2.3 Lead Scoring

```bash
/crm
*lead-scoring        # Lead scoring model
```

**Scoring Model:**

| Factor | Points | Criteria |
|--------|--------|----------|
| **Demographic Fit** | | |
| Job title match | +20 | Decision maker |
| Company size match | +15 | Target size |
| Industry match | +15 | Target industry |
| **Engagement** | | |
| Email opens | +5 each | Recent 30 days |
| Link clicks | +10 each | Recent 30 days |
| Content downloads | +15 each | Gated content |
| Demo request | +50 | High intent |
| Pricing page visit | +30 | Purchase intent |
| **Negative** | | |
| Unsubscribe | -50 | Lost interest |
| No activity 30d | -20 | Declining |

**Score Tiers:**

| Score | Tier | Action |
|-------|------|--------|
| 80+ | Hot | Sales outreach |
| 50-79 | Warm | Nurture + SDR |
| 20-49 | Cold | Nurture sequence |
| <20 | Inactive | Re-engagement or remove |

### Phase 2 Gate

- [ ] RFM analysis complete
- [ ] Behavioral segments defined
- [ ] Lead scoring implemented
- [ ] Segments populated

---

## Phase 3: Automation (Week 3-5)

### Agents: `/crm` → `/copywriter` → `/ux-expert`

### 3.1 Automation Strategy

```bash
/crm
*automation          # Automation planning
```

**Automation Types:**

| Type | Trigger | Purpose |
|------|---------|---------|
| Welcome | Signup | Onboarding |
| Nurture | Lead score threshold | Move to sale |
| Re-engagement | Inactivity | Prevent churn |
| Win-back | Churned | Recover customer |
| Upsell | Usage/time trigger | Expand revenue |
| Loyalty | Milestone | Reward/retain |
| Transactional | Action | Confirm/inform |

### 3.2 Lifecycle Automations

#### Welcome/Onboarding Sequence

```bash
/copywriter
*email-welcome       # Welcome series
```

```bash
/ux-expert
*email-design        # Email templates
```

**Sequence:**

| Day | Email | Goal |
|-----|-------|------|
| 0 | Welcome + getting started | Activate |
| 2 | Key feature #1 | Educate |
| 5 | Key feature #2 | Educate |
| 7 | Success story/tip | Inspire |
| 14 | Check-in + support | Support |

#### Nurture Sequence

```bash
/copywriter
*email-sequence      # Nurture emails
```

**Sequence:**

| Day | Email | Goal |
|-----|-------|------|
| 0 | Value content #1 | Educate |
| 4 | Case study | Build trust |
| 8 | Value content #2 | Educate |
| 12 | Comparison/differentiation | Position |
| 16 | Offer/CTA | Convert |

#### Re-engagement Sequence

```bash
/crm
*win-back            # Win-back campaign
```

**Sequence:**

| Trigger | Email | Goal |
|---------|-------|------|
| 14 days inactive | "We miss you" | Re-engage |
| 21 days inactive | "What's new" | Value reminder |
| 30 days inactive | Special offer | Incentivize |
| 45 days inactive | Final attempt | Last chance |

### 3.3 Behavioral Triggers

```bash
/crm
*triggers            # Trigger definitions
```

**Trigger Examples:**

| Trigger | Action | Timing |
|---------|--------|--------|
| Viewed pricing 2x | Sales alert + email | Within 1 hour |
| Downloaded 3+ resources | Move to nurture | Next day |
| High NPS response | Referral ask | 2 days later |
| Low NPS response | Support outreach | Immediate |
| Cart abandonment | Reminder email | 1 hour, 24 hours |
| Feature not used | Education email | 7 days after signup |

### Phase 3 Gate

- [ ] Automation strategy approved
- [ ] Email content created
- [ ] Workflows built
- [ ] Testing complete

---

## Phase 4: Retention Programs (Ongoing)

### Agents: `/crm` → `/community`

### 4.1 Churn Prevention

```bash
/crm
*churn-prediction    # Churn modeling
*retention-strategy  # Retention tactics
```

**Churn Signals:**

| Signal | Risk Level | Action |
|--------|------------|--------|
| Login decline >50% | High | Personal outreach |
| Support tickets up | Medium | Check satisfaction |
| Feature usage down | Medium | Education campaign |
| Payment failure | High | Immediate contact |
| NPS decline | High | Feedback follow-up |

**Intervention Playbook:**

| Risk Level | Intervention | Owner |
|------------|--------------|-------|
| Low | Automated nurture | Marketing |
| Medium | Targeted campaign | Marketing + CS |
| High | Personal outreach | CS/Account team |
| Critical | Executive escalation | Leadership |

### 4.2 Loyalty Program

```bash
/crm
*loyalty             # Loyalty program design
```

**Program Elements:**

| Element | Description |
|---------|-------------|
| Points | Earn for purchases, engagement |
| Tiers | Bronze → Silver → Gold → Platinum |
| Rewards | Discounts, exclusive access, swag |
| Recognition | Badges, community status |
| Experiences | Events, early access |

### 4.3 Community Engagement

```bash
/community
*strategy            # Community for retention
*advocate-identify   # Find advocates
*ambassador-program  # Ambassador development
```

**Community Retention Tactics:**
- Exclusive community access for customers
- Customer-only events
- Peer support and networking
- User groups and forums
- Success story spotlights

### 4.4 Referral Program

```bash
/community
*referral            # Referral program
```

**Program Structure:**

| Element | Referrer Gets | Referee Gets |
|---------|---------------|--------------|
| Reward | $X credit | $X off first purchase |
| Timing | On referee purchase | On first purchase |
| Limit | X referrals/month | One-time |

### Phase 4 Gate

- [ ] Churn prediction active
- [ ] Retention interventions defined
- [ ] Loyalty program launched
- [ ] Referral program active

---

## Phase 5: Growth & Expansion (Ongoing)

### Agents: `/crm` → `/strategist`

### 5.1 Upsell/Cross-sell

```bash
/crm
*upsell              # Upsell strategy
```

**Opportunity Identification:**

| Signal | Opportunity | Offer |
|--------|-------------|-------|
| High usage | Plan upgrade | Next tier |
| Feature limit hit | Add-on | Feature pack |
| Complementary need | Cross-sell | Related product |
| Contract renewal | Expansion | Multi-year deal |

### 5.2 LTV Optimization

```bash
/crm
*ltv                 # LTV analysis
```

```bash
/marketing
*data-ltv            # LTV modeling
```

**LTV Levers:**

| Lever | Tactic | Impact |
|-------|--------|--------|
| Increase retention | Reduce churn 5% | +25% LTV |
| Increase frequency | Upsell campaigns | +X% LTV |
| Increase AOV | Cross-sell, bundles | +X% LTV |
| Decrease CAC | Referrals, organic | Better ratio |

### 5.3 Customer Advocacy

```bash
/community
*advocate-activate   # Activate advocates
*ugc-campaign        # UGC for growth
```

**Advocacy Programs:**
- Review/testimonial requests
- Case study development
- Referral program
- Social sharing incentives
- Community leadership roles

### 5.4 Reporting & Analysis

```bash
/crm
*report              # CRM reporting
```

```bash
/marketing
*data-cohort         # Cohort analysis
*data-churn          # Churn analysis
```

**Monthly CRM Report:**

```markdown
## CRM Performance Report: [Month]

### Summary
| Metric | Target | Actual | Δ |
|--------|--------|--------|---|
| Retention Rate | X% | X% | +X% |
| Churn Rate | X% | X% | -X% |
| LTV | $X | $X | +$X |
| NPS | X | X | +X |

### Cohort Retention
| Cohort | M1 | M2 | M3 | M6 | M12 |
|--------|-----|-----|-----|-----|------|
| [Month] | X% | X% | X% | X% | X% |

### Email Performance
| Sequence | Sent | Open | CTR | Conversion |
|----------|------|------|-----|------------|
| Welcome | X | X% | X% | X% |
| Nurture | X | X% | X% | X% |
| Re-engage | X | X% | X% | X% |

### Segment Health
| Segment | Size | Trend | Action |
|---------|------|-------|--------|
| Champions | X | ↑↓→ | [Action] |
| At Risk | X | ↑↓→ | [Action] |

### Churn Analysis
| Reason | % | Intervention |
|--------|---|--------------|
| [Reason 1] | X% | [Action] |

### Next Month Focus
1. [Priority 1]
2. [Priority 2]
```

---

## Documentation Structure

```
docs/marketing/crm/
├── strategy/
│   ├── crm-strategy.md
│   └── customer-journey.md
├── segments/
│   ├── rfm-analysis.md
│   ├── behavioral-segments.md
│   └── lead-scoring.md
├── automations/
│   ├── welcome-sequence.md
│   ├── nurture-sequence.md
│   └── winback-sequence.md
├── programs/
│   ├── loyalty-program.md
│   └── referral-program.md
└── reports/
    └── monthly/
```

## Begin

Start by asking:

1. "Is there a CRM/email platform currently in use?"
2. "What is the current customer/user base?"
3. "What is the current retention rate?"
4. "Is there existing segmentation or are we starting from scratch?"

Then proceed to Phase 1: CRM Foundation.
