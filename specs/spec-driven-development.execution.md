# Spec: pm-workflow — Development Execution & Quality
**Source:** plugins/pm-workflow/ (brownfield reverse-engineering)
**Epic:** E-D
**Glossary:** specs/glossary.md
**Generated:** 2026-03-22
**Status:** DRAFT — requires operator review

---

## System Constraints

- **SC-01**: The orchestrator skill never writes or modifies application code; all production changes flow exclusively through builder subagents.
- **SC-02**: Builder subagents must be invoked using `@"builder (agent)"` reference syntax, not via a named subagent_type; planner subagents use `@"planner (agent)"` similarly.
- **SC-03**: Multiple unblocked builders must be launched as a single response (parallel tool calls); launching them sequentially is a behavioral defect.
- **SC-04**: /reviewing-code-quality is a diagnostic tool — it produces findings, never rewrites.
- **SC-05**: /stress-testing generates tests that aim to find failures, not confirm correctness; 100+ random cases is the minimum threshold.
- **SC-06**: /git-commit-changes never includes Co-Authored-By lines, never amends existing commits, and never pushes to remote.
- **SC-07**: /conducting-post-mortem is read-only — it proposes CLAUDE.md changes but does not apply them.

---

## F-01: Workflow Orchestration | MUST

**F-01.1: Pre-flight — all prerequisites present (happy path)**
- **GIVEN** an operator invokes /orchestrating-workflow with a feature description, and CLAUDE.md, .claude/agents/planner.md, and .claude/agents/builder.md all exist
- **WHEN** the skill begins execution
- **THEN** the skill proceeds to requirements gathering without error

**F-01.2: Pre-flight — CLAUDE.md missing (failure)**
- **GIVEN** an operator invokes /orchestrating-workflow but no CLAUDE.md exists in the project root
- **WHEN** the skill performs pre-flight checks
- **THEN** the skill halts immediately and reports that CLAUDE.md is missing; it does not proceed to decomposition

**F-01.3: Pre-flight — planner agent missing (failure)**
- **GIVEN** CLAUDE.md exists but .claude/agents/planner.md does not exist
- **WHEN** the skill performs pre-flight checks
- **THEN** the skill halts and reports the missing planner agent with a suggestion to run /compiling-planner-agent first

**F-01.4: Pre-flight — builder agent missing (failure)**
- **GIVEN** CLAUDE.md and planner.md exist but .claude/agents/builder.md does not exist
- **WHEN** the skill performs pre-flight checks
- **THEN** the skill halts and reports the missing builder agent with a suggestion to run /compiling-builder-agent first

**F-01.5: Requirements gathering — clarification questions**
- **GIVEN** a feature description is provided but contains ambiguities about scope
- **WHEN** the skill reaches the requirements gathering phase
- **THEN** the skill asks at most 3 clarification questions via AskUserQuestion before proceeding to decomposition

**F-01.6: Decomposition — valid breakdown presented for approval**
- **GIVEN** requirements are gathered and the feature is understood
- **WHEN** the skill decomposes the feature
- **THEN** it produces 2-6 independent sub-tasks, each with a title, scope, likely files affected, and declared dependencies; the decomposition is presented to the operator for approval before any agents are spawned

**F-01.7: Decomposition — more than 6 sub-tasks attempted (constraint violation)**
- **GIVEN** the feature naturally decomposes into more than 6 sub-tasks
- **WHEN** the skill attempts decomposition
- **THEN** the skill consolidates related sub-tasks to stay within the 2-6 range and presents the consolidated plan; it does not proceed with more than 6 sub-tasks

**F-01.8: Decomposition — circular dependency detected**
- **GIVEN** a proposed decomposition creates a circular dependency (A depends on B, B depends on A)
- **WHEN** the skill validates the task graph
- **THEN** the skill rejects the circular dependency, reports it to the operator, and proposes a revised decomposition that resolves the cycle

