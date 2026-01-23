# Agentic Workflow Setup Guide

This repository includes a complete agentic workflow system with **planner** and **builder** agents that work together through a task file system.

## Quick Start

To set up the agentic workflow in a **new project**:

```bash
# 1. Copy bootstrap files to your new project
cp bootstrap-agentic.sh /path/to/new-project/
cp -r templates/ /path/to/new-project/

# 2. Navigate to new project
cd /path/to/new-project/

# 3. Run bootstrap (requires git init and Claude CLI)
./bootstrap-agentic.sh
```

The script will:
- ✅ Create directory structure (`tasks/`, `.claude/agents/`)
- ✅ Copy task templates (TEMPLATE.md, README.md, example)
- ✅ Generate `CLAUDE.md` (architecture overview)
- ✅ Generate `.claude/agents/planner.md` (using `agent-author` agent)
- ✅ Generate `.claude/agents/builder.md` (using `agent-author` agent)
- ✅ Validate the complete setup

**Total time**: ~2-5 minutes depending on Claude API speed.

## What Gets Created

```
your-project/
├── CLAUDE.md                      # Architecture overview, patterns, gotchas
├── .claude/
│   └── agents/
│       ├── planner.md             # Planning specialist agent
│       └── builder.md             # Implementation agent
├── tasks/
│   ├── TEMPLATE.md                # Template for new tasks
│   ├── README.md                  # Task system documentation
│   ├── 000-example-task.md        # Example task (placeholder)
│   ├── backlog/                   # Future tasks
│   └── completed/                 # Archived completed tasks
├── templates/                     # Bootstrap templates (optional to keep)
│   ├── README.md
│   ├── tasks-TEMPLATE.md
│   ├── tasks-README.md
│   └── tasks-000-example-task.md
└── bootstrap-agentic.sh           # Setup script (optional to keep)
```

## How It Works

### 1. Task-Driven Workflow

The workflow revolves around **task files** (`tasks/XXX-name.md`):

```
Planner Agent          Task File           Builder Agent
     ↓                     ↓                     ↓
  Analyzes          Created by planner    Reads task file
  Designs solution  Contains:             Implements mechanically
  Plans approach    - Problem analysis    Writes tests
     ↓              - Implementation      Documents work
  Writes task       - Code snippets       Marks complete
     ↓              - Context                ↓
  Ready for         - Test requirements   Moves to completed/
  builder              ↓
                   Builder can execute
                   without questions
```

### 2. Agent Separation of Concerns

**Planner Agent** (`claude --agent planner`):
- 🧠 **Thinks**: Analyzes problems, designs solutions
- 📝 **Plans**: Creates detailed task files
- 🎯 **Goal**: Builder can execute mechanically without decisions

**Builder Agent** (`claude --agent builder`):
- 🛠️ **Executes**: Implements according to task file
- ✅ **Tests**: Writes and runs tests proactively
- 📊 **Documents**: Records what was actually built
- 🎯 **Goal**: Mechanical execution, no design decisions

### 3. Task File Anatomy

Each task file has two main sections:

#### Planner Section (Written by planner)
- **Requirements**: Testable acceptance criteria
- **Problem Analysis**: Root cause, current vs proposed architecture
- **Files to Modify**: Exact paths with line numbers
- **Implementation Steps**: Phases with complete code snippets
- **Context**: Patterns, gotchas, test requirements

#### Builder Section (Written by builder during implementation)
- **Implementation Notes**: What was actually built
- **Test Results**: Tests written and passed
- **Manual Verification**: Steps performed
- **Deviations from Plan**: Changes and rationale

## Usage Examples

### Creating a Task

```bash
claude --agent planner -p "Create a task to add user authentication"
```

Planner will:
1. Read CLAUDE.md to understand architecture
2. Explore the codebase
3. Design the solution
4. Create `tasks/001-add-user-authentication.md`

### Implementing a Task

```bash
claude --agent builder -p "Implement task 001"
```

Builder will:
1. Read `tasks/001-add-user-authentication.md`
2. Implement according to specifications
3. Write tests proactively
4. Document in Builder section
5. Move to `tasks/completed/001-add-user-authentication.md`

### Ad-hoc Implementation (Without Task File)

```bash
claude --agent builder -p "Fix the typo in README.md line 42"
```

Builder can handle direct instructions for simple tasks that don't need planning.

## Architecture Overview (CLAUDE.md)

The `CLAUDE.md` file is the **single source of truth** for project architecture. Both agents reference it.

