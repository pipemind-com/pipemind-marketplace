# Getting Started

> **AI Context Summary**: Install the factory once per machine by symlinking or copying
> `user_level_settings/` to `~/.claude/`. Then bootstrap any project by invoking the
> initializing-* and compiling-* skills inside that project. Symlinks are preferred—`git pull` propagates
> factory updates automatically. Requires Claude Code CLI and a git repository.

## Prerequisites

- Claude Code CLI installed and authenticated
- Git repository (factory skills require `git rev-parse --is-inside-work-tree`)
- No language runtime required—pure markdown/YAML system

## Step 1: Install the Global Factory (Once Per Machine)

```bash
# Navigate to this repo
cd /path/to/claude-agentic

# Option A: Symlink (recommended — git pull auto-updates)
mkdir -p ~/.claude
ln -sf "$(pwd)/user_level_settings/agents" ~/.claude/agents
ln -sf "$(pwd)/user_level_settings/skills" ~/.claude/skills

# Option B: Copy (manual updates required)
cp -r user_level_settings/agents ~/.claude/
cp -r user_level_settings/skills ~/.claude/

# Verify
ls ~/.claude/agents/agent-author.md          # meta-agent
ls ~/.claude/skills/*/SKILL.md               # 13 skills
```

**Windows (PowerShell):**
```powershell
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\agents" `
  -Target "$(Get-Location)\user_level_settings\agents"
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills" `
  -Target "$(Get-Location)\user_level_settings\skills"
```

## Step 2: Bootstrap a Project

In any git repository with Claude Code:

```bash
# 1. Generate CLAUDE.md (lean project context)
/initializing-project-settings

# 2. Generate docs/ (progressive disclosure)
/initializing-project-docs

# 3. Compile project-specific agents
/compiling-planner-agent
/compiling-builder-agent

# Optional specialized agents
/compiling-security-agent
/compiling-devops-agent
```

Each skill analyzes the codebase and generates files tailored to the tech stack.

## Step 3: Verify the Setup

```bash
# Check factory installation
ls ~/.claude/agents/agent-author.md
ls ~/.claude/skills/

# Check compiled products
ls .claude/agents/planner.md
ls .claude/agents/builder.md
cat CLAUDE.md | head -20    # Should show project-specific content
```

**Test agents interactively:**
```bash
claude --agent planner
# > List available tasks

claude --agent builder
# > Show me the current tech stack
```

## Common Issues

| Problem | Solution |
|---------|----------|
| `Command not found: /compiling-planner-agent` | Skills must be at `~/.claude/skills/<name>/SKILL.md` |
| "agent-author not found" | Complete Step 1 first; restart Claude CLI |
| Skills show generic output | Ensure CLAUDE.md exists before running compiling-*-agent |
| Builder uses wrong test framework | Update CLAUDE.md testing section, re-run `/compiling-builder-agent` |

## Updating the Factory

```bash
# If using symlinks — just pull!
git pull   # ~/.claude/agents and ~/.claude/skills update automatically

# If using copies — re-copy after pulling
git pull
cp -r user_level_settings/agents ~/.claude/
cp -r user_level_settings/skills ~/.claude/
```

## Cross-References

- System overview: [architecture.md](./architecture.md)
- Planner/builder workflow: [workflow.md](./workflow.md)
- Agent/skill format reference: [tech-stack.md](./tech-stack.md)
