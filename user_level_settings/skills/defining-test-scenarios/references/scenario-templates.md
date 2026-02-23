# Scenario Templates & Reference

Detailed templates, field definitions, and checklists for the `/defining-test-scenarios` skill. The SKILL.md has the workflow and constraints; this file has the structural specifics.

## Scenario Structure

```markdown
# Test Scenarios: {Feature ID(s)} — {Feature Name(s)}

**Source spec:** {spec filename}
**Scope:** {Feature IDs covered}
**Generated:** {date}
**Status:** DRAFT — requires operator review

## Prerequisites
[Conditions that must be true before ANY scenario in this set can run.
These are shared GIVEN conditions factored out to avoid repetition.]

- The platform is deployed and accessible
- [Required accounts, states, and test data]
```

Each scenario:

```markdown
### TS-{FeatureID}.{number}: {Short descriptive name}

**Traces to:** {Spec scenario ID, e.g., F-05.1 | or IMPLICIT | or F-05.1 x F-08.3 for cross-feature}
**Category:** {HAPPY PATH | FAILURE | EDGE CASE | BOUNDARY | CONSTRAINT VALIDATION} {| CROSS-FEATURE if applicable}
**Criticality:** {BLOCKING | HIGH | MEDIUM | LOW}

**GIVEN:**
- [Teacher_A] has created [Class_Alpha] with NFT Certificate reward enabled

**WHEN:**
- [Teacher_A] saves the class configuration

**THEN:**
- [Class_Alpha] displays an NFT Certificate reward indicator on the class listing visible to students

**NOTES:** {Optional. Flag assumptions, dependencies, or clarify intent.}
```

## Field Definitions

**Traces to**: Links to the spec scenario this validates. Mark `IMPLICIT — no direct spec scenario` for gap coverage. Use `x` notation for cross-feature intersections.

**Category**: `HAPPY PATH` (success flow) | `FAILURE` (error handling) | `EDGE CASE` (unusual but valid) | `BOUNDARY` (exact threshold limits) | `CONSTRAINT VALIDATION` (tests SC-XX). Append `| CROSS-FEATURE` when the scenario spans features.

**Criticality assignment guidance:**
- `BLOCKING` — the happy path. If this fails, the feature is non-functional and no other test results are meaningful.
- `HIGH` — failure/edge cases on financial flows, data integrity, or security boundaries.
- `MEDIUM` — UX correctness, non-critical edge cases, robustness under unusual conditions.
- `LOW` — cosmetic behavior, unlikely concurrency scenarios, polish.

## Expansion Checklist

For each spec scenario, systematically consider:

- [ ] **Happy path**: Success case with realistic preconditions?
- [ ] **Input boundaries**: AT, just BELOW, and just ABOVE thresholds?
- [ ] **Empty / zero state**: No data exists yet?
- [ ] **Duplicate action**: Same action performed twice?
- [ ] **Sequence dependence**: Prerequisite not met?
- [ ] **State transition**: New state visible, old state gone?
- [ ] **Concurrency**: Two actors triggering simultaneously?
- [ ] **Partial completion**: Flow abandoned midway?
- [ ] **Permission / authorization**: Wrong actor attempts action?
- [ ] **Cascade / side effects**: Action affects other features?
- [ ] **Assumption-dependent**: `[ASSUMPTION]` tag? Apply Assumption Handling rules.
- [ ] **Constraint intersection**: System Constraint applies? Dedicated scenario.

## Self-Check

Before finalizing each scenario, verify: **could this scenario pass AND the feature still be broken in a way a user would notice?** If yes, the scenario is not testing the right thing — it's testing an implementation detail or a tautology. Rewrite it to target the actual observable failure.

## Coverage Summary Template

End every draft (and update) with a traceability list:

```markdown
## Coverage Summary

- **F-05.1** -> TS-05.01, TS-05.02, TS-05.03 — Happy Path, Boundary, Edge Case
- **F-05.2** -> TS-05.04 — Happy Path
- **(implicit)** -> TS-05.05 — Constraint Validation
- **F-05.1 x F-07.1** -> TS-05.06 — Cross-Feature, Edge Case

**Total spec scenarios in scope:** X
**Total test scenarios generated:** Y
**Expansion ratio:** Y/X

### Gaps
- {Spec scenarios that could not be fully expanded}
- {Behaviors from the expansion checklist that seem unspecified}

### Glossary Gaps
- {Any terms used in scenarios that are not in the Domain Glossary}
```

## Workflow Summary

```
Behavioral Spec + Feature ID
           |
           v
   +---------------+
   |   STEP 1      |---- Write full draft scenarios ---> specs/{name}.test.{FXX}.md
   |   (Draft)     |
   +-------+-------+
           |
           v
   +---------------+
   |   STEP 2      |---- AskUserQuestion (max 4) ------> Operator
   |   (Ask)       |<--- Answers --------------------+
   +-------+-------+
           |
           v
   +---------------+
   |   STEP 3      |---- Update scenarios file ---> specs/{name}.test.{FXX}.md
   |   (Update)    |---- Loop back to Step 2
   +---------------+
```

Only approved scenarios are handed to the downstream test-writing agent.
