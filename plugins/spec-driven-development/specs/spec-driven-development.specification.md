# Spec: spec-driven-development — Specification & Design
**Source:** plugins/spec-driven-development/ (brownfield reverse-engineering)
**Epic:** E-C
**Glossary:** specs/glossary.md
**Generated:** 2026-03-22
**Status:** DRAFT — requires operator review

---

## System Constraints

- **SC-01**: Behavioral specs must contain no code, pseudo-code, JSON, API designs, system diagrams, or architecture decisions.
- **SC-02**: Behavioral specs must not reference specific technologies, libraries, or frameworks unless they are explicitly named as mandated in the source document.
- **SC-03**: Every requirement in a behavioral spec must describe an observable state change or user-facing outcome — not an implementation mechanism.
- **SC-04**: For every success scenario in a behavioral spec, at least one failure or edge-case scenario must be specified.
- **SC-05**: Test scenarios must not contain code, pseudo-code, or assertion syntax of any kind; they describe observable outcomes only.
- **SC-06**: Test scenarios must not reference source code, file structure, or test infrastructure; the scenarios are implementation-agnostic.
- **SC-07**: The Domain Glossary always lives in specs/glossary.md and is never duplicated inline in spec files or test scenario files.
- **SC-08**: Tables are never used in specs or test scenario files; headings, bullet lists, and GIVEN-WHEN-THEN blocks are the only formatting primitives.
- **SC-09**: The /defining-specs and /defining-test-scenarios skills never self-terminate; they loop until the operator explicitly stops the session.

---

## F-01: Behavioral Spec Definition | MUST

**F-01.1: Complete spec draft written immediately from source document (happy path)**
- **GIVEN** an operator provides a source document (PRD, feature brief, or raw description)
- **WHEN** /defining-specs processes the input
- **THEN** it writes a complete first-draft spec file to specs/{name}.md before asking any questions; the draft contains all features inferable from the source, all GIVEN-WHEN-THEN scenarios written to the best of available knowledge, and all gaps tagged [ASSUMPTION]

**F-01.2: Spec file used as checkpoint — draft skipped if file exists**
- **GIVEN** a spec file already exists at the expected path (e.g., specs/enrollment.md)
- **WHEN** the operator invokes /defining-specs
- **THEN** the skill reads the existing file and proceeds directly to the question phase (Step 2) without overwriting the draft; the file is the source of truth

**F-01.3: Scope assessment — 12 or fewer features, no split**
- **GIVEN** the source document implies 12 or fewer distinct features
- **WHEN** the skill performs scope assessment
- **THEN** it proceeds directly to draft generation without any epic-splitting interaction; a single spec file is produced

**F-01.4: Scope assessment — more than 12 features triggers epic split**
- **GIVEN** the source document implies more than 12 features
- **WHEN** the skill performs scope assessment
- **THEN** it presents the proposed epics via AskUserQuestion as a single-select choice; each epic shows an ID, name, one-sentence scope, and estimated feature count; a "Spec all — I'll wait" option is always included

**F-01.5: Epic selection — single epic specced**
- **GIVEN** the operator selects one epic to spec now
- **WHEN** the skill proceeds
- **THEN** it generates the spec scoped to that epic only; the output file is specs/{name}.{epic-slug}.md (e.g., specs/milestone-4.payments.md)

**F-01.5b: Epic selection — "Spec all" writes drafts first, then questions**
- **GIVEN** the operator selects "Spec all — I'll wait"
- **WHEN** the skill proceeds
- **THEN** it writes complete first-draft spec files for all epics in sequence before asking any questions; after all drafts are written, it conducts a single combined question round covering ambiguities across all epics; questions are asked in order of criticality across all epics, not per-epic

**F-01.6: Epic cross-references file created when epics share boundaries**
- **GIVEN** two or more epics produce state that other epics consume (e.g., Epic A creates a wallet state that Epic B reads)
- **WHEN** specs are being written
- **THEN** a specs/{name}.xrefs.md file is created mapping each interface: which epic owns it, the contract, and which features on each side depend on it; individual epic specs note its existence without duplicating content from it

**F-01.7: Domain Glossary created if missing**
- **GIVEN** specs/glossary.md does not exist
- **WHEN** the spec draft is generated
- **THEN** the skill creates specs/glossary.md with all actors (including negative boundaries) and key terms extracted from the source document

