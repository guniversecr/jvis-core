---
description: End-to-end influencer marketing campaign workflow
---

# Marketing Suite: Influencer Campaign Workflow

You are now executing the **Influencer Campaign** workflow from the Marketing Suite.

## Your Mission

Plan and execute a complete influencer marketing campaign from strategy through measurement.

## Process Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        INFLUENCER CAMPAIGN WORKFLOW                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  PHASE 1        PHASE 2        PHASE 3        PHASE 4        PHASE 5           │
│  ────────       ────────       ────────       ────────       ────────           │
│  Strategy   →   Discovery  →   Activate   →   Execute    →   Measure           │
│  /marketing     /influencer    /influencer    /community     /marketing        │
│  /influencer    /copywriter    /copywriter    /influencer    /influencer       │
│                                                                                  │
│  Week 1         Week 2         Week 3-4       Week 4-8       Week 8+           │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Strategy (Week 1)

### Agent: `/strategist` → `/influencer`

### 1.1 Campaign Objectives

```bash
/marketing
*campaign-create     # Campaign brief with influencer focus
```

**Define:**

| Element | Definition |
|---------|------------|
| Objective | Awareness / Engagement / Conversions / Content |
| KPIs | Reach, EMV, Engagement Rate, Conversions, UGC pieces |
| Budget | Total and per-influencer allocation |
| Timeline | Campaign duration and key dates |
| Product/Message | What to promote and key messages |

### 1.2 Influencer Strategy

```bash
/influencer
*strategy            # Comprehensive influencer strategy
```

**Determine:**

| Decision | Options |
|----------|---------|
| Influencer Tier | Nano / Micro / Mid / Macro / Mega |
| Platform Focus | Instagram / TikTok / YouTube / Twitter / LinkedIn |
| Content Type | Posts / Stories / Reels / Videos / Reviews |
| Relationship | One-off / Campaign / Ambassador |
| Compensation | Gifting / Flat fee / Performance / Hybrid |

### 1.3 Target Influencer Profile

```markdown
## Ideal Influencer Profile

**Demographics:**
- Audience age: [Range]
- Audience gender: [Split]
- Audience location: [Regions]

**Content Style:**
- Aesthetic: [Description]
- Tone: [Professional/Casual/Edgy/etc.]
- Content frequency: [X posts/week]

**Engagement:**
- Minimum engagement rate: [X%]
- Minimum followers: [X]
- Maximum followers: [X]

**Values Alignment:**
- Topics covered: [List]
- Brand safety: [Requirements]
- Exclusions: [Categories to avoid]
```

### Phase 1 Gate

- [ ] Campaign objectives defined
- [ ] Influencer strategy approved
- [ ] Budget allocated
- [ ] Target profile documented

---

## Phase 2: Discovery & Vetting (Week 2)

### Agent: `/influencer`

### 2.1 Influencer Discovery

```bash
/influencer
*discover            # Find potential influencers
```

**Sources:**
- Platform native search (hashtags, explore)
- Influencer platforms (AspireIQ, Grin, CreatorIQ)
- Competitor analysis (who do they work with?)
- Community recommendations
- Agency networks

**Create longlist:** 50-100 potential influencers

### 2.2 Vetting Process

```bash
/influencer
*vet                 # Deep-dive vetting
```

**Vetting Checklist:**

| Criteria | Weight | Score (1-5) |
|----------|--------|-------------|
| Audience demographics match | 20% | |
| Content quality | 20% | |
| Engagement rate | 15% | |
| Brand alignment | 15% | |
| Past brand partnerships | 10% | |
| Authenticity (fake follower check) | 10% | |
| Professionalism (past issues) | 10% | |

**Red Flags:**
- Engagement rate <1% or >10% (suspicious)
- Sudden follower spikes
- Generic/bot comments
- Controversial past content
- Competing brand partnerships

### 2.3 Shortlist Creation

**Tier the shortlist:**

| Tier | Count | Budget/Person | Expected Reach |
|------|-------|---------------|----------------|
| Anchor (Macro) | 1-2 | $X,XXX | X M |
| Core (Mid) | 5-10 | $X,XXX | X00K each |
| Scale (Micro) | 10-20 | $XXX | X0K each |
| Nano/Gifting | 20-50 | Product only | XK each |

### Phase 2 Gate

- [ ] Longlist created (50-100)
- [ ] Vetting completed
- [ ] Shortlist finalized (20-30)
- [ ] Budget per tier allocated

---

## Phase 3: Activation (Week 3-4)

### Agents: `/influencer` → `/copywriter`

### 3.1 Outreach

```bash
/influencer
*outreach-email      # Craft outreach messages
```

**Outreach Sequence:**

| Email | Timing | Purpose |
|-------|--------|---------|
| Initial | Day 0 | Introduction, partnership interest |
| Follow-up 1 | Day 3 | Gentle reminder |
| Follow-up 2 | Day 7 | Final attempt |

**Outreach Template:**
```
Subject: Collaboration with [Brand] 🤝

Hi [Name],

I've been following your content on [platform] and love your
[specific content reference]. Your [specific quality] really
resonates with our brand.

We're launching [product/campaign] and think you'd be a perfect
fit to share it with your audience.

Here's what we're thinking:
- [Deliverables]
- [Compensation/value]
- [Timeline]

Would you be interested in chatting more?

Best,
[Your name]
[Brand]
```

### 3.2 Negotiation & Contracting

```bash
/influencer
*contract            # Partnership agreement
```

**Negotiate:**
- Deliverables (type, quantity)
- Timeline and deadlines
- Compensation structure
- Usage rights
- Exclusivity period
- Revision rounds

