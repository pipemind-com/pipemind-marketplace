---
name: creating-builder-agent
description: Creates project-specific builder agent with coding standards and workflows
user-invocable: true
argument-hint: "optional: customization notes or tech stack details"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - WebFetch
  - WebSearch
model: sonnet
color: blue
---

# Creating Builder Agent

Creates a project-specific `builder.md` agent file customized for your tech stack, including coding standards, task workflows, and testing patterns.

**IMPORTANT**: This skill creates a **PROJECT-level** agent at `<project>/.claude/agents/builder.md` (relative to current working directory), NOT in user-level settings (`~/.claude/`). This agent is specific to the current project's coding standards and tech stack.

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

**3. 🌐 Smart Context Loading** (#4):
   - Auto-detect tech stack from project files:
     - `package.json` → Node.js/JavaScript/TypeScript frameworks
     - `requirements.txt`, `pyproject.toml` → Python frameworks
     - `Cargo.toml` → Rust frameworks
     - `go.mod` → Go frameworks
   - Search web for framework-specific best practices
   - Fetch official documentation patterns
   - Incorporate modern idioms and conventions

**4. 📝 Generate Builder Agent**:
   - Create `.claude/agents/builder.md` with all required sections
   - Customize content based on project's tech stack
   - Include project-specific patterns from `CLAUDE.md`
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

**Optional**: Customization notes or additional context
- Example: `"Focus on Python FastAPI patterns"`
- Example: `"Include React Server Components best practices"`
- Example: `"Add Docker deployment workflow"`
- Default: Uses only what's in `CLAUDE.md` and auto-detected context

## Agent Template Sections

The generated `builder.md` agent will include these 8 core sections:

### 1. Scope
What the builder is responsible for across all layers/stacks of the project.

### 2. Coding Guidelines
References from `CLAUDE.md`:
- Core principles (Human-Centric, Least Surprise, Strict Typing, etc.)
- Architecture patterns
- Key implementation patterns with code examples
- Anti-patterns to avoid (table format)

### 3. Language/Framework Patterns
- Modern language features (e.g., Python 3.12+, TypeScript 5.0+ patterns)
- Component structure examples
- Data fetching patterns
- Form handling
- State management

### 4. Framework-Specific Patterns
Customized for your stack (e.g., Supabase, FastAPI, Next.js, Django):
- Edge Function structure
- Database queries and ORM patterns
- Migration format
- Service integration
- API route patterns

### 5. Task File System
- How to read task files from `tasks/` directory
- Task workflow: read → implement → complete → move to `completed/`
- Task completion checklist
- How to update task status

### 6. When Invoked Workflow
Builder's step-by-step process:
1. Read task file (if applicable)
2. Understand context and requirements
3. Implement incrementally
4. Write tests proactively (critical!)
5. Run tests and verify passing
6. Lint and format code
7. Integration verification
8. Document changes and mark task complete

### 7. Testing Standards
- Test framework patterns for each layer
- Code examples for unit/integration/E2E tests
- How to run tests (`npm test`, `pytest`, etc.)
- Coverage requirements
- Test organization patterns

### 8. Project Commands
References `CLAUDE.md` for:
- Development server commands
- Build commands
- Test commands
- Deployment commands
- Database migration commands

## Critical Philosophy

**Builder executes mechanically, never analyzes or makes design decisions.**

All architectural thinking, planning, and design decisions are the planner's job. The builder implements exactly what's specified in task files without deviation or interpretation.

## Output

Creates `.claude/agents/builder.md` with:
- Complete YAML frontmatter (name, description, tools, model)
- All 8 core sections fully populated
- Project-specific patterns and examples
- Framework-specific best practices
- Task file system integration
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

🌐 Smart Context Loading
   • Detected: Python 3.12, FastAPI 0.109
   • Fetching: FastAPI best practices
   • Fetching: Supabase Python client patterns

📝 Generating Builder Agent
   • Creating: .claude/agents/builder.md
   • Sections: 8/8 populated
   • Lines: 287

✅ Template Validation
   ✅ YAML frontmatter valid
   ✅ All 8 sections present
   ✅ No placeholders remaining
   ✅ Content validated

📊 Results
   ✅ Created: .claude/agents/builder.md
   📦 Tech Stack: Python, FastAPI, Supabase
   📝 Sections: Scope, Coding Guidelines, Language Patterns,
              Framework Patterns, Task System, Workflow,
              Testing Standards, Project Commands
```

### With Customization
```
/creating-builder-agent "Include Docker deployment patterns and Redis caching"
```

**Expected Output:**
```
✅ Pre-Flight Validation Passed
📖 Reading Project Context
🌐 Smart Context Loading
   • Added: Docker best practices
   • Added: Redis Python patterns
📝 Generating Builder Agent (with custom sections)
✅ Template Validation Passed
📊 Created: .claude/agents/builder.md (312 lines)
   • Added Docker deployment section
   • Added Redis caching patterns
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
Builder implements code following project-specific standards
```