**F-01.9: Two-pass planning — parallel planner dispatch**
- **GIVEN** the decomposition is approved and has independent sub-tasks
- **WHEN** the skill dispatches planners for Pass 1
- **THEN** all independent planner subagents are launched as simultaneous tool calls in a single response; the skill waits for all to complete before proceeding to reconciliation

**F-01.10: Two-pass planning — reconciliation detects file overlap**
- **GIVEN** two planner outputs both intend to modify the same file
- **WHEN** the skill performs Pass 2 reconciliation
- **THEN** the skill identifies the conflict, determines which sub-task should own the file, adjusts the other sub-task's scope accordingly, and notes the resolution before building

**F-01.11: Parallel building — all unblocked builders launched together**
- **GIVEN** the task graph has multiple sub-tasks with no unresolved dependencies
- **WHEN** the skill launches builders
- **THEN** all unblocked builders are dispatched as simultaneous tool calls in a single response

**F-01.12: Parallel building — blocked sub-task waits for dependency**
- **GIVEN** sub-task B depends on sub-task A, and A has not yet completed
- **WHEN** the skill considers launching B
- **THEN** B is not launched until A's builder reports completion; the skill continues with other unblocked tasks in the meantime

**F-01.13: Partial builder completion — auto-retry once**
- **GIVEN** a builder subagent reports that some tests pass and some fail (partial completion)
- **WHEN** the orchestrator receives the result
- **THEN** it re-launches the builder for that sub-task exactly once with a note about the specific test failures; if the retry also reports partial or full failure, the orchestrator marks the sub-task as failed and escalates to the operator before proceeding

**F-01.14: Completion report**
- **GIVEN** all builders have reported completion or failure
- **WHEN** the skill produces its final output
- **THEN** it presents a summary of sub-tasks (status, files modified, test results), lists any outstanding issues, and suggests invoking /git-commit-changes and /conducting-post-mortem as next steps

---

## F-02: Code Quality Review | MUST

**Requires:** N/A (standalone utility, also invoked by builder agents as quality gate)

**F-02.1: Review submitted code (happy path — no defects)**
- **GIVEN** an operator submits a code file, snippet, or directory for review
- **WHEN** /reviewing-code-quality processes the input
- **THEN** it evaluates the code across all 6 axes (purity/state management, testability/modularity, abstraction fitness, readability/structure, documentation quality, robustness/correctness) and produces a report; the Strengths section is always present regardless of how many issues are found

**F-02.2: Defect found — concrete location reference required**
- **GIVEN** a defect is identified during review
- **WHEN** the finding is reported
- **THEN** the finding references a concrete location (file path and/or line context) and describes exactly one issue; it does not bundle multiple issues under one finding

**F-02.3: Advisory finding — no rewrite provided**
- **GIVEN** the review identifies an advisory-level improvement
- **WHEN** the finding is reported
- **THEN** the skill provides the minimum code necessary to illustrate the suggestion (if code is needed at all); it does not rewrite or refactor the surrounding code

**F-02.4: No clarifying questions before reviewing**
- **GIVEN** a review request is submitted with ambiguous scope
- **WHEN** the skill begins
- **THEN** it makes reasonable assumptions about language, context, and intent, states those assumptions in the report, and proceeds immediately — it never asks clarifying questions before starting

**F-02.5: Language detection**
- **GIVEN** the operator does not specify the programming language
- **WHEN** the skill reviews the code
- **THEN** it infers the language from file extension, syntax, or idioms; reviews against that language's ecosystem conventions; and notes the detected language in assumptions

**F-02.6: Review is proportional to scope**
- **GIVEN** a small utility function (under 30 lines) is submitted for review
- **WHEN** findings are generated
- **THEN** the severity calibration reflects the function's limited scope; issues that would be defects in a payment service may be advisories in a utility, and the report does not apply payment-system rigor to a trivial helper

**F-02.7: Quality gate invocation by builder agent**
- **GIVEN** a builder agent has completed implementation and is about to declare work done
- **WHEN** the builder invokes /reviewing-code-quality as a gate
- **THEN** the review output determines whether the builder proceeds (Pass/Advisory) or must address findings (Warning/Defect) before declaring completion

