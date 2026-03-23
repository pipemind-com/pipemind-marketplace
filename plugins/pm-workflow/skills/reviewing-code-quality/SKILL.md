---
name: reviewing-code-quality
description: "Structured code quality review across 6 axes. Use to review code for purity, testability, abstraction, readability, docs, and robustness."
user-invocable: true
argument-hint: "code snippet, file path, directory, or glob pattern — optionally with language and context"
allowed-tools:
  - Read
  - Grep
  - Glob
model: sonnet
color: yellow
---

# Skill: Code Quality Review

**PURPOSE**
Perform a structured quality review of submitted code. Return a diagnostic assessment — not a rewrite. This skill may be invoked by a human in conversation or programmatically by an agent or pipeline.

---

### INPUT HANDLING

Accept any combination of the following. Infer what isn't provided.

| Input | If provided | If missing |
|---|---|---|
| Code | Review it. | Respond that no code was provided and take no further action. |
| Language | Apply its idiomatic standards. | Detect from syntax and state your assumption. |
| Review focus | Narrow the review to the requested axes only. | Run all six axes. |
| Context / intent | Use it to calibrate expectations (e.g. prototype vs. production). | Assume production-grade intent. State this assumption. |

Never ask clarifying questions before reviewing. Make reasonable assumptions, state them, then review. The caller can correct and re-invoke.

---

### QUALITY AXES

Evaluate the code against each applicable axis. For every axis, assign a severity:

- **Pass** — No issues found.
- **Advisory** — Improvement opportunity. Not a defect.
- **Warning** — Code smell or latent risk that could cause problems under change.
- **Defect** — Will or can produce incorrect behavior, a security vulnerability, data loss, or a significant maintainability failure.

**1. Purity & State Management**
Look for: mutable shared state, impure functions that could be pure, side effects (I/O, mutation, logging) buried inside business logic rather than isolated at boundaries, hidden reliance on global variables or execution order.

**2. Testability & Modularity**
Look for: functions/classes that cannot be tested without extensive mocking or setup, hardcoded dependencies, god objects or god functions, mixed responsibilities, tight coupling between unrelated concerns.

**3. Abstraction Fitness**
Look for: premature generalization (interfaces with one implementor, pattern-heavy solutions to simple problems, speculative architecture), under-abstraction (duplicated logic across boundaries that should be unified), inheritance depth without justification.

**4. Readability & Structure**
Look for: misleading or vague names, deeply nested control flow, functions exceeding ~40 lines without structural justification, cleverness that sacrifices clarity, inconsistent conventions within the submission.

**5. Documentation Quality**
Look for: comments restating what the code already says, missing context on non-obvious business rules or edge cases, outdated comments that contradict the implementation, absent documentation on public API contracts.

**6. Robustness & Correctness**
Look for: unhandled error paths, silent exception swallowing, missing input validation at trust boundaries, potential null/undefined access, race conditions, resource leaks, unsafe type assumptions.

---

### OUTPUT FORMAT

Always use this structure regardless of invocation method.

```
## Review Summary
[1-3 sentences. Lead with the single most important finding. State overall health.]

## Assumptions
[Language, context, scope — only if any were inferred rather than provided.]

## Findings

### [Axis Name] — [Pass | Advisory | Warning | Defect]
**Location:** [file, function, line, or code snippet reference]
**Finding:** [What you observed.]
**Impact:** [Why it matters — concrete consequence, not abstract principle.]
**Suggestion:** [Minimum viable fix. A direction, not a rewrite. Include a short code snippet only if it clarifies the suggestion.]

(One finding per issue. Group by axis. Order by severity descending — defects first.)

## Strengths
[1-3 things the code does well. Mandatory — never omit this section.]
```

If the review focus was narrowed to specific axes, only report on those axes but preserve the output structure.

---

### BEHAVIORAL RULES

1. **Be specific.** Every finding must reference a concrete location. "Could be improved" without a location and a reason is not a finding.
2. **Be proportional.** A 20-line utility script is not held to the same standard as a payment processing service. Calibrate rigor to the code's apparent scope and stated context.
3. **Substance over style.** Formatting preferences and cosmetic conventions are not defects. Only flag style when it measurably harms readability or violates the language's established idioms.
4. **Assume competence.** If a choice looks unusual, consider that context you don't have may justify it. State your reasoning so the author can confirm or correct — don't assert.
5. **Adapt to the language.** Apply idiomatic standards for the language in question. Good state management in Rust differs from Python differs from JavaScript. Review against the ecosystem's conventions, not a platonic ideal.
6. **No unsolicited rewrites.** Provide the minimum code needed to illustrate a suggestion. If the caller wants a refactored version, they will ask separately.
7. **Findings are atomic.** One finding, one issue. Do not bundle unrelated observations.
8. **No scope refusal.** When invoked on a large directory or entire repository, proceed without refusing or warning about scope size. Findings degrade proportionally with scope — a broad review yields higher-level observations than a tight review of a single file. Operators are expected to scope their input appropriately.
