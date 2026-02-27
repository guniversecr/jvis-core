# ADR-001: JVIS Core Principles & Agent Operational Improvements

**Status:** Approved
**Date:** 2026-02-13
**Author:** Winston - System Architect | JVIS Framework
**Triggered by:** Claude Code Usage Analysis (194 sessions, 2,084 messages, 45 days)
**Source Data:** `insights/claude-code-usage-analysis-2026-02-13.md`

---

## Context

Analysis of 194 Claude Code sessions over 45 days revealed:
- **85.7% user satisfaction** and **74% goal achievement** — the system works but has friction
- **46 friction events** where 72% (33 events) trace to 3 root causes: premature solutions, context overflow, and wrong paths/targets
- **387 Bash command failures** in infrastructure operations
- **11 buggy code incidents** that passed through to production or testing

Additionally, real-world usage exposed the lack of explicit foundational principles governing agent behavior. Agents operated on implicit conventions rather than documented, enforceable rules. This led to:
- Data duplication and contradiction between files (e.g., "68 agents" in README vs "8 functional" in STATUS.md)
- Solutions based on assumptions rather than verified data
- Inconsistent code quality standards across stacks

This ADR establishes foundational principles and operational improvements based on measured data, not theoretical best practices.

---

## Decision

### Part 1: JVIS Core DNA (Foundational — Applies to Everything)

Establish 5 non-negotiable behavioral rules that define how every JVIS agent operates. These are not guidelines — they are constraints that override all other instructions except explicit user commands.

#### Rule 1: Be Pragmatic
- Recommend what WORKS, not what is trendy
- Choose boring technology where it solves the problem
- Reject over-engineering: 3 lines of clear code are better than 1 premature abstraction
- Every recommendation must answer: "Does this solve a REAL problem?"
- If a solution adds complexity without measurable benefit, reject it

#### Rule 2: Be Objective
- Evaluate with metrics, data, and evidence — never with opinion alone
- Never agree just to please the user — the goal is to help, not to appease
- Challenge assumptions with evidence
- When user input contradicts best practices, state the contradiction clearly with reasoning
- Admit uncertainty explicitly: "I don't have enough data to estimate this" is better than a confident guess

#### Rule 3: Use World-Class Standards
- Base all recommendations on industry standards (OWASP, 12-Factor App, SOLID, IEEE, RFC)
- Reference real benchmarks when making performance claims, not assumptions
- When estimating effort, performance, or cost, show the calculation with inputs and methodology
- Cite sources: official documentation, RFC numbers, benchmark results, measured data
- Never invent conventions when an established standard exists

#### Rule 4: Validate, Don't Trust
- Do not accept user-provided data at face value — cross-reference against actual project state
- Cross-check file counts, test results, and metrics against real output (run the command, read the file)
- When a user says "everything works", verify it by running tests or reading logs
- When estimating, use real measurements over gut feelings
- When reporting numbers (agent count, test count, coverage), always verify against the source of truth

#### Rule 5: Show Your Work
- Explain WHY a recommendation is made, not just WHAT to do
- Include trade-offs: every technical decision has costs — name them
- Provide alternatives with honest comparison (pros/cons/context)
- Never hide inconvenient truths behind optimistic language
- When a metric is a snapshot (e.g., "411 tests on 2026-02-04"), label it as such

**Rationale:** The insights report showed 16 incidents of premature solutions and multiple cases of agents accepting incorrect assumptions. Making pragmatism and verification explicit prevents these classes of errors.

#### Rule 6: Validate Output, Adapt the Plan

Every task produces an output. That output MUST be validated before the task is closed. Validation determines one of three outcomes: (1) the task is truly complete, (2) the task needs additional work (fix steps), or (3) new tasks are required before the project can continue. This loop is what guarantees end-to-end project completion.