**F-02.8: Large input — no hard limit, garbage-in garbage-out**
- **GIVEN** an operator invokes /reviewing-code-quality on an entire repository or very large directory
- **WHEN** the skill processes the input
- **THEN** it proceeds without refusing; quality of findings degrades proportionally with scope size; the skill does not warn or refuse; operators are expected to scope their input appropriately (e.g., git diff output, a specific directory, or a glob pattern)

---

## F-03: Stress Testing | SHOULD

**F-03.1: Function-under-test identified from argument (happy path)**
- **GIVEN** an operator invokes /stress-testing with a specific function or file path as argument
- **WHEN** the skill locates the function
- **THEN** it identifies applicable invariants, generates a standalone property-based test script for that function using the project's language-appropriate framework (hypothesis for Python, fast-check for JS/TS, proptest for Rust), and writes the script to tmp/

**F-03.2: Function-under-test identified from context**
- **GIVEN** no argument is provided but the most recently discussed function is clear from conversation context
- **WHEN** the skill begins
- **THEN** it identifies that function as the target, states its inference, and proceeds to test generation

**F-03.3: No function-under-test identifiable (failure)**
- **GIVEN** no argument is provided and no target is inferable from context
- **WHEN** the skill attempts identification
- **THEN** it reports that no target could be identified and stops; it does not generate tests for arbitrary code

**F-03.4: Test script generates 100+ random cases**
- **GIVEN** a function-under-test is identified
- **WHEN** the test script is generated
- **THEN** the script is configured to generate at least 100 random test cases; the script is self-contained and runnable without additional setup beyond the testing framework

**F-03.5: Tests executed and failures reported**
- **GIVEN** the test script is generated
- **WHEN** the skill runs the script
- **THEN** any failures are reported with the specific input that caused the failure, making them reproducible; passing tests are summarized with case count

**F-03.6: Invariant identification — round-trip**
- **GIVEN** the function-under-test involves serialization, encoding, or parsing
- **WHEN** the skill identifies invariants
- **THEN** it generates a round-trip invariant test: decode(encode(x)) equals x

**F-03.7: Test script runtime crash — debug and retry once**
- **GIVEN** the generated test script crashes at runtime (e.g., import error, segfault) rather than producing test failures
- **WHEN** the skill receives the crash output
- **THEN** it attempts to diagnose and fix the script (e.g., resolves import errors, corrects API usage) and re-runs once; if the retry also crashes, it reports the crash output as a finding and stops

**F-03.8: No framework installed (failure)**
- **GIVEN** the language requires hypothesis/fast-check/proptest but the framework is not installed in the project
- **WHEN** the skill attempts to run tests
- **THEN** it reports the missing dependency with the install command and does not proceed to test execution

---

## F-04: Atomic Git Commits | MUST

**F-04.1: Survey changes in parallel (happy path)**
- **GIVEN** there are uncommitted changes (staged and/or unstaged) in the working tree
- **WHEN** the operator invokes /git-commit-changes
- **THEN** the skill surveys git status, git diff, and git diff --cached simultaneously to understand all changes before grouping

**F-04.2: Changes grouped by logical relationship**
- **GIVEN** changes exist across multiple files
- **WHEN** the skill groups changes into commits
- **THEN** it groups by logical relationship in priority order: same concern (function + its tests) first, same feature across files second, same change type (renames, formatting) third, config/chore last; files are not committed one per commit

**F-04.3: Commit plan presented with 30-second auto-proceed**
- **GIVEN** the grouping is complete
- **WHEN** the skill presents its plan
- **THEN** it shows a numbered list of proposed commits, each with type, description, and files included; it waits up to 30 seconds for operator response; if no response is received within 30 seconds, it auto-proceeds with the plan as shown

**F-04.4: Execution uses specific file staging**
- **GIVEN** the operator confirms the plan
- **WHEN** commits are executed
- **THEN** each commit stages only its specific files (not `git add -A` or `git add .`); conventional commit format (type: description) is used for all messages

