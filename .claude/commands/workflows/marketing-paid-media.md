---
description: Paid media campaign from planning to optimization
---

# Marketing Suite: Paid Media Campaign Workflow

You are now executing the **Paid Media Campaign** workflow from the Marketing Suite.

## Your Mission

Plan, execute, and optimize paid media campaigns across all channels - digital, programmatic, TV, radio, and OOH.

## Process Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         PAID MEDIA CAMPAIGN WORKFLOW                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  STRATEGY       PLANNING        CREATIVE       LAUNCH        OPTIMIZE           │
│  ────────       ────────        ────────       ──────        ────────           │
│                                                                                  │
│  /marketing     /media-buyer    /copywriter    /marketing    /marketing         │
│  /media-buyer   /marketing      /ux-expert     /media-buyer  /media-buyer       │
│                                 /creative-dir                                    │
│                                                                                  │
│  Week 1         Week 1-2        Week 2-3       Week 3        Week 4+            │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Strategy (Week 1)

### Agents: `/strategist` → `/media-buyer`

### 1.1 Campaign Objectives

```bash
/marketing
*campaign-create     # Campaign brief
*analytics-goals     # KPIs definition
```

**Define:**

| Element | Definition |
|---------|------------|
| Business Objective | What business outcome? |
| Marketing Objective | Awareness / Consideration / Conversion |
| Target Audience | Primary and secondary |
| KPIs | Primary and secondary metrics |
| Budget | Total and by phase |
| Timeline | Campaign duration |
| Geography | Target regions |

### 1.2 Media Strategy

```bash
/media-buyer
*media-brief         # Media planning brief
*channel-recommend   # Channel selection
*reach-frequency     # R&F modeling
```

**Channel Mix Decision:**

| Channel | Role | Budget % | Expected Outcome |
|---------|------|----------|------------------|
| Search | Intent capture | X% | Conversions |
| Social | Awareness/Retargeting | X% | Reach + Conversions |
| Display | Awareness | X% | Impressions |
| Video | Consideration | X% | Views + Engagement |
| TV/CTV | Awareness | X% | Reach |
| Audio | Awareness | X% | Reach |
| OOH | Awareness | X% | Impressions |

### 1.3 Audience Strategy

```bash
/marketing
*social-audience     # Audience definitions
```

```bash
/media-buyer
*audience-plan       # Cross-channel audience plan
```

**Audience Framework:**

| Audience | Size | Channel | Targeting |
|----------|------|---------|-----------|
| Prospecting - Broad | Large | Display, Social | Demo + Interest |
| Prospecting - Lookalike | Medium | Social, Programmatic | Lookalike |
| Intent | Medium | Search, YouTube | Keywords, In-market |
| Retargeting - Site | Small | All | Pixel |
| Retargeting - Engaged | Small | All | Custom audiences |
| Conquest | Medium | Search, Display | Competitor |

### Phase 1 Gate

- [ ] Campaign objectives approved
- [ ] Channel mix decided
- [ ] Budget allocated
- [ ] Audience strategy defined

---

## Phase 2: Media Planning (Week 1-2)

### Agent: `/media-buyer`

### 2.1 Comprehensive Media Plan

```bash
/media-buyer
*media-plan          # Full media plan
*budget-allocation   # Detailed budget
*flighting           # Campaign flighting
```

**Media Plan Components:**

```markdown
## Media Plan: [Campaign Name]

### Budget Summary
| Channel | Budget | % of Total |
|---------|--------|------------|
| Total | $X | 100% |

### Flighting Strategy
[Even / Front-loaded / Pulsed / etc.]

### Channel Details

#### Search
- Platforms: Google, Bing
- Budget: $X
- Campaign types: [Brand, Non-brand, Shopping]
- Target CPC: $X
- Target CPA: $X

#### Paid Social
- Platforms: Meta, LinkedIn, TikTok
- Budget: $X
- Objectives: [Awareness, Traffic, Conversions]
- Target CPM: $X
- Target CPA: $X

[Continue for each channel...]

### Reach & Frequency Goals
- Target Reach: X% of audience
- Target Frequency: X times
- Effective reach: X%

### Measurement Plan
- Attribution model: [Model]
- Conversion window: [Days]
- Key conversion events: [List]
```

### 2.2 Platform-Specific Planning

#### Search (Google/Bing)

```bash
/marketing
*sem-structure       # Campaign structure
*sem-keywords        # Keyword research
```

**Structure:**
```
Account
├── Brand
│   ├── Brand - Exact
│   └── Brand - BMM
├── Non-Brand
│   ├── Category A
│   │   ├── Ad Group 1
│   │   └── Ad Group 2
│   └── Category B
├── Competitor
└── Shopping (if e-comm)
```

