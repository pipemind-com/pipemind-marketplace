# Workflow

> **AI Context Summary**: The core pattern is Planner → Builder separation of concerns: planner
> designs and writes task files, builder reads task files and implements mechanically. The main
> thread orchestrates by spawning agents via `claude --agent <name>` interactively, or via the
> Task tool in automated pipelines. Task tracking uses Claude Code's native TaskCreate/TaskUpdate/
> TaskList/TaskGet tools in the main thread.

## Planner → Builder Pattern

```
Main Thread / User
       │
       ├─► claude --agent planner
       │         ↓
       │   Reads CLAUDE.md + docs/
       │   Analyzes codebase
       │   Writes tasks/NNN-name.md (full spec)
       │         ↓
       ├─► claude --agent builder
       │         ↓
       │   Reads tasks/NNN-name.md
       │   Implements mechanically
       │   Writes tests, marks complete
       │   Moves to tasks/completed/
       │
       ├─► (optional) claude --agent security
       └─► (optional) claude --agent devops
```

## Separation of Concerns

| Agent | Mindset | Does | Never Does |
|-------|---------|------|-----------|
| **Planner** | Analytical | Designs, plans, writes task files | Write production code |
| **Builder** | Mechanical | Implements, tests, documents | Make design decisions |
| **Security** | Adversarial | Audits, finds vulnerabilities | Fix application logic |
| **DevOps** | Operational | Infrastructure, CI/CD, containers | Modify app code |

## Task File Structure

Task files live at `tasks/NNN-description.md` and are the contract between planner and builder.

```markdown
# Task: Add User Authentication

## Requirements
- [ ] JWT tokens with 15-minute expiry
- [ ] Refresh token rotation on use

## Problem Analysis
Current state: no auth middleware
Proposed: auth.ts middleware + /auth routes

## Files to Modify
- `src/routes/auth.ts` (create)
- `src/middleware/auth.ts` (create)
- `src/app.ts:42` (register middleware)

## Implementation Steps
### Phase 1: Auth middleware
```typescript
// src/middleware/auth.ts
export const authMiddleware = ...
```

## Builder Section
<!-- Builder fills this in during implementation -->
- Implementation notes
- Test results
- Deviations from plan
```

## Skill Invocation

Skills are invoked as slash commands in the main Claude Code session:

```bash
# Full project compilation (one command)
/compiling-agentic-workflow

# Or individual compilation steps
/compiling-project-settings
/compiling-project-docs

# Agent factory skills
/compiling-planner-agent
/compiling-builder-agent
/compiling-security-agent
/compiling-devops-agent

# Utility skills (can pass arguments)
/git-commit-changes
/conducting-post-mortem tasks/completed/001-auth.md
/stress-testing src/auth/login.ts
/reviewing-code-quality
/defining-specs
/defining-test-scenarios
```

Skills listed in `system-reminder` are live—changes to SKILL.md take effect without restart.

## Main Thread Task Tracking

When orchestrating multiple agents, use native task tools in the main thread:

```
TaskCreate  → register a new feature/bug to implement
TaskUpdate  → mark in_progress when spawning builder, completed when done
TaskList    → see all pending/in-progress/completed work
TaskGet     → fetch full task description before delegating
```

**Example orchestration sequence:**
1. `TaskCreate` with feature description
2. Spawn planner: `Task(subagent_type: general-purpose, prompt: "@\"planner (agent)\"\n\n{task description}")`
3. Planner returns task file path
4. `TaskUpdate` status to `in_progress`
5. Spawn builder: `Task(subagent_type: general-purpose, prompt: "@\"builder (agent)\"\n\n{planner output}")`
6. Builder returns completion status
7. `TaskUpdate` status to `completed`

## Post-Task Learning Loop

```bash
# After completing major tasks, extract lessons
/conducting-post-mortem tasks/completed/NNN-name.md

# This proposes updates to CLAUDE.md
# Review and apply updates to improve future agent performance
```

## Complete Development Lifecycle

```
/compiling-agentic-workflow   ← Full project compilation (or run steps individually below)
        ↓
claude --agent planner       ← Design: write task files
claude --agent builder       ← Build: implement + test
/git-commit-changes          ← Commit: atomic git commits
claude --agent security      ← Audit: find vulnerabilities
claude --agent devops        ← Deploy: infra configuration
/conducting-post-mortem      ← Learn: improve CLAUDE.md
```

## Automated Orchestration via `/orchestrating-workflow`

For multi-part features, the `/orchestrating-workflow` skill automates the full planner-to-builder pipeline:

```
/orchestrating-workflow "Add user authentication with JWT, refresh tokens, and role-based access"
```

This replaces the manual sequence of spawning individual planner and builder agents. The skill:

1. **Decomposes** the feature into 2-6 independent sub-tasks
2. **Plans** each sub-task via parallel planner subagents
3. **Reconciles** plans for file conflicts and interface dependencies
4. **Builds** via parallel builder subagents (respecting dependency order)
5. **Reports** completion status with files modified and test results

Use `/orchestrating-workflow` when a feature spans multiple files or components and benefits from parallel execution. For single-file changes, the manual planner → builder pattern above is simpler.

## Gotchas

**Spawning project-level agents via Task tool**: Using `subagent_type: "planner"` or `subagent_type: "builder"` does NOT work — the Task tool only accepts built-in type names (Bash, general-purpose, Explore, Plan, etc.). To instantiate a compiled project agent with its full identity (color, model, tools), use `subagent_type: general-purpose` and begin the prompt with `@"planner (agent)"` or `@"builder (agent)"`. Claude Code resolves the `@"<name> (agent)"` reference to `.claude/agents/<name>.md`.

**Compiled agents need `color` in frontmatter**: Without a `color` field in the agent's YAML frontmatter, the agent runs correctly but shows no colored tag in the UI. The `compiling-planner-agent` and `compiling-builder-agent` skills include `color: purple` and `color: blue` respectively in their templates.

**Parallel = multiple Task calls in one response**: Sending two `Task` tool calls in the same response runs them concurrently. Sending them in separate responses serializes them. Always batch all unblocked agents into a single response.

## Cross-References

- Architecture overview: [architecture.md](./architecture.md)
- Agent/skill format: [tech-stack.md](./tech-stack.md)
- Installation: [getting-started.md](./getting-started.md)