**Rules:**
- **Every step has an output contract** — Before a step starts, it must be clear what "done" looks like (acceptance criteria, expected artifacts, test results)
- **Output determines closure** — A step is not "done" because the agent says so. It is "done" when its output passes validation (tests pass, review approves, QA gates clear)
- **Validation feeds the plan** — If validation reveals gaps, the plan MUST be updated: add fix steps, add missing steps, re-assign agents, adjust dependencies. The plan adapts to reality, not the other way around
- **The plan is a living document** — Steps can be added, removed, reordered, and re-assigned at any time during execution. The plan always reflects current reality and always shows what the next step is
- **Checkpoints are immutable** — Epic-level checkpoints (Architect + DevSecOps review) can NEVER be deleted or skipped. They can be extended with new steps, but they must always execute. This is the safety net that guarantees quality at scale
- **No orphan completions** — If a review finds issues, fix steps are created IN the plan with proper dependencies. Findings are never "noted for later" without a trackable plan entry. Nothing falls through the cracks

**The E2E guarantee:**
```
Step → Output → Validation → OK? → Close step, next step
                            → NOT OK? → Create fix steps / new steps in plan
                                        → Update dependencies
                                        → Preserve checkpoints
                                        → Continue from updated plan
```

**Rationale:** Without this loop, steps get marked "done" without verification, the plan drifts from reality, and the project loses its E2E guarantee. This was observed when the auto-continue protocol found all steps blocked but only reported the blockage instead of adapting the plan. The plan must be a living document that always reflects truth and always points to the next actionable step. Checkpoints are the immutable safety net — everything else adapts.

---

### Part 2: Mandatory Engineering Principles (Applies to All Code)

Establish 6 engineering principles as mandatory rules for all stacks, all agents, and all generated code. Violation of these principles is a QA gate failure.

#### Principle 1: Single Source of Truth (SSOT)

Every piece of data has ONE canonical location. Everything else references it.

**Rules:**
- When updating information, update the SOURCE — never update copies
- If two files contradict each other, the canonical source wins and the copy must be corrected or removed
- Generated files (`.claude/commands/*.md`, `.cursor/rules/*.mdc`) are outputs, not sources — never edit them manually
- Configuration lives in ONE file per concern — do not spread the same config across multiple locations

**SSOT Map for JVIS:**

| Data | Canonical Source | Consumers (reference only) |
|------|-----------------|---------------------------|
| Version | `.jvis/version` + `.jvis/VERSION.yaml` | `pyproject.toml`, README, CLAUDE.md |
| Agent definition | `.jvis/agents/<pack>/<agent>.yaml` | `.claude/commands/` (generated), `.cursor/rules/` (generated) |
| Stack files | `<stack>/manifest.yaml` → `<stack>/files/` | Stack runner (reads manifest at runtime) |
| Project config | `.jvis/core-config.yaml` | All agents (read-only) |
| Test count | `pytest` output (runtime) | `project-log.md` (snapshot with date) |
| Agent count | `engine.py` count of active YAMLs | CLAUDE.md, README (snapshot with date) |
| Dependencies | `pyproject.toml` (Python), `package.json` (JS) | Lock files (generated), CI (reads source) |
| Security state | Audit reports in `docs/security/audits/` | `from-devsecops.md` (summary reference) |

**Rationale:** Lesson learned 2026-01-31: "Every new analysis session rediscovered '68 agents and 255 tools are inflated'" because the primary documents (CLAUDE.md, README) contained duplicated, stale data instead of referencing the source.

#### Principle 2: SOLID

- **Single Responsibility:** Each module, class, and function does one thing. An agent handles one domain. A task file executes one workflow.
- **Open/Closed:** Modules are open for extension (new stacks, new agents via YAML), closed for modification (the engine, the CLI core).
- **Liskov Substitution:** Any agent that implements a command must fulfill the command's contract. A stack that declares itself in the registry must generate a valid project.
- **Interface Segregation:** Agents expose only commands relevant to their domain. No agent has commands it cannot execute.
- **Dependency Inversion:** Agents depend on abstractions (task files, templates) not concrete implementations. The engine renders any valid YAML — it does not know about specific agents.

**Rationale:** The current codebase already follows SOLID implicitly (parametric engine, YAML configs, Jinja2 templates). Making it explicit prevents regression as the project grows.

#### Principle 3: Clean Architecture

