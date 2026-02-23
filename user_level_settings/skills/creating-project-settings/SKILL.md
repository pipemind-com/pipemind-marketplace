---
name: creating-project-settings
description: "Generates lean CLAUDE.md (~50-100 lines) with progressive disclosure. Use when setting up a new project or when CLAUDE.md is missing or bloated."
user-invocable: true
argument-hint: "optional: --focus 'area' to emphasize specific patterns"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Bash
model: sonnet
color: green
---

# Creating Project Settings

Analyzes your codebase and generates a **lean** `CLAUDE.md` following the "less is more" principle. References `docs/` for detailed content.

## Critical: The 150 Instruction Limit

Claude reliably follows ~150 instructions. Claude Code's system prompt uses ~50, leaving **~100 for CLAUDE.md + agents combined**. A bloated CLAUDE.md degrades all instruction-following.

## Safety

**Always use `fd` instead of `find`** for filesystem discovery. `fd` is safe by design (no `-exec`, no `-delete`).

## When Invoked

**1. Pre-Flight Validation**:
   - Verify git repository (FAIL if not)
   - Check if `CLAUDE.md` exists (warn, allow override)

**2. Codebase Analysis**:
   - Detect tech stack from project files
   - Identify framework and architecture pattern
   - Map key directory structure
   - Check for `.claude/agents/planner.md` and `builder.md` (triggers Workflow section)

**3. Code Exploration**:
   - Read key configuration files
   - Sample 2-3 implementation files to detect patterns
   - Identify essential commands (build, test, run)

**4. Generate Lean CLAUDE.md** (~50-100 lines):
   1. **Project Context** (2-3 sentences) — what this is
   2. **About This Project** (tech stack, 2-3 sentences)
   3. **Key Directories** (5-8 items max)
   4. **Commands** (essential only)
   5. **Standards** (critical conventions only)
   6. **Notes** (gotchas, warnings)
   7. **Workflow** (conditional — only if planner/builder agents exist)
   8. **Additional Documentation** — references to `docs/` files

**5. Validation**:
   - Verify under 100 lines
   - Verify 80% rule compliance
   - Confirm no bloat or linting instructions

## Arguments

- `--focus "area"`: Emphasize specific patterns (e.g., "caching", "auth")
- Default: Lean CLAUDE.md only. Run `/creating-project-docs` afterward for detailed docs.

## CLAUDE.md Template (Target: 50-100 lines)

```markdown
# Project Context

Brief philosophy (1-2 sentences).

## About This Project

[Tech stack, 2-3 sentences max]

## Key Directories

- `src/` — Source code
- `tests/` — Test files
- [5-8 items max]

## Commands

```bash
[command]  # Dev server
[command]  # Run tests
[command]  # Build
```

## Standards

- [Critical convention 1]
- [3-5 items max, only what causes bugs if missed]

## Notes

- [Gotcha 1]
- [Only critical warnings]

## Workflow
<!-- Only if .claude/agents/planner.md and builder.md exist -->

When implementing multi-part features:
1. Decompose into independent subproblems
2. Spawn parallel planner agents via Task tool
3. Collect plans, resolve file-overlap conflicts
4. Spawn parallel builder agents for independent tasks
5. Sequence tasks that touch shared files; parallelize the rest

## Additional Documentation

Before specific tasks, read relevant documentation:
- Architecture: `docs/architecture.md`
- Testing: `docs/testing.md`
Read only what's relevant to your current task.

Generate docs with: `/creating-project-docs`
```

## The 80% Rule

**Only include instructions relevant to 80%+ of sessions.**

Include in CLAUDE.md: essential commands, critical conventions, key directories, gotchas, tech stack overview.

Move to `docs/`: detailed deployment steps, comprehensive code style, full architecture, database schema, edge case handling.

Do NOT include: linting rules (use actual linters), what Claude can infer, task-specific instructions (belong in agents), sensitive info (API keys, credentials).

Run `/creating-project-docs` to generate the `docs/` content.