**Contract Must Include:**
- [ ] Deliverables specification
- [ ] Payment terms
- [ ] Content ownership/licensing
- [ ] FTC disclosure requirements
- [ ] Approval process
- [ ] Exclusivity clause
- [ ] Termination conditions

### 3.3 Creative Brief

```bash
/influencer
*brief               # Creative brief for influencers
```

```bash
/copywriter
*messaging-framework # Key messages
*hook                # Hook suggestions
```

**Brief Contents:**

```markdown
## Campaign Brief: [Campaign Name]

### About the Brand
[2-3 sentences about brand]

### Campaign Objective
[What we want to achieve]

### Product Information
- Product: [Name]
- Key features: [List]
- Key benefits: [List]
- Price: [If applicable]

### Key Messages
Must mention:
- [Message 1]
- [Message 2]

Can mention:
- [Optional message]

Do NOT mention:
- [Competitor names]
- [Specific claims we can't make]

### Content Requirements
- Platform: [Specific platform]
- Format: [Post/Story/Reel/Video]
- Length: [If video, duration]
- Posting date: [Date or range]
- Hashtags: #sponsored #ad [brand hashtags]
- Tag: @[brand handle]
- Link: [If applicable]

### Creative Direction
- Tone: [Authentic, fun, educational, etc.]
- Style: [Match your usual content]
- We love when you: [Examples of their content we liked]

### What NOT to Do
- [Don't make medical claims]
- [Don't bash competitors]
- [Don't use copyrighted music]

### Approval Process
1. Submit draft by [date]
2. We review within 48 hours
3. Max 2 revision rounds
4. Final approval before posting

### Deliverables Summary
| Deliverable | Due Date | Platform |
|-------------|----------|----------|
| [Item 1] | [Date] | [Platform] |
```

### Phase 3 Gate

- [ ] Outreach completed
- [ ] Contracts signed
- [ ] Briefs delivered
- [ ] Product shipped (if applicable)

---

## Phase 4: Execution (Week 4-8)

### Agents: `/influencer` → `/community`

### 4.1 Content Review & Approval

```bash
/influencer
*review              # Review submitted content
```

**Review Checklist:**
- [ ] Key messages included
- [ ] Required hashtags/disclosures
- [ ] Brand mentioned/tagged correctly
- [ ] No competitor mentions
- [ ] Content quality meets standards
- [ ] Aligns with brand guidelines
- [ ] Posting time confirmed

### 4.2 Posting Coordination

**Content Calendar:**

| Influencer | Platform | Post Date | Post Time | Status |
|------------|----------|-----------|-----------|--------|
| @influencer1 | Instagram | [Date] | [Time] | Scheduled |
| @influencer2 | TikTok | [Date] | [Time] | Approved |

### 4.3 Amplification

```bash
/community
*engage              # Engage with influencer posts
```

**Brand Actions:**
- Like and comment on all posts (within 1 hour)
- Share to brand stories
- Respond to comments on influencer posts
- Boost top-performing posts (if rights allow)

### 4.4 Community Management

```bash
/community
*respond             # Handle audience comments
*ugc-curate          # Capture valuable UGC
```

**Monitor:**
- Comments on influencer posts
- Brand mentions from influencer's audience
- UGC created as result of campaign
- Questions requiring brand response

### Phase 4 Gate

- [ ] All content posted
- [ ] Brand engagement completed
- [ ] UGC captured
- [ ] Issues addressed

---

## Phase 5: Measurement (Week 8+)

### Agents: `/influencer` → `/strategist`

### 5.1 Performance Tracking

```bash
/influencer
*campaign-report     # Comprehensive report
```

**Metrics to Track:**

| Metric | Calculation | Target | Actual |
|--------|-------------|--------|--------|
| Total Reach | Sum of impressions | | |
| Engagement Rate | (Likes+Comments)/Reach | | |
| EMV | Earned media value | | |
| CPE | Cost per engagement | | |
| Conversions | Link clicks/sales | | |
| UGC Pieces | Content created | | |
| New Followers | Brand follower growth | | |

### 5.2 ROI Analysis

```bash
/marketing
*analytics-report    # Campaign ROI
```

**Calculate:**
- Total investment (fees + product + management)
- Total value generated (EMV + conversions)
- ROI = (Value - Investment) / Investment
- Compare to other channel performance

### 5.3 Influencer Scorecard

| Influencer | Reach | Engagement | Conversions | Professionalism | Score | Action |
|------------|-------|------------|-------------|-----------------|-------|--------|
| @name1 | A | A | B | A | 4.0 | Ambassador |
| @name2 | B | C | A | B | 3.0 | Reuse |
| @name3 | C | D | D | A | 2.5 | Review |

### 5.4 Learnings & Optimization

**Document:**
- Top performing content types
- Best posting times/days
- Most effective influencer tiers
- Messages that resonated
- What to do differently

### 5.5 Relationship Development

```bash
/influencer
*ambassador-program  # Convert top performers
```

**For top performers:**
- Thank you note/gift
- Invite to ambassador program
- First look at new products
- Long-term partnership discussion

---

## Documentation Structure

```
docs/marketing/influencer/
├── campaigns/
│   └── {campaign-name}/
│       ├── strategy.md
│       ├── influencer-list.md
│       ├── contracts/
│       ├── briefs/
│       ├── content/
│       └── report.md
├── ambassadors/
│   └── program-overview.md
└── templates/
    ├── outreach-templates.md
    ├── brief-template.md
    └── contract-template.md
```

## Begin

Start by asking:

1. "What is the main campaign objective?"
2. "What is the total budget?"
3. "Which platform is the priority?"
4. "Is this a one-off campaign or are you looking for long-term relationships?"

Then proceed to Phase 1: Strategy.