#### Programmatic

```bash
/media-buyer
*programmatic-strategy   # Programmatic plan
*dsp-setup              # DSP configuration
*pmp-deal               # Private deals
```

**Targeting Layers:**
- Contextual targeting
- Audience targeting (1P, 3P)
- Retargeting pools
- Private marketplace deals

#### TV/CTV/OTT

```bash
/media-buyer
*tv-plan             # Linear TV plan
*ctv-plan            # Connected TV plan
```

#### Audio

```bash
/media-buyer
*radio-plan          # Radio planning
*podcast-plan        # Podcast advertising
```

#### Out-of-Home

```bash
/media-buyer
*ooh-plan            # OOH planning
*dooh-plan           # Digital OOH
```

### 2.3 Vendor/Publisher Negotiations

```bash
/media-buyer
*rfp                 # RFP to vendors
*negotiate           # Rate negotiations
*io                  # Insertion orders
```

### Phase 2 Gate

- [ ] Media plan approved
- [ ] Vendor negotiations complete
- [ ] IOs signed
- [ ] Placements secured

---

## Phase 3: Creative Development (Week 2-3)

### Agents: `/copywriter` → `/ux-expert` → `/creative-director`

### 3.1 Creative Strategy

```bash
/creative-director
*creative-strategy   # Creative approach
*creative-brief      # Briefs for all assets
```

### 3.2 Copy Development

```bash
/copywriter
*ad-google           # Search ads (15 headlines, 4 descriptions)
*ad-meta             # Social ads (5+ variations)
*ad-linkedin         # LinkedIn ads
*hook                # Video hooks
```

**Copy Matrix:**

| Platform | Format | Variations | Specs |
|----------|--------|------------|-------|
| Google RSA | Headlines | 15 | 30 chars |
| Google RSA | Descriptions | 4 | 90 chars |
| Meta | Primary text | 5 | 125 chars optimal |
| Meta | Headlines | 5 | 40 chars |
| LinkedIn | Intro | 3 | 150 chars |
| Display | Headlines | 3 | 25 chars |

### 3.3 Visual Development

```bash
/ux-expert
*ad-creative         # Static ad visuals
*banner-design       # Display banners
*social-graphic      # Social images
```

**Asset Specs:**

| Platform | Format | Sizes |
|----------|--------|-------|
| Meta | Static | 1080x1080, 1080x1920, 1200x628 |
| Google Display | Responsive | 1200x628, 1200x1200, 300x250 |
| LinkedIn | Single | 1200x627 |
| Programmatic | Standard | IAB standard sizes |

### 3.4 Video Development

```bash
/video-producer
*script-ad           # Ad scripts
*social-cuts         # Social video edits
```

**Video Specs:**

| Platform | Format | Duration | Specs |
|----------|--------|----------|-------|
| YouTube | Skippable | 15-30s | 1920x1080 |
| Meta Reels | Vertical | 15-30s | 1080x1920 |
| TikTok | Vertical | 15-60s | 1080x1920 |
| CTV | TV | 15-30s | 1920x1080 |

### 3.5 Creative Review

```bash
/creative-director
*review              # Quality review
```

### Phase 3 Gate

- [ ] All copy written and approved
- [ ] All visuals created
- [ ] All videos produced
- [ ] A/B test variations ready
- [ ] Assets sized for all platforms

---

## Phase 4: Launch (Week 3)

### Agents: `/strategist` → `/media-buyer`

### 4.1 Tracking Setup

```bash
/marketing
*analytics-setup     # Conversion tracking
```

**Tracking Checklist:**
- [ ] Google Ads conversion tracking
- [ ] Meta Pixel installed
- [ ] LinkedIn Insight Tag
- [ ] Google Analytics 4 configured
- [ ] UTM parameters standardized
- [ ] Offline conversion import (if needed)

### 4.2 Campaign Build

```bash
/marketing
*campaign-launch     # Campaign setup checklist
```

**Build Checklist:**

#### Search
- [ ] Campaigns created with correct settings
- [ ] Ad groups structured properly
- [ ] Keywords added with correct match types
- [ ] Negative keywords added
- [ ] Ads created with all assets
- [ ] Extensions configured
- [ ] Bidding strategy set
- [ ] Budget allocated

#### Social
- [ ] Campaigns created
- [ ] Audiences built
- [ ] Ad sets structured
- [ ] Creative uploaded
- [ ] Tracking verified
- [ ] Budget and schedule set

