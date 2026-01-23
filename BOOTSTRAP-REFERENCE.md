# Bootstrap Script Reference

## Files in This Repository

### Bootstrap Scripts
- **`bootstrap-agentic.sh`** - Complete one-command setup (RECOMMENDED)
- `init-agentic-repo.sh` - Directory structure only
- `init-agentic-agents.sh` - Agent generation only

### Templates Directory (`templates/`)
- `tasks-TEMPLATE.md` - Task file structure template
- `tasks-README.md` - Task system documentation
- `tasks-000-example-task.md` - Example task placeholder
- `README.md` - Template directory docs

### Documentation
- `AGENTIC-SETUP.md` - Complete usage guide
- `BOOTSTRAP-REFERENCE.md` - This file (quick reference)

## Claude Code Skills Used

The bootstrap script uses these Claude Code skills:

| Agent | Skill | Purpose | Phase |
|-------|-------|---------|-------|
| (default) | (custom prompt) | Generate CLAUDE.md architecture overview | Phase 3 |
| `agent-author` | `/creating-planner-agent` | Generate `.claude/agents/planner.md` | Phase 4 |
| `agent-author` | `/creating-builder-agent` | Generate `.claude/agents/builder.md` | Phase 5 |
| (default) | (custom prompt) | Validate complete setup | Phase 6 |

**Note**:
- Agent creation uses the specialized `agent-author` agent for best results
- CLAUDE.md generation uses a custom prompt because it needs to analyze the specific codebase architecture
- The agent generation skills are project-aware and will adapt to the codebase

## Related Skills (Not in Bootstrap)

These skills are for using the agentic workflow after bootstrap:

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `/conducting-post-mortem` | Analyze what went wrong | After failed implementation or bug |
| `/verifying-implementation` | Verify code works correctly | After builder completes implementation |

## Quick Start

```bash
# For a new project
cp bootstrap-agentic.sh /new-project/
cp -r templates/ /new-project/
cd /new-project/
./bootstrap-agentic.sh
```

## What Gets Created

```
project/
├── CLAUDE.md                    # Architecture (Phase 3)
├── .claude/agents/
│   ├── planner.md              # Planning agent (Phase 4)
│   └── builder.md              # Builder agent (Phase 5)
└── tasks/
    ├── TEMPLATE.md             # From templates/ (Phase 2)
    ├── README.md               # From templates/ (Phase 2)
    ├── 000-example-task.md     # From templates/ (Phase 2)
    ├── backlog/
    └── completed/
```

## Typical Workflow After Bootstrap

1. **Create a task** (planner agent):
   ```bash
   claude --agent planner -p "Create a task to add user authentication"
   ```
   → Creates `tasks/001-add-user-authentication.md`

2. **Implement task** (builder agent):
   ```bash
   claude --agent builder -p "Implement task 001"
   ```
   → Reads task → implements → tests → moves to `tasks/completed/`

3. **Verify implementation**:
   ```bash
   claude -p "/verifying-implementation"
   ```
   → Runs tests, checks functionality

4. **Post-mortem** (if issues):
   ```bash
   claude -p "/conducting-post-mortem"
   ```
   → Analyzes what went wrong, suggests improvements

## Customization

### Before Bootstrap
Edit templates in `templates/` directory to customize structure.

### After Bootstrap
- Review generated `CLAUDE.md` and add project-specific patterns
- Update agent definitions in `.claude/agents/` if needed
- Replace `tasks/000-example-task.md` with real example after first task

## Troubleshooting

### "Template directory not found"
- Copy both `bootstrap-agentic.sh` AND `templates/` directory

### "Claude CLI not found"
- Install from https://github.com/anthropics/claude-code

### "Not in a git repository"
- Run `git init` first

### Skills not working
- Ensure Claude Code CLI is updated to latest version
- Skills are built into Claude Code (no setup needed)

## Philosophy

**Planner** (`/creating-planner-agent`):
- 🧠 Analyzes problems, designs solutions
- 📝 Creates detailed task files
- 🎯 Goal: Builder executes mechanically

**Builder** (`/creating-builder-agent`):
- 🛠️ Implements according to task file
- ✅ Writes tests proactively
- 📊 Documents what was built
- 🎯 Goal: Mechanical execution, no decisions

**Task File**: Complete contract between planner and builder.

---

**Note**: This is a portable system - copy `bootstrap-agentic.sh` and `templates/` to any new project and run to set up the agentic workflow.
