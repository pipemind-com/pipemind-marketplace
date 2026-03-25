# Test Scenarios: F-01 — Workflow Orchestration

**Source spec:** specs/spec-driven-development.execution.md
**Scope:** F-01 (all sub-scenarios), SC-01, SC-02, SC-03, SC-08
**Generated:** 2026-03-25
**Status:** DRAFT — requires operator review

## Prerequisites

- The project has a git repository initialized
- The /orchestrating-workflow skill is invokable
- All entity labels are scoped per scenario unless otherwise stated

---

## Phase 1: Pre-Flight

### TS-01.01: Pre-flight passes — all prerequisites present

**Traces to:** F-01.1
**Category:** HAPPY PATH
**Criticality:** BLOCKING

**GIVEN:**
- /orchestrating-workflow is invoked with a feature description
- CLAUDE.md exists in the project root
- .claude/agents/planner.md exists
- .claude/agents/builder.md exists
- A test runner command is configured (discoverable from package.json, Makefile, Cargo.toml, or CLAUDE.md)
- At least one test scenario spec file exists in specs/

**WHEN:**
- The orchestrator performs pre-flight checks

**THEN:**
- The orchestrator proceeds to requirements gathering without reporting any error or halting

---

### TS-01.02: Pre-flight halts — CLAUDE.md missing

**Traces to:** F-01.2
**Category:** FAILURE
**Criticality:** HIGH

**GIVEN:**
- /orchestrating-workflow is invoked
- No CLAUDE.md exists in the project root

**WHEN:**
- The orchestrator performs pre-flight checks

**THEN:**
- The orchestrator halts immediately
- The operator receives a report stating that CLAUDE.md is missing
- The orchestrator does not proceed to decomposition or spawn any agents

---

### TS-01.03: Pre-flight halts — planner agent missing

**Traces to:** F-01.3
**Category:** FAILURE
**Criticality:** HIGH

**GIVEN:**
- CLAUDE.md exists in the project root
- .claude/agents/planner.md does not exist

**WHEN:**
- The orchestrator performs pre-flight checks

**THEN:**
- The orchestrator halts
- The report names planner.md as the missing file
- The report suggests running /compiling-planner-agent
- The orchestrator does not proceed

---

### TS-01.04: Pre-flight halts — builder agent missing

**Traces to:** F-01.4
**Category:** FAILURE
**Criticality:** HIGH

**GIVEN:**
- CLAUDE.md and .claude/agents/planner.md exist
- .claude/agents/builder.md does not exist

**WHEN:**
- The orchestrator performs pre-flight checks

**THEN:**
- The orchestrator halts
- The report names builder.md as the missing file and suggests running /compiling-builder-agent

---

### TS-01.05: Pre-flight halts — test runner not configured

**Traces to:** F-01.4a
**Category:** FAILURE
**Criticality:** HIGH

**GIVEN:**
- CLAUDE.md, planner.md, and builder.md all exist
- No test runner command is discoverable in package.json scripts, Makefile, Cargo.toml, or CLAUDE.md

**WHEN:**
- The orchestrator performs pre-flight checks

**THEN:**
- The orchestrator halts
- The report states that no test runner was found and that the two-wave build cannot proceed without one
- The orchestrator does not proceed to requirements gathering

---

### TS-01.06: Pre-flight halts — no test scenario specs exist

**Traces to:** F-01.4a
**Category:** FAILURE
**Criticality:** HIGH

**GIVEN:**
- CLAUDE.md, agents, and test runner all exist
- No test scenario spec files exist in specs/

**WHEN:**
- The orchestrator performs pre-flight checks

**THEN:**
- The orchestrator halts
- The report states that no test scenario specs were found and suggests running /defining-test-scenarios first

---

### TS-01.07: Pre-flight discovers test runner from package.json

**Traces to:** F-01.4a
**Category:** HAPPY PATH
**Criticality:** HIGH

**GIVEN:**
- A test command is defined in package.json scripts (e.g., "test": "jest")
- No test runner is specified in CLAUDE.md

**WHEN:**
- The orchestrator performs pre-flight checks

**THEN:**
- The orchestrator identifies the test runner from package.json
- The orchestrator proceeds without halting
- The discovered test runner command is available to be passed to Wave 1 builders

---

### TS-01.08: Pre-flight discovers test file naming convention from existing files

**Traces to:** F-01.4a
**Category:** HAPPY PATH
**Criticality:** HIGH

**GIVEN:**
- Existing test files follow a consistent naming pattern (e.g., all end in .test.ts)
- No naming convention is explicitly declared in CLAUDE.md or framework config

**WHEN:**
- The orchestrator performs pre-flight checks

**THEN:**
- The orchestrator identifies the naming convention from the existing test files
- The naming convention is available to be passed to Wave 1 builders

---

### TS-01.09: Pre-flight halts — no feature description provided

**Traces to:** F-01.1 (implicit)
**Category:** FAILURE
**Criticality:** HIGH

**GIVEN:**
- All agent files, test runner, and test scenario specs exist
- /orchestrating-workflow is invoked with no argument (no feature description)

**WHEN:**
- The orchestrator performs pre-flight checks

**THEN:**
- The orchestrator halts
- The report requests a feature description, spec file path, or issue URL

---

## Phase 2: Requirements Gathering

