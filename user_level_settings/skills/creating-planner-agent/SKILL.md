---
name: creating-planner-agent
description: Creates lean project-specific planner agent (50-100 lines)
user-invocable: true
argument-hint: "optional: customization notes or task template preferences"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Bash
model: sonnet
color: purple
---

# Creating Planner Agent

Creates an **ultra-lean** project-specific `planner.md` agent (50-100 lines) that references CLAUDE.md and `docs/` instead of duplicating content.

**Core Philosophy**:
- **Reference, don't duplicate** - CLAUDE.md has context, docs/ has patterns
- **80% rule** - Only include instructions that apply to 80%+ of planning tasks
- **Mission-specific only** - No general advice (that's in CLAUDE.md)

**IMPORTANT**: Generated agent at `<project>/.claude/agents/planner.md` should be ~50-100 lines of mission-specific instructions with references to existing documentation.

## When Invoked

This skill will:

**1. ✅ Pre-Flight Validation** (#1):
   - Check if `CLAUDE.md` exists (FAIL if missing - required for context)
   - Check if `.claude/agents/planner.md` already exists (WARN but allow override)
   - Verify `CLAUDE.md` contains architecture and project context
   - Report validation status

**2. 📖 Read Project Context**:
   - Read `CLAUDE.md` to understand architecture and patterns
   - Extract task management workflow (if documented)
   - Identify project structure and conventions

**3. 🔍 Tech Stack Detection**:
   - Auto-detect from project files:
     - `package.json` → Node.js/TypeScript
     - `requirements.txt`, `pyproject.toml` → Python
     - `Cargo.toml` → Rust
     - `go.mod` → Go
   - Use patterns from existing codebase (no web fetching needed)

**4. 📝 Generate Planner Agent**:
   - Create `.claude/agents/planner.md` with all required sections
   - Customize content based on project's architecture
   - Include task file creation standards
   - Apply any user-provided customization notes

**5. ✅ Template Validation** (#3):
   - Verify YAML frontmatter is valid
   - Check ultra-lean structure (Mission, Workflow, Requirements, References)
   - **Target: 50-100 lines** (references, not content)
   - Ensure no duplicated content from CLAUDE.md or docs/
   - Verify each instruction is 80%+ applicable to planning tasks
   - Report validation results

**6. 📊 Report Results**:
   - Confirm file creation location
   - List included sections
   - Report any warnings or issues

## Arguments

**Optional**: Customization notes or task template preferences
- Example: `"Focus on microservices architecture planning"`
- Example: `"Include API-first design methodology"`
- Example: `"Add database migration planning patterns"`
- Default: Uses only what's in `CLAUDE.md` and auto-detected context

## Agent Template (Target: 50-100 lines)

The generated `planner.md` agent will be **ultra-lean** with mostly references:

```markdown
# Planner Agent

## Mission
Create task files that builders execute without questions. All design decisions made here.

## Before Any Task
1. Read CLAUDE.md (architecture, tech stack, patterns)
2. For architecture details: see docs/architecture.md
3. For tech constraints: see docs/tech-stack.md
4. Check tasks/TEMPLATE.md if exists
5. Review 1-2 completed tasks for format

## Workflow
1. Analyze problem (which layers affected?)
2. Explore codebase (find similar patterns)
3. Design solution (data flow, API contracts)
4. Write task file with exact file paths
5. Verify: "Can builder execute without questions?"

## Task File Must Include (80%+ of tasks)
- Scope: what's in/out
- File paths with line numbers
- Code snippets with imports
- Test requirements

## Quality Check
❌ "Add authentication" → Too vague
✅ "Add JWT middleware at `src/auth/middleware.ts:15`" → Actionable

## References
- Architecture: docs/architecture.md
- Tech stack: docs/tech-stack.md
- Patterns: CLAUDE.md ## Patterns
- Task template: tasks/TEMPLATE.md
```

**That's it.** ~50-80 lines. No duplicated content.

## Critical Philosophy

**Planner thinks architecturally, builder executes mechanically.**

- Planner makes ALL design decisions
- Builder implements exactly what's specified
- No ambiguity or interpretation needed
- Task files are the contract between planner and builder

## Output

Creates `.claude/agents/planner.md` with:
- YAML frontmatter (name, description, model, tools)
- Ultra-lean structure (50-100 lines total)
- References to CLAUDE.md, docs/, tasks/TEMPLATE.md
- Mission-specific workflow and requirements only
- One quality example (not comprehensive guidelines)

## Examples

### Basic Usage
```
/creating-planner-agent
```

**Expected Output:**
```
✅ Pre-Flight Validation
   ✅ CLAUDE.md exists
   ⚠️  planner.md already exists - will override
   ✅ Architecture found: Microservices, API-first

📖 Reading Project Context
   • Architecture: API-first with microservices
   • Tech stack: Node.js, TypeScript, PostgreSQL
   • Task workflow: tasks/active/ → completed/

🔍 Tech Stack Detection
   • Detected: TypeScript 5.0, Node.js 20
   • Patterns from: existing codebase + CLAUDE.md

📝 Generating Planner Agent
   • Creating: .claude/agents/planner.md
   • Structure: Mission + Workflow + Requirements + References
   • Lines: 58 (within 50-100 target)

✅ Template Validation
   ✅ YAML frontmatter valid
   ✅ Ultra-lean structure (58 lines)
   ✅ No duplicated content from CLAUDE.md
   ✅ References docs/ and tasks/TEMPLATE.md

📊 Results
   ✅ Created: .claude/agents/planner.md (58 lines)
   📝 Structure: Mission, Before Task, Workflow, Requirements, Quality, References
   🔗 References: CLAUDE.md, docs/architecture.md, tasks/TEMPLATE.md
```

### With Customization
```
/creating-planner-agent "Include database migration planning and async job queue patterns"
```

**Expected Output:**
```
✅ Pre-Flight Validation Passed
📖 Reading Project Context
📝 Generating Planner Agent
   • Added reference: "For migrations, see docs/database.md"
   • Added reference: "For job queues, see docs/architecture.md#jobs"
✅ Template Validation Passed
📊 Created: .claude/agents/planner.md (63 lines)
   • Focus areas added as REFERENCES, not content
```

### Error Case
```
/creating-planner-agent
```

**Output when CLAUDE.md missing:**
```
❌ Pre-Flight Validation Failed
   ❌ CLAUDE.md not found

ERROR: Cannot create planner agent without CLAUDE.md
Please create CLAUDE.md with your project's:
- Architecture overview
- Tech stack
- Project structure
- Task management workflow

Run this skill again after creating CLAUDE.md.
```

## Quality Standards

**Target Output: 50-100 lines** (ultra-lean, mostly references)

**The Formula**:
- 10% mission statement
- 20% workflow steps
- 30% task file requirements (80%+ applicable only)
- 40% references to CLAUDE.md, docs/, and tasks/TEMPLATE.md

**Required**:
- Mission statement (2-3 lines)
- "Before Any Task" checklist with references
- Workflow (5 steps max)
- Task file requirements (essential only)
- One quality example (Too Little vs Just Right)
- References section

**Red Flags (Output needs revision)**:
- Over 100 lines → too much duplication
- Lists all possible task file sections → reference TEMPLATE.md instead
- Contains architecture details → that's in docs/architecture.md
- Contains coding standards → that's in CLAUDE.md
- Generic planning advice → remove it

**Validation Question**: For each line, ask "Is this planner-specific AND 80%+ applicable?" If no, delete it or move to reference.

## Tips

- **First Time Setup**: Run this after creating your `CLAUDE.md`
- **Updates**: Re-run when architecture changes or new planning patterns emerge
- **Customization**: Use argument to add specific planning methodologies
- **Validation**: Always review generated file to ensure accuracy
- **Task Templates**: Create `tasks/TEMPLATE.md` for consistent task file structure
- **Integration**: Planner will reference `CLAUDE.md` for up-to-date project context
- **Pairing**: Use with `/creating-builder-agent` to establish complete workflow

## Integration

This skill is designed to:
1. **Live in user-level settings** at `~/.claude/skills/creating-planner-agent/` (the factory skill itself)
2. **Create project-specific agents** at `<project>/.claude/agents/planner.md` (the generated agent)
3. **Be invoked** by agent-author or directly by user
4. **Work with builder** agent (planner creates tasks, builder implements them)

The factory pattern workflow:
```
~/.claude/skills/creating-planner-agent/  ← Factory skill (user-level)
  ↓ invoked in project directory
<project>/.claude/agents/planner.md       ← Generated agent (project-level)
  ↓ used for planning in this project
Planner creates task files specific to this codebase
```
