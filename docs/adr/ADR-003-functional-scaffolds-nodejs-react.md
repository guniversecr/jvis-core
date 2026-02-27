# ADR-003: Functional Scaffolds for Node.js Express & React Vite

**Status:** Approved
**Date:** 2026-02-15
**Author:** Dev
**Reviewers:** QA, Architect

---

## Context

ADR-002 made `python-fastapi` the first functional stack — generating a working CRUD API with Clean Architecture, tests, and database integration. 16 of 17 stacks remain hollow (directory structure + config, no business logic). This ADR extends the functional scaffold pattern to the two highest-priority stacks and validates everything with integration tests.

**Goal:** 3 of 17 stacks functional, with cross-stack integration tests.

## Decision

### Scope: Node.js Express + React Vite (Epic 3)

Extend the functional scaffold pattern established in ADR-002 to:
1. **nodejs-express** — CRUD API with Prisma + TypeScript + Clean Architecture
2. **react-vite** — UI scaffold with pages, components, hooks, API client

### Architecture Pattern (Node.js Express)

```
src/
├── domain/
│   ├── entities/item.ts         # Pure TypeScript interface
│   └── errors/app-error.ts      # Custom error classes
├── application/
│   ├── dto/item.dto.ts          # Zod validation schemas
│   └── use-cases/item.service.ts # Business logic CRUD
├── infrastructure/
│   ├── database/prisma-client.ts # PrismaClient singleton
│   ├── config/env.ts             # Env config with Zod
│   └── repositories/item.repository.ts # Prisma-backed CRUD
├── presentation/
│   ├── controllers/item.controller.ts  # Express handlers
│   ├── routes/items.ts                 # Express Router
│   └── middleware/error-handler.ts     # Global error middleware
tests/
├── setup.ts
├── unit/item.service.test.ts
└── integration/items.test.ts
```

### Architecture Pattern (React Vite)

```
src/
├── types/item.ts               # TypeScript interfaces
├── services/api.ts             # Axios CRUD client
├── utils/config.ts             # API_BASE_URL from env
├── hooks/
│   ├── useItems.ts             # Item state management
│   └── useApi.ts               # Generic async hook
├── pages/
│   ├── HomePage.tsx            # Item list + create form
│   └── NotFoundPage.tsx        # 404 page
├── components/
│   ├── layout/AppLayout.tsx    # Header + Outlet
│   └── ui/
│       ├── ItemList.tsx        # List of items
│       ├── ItemCard.tsx        # Single item display
│       └── ItemForm.tsx        # Create/edit form
├── styles/index.css            # Minimal CSS
tests/
├── setup.ts
├── unit/components/
└── unit/hooks/
```

### Key Technical Decisions

1. **Prisma abstracts DB** — No database-conditional branching in application code (unlike python-fastapi). Prisma handles it via `DATABASE_URL`.
2. **Most `.ts` files are NOT `.j2` templates** — Avoids JSX/Jinja2 `{}` conflicts. Only files needing `{{ project_name }}` use `.j2`.
3. **Zod replaces Pydantic** — Runtime validation for TypeScript.
4. **`cuid` IDs** — Via Prisma `@default(cuid())`.
5. **No state management library** — `useState` + custom hooks sufficient for CRUD demo.
6. **API client configurable** — Points to `API_BASE_URL` env var.

## Consequences

### Positive
- 3 of 17 stacks produce functional, working projects
- Cross-stack integration tests catch regressions
- Frontend + backend pair demonstrates full-stack JVIS workflow
- Pattern is proven and repeatable for remaining stacks

### Negative
- More template files to maintain per stack
- Template updates require re-running integration tests

### Risks
- Jinja2 `{}` conflicts with TypeScript/JSX — mitigated by using `.j2` only where needed
- Prisma version drift — pinned at `^5.19.0`

## Stories

1. **Story 3.1** — Node.js Express Functional Scaffold (L)
2. **Story 3.2** — React Vite Functional Scaffold (M)
3. **Story 3.3** — Integration Tests (S)
