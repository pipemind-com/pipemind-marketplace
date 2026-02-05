---
name: creating-builder-agent
description: Creates lean project-specific builder agent (50-100 lines)
user-invocable: true
argument-hint: "optional: customization notes or tech stack details"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Bash
model: sonnet
color: blue
---

# Creating Builder Agent

Creates an **ultra-lean** project-specific `builder.md` agent (50-100 lines) that references CLAUDE.md and `docs/` instead of duplicating content.

**Core Philosophy**:
- **Reference, don't duplicate** - CLAUDE.md has context, docs/ has patterns
- **80% rule** - Only include instructions that apply to 80%+ of builder tasks
- **Mission-specific only** - No general coding advice (that's in CLAUDE.md)
- **Clean I/O** - Receive task description via prompt, return completion status

**IMPORTANT**: Generated agent at `<project>/.claude/agents/builder.md` should be ~50-100 lines of mission-specific instructions with references to existing documentation.

## When Invoked

This skill will:

**1. ✅ Pre-Flight Validation** (#1):
   - Check if `CLAUDE.md` exists (FAIL if missing - required for context)
   - Check if `.claude/agents/builder.md` already exists (WARN but allow override)
   - Verify `CLAUDE.md` contains tech stack information
   - Report validation status

**2. 📖 Read Project Context**:
   - Read `CLAUDE.md` to understand architecture, coding standards, and patterns
   - Extract tech stack details
   - Identify framework-specific requirements

**3. 🔍 Tech Stack Detection**:
   - Auto-detect from project files:
     - `package.json` → Node.js/TypeScript
     - `requirements.txt`, `pyproject.toml` → Python
     - `Cargo.toml` → Rust
     - `go.mod` → Go
   - Use patterns from existing codebase (no web fetching needed)

**4. 📝 Generate Lean Builder Agent**:
   - Create `.claude/agents/builder.md` with all required sections
   - Customize content based on project's tech stack
   - Include project-specific patterns from `CLAUDE.md`
   - Apply any user-provided customization notes

**5. ✅ Template Validation** (#3):
   - Verify YAML frontmatter is valid
   - Check ultra-lean structure (Mission, Workflow, Rules, References)
   - **Target: 50-100 lines** (references, not content)
   - Ensure no duplicated content from CLAUDE.md or docs/
   - Verify each rule is 80%+ applicable to builder tasks
   - Verify output format section is included
   - Check anti-patterns table (5 items max)
   - Report validation results

**6. 📊 Report Results**:
   - Confirm file creation location
   - List included sections
   - Report any warnings or issues

## Arguments

**Optional**: Customization notes or additional context
- Example: `"Focus on Python FastAPI patterns"`
- Example: `"Include React Server Components best practices"`
- Example: `"Add Docker deployment workflow"`
- Default: Uses only what's in `CLAUDE.md` and auto-detected context

## Agent Template (Target: 50-100 lines)

The generated `builder.md` agent will be **ultra-lean** with mostly references:

```markdown
# Builder Agent

## Mission
Receive task description via prompt, implement exactly as specified, return completion status.

## Before Any Task
1. Read CLAUDE.md (project context, commands, standards)
2. Read the task description from prompt completely
3. For architecture questions: see docs/architecture.md
4. For testing patterns: see docs/testing.md
5. For framework patterns: see docs/tech-stack.md

## Workflow
1. Parse task description from prompt
2. Implement exactly what's specified
3. Write tests (see CLAUDE.md for test command)
4. Run tests, fix failures
5. Return completion status

## Builder-Specific Rules (80%+ applicable)
- Implement exactly what task specifies - no more, no less
- Write tests before reporting complete
- Never refactor beyond task scope
- If requirements unclear, report blocker in output
- [2-3 more project-specific rules]

## Output Format
Return completion status:
'''
## Status: [completed|blocked|failed]
## Summary: [what was done]
## Files modified:
- path/file.ts - description
## Tests: [passed/failed with details]
## Issues: [any blockers or concerns]
'''

## Anti-Patterns (5 max)
| Don't | Do |
|-------|-----|
| Make design decisions | Follow task description exactly |
| Skip tests | Always test before complete |
| Refactor unrelated code | Stay in task scope |

## References
- Commands: CLAUDE.md ## Commands
- Patterns: docs/architecture.md
- Testing: docs/testing.md
- Tech stack: docs/tech-stack.md
```

**That's it.** ~50-80 lines. No duplicated content.

## Critical Philosophy

**Builder executes mechanically, never analyzes or makes design decisions.**

All architectural thinking, planning, and design decisions are the planner's job. The builder implements exactly what's specified in the prompt without deviation or interpretation.

## Output

Creates `.claude/agents/builder.md` with:
- Complete YAML frontmatter (name, description, tools: Read/Write/Edit/Glob/Grep/Bash, model)
- All core sections fully populated
- Project-specific patterns and examples
- Framework-specific best practices
- Clean prompt→output workflow (receives task, returns status)
- Testing standards and commands

## Examples

### Basic Usage
```
/creating-builder-agent
```

**Expected Output:**
```
✅ Pre-Flight Validation
   ✅ CLAUDE.md exists
   ⚠️  builder.md already exists - will override
   ✅ Tech stack found: Python, FastAPI, Supabase

📖 Reading Project Context
   • Architecture: API-first, PostgreSQL database
   • Coding standards: Type hints, async/await
   • Testing: pytest with 80% coverage

🔍 Tech Stack Detection
   • Detected: Python 3.12, FastAPI 0.109
   • Patterns from: existing codebase + CLAUDE.md

📝 Generating Builder Agent
   • Creating: .claude/agents/builder.md
   • Structure: Mission + Workflow + Rules + Output Format + References
   • Tools: Read, Write, Edit, Glob, Grep, Bash
   • Lines: 72 (within 50-100 target)

✅ Template Validation
   ✅ YAML frontmatter valid
   ✅ Ultra-lean structure (72 lines)
   ✅ No duplicated content from CLAUDE.md
   ✅ Output format section included

📊 Results
   ✅ Created: .claude/agents/builder.md (67 lines)
   📝 Structure: Mission, Before Task, Workflow, Rules, Anti-patterns, References
   🔗 References: CLAUDE.md, docs/architecture.md, docs/testing.md
```

### With Customization
```
/creating-builder-agent "Include Docker deployment patterns and Redis caching"
```

**Expected Output:**
```
✅ Pre-Flight Validation Passed
📖 Reading Project Context
📝 Generating Builder Agent
   • Added rule: "For Docker builds, see docs/deployment.md"
   • Added rule: "For Redis, see docs/architecture.md#caching"
   • Output format configured
✅ Template Validation Passed
📊 Created: .claude/agents/builder.md (72 lines)
   • Focus areas added as REFERENCES, not content
```

### Error Case
```
/creating-builder-agent
```

**Output when CLAUDE.md missing:**
```
❌ Pre-Flight Validation Failed
   ❌ CLAUDE.md not found

ERROR: Cannot create builder agent without CLAUDE.md
Please create CLAUDE.md with your project's:
- Tech stack
- Architecture overview
- Coding standards
- Testing requirements

Run this skill again after creating CLAUDE.md.
```

## Quality Standards

**Target Output: 50-100 lines** (ultra-lean, mostly references)

**The Formula**:
- 10% mission statement
- 20% workflow steps
- 30% mission-specific rules (80%+ applicable only)
- 20% output format
- 20% references to CLAUDE.md and docs/

**Required**:
- Mission statement (2-3 lines)
- "Before Any Task" checklist with references
- Workflow (5 steps max)
- Builder-specific rules (5-8 items, 80%+ applicable)
- Output format section
- Anti-patterns table (5 items max)
- References section

**Red Flags (Output needs revision)**:
- Over 100 lines → too much duplication
- Contains coding standards → that's in CLAUDE.md
- Contains framework patterns → that's in docs/
- Contains tech stack details → that's in CLAUDE.md
- Generic advice that applies to any agent → remove it
- Missing output format → critical omission

**Validation Question**: For each line, ask "Is this builder-specific AND 80%+ applicable?" If no, delete it or move to reference.

## Tips

- **First Time Setup**: Run this after creating your `CLAUDE.md`
- **Updates**: Re-run when tech stack changes or new patterns emerge
- **Customization**: Use argument to add specific sections or patterns
- **Validation**: Always review generated file to ensure accuracy
- **Integration**: Builder will reference `CLAUDE.md` for up-to-date project context

## Integration

This skill is designed to:
1. **Live in user-level settings** at `~/.claude/skills/creating-builder-agent/` (the factory skill itself)
2. **Create project-specific agents** at `<project>/.claude/agents/builder.md` (the generated agent)
3. **Be invoked** by agent-author or directly by user
4. **Work with planner** agent (planner creates tasks, builder implements them)

The factory pattern workflow:
```
~/.claude/skills/creating-builder-agent/  ← Factory skill (user-level)
  ↓ invoked in project directory
<project>/.claude/agents/builder.md       ← Generated agent (project-level)
  ↓ used for building in this project
Builder implements tasks from prompt, returns completion status to main thread
```
