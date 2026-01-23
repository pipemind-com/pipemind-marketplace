# XXX: Descriptive Title

## Planner

**Layers Affected**: [frontend | backend | service | database]
**Deployment Order**: [database → service → backend → frontend]

### Requirements

- [ ] Requirement 1 (testable, specific)
- [ ] Requirement 2 (testable, specific)
- [ ] Requirement 3 (testable, specific)

### Problem Analysis

#### Root Cause

Explain the root cause, not just symptoms.

**❌ Current Architecture (BROKEN):**
```
[Show current broken flow with specific file paths and line numbers]
Component A (src/path/file.ts:42)
  ↓ Problem: [what's wrong]
  ↓ Consequence: [impact]
```

**Problems:**
1. `src/path/file.ts:42` - [specific issue]
2. `src/path/other.ts:89` - [specific issue]

**✓ Proposed Architecture:**
```
[Show proposed fixed flow]
Component A
  ↓ Calls: [what it should call]
  ↓ Layer B handles: [what this layer does]
  ↓ Returns: [what comes back]
```

**Benefits:**
- Benefit 1
- Benefit 2
- Benefit 3

### Files to Modify

| File | Change | Lines |
|------|--------|-------|
| `path/to/file1.ext` | Description of change | 42-58 |
| `path/to/file2.ext` | Description of change | New file |
| `path/to/file3.ext` | Description of change | 123-145 |

### Implementation Steps

#### Phase 1: [Phase Name]

1. **[Step description]:**
   ```language
   // path/to/file.ext
   // Complete code snippet with imports

   import { Dependency } from 'package';

   export function newFunction() {
     // Implementation
   }
   ```

2. **[Next step description]:**
   ```language
   // More complete code
   ```

#### Phase 2: [Next Phase Name]

[Continue with implementation phases...]

### Context

**Key Design Principles:**
- Principle 1: Explanation
- Principle 2: Explanation

**Key Patterns:**
- Pattern 1: How to use it
- Pattern 2: How to use it

**Gotchas:**
- ⚠️ Gotcha 1: What to watch out for
- ⚠️ Gotcha 2: What to watch out for

**Testing Strategy:**
- Unit tests: What to test
- Integration tests: What to test
- E2E tests: What to test

**Deployment:**
```bash
# Commands to deploy each layer
```

---

## Builder

_Builder fills this section during implementation._

### Implementation Notes

[What was actually built, any deviations from plan and why]

### Test Results

[Which tests were written, which passed, coverage achieved]

### Manual Verification

[Steps performed to manually verify the implementation]

### Deviations from Plan

[Any changes from the original plan and rationale]

---

## Status

- [ ] Planned (planner checks when task created)
- [ ] Built & Tested (builder checks when complete)
