# JVIS Fullstack Story Template
# Version: 1.0
# Usage: For stories requiring both backend and frontend work
# Location: {devStoryLocation}/{epicNum}.{storyNum}.story.md

---
# Story Metadata
epic: "{epicNum}"
story: "{storyNum}"
title: "{Story Title}"
status: "Draft"  # Draft | Ready | In Progress | Review | Done | Blocked
priority: "Medium"  # Critical | High | Medium | Low
complexity: "Medium"  # XS | S | M | L | XL
type: "fullstack"  # fullstack | feature | bugfix | refactor | spike | chore

# Stack Coverage
stack:
  backend: true
  frontend: true
  database: true
  api: true

# Ownership
assignee: ""
backend_dev: ""
frontend_dev: ""
reviewer: ""
created: "{YYYY-MM-DD}"
updated: "{YYYY-MM-DD}"

# Links
epic_ref: "docs/epics/{epicNum}.epic.md"
prd_ref: "docs/prd/PRD.md#{section}"
architecture_ref: "docs/architecture/fullstack-architecture.md"
---

# {epicNum}.{storyNum} - {Story Title}

## Story Statement

As a **{user type}**,
I want **{goal/desire}**,
So that **{benefit/value}**.

## Acceptance Criteria

### AC-1: {First Criterion Title}
- [ ] Given {precondition}
- [ ] When {action}
- [ ] Then {expected result}
- **Backend**: {backend validation}
- **Frontend**: {frontend validation}

### AC-2: {Second Criterion Title}
- [ ] Given {precondition}
- [ ] When {action}
- [ ] Then {expected result}
- **Backend**: {backend validation}
- **Frontend**: {frontend validation}

### AC-3: {Third Criterion Title}
- [ ] Given {precondition}
- [ ] When {action}
- [ ] Then {expected result}
- **Backend**: {backend validation}
- **Frontend**: {frontend validation}

---

## Backend Implementation