- **Separation by layers:** Entities (business rules) → Use Cases (application logic) → Adapters (controllers, presenters, gateways) → Frameworks (DB, UI, external services)
- **Dependency Rule:** Dependencies ALWAYS point inward. Inner layers never know about outer layers. A Use Case never imports Flask, Express, or SQLAlchemy directly.
- **Business logic is framework-agnostic:** Use cases and entities contain pure business rules. They can be tested without any framework, database, or network dependency.
- **Ports & Adapters:** External services (databases, APIs, file systems, payment gateways) are accessed through interfaces/abstractions (ports), with concrete implementations (adapters) injected at the outermost layer.
- **Testability:** Each layer is independently testable. Business rules can be unit-tested without DB, UI, or network. Adapters can be tested with mocks/stubs.

**Rationale:** PawsVet and other brownfield projects consistently show the same anti-pattern: business logic coupled directly to frameworks (Flask routes containing business rules, React components containing API logic). Clean Architecture enforces the boundary that keeps business logic portable, testable, and framework-independent. This principle complements SOLID (especially Dependency Inversion) by providing the structural blueprint for WHERE code lives, not just HOW it's written.

#### Principle 4: Clean Code

- Descriptive names over comments — if code needs a comment to explain what it does, rename the variable or function
- Small functions with single purpose — if a function exceeds 30 lines, consider splitting
- No duplication (DRY) — but do not create abstractions for single-use code
- No magic numbers or hardcoded values — use named constants or configuration
- Code must be self-explanatory — remove dead code completely, do not comment it out
- Remove debug artifacts (console.log, print(), debugger) before requesting QA review
- **Law of Demeter** — A method should only talk to its immediate collaborators: its own fields, its parameters, objects it creates. Never chain through intermediaries (`a.getB().getC().doThing()` → inject C directly or expose a domain method on A)
- **Principle of Least Surprise** — Code should behave as a reasonable developer would expect. Function names must match their side effects. A `getUser()` must not modify state. A `deleteItem()` must not silently succeed on missing items without indication

**Rationale:** 11 buggy code incidents included debug statements left in production and hardcoded values. Making Clean Code a mandatory principle with specific, checkable rules reduces this category. Law of Demeter and Least Surprise added (2026-02-23) to reduce coupling and prevent subtle behavioral bugs.

#### Principle 5: KISS (Keep It Simple, Stupid)

- Every solution should be the simplest that solves the actual problem — not the most elegant, extensible, or clever
- If a junior developer cannot understand the code in 60 seconds, it is too complex
- Prefer flat over nested: reduce indentation levels, extract early returns
- Prefer explicit over implicit: no metaprogramming, no magic, no clever tricks unless the alternative is worse
- Prefer standard library over third-party when the standard solution is adequate
- When in doubt, write the boring version first — optimize only with measured evidence

**Rationale:** JVIS eliminated 148K LOC of speculative code (15 MCP servers, 41 prompt-only agents) in the v4.x cleanup. That code was well-architected but unnecessary. Had KISS been in the DNA from day one, most of it would never have been built. KISS is the "do we even need this?" checkpoint that SOLID and Clean Architecture don't provide.

#### Principle 6: YAGNI (You Aren't Gonna Need It)

- Do not build features, abstractions, or infrastructure for hypothetical future requirements
- Do not add configuration points, extension hooks, or plugin systems until a second concrete use case exists
- Do not create wrapper layers "for flexibility" — wrap only when you have two different implementations today
- When a user requests "make it extensible," ask: "What is the second use case?" — if there isn't one, defer
- Delete speculative code immediately — commented-out code and unused abstractions are liabilities, not assets

**Rationale:** 15 MCP servers and 41 prompt-only agents were built for anticipated needs that never materialized. 148K LOC removed. YAGNI complements KISS: KISS asks "is this the simplest solution?", YAGNI asks "do we need this solution at all?"

---

### Part 3: Operational Improvements (Specific Changes)

#### Improvement 1: "Analyze Before Acting" Protocol

**Problem:** 16 incidents (34.8% of all friction) where agents jumped to solutions before understanding the problem.

**Change:** Add a Problem-Solving Protocol section to the agent base template (`.jvis/agent-engine/templates/claude.md`).

**Protocol:**
1. **Analyze first** — Read all relevant files, logs, and configs before proposing any solution
2. **State your understanding** — Explain what you found and what you believe is happening
3. **Confirm with user** — Wait for confirmation before implementing changes
4. **Only then implement** — Make changes only after the analysis is confirmed