**F-04.5: Verification after completion**
- **GIVEN** all commits have been created
- **WHEN** the skill finishes
- **THEN** it runs git log --oneline and shows the new commits to the operator as verification

**F-04.6: No Co-Authored-By lines (hard constraint)**
- **GIVEN** any commit is being created
- **WHEN** the commit message is composed
- **THEN** the message contains no Co-Authored-By lines under any circumstances

**F-04.7: No amend to existing commits (hard constraint)**
- **GIVEN** the operator's staged changes could logically extend the previous commit
- **WHEN** the skill creates commits
- **THEN** it always creates new commits; it never amends the previous commit

**F-04.8: No push to remote (hard constraint)**
- **GIVEN** commits are created successfully
- **WHEN** the skill completes
- **THEN** it does not push to any remote; the operator pushes manually

**F-04.9: Clean working tree (no-op)**
- **GIVEN** there are no staged or unstaged changes
- **WHEN** the operator invokes /git-commit-changes
- **THEN** the skill reports that there are no changes to commit and exits without creating any commits

---

## F-05: Post-Mortem Learning | SHOULD

**F-05.1: Gotchas identified, ranked, and proposed (happy path)**
- **GIVEN** the operator invokes /conducting-post-mortem after completing a task
- **WHEN** the skill analyzes the conversation history
- **THEN** it identifies up to 3 undocumented gotchas, ranks them by potential impact on future sessions, and proposes specific markdown content for each (problem, solution, suggested CLAUDE.md location); the operator can apply any or all of the proposals

**F-05.2: No gotcha found — report without fabrication**
- **GIVEN** the skill analyzes the conversation but finds no undocumented gotchas
- **WHEN** the skill produces output
- **THEN** it reports that no new learnings were found; it does not fabricate or pad a gotcha to appear useful

**F-05.3: Proposed update already documented — skip**
- **GIVEN** the only candidate gotcha is already present in CLAUDE.md
- **WHEN** the skill evaluates whether to propose an update
- **THEN** it notes the existing documentation and reports that no new update is needed

**F-05.4: Read-only constraint — no direct modification**
- **GIVEN** a gotcha and proposed CLAUDE.md update are identified
- **WHEN** the skill outputs its proposal
- **THEN** it presents the proposed content as a suggestion for the operator to review and apply; it does not modify CLAUDE.md directly

**F-05.5: CLAUDE.md missing — warn but continue**
- **GIVEN** no CLAUDE.md exists in the project root
- **WHEN** the skill attempts to check for existing documentation
- **THEN** it warns that CLAUDE.md is missing and continues with its analysis; it proposes creating a CLAUDE.md with the captured learning rather than halting

**F-05.6: Optional task file input**
- **GIVEN** the operator provides a path to a completed task file (e.g., tasks/completed/001-auth.md) as an argument
- **WHEN** the skill analyzes lessons learned
- **THEN** it reads the task file content as additional context alongside the conversation history to improve the quality of the gotcha identification

---

## Open Questions

*(No unresolved questions.)*

## Assumptions

- **A-01**: [ASSUMPTION] /orchestrating-workflow requires interactive mode — it cannot function in one-shot (-p) mode because it must wait for operator approval of the decomposition plan before spawning agents.
- **A-06**: Task tracking via TaskCreate/TaskUpdate/TaskList/TaskGet is ephemeral to the current Claude Code session. If the session ends mid-orchestration, task state is lost and the orchestration must be restarted.
- **A-02**: [ASSUMPTION] The "parallel tool calls in single response" constraint for builder launching is enforced by the skill's own instructions, not by Claude Code tooling; the skill would not detect a violation if builders were launched sequentially.
- **A-03**: [ASSUMPTION] /reviewing-code-quality does not have a hard line limit for input; it handles directories and globs by processing files iteratively.
- **A-04**: [ASSUMPTION] /git-commit-changes operates only on the current git repository's working tree; it does not traverse into submodules.
- **A-05**: [ASSUMPTION] /conducting-post-mortem does not have access to previous conversation sessions; it can only analyze the current session's history.