### API Endpoints
<!-- API specifications from architecture document -->
<!-- [Source: architecture/fullstack-architecture.md#api-design] -->

| Method | Endpoint | Purpose | Request | Response |
|--------|----------|---------|---------|----------|
| {METHOD} | `/api/v1/{endpoint}` | {purpose} | {request schema} | {response schema} |

### Backend Data Models
<!-- Database models affected by this story -->
<!-- [Source: architecture/fullstack-architecture.md#data-models] -->

```yaml
{ModelName}:
  fields:
    - name: id
      type: UUID
      required: true
    - name: {field}
      type: {type}
      validation: {rules}
  relationships:
    - {relationship}
```

### Backend Services
<!-- Service layer changes required -->

| Service | Method | Purpose |
|---------|--------|---------|
| `{ServiceName}` | `{method}` | {description} |

### Backend File Locations
<!-- Where backend code should be created/modified -->

| File | Purpose |
|------|---------|
| `src/api/routes/{resource}.py` | API routes |
| `src/services/{service}.py` | Business logic |
| `src/repositories/{repo}.py` | Data access |
| `tests/api/test_{resource}.py` | API tests |
| `tests/services/test_{service}.py` | Service tests |

---

## Frontend Implementation

### UI Components
<!-- Component specifications from architecture -->
<!-- [Source: architecture/fullstack-architecture.md#frontend-architecture] -->

| Component | Location | Props | Purpose |
|-----------|----------|-------|---------|
| `{ComponentName}` | `src/components/{path}/` | `{ prop: Type }` | {description} |

### Frontend State Management
<!-- State changes required -->

```typescript
// Store/State shape
interface {FeatureName}State {
  {field}: {Type};
  loading: boolean;
  error: string | null;
}

// Actions/Mutations
- {ACTION_NAME}: {description}
```

### API Integration
<!-- How frontend calls backend -->

```typescript
// API Client method
async function {methodName}(params: {ParamsType}): Promise<{ResponseType}> {
  return api.{method}('/api/v1/{endpoint}', params);
}
```

### Frontend File Locations
<!-- Where frontend code should be created/modified -->

| File | Purpose |
|------|---------|
| `src/components/{Feature}/{Component}.tsx` | Component |
| `src/components/{Feature}/{Component}.test.tsx` | Component tests |
| `src/stores/{feature}.ts` | State management |
| `src/api/{feature}.ts` | API client |
| `src/types/{feature}.ts` | TypeScript types |

---

## Shared Types

<!-- Types shared between frontend and backend -->
<!-- [Source: packages/shared-types/] -->

```typescript
// Shared type definitions
export interface {EntityName} {
  id: string;
  {field}: {Type};
  createdAt: Date;
  updatedAt: Date;
}

export interface {RequestType} {
  {field}: {Type};
}

export interface {ResponseType} {
  data: {EntityName};
  message?: string;
}
```

---

## Implementation Sequence

### Phase 1: Backend Foundation
- [ ] **Task 1.1**: Create/update database models (AC: 1)
  - [ ] Add migrations
  - [ ] Seed test data
- [ ] **Task 1.2**: Implement repository layer (AC: 1)
  - [ ] CRUD operations
  - [ ] Query methods
- [ ] **Task 1.3**: Implement service layer (AC: 1, 2)
  - [ ] Business logic
  - [ ] Validation
- [ ] **Task 1.4**: Create API endpoints (AC: 1, 2, 3)
  - [ ] Route handlers
  - [ ] Request validation
  - [ ] Response serialization

### Phase 2: Backend Testing
- [ ] **Task 2.1**: Unit tests for services
- [ ] **Task 2.2**: API integration tests
- [ ] **Task 2.3**: Verify API documentation

### Phase 3: Frontend Foundation
- [ ] **Task 3.1**: Create shared types (AC: 1)
- [ ] **Task 3.2**: Implement API client methods
- [ ] **Task 3.3**: Create state management
- [ ] **Task 3.4**: Implement UI components (AC: 1, 2, 3)
  - [ ] Component structure
  - [ ] Styling
  - [ ] Event handlers

### Phase 4: Frontend Testing
- [ ] **Task 4.1**: Component unit tests
- [ ] **Task 4.2**: State management tests
- [ ] **Task 4.3**: API integration tests (mocked)

### Phase 5: Integration
- [ ] **Task 5.1**: End-to-end flow verification
- [ ] **Task 5.2**: Cross-browser testing
- [ ] **Task 5.3**: Performance verification

### Phase 6: Documentation & Cleanup
- [ ] **Task 6.1**: Update API documentation
- [ ] **Task 6.2**: Update component storybook (if applicable)
- [ ] **Task 6.3**: Code cleanup and refactoring

---

## Dependencies

### Blocked By
- [ ] {dependency description} - Status: {status}

### Blocks
- [ ] Story {X.Y}: {description}

### External Dependencies
- [ ] {API/Service}: {availability status}

---

## QA Notes

### Test Scenarios

| Scenario | Backend | Frontend | Steps | Expected | Status |
|----------|---------|----------|-------|----------|--------|
| Happy path | ✓ | ✓ | 1. {step} 2. {step} | {result} | ⬜ |
| Validation error | ✓ | ✓ | 1. {step} 2. {step} | {error msg} | ⬜ |
| Network error | - | ✓ | 1. {step} 2. {step} | {fallback} | ⬜ |
| Auth failure | ✓ | ✓ | 1. {step} 2. {step} | {redirect} | ⬜ |

### Non-Functional Requirements
- [ ] Performance: API response < {X}ms, UI render < {Y}ms
- [ ] Security: {requirement}
- [ ] Accessibility: WCAG {level}

---

## Dev Agent Record

### Implementation Log
<!-- Filled by Dev Agent during implementation -->
```
[{timestamp}] Started backend implementation
[{timestamp}] Backend API complete, starting frontend
[{timestamp}] Frontend components complete
[{timestamp}] Integration testing
[{timestamp}] Completed
```

### Completion Notes
<!-- Filled by Dev Agent upon completion -->
- Backend implementation: {description}
- Frontend implementation: {description}
- Integration notes: {description}
- Deviations from plan: {description}

### Challenges & Lessons Learned
<!-- For future story preparation -->
- Challenge: {description}
- Solution: {description}
- Lesson: {insight}

---
## Status History
| Date | Status | Notes |
|------|--------|-------|
| {date} | Draft | Initial creation |
