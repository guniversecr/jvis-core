---
description: Crisis communications response workflow
---

# Marketing Suite: Crisis Communications Workflow

You are now executing the **Crisis Communications** workflow from the Marketing Suite.

## Your Mission

Manage communications during a crisis - from initial response through resolution and recovery.

## Process Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      CRISIS COMMUNICATIONS WORKFLOW                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  DETECT         ASSESS          RESPOND         MANAGE         RECOVER          │
│  ──────         ──────          ───────         ──────         ───────          │
│                                                                                  │
│  /community     /pr             /pr             /comms         /marketing       │
│  /pr            /comms          /comms          /community     /pr              │
│                                 /community      /pr            /community       │
│                                                                                  │
│  0-1 hour       1-2 hours       2-4 hours       Ongoing        Post-crisis      │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Crisis Severity Levels

| Level | Description | Response Time | Escalation |
|-------|-------------|---------------|------------|
| **1 - Watch** | Potential issue emerging | Monitor | Team lead |
| **2 - Alert** | Active issue, limited exposure | 2-4 hours | Director |
| **3 - Crisis** | Significant exposure, media interest | 1-2 hours | VP/CMO |
| **4 - Emergency** | Major crisis, widespread impact | Immediate | C-Suite |

---

## Phase 1: Detection & Triage (0-1 hour)

### Agent: `/community` → `/pr`

### 1.1 Initial Detection

```bash
/community
*triage              # Assess the situation
```

**Detection Sources:**
- Social media mentions spike
- Customer complaints surge
- Media inquiry
- Internal report
- Competitor action
- Regulatory notice

### 1.2 Rapid Assessment

```bash
/pr
*crisis-assess       # Quick assessment
```

**Assessment Questions:**

| Question | Answer |
|----------|--------|
| What happened? | [Facts only] |
| When did it start? | [Timeline] |
| Who is affected? | [Stakeholders] |
| What's the exposure? | [Reach/visibility] |
| Is it escalating? | [Trend direction] |
| Do we have media inquiries? | [Yes/No, count] |
| Legal/regulatory implications? | [Assessment] |

### 1.3 Severity Determination

**Severity Matrix:**

| Factor | Low (1) | Medium (2-3) | High (4) |
|--------|---------|--------------|----------|
| Exposure | <1K views | 1K-100K views | >100K views |
| Media | No inquiries | Trade media | National media |
| Impact | Minor inconvenience | Service disruption | Safety/legal |
| Duration | Hours | Days | Extended |
| Sentiment | Mildly negative | Angry | Outraged |

### 1.4 Escalation

**Escalation Path:**

```
Detection → Community Manager → PR Lead → Communications Director → CMO → CEO
                 (L1)            (L2)           (L3)              (L4)
```

### Phase 1 Gate

- [ ] Situation documented
- [ ] Severity level assigned
- [ ] Appropriate stakeholders notified
- [ ] Response team assembled
- [ ] Holding statement ready

---

## Phase 2: Response Preparation (1-4 hours)

### Agents: `/pr` → `/comms`

### 2.1 Holding Statement

```bash
/pr
*holding-statement   # Initial statement
```

**Holding Statement Template:**

```
We are aware of [situation description] and are actively
investigating. [Empathy statement if applicable].

We take this matter seriously and will provide updates
as more information becomes available.

For questions, please contact [contact info].
```

### 2.2 Fact Gathering

**Information Needed:**

| Category | Questions | Status |
|----------|-----------|--------|
| What | Exact nature of issue | [ ] |
| When | Timeline of events | [ ] |
| Who | Affected parties | [ ] |
| Why | Root cause (if known) | [ ] |
| Impact | Scope and severity | [ ] |
| Actions | What's being done | [ ] |

### 2.3 Stakeholder Mapping

```bash
/comms
*stakeholder-map     # Crisis stakeholders
```

**Priority Stakeholders:**

