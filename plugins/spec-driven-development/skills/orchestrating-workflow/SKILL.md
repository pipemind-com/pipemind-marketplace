---
name: orchestrating-workflow
description: "Decomposes features into parallel sub-tasks, plans each via planner agents, builds via parallel builder agents. Use for multi-part features requiring coordinated implementation."
user-invocable: true
argument-hint: "feature description, spec file path, or issue URL"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Task
  - AskUserQuestion
  - TaskCreate
  - TaskUpdate
  - TaskList
  - TaskGet
model: opus
color: cyan
---

# Orchestrating Workflow

Coordinates planner and builder agents to implement multi-part features. The orchestrator decomposes, delegates, and tracks — it never writes production code or makes design decisions.

**Core principle**: The orchestrator coordinates — it never writes production code or makes design decisions. All code changes flow through builder subagents.

## Pre-Flight Checks

Before anything else, verify all prerequisites exist. FAIL and stop if any are missing:

1. `CLAUDE.md` exists in project root — if not: "Run `/compiling-project-settings` first"
2. `.claude/agents/planner.md` exists — if not: "Run `/compiling-planner-agent` first"
3. `.claude/agents/builder.md` exists — if not: "Run `/compiling-builder-agent` first"
4. Feature description was provided as argument — if not: "Provide a feature description, spec file path, or issue URL"
5. Discover test runner command: check `package.json` scripts, `Makefile`, `Cargo.toml`, then `CLAUDE.md` — if not found: halt with "No test runner found — add a test command to package.json, Makefile, or CLAUDE.md"
6. Discover test file naming convention: scan existing test files for pattern (e.g., `*.test.ts`, `*_test.go`, `test_*.py`) — if not found: halt with "No test file naming convention found — add example to CLAUDE.md"
7. Verify test scenario spec files exist in `specs/` (produced by `/defining-test-scenarios`) — if none found: halt with "No test scenario specs in specs/ — run `/defining-test-scenarios` first"
8. Store discovered test runner command and naming convention for Wave 1 builder prompts

Once verified, read `CLAUDE.md` and list available `docs/*.md` files — these will be passed as context to subagents.

## Phase 1: Requirements Gathering

1. Read `CLAUDE.md` for architecture, stack, and coding patterns
2. Read the feature description from the argument (if a file path, read the file; if inline text, use directly)
3. Explore the codebase: use Glob/Grep to identify affected areas, existing patterns, and related code
4. Use AskUserQuestion to clarify (max 3 questions): scope boundaries, priority constraints, known blockers
5. If user declines to answer: proceed with best-judgment defaults and tag uncertain items as **[assumption]**

## Phase 2: Decomposition

Break the feature into **2-6 independent sub-tasks**. Each sub-task must be:
- **Plannable in isolation** — a planner can design it without seeing other sub-tasks
- **Buildable in isolation** — a builder can implement it given only its plan
- **Testable in isolation** — can be verified without other sub-tasks complete

For each sub-task, define:
- **Title** (imperative verb phrase): e.g., "Add authentication middleware"
- **Scope** (2-3 sentences): what's included and what's explicitly excluded
- **Likely files**: best-guess list of files to create or modify
- **Dependencies**: which other sub-tasks must complete first

**Dependency rules**:
- A creates an interface that B consumes → B depends on A
- A and B modify the same file at overlapping locations → add dependency (serialize them)
- No circular dependencies allowed — restructure sub-tasks if detected

Present the decomposition to user via AskUserQuestion for confirmation. Adjust if user requests changes.

## Phase 3: Two-Pass Planning

### Pass 1 — Parallel Planning

Spawn planner subagents via the `Task` tool with `subagent_type: general-purpose`, beginning the prompt with `@"planner (agent)"` — this routes to the compiled planner agent with its full identity. Only pass task-specific context in the rest of the prompt:

Each planner prompt includes:
- Contents of `CLAUDE.md` as project context
- List of available `docs/` files
- Sub-task title and scope
- Dependency context: predecessor sub-task scopes and their completed plans (if available)
- Relevant test scenario spec file path(s) from `specs/` — so the planner can reference specific scenarios in its output for Wave 1 builders

**Emit all independent planner Task calls in a single response** — multiple tool calls in one message run concurrently. Never launch planners one at a time. Only wait for a predecessor's plan to finish before launching a dependent sub-task, then immediately launch that dependent planner.

### Pass 2 — Reconciliation

After ALL planner outputs return, review them together for conflicts:

1. **File overlap check**: Two plans modify the same file at overlapping locations → add `blockedBy` so they run sequentially
2. **Interface check**: Plan A defines an interface/type that Plan B consumes → B blocked by A
3. **Test isolation check**: Plans share DB state, same port, or global config → add dependency or note isolation requirement