#### Programmatic
- [ ] Campaigns live in DSP
- [ ] Targeting configured
- [ ] Deals activated
- [ ] Brand safety settings applied
- [ ] Frequency caps set

### 4.3 QA & Launch

```bash
/media-buyer
*brand-safety        # Brand safety verification
```

**Pre-Launch QA:**
- [ ] All ads approved by platforms
- [ ] Landing pages live and loading
- [ ] Tracking firing correctly
- [ ] Budget caps set correctly
- [ ] Start dates confirmed
- [ ] Team notified of launch

### Phase 4 Gate

- [ ] All campaigns built
- [ ] Tracking verified
- [ ] QA passed
- [ ] Campaigns launched

---

## Phase 5: Optimization (Week 4+)

### Agents: `/strategist` → `/media-buyer`

### 5.1 Daily Monitoring

```bash
/marketing
*campaign-review     # Performance review
```

**Daily Checks:**
- Budget pacing
- Cost anomalies
- Delivery issues
- Conversion tracking
- Disapproved ads

### 5.2 Weekly Optimization

```bash
/marketing
*campaign-optimize   # Optimization actions
```

```bash
/media-buyer
*optimize-mix        # Channel optimization
```

**Optimization Actions:**

| Area | Action | Frequency |
|------|--------|-----------|
| Budget | Shift to winners | Weekly |
| Bids | Adjust based on performance | 2x/week |
| Audiences | Expand/contract | Weekly |
| Creative | Pause losers, test new | Weekly |
| Placements | Exclude poor performers | Weekly |
| Keywords | Add/pause based on data | 2x/week |

### 5.3 A/B Testing

```bash
/marketing
*cro-ab-test         # A/B test planning
```

**Test Roadmap:**

| Week | Test | Variable | Hypothesis |
|------|------|----------|------------|
| 1-2 | Creative A vs B | Image style | [Hypothesis] |
| 3-4 | Copy A vs B | Value prop | [Hypothesis] |
| 5-6 | Audience A vs B | Targeting | [Hypothesis] |

### 5.4 Scaling

```bash
/marketing
*campaign-scale      # Scale winners
```

```bash
/media-buyer
*scale-winners       # Increase budgets
```

**Scaling Rules:**
- ROAS >X → Increase budget 20%
- CPA <$X → Increase budget 15%
- Hold for 3+ days of consistent performance
- Scale incrementally (not 2x overnight)

### 5.5 Reporting

```bash
/marketing
*analytics-report    # Performance report
```

```bash
/media-buyer
*media-report        # Media performance
*post-buy            # Post-buy analysis
```

**Reporting Cadence:**

| Report | Frequency | Audience |
|--------|-----------|----------|
| Dashboard | Real-time | Team |
| Performance summary | Weekly | Stakeholders |
| Deep-dive analysis | Bi-weekly | Team + leadership |
| Full report | Monthly | All stakeholders |

---

## Performance Dashboard

### Key Metrics by Channel

| Channel | Primary KPI | Secondary | Benchmark |
|---------|-------------|-----------|-----------|
| Search Brand | ROAS | CPC | >800% |
| Search Non-Brand | CPA | CTR | <$X |
| Social Prospecting | CPM | CTR | <$X |
| Social Retargeting | ROAS | Frequency | >400% |
| Display | CPM | Viewability | <$X |
| Video | CPCV | VTR | <$X |
| CTV | CPM | Reach | <$X |

### Optimization Decision Tree

```
Performance Below Target?
    │
    ├── Low CTR
    │   ├── Creative issue → Test new creative
    │   └── Targeting issue → Refine audience
    │
    ├── High CPC/CPM
    │   ├── Competition → Adjust bids/targeting
    │   └── Quality issue → Improve relevance
    │
    ├── Low Conversion Rate
    │   ├── Traffic quality → Refine targeting
    │   └── Landing page → CRO audit
    │
    └── Budget not spending
        ├── Bids too low → Increase bids
        └── Audience too narrow → Expand targeting
```

---

## Documentation Structure

```
docs/marketing/paid-media/
├── strategy/
│   ├── media-strategy.md
│   └── audience-strategy.md
├── plans/
│   ├── media-plan.md
│   └── channel-plans/
├── creative/
│   ├── copy/
│   └── assets/
├── tracking/
│   └── tracking-setup.md
└── reports/
    ├── weekly/
    └── monthly/
```

## Begin

Start by asking:

1. "What is the main objective? (awareness, leads, sales)"
2. "What is the total available budget?"
3. "Which channels are already active vs new?"
4. "What is the campaign timeline?"

Then proceed to Phase 1: Strategy.