### TS-01.10: Clarification questions asked for ambiguous feature

**Traces to:** F-01.5
**Category:** HAPPY PATH
**Criticality:** HIGH

**GIVEN:**
- Pre-flight passes
- The feature description contains multiple ambiguities about scope boundaries

**WHEN:**
- The orchestrator reaches requirements gathering

**THEN:**
- The orchestrator asks at most 3 clarification questions via AskUserQuestion before proceeding to decomposition
- The orchestrator does not ask more than 3 questions regardless of the number of ambiguities

---

### TS-01.11: Clarification limit — 3 questions maximum enforced

**Traces to:** F-01.5
**Category:** BOUNDARY
**Criticality:** HIGH

**GIVEN:**
- Pre-flight passes
- The feature description contains 5 distinct ambiguities

**WHEN:**
- The orchestrator performs requirements gathering

**THEN:**
- The orchestrator asks exactly 3 questions — not 4, not 5
- The orchestrator proceeds to decomposition after receiving 3 answers (or choosing to proceed without)

---

### TS-01.12: No clarification needed — unambiguous feature

**Traces to:** F-01.5
**Category:** EDGE CASE
**Criticality:** MEDIUM

**GIVEN:**
- Pre-flight passes
- The feature description is specific and self-contained with no ambiguities

**WHEN:**
- The orchestrator reaches requirements gathering

**THEN:**
- The orchestrator proceeds directly to decomposition without presenting any clarification questions to the operator

---

## Phase 3: Decomposition

### TS-01.13: Decomposition produces 2–6 sub-tasks and requests approval

**Traces to:** F-01.6
**Category:** HAPPY PATH
**Criticality:** BLOCKING

**GIVEN:**
- Requirements are gathered for [Feature_Alpha]
- [Feature_Alpha] decomposes into 4 independent sub-tasks

**WHEN:**
- The orchestrator decomposes the feature

**THEN:**
- The orchestrator presents exactly 4 sub-tasks to the operator
- Each sub-task has a title, scope, likely files affected, and declared dependencies
- The presentation explicitly awaits operator approval before any agents are spawned

---

### TS-01.14: Decomposition — minimum boundary of 2 sub-tasks

**Traces to:** F-01.6
**Category:** BOUNDARY
**Criticality:** MEDIUM

**GIVEN:**
- [Feature_Beta] naturally decomposes into exactly 2 sub-tasks

**WHEN:**
- The orchestrator decomposes [Feature_Beta]

**THEN:**
- The orchestrator presents 2 sub-tasks without consolidating them further

---

### TS-01.15: Decomposition — maximum boundary of 6 sub-tasks

**Traces to:** F-01.6
**Category:** BOUNDARY
**Criticality:** HIGH

**GIVEN:**
- [Feature_Gamma] naturally decomposes into exactly 6 sub-tasks

**WHEN:**
- The orchestrator decomposes [Feature_Gamma]

**THEN:**
- The orchestrator presents all 6 sub-tasks without consolidating any

---

### TS-01.16: Decomposition over limit — consolidated to 6

**Traces to:** F-01.7
**Category:** FAILURE
**Criticality:** HIGH

**GIVEN:**
- [Feature_Delta] naturally decomposes into 8 sub-tasks

**WHEN:**
- The orchestrator attempts decomposition

**THEN:**
- The orchestrator consolidates related sub-tasks
- The final presented plan contains no more than 6 sub-tasks
- The rationale for consolidation is included in the presentation

---

### TS-01.17: Decomposition — circular dependency detected and rejected

**Traces to:** F-01.8
**Category:** FAILURE
**Criticality:** HIGH

**GIVEN:**
- [Task_A] is declared as depending on [Task_B]
- [Task_B] is declared as depending on [Task_A]

**WHEN:**
- The orchestrator validates the task graph

**THEN:**
- The orchestrator rejects the circular dependency
- The operator receives a report naming the cycle ([Task_A] → [Task_B] → [Task_A])
- The orchestrator proposes a revised decomposition that resolves the cycle
- No agents are spawned

---

### TS-01.18: Decomposition approval is required before agents spawn

**Traces to:** F-01.6
**Category:** CONSTRAINT VALIDATION
**Criticality:** HIGH

**GIVEN:**
- Decomposition is complete and presented to the operator
- The operator has not yet responded

**WHEN:**
- The orchestrator waits for operator response

**THEN:**
- No planner agents or builder agents are launched until the operator explicitly confirms the decomposition

---

### TS-01.18a: Decomposition rejected — orchestrator proposes revised breakdown

**Traces to:** F-01.6 (implicit)
**Category:** EDGE CASE
**Criticality:** HIGH

**GIVEN:**
- The decomposition is presented to the operator
- The operator rejects the breakdown and requests changes (e.g., different task groupings, different scope boundaries)

**WHEN:**
- The orchestrator receives the rejection

**THEN:**
- The orchestrator produces a revised decomposition reflecting the operator's feedback
- The revised plan is presented to the operator for approval
- No agents are spawned until the operator confirms the revised decomposition

---

## Phase 4: Two-Pass Planning

### TS-01.19: Parallel planner dispatch — all independent sub-tasks in one response

**Traces to:** F-01.9
**Category:** HAPPY PATH
**Criticality:** BLOCKING

