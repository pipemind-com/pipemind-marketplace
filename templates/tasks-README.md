# Task File System

This directory contains task files for the planner-builder agentic workflow.

## Structure

```
tasks/
├── README.md              # This file
├── TEMPLATE.md            # Template for new tasks
├── 000-example-task.md    # Reference example (if exists)
├── XXX-active-task.md     # Active tasks (being worked on)
├── backlog/
│   └── XXX-task.md        # Future tasks (not started)
└── completed/
    └── XXX-task.md        # Completed tasks (archived)
```

## Task File Naming Convention

- **Format**: `XXX-kebab-case-description.md`
- **XXX**: Three-digit sequential number (001, 002, 003, etc.)
- **Description**: Short, descriptive name in kebab-case

**Examples**:
- `001-add-user-authentication.md`
- `002-fix-cache-invalidation-bug.md`
- `003-implement-export-feature.md`

## Finding Next Task Number

```bash
# Find highest existing task number
ls tasks/*.md tasks/backlog/*.md tasks/completed/*.md 2>/dev/null | \
  grep -oE '[0-9]{3}' | sort -n | tail -1

# Next number is highest + 1
```

## Task Lifecycle

1. **Planning**: Planner creates `tasks/XXX-name.md`
2. **Active**: Task stays in `tasks/` while being worked on
3. **Implementation**: Builder updates "Builder" section with progress
4. **Completion**: Builder marks "Built & Tested" checkbox
5. **Archive**: Builder moves to `tasks/completed/XXX-name.md`

## Planner Responsibilities

The planner creates task files that enable builders to execute mechanically:

- ✅ Analyze root cause (not just symptoms)
- ✅ Design solution architecture
- ✅ Specify exact files and line numbers
- ✅ Provide complete code snippets with imports
- ✅ Document patterns, gotchas, constraints
- ✅ Define test requirements
- ✅ Specify deployment order (if multi-layer)

**Goal**: Builder should read once and execute to completion without questions.

## Builder Responsibilities

The builder implements according to the task file:

- ✅ Read task file completely before starting
- ✅ Implement according to specifications
- ✅ Write tests proactively (not just when asked)
- ✅ Document implementation in "Builder" section
- ✅ Note any deviations from plan (and why)
- ✅ Verify all acceptance criteria met
- ✅ Mark "Built & Tested" checkbox
- ✅ Move to `tasks/completed/` when done

**Goal**: Execute mechanically without making design decisions.

## Task File Structure

Every task file must have:

### Planner Section
- **Layers Affected**: Which parts of the system
- **Deployment Order**: Sequence if multi-layer
- **Requirements**: Testable checkboxes
- **Problem Analysis**: Root cause with current vs proposed architecture
- **Files to Modify**: Exact paths with line numbers
- **Implementation Steps**: Phases with complete code snippets
- **Context**: Patterns, gotchas, test requirements

### Builder Section
- **Implementation Notes**: What was actually built
- **Test Results**: Tests written and passed
- **Manual Verification**: Steps performed
- **Deviations from Plan**: Changes and rationale

### Status
- [ ] Planned (planner checks)
- [ ] Built & Tested (builder checks)

## Quality Standards

A task file is builder-ready when:
1. Builder can read it once and understand completely
2. Builder can execute without asking questions
3. Builder doesn't need to make design decisions
4. Builder has all code snippets needed
5. Builder knows how to test completion

**Detail Balance**: Not too little (builder must decide), not too much (builder drowns), just right (builder executes mechanically).

## Examples

See `000-example-task.md` or `tasks/completed/*` for reference examples of high-quality task files.
