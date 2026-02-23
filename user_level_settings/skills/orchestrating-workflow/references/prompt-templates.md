# Prompt Templates

Templates for injecting project-specific context into Task subagents. The orchestrator reads these templates and fills in the `{placeholders}` before passing to the Task tool prompt.

## Planner Subagent Prompt

```
You are a planner agent for this project. Follow these instructions:

{contents of .claude/agents/planner.md}

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

Return your plan using the Output Format defined in the planner instructions above.
```

## Builder Subagent Prompt

```
You are a builder agent. Follow these instructions:

{contents of .claude/agents/builder.md}

Project context:
{contents of CLAUDE.md}

Your task:
{full planner output from TaskGet description}

Constraints:
- Implement ONLY what the plan specifies — no extra features or refactoring
- Run tests after implementation
- If blocked by a missing dependency or unclear requirement, report the blocker clearly instead of guessing

Return your status using the Output Format defined in the builder instructions above.
```

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