**GIVEN:**
- The decomposition is approved with 3 sub-tasks: [Task_A], [Task_B], [Task_C]
- All 3 sub-tasks are independent (no dependencies between them)

**WHEN:**
- The orchestrator dispatches planners for Pass 1

**THEN:**
- All 3 planner agents are launched as simultaneous tool calls in a single response
- The orchestrator does not launch any planner before receiving another's output (no sequential dispatch)

---

### TS-01.20: Planner prompt includes test scenario spec reference

**Traces to:** F-01.9
**Category:** CONSTRAINT VALIDATION
**Criticality:** HIGH

**GIVEN:**
- Test scenario spec files exist in specs/
- The decomposition is approved

**WHEN:**
- The orchestrator composes each planner's prompt

**THEN:**
- Each planner prompt includes the relevant test scenario spec file path(s) for that sub-task's scope

---

### TS-01.21: Dependent planner waits for predecessor

**Traces to:** F-01.9
**Category:** EDGE CASE
**Criticality:** HIGH

**GIVEN:**
- [Task_B] depends on [Task_A] in the approved task graph

**WHEN:**
- The orchestrator dispatches planners

**THEN:**
- [Task_A]'s planner is dispatched first
- [Task_B]'s planner is not dispatched until [Task_A]'s planner has reported completion

---

### TS-01.22: Reconciliation detects and resolves file overlap

**Traces to:** F-01.10
**Category:** FAILURE
**Criticality:** HIGH

**GIVEN:**
- [Planner_A]'s output intends to modify [File_X] at overlapping locations
- [Planner_B]'s output also intends to modify [File_X] at overlapping locations

**WHEN:**
- The orchestrator performs Pass 2 reconciliation

**THEN:**
- The orchestrator identifies the conflict
- The orchestrator determines which sub-task owns [File_X] and adjusts the other sub-task's scope
- The resolution is documented before Wave 1 begins

---

### TS-01.23: Reconciliation — no conflict when file access is non-overlapping

**Traces to:** F-01.10
**Category:** EDGE CASE
**Criticality:** MEDIUM

**GIVEN:**
- [Planner_A] intends to add content to [File_X]
- [Planner_B] also intends to add content to [File_X], but at a non-overlapping location

**WHEN:**
- The orchestrator performs reconciliation

**THEN:**
- The orchestrator notes that both plans touch [File_X] but determines no dependency adjustment is needed
- Both sub-tasks proceed to Wave 1 without serialization

---

## Phase 5: Wave 1 — Test Building

### TS-01.24: Wave 1 dispatch — all test builders launched simultaneously

**Traces to:** F-01.11
**Category:** HAPPY PATH
**Criticality:** BLOCKING

**GIVEN:**
- The task graph is reconciled with 3 sub-tasks: [Task_A], [Task_B], [Task_C]
- [Task_B] depends on [Task_A] in the task graph
- Wave 1 begins

**WHEN:**
- The orchestrator dispatches Wave 1 test builders

**THEN:**
- All 3 test builders ([Builder_A], [Builder_B], [Builder_C]) are launched as simultaneous tool calls in a single response
- [Builder_B] is launched in the same response as [Builder_A] — the dependency graph is not enforced in Wave 1

---

### TS-01.25: Wave 1 builder prompt — planner output and test-only instruction

**Traces to:** F-01.11
**Category:** CONSTRAINT VALIDATION
**Criticality:** HIGH

**GIVEN:**
- Wave 1 is dispatching test builders
- [Task_Alpha]'s planner output is available

**WHEN:**
- The orchestrator composes the prompt for [Task_Alpha]'s Wave 1 builder

**THEN:**
- The prompt includes [Task_Alpha]'s planner output as context
- The prompt includes an explicit instruction to write tests only — no implementation code

---

### TS-01.26: Wave 1 scope — only test artifacts and type stubs produced

**Traces to:** F-01.12
**Category:** CONSTRAINT VALIDATION
**Criticality:** HIGH

**GIVEN:**
- [Builder_Alpha] completes Wave 1 for [Task_Alpha]

**WHEN:**
- The orchestrator reviews [Builder_Alpha]'s output

**THEN:**
- All created or modified files are test files (following the project naming convention), fixtures, test helpers, or minimal type stub files
- No production source files containing implementation logic are created or modified

---

### TS-01.27: Wave 1 scope — type stubs with signatures only are accepted

**Traces to:** F-01.12
**Category:** EDGE CASE
**Criticality:** HIGH

**GIVEN:**
- [Builder_Alpha] creates [Stub_File] containing only interface and type definitions with no implementation logic

**WHEN:**
- The orchestrator reviews Wave 1 output

**THEN:**
- [Stub_File] is accepted as valid Wave 1 output

---

### TS-01.28: Wave 1 scope — builder self-enforces no implementation logic in stubs

**Traces to:** F-01.12
**Category:** CONSTRAINT VALIDATION
**Criticality:** HIGH

**GIVEN:**
- [Builder_Alpha] is producing type stub files during Wave 1

**WHEN:**
- [Builder_Alpha] creates [Stub_File]

**THEN:**
- [Stub_File] contains only type signatures and interface definitions
- [Builder_Alpha] does not add any function bodies or executable implementation logic to [Stub_File]
- If implementation logic were present in [Stub_File], the red-phase check would detect unexpectedly passing tests and the builder would revise accordingly

