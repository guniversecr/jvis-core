# Stack Development Skill

Knowledge for creating and modifying JVIS technology stack scaffolds.

## Stack Architecture

JVIS stacks are **data-driven** — each stack is a YAML manifest + Jinja2 templates directory under `src/jvis/data/stacks/`. Zero Python code per stack.

### Manifest Format (`manifest.yaml`)

```yaml
id: stack-id              # Lowercase, hyphenated
name: "Display Name"
description: "One-line description"
type: backend|frontend|fullstack
language: python|typescript|php|rust
framework: fastapi|express|vite|etc
requires_database: true|false
agents: [dev, qa, architect, ...]

directories:              # Created as empty dirs
  - src
  - src/domain
  - tests

files:                    # Template → output mapping
  - {src: "package.json.j2", dst: "package.json"}
  - {src: "src/app.ts", dst: "src/app.ts"}  # No .j2 = copied verbatim
```

### Template Conventions

- Files with `{{ }}` or `{% %}` Jinja2 syntax **MUST** have `.j2` extension
- Files without template variables are copied verbatim (no `.j2`)
- Template variables: `{{ project_name }}`, `{{ database_type }}`, `{{ database_driver }}`
- `manifest.yaml` `dst` field controls the output filename

### Jinja2/JSX Conflict (CRITICAL)

JSX uses `{{ }}` for inline styles: `style={{ color: 'red' }}`. This conflicts with Jinja2 expression syntax.

**Resolution:** Use CSS classes instead of inline styles in `.j2` template files. Reserve `.j2` extension ONLY for files needing actual Jinja2 template variables like `{{ project_name }}`.

See: `docs/notes/lessons-learned.md` — "Jinja2 Template File Naming Convention"

### File Generation Flow

1. `src/jvis/scaffold/stack_runner.py` reads `manifest.yaml`
2. Creates directories from `directories` list
3. For each file in `files`:
   - `.j2` extension → render through Jinja2 with project context
   - No `.j2` → copy verbatim from `files/` directory
4. Output stripped of `.j2` extension per `dst` field

### Functional Stacks (3 of 17)

Three stacks generate working CRUD scaffolds with Clean Architecture:

| Stack | Entity | Architecture | Tests |
|-------|--------|-------------|-------|
| `python-fastapi` | Item (SQLAlchemy) | Domain → Use Cases → Infrastructure → Controllers | pytest + SQLite in-memory |
| `nodejs-express` | Item (Prisma) | Domain → Application → Infrastructure → Presentation | vitest + supertest |
| `react-vite` | Item (Axios client) | Types → Services → Hooks → Pages → Components | vitest + jsdom |

### Testing Scaffolds

Every new stack template should have a corresponding test in `tests/unit/test_scaffold.py`:
- Verify `run_stack()` generates all files without errors
- Verify no Jinja2 artifacts (`{{`, `{%`) in generated output
- Verify expected file structure matches manifest

See: `docs/adr/ADR-002-functional-stack-scaffolding.md`, `docs/adr/ADR-003-functional-scaffolds-nodejs-react.md`