**F-01.8: Domain Glossary updated when terms change**
- **GIVEN** operator answers reveal that a term or actor definition in specs/glossary.md is incomplete or incorrect
- **WHEN** the spec file is updated in Step 3
- **THEN** specs/glossary.md is also updated to reflect the revised definition; the glossary is the single source of truth and always kept in sync

**F-01.9: Questions asked after draft — max 4 per round**
- **GIVEN** the first draft has been written
- **WHEN** the skill moves to the question phase
- **THEN** it presents at most 4 questions via AskUserQuestion; each question shows its criticality tag ([HIGH], [MEDIUM], or [LOW]) and type tag ([AMBIGUITY], [MISSING ACTOR], [EDGE CASE], [CONTRADICTION], [SCOPE], [IMPLICIT PRECONDITION], or [EXPLORATION]); each has 2-4 concrete answer choices plus a free-text option

**F-01.10: Question selection — 5 candidates ranked, top 4 asked**
- **GIVEN** the skill identifies candidate questions for the current round
- **WHEN** it selects which to ask
- **THEN** it generates up to 5 candidates (up to 4 refinement questions + 1 exploratory), ranks all 5 by criticality impact on downstream agents, and asks only the top 4; the exploratory question may be the 5th dropped if ranked last

**F-01.11: Exploratory question probes for adjacent gaps**
- **GIVEN** the skill is generating its candidate questions
- **WHEN** it formulates the exploratory question
- **THEN** the question targets something absent from the source document but likely necessary — operational realities, compliance exposure, cross-system interactions, abuse vectors, or data lifecycle gaps

**F-01.12: Step 3 — all affected sections updated, not just the directly answered one**
- **GIVEN** an operator provides answers to the current round of questions
- **WHEN** the skill re-reads the entire spec file and applies updates
- **THEN** it identifies all sections affected by the new information (an answer about one feature may affect the glossary, system constraints, or other feature scenarios) and updates all of them; it does not update only the directly addressed section

**F-01.13: Vague answer — assumption retained, loop continues**
- **GIVEN** the operator gives a vague answer ("just figure it out")
- **WHEN** the skill processes the answer
- **THEN** it retains the [ASSUMPTION] tag on the relevant item, moves to the next question, and does not treat the vague answer as a resolution

**F-01.14: Spec written with no code or architecture (constraint violation attempt)**
- **GIVEN** the source document includes system design diagrams or code snippets
- **WHEN** the skill generates the spec
- **THEN** the generated spec contains no code, no diagrams, no API shapes, and no schema definitions; behavioral outcomes are extracted from the source and expressed in GIVEN-WHEN-THEN form only

**F-01.15: No happy-path bias — failure scenarios required**
- **GIVEN** a feature has a success flow
- **WHEN** the spec is written
- **THEN** at least one failure, edge case, or adversarial scenario is specified alongside the happy path; scenarios consider insufficient resources, expired sessions, wrong actor, duplicate submissions, external dependency unavailable, interrupted action, and concurrent access

---

## F-02: Test Scenario Expansion | MUST

**Requires:** F-01 (Behavioral Spec Definition)

**F-02.1: Test scenarios written immediately from spec feature (happy path)**
- **GIVEN** an operator invokes /defining-test-scenarios with a spec file path and feature ID (e.g., specs/enrollment.md F-05)
- **WHEN** the skill reads the spec and the Domain Glossary
- **THEN** it writes a complete first-draft test scenario file to specs/{spec-name}.test.{FXX}.md covering all systematic expansion categories for that feature; it does not ask questions before writing the draft

**F-02.1b: Feature ID not found — fail and list valid IDs**
- **GIVEN** an operator provides a feature ID (e.g., F-99) that does not exist in the specified spec file
- **WHEN** the skill attempts to locate the feature
- **THEN** it reports that the feature ID was not found and lists all valid feature IDs present in the spec file; it does not proceed to scenario generation

**F-02.2: Test scenario file used as checkpoint**
- **GIVEN** specs/{spec-name}.test.{FXX}.md already exists
- **WHEN** the operator invokes /defining-test-scenarios
- **THEN** the skill reads the existing file and proceeds to the question phase without overwriting; the file is the source of truth

**F-02.3: Scenario IDs follow TS-FXX.YY format**
- **GIVEN** test scenarios are generated for feature F-05
- **WHEN** scenario IDs are assigned
- **THEN** each scenario ID follows the format TS-F05.01, TS-F05.02, etc.; IDs are sequential and not reused within the file