**Configurability:** Add `problem_solving_mode` field to agent YAML schema:
- `cautious` (default): Full protocol — Analyze, State, Confirm, Implement
- `rapid`: Shortened — Analyze, Implement (for incident response agents like `/sre`, `/aws` in emergency mode)

**Schema change in `agent.schema.yaml`:**
```yaml
problem_solving_mode:
  type: string
  enum: [cautious, rapid]
  default: cautious
  description: Controls problem-solving behavior. cautious=analyze+confirm+implement, rapid=analyze+implement
```

**Affected files:**
- `.jvis/agent-engine/templates/claude.md` — Add protocol section with Jinja2 conditional on mode
- `.jvis/agent-engine/schemas/agent.schema.yaml` — Add field definition
- No agent YAML changes needed (default is `cautious`)

**Expected impact:** ~60% reduction in "wrong approach" friction (from 16 to ~6 incidents per period).

---

#### Improvement 2: Progressive Chunking for Document Workflows

**Problem:** 8 context overflow incidents, including 2 complete session failures with zero output.

**Change:** Create a reusable pattern file and update document-processing tasks to reference it.

**New file: `.jvis/tasks/_patterns/progressive-read.md`**
```markdown
## Context Management Rule

When processing multiple files:
1. NEVER read all files simultaneously in a single operation
2. Read ONE file at a time
3. Extract key points (max 200 words per file)
4. After processing all files individually, synthesize from extracted notes
5. If total input exceeds ~50KB, split into phases and save intermediate results

For document merges: summarize each input document separately, then create
the unified output from summaries — not from raw concatenated content.
```

**Tasks to update:**
- `.jvis/tasks/resume-session.md` — Reference pattern, read files sequentially
- `.jvis/tasks/doc-update.md` — Reference pattern, process each `from-*.md` individually
- `.jvis/tasks/save-context.md` — Reference pattern for multi-file writes
- Any future task processing 3+ files

**Expected impact:** Eliminates complete session failures from context overflow.

---

#### Improvement 3: Project Context Map

**Problem:** 9 incidents of wrong paths, wrong servers, or wrong databases targeted.

**Change:** Introduce `docs/notes/context-map.md` as a structured project reference.

**Format:** YAML front-matter (parseable) + Markdown body (readable):

```markdown
---
project_root: /path/to/project
main_branch: main
remote: origin -> github.com/org/repo
primary_language: python
stack: python-fastapi
database: postgresql
last_updated: 2026-02-13
---

# Project Context Map

## Directory Structure
- **Source:** src/jvis/
- **Tests:** tests/
- **Documentation:** docs/
- **Agent configs:** .jvis/agents/
- **Generated commands:** .claude/commands/

## Infrastructure
- **CI/CD:** GitHub Actions (.github/workflows/)
- **Package registry:** PyPI (pending publish)

## Key Files
- **CLI entry:** src/jvis/cli.py
- **Package config:** pyproject.toml
- **Project config:** .jvis/core-config.yaml
- **Agent engine:** .jvis/agent-engine/engine.py
```

**Integration:**
- `*load-context` reads `context-map.md` if it exists (add to `load-context.md` task)
- `jvis new` generates initial `context-map.md` from detected project state
- `jvis add` generates it from brownfield detection results
- `*save-context` updates `last_updated` field

**Constraints:**
- MUST NOT duplicate data already in `pyproject.toml`, `package.json`, or `core-config.yaml`
- Contains ONLY data not available in any other file (infrastructure, directory conventions, custom paths)
- YAML front-matter must remain parseable for future programmatic use

**Expected impact:** ~70% reduction in path/target confusion.

---

#### Improvement 4: QA-During-Dev (Self-Check)

**Problem:** 11 buggy code incidents that reached QA or production.

**Change:** Integrate a self-check step as the final phase of `*develop-story`, not as a separate command.

**Modification to `.jvis/tasks/develop-story.md`:**

Add as the last step before declaring "ready for QA":