**NOTES:** Scope enforcement is self-imposed by the builder per its Wave 1 instructions. The orchestrator does not independently inspect stub file contents.

---

### TS-01.29: Wave 1 quality gate — /reviewing-code-quality run on test output

**Traces to:** F-01.12a
**Category:** CONSTRAINT VALIDATION
**Criticality:** HIGH

**GIVEN:**
- [Builder_Alpha] has produced test files for [Task_Alpha] and passed the spec coverage check

**WHEN:**
- The builder executes its quality gate

**THEN:**
- The builder runs /reviewing-code-quality on its test files
- If Warning or Defect findings are reported, the builder addresses them before proceeding to the red-phase check

---

### TS-01.30: Wave 1 quality gate — spec scenario coverage verified

**Traces to:** F-01.12a
**Category:** CONSTRAINT VALIDATION
**Criticality:** HIGH

**GIVEN:**
- [Builder_Alpha] has produced tests for [Task_Alpha]
- The planner output for [Task_Alpha] references [Spec_File_X] as the relevant test scenario spec

**WHEN:**
- The builder checks scenario coverage

**THEN:**
- The builder compares its tests against the scenarios in [Spec_File_X]
- If any scenarios lack test coverage, the builder writes additional tests before proceeding to the red-phase check

---

### TS-01.31: Wave 1 quality gate passes — builder proceeds to red-phase check

**Traces to:** F-01.12a
**Category:** HAPPY PATH
**Criticality:** HIGH

**GIVEN:**
- [Builder_Alpha]'s tests cover all scenarios in the referenced spec
- /reviewing-code-quality reports no Warning or Defect findings on the test files

**WHEN:**
- The builder evaluates its quality gate

**THEN:**
- The builder proceeds to the red-phase check without modifying any test files

---

### TS-01.32: Wave 1 red phase — all tests fail as expected

**Traces to:** F-01.13
**Category:** HAPPY PATH
**Criticality:** BLOCKING

**GIVEN:**
- [Builder_Alpha] has produced tests for [Task_Alpha] and passed the quality gate
- No implementation code exists for [Task_Alpha]

**WHEN:**
- [Builder_Alpha] runs its tests

**THEN:**
- All tests fail
- The builder confirms the red phase and reports successful completion to the orchestrator

---

### TS-01.33: Wave 1 red phase — unexpected passing test rewritten

**Traces to:** F-01.13
**Category:** EDGE CASE
**Criticality:** HIGH

**GIVEN:**
- [Builder_Alpha] runs its tests
- [Test_X] passes unexpectedly because it tests already-implemented behavior

**WHEN:**
- The builder diagnoses [Test_X]

**THEN:**
- The builder rewrites [Test_X] to target unimplemented behavior
- After the rewrite, [Test_X] fails
- The builder does not report success until all tests (including the rewritten [Test_X]) fail

---

### TS-01.34: Wave 1 red phase — trivial passing test deleted

**Traces to:** F-01.13
**Category:** EDGE CASE
**Criticality:** HIGH

**GIVEN:**
- [Builder_Alpha] runs its tests
- [Test_Y] passes because it contains a no-op or trivially true assertion

**WHEN:**
- The builder diagnoses [Test_Y]

**THEN:**
- The builder deletes [Test_Y] and notes the deletion
- The builder does not report success until all remaining tests fail

---

### TS-01.35: Wave 1 red phase — builder does not report success with any passing test

**Traces to:** F-01.13
**Category:** CONSTRAINT VALIDATION
**Criticality:** HIGH

**GIVEN:**
- [Builder_Alpha] runs 5 tests
- 1 test passes, 4 tests fail

**WHEN:**
- The builder evaluates red-phase status

**THEN:**
- The builder does not report success to the orchestrator
- The builder continues iterating (rewriting or deleting the passing test) until all tests fail or natural context limits are hit

---

### TS-01.36: Wave 1 — builder produces zero test files (failure)

**Traces to:** F-01.14 (implicit)
**Category:** FAILURE
**Criticality:** HIGH

**GIVEN:**
- [Builder_Alpha] reports completion but has produced no test files or type stubs

**WHEN:**
- The orchestrator validates [Builder_Alpha]'s output

**THEN:**
- The orchestrator treats this as a Wave 1 failure for [Task_Alpha]
- The orchestrator follows the Wave 1 failure path: asks the operator with a 30-second timeout

---

### TS-01.37: Wave 1 transition — orchestrator waits for all builders before Wave 2

**Traces to:** F-01.14
**Category:** HAPPY PATH
**Criticality:** BLOCKING

**GIVEN:**
- 3 test builders are running: [Builder_A], [Builder_B], [Builder_C]
- [Builder_A] reports successful completion
- [Builder_B] and [Builder_C] are still running

**WHEN:**
- The orchestrator receives [Builder_A]'s success

**THEN:**
- The orchestrator does not begin Wave 2
- The orchestrator continues waiting for [Builder_B] and [Builder_C]

---

### TS-01.38: Wave 1 transition — Wave 2 begins after all builders report

**Traces to:** F-01.14
**Category:** HAPPY PATH
**Criticality:** BLOCKING

