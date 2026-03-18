# Project Context

This repo is the **agentic-marketplace**: a collection of Claude Code plugins (agents + skills) installable into `~/.claude/`. Each plugin lives under `plugins/<name>/` and is self-contained.

## About This Project

Pure markdown/YAML system — no build pipeline, no runtime dependencies. Plugins ship agents and skills; users install them once globally, then use the skills to compile project-specific agents for any codebase.

## Key Directories

- `plugins/` - All marketplace plugins
- `plugins/pm-workflow/` - Agentic workflow factory plugin (agents + skills + docs)
- `marketplace.json` - Plugin registry index
- `install.sh` - CLI installer
- `.claude/` - Local permissions config (`settings.local.json`)

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

## Plugin Standards

- **`plugin.json`**: `name` (kebab-case), `version`, `description`, `agents[]`, `skills[]`, `dependencies[]`
- **Agent files**: 50-100 lines, YAML frontmatter with `name`, `description`, `model`, `tools`, `color`
- **Skill files**: 100-200 lines, YAML frontmatter with `user-invocable: true`, `name` in gerund form
- **80% rule**: every instruction must apply to 80%+ of sessions; move niche content to `docs/`
- **150 instruction limit**: Claude Code's system prompt uses ~50; CLAUDE.md + all agents share the remaining ~100

## Notes

- NEVER add `Co-Authored-By` lines to commits
- Symlinks are preferred — `git pull` propagates updates to all machines
- When adding a skill to `pm-workflow`, place it under `plugins/pm-workflow/skills/<gerund-name>/SKILL.md`
- Skills listed in `system-reminder` are live; changes take effect immediately without restart

## Additional Documentation

- Full workflow and skill descriptions: `README.md`
- pm-workflow agent authoring: `plugins/pm-workflow/agents/agent-author.md`
- Architecture deep-dive: `plugins/pm-workflow/docs/architecture.md`
- Installation and setup: `plugins/pm-workflow/docs/getting-started.md`
- Planner/builder workflow: `plugins/pm-workflow/docs/workflow.md`
- YAML format and constraints: `plugins/pm-workflow/docs/tech-stack.md`