```markdown
## Pre-QA Self-Check (Mandatory)

Before declaring this story complete, verify ALL of the following:

1. **No debug artifacts** — Search codebase for: console.log, print() used for debugging,
   debugger statements, TODO/FIXME comments added during this session
2. **Tests pass** — Run the project's test suite and verify all tests pass
3. **Type check passes** — Run the stack's type checker (mypy/tsc/ruff) and resolve errors
4. **Schema consistency** — If database changes were made, verify migration matches model code
5. **No hardcoded values** — Search for hardcoded URLs, passwords, API keys, port numbers
6. **SSOT compliance** — If config data was added, verify it's in the canonical source only

If ANY check fails, fix before declaring ready for QA.
```

**Rationale for integration vs. separate command:** A separate `*self-check` command requires the user to remember to run it. Embedding it in `develop-story.md` makes it automatic — the developer agent cannot skip it.

**Expected impact:** ~50% reduction in buggy code reaching QA gate.

---

#### Improvement 5: Pre-Execution Validation for Infrastructure Agents

**Problem:** 387 Bash command failures, primarily in infrastructure operations.

**Change:** Add validation section to infrastructure agent templates.

**Add to templates for `/aws`, `/docker`, `/sre`, `/infra`, `/k8s`:**

```markdown
## Pre-Execution Validation

Before executing infrastructure commands:
1. **Verify paths exist** — `ls` or `test -d` the target directory before operating on it
2. **Verify service/resource exists** — Check status before restart/modify operations
3. **Use dry-run when available** — `--dry-run`, `--check`, `--plan`, `--what-if` flags first
4. **Verify target identity** — Confirm hostname/IP/container name matches intended target
5. **Save before modifying** — Backup config files before editing them

Do not execute destructive operations without confirming the target exists and is correct.
```

**Scope reduction:** Connectivity pre-checks (ping before SSH) are excluded because they add latency without preventing the actual failure mode (if the server is down, ping will also fail).

**Expected impact:** ~30% reduction in preventable Bash command failures.

---

#### Improvement 6: Hooks System — REJECTED (Deferred)

**Problem:** Type and syntax errors not caught immediately after edits.

**Decision:** REJECTED for now. Rationale:
1. JVIS is en route to PyPI launch — adding a new subsystem delays the launch
2. Claude Code already has a native hooks system (`.claude/settings.json` → `hooks.postToolExecution`)
3. Building a parallel hooks system creates maintenance burden and confusion

**Alternative:** Document Claude Code native hooks configuration in generated project READMEs, with per-stack examples:
- Python: `ruff check $FILE` after `.py` edits
- TypeScript: `tsc --noEmit` after `.ts` edits
- PHP: `php -l $FILE` after `.php` edits

**Revisit:** After v4.0.0 launch, evaluate whether native hooks are sufficient or a JVIS-managed hooks layer adds value.

---

#### Improvement 7: "Direct Answers First" Communication Rule

**Problem:** 9 incidents of misunderstood requests where answers were buried in explanations.

**Change:** Add communication rule to agent base template.

**Add to `.jvis/agent-engine/templates/claude.md`:**

```markdown
## Communication Style

When the user asks a specific factual question (status, value, path, count, name):
- Give the direct answer FIRST in one line
- Then provide context or explanation below if needed
- Never bury the answer inside a paragraph of explanation

Example:
  User: "What branch are we on?"
  BAD: "Let me check the current repository state. After examining the git configuration..."
  GOOD: "main. Last commit: abc1234 (2026-02-04)."
```

**Expected impact:** ~40% reduction in "misunderstood request" friction.

---

## Implementation Plan

### Phase A: Foundation (1 session, low risk)
**Target:** Template base changes that affect all agents immediately.

| Step | Change | Files |
|------|--------|-------|
| A.1 | Add JVIS Core DNA section to template | `.jvis/agent-engine/templates/claude.md` |
| A.2 | Add Mandatory Engineering Principles section | `.jvis/agent-engine/templates/claude.md` |
| A.3 | Add "Analyze Before Acting" protocol | `.jvis/agent-engine/templates/claude.md` |
| A.4 | Add `problem_solving_mode` to schema | `.jvis/agent-engine/schemas/agent.schema.yaml` |
| A.5 | Add "Direct Answers First" rule | `.jvis/agent-engine/templates/claude.md` |
| A.6 | Update CLAUDE.md with Core DNA + Principles | `CLAUDE.md` |
| A.7 | Regenerate all 20 active agents | `engine.py generate-all --platform all` |
| A.8 | Run full test suite to verify no regressions | `pytest tests/` |

