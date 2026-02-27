# Journey Start

Initialize journey tracking for a new project.

## Instructions

### 1. Create Journey Structure

```bash
mkdir -p docs/journey
mkdir -p docs/ideation
mkdir -p docs/validation
mkdir -p docs/planning
```

### 2. Initialize Journey State

Copy from `.jvis/journey/state-template.yaml` to `docs/journey/journey-state.yaml`

Update:
- `project.name` - From package.json, pyproject.toml, or ask user
- `project.started` - Today's date
- `current_phase` - "ideation"
- `phases.ideation.status` - "in_progress"
- `phases.ideation.started` - Today's date

### 3. Create Idea Brief Template

Create `docs/ideation/idea-brief.md`:

```markdown
# Idea Brief

## Problem Statement

What problem are you solving? Who has this problem?

[Describe the problem clearly]

## Target Audience

Who is your ideal customer?

- **Demographics:**
- **Psychographics:**
- **Current solutions they use:**

## Proposed Solution

What will you build to solve this problem?

[High-level description of your solution]

## Why Now?

Why is this the right time to build this?

- Market trends:
- Technology enablers:
- Competitive gaps:

## Success Metrics

How will you measure success?

1.
2.
3.

---

*Next step: Run `/strategist` and use `*idea-score` to evaluate this idea*
```

### 4. Display Welcome Message

```markdown
# 🚀 Journey Started!

Your project journey has been initialized.

**Current Phase:** 💡 Ideation
**Progress:** 0/35 checkpoints (0%)

## First Steps

1. **Complete Idea Brief**
   Edit `docs/ideation/idea-brief.md` with your idea details

2. **Score Your Idea**
   ```
   /strategist
   *idea-score
   ```
   Minimum score of 6/10 required to proceed

3. **Check Progress**
   ```
   /journey:status
   ```

## Journey Phases

1. 💡 **Ideation** ← You are here
2. 🔬 Validation
3. 📋 Planning
4. 🔨 Development
5. 🚀 Production

Good luck! 🍀
```

## Success Criteria

- [ ] Journey directories created
- [ ] State file initialized
- [ ] Idea brief template created
- [ ] Welcome message displayed
- [ ] First steps explained