**GIVEN:**
- All 3 test builders have reported successful completion (tests written, quality gate passed, red phase confirmed)

**WHEN:**
- The orchestrator collects the final builder result

**THEN:**
- Wave 2 begins immediately after the last builder reports

---

### TS-01.39: Wave 1 failure — operator asked per sub-task with 30-second timeout

**Traces to:** F-01.14
**Category:** FAILURE
**Criticality:** HIGH

**GIVEN:**
- [Builder_Fail] reports failure (unable to produce valid failing tests)
- [Builder_OK_1] and [Builder_OK_2] have succeeded

**WHEN:**
- The orchestrator receives [Builder_Fail]'s failure

**THEN:**
- The orchestrator asks the operator specifically about [Task_Fail]: skip it in Wave 2 or build without tests
- Wave 2 does not begin until the operator responds or the 30-second timeout expires

---

### TS-01.40: Wave 1 failure — 30-second timeout defaults to skip

**Traces to:** F-01.14
**Category:** EDGE CASE
**Criticality:** HIGH

**GIVEN:**
- [Builder_Fail] has failed
- The orchestrator has asked the operator about [Task_Fail]
- 30 seconds pass without an operator response

**WHEN:**
- The timeout expires

**THEN:**
- The orchestrator defaults to skipping [Task_Fail] in Wave 2
- Wave 2 proceeds for sub-tasks with successful Wave 1 results
- The skip is noted in the final completion report

---

### TS-01.41: Wave 1 failure — operator explicitly chooses build without tests

**Traces to:** F-01.14
**Category:** EDGE CASE
**Criticality:** MEDIUM

**GIVEN:**
- [Builder_Fail] has failed
- The operator responds within 30 seconds choosing to build without tests for [Task_Fail]

**WHEN:**
- The orchestrator receives the operator's response

**THEN:**
- [Task_Fail] is included in Wave 2 with no test file paths in its code builder's prompt
- Wave 2 proceeds

---

## Phase 6: Wave 2 — Code Building

### TS-01.42: Wave 2 dispatch — unblocked code builders launched in parallel

**Traces to:** F-01.15
**Category:** HAPPY PATH
**Criticality:** BLOCKING

**GIVEN:**
- Wave 1 is complete
- [Task_A], [Task_B], and [Task_C] have no dependencies between them

**WHEN:**
- Wave 2 begins

**THEN:**
- All 3 code builders are launched as simultaneous tool calls in a single response

---

### TS-01.43: Wave 2 dispatch — blocked code builder waits for dependency

**Traces to:** F-01.17
**Category:** HAPPY PATH
**Criticality:** HIGH

**GIVEN:**
- Wave 1 is complete
- [Task_B] depends on [Task_A]
- Wave 2 begins

**WHEN:**
- The orchestrator dispatches Wave 2 code builders

**THEN:**
- [Task_A]'s code builder is launched immediately
- [Task_B]'s code builder is not launched until [Task_A]'s code builder reports completion

---

### TS-01.44: Wave 2 dispatch — dependency resolved unblocks waiting builder

**Traces to:** F-01.17
**Category:** HAPPY PATH
**Criticality:** HIGH

**GIVEN:**
- [Task_B] was waiting on [Task_A] in Wave 2
- [Task_A]'s code builder reports successful completion

**WHEN:**
- The orchestrator receives [Task_A]'s completion

**THEN:**
- [Task_B]'s code builder is launched in the next response immediately following [Task_A]'s completion

---

### TS-01.45: Wave 2 context — code builder receives test file paths

**Traces to:** F-01.16
**Category:** CONSTRAINT VALIDATION
**Criticality:** HIGH

**GIVEN:**
- Wave 1 produced test files for [Task_Alpha]
- [Task_Alpha]'s code builder is launched in Wave 2

**WHEN:**
- The orchestrator composes the builder's prompt

**THEN:**
- The prompt includes the file paths of [Task_Alpha]'s Wave 1 test files
- The test file content is not inlined in the prompt — only paths are provided

---

### TS-01.46: Wave 2 context — no test paths when Wave 1 failed and operator chose build without tests

**Traces to:** F-01.16
**Category:** EDGE CASE
**Criticality:** MEDIUM

**GIVEN:**
- [Task_Alpha]'s Wave 1 builder failed
- The operator chose to build without tests for [Task_Alpha]
- [Task_Alpha]'s Wave 2 code builder is launched

**WHEN:**
- The orchestrator composes the builder's prompt

**THEN:**
- The prompt includes no test file paths
- The builder receives planner output and feature context only

---

### TS-01.47: Wave 2 convergence — builder iterates until all tests pass

**Traces to:** F-01.18
**Category:** HAPPY PATH
**Criticality:** BLOCKING

**GIVEN:**
- [Task_Alpha]'s code builder runs
- [Test_X] fails on the first implementation attempt

**WHEN:**
- The builder detects the failure

**THEN:**
- The builder diagnoses the failure, adjusts implementation, and re-runs tests
- This cycle repeats internally until all Wave 1 tests for [Task_Alpha] pass
- The builder does not report completion to the orchestrator until all tests pass

---

### TS-01.48: Wave 2 convergence — no orchestrator retry limit

**Traces to:** F-01.18
**Category:** CONSTRAINT VALIDATION
**Criticality:** HIGH

