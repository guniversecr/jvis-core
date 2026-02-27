---
description: Content production pipeline from brief to multi-channel distribution
---

# Marketing Suite: Content Production Pipeline

You are now executing the **Content Production Pipeline** workflow from the Marketing Suite.

## Your Mission

Orchestrate efficient content production from brief through creation, approval, and multi-channel distribution.

## Process Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                       CONTENT PRODUCTION PIPELINE                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  BRIEF         CREATE          REVIEW         DISTRIBUTE      MEASURE           │
│  ─────         ──────          ──────         ──────────      ───────           │
│                                                                                  │
│  /marketing    /copywriter     /creative-dir  /marketing      /marketing        │
│  /creative-dir /ux-expert      /brand         /community                        │
│               /video-producer                                                    │
│                                                                                  │
│  Day 1         Day 2-7         Day 7-8        Day 8+          Ongoing           │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Brief & Planning

### Agents: `/strategist` → `/creative-director`

### 1.1 Content Strategy

```bash
/marketing
*content-strategy    # Content marketing strategy
*content-calendar    # Monthly content plan
```

**Define:**
- Content pillars (3-5 themes)
- Content types per pillar
- Channel mix
- Publishing cadence
- Success metrics

### 1.2 Content Brief

```bash
/creative-director
*creative-brief      # Individual content brief
```

**Brief Template:**

```markdown
## Content Brief: [Title]

### Overview
**Content Type:** [Blog / Video / Social / Email / etc.]
**Primary Channel:** [Where it will live]
**Secondary Channels:** [Repurpose destinations]
**Due Date:** [Date]

### Objective
**Goal:** [Awareness / Engagement / Conversion / Education]
**Target Action:** [What should audience do?]

### Audience
**Primary:** [Persona]
**Stage:** [Awareness / Consideration / Decision]
**Pain Points:** [What problem does this solve?]

### Key Messages
**Main Message:** [Single sentence]
**Supporting Points:**
1. [Point 1]
2. [Point 2]
3. [Point 3]

### SEO (if applicable)
**Primary Keyword:** [Keyword]
**Secondary Keywords:** [List]
**Search Intent:** [Informational / Commercial / Transactional]

### Creative Direction
**Tone:** [Tone description]
**Style:** [Style description]
**References:** [Links to examples]

### Requirements
**Word Count / Length:** [Specification]
**Visuals Needed:** [List]
**CTA:** [Call to action]
**Links to Include:** [Internal/external links]

### Deliverables
| Asset | Specs | Owner | Due |
|-------|-------|-------|-----|
| [Asset 1] | [Specs] | [Who] | [Date] |

### Approval Chain
1. [Person 1] - [Role]
2. [Person 2] - [Role]
```

### Phase 1 Gate

- [ ] Content calendar approved
- [ ] Briefs created for period
- [ ] Resources assigned
- [ ] Timeline confirmed

---

## Phase 2: Content Creation

### Content Type Workflows

### 2.1 Written Content (Blog, Articles)

```bash
/copywriter
*blog-post           # Write blog content
*seo-optimize        # SEO optimization
```

**Process:**
1. Research and outline
2. First draft
3. SEO optimization
4. Internal review
5. Final polish

**Quality Checklist:**
- [ ] Matches brief requirements
- [ ] Headline is compelling
- [ ] Introduction hooks reader
- [ ] Logical flow and structure
- [ ] Subheadings scannable
- [ ] Internal/external links included
- [ ] CTA clear
- [ ] Meta title/description
- [ ] Images specified

### 2.2 Social Media Content

```bash
/copywriter
*social-post         # Social copy
*hook                # Attention hooks
```

```bash
/ux-expert
*social-graphic      # Visual assets
*carousel-design     # Multi-image posts
*story-design        # Stories/Reels
```

**Platform-Specific:**

| Platform | Copy Length | Visual Specs | Best Practices |
|----------|-------------|--------------|----------------|
| LinkedIn | 1300 chars | 1200x627 | Professional, value-driven |
| Instagram | 2200 chars | 1080x1080/1350 | Visual-first, hashtags |
| Twitter/X | 280 chars | 1200x675 | Concise, engaging |
| TikTok | Brief | 1080x1920 | Trend-aware, authentic |
| Facebook | 500 chars | 1200x630 | Community, shareable |

### 2.3 Video Content

```bash
/video-producer
*script              # Video script
*storyboard          # Visual storyboard
*production-plan     # Production details
```

**Video Workflow:**
1. Script writing
2. Storyboard creation
3. Production planning
4. Filming/animation
5. Editing
6. Sound design
7. Review cuts
8. Final delivery

**Deliverable Types:**
- Hero video (60-90s)
- Social cuts (15s, 30s)
- Stories format (9:16)
- Thumbnail

### 2.4 Email Content

```bash
/copywriter
*email-template      # Email copy
*email-subject       # Subject line options
```

```bash
/ux-expert
*email-design        # Email visual design
```

**Email Checklist:**
- [ ] Subject line A/B options
- [ ] Preview text
- [ ] Header/hero image
- [ ] Body copy clear
- [ ] CTA prominent
- [ ] Mobile responsive
- [ ] Links working
- [ ] Unsubscribe included

### 2.5 Advertising Content

```bash
/copywriter
*ad-google           # Search ads
*ad-meta             # Social ads
*ad-linkedin         # LinkedIn ads
```

```bash
/ux-expert
*ad-creative         # Ad visuals
*banner-design       # Display ads
```

**Ad Content Matrix:**