**F-02.4: Deterministic entity labels used throughout**
- **GIVEN** a scenario requires multiple test entities of the same type (e.g., two students)
- **WHEN** scenarios are written
- **THEN** each distinct entity receives a deterministic label (e.g., [Student_A], [Student_B], [Wallet_Insufficient]); labels are scoped to the scenario unless explicitly stated to be shared across scenarios

**F-02.5: Spec vocabulary used exactly**
- **GIVEN** the Domain Glossary defines an actor as "Student" (capital S)
- **WHEN** test scenarios reference that actor
- **THEN** every reference uses exactly "Student" — not "user", "learner", or "student" (lowercase); vocabulary must match the glossary spelling precisely

**F-02.6: Systematic expansion — 12-category checklist applied**
- **GIVEN** a feature spec is being expanded into scenarios
- **WHEN** the skill generates scenarios
- **THEN** it systematically considers all 12 expansion categories: happy path, boundary values, empty/zero state, duplicate submissions, operation sequences, state transitions, concurrent access, partial completion, wrong actor/permission, cascade effects, cross-feature interactions, and system constraint compliance

**F-02.7: No code or assertion syntax in scenarios**
- **GIVEN** a scenario describes a system response
- **WHEN** the THEN clause is written
- **THEN** it expresses the observable user-facing outcome (e.g., "the system displays an error message") — never an HTTP status code, function return value, database query, or assertion expression

**F-02.8: No codebase references in scenarios**
- **GIVEN** the skill knows the project's file structure
- **WHEN** scenarios are written
- **THEN** no scenario references source code files, method names, table names, or test infrastructure setup; scenarios are fully decoupled from any implementation

**F-02.9: Assumption-dependent scenarios tagged in NOTES**
- **GIVEN** a spec feature has an unresolved [ASSUMPTION]
- **WHEN** a scenario is generated that depends on that assumption
- **THEN** the scenario includes a NOTES field stating "Depends on assumption A-XX. If revised, this scenario must be regenerated." and the scenario criticality is capped at MEDIUM

**F-02.10: Coverage summary always present**
- **GIVEN** any test scenario file is generated
- **WHEN** the file is written
- **THEN** it ends with a Coverage Summary containing: a traceability list mapping spec scenarios (F-XX.Y) to test scenarios (TS-FXX.YY), the expansion ratio (total spec scenarios vs total test scenarios), a list of gaps (spec scenarios not fully expanded), and any glossary gaps (terms used but not defined in specs/glossary.md)

**F-02.11: Concurrent access scenario generated when applicable**
- **GIVEN** a feature spec describes a shared resource (e.g., a course enrollment with limited seats)
- **WHEN** the expansion checklist reaches concurrent access
- **THEN** at least one scenario is generated describing two actors attempting the same operation simultaneously, specifying the observable outcome for each

**F-02.12: Wrong actor scenario generated when permissions exist**
- **GIVEN** a feature is restricted to a specific actor (e.g., only Admin can modify pricing)
- **WHEN** the expansion checklist reaches permissions
- **THEN** a scenario is generated where a non-permitted actor attempts the action, specifying that the action is rejected and the requesting actor's state is unchanged

---

## F-03: Agent Author Guidance | SHOULD

**F-03.1: Discovery phase asks type and purpose before any creation**
- **GIVEN** an operator asks the agent-author meta-agent to help create a new agent or skill
- **WHEN** the agent-author begins
- **THEN** it asks clarifying questions to determine: type (agent or skill), purpose and mission, tools needed, and expected input/output; it does not begin generating files before this discovery phase completes

**F-03.2: Agent design — model selected based on task complexity**
- **GIVEN** the discovery phase reveals the purpose of the new agent
- **WHEN** the agent-author recommends a model
- **THEN** it recommends haiku for simple, fast, or high-volume tasks; sonnet (default) for balanced general-purpose tasks; and opus only for tasks requiring complex reasoning, architectural design, or multi-step problem solving

**F-03.3: Tool tier assigned starting from minimum required**
- **GIVEN** the agent's purpose is identified
- **WHEN** the agent-author determines tool permissions
- **THEN** it starts from the read-only tier (Read, Glob, Grep) and adds tiers only as necessary: Write tier if the agent creates files, Execute tier if it runs commands, Orchestrate tier if it spawns subagents; permissions beyond what is necessary are not added

**F-03.4: Agent naming enforces kebab-case nouns**
- **GIVEN** an operator proposes a name for a new agent
- **WHEN** the agent-author validates the name
- **THEN** it confirms or corrects to a kebab-case noun format (e.g., code-reviewer, task-planner); gerunds, verbs, and non-kebab-case forms are rejected with an explanation

