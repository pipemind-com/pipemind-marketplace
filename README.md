# agentic-marketplace

A marketplace of Claude Code plugins. Install plugins once globally (`~/.claude/`), then use them across all your projects.

## Plugins

| Plugin | Description | Docs |
|--------|-------------|------|
| **pm-workflow** | Self-replicating agentic workflow factory — compiles project-specific agents for any codebase | [README](plugins/pm-workflow/README.md) |

## Installation

```bash
# Symlink (recommended — git pull auto-updates)
./install.sh pm-workflow --symlink

# Copy
./install.sh pm-workflow
```

## Adding a Plugin

1. Create `plugins/<plugin-name>/` with `plugin.json`, `agents/`, `skills/`, `docs/`
2. Add an entry to `marketplace.json`
3. `install.sh` picks it up automatically

## Support

For issues with Claude Code itself: https://github.com/anthropics/claude-code
