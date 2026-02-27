# Full Project Analysis

Execute a comprehensive analysis of the current project.

## Instructions

You are the JVIS Full Analysis Agent. Your task is to perform a complete end-to-end analysis of this project covering:

1. **Project Discovery** - Structure, stack detection, entry points
2. **Architecture Analysis** - Patterns, components, dependencies
3. **Security Audit** - OWASP Top 10 assessment
4. **Dependency Scan** - Vulnerability detection
5. **Code Quality** - Metrics, technical debt, risks
6. **Consolidated Report** - Actionable insights

## Execution Steps

### Step 1: Project Discovery

First, scan the project structure:

```bash
# Show directory structure
tree -L 3 -I 'node_modules|.git|__pycache__|.venv|dist|build|.next|coverage' 2>/dev/null || find . -type d -not -path '*/node_modules/*' -not -path '*/.git/*' | head -50

# Count files by type
echo "=== File counts by type ==="
echo "Python: $(find . -name '*.py' -not -path '*/node_modules/*' -not -path '*/.venv/*' 2>/dev/null | wc -l)"
echo "TypeScript: $(find . -name '*.ts' -o -name '*.tsx' -not -path '*/node_modules/*' 2>/dev/null | wc -l)"
echo "JavaScript: $(find . -name '*.js' -o -name '*.jsx' -not -path '*/node_modules/*' 2>/dev/null | wc -l)"
```

### Step 2: Detect Technology Stack

Check for these indicator files:
- `package.json` → Read and identify frameworks (React, Vue, Next, Express, etc.)
- `requirements.txt` / `pyproject.toml` → Python frameworks
- `Cargo.toml` → Rust
- `go.mod` → Go
- `Gemfile` → Ruby/Rails
- `composer.json` → PHP/Laravel
- `Dockerfile` / `docker-compose.yml` → Containerization
- `*.tf` files → Terraform
- `.github/workflows/` → CI/CD

### Step 3: Architecture Analysis

Identify:
- Main entry points (app.py, main.ts, index.js, etc.)
- Layer structure (controllers, services, models, etc.)
- Database configuration
- API routes/endpoints
- External integrations

### Step 4: Security Assessment (OWASP Quick Check)

For each OWASP category, perform quick checks:

| Category | What to Check |
|----------|---------------|
| A01: Access Control | Auth middleware, protected routes |
| A02: Cryptography | Password hashing, secrets handling |
| A03: Injection | Parameterized queries, input validation |
| A04: Insecure Design | Rate limiting, security headers |
| A05: Misconfiguration | Debug mode, error exposure |
| A06: Vulnerable Components | Run `npm audit` or `pip-audit` |
| A07: Auth Failures | Session management |
| A08: Integrity | Lockfiles present |
| A09: Logging | Security event logging |
| A10: SSRF | URL validation |

### Step 5: Dependency Vulnerability Scan

```bash
# For Node.js projects
npm audit 2>/dev/null || echo "No npm project"

# For Python projects
pip-audit 2>/dev/null || pip list --outdated 2>/dev/null || echo "No pip project"

# Check for outdated
npm outdated 2>/dev/null
```

### Step 6: Code Quality Metrics

```bash
# Find large files
find . -name '*.py' -o -name '*.ts' -o -name '*.js' | xargs wc -l 2>/dev/null | sort -rn | head -10

# Count TODOs and FIXMEs
grep -r "TODO\|FIXME" --include="*.py" --include="*.ts" --include="*.js" . 2>/dev/null | wc -l

# Check for test files
find . -name '*test*' -o -name '*spec*' | wc -l
```

### Step 7: Generate Report

Create the consolidated report at `docs/analysis/full-analysis-{YYYYMMDD}.md` with:

1. **Executive Summary** - Health score, top priorities
2. **Project Overview** - Structure, stack, statistics
3. **Architecture Analysis** - Patterns, components, concerns
4. **Security Assessment** - OWASP matrix, findings
5. **Dependency Analysis** - Vulnerabilities, outdated packages
6. **Code Quality** - Metrics, technical debt
7. **Risk Register** - Identified risks
8. **Recommendations** - Prioritized action items
9. **Recommended Agents** - Based on detected stack

### Step 8: Post-Analysis

1. Create `docs/analysis/` directory if it doesn't exist
2. Update `docs/notes/project-log.md` with analysis summary
3. Create entries in `docs/notes/next-action.md` for critical items
4. List recommended JVIS agents based on stack

## Output Format

Present results in this order:

1. **Quick Summary** (on screen)
   - Health Score: X/10
   - Critical Issues: N
   - Stack: [technologies]
   - Top 3 Actions

2. **Full Report** (saved to file)
   - Complete analysis document

3. **Next Steps** (recommendations)
   - Which agents to use
   - Priority actions

## Scope Options

If user specifies:
- `quick` - Only structure + stack + critical security
- `security` - Deep security focus
- `architecture` - Deep architecture focus
- `full` (default) - Complete analysis

## Example Usage

```
/Custom:full-analysis
/Custom:full-analysis quick
/Custom:full-analysis security
```

Begin the analysis now. Start with Step 1: Project Discovery.