**GIVEN:**
- [Task_Alpha]'s code builder is iterating on a test failure

**WHEN:**
- The orchestrator monitors the builder's progress

**THEN:**
- The orchestrator does not impose a retry count or iteration limit on the builder
- The builder runs until it converges or hits Claude Code's natural context limits

---

### TS-01.49: Wave 2 failure — builder reports to orchestrator after exhausting context

**Traces to:** F-01.18
**Category:** FAILURE
**Criticality:** HIGH

**GIVEN:**
- [Task_Alpha]'s code builder has exhausted its context while attempting to make [Test_X] pass

**WHEN:**
- The builder reports failure to the orchestrator

**THEN:**
- The orchestrator escalates to the operator with the failure reason and the name of the failing test
- The operator decides how to proceed (retry with guidance, skip, abort)

---

### TS-01.50: Wave 2 spec gate — all spec requirements verified before declaring done

**Traces to:** F-01.18a
**Category:** HAPPY PATH
**Criticality:** HIGH

**GIVEN:**
- [Task_Alpha]'s code builder has made all Wave 1 tests pass
- The planner output references behavioral spec scenarios for [Task_Alpha]

**WHEN:**
- The builder performs the spec-implemented gate

**THEN:**
- The builder reviews all behavioral spec scenarios referenced in its planner output
- The builder verifies that every specified behavior has been implemented
- If all requirements are covered and all tests pass, the builder declares completion

---

### TS-01.51: Wave 2 spec gate — gap found, builder executes TDD micro-cycle

**Traces to:** F-01.18a
**Category:** EDGE CASE
**Criticality:** HIGH

**GIVEN:**
- [Task_Alpha]'s code builder has made all Wave 1 tests pass
- The spec gate identifies [Scenario_X] as a spec requirement that is neither tested nor implemented

**WHEN:**
- The builder addresses the gap

**THEN:**
- The builder writes a test for [Scenario_X]
- The builder confirms the test fails (red phase)
- The builder implements the code to satisfy [Scenario_X]
- The builder confirms the test passes
- Only after this TDD micro-cycle does the builder declare completion

---

### TS-01.52: Wave 2 spec gate — builder does not declare completion with uncovered spec requirement

**Traces to:** F-01.18a
**Category:** CONSTRAINT VALIDATION
**Criticality:** HIGH

**GIVEN:**
- [Task_Alpha]'s code builder has made all Wave 1 tests pass
- The spec gate identifies one spec requirement that is uncovered

**WHEN:**
- The builder evaluates completion status

**THEN:**
- The builder does not declare completion
- The builder addresses the gap before declaring done

---

## Phase 7: Final Verification & Completion Report

### TS-01.53: Final verification — full test suite run after all Wave 2 complete

**Traces to:** F-01.19
**Category:** HAPPY PATH
**Criticality:** BLOCKING

**GIVEN:**
- All code builders have reported completion or failure

**WHEN:**
- The orchestrator performs final verification

**THEN:**
- The orchestrator runs the project's full test suite
- The orchestrator does not skip this step even if all individual builders reported their tests passing

---

### TS-01.54: Final verification — all Wave 1 tests pass (green)

**Traces to:** F-01.19
**Category:** HAPPY PATH
**Criticality:** BLOCKING

**GIVEN:**
- All Wave 2 code builders succeeded
- No cross-contamination occurred

**WHEN:**
- The final test suite runs

**THEN:**
- All Wave 1 tests corresponding to completed sub-tasks pass

---

### TS-01.55: Final verification — cross-contamination detected and reported

**Traces to:** F-01.19
**Category:** FAILURE
**Criticality:** HIGH

**GIVEN:**
- [Builder_B]'s code changes caused [Task_A]'s Wave 1 tests to fail

**WHEN:**
- The final test suite runs

**THEN:**
- The orchestrator identifies the cross-contamination
- The orchestrator reports which sub-task's tests broke ([Task_A]) and which builder likely caused it ([Builder_B])
- The orchestrator does not auto-relaunch any builder
- The operator receives the report for manual resolution

---

### TS-01.56: Final verification — skipped sub-tasks excluded from green requirement

**Traces to:** F-01.19
**Category:** EDGE CASE
**Criticality:** MEDIUM

**GIVEN:**
- [Task_Alpha] was skipped in Wave 2 (Wave 1 failed, operator chose skip)
- All other sub-tasks have passing Wave 1 tests

**WHEN:**
- Final verification runs

**THEN:**
- Only tests for completed sub-tasks are evaluated for green status
- The absence of [Task_Alpha]'s tests does not cause final verification to report failure

---

### TS-01.57: Completion report — rolled-up status for each sub-task

**Traces to:** F-01.20
**Category:** HAPPY PATH
**Criticality:** HIGH

**GIVEN:**
- Final verification is complete

**WHEN:**
- The orchestrator produces the completion report

**THEN:**
- The report lists each sub-task with: status (completed / failed / skipped), files modified, and test results
- The report does not break down per-wave details — a single rolled-up status is shown per sub-task

---

### TS-01.58: Completion report — outstanding issues listed

**Traces to:** F-01.20
**Category:** EDGE CASE
**Criticality:** MEDIUM

**GIVEN:**
- One sub-task is marked failed
- Final verification detected 2 cross-contamination failures

