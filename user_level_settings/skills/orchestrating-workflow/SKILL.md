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

## Phase 4: Parallel Building

### Launch Loop

1. Call `TaskList` to identify all currently unblocked pending tasks
2. For each unblocked task, call `TaskUpdate` to `in_progress` and `TaskGet` to retrieve its planner output — do these prep calls in parallel too
3. Check each for file conflicts with already-running builders
4. **In a single response, emit one `Task` call per non-conflicting builder** — this launches them all concurrently. Never serialize builders that could run in parallel. Each Task call must use `subagent_type: general-purpose` and begin the prompt with `@"builder (agent)"` so Claude Code routes it to the compiled builder agent.

### Completion Handling

- **Builder completes successfully** → `TaskUpdate` to `completed`, call `TaskList` to find all newly unblocked tasks, **launch them all in a single response**
- **Builder reports blocked** → pause, surface to user via AskUserQuestion: "Builder for '{task}' is blocked: {reason}" with options: Provide guidance / Skip task / Abort all
- **Builder fails** → same pause-and-ask pattern with options: Retry with guidance / Skip task / Abort all

Repeat the launch loop until all tasks are completed, skipped, or aborted.

## Phase 5: Completion Report

When all tasks finish, print a summary:

```
Orchestration Complete
=====================
| # | Task                    | Status    | Files Modified           |
|---|-------------------------|-----------|--------------------------|
| 1 | Add auth middleware      | completed | src/middleware/auth.ts    |
| 2 | Add login/logout routes  | completed | src/routes/auth.ts       |
| 3 | Add session persistence  | skipped   | —                        |
| 4 | Add auth tests           | completed | tests/auth.test.ts       |

Test Results: 12 passed, 0 failed
Issues: Task #3 skipped (user decision)
```

Then run `/git-commit-changes of the changes we implemented` to create atomic commits

Suggest next steps:
- `/conducting-post-mortem` to capture lessons learned

## Red Flags

Stop and reassess if any of these occur:
- Orchestrator is about to modify files directly (delegate to a builder instead)
- Decomposition exceeds 6 sub-tasks (consolidate — the feature may need splitting into multiple orchestrations)
- Builders are launching without planner output (every builder needs a plan)
- No user confirmation happened before building phase (always confirm decomposition first)
- A failure is being silently swallowed (always surface errors to the user)
- Agents are being launched one at a time when multiple are unblocked (always batch into a single response)