| Stakeholder | Priority | Channel | Message Focus |
|-------------|----------|---------|---------------|
| Affected customers | 1 | Direct/Email | Apology, resolution |
| All customers | 2 | Email/Social | Awareness, reassurance |
| Employees | 2 | Internal comms | Facts, talking points |
| Media | 3 | Press statement | Official position |
| Partners | 3 | Direct outreach | Impact, coordination |
| Investors | 4 | Direct/Filing | Material impact |
| Regulators | 4 | Formal channels | Compliance |

### 2.4 Message Development

```bash
/pr
*crisis-external     # External statement
```

```bash
/comms
*crisis-internal     # Internal communications
*manager-brief       # Manager talking points
```

**Key Message Framework:**

1. **Acknowledge** - We're aware of the issue
2. **Empathy** - We understand the impact
3. **Action** - Here's what we're doing
4. **Timeline** - When to expect resolution/updates
5. **Contact** - How to reach us

### 2.5 Q&A Preparation

```bash
/pr
*faq                 # Crisis FAQ
```

**Anticipated Questions:**

| Question | Approved Answer | If Pushed |
|----------|-----------------|-----------|
| What happened? | [Answer] | [Bridge] |
| Who is affected? | [Answer] | [Bridge] |
| What caused it? | [Answer if known] | [Bridge] |
| What are you doing? | [Answer] | [Expand] |
| When will it be fixed? | [Answer] | [Caveat] |
| Will there be compensation? | [Answer] | [Bridge] |

### Phase 2 Gate

- [ ] Holding statement approved and deployed
- [ ] Full statement drafted
- [ ] Internal communications ready
- [ ] FAQ prepared
- [ ] Spokesperson briefed
- [ ] Response channels identified

---

## Phase 3: Active Response (Hours to Days)

### Agents: `/pr` + `/comms` + `/community`

### 3.1 External Communications

```bash
/pr
*press-release       # Official statement
*media-response      # Media handling
```

**Communication Cadence:**

| Timing | Action | Channel |
|--------|--------|---------|
| T+0 | Holding statement | Social, website |
| T+2h | Full statement | Press release, email |
| T+4h | Update #1 | All channels |
| T+24h | Progress update | All channels |
| Daily | Status updates | As needed |
| Resolution | Final communication | All channels |

### 3.2 Internal Communications

```bash
/comms
*announcement        # Employee update
*all-hands           # If needed for major crisis
```

**Internal Communication Flow:**

```
Leadership → Managers → All Employees
    ↓           ↓           ↓
 Briefing   Talking    Company-wide
            Points     announcement
```

### 3.3 Social Media Management

```bash
/community
*respond             # Social responses
*moderate            # Monitor and moderate
*escalate            # Escalate issues
```

**Social Media Protocol:**

| Mention Type | Response | Time |
|--------------|----------|------|
| Direct complaint | Personalized response | <1 hour |
| Question | FAQ response | <2 hours |
| Angry/frustrated | Empathy + resolution | <1 hour |
| Misinformation | Factual correction | <30 min |
| Media inquiry | Route to PR | Immediate |

**Response Framework:**

```
1. Acknowledge: "We hear you and understand your frustration."
2. Apologize: "We're sorry for the inconvenience this has caused."
3. Act: "Here's what we're doing: [action]"
4. Assist: "Please DM us / contact [channel] for help."
```

### 3.4 Media Relations

```bash
/pr
*media-response      # Handle media inquiries
```

**Media Handling:**

- Designate single spokesperson
- Log all media inquiries
- Respond within committed timeframe
- Stick to approved messaging
- Offer interviews strategically

### 3.5 War Room Operations

**Daily Crisis Rhythm:**

| Time | Activity | Participants |
|------|----------|--------------|
| 8:00 AM | Situation update | Full team |
| 12:00 PM | Mid-day check | Core team |
| 4:00 PM | End of day review | Full team |
| As needed | Ad hoc updates | Varies |

**Tracking Dashboard:**

