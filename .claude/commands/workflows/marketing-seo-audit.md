---
description: Complete SEO/SEM audit workflow for websites
---

# Marketing Suite: SEO/SEM Audit

You are now executing the **SEO/SEM Audit** workflow from the Marketing & Strategy Suite.

## Your Mission

Conduct a comprehensive SEO and SEM audit of a website, providing actionable recommendations.

## Process Steps

### Step 1: Target Definition

Ask the user:

```
1. What is the URL of the site to audit?
2. Who are the main competitors?
3. What are the current target keywords?
4. Are there any specific areas of concern?
```

### Step 2: Technical SEO Audit

Use `/strategist` agent with MCP research-server:

```bash
/marketing
*seo-audit <url>
```

**Check List:**

#### Crawlability & Indexing
- [ ] Robots.txt configuration
- [ ] XML Sitemap present and valid
- [ ] No index/nofollow tags appropriate
- [ ] Canonical tags implemented
- [ ] Hreflang for international sites

#### Site Speed
- [ ] Core Web Vitals (LCP, FID, CLS)
- [ ] Page load time < 3s
- [ ] Image optimization
- [ ] Code minification
- [ ] CDN usage

#### Mobile Optimization
- [ ] Mobile-friendly design
- [ ] Responsive images
- [ ] Touch-friendly navigation
- [ ] Mobile page speed

#### Security
- [ ] HTTPS implemented
- [ ] No mixed content
- [ ] Security headers

### Step 3: On-Page SEO Analysis

**For each key page, check:**

| Element | Best Practice |
|---------|---------------|
| Title Tag | 50-60 chars, keyword included |
| Meta Description | 150-160 chars, compelling CTA |
| H1 | One per page, includes keyword |
| URL Structure | Short, descriptive, hyphenated |
| Image Alt Text | Descriptive, includes keywords |
| Internal Links | Logical structure, anchor text |

### Step 4: Content Analysis

```bash
*keyword-research
```

**Evaluate:**
- Content quality and uniqueness
- Keyword optimization (density, placement)
- Content freshness
- E-A-T signals (Expertise, Authority, Trust)
- User intent alignment

### Step 5: Off-Page SEO

**Backlink Profile:**
- Total backlinks
- Referring domains
- Domain authority of linking sites
- Anchor text distribution
- Toxic links to disavow

**Brand Signals:**
- Social media presence
- Brand mentions
- Local citations (if applicable)

### Step 6: SEM Analysis

```bash
*sem-analysis <url>
```

**Review:**
- Current PPC campaigns (if visible)
- Competitor ad strategies
- Keyword opportunities for paid
- Landing page quality

### Step 7: Competitor Comparison

| Metric | Your Site | Competitor 1 | Competitor 2 |
|--------|-----------|--------------|--------------|
| Domain Authority | - | - | - |
| Organic Keywords | - | - | - |
| Backlinks | - | - | - |
| Page Speed | - | - | - |

### Step 8: Recommendations

Prioritize findings:

**Priority Matrix:**

| Impact | Effort | Priority |
|--------|--------|----------|
| High | Low | DO FIRST |
| High | High | PLAN |
| Low | Low | QUICK WINS |
| Low | High | CONSIDER |

### Step 9: Documentation

Save audit to: `docs/seo-audits/audit-{domain}-{date}.md`

## Output Format

```markdown
# SEO/SEM Audit Report

**Site:** [URL]
**Date:** [Date]
**Auditor:** Marketing Suite

## Executive Summary

**Overall Score:** X/100

| Category | Score | Status |
|----------|-------|--------|
| Technical SEO | X/25 | 🔴/🟡/🟢 |
| On-Page SEO | X/25 | 🔴/🟡/🟢 |
| Content | X/25 | 🔴/🟡/🟢 |
| Off-Page SEO | X/25 | 🔴/🟡/🟢 |

## Critical Issues (Fix Immediately)
1. [Issue + Solution]

## High Priority (This Month)
1. [Issue + Solution]

## Medium Priority (This Quarter)
1. [Issue + Solution]

## Opportunities
1. [Opportunity + Action]

## Detailed Findings
[Categorized findings with evidence]

## Competitor Insights
[Key learnings from competitors]

## Action Plan
| # | Action | Priority | Effort | Owner |
|---|--------|----------|--------|-------|
| 1 | [Action] | High | Low | - |
```

## Begin

Ask the user for the URL they want to audit.
