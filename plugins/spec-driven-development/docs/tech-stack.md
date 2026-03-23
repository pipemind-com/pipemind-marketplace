# Tech Stack

> **AI Context Summary**: Pure markdown/YAML system—no build pipeline, no runtime dependencies,
> no package manager. All configuration is YAML frontmatter at the top of .md files. Agent files
> use kebab-case noun names (50-100 lines); skill files use gerund names (100-200 lines). Available
> models: haiku (fast/simple), sonnet (balanced, default), opus (complex reasoning). Start with
> minimal tool permissions and add only what's necessary.

## Stack Overview

| Layer | Technology | Notes |
|-------|------------|-------|
| Language | Markdown + YAML | No compilation, no interpreter |
| Format | GitHub-flavored Markdown | YAML frontmatter delimited by `---` |
| Storage | Plain files | `~/.claude/` (global) + `.claude/` (per-project) |
| Runtime | Claude Code CLI | Reads agents/skills, provides tools |
| Version control | Git | Required for most skills |

## YAML Frontmatter Reference

### Agent Format

```yaml
---
name: kebab-case-noun        # Required: e.g., code-reviewer, task-planner
description: Under 100 chars # Required: shown in agent selection UI
model: sonnet                # haiku | sonnet | opus
tools:                       # Minimal necessary set
  - Read
  - Glob
  - Grep
  - Edit                     # Add if agent writes files
  - Write                    # Add if agent creates new files
  - Bash                     # Add if agent runs commands
  - Task                     # Add if agent spawns subagents
color: blue                  # purple|blue|red|orange|green|yellow|cyan
---
```

**File location**: `user_level_settings/agents/<name>.md` (global) or `.claude/agents/<name>.md` (per-project)

### Skill Format

```yaml
---
name: gerund-form            # Required: e.g., reviewing-code, compiling-planner-agent
description: What it does    # Required: under 100 chars
user-invocable: true         # Makes available as /command in Claude Code
argument-hint: "path/to/file"# Optional: shown as hint in UI
allowed-tools:               # Tools the skill can use
  - Read
  - Glob
  - Grep
  - Write
  - Bash
model: sonnet                # Optional: override default model
color: green                 # Optional: UI color
---
```

**File location**: `user_level_settings/skills/<gerund-name>/SKILL.md`

## Model Selection Guide

| Model | Use When | Cost |
|-------|----------|------|
| `haiku` | Simple, fast tasks; high-volume operations | Lowest |
| `sonnet` | General-purpose; balanced quality/speed (default) | Medium |
| `opus` | Complex reasoning; agent-author, architecture design | Highest |

## Tool Permission Tiers

Start at the lowest tier that accomplishes the task:

| Tier | Tools | Use For |
|------|-------|---------|
| Read-only | `Read, Glob, Grep` | Analysis, review, research |
| Write | + `Edit, Write` | Document generation, code modification |
| Execute | + `Bash` | Running tests, git operations, commands |
| Orchestrate | + `Task` | Spawning subagents for parallel work |

## File Naming Conventions

```
# Agents (nouns, kebab-case)
agent-author.md
code-reviewer.md
task-planner.md

# Skills (gerunds, kebab-case, in subdirectory)
compiling-planner-agent/SKILL.md
reviewing-code-quality/SKILL.md
conducting-post-mortem/SKILL.md

# Project agents (compiled products)
.claude/agents/planner.md
.claude/agents/builder.md
.claude/agents/security.md
.claude/agents/devops.md
```

## Size Constraints

| File Type | Target Lines | Rationale |
|-----------|-------------|-----------|
| Project agents | 50-100 | 150 instruction limit; each line ~= 1 instruction |
| Factory skills | 100-200 | More detail needed; not in permanent context |
| CLAUDE.md | 50-100 | Loaded every session; must stay lean |
| `docs/*.md` | 80-300 | Loaded on demand; can be detailed |

## The 150 Instruction Limit

Claude Code's system prompt uses ~50 instructions. CLAUDE.md + all agents loaded share the
remaining ~100. Exceeding this degrades all instruction-following.

**Mitigation**: Progressive disclosure pattern:
```
CLAUDE.md (≤100 lines) ──references──► docs/architecture.md (150-250 lines)
Agent (≤100 lines)     ──references──► CLAUDE.md, docs/
```

## Cross-References

- How files fit together: [architecture.md](./architecture.md)
- Using agents in practice: [workflow.md](./workflow.md)
- Full agent authoring guide: `user_level_settings/agents/agent-author.md`