**WHEN:**
- The completion report is produced

**THEN:**
- The report includes an outstanding issues section
- The failed sub-task and both cross-contamination failures are listed with context

---

### TS-01.59: Completion report — next steps suggested

**Traces to:** F-01.20
**Category:** HAPPY PATH
**Criticality:** LOW

**GIVEN:**
- The completion report is produced

**WHEN:**
- The operator reads the report

**THEN:**
- The report explicitly suggests running /git-commit-changes as a next step
- The report explicitly suggests running /conducting-post-mortem as a next step

---

## System Constraint Validations

### TS-01.60: SC-01 — orchestrator never modifies production files directly

**Traces to:** F-01.6 (implicit — SC-01)
**Category:** CONSTRAINT VALIDATION
**Criticality:** HIGH

**GIVEN:**
- The orchestrator is in any execution phase

**WHEN:**
- A production file needs to be created or modified to advance the workflow

**THEN:**
- The orchestrator delegates the change to a builder subagent
- The orchestrator itself does not create or modify any production source file

---

### TS-01.61: SC-02 — builder and planner use correct invocation syntax

**Traces to:** F-01.9, F-01.11, F-01.15
**Category:** CONSTRAINT VALIDATION
**Criticality:** HIGH

**GIVEN:**
- The orchestrator is spawning a planner or builder subagent

**WHEN:**
- The subagent's prompt is composed

**THEN:**
- Planner prompts begin with `@"planner (agent)"`
- Builder prompts begin with `@"builder (agent)"`
- No other reference syntax or subagent_type value is used

---

### TS-01.62: SC-03 — unblocked builders launched simultaneously, not serially

**Traces to:** F-01.11, F-01.15
**Category:** CONSTRAINT VALIDATION
**Criticality:** HIGH

**GIVEN:**
- 3 unblocked sub-tasks exist (in Wave 1 or Wave 2)

**WHEN:**
- The orchestrator dispatches builders

**THEN:**
- All 3 builders are launched as simultaneous tool calls in a single response
- No builder waits for another's completion unless a declared dependency exists

---

### TS-01.63: SC-08 — Wave 1 cannot be skipped even when operator requests it

**Traces to:** F-01.11
**Category:** CONSTRAINT VALIDATION
**Criticality:** HIGH

**GIVEN:**
- The operator's feature request explicitly states "skip tests" or "skip Wave 1"

**WHEN:**
- The orchestrator interprets the request

**THEN:**
- The orchestrator does not skip Wave 1
- The orchestrator proceeds with the two-wave model regardless of the instruction

---

### TS-01.64: SC-08 — Wave 2 does not begin before Wave 1 is fully collected

**Traces to:** F-01.14
**Category:** CONSTRAINT VALIDATION
**Criticality:** HIGH

**GIVEN:**
- Wave 1 is in progress with at least one builder still running

**WHEN:**
- The orchestrator considers starting any Wave 2 code builder

**THEN:**
- No Wave 2 code builder is launched until all Wave 1 results are collected (success or escalated failure for each sub-task)

---

### TS-01.65: A-07 — Wave 1 dependency graph not enforced

**Traces to:** F-01.11
**Category:** CONSTRAINT VALIDATION
**Criticality:** MEDIUM

**GIVEN:**
- [Task_B] has a declared dependency on [Task_A] in the task graph

**WHEN:**
- Wave 1 dispatches test builders

**THEN:**
- [Task_B]'s test builder is launched in the same response as [Task_A]'s test builder
- The dependency is not enforced during Wave 1

**NOTES:** Depends on assumption A-07. If revised (dependency ordering added to Wave 1), this scenario must be regenerated.

---

### TS-01.66: A-09 — planners produce single unified plan per sub-task

**Traces to:** F-01.9
**Category:** CONSTRAINT VALIDATION
**Criticality:** MEDIUM

**GIVEN:**
- The decomposition is approved and planners are dispatched

**WHEN:**
- Planners produce output

**THEN:**
- Each planner produces one unified plan per sub-task
- No separate test plan and code plan are produced
- The orchestrator uses the single plan to instruct both Wave 1 and Wave 2 builders differently via prompt instructions

**NOTES:** Depends on assumption A-09. If revised (separate planning phases introduced), this scenario must be regenerated.

---

### TS-01.67: Cross-feature — Wave 1 quality gate requires test scenario spec accessibility

**Traces to:** F-01.12a × F-01.4a
**Category:** CONSTRAINT VALIDATION | CROSS-FEATURE
**Criticality:** HIGH

**GIVEN:**
- Wave 1 builders are launched
- The test scenario spec file for the feature exists in specs/ (confirmed at pre-flight)

**WHEN:**
- A test builder runs its quality gate

**THEN:**
- The test scenario spec file is accessible and readable by the builder
- The builder can compare its test output against the spec scenarios to identify coverage gaps

---

### TS-01.68: Cross-feature — completion report references /git-commit-changes

**Traces to:** F-01.20 × F-04
**Category:** HAPPY PATH | CROSS-FEATURE
**Criticality:** LOW

**GIVEN:**
- Orchestration completes with at least one completed sub-task

**WHEN:**
- The completion report is presented

**THEN:**
- The report explicitly names /git-commit-changes as a suggested next step

---