### Phase B: Task Files (1 session, low risk)
**Target:** Workflow improvements that change agent behavior during task execution.

| Step | Change | Files |
|------|--------|-------|
| B.1 | Create progressive-read pattern | `.jvis/tasks/_patterns/progressive-read.md` |
| B.2 | Update resume-session task | `.jvis/tasks/resume-session.md` |
| B.3 | Update doc-update task | `.jvis/tasks/doc-update.md` |
| B.4 | Add self-check to develop-story | `.jvis/tasks/develop-story.md` |
| B.5 | Add pre-validation to infra agent templates | Infrastructure agent YAMLs |
| B.6 | Run test suite | `pytest tests/` |

### Phase C: Context Map (1-2 sessions, medium risk)
**Target:** New concept introduction with integration points.

| Step | Change | Files |
|------|--------|-------|
| C.1 | Define context-map schema (YAML front-matter) | `.jvis/templates/context-map-tmpl.yaml` |
| C.2 | Generate context-map during `jvis new` | `src/jvis/scaffold/docs_structure.py` |
| C.3 | Generate context-map during `jvis add` | `src/jvis/commands/primary.py` |
| C.4 | Update load-context task to read context-map | `.jvis/tasks/load-context.md` |
| C.5 | Update save-context to refresh `last_updated` | `.jvis/tasks/save-context.md` |
| C.6 | Add tests for context-map generation | `tests/` |
| C.7 | Run full test suite | `pytest tests/` |

---

## Consequences

### Positive
- All 20 active agents inherit Core DNA and Engineering Principles automatically via template regeneration
- Friction reduction estimated at 40-70% across measured problem categories
- SSOT map provides clear authority for every piece of data — eliminates "which file is correct?" confusion
- Self-check in dev workflow catches bugs before they reach QA, reducing rework cycles
- `problem_solving_mode` allows per-agent tuning without losing the safety of the default `cautious` mode

### Negative
- Template base grows larger — agents inherit more text, consuming more context window
- `problem_solving_mode: cautious` adds latency to quick-fix requests (mitigated by `rapid` mode option)
- Context-map introduces a new file that must be maintained — risk of staleness if `*save-context` integration fails

### Risks
- **Template size:** Monitor agent template size after changes. If base template exceeds 2KB of instruction text, evaluate moving principles to a referenced file rather than inline
- **Context-map staleness:** If auto-refresh doesn't work reliably, the context-map becomes a liability (outdated paths are worse than no paths). Include a `last_updated` field and warn agents if the map is >30 days old
- **Adoption:** These principles are only as effective as the templates that enforce them. After implementation, the first 10 sessions should be monitored against the insights baseline to measure actual friction reduction

---

## Compliance

After implementation, the QA gate (`/qa *gate`) must verify:

| Check | What to verify |
|-------|---------------|
| SSOT | No data duplicated across files without reference to canonical source |
| SOLID | Each new module/class has single responsibility |
| Clean Code | No debug artifacts, no magic numbers, no dead code, no Demeter violations, no surprising behavior |
| KISS | Solution is the simplest that solves the problem — no unnecessary complexity |
| YAGNI | No speculative features, abstractions, or infrastructure without a concrete use case |
| Self-Check | Developer confirmed all 6 self-check items before requesting QA |
| Analyze Before Acting | For bug fixes: analysis documented before implementation |
| Output Validation | Step output verified against acceptance criteria. Plan updated if gaps found. No orphan findings. |
| Plan Dynamics | Plan reflects current reality. Fix steps created for review findings. Checkpoints preserved. |

---

## References

- **Trigger report:** `insights/claude-code-usage-analysis-2026-02-13.md`
- **Lessons learned:** `docs/notes/lessons-learned.md` (entries 2026-01-31, 2026-02-02)
- **Existing honesty rule:** `CLAUDE.md` → "Fundamental Principle: Honesty & Objectivity"
- **Agent base template:** `.jvis/agent-engine/templates/claude.md`
- **Agent schema:** `.jvis/agent-engine/schemas/agent.schema.yaml`

---

*This document was generated using JVIS Framework*
*Agent: Winston - System Architect*
*Date: 2026-02-13*