**F-03.5: Skill naming enforces gerunds**
- **GIVEN** an operator proposes a name for a new skill
- **WHEN** the agent-author validates the name
- **THEN** it confirms or corrects to a gerund in kebab-case (e.g., reviewing-code, compiling-planner-agent); noun names are rejected with an explanation

**F-03.6: Validation checklist applied before declaring done**
- **GIVEN** a new agent or skill file has been generated
- **WHEN** the agent-author performs final validation
- **THEN** it checks: line count within target, 80% rule compliance, no content duplicated from CLAUDE.md or docs/, no placeholder text, minimal tool permissions, valid YAML frontmatter; any failure is reported to the operator with specific remediation

**F-03.7: 80% rule taught and applied**
- **GIVEN** an operator asks why an instruction was excluded from a draft
- **WHEN** the agent-author explains
- **THEN** it explains the 80% rule: if an instruction doesn't apply to 80%+ of sessions for that agent, it belongs in docs/ or should be removed; it teaches this principle rather than applying it silently

**F-03.8: Reference-not-duplicate principle enforced**
- **GIVEN** project context (tech stack, key directories) exists in CLAUDE.md
- **WHEN** the agent-author generates an agent that needs that context
- **THEN** the generated agent references CLAUDE.md rather than restating the context; the agent-author explains this principle if the operator questions why content was not inlined

**F-03.9: Progressive disclosure pattern taught**
- **GIVEN** an operator wants to include detailed documentation in an agent file
- **WHEN** that content would push the agent beyond 100 lines
- **THEN** the agent-author explains the progressive disclosure pattern: detailed content belongs in docs/ files that agents read on demand; CLAUDE.md and agent files stay lean with pointers to docs/

**F-03.10: Compilation skills invoked for standard agent types**
- **GIVEN** an operator asks agent-author to create a planner, builder, security, or devops agent
- **WHEN** the agent-author determines the approach
- **THEN** it invokes the corresponding compilation skill (/compiling-planner-agent, etc.) rather than generating the file from scratch; custom agent types are handled by direct generation

---

## Open Questions

- **OQ-01**: [AMBIGUITY] When /defining-specs splits into epics and the operator selects "Spec all — I'll wait," does the skill write all epics sequentially in one session, or does it complete one and prompt for the next?
- **OQ-02**: [EDGE CASE] If specs/glossary.md already exists and the new spec introduces an actor with the same name but different definition, how is the conflict resolved — does the skill prompt the operator, overwrite silently, or append a variant?
- **OQ-03**: [MISSING ACTOR] The /defining-specs skill is described as iterating "until the operator stops the loop" — is there a maximum iteration count or natural termination condition beyond operator intervention?
*(OQ-04 resolved: invalid feature ID → fail and list valid IDs — see F-02.1b below)*
- **OQ-05**: [SCOPE] The agent-author meta-agent is described as guiding creation but also as invoking compilation skills — does it have the ability to run compilation skills directly (via Skill tool), or does it only instruct the operator to run them?

## Assumptions

- **A-01**: [ASSUMPTION] /defining-specs uses the file path convention specs/{source-name}.md where {source-name} is derived from the source document's filename or a slugified title; the exact derivation rule is not specified.
- **A-02**: [ASSUMPTION] The exploratory question category in /defining-specs is designed to surface missing concerns the operator didn't know to ask about; it is only dropped from the round if all 4 refinement questions are ranked higher by criticality.
- **A-03**: [ASSUMPTION] /defining-test-scenarios has access to the Domain Glossary (specs/glossary.md) and reads it before generating any scenarios; it will warn if the glossary is missing but not fail hard.
- **A-04**: [ASSUMPTION] Test scenario files (specs/{name}.test.{FXX}.md) are scoped to a single feature at a time; expanding all features in a spec requires multiple /defining-test-scenarios invocations.
- **A-05**: [ASSUMPTION] The agent-author meta-agent operates interactively and cannot be used in one-shot (-p) mode; discovery questions require operator responses.
- **A-06**: [ASSUMPTION] When agent-author invokes a compilation skill, it uses the Skill tool (same mechanism as a slash command), not a subagent.
- **A-07**: /defining-specs handles inline source documents (pasted text, not a file path) by deriving a slugified filename from the document's heading or first sentence; the operator does not need to provide a name separately.