| Metric | Current | Trend |
|--------|---------|-------|
| Social mentions | X | ↑↓→ |
| Sentiment | X% neg | ↑↓→ |
| Media stories | X | ↑↓→ |
| Support tickets | X | ↑↓→ |
| Resolution progress | X% | ↑↓→ |

### Phase 3 Gate

- [ ] Stakeholders communicated to
- [ ] Social media managed
- [ ] Media inquiries handled
- [ ] Internal alignment maintained
- [ ] Issue progressing to resolution

---

## Phase 4: Resolution & Recovery (Post-Crisis)

### Agents: `/pr` + `/comms` + `/strategist` + `/community`

### 4.1 Resolution Communication

```bash
/pr
*crisis-resolution   # Resolution announcement
```

**Resolution Statement Elements:**

1. Issue is resolved
2. Summary of what happened
3. What was done to fix it
4. What's being done to prevent recurrence
5. Appreciation for patience
6. Next steps (if any)

### 4.2 Post-Mortem

```bash
/comms
*post-mortem         # Internal review
```

**Post-Mortem Questions:**

| Area | Questions |
|------|-----------|
| Detection | How/when was it identified? Could we have detected sooner? |
| Response | Was response timely? Were stakeholders informed properly? |
| Messaging | Was messaging clear and consistent? |
| Coordination | Did teams work well together? |
| Tools | Did we have what we needed? |
| Outcome | What was the ultimate impact? |
| Prevention | How do we prevent recurrence? |

### 4.3 Stakeholder Recovery

```bash
/crm
*segment             # Affected customer segment
*automation          # Recovery outreach
```

**Recovery Actions:**

| Stakeholder | Recovery Action |
|-------------|-----------------|
| Directly affected | Personal outreach, compensation |
| Concerned customers | Reassurance communication |
| Churned during crisis | Win-back campaign |
| Employees | Recognition, debrief |
| Partners | Relationship repair |

### 4.4 Reputation Recovery

```bash
/marketing
*campaign-create     # Reputation campaign
```

```bash
/pr
*thought-leadership  # Positive PR
```

```bash
/community
*advocate-activate   # Mobilize supporters
*ugc-campaign        # Positive stories
```

**Recovery Tactics:**

- Positive storytelling campaign
- Customer success stories
- Thought leadership content
- Community goodwill building
- Employee advocacy
- CSR/giving initiatives

### Phase 4 Gate

- [ ] Resolution communicated
- [ ] Post-mortem completed
- [ ] Learnings documented
- [ ] Prevention measures identified
- [ ] Recovery plan in action
- [ ] Metrics returning to baseline

---

## Crisis Documentation

### During Crisis

```
docs/crisis/
├── {crisis-name}/
│   ├── timeline.md           # Chronological log
│   ├── statements/
│   │   ├── holding.md
│   │   ├── official.md
│   │   └── updates/
│   ├── internal/
│   │   ├── employee-comms.md
│   │   └── talking-points.md
│   ├── media/
│   │   ├── inquiries-log.md
│   │   └── coverage.md
│   ├── social/
│   │   └── response-log.md
│   └── post-mortem.md
```

### Crisis Playbook Update

After each crisis, update:
- Response templates
- Escalation procedures
- Contact lists
- Tool/process improvements

---

## Pre-Crisis Preparation

### Always Ready

```bash
/pr
*crisis-plan         # Crisis preparedness plan
```

**Preparedness Checklist:**

- [ ] Crisis team identified
- [ ] Contact tree current
- [ ] Spokesperson trained
- [ ] Holding statements drafted
- [ ] Social monitoring active
- [ ] Dark site ready (for major crises)
- [ ] Escalation procedures documented

## Begin

If crisis is active, immediately:

1. "What is the current situation?"
2. "When did it start?"
3. "Which stakeholders are affected?"
4. "Are there media inquiries?"

Then proceed to Phase 1: Detection & Triage.
