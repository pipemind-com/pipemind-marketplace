---
name: creating-planner-agent
description: Creates project-specific planner agent with task file creation standards
user-invocable: true
argument-hint: "optional: customization notes or task template preferences"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - WebFetch
  - WebSearch
model: sonnet
color: purple
---

# Creating Planner Agent

Creates a project-specific `planner.md` agent file customized for your tech stack and task management workflow, focused on creating detailed, actionable task files.

**IMPORTANT**: This skill creates a **PROJECT-level** agent at `<project>/.claude/agents/planner.md` (relative to current working directory), NOT in user-level settings (`~/.claude/`). This agent is specific to the current project's planning workflow.

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

**3. 🌐 Smart Context Loading** (#4):
   - Auto-detect tech stack from project files:
     - `package.json` → Node.js/JavaScript/TypeScript frameworks
     - `requirements.txt`, `pyproject.toml` → Python frameworks
     - `Cargo.toml` → Rust frameworks
     - `go.mod` → Go frameworks
   - Search web for framework architecture patterns
   - Fetch task management and planning best practices
   - Incorporate modern planning methodologies

**4. 📝 Generate Planner Agent**:
   - Create `.claude/agents/planner.md` with all required sections
   - Customize content based on project's architecture
   - Include task file creation standards
   - Apply any user-provided customization notes

**5. ✅ Template Validation** (#3):
   - Verify YAML frontmatter is valid
   - Check all 8 required sections are present
   - Ensure no placeholder text like `[PROJECT_NAME]` remains
   - Validate section content is populated
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

## Agent Template Sections

The generated `planner.md` agent will include these 8 core sections:

### 1. Model & Efficiency
When Sonnet is sufficient vs when to request elevated reasoning:
- Sonnet: Standard tasks, well-understood patterns
- Opus: Complex architecture decisions, novel problems, multi-system integration

### 2. Mission Statement
Creating builder-ready task files with optimal detail balance.

**Core Principle**: The planner's PRIMARY OUTPUT is task files (`tasks/XXX-name.md`) that enable builders to execute mechanically without making design decisions.

### 3. Project Context
Reference `CLAUDE.md` for architecture, always read it first:
- Architecture overview
- Tech stack details
- Coding standards
- Testing requirements
- Deployment workflows

### 4. Workflow
Planner's complete process:
1. **Read CLAUDE.md** - Understand project context
2. **Analyze Problem** - Which layers affected, root cause identification
3. **Explore Codebase** - Find patterns, similar implementations, existing solutions
4. **Design Solution** - Data flow, API contracts, component interactions
5. **Write Task File** - Detailed, actionable specifications
6. **Update PLAN.md** - If project uses planning document

### 5. Before Creating Task (REQUIRED Preparation)
Never create a task file without:
- Reading `tasks/TEMPLATE.md` (if exists)
- Reading `tasks/README.md` (if exists)
- Reviewing 2-3 example completed tasks
- Using `TEMPLATE.md` as base structure

### 6. Task File Requirements
Every task file must include:
- **Scope Boundaries**: What's in scope, what's explicitly out of scope
- **Testable Requirements**: Checkboxes for verification
- **Root Cause Analysis**: Diagrams showing problem and solution
- **Exact File Paths**: With line numbers for modifications
- **Complete Code Snippets**: With all necessary imports
- **Context**: Patterns to follow, gotchas to avoid, constraints to respect
- **Test Requirements**: Unit/integration/E2E test specifications
- **Deployment Order**: If multi-layer changes required

### 7. Quality Standards
Task files must be "just right":
- **Not Too Little**: Builder shouldn't need to make design decisions
- **Not Too Much**: Avoid overwhelming with unnecessary details
- **Builder Can Execute Without Questions**: The ultimate test

**Examples of Good vs Bad Detail Levels**:

❌ **Too Little**: "Add authentication to the API"
✅ **Just Right**: "Add JWT authentication middleware at `src/middleware/auth.ts` using the existing `verifyToken` helper from `src/utils/jwt.ts`. Apply to routes listed in section 3. See code example below."

❌ **Too Much**: 500 lines explaining JWT theory and 15 alternative approaches
✅ **Just Right**: Brief context on why JWT chosen (reference `CLAUDE.md`), then implementation details

### 8. After Creating Task
Completion checklist:
1. **Verify Task Quality**:
   - [ ] All required sections present
   - [ ] Code snippets are complete and runnable
   - [ ] File paths are exact with line numbers
   - [ ] Requirements are testable (checkboxes)
   - [ ] Builder can execute without questions
2. **Update PLAN.md** (if exists): Add task to roadmap
3. **Announce Creation**: Confirm task file location
4. **File Appropriately**: `tasks/active/` vs `tasks/backlog/`

## Critical Philosophy

**Planner thinks architecturally, builder executes mechanically.**

- Planner makes ALL design decisions
- Builder implements exactly what's specified
- No ambiguity or interpretation needed
- Task files are the contract between planner and builder

## Output

Creates `.claude/agents/planner.md` with:
- Complete YAML frontmatter (name, description, tools, model)
- All 8 core sections fully populated
- Project-specific planning patterns
- Task file creation standards
- Quality guidelines and examples
- Workflow integration

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

🌐 Smart Context Loading
   • Detected: TypeScript 5.0, Node.js 20
   • Fetching: Microservices planning patterns
   • Fetching: API-first design methodologies

📝 Generating Planner Agent
   • Creating: .claude/agents/planner.md
   • Sections: 8/8 populated
   • Lines: 294

✅ Template Validation
   ✅ YAML frontmatter valid
   ✅ All 8 sections present
   ✅ No placeholders remaining
   ✅ Content validated

📊 Results
   ✅ Created: .claude/agents/planner.md
   📦 Tech Stack: TypeScript, Node.js, PostgreSQL
   📝 Sections: Model & Efficiency, Mission Statement,
              Project Context, Workflow, Before Creating Task,
              Task File Requirements, Quality Standards,
              After Creating Task
```

### With Customization
```
/creating-planner-agent "Include database migration planning and async job queue patterns"
```

**Expected Output:**
```
✅ Pre-Flight Validation Passed
📖 Reading Project Context
🌐 Smart Context Loading
   • Added: Database migration planning patterns
   • Added: Async job queue design patterns (Bull, BullMQ)
📝 Generating Planner Agent (with custom sections)
✅ Template Validation Passed
📊 Created: .claude/agents/planner.md (318 lines)
   • Added database migration workflow section
   • Added async job queue planning patterns
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
