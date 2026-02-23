---
name: creating-planner-agent
description: "Creates lean project-specific planner agent (50-100 lines). Use when setting up task planning for a project's agentic workflow."
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

Creates a project-specific `planner.md` agent at `.claude/agents/planner.md`.

**Core philosophy**: Reference, don't duplicate. CLAUDE.md has project context, `docs/` has patterns. The planner agent should be 50-100 lines of mission-specific instructions with pointers to existing documentation.

**Arguments** (optional): Customization notes or task template preferences.
- Example: `"Focus on microservices architecture planning"`
- Example: `"Add database migration planning patterns"`
- Default: Uses only CLAUDE.md and auto-detected context.

---

## Execution Steps

### 1. Pre-Flight Validation
- **CLAUDE.md must exist.** If missing, report the error below and stop:
  ```
  ❌ Cannot create planner agent without CLAUDE.md
  Please create CLAUDE.md with: architecture overview, tech stack, project structure, coding standards.
  ```
- **Check `.claude/agents/planner.md`** — warn if it exists, but allow override.
- **Verify CLAUDE.md contains architecture and project context.**

### 2. Read Project Context
- Read `CLAUDE.md` for architecture, patterns, conventions.
- Identify project structure and architectural style.

### 3. Tech Stack Detection
Auto-detect from project files (no web fetching):
- `package.json` → Node.js/TypeScript
- `requirements.txt` / `pyproject.toml` → Python
- `Cargo.toml` → Rust
- `go.mod` → Go

Cross-reference with CLAUDE.md. Detection supplements what's documented — doesn't override it.

### 4. Check for `docs/` References
Scan for available documentation files (`docs/architecture.md`, `docs/tech-stack.md`, `docs/database.md`, etc.). Only include references to files that actually exist. If `docs/` is empty or absent, omit the references — don't point the planner at files that aren't there.

### 5. Generate Planner Agent
Create `.claude/agents/planner.md` using the template below. Customize based on:
- Detected tech stack and architecture
- Patterns found in CLAUDE.md
- User-provided customization notes (if any)
- Available `docs/` files

Model selection: Default to `sonnet`. Note in output if the project's architectural complexity might warrant a different choice.

### 6. Validate Output
Before writing the file, verify:
- YAML frontmatter is valid.
- Total length is 50-100 lines.
- Every instruction passes the **80% test**: "Is this planner-specific AND applicable to 80%+ of planning tasks?" If not, delete it or convert to a reference.
- No content duplicated from CLAUDE.md or docs/.
- Output format section is present and includes architectural decision fields (state management, error strategy, dependency design).
- Design Constraints section is present.
- Workflow includes design quality verification step.
- Quality check shows both specificity *and* design quality.

If validation fails, revise before writing.

### 7. Report Results
```
✅ Pre-Flight Validation: [status]
📖 Project Context: [architecture style, tech stack, key patterns]
📝 Generated: .claude/agents/planner.md ([N] lines)
   Sections: [list]
   References: [list of linked files]
   ⚠️  [any warnings]
```

---

## Planner Agent Template

This is the structural template. Populate each section with project-specific content — do not use placeholder text.

```markdown
---
name: planner
description: Designs solutions and produces task descriptions for builder
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
model: sonnet
---

# Planner Agent

## Mission
Receive feature/bug via prompt. Make all design decisions. Return a task description detailed enough that a builder can execute without interpretation. Planner owns architecture — builder owns implementation.

## Before Any Task
1. Read CLAUDE.md (architecture, tech stack, patterns)
2. Read the full feature/bug description from prompt
[3-N. Conditional references to docs/ files that actually exist in this project]

## Design Constraints
When designing solutions: prefer stateless data flow with side effects at system boundaries; decompose so each unit is testable in isolation without complex mocking; match abstraction level to actual complexity — don't introduce patterns ahead of need; define explicit error handling strategy at trust boundaries; specify dependency direction (who depends on whom).

## Workflow
1. Analyze the feature/bug from prompt
2. Explore codebase — find similar patterns, understand existing conventions
3. Design solution (data flow, state management, API contracts, error strategy)
4. Verify design quality: "Would this pass review on purity, testability, and abstraction fitness?"
5. Write detailed task description using Output Format below
6. Verify task completeness: "Can builder execute this without making any design decisions?"

## Task Description Must Include
- Scope: what's in and what's explicitly out
- File paths (with line numbers where relevant)
- Code snippets with imports for non-trivial logic
- State management approach (where state lives, how it flows)
- Error handling strategy (what fails, how it's caught, what surfaces to user)
- Dependency design (new modules, injection points, who depends on whom)
- Test requirements (what to test, expected behaviors)

## Output Format
'''
## Task: [title]
## Scope
In: [what to implement]
Out: [what NOT to touch]
## Design Decisions
- State: [where state lives, data flow]
- Errors: [handling strategy]
- Dependencies: [new/modified, direction]
## Files to Modify
- path/file.ext:line - what to change and why
## Implementation Steps
[ordered steps with code snippets where non-trivial]
## Tests
[what to test, expected behaviors, edge cases]
'''

## Quality Check
❌ "Add authentication" → Too vague, no design decisions
❌ "Add JWT middleware at src/auth/middleware.ts using shared global token cache" → Specific but poor design (shared mutable state)
✅ "Add stateless JWT middleware at src/auth/middleware.ts:15 — validates token per-request, no shared state; inject via app.use(); errors return 401 with structured error body" → Specific AND sound design

## References
- Project context: CLAUDE.md
[additional references to docs/ files that exist]
```

---

## Red Flags (Revise if any are true)

- **Over 100 lines** → duplicating content that belongs in CLAUDE.md or docs/
- **Contains architecture details, coding standards, or tech stack specifics** → those live in references
- **Generic planning advice applicable to any agent** → not planner-specific, remove it
- **Missing output format or design constraints** → critical omissions
- **Task description template lacks architectural fields** (state, errors, dependencies) → builder will have to make design decisions, defeating the planner's purpose
- **Quality check only tests specificity, not design quality** → planner will produce detailed but architecturally flawed plans

---