| Platform | Headlines | Descriptions | Visuals |
|----------|-----------|--------------|---------|
| Google RSA | 15 (30 chars) | 4 (90 chars) | - |
| Meta | 5 variations | 5 variations | 3-5 images |
| LinkedIn | 3 variations | 3 variations | 1200x627 |
| Display | - | - | 6-8 sizes |

---

## Phase 3: Review & Approval

### Agents: `/creative-director` → `/brand`

### 3.1 Creative Review

```bash
/creative-director
*review              # Creative quality review
```

**Review Criteria:**

| Criteria | Weight | Score |
|----------|--------|-------|
| On-brief alignment | 25% | /5 |
| Creative quality | 25% | /5 |
| Message clarity | 20% | /5 |
| Brand consistency | 20% | /5 |
| Technical accuracy | 10% | /5 |

### 3.2 Brand Review

```bash
/brand
*audit               # Brand compliance check
```

**Brand Checklist:**
- [ ] Logo usage correct
- [ ] Colors on-brand
- [ ] Typography correct
- [ ] Voice/tone aligned
- [ ] No brand violations

### 3.3 Approval Workflow

```
Creator → Creative Review → Brand Review → Stakeholder → Final
   ↓           ↓                ↓              ↓
 Draft    Feedback/OK      Feedback/OK    Feedback/OK    Publish
```

**Revision Rules:**
- Max 2 revision rounds per piece
- Feedback consolidated before sending
- 24-48 hour turnaround per round
- Scope creep requires new brief

### Phase 3 Gate

- [ ] Creative approved
- [ ] Brand approved
- [ ] Stakeholder approved
- [ ] Assets finalized
- [ ] All formats exported

---

## Phase 4: Distribution

### Agents: `/strategist` → `/community`

### 4.1 Publishing

```bash
/marketing
*content-calendar    # Publishing schedule
```

**Publishing Checklist:**
- [ ] Content uploaded to CMS/platform
- [ ] Metadata complete (title, description, tags)
- [ ] Images optimized
- [ ] Links verified
- [ ] Scheduled for optimal time
- [ ] Cross-promote planned

### 4.2 Promotion

```bash
/marketing
*content-promote     # Promotion plan
```

**Distribution Matrix:**

| Content Type | Primary | Secondary | Paid |
|--------------|---------|-----------|------|
| Blog | Website | LinkedIn, Twitter, Email | Search, Social |
| Video | YouTube | LinkedIn, TikTok, Instagram | YouTube, Social |
| Infographic | Website | Pinterest, LinkedIn | Display |
| Podcast | Platform | Website, Social, Email | - |

### 4.3 Community Amplification

```bash
/community
*engage              # Community sharing
*respond             # Engagement management
```

**Actions:**
- Share in community channels
- Respond to comments
- Engage with shares
- Answer questions

### 4.4 Repurposing

```bash
/marketing
*content-repurpose   # Repurpose plan
```

**Repurpose Map:**

```
Blog Post (Original)
    ├── Social posts (5-10 per post)
    ├── LinkedIn article
    ├── Email newsletter section
    ├── Video script
    ├── Infographic
    ├── Podcast topic
    ├── Slide deck
    └── Quote graphics
```

---

## Phase 5: Measurement

### Agent: `/strategist`

### 5.1 Performance Tracking

```bash
/marketing
*analytics-report    # Content performance
```

**Metrics by Type:**

| Content Type | Primary Metrics | Secondary |
|--------------|-----------------|-----------|
| Blog | Traffic, Time on page, Conversions | Social shares, Backlinks |
| Video | Views, Watch time, CTR | Engagement rate |
| Social | Reach, Engagement, Saves | Shares, Comments |
| Email | Open rate, CTR, Conversions | Unsubscribes |
| Ads | CTR, Conversions, ROAS | Quality score |

### 5.2 Content Scoring

**Content Performance Score:**

| Factor | Weight | Scoring |
|--------|--------|---------|
| Traffic/Reach | 25% | vs. benchmark |
| Engagement | 25% | vs. benchmark |
| Conversion | 25% | vs. goal |
| Efficiency | 25% | Cost per result |

### 5.3 Optimization

**Based on performance:**
- Update/refresh top performers
- Improve underperformers or sunset
- Scale winning formats
- Test new variations

---

## Content Production Calendar Template

### Weekly View

| Day | Task | Owner | Content |
|-----|------|-------|---------|
| Mon | Briefs for week | Creative Dir | - |
| Tue | Draft creation | Writers/Designers | [List] |
| Wed | Internal review | Creative Dir | [List] |
| Thu | Revisions | Writers/Designers | [List] |
| Fri | Final approval | Stakeholders | [List] |
| Weekend | Scheduled | Auto-publish | [List] |

### Monthly Output Goals

| Content Type | Volume | Distribution |
|--------------|--------|--------------|
| Blog posts | 8-12 | Weekly |
| Social posts | 40-60 | Daily |
| Videos | 2-4 | Bi-weekly |
| Emails | 4-8 | Weekly |
| Ads refresh | 1 set | Monthly |

---

## Documentation Structure

```
docs/marketing/content/
├── strategy/
│   ├── content-strategy.md
│   └── content-pillars.md
├── calendar/
│   └── {month}-calendar.md
├── briefs/
│   └── {content-name}-brief.md
├── assets/
│   ├── copy/
│   ├── images/
│   └── video/
└── reports/
    └── {month}-performance.md
```

## Begin

Start by asking:

1. "Is there an existing content strategy or are we starting from scratch?"
2. "What is the target content volume per month?"
3. "Which channels are the priority?"
4. "Is there a production team or is everything in-house/AI?"

Then proceed to Phase 1: Brief & Planning.
