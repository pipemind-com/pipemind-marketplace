# Quick Reference

> **For comprehensive documentation, see [README.md](README.md)**. This is a condensed reference for experienced users.

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
| `agent-author` | `/creating-claude-settings` | Generate CLAUDE.md architecture overview | Phase 3 |
| `agent-author` | `/creating-planner-agent` | Generate `.claude/agents/planner.md` | Phase 4 |
| `agent-author` | `/creating-builder-agent` | Generate `.claude/agents/builder.md` | Phase 5 |
| `agent-author` | `/creating-security-agent` | Generate `.claude/agents/security.md` (optional) | Phase 6 |
| `agent-author` | `/creating-devops-agent` | Generate `.claude/agents/devops.md` (optional) | Phase 7 |
| (default) | (custom prompt) | Validate complete setup | Final |

**Note**:
- Agent creation uses the specialized `agent-author` agent for best results
- All generation skills are project-aware and will adapt to the codebase
- Security and DevOps agents are optional - use `--security`, `--devops`, or `--full` flags

## Related Skills (Not in Bootstrap)

These skills are for using the agentic workflow after bootstrap:

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `/conducting-post-mortem` | Analyze what went wrong | After failed implementation or bug |
| `/verifying-implementation` | Verify code works correctly | After builder completes implementation |

## Quick Start

```bash
# For a new project (core agents: planner + builder)
cp bootstrap-agentic.sh /new-project/
cp -r templates/ /new-project/
cd /new-project/
./bootstrap-agentic.sh

# With optional agents
./bootstrap-agentic.sh --security    # Also generate security agent
./bootstrap-agentic.sh --devops      # Also generate devops agent
./bootstrap-agentic.sh --full        # Generate all agents (planner, builder, security, devops)
```

## Bootstrap Flags

| Flag | Description |
|------|-------------|
| (none) | Generate core agents only (planner + builder) |
| `--security` | Also generate security auditor agent |
| `--devops` | Also generate DevOps/infrastructure agent |
| `--full` | Generate all agents (equivalent to `--security --devops`) |
| `-h`, `--help` | Show usage help |

## What Gets Created

```
project/
├── CLAUDE.md
├── .claude/agents/
│   ├── planner.md
│   ├── builder.md
│   ├── security.md      # (with --security or --full)
│   └── devops.md        # (with --devops or --full)
└── tasks/
    ├── TEMPLATE.md
    ├── README.md
    ├── 000-example-task.md
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

See [README.md - Troubleshooting](README.md#-troubleshooting) for comprehensive issue resolution.

## Philosophy

See [README.md - Philosophy](README.md#philosophy) for the complete philosophy explanation.

---

**Note**: This is a portable system - copy `bootstrap-agentic.sh` and `templates/` to any new project and run to set up the agentic workflow.
