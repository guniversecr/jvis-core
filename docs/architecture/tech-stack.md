# Tech Stack

Technology selection document for the project.

---

## Selected Stack

> Update this section with the technologies chosen for your project.

### Frontend
- **Framework:** [React + Vite / React Native + Expo / None]
- **Language:** TypeScript (strict mode)
- **Styling:** [Tailwind / CSS Modules / Styled Components]
- **State Management:** [Zustand / Redux / Context API]

### Backend
- **Framework:** [FastAPI / Flask / Express]
- **Language:** [Python 3.13+ / TypeScript]
- **ORM:** [SQLAlchemy / Prisma]
- **Cache:** [Redis / In-memory]

### Database
- **Primary:** [PostgreSQL / MySQL / MongoDB]
- **Migrations:** [Alembic / Prisma Migrate / Flask-Migrate]

### Infrastructure
- **Hosting:** [AWS / Azure / SSH (OVH/Contabo)]
- **IaC:** Terraform
- **CI/CD:** [GitHub Actions / GitLab CI / Manual]

---

## Decision Justification

### Why [chosen Framework]?
[Explain the reason for the choice]

### Why [chosen Database]?
[Explain the reason for the choice]

### Why [chosen Cloud provider]?
[Explain the reason for the choice]

---

## Available Stacks Reference

### Python Backend

| Stack | Use Case | Includes |
|-------|----------|----------|
| **FastAPI** | Async APIs, microservices | SQLAlchemy async, Pydantic, Clean Arch |
| **Flask** | Traditional APIs, MVPs | SQLAlchemy, Flask-Migrate, Redis |

### JavaScript/TypeScript Backend

| Stack | Use Case | Includes |
|-------|----------|----------|
| **Express** | Fast APIs, full-stack | TypeScript, Prisma, Jest |

### Frontend

| Stack | Use Case | Includes |
|-------|----------|----------|
| **React + Vite** | SPAs, dashboards | TypeScript strict, Vitest, ESLint |
| **React Native + Expo** | Mobile apps | TypeScript, Jest, EAS Build |

---

## Standard Tooling (all stacks)

### Code Quality
| Language | Formatting | Linting | Types | Tests |
|----------|------------|---------|-------|-------|
| Python | Black | Ruff | MyPy | Pytest |
| TypeScript | Prettier | ESLint | TSC | Vitest/Jest |

### Automation
- **Pre-commit:** Automatic hooks on every commit
- **EditorConfig:** Consistency across editors
- **GitHub Templates:** Structured issues and PRs

### Documentation
- SECURITY.md
- CHANGELOG.md
- CONTRIBUTING.md
- .env.example

---

## Technical Constraints

### Package Managers
- **JavaScript:** Yarn (not npm)
- **Python:** pip + venv

### NOT Recommended Frameworks
- Create React App (CRA) - deprecated, use Vite
- npm - use Yarn

### Infrastructure
- Docker is **optional**, not required by default
- Terraform for multi-cloud IaC

---

## Resources

- Technical preferences: `.jvis/data/technical-preferences.md`
- Coding standards: `docs/architecture/coding-standards.md`
- Excellence principles: `.jvis/data/excellence-principles.md` (APEX6)
