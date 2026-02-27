# JVIS Fullstack Mobile Story Template
# Version: 1.0
# Usage: For stories requiring backend API + mobile app implementation
# Location: {devStoryLocation}/{epicNum}.{storyNum}.story.md

---
# Story Metadata
epic: "{epicNum}"
story: "{storyNum}"
title: "{Story Title}"
status: "Draft"  # Draft | Ready | In Progress | Review | Done | Blocked
priority: "Medium"  # Critical | High | Medium | Low
complexity: "Medium"  # XS | S | M | L | XL
type: "fullstack-mobile"

# Stack Coverage
stack:
  backend: true
  mobile_ios: true
  mobile_android: true
  database: true
  api: true

# Platform Targets
platforms:
  - ios: "{min_ios_version}"
  - android: "{min_android_version}"

# Ownership
assignee: ""
backend_dev: ""
mobile_dev: ""
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
- **iOS**: {ios validation}
- **Android**: {android validation}

### AC-2: {Second Criterion Title}
- [ ] Given {precondition}
- [ ] When {action}
- [ ] Then {expected result}
- **Backend**: {backend validation}
- **iOS**: {ios validation}
- **Android**: {android validation}

### AC-3: {Third Criterion Title}
- [ ] Given {precondition}
- [ ] When {action}
- [ ] Then {expected result}
- **Backend**: {backend validation}
- **iOS**: {ios validation}
- **Android**: {android validation}

---

## Backend Implementation

