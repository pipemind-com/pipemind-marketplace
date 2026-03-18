---
name: compiling-agentic-workflow
description: "Compiles the full agentic workflow for a project: CLAUDE.md, docs/, planner, and builder agents. Idempotent — safe to re-run."
user-invocable: true
argument-hint: "optional: customization notes passed to sub-skills"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Bash
  - Skill
model: sonnet
color: cyan
---

# Compiling Agentic Workflow

Orchestrates the full project compilation sequence in one invocation. Calls each sub-skill in dependency order, passing results forward. Idempotent — re-running updates all artifacts to match current codebase state.

## Pre-Flight Checks

1. Verify git repository (`git rev-parse --is-inside-work-tree`) — FAIL if not
2. Note whether `CLAUDE.md`, `docs/`, `.claude/agents/planner.md`, `.claude/agents/builder.md` already exist (for reporting)

## Compilation Sequence

Execute these skills **in order** — each depends on the output of the previous:

### Step 1: Compile Project Settings
```
/compiling-project-settings {user arguments if provided}
```
Generates or updates `CLAUDE.md` (~50-100 lines). All subsequent steps reference this file.

### Step 2: Compile Project Docs
```
/compiling-project-docs
```
Generates or updates `docs/` directory. Planner and builder agents reference these files.

### Step 3: Compile Planner Agent
```
/compiling-planner-agent {user arguments if provided}
```
Generates or updates `.claude/agents/planner.md`.

### Step 4: Compile Builder Agent
```
/compiling-builder-agent {user arguments if provided}
```
Generates or updates `.claude/agents/builder.md`.

## After Completion

Report what was compiled:

```
Agentic Workflow Compiled
=========================
| Artifact                      | Status  | Lines |
|-------------------------------|---------|-------|
| CLAUDE.md                     | created | 72    |
| docs/ (N files)               | created | 580   |
| .claude/agents/planner.md     | created | 85    |
| .claude/agents/builder.md     | created | 91    |

Next steps:
  claude --agent planner    # Design a feature
  claude --agent builder    # Implement a task
  /compiling-security-agent # (optional) Add security auditor
  /compiling-devops-agent   # (optional) Add DevOps specialist
```

Use `created` for new files, `updated` for re-compilations.

## Error Handling

- If any sub-skill fails, **stop and report** — don't continue with missing prerequisites
- If `CLAUDE.md` already exists, sub-skills handle the override prompt — don't suppress it

## Arguments

All arguments are forwarded to sub-skills where applicable:
- Customization notes → passed to `/compiling-project-settings` and agent compilers
- `--focus "area"` → passed to `/compiling-project-settings`