Then create the task graph:
- `TaskCreate` for each sub-task with the full planner output as the description
- Set `blockedBy` relationships using the returned task IDs
- Print the task graph summary for user visibility:
  ```
  Task Graph:
  #1 Add auth middleware          [no dependencies]
  #2 Add login/logout routes      [blocked by #1]
  #3 Add session persistence      [blocked by #1]
  #4 Add auth tests               [blocked by #2, #3]
  ```

## Wave 1 — Test Building

Launch ALL test builders for every sub-task simultaneously in a single response — dependency ordering is Wave 2's concern.

Each Wave 1 builder prompt begins with `@"builder (agent)"` using `subagent_type: general-purpose`, and includes: planner output, instruction to write TESTS ONLY, discovered test runner command, test file naming convention, and relevant test scenario spec file path(s).

Builders may only produce: test files, fixtures, test helpers, and minimal type/interface stubs (type signatures only — no implementation logic).

Each Wave 1 builder must satisfy these completion criteria before reporting done:

1. Builder runs `/reviewing-code-quality` on its test files — addresses any Warning/Defect findings
2. Builder verifies all scenarios from the referenced test scenario spec file are covered by at least one test
3. Builder runs tests and confirms ALL fail (red phase) — if any test passes: rewrite it to target unimplemented behavior, or delete it if trivially true; iterate until all tests fail (no orchestrator retry limit)

Wait for ALL Wave 1 builders before starting Wave 2.

If a builder fails: ask operator per sub-task — "Skip in Wave 2 or build without tests?" (30-second timeout defaults to skip).

## Wave 2 — Code Building

Launch unblocked code builders in parallel (single response), respecting the dependency graph.

Each Wave 2 builder prompt begins with `@"builder (agent)"` using `subagent_type: general-purpose`, and includes: planner output and the FILE PATHS (not content) of Wave 1 test files. The builder reads those files itself.

Each Wave 2 builder must satisfy these completion criteria before reporting done:

1. Builder implements code, iterates until all Wave 1 tests pass (no orchestrator retry limit)
2. After tests pass: builder runs spec-implemented gate — reviews feature description and behavioral spec scenarios to verify all specified behaviors are implemented
3. If gap found: builder runs TDD micro-cycle inline (write test → confirm fail → implement → confirm pass)
4. Builder does not declare completion until all tests pass AND all spec scenarios are covered

Completion handling:
- Builder completes → `TaskUpdate` to `completed`, `TaskList` to find newly unblocked tasks, launch them in single response
- Builder reports blocked → pause, surface to user via AskUserQuestion: "Builder for '{task}' is blocked: {reason}" with options: Provide guidance / Skip task / Abort all
- Builder reports partial completion → re-launch exactly once with failing test list; if retry fails → mark `failed`, surface to user via AskUserQuestion: "Builder for '{task}' failed after retry: {reason}" with options: Retry with guidance / Skip task / Abort all
- Builder fails → same pause-and-ask pattern with options: Retry with guidance / Skip task / Abort all
- Repeat until all tasks completed, skipped, or aborted

## Phase 5: Final Verification

1. Run the project's full test suite using the discovered test runner command
2. If any Wave 1 test for a completed sub-task fails: identify cross-contamination — report which sub-task's tests broke and which Wave 2 builder likely caused it
3. Surface cross-contamination to operator via AskUserQuestion before proceeding to completion report

## Phase 6: Completion Report

When all tasks finish, print a summary:

```
Orchestration Complete
=====================
| # | Task                    | Status    | Files Modified           | Tests |
|---|-------------------------|-----------|--------------------------|-------|
| 1 | Add auth middleware      | completed | src/middleware/auth.ts    | 4     |
| 2 | Add login/logout routes  | completed | src/routes/auth.ts       | 6     |
| 3 | Add session persistence  | skipped   | —                        | —     |
| 4 | Add auth tests           | completed | tests/auth.test.ts       | 3     |

Test Results: 13 passed, 0 failed
Issues: Task #3 skipped (user decision)
```

Suggest next steps:
- `/git-commit-changes` to create atomic commits
- `/conducting-post-mortem` to capture lessons learned

## Red Flags

Stop and reassess if any of these occur:
- Orchestrator is about to modify files directly (delegate to a builder instead)
- Decomposition exceeds 6 sub-tasks (consolidate — the feature may need splitting into multiple orchestrations)
- Builders are launching without planner output (every builder needs a plan)
- No user confirmation happened before building phase (always confirm decomposition first)
- A failure is being silently swallowed (always surface errors to the user)
- Agents are being launched one at a time when multiple are unblocked (always batch into a single response)
- Wave 2 builders are launching before all Wave 1 builders have confirmed all-tests-failing (always wait for complete red phase)
- A Wave 1 builder produced implementation code rather than tests (re-run with explicit test-only instruction)
