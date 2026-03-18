# Prompt Templates

Reference for how the orchestrator should construct prompts when spawning planner and builder subagents via the `Task` tool.

## Spawning a Planner

```
Task(
  subagent_type: general-purpose,
  description: "Plan <sub-task title>",
  prompt: |
    @"planner (agent)"

    Project context:
    {contents of CLAUDE.md}

    Available documentation:
    {list of docs/ files that exist}

    Your sub-task:
    Title: {sub-task title}
    Scope: {sub-task scope description}
    Likely files: {list of likely files}

    Dependencies context:
    {list of predecessor sub-tasks with their scope descriptions}
    {completed plans of predecessor dependencies, if available}

    Constraints:
    - Plan ONLY the sub-task above — do not plan work belonging to other sub-tasks
    - Reference existing patterns found in the codebase
    - If a dependency plan is provided above, ensure your plan is compatible with its interfaces
)
```

## Spawning a Builder

```
Task(
  subagent_type: general-purpose,
  description: "Build <task title>",
  prompt: |
    @"builder (agent)"

    {full planner output from TaskGet description}

    Constraints:
    - Implement ONLY what the plan specifies — no extra features or refactoring
    - Run only tests relevant to your changes (parallel builders share the environment)
    - If blocked by a missing dependency or unclear requirement, report the blocker clearly instead of guessing
)
```

## Why `@"agent (agent)"` syntax

Claude Code resolves `@"<name> (agent)"` references at the start of a Task prompt to the compiled agent at `.claude/agents/<name>.md`, instantiating it with its full identity (color, model, tools, system prompt). Using `subagent_type: "planner"` or `subagent_type: "builder"` does NOT work — the Task tool only accepts built-in type names. The `@` reference in the prompt is the correct mechanism for project-level agents.

## Decomposition Summary

Shown to user for approval before planning begins:

```
Feature: {feature description}

Sub-tasks:
1. {title}
   Scope: {scope}
   Files: {likely files}
   Dependencies: none

2. {title}
   Scope: {scope}
   Files: {likely files}
   Dependencies: #1

...

Dependency graph:
#1 ──► #2 ──► #4
#1 ──► #3 ──► #4

Proceed with planning? [Approve / Adjust / Cancel]
```
