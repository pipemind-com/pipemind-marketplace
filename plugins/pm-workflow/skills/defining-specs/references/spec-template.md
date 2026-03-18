# Spec Template Reference

Use this as the structural template when generating spec files. Populate every section with content derived from the source document — do not leave placeholder text.

---

## File Header

```markdown
# Spec: {Milestone or Feature Name} — {Epic Name if applicable}
**Source:** {filename or description of input}
**Epic:** {E-XX if applicable, otherwise "N/A — single spec"}
**Glossary:** specs/glossary.md
**See also:** specs/{name}.xrefs.md (if cross-epic boundaries exist, otherwise omit)
**Generated:** {date}
**Status:** DRAFT — requires operator review
```

---

## Domain Glossary

The Domain Glossary always lives in `specs/glossary.md` — never inline in spec files. Define every Actor and key domain term there. For each Actor, define **negative boundaries** — what the actor explicitly *cannot* do. This prevents downstream agents from inferring permissions that were never granted.

Spec files reference it in their header and do not duplicate glossary content. The glossary format:

```markdown
# Domain Glossary

## Actors

**Student**
End-user enrolled in the platform with a connected wallet.
*Cannot:* modify pricing, issue rewards, or access other students' data.

**Admin**
Platform operator with elevated privileges for configuration and oversight.
*Cannot:* access or transact with student wallets directly.

## Key Terms

**Enrollment**
The state transition when a student...

**Staking Reward**
ADA distributed to a student's wallet as a result of...
```

---

## System Constraints (Non-Behavioral)

Requirements that gate acceptance but are not user flows. Number them `SC-XX`.

```markdown
## System Constraints
- **SC-01**: All financial calculations must be deterministic and reproducible given the same inputs.
```

---

## Feature Specs (GIVEN-WHEN-THEN)

Each feature gets:
- A **Feature ID** (`F-XX`) and short name
- A **Priority**: `MUST`, `SHOULD`, `COULD`, `WON'T (this milestone)`
- **Cross-feature dependencies** where applicable: `**Requires:** F-YY ({name})` — this tells downstream agents and the test scenario skill where features interconnect
- One or more **Scenarios** in GIVEN-WHEN-THEN with **Scenario IDs** (`F-XX.Y`)

**Priority assignment guidance:**
- `MUST` — the milestone/epic fails acceptance without this. Core flows, payment, and data integrity.
- `SHOULD` — expected by users but the system is functional without it. Error messages, edge case handling.
- `COULD` — improves UX but is clearly deferrable. Polish, convenience features.
- `WON'T` — explicitly out of scope for this milestone. Include only to prevent downstream agents from building it.

```markdown
### F-01: Student Enrollment | MUST

**Requires:** F-04 (Wallet Connection)

**F-01.1: Successful enrollment (happy path)**
- **GIVEN** a visitor with a compatible browser wallet containing at least the minimum required ADA
- **WHEN** the visitor connects their wallet and confirms the enrollment transaction
- **THEN** the system records the enrollment, the dashboard becomes accessible, and confirmation is displayed

**F-01.2: Enrollment with insufficient funds (failure)**
- **GIVEN** a visitor with a wallet containing less than the minimum required ADA
- **WHEN** the visitor attempts to confirm enrollment
- **THEN** the transaction is not submitted and the visitor sees the shortfall amount
```

---

## Open Questions & Assumptions Log

```markdown
## Open Questions
- OQ-01: {Unresolved question}

## Assumptions
- A-01: {Assumption made, referenced as [ASSUMPTION] in the spec}
```