### API Endpoints
<!-- API specifications for mobile clients -->
<!-- [Source: architecture/fullstack-architecture.md#api-design] -->

| Method | Endpoint | Purpose | Request | Response |
|--------|----------|---------|---------|----------|
| {METHOD} | `/api/v1/{endpoint}` | {purpose} | {request schema} | {response schema} |

### Backend Data Models
<!-- Database models affected by this story -->

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

### Mobile API Considerations
<!-- Special considerations for mobile clients -->

| Consideration | Implementation |
|---------------|----------------|
| Pagination | {cursor-based/offset pagination} |
| Offline Support | {sync strategy} |
| Push Notifications | {notification payload schema} |
| Image/Media Handling | {upload/download approach} |
| Rate Limiting | {mobile-specific limits} |

### Backend File Locations

| File | Purpose |
|------|---------|
| `src/api/routes/{resource}.py` | API routes |
| `src/services/{service}.py` | Business logic |
| `src/repositories/{repo}.py` | Data access |
| `tests/api/test_{resource}.py` | API tests |

---

## iOS Implementation

### UI Screens/Views
<!-- SwiftUI views required -->
<!-- [Source: architecture/ios-architecture.md] -->

| View | Location | Purpose |
|------|----------|---------|
| `{ViewName}View` | `Sources/Views/{Feature}/` | {description} |
| `{ViewName}ViewModel` | `Sources/ViewModels/{Feature}/` | {description} |

### iOS Data Models
<!-- Swift models for this feature -->

```swift
// Domain Model
struct {ModelName}: Identifiable, Codable {
    let id: UUID
    let {field}: {Type}
    let createdAt: Date
}

// API Response
struct {ResponseName}: Codable {
    let data: {ModelName}
    let message: String?
}
```

### iOS State Management
<!-- State handling approach -->

```swift
// ViewModel
@Observable
class {FeatureName}ViewModel {
    var items: [{ModelName}] = []
    var isLoading = false
    var error: Error?

    func load() async {
        // Implementation
    }
}
```

### iOS File Locations

| File | Purpose |
|------|---------|
| `Sources/Views/{Feature}/{View}.swift` | SwiftUI View |
| `Sources/ViewModels/{Feature}/{ViewModel}.swift` | ViewModel |
| `Sources/Models/{Model}.swift` | Data model |
| `Sources/Services/{Service}.swift` | API service |
| `Tests/{Feature}Tests/{Test}.swift` | Unit tests |

---

## Android Implementation

### UI Screens/Composables
<!-- Jetpack Compose screens required -->
<!-- [Source: architecture/android-architecture.md] -->

| Composable | Location | Purpose |
|------------|----------|---------|
| `{ScreenName}Screen` | `ui/{feature}/` | {description} |
| `{ScreenName}ViewModel` | `ui/{feature}/` | {description} |

### Android Data Models
<!-- Kotlin models for this feature -->

```kotlin
// Domain Model
data class {ModelName}(
    val id: String,
    val {field}: {Type},
    val createdAt: Instant
)

// API Response
@Serializable
data class {ResponseName}(
    val data: {ModelName},
    val message: String? = null
)
```

### Android State Management
<!-- State handling with ViewModel -->

```kotlin
// ViewModel
@HiltViewModel
class {FeatureName}ViewModel @Inject constructor(
    private val repository: {FeatureName}Repository
) : ViewModel() {

    private val _uiState = MutableStateFlow<UiState>(UiState.Loading)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    sealed interface UiState {
        data object Loading : UiState
        data class Success(val items: List<{ModelName}>) : UiState
        data class Error(val message: String) : UiState
    }
}
```

### Android File Locations

| File | Purpose |
|------|---------|
| `app/src/main/java/.../ui/{feature}/{Screen}.kt` | Composable Screen |
| `app/src/main/java/.../ui/{feature}/{ViewModel}.kt` | ViewModel |
| `app/src/main/java/.../data/model/{Model}.kt` | Data model |
| `app/src/main/java/.../data/repository/{Repo}.kt` | Repository |
| `app/src/test/java/.../ui/{feature}/{Test}.kt` | Unit tests |

---

## Cross-Platform Considerations

### Shared API Contract
<!-- Types shared between platforms -->

```typescript
// Shared type definition (for documentation)
interface {EntityName} {
    id: string;
    {field}: {Type};
    createdAt: string; // ISO 8601
}
```

### Platform Parity Checklist
- [ ] UI/UX matches across platforms
- [ ] Same data validation rules
- [ ] Consistent error messages
- [ ] Identical API consumption
- [ ] Same offline behavior

### Platform-Specific Differences
<!-- Document any intentional differences -->

| Feature | iOS | Android | Reason |
|---------|-----|---------|--------|
| {feature} | {ios approach} | {android approach} | {why different} |

---

## Implementation Sequence

### Phase 1: Backend API
- [ ] **Task 1.1**: Create/update database models (AC: 1)
- [ ] **Task 1.2**: Implement service layer (AC: 1, 2)
- [ ] **Task 1.3**: Create API endpoints (AC: 1, 2, 3)
- [ ] **Task 1.4**: API tests

### Phase 2: iOS Implementation
- [ ] **Task 2.1**: Create Swift models
- [ ] **Task 2.2**: Implement API service
- [ ] **Task 2.3**: Create ViewModel
- [ ] **Task 2.4**: Build SwiftUI views (AC: 1, 2, 3)
- [ ] **Task 2.5**: iOS unit tests

### Phase 3: Android Implementation
- [ ] **Task 3.1**: Create Kotlin models
- [ ] **Task 3.2**: Implement repository
- [ ] **Task 3.3**: Create ViewModel
- [ ] **Task 3.4**: Build Compose screens (AC: 1, 2, 3)
- [ ] **Task 3.5**: Android unit tests

### Phase 4: Integration & Testing
- [ ] **Task 4.1**: E2E testing on iOS
- [ ] **Task 4.2**: E2E testing on Android
- [ ] **Task 4.3**: Cross-platform parity verification
- [ ] **Task 4.4**: Performance testing

### Phase 5: Polish & Documentation
- [ ] **Task 5.1**: Accessibility audit (both platforms)
- [ ] **Task 5.2**: Dark mode verification
- [ ] **Task 5.3**: Localization check
- [ ] **Task 5.4**: Documentation update

---

## Dependencies

### Blocked By
- [ ] {dependency description} - Status: {status}

### Blocks
- [ ] Story {X.Y}: {description}

### External Dependencies
- [ ] {API/Service}: {availability status}
- [ ] {SDK/Library}: {version requirement}

---

## QA Notes

### Test Scenarios

| Scenario | Backend | iOS | Android | Steps | Expected | Status |
|----------|---------|-----|---------|-------|----------|--------|
| Happy path | ✓ | ✓ | ✓ | 1. {step} | {result} | ⬜ |
| Offline mode | - | ✓ | ✓ | 1. {step} | {fallback} | ⬜ |
| Auth expired | ✓ | ✓ | ✓ | 1. {step} | {refresh} | ⬜ |
| Network error | - | ✓ | ✓ | 1. {step} | {retry UI} | ⬜ |

### Device Testing Matrix

| Device | OS Version | Status |
|--------|------------|--------|
| iPhone 14 | iOS 17 | ⬜ |
| iPhone SE | iOS 16 | ⬜ |
| iPad Pro | iPadOS 17 | ⬜ |
| Pixel 7 | Android 14 | ⬜ |
| Samsung S23 | Android 13 | ⬜ |

### Non-Functional Requirements
- [ ] Performance: API < {X}ms, App startup < {Y}s
- [ ] Memory: Max {X}MB per screen
- [ ] Battery: No excessive drain
- [ ] Accessibility: VoiceOver/TalkBack support

---

## Dev Agent Record

### Implementation Log
```
[{timestamp}] Started backend implementation
[{timestamp}] Backend API complete
[{timestamp}] iOS implementation started
[{timestamp}] iOS complete, starting Android
[{timestamp}] Android complete
[{timestamp}] Integration testing
[{timestamp}] Completed
```

### Completion Notes
- Backend implementation: {description}
- iOS implementation: {description}
- Android implementation: {description}
- Deviations from plan: {description}

### Challenges & Lessons Learned
- Challenge: {description}
- Solution: {description}
- Lesson: {insight}

---
## Status History
| Date | Status | Notes |
|------|--------|-------|
| {date} | Draft | Initial creation |
