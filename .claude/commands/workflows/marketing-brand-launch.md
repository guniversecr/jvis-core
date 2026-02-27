---
description: Complete brand launch from strategy to market introduction
---

# Marketing Suite: Brand Launch Workflow

You are now executing the **Brand Launch** workflow from the Marketing Suite.

## Your Mission

Guide the complete brand launch process from brand strategy development through market introduction, coordinating multiple specialized agents.

## Process Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           BRAND LAUNCH WORKFLOW                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  FASE 1        FASE 2         FASE 3         FASE 4        FASE 5              │
│  ────────      ────────       ────────       ────────      ────────            │
│  Strategy  →   Identity   →   Content    →   Launch    →   Activation          │
│  /strategist   /brand         /copywriter    /pr           /marketing          │
│  /brand        /ux-expert     /creative-dir  /events       /community          │
│                                                                                  │
│  Week 1-2      Week 2-4       Week 4-6       Week 6-8      Week 8+             │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Phase 1: Brand Strategy (Week 1-2)

### Agents: `/strategist` → `/brand`

### 1.1 Market Positioning

```bash
/strategist
*market-scan
*competitor-analysis
*positioning-strategy
```

**Define:**
- Market opportunity
- Competitive landscape
- Target audience
- Positioning statement

### 1.2 Brand Strategy

```bash
/brand
*strategy
*positioning
*archetype
```

**Deliverables:**
- Brand purpose, vision, mission
- Brand values
- Brand archetype selection
- Positioning statement
- Brand promise

### Phase 1 Gate

- [ ] Market research complete
- [ ] Positioning approved
- [ ] Brand strategy documented
- [ ] Stakeholder sign-off

**Save to:** `docs/brand/strategy/brand-strategy-{date}.md`

---

## Phase 2: Brand Identity (Week 2-4)

### Agents: `/brand` → `/ux-expert`

### 2.1 Verbal Identity

```bash
/brand
*voice
*messaging
*naming (if needed)
```

**Define:**
- Brand voice & tone
- Key messages by audience
- Tagline/slogan
- Naming conventions

### 2.2 Visual Identity

```bash
/ux-expert
*brand-assets
*color-system
*typography-system
*design-system
```

**Create:**
- Logo system (primary, secondary, icon)
- Color palette (primary, secondary, accent)
- Typography scale
- Photography/illustration style
- Iconography system

### 2.3 Brand Guidelines

```bash
/brand
*guidelines
```

**Document:**
- Logo usage rules
- Color specifications
- Typography rules
- Voice & tone guidelines
- Do's and don'ts

### Phase 2 Gate

- [ ] Visual identity approved
- [ ] Verbal identity approved
- [ ] Brand guidelines complete
- [ ] Asset library created

**Save to:** `docs/brand/identity/`

---

## Phase 3: Content Creation (Week 4-6)

### Agents: `/copywriter` → `/creative-director` → `/video-producer`

### 3.1 Messaging Framework

```bash
/copywriter
*voice-guide
*messaging-framework
*boilerplate
```

**Create:**
- Brand story
- Elevator pitches (30s, 60s, 2min)
- Boilerplate copy
- Key messages by channel

### 3.2 Creative Direction

```bash
/creative-director
*creative-strategy
*creative-brief
*campaign-canvas
```

**Define:**
- Creative concept for launch
- Visual direction
- Campaign look & feel
- Asset requirements

### 3.3 Content Production

```bash
/copywriter
*landing-hero
*ad-google
*ad-meta
*email-welcome
```

```bash
/ux-expert
*social-graphic
*ad-creative
*presentation-design
```

```bash
/video-producer
*script-corporate
*storyboard
*production-plan
```

**Produce:**
- Website copy
- Launch video script
- Ad copy (all platforms)
- Social content
- Email sequences
- Sales materials

### Phase 3 Gate

- [ ] All copy written and approved
- [ ] Creative assets produced
- [ ] Video content scripted
- [ ] Launch materials ready

**Save to:** `docs/brand/content/`

---

## Phase 4: Launch Execution (Week 6-8)