### TS-01.70: Session interruption — operator must restart orchestration

**Traces to:** F-01.1 (implicit — A-06)
**Category:** EDGE CASE
**Criticality:** MEDIUM

**GIVEN:**
- The orchestrator is mid-execution (e.g., between Wave 1 and Wave 2)
- The Claude Code session ends unexpectedly

**WHEN:**
- The operator attempts to resume by re-invoking /orchestrating-workflow

**THEN:**
- The orchestrator begins from the start (pre-flight checks, requirements gathering)
- No automatic recovery or resumption from Wave 1 test artifacts occurs
- The operator is not shown a partial state from the prior session

**NOTES:** Depends on assumption A-06 (task state is ephemeral to the session). If session-persistent task state is added, this scenario must be regenerated.

---

### TS-01.69: Cross-feature — completion report references /conducting-post-mortem

**Traces to:** F-01.20 × F-05
**Category:** HAPPY PATH | CROSS-FEATURE
**Criticality:** LOW

**GIVEN:**
- The completion report is presented

**WHEN:**
- The operator reads the report

**THEN:**
- The report explicitly names /conducting-post-mortem as a suggested next step

---

## Coverage Summary

- **F-01.1** → TS-01.01 — Happy Path
- **F-01.2** → TS-01.02 — Failure
- **F-01.3** → TS-01.03 — Failure
- **F-01.4** → TS-01.04 — Failure
- **F-01.4a** → TS-01.05, TS-01.06, TS-01.07, TS-01.08 — Failure, Failure, Happy Path, Happy Path
- **F-01.1 (implicit)** → TS-01.09 — Failure (no feature description)
- **F-01.5** → TS-01.10, TS-01.11, TS-01.12 — Happy Path, Boundary, Edge Case
- **F-01.6** → TS-01.13, TS-01.14, TS-01.15, TS-01.18, TS-01.18a — Happy Path, Boundary, Boundary, Constraint Validation, Edge Case (rejection)
- **F-01.7** → TS-01.16 — Failure
- **F-01.8** → TS-01.17 — Failure
- **F-01.9** → TS-01.19, TS-01.20, TS-01.21 — Happy Path, Constraint Validation, Edge Case
- **F-01.10** → TS-01.22, TS-01.23 — Failure, Edge Case
- **F-01.11** → TS-01.24, TS-01.25 — Happy Path, Constraint Validation
- **F-01.12** → TS-01.26, TS-01.27, TS-01.28 — Constraint Validation, Edge Case, Failure
- **F-01.12a** → TS-01.29, TS-01.30, TS-01.31 — Constraint Validation, Constraint Validation, Happy Path
- **F-01.13** → TS-01.32, TS-01.33, TS-01.34, TS-01.35 — Happy Path, Edge Case, Edge Case, Constraint Validation
- **F-01.14** → TS-01.36, TS-01.37, TS-01.38, TS-01.39, TS-01.40, TS-01.41 — Failure, Happy Path, Happy Path, Failure, Edge Case, Edge Case
- **F-01.15** → TS-01.42 — Happy Path
- **F-01.16** → TS-01.45, TS-01.46 — Constraint Validation, Edge Case
- **F-01.17** → TS-01.43, TS-01.44 — Happy Path, Happy Path
- **F-01.18** → TS-01.47, TS-01.48, TS-01.49 — Happy Path, Constraint Validation, Failure
- **F-01.18a** → TS-01.50, TS-01.51, TS-01.52 — Happy Path, Edge Case, Constraint Validation
- **F-01.19** → TS-01.53, TS-01.54, TS-01.55, TS-01.56 — Happy Path, Happy Path, Failure, Edge Case
- **F-01.20** → TS-01.57, TS-01.58, TS-01.59 — Happy Path, Edge Case, Happy Path
- **SC-01** → TS-01.60 — Constraint Validation
- **SC-02** → TS-01.61 — Constraint Validation
- **SC-03** → TS-01.62 — Constraint Validation
- **SC-08** → TS-01.63, TS-01.64 — Constraint Validation, Constraint Validation
- **A-07** → TS-01.65 — Constraint Validation
- **A-06** → TS-01.70 — Edge Case (session interruption)
- **A-09** → TS-01.66 — Constraint Validation
- **F-01.12a × F-01.4a** → TS-01.67 — Cross-Feature, Constraint Validation
- **F-01.20 × F-04** → TS-01.68 — Cross-Feature, Happy Path
- **F-01.20 × F-05** → TS-01.69 — Cross-Feature, Happy Path

**Total spec scenarios in scope:** 24 (F-01.1 through F-01.20 including F-01.4a, F-01.12a, F-01.18a)
**Total test scenarios generated:** 71
**Expansion ratio:** 3.0×

### Gaps

- F-01.5: No scenario covers the case where the operator declines to answer clarification questions (the spec says "proceed with best-judgment defaults") — this is an implicit behavior that could be specced more precisely.
- F-01.18: No scenario covers the case where a Wave 2 code builder is blocked (not failing, but blocked on an external dependency). The spec's blocking handler is addressed in the skill itself but not explicitly in the F-01 spec scenarios.

### Glossary Gaps

- *(resolved)* — "Test Builder," "Code Builder," and "Test Scenario Spec File" have been added to specs/glossary.md.
