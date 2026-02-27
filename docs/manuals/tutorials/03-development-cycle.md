# Tutorial 3: Complete Development Cycle

## Objective

Complete a full development cycle: from creating the PRD to committing code with QA approval.

## Prerequisites

- [ ] JVIS project created (Tutorial 1)
- [ ] Claude Code open in the project

## Estimated time: 30 minutes

---

## Phase 1: Create PRD with PM (10 min)

### Step 1.1: Load the PM agent

```bash
# In Claude Code
/pm
```

You will see the agent's welcome message:

```
╔═══════════════════════════════════════════════════════════╗
║  PM Agent - John                                          ║
║  Product Manager specialized in PRDs and backlog          ║
╠═══════════════════════════════════════════════════════════╣
║  Commands: *help, *create-prd, *review-prd, *exit         ║
╚═══════════════════════════════════════════════════════════╝
```

### Step 1.2: Create PRD

```
*create-prd
```

The agent will guide you with questions:
- Product name
- Brief description
- Target users
- Problem it solves
- Main features

### Step 1.3: Review the generated PRD

```
*review-prd
```

### Step 1.4: Exit the agent

```
*exit
```

**Generated file:** `docs/prd.md`

---

## Phase 2: Design Architecture (5 min)

### Step 2.1: Load the Architect agent

```
/architect
```

### Step 2.2: Design architecture

```
*create-full-stack-architecture
```

The agent will analyze the PRD and propose:
- System components
- Architecture patterns
- Technical decisions (ADRs)

### Step 2.3: Exit

```
*exit
```

**Generated file:** `docs/architecture.md`

---

## Phase 3: Shard Documents (MANDATORY)

### Step 3.1: Load the PO agent

```
/po
```

### Step 3.2: Shard the PRD

```
*shard-doc docs/prd.md prd
```

This creates individual files per feature in `docs/prd/`.

### Step 3.3: Shard the Architecture

```
*shard-doc docs/architecture.md architecture
```

### Step 3.4: Exit

```
*exit
```

> **IMPORTANT:** This step is mandatory. Without sharding, the `/dev` agent will not have the necessary context.

---

## Phase 4: Create User Story (5 min)

### Step 4.1: Load the SM agent

```
/sm
```

### Step 4.2: Create a story

```
*draft
```

The agent will ask you:
- Which epic it belongs to
- Story title
- Description
- Acceptance criteria

### Step 4.3: View the created story

```
*list
```

### Step 4.4: Exit

```
*exit
```

**Generated file:** `docs/stories/EPIC-001/STORY-001.md`

---

## Phase 5: Develop (10 min)

### Step 5.1: Load the Dev agent

```
/dev
```

### Step 5.2: Develop the story

```
*develop-story docs/stories/EPIC-001/STORY-001.md
```

The agent will:
1. Read the story and its criteria
2. Analyze the sharded PRD and architecture
3. Implement the code
4. Create unit tests
5. Mark completed tasks in the story

### Step 5.3: Verify the implementation

Review the created/modified files.

### Step 5.4: Exit

```
*exit
```

---

## Phase 6: Quality Gate (5 min)

### Step 6.1: Load the QA agent

```
/qa
```

### Step 6.2: Review the story

```
*review docs/stories/EPIC-001/STORY-001.md
```

The agent will verify:
- Acceptance criteria met
- Tests exist and pass
- Code coverage
- Code quality

### Step 6.3: Create Quality Gate

```
*gate
```

Possible results:
- **PASS** - Ready to commit
- **CONCERNS** - Approved with observations
- **FAIL** - Requires corrections
- **WAIVED** - Approved with documented exceptions

### Step 6.4: Exit

```
*exit
```

**Generated file:** `docs/qa/gates/EPIC-001.STORY-001-{slug}.yml`

---

## Phase 7: Commit

### Only if QA = PASS or WAIVED

```bash
# View changes
git status

# Add files
git add .

# Commit with a descriptive message
git commit -m "feat(STORY-001): implement user authentication

- Add login endpoint
- Add JWT token generation
- Add user validation

QA Gate: PASS"
```

---

## Flow Summary

```
/pm *create-prd → /architect *create-full-stack-architecture → /po *shard-doc
                                              ↓
                                        /sm *draft
                                              ↓
                                     /dev *develop-story
                                              ↓
                                      /qa *review → *gate
                                              ↓
                                    git commit (if PASS)
```

---

## Final Verification

- [ ] `docs/prd.md` exists and is complete
- [ ] `docs/architecture.md` exists
- [ ] `docs/prd/` and `docs/architecture/` have sharded files
- [ ] `docs/stories/EPIC-001/STORY-001.md` exists
- [ ] Code implemented in `src/`
- [ ] Tests in `tests/`
- [ ] `docs/qa/gates/` has the quality gate
- [ ] Commit made with a descriptive message

---

## Tips

1. **One agent per conversation:** Start a new conversation when switching agents
2. **Automatic context:** `*load-context` runs when the agent loads
3. **Always use `*exit`:** Saves context for the next session
4. **QA before commit:** Never commit without QA PASS

---

## Next Step

For deeper documentation on workflows and agents, see:
- [Development Workflow](../../DEVELOPMENT-WORKFLOW.md) — Full agent sequence and plan system
- [Documentation Index](../../INDEX.md) — Navigation hub for all JVIS docs