### Agents: `/pr` → `/events` → `/comms`

### 4.1 PR & Communications

```bash
/pr
*press-release
*media-list
*pitch-email
*press-kit
```

**Prepare:**
- Press release
- Media kit
- Journalist outreach list
- Pitch angles

### 4.2 Launch Event

```bash
/events
*launch-event
*agenda
*promotion-plan
*run-of-show
```

**Plan:**
- Launch event format (virtual/in-person/hybrid)
- Agenda and speakers
- Invitations and registration
- Run of show

### 4.3 Internal Communications

```bash
/comms
*announcement
*manager-brief
*all-hands
```

**Prepare:**
- Internal announcement
- Manager talking points
- All-hands presentation
- Employee FAQ

### Phase 4 Gate

- [ ] PR materials approved
- [ ] Launch event planned
- [ ] Internal comms ready
- [ ] Launch date confirmed

**Save to:** `docs/brand/launch/`

---

## Phase 5: Market Activation (Week 8+)

### Agents: `/strategist` → `/media-buyer` → `/community` → `/influencer`

### 5.1 Paid Media

```bash
/marketing
*campaign-create
*campaign-launch
```

```bash
/media-buyer
*media-plan
*programmatic-strategy
*budget-allocation
```

**Execute:**
- Paid search campaigns
- Social advertising
- Display/programmatic
- Retargeting

### 5.2 Influencer Activation

```bash
/influencer
*strategy
*discover
*outreach-email
*brief
```

**Execute:**
- Influencer identification
- Partnership negotiations
- Content briefs
- Campaign coordination

### 5.3 Community Building

```bash
/community
*strategy
*engagement-plan
*welcome
*ugc-campaign
```

**Build:**
- Community channels
- Welcome sequences
- Engagement calendar
- UGC initiatives

### Phase 5 Gate

- [ ] Campaigns live
- [ ] Influencers activated
- [ ] Community growing
- [ ] Metrics tracking

---

## Measurement & Optimization

### KPIs by Phase

| Phase | Key Metrics |
|-------|-------------|
| Strategy | Stakeholder approval, research depth |
| Identity | Asset completion, guideline adoption |
| Content | Content volume, approval rate |
| Launch | PR coverage, event attendance |
| Activation | Reach, engagement, conversions |

### Brand Health Metrics

```bash
/strategist
*pmf-check
```

Track:
- Brand awareness (aided/unaided)
- Brand consideration
- Brand preference
- Net Promoter Score
- Share of voice

---

## Documentation Structure

```
docs/brand/
├── strategy/
│   ├── market-research-{date}.md
│   ├── brand-strategy-{date}.md
│   └── positioning-{date}.md
├── identity/
│   ├── visual-identity.md
│   ├── verbal-identity.md
│   └── brand-guidelines.md
├── content/
│   ├── messaging-framework.md
│   ├── creative-briefs/
│   └── assets/
├── launch/
│   ├── pr-plan.md
│   ├── event-plan.md
│   └── internal-comms.md
└── campaigns/
    ├── paid-media-plan.md
    ├── influencer-plan.md
    └── reports/
```

## Agent Handoff Protocol

| From | To | Handoff File | Content |
|------|-----|--------------|---------|
| `/strategist` | `/brand` | `from-marketing.md` | Market insights, positioning |
| `/brand` | `/copywriter` | `from-brand.md` | Voice guide, messaging |
| `/brand` | `/ux-expert` | `from-brand.md` | Visual direction |
| `/creative-director` | `/video-producer` | `from-creative-director.md` | Creative brief |
| `/pr` | `/strategist` | `from-pr.md` | Launch timing, key messages |
| `/strategist` | `/community` | `from-marketing.md` | Campaign details |

## Begin

Start by asking:

1. "Is this a new brand or a rebrand?"
2. "What is the target timeline for launch?"
3. "Is there a defined budget?"

Based on answers, determine:
- **New brand:** Start at Phase 1
- **Rebrand:** May skip parts of Phase 1
- **Tight timeline:** Identify phases to parallelize
