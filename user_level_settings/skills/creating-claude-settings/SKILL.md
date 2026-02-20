---
name: creating-claude-settings
description: Generates lean CLAUDE.md (~50-100 lines) with progressive disclosure
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

# Creating Claude Settings

Analyzes your codebase and generates a **lean** `CLAUDE.md` file following the "less is more" principle. Uses progressive disclosure by referencing `docs/` for detailed content.

## Critical Principle: The 150 Instruction Limit

Claude can reliably follow ~150-200 instructions. Claude Code's system prompt uses ~50, leaving **~100-150 for your CLAUDE.md**.

**If you stuff CLAUDE.md with too much, Claude ignores it.**

This skill generates:
- **Lean CLAUDE.md**: 50-100 lines (core context only)
- References `docs/` for detailed content (use `/creating-project-docs` to generate)

## When Invoked

**1. Pre-Flight Validation**:
   - Check if in a git repository
   - Check if `CLAUDE.md` already exists (warn, allow override)
   - Report validation status

**2. Codebase Analysis**:
   - Detect tech stack from project files
   - Identify framework and architecture pattern
   - Map key directory structure
   - Find essential configuration files
   - Check for `.claude/agents/planner.md` and `builder.md` (triggers Workflow section)

**3. Code Exploration**:
   - Read key configuration files
   - Sample 2-3 implementation files to detect patterns
   - Identify essential commands (build, test, run)

**4. Generate Lean CLAUDE.md** (~50-100 lines):
   Six core sections following WHAT/WHY/HOW framework:
   1. **Project Context** (2-3 sentences) - WHAT this is
   2. **About This Project** (tech stack, 2-3 sentences)
   3. **Key Directories** (5-8 items max)
   4. **Commands** (essential only)
   5. **Standards** (critical conventions only)
   6. **Notes** (gotchas, warnings)
   7. **Workflow** (conditional — only if `.claude/agents/planner.md` and `builder.md` exist) - parallel orchestration via Task tool

**5. Reference docs/** (for progressive disclosure):
   CLAUDE.md will reference `docs/` for detailed content.
   Run `/creating-project-docs` to generate comprehensive documentation:
   - `docs/architecture.md` - detailed architecture
   - `docs/testing.md` - testing strategy
   - `docs/deployment.md` - deployment procedures
   - `docs/getting-started.md` - setup guide

**6. Validation**:
   - Verify CLAUDE.md is under 100 lines
   - Check 80% rule: content relevant to most sessions
   - Confirm no bloat or linting instructions

## Arguments

**Optional flags:**
- `--focus "area"`: Emphasize specific patterns (e.g., "caching", "auth")
- Default: Lean CLAUDE.md only

**For detailed documentation:** Run `/creating-project-docs` after this skill.

## CLAUDE.md Template (Target: 50-100 lines)

```markdown
# Project Context

Brief philosophy (1-2 sentences about working approach).

## About This Project

[Tech stack, 2-3 sentences max]

## Key Directories

- `src/` - Source code
- `tests/` - Test files
- [5-8 items max, most important only]

## Commands

```bash
[command]  # Dev server
[command]  # Run tests
[command]  # Build
```

## Standards

- [Critical convention 1]
- [Critical convention 2]
- [3-5 items max, only what causes bugs if missed]

## Notes

- [Gotcha 1]
- [Gotcha 2]
- [Only critical warnings]

## Workflow
<!-- Only include this section if .claude/agents/planner.md and builder.md exist -->

When implementing multi-part features:
1. Decompose the problem into independent subproblems with shared architectural constraints
2. Spawn parallel planner agents (one per subproblem) via Task tool
3. Collect plans, resolve file-overlap conflicts, produce unified task list
4. Spawn parallel builder agents for independent tasks via Task tool
5. Sequence tasks that touch shared files; parallelize the rest

## Additional Documentation

Before specific tasks, read relevant documentation:
- Architecture: `docs/architecture.md`
- Tech stack: `docs/tech-stack.md`
- Testing: `docs/testing.md`
- Getting Started: `docs/getting-started.md`
Read only what's relevant to your current task.

Generate docs with: `/creating-project-docs`
```

## The 80% Rule

**Only include instructions relevant to 80%+ of Claude Code sessions.**

| Include in CLAUDE.md | Move to docs/ |
|---------------------|---------------|
| Essential commands | Detailed deployment steps |
| Critical conventions | Comprehensive code style |
| Key directory structure | Full architecture diagrams |
| Gotchas that cause bugs | Edge case handling |
| Tech stack overview | Database schema details |

Use `/creating-project-docs` to generate the `docs/` content.

## What NOT to Include in CLAUDE.md

- **Linting rules**: Use actual linters (ESLint, Black, etc.)
- **Everything Claude can infer**: File contents, obvious patterns
- **Task-specific instructions**: Belong in agent files
- **Sensitive information**: API keys, credentials
- **Detailed code style**: Use proper tools

## Examples

### Basic Usage
```
/creating-claude-settings
```

**Output:**
```
Pre-Flight Validation
   Git repository detected
   No existing CLAUDE.md

Codebase Analysis
   Detected: Python 3.12, FastAPI 0.109
   Framework: FastAPI with PostgreSQL
   Architecture: Layered (routes > services > models)

Generating Lean CLAUDE.md
   Project Context (3 lines)
   About This Project (4 lines)
   Key Directories (6 items)
   Commands (4 commands)
   Standards (4 items)
   Notes (3 items)
   Workflow (included — planner/builder agents detected)

Validation
   Total: 76 lines (under 100 limit)
   80% rule: All content universally applicable

Created: CLAUDE.md (67 lines)
```

### With Focus Area
```
/creating-claude-settings --focus "authentication and Redis caching"
```

**Output:**
```
[...standard generation...]

Focus Areas Added:
   Standards: JWT token handling note
   Notes: Redis cache invalidation gotcha

Next step: Run /creating-project-docs to generate detailed docs/
```

### Error Case
```
/creating-claude-settings
```

**When not in git repo:**
```
Pre-Flight Validation FAILED
   Not in a git repository

Run 'git init' first, then try again.
```

## Integration

This skill is the **first step** in the agentic workflow:

```
/creating-claude-settings     ← Lean CLAUDE.md (50-100 lines)
  ↓
/creating-project-docs        ← Detailed docs/ for progressive disclosure
  ↓
/creating-planner-agent
  ↓
/creating-builder-agent
  ↓
Ready for agentic workflow!
```

## Tips

- **Start lean**: You can always add more later
- **Run /creating-project-docs next**: Generates detailed `docs/` for progressive disclosure
- **Review the output**: Validate accuracy for your project
- **Update iteratively**: Use `#` shortcut to add instructions as you discover them
- **Don't duplicate**: Reference CLAUDE.md from agents, don't copy

## Philosophy

**CLAUDE.md is the single source of truth for project context—but only the essential context.**

All agents reference CLAUDE.md. If it's bloated, every agent suffers from instruction limit degradation.

Keep it lean. Use progressive disclosure. Let Claude focus on what matters.