**What it contains:**
- Tech stack and layer communication
- Data flow diagrams
- Key patterns (with code examples)
- Anti-patterns to avoid
- Deployment strategy and order
- Testing strategy
- Common gotchas

**Why it matters:**
- Planner uses it to design solutions that fit the architecture
- Builder uses it to implement code that follows patterns
- Ensures consistency across all agent work

## Customization

### Before Bootstrap

Edit templates in `templates/` directory before running bootstrap:

```bash
# Customize task structure
vim templates/tasks-TEMPLATE.md

# Customize task documentation
vim templates/tasks-README.md

# Run bootstrap with your customizations
./bootstrap-agentic.sh
```

### After Bootstrap

1. **Review generated files**: Claude generates CLAUDE.md and agent definitions based on your codebase
2. **Customize for your needs**: Edit files to add project-specific patterns
3. **Create first real task**: Replace `tasks/000-example-task.md` with a real example

## Best Practices

### For Planners
- ✅ Always read CLAUDE.md first
- ✅ Provide exact file paths with line numbers
- ✅ Include complete code snippets with imports
- ✅ Show current vs proposed architecture
- ✅ Balance detail: not too little, not too much
- ❌ Don't leave design decisions to builder

### For Builders
- ✅ Read task file completely before starting
- ✅ Write tests proactively (not just when asked)
- ✅ Document deviations in Builder section
- ✅ Mark "Built & Tested" when complete
- ✅ Move to completed/ directory
- ❌ Don't make architectural decisions

### For Task Files
- ✅ Use sequential three-digit numbers (001, 002, 003)
- ✅ Use kebab-case descriptions (add-feature, fix-bug)
- ✅ Keep active tasks in `tasks/`
- ✅ Move completed to `tasks/completed/`
- ✅ Put future work in `tasks/backlog/`

## Troubleshooting

### Bootstrap Script Fails

**Problem**: Script exits with "Template directory not found"

**Solution**: Ensure you copied both `bootstrap-agentic.sh` AND `templates/` directory

**Problem**: "Claude CLI not found"

**Solution**: Install Claude Code CLI from https://github.com/anthropics/claude-code

**Problem**: "Not in a git repository"

**Solution**: Run `git init` first

### Agent Doesn't Follow Patterns

**Problem**: Builder makes design decisions instead of following task file

**Solution**:
1. Check if task file has enough detail (read tasks/README.md quality standards)
2. Ensure planner included complete code snippets
3. Verify exact file paths and line numbers are specified

**Problem**: Planner doesn't understand architecture

**Solution**:
1. Check if CLAUDE.md is comprehensive (run validation)
2. Explicitly tell planner to "read CLAUDE.md first"
3. Update CLAUDE.md with missing patterns

## Files You Can Delete After Bootstrap

Once bootstrap is complete, you can optionally remove:

- `bootstrap-agentic.sh` (setup is done)
- `templates/` directory (task files are already created)
- This `AGENTIC-SETUP.md` file (keep if you want reference)

**Keep these:**
- `CLAUDE.md` (agents need this!)
- `.claude/agents/` (planner.md, builder.md)
- `tasks/` directory (your workflow depends on this)

## Replicating in New Projects

To use this system in multiple projects:

1. **Keep a reference repository** with the bootstrap system
2. **Copy these files to new projects**:
   ```bash
   cp bootstrap-agentic.sh /new-project/
   cp -r templates/ /new-project/
   cp AGENTIC-SETUP.md /new-project/  # Optional
   ```
3. **Run bootstrap** in new project:
   ```bash
   cd /new-project
   ./bootstrap-agentic.sh
   ```

Each project gets a custom CLAUDE.md and agents tailored to its codebase!

## Philosophy

The agentic workflow is built on these principles:

1. **Separation of Concerns**: Planner thinks, builder executes
2. **Task Files as Contract**: Complete specification, no questions needed
3. **Optimal Detail**: "Just right" - builder knows exactly what to do
4. **Proactive Testing**: Tests are written alongside implementation
5. **Mechanical Execution**: Builder never makes design decisions
6. **Documentation Loop**: Builder records implementation reality

**The magic**: Planner does heavy analytical lifting so builder can execute autonomously to completion.

## Support

If you encounter issues or have improvements:

1. Check the validation report from bootstrap
2. Review tasks/README.md quality standards
3. Read CLAUDE.md for project-specific patterns
4. Consult .claude/agents/planner.md and builder.md

For questions about Claude Code itself, see: https://github.com/anthropics/claude-code
