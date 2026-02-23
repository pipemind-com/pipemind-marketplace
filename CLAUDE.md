# Project Context

This repo is the **agentic workflow factory**: install it globally once (`~/.claude/`), then use its skills to compile project-specific agents for any codebase. Treat the skills and agents here as software—edit them with the same rigor you'd apply to production code.

## About This Project

Pure markdown/YAML system—no build pipeline, no runtime dependencies. Two tiers: **factory** (`user_level_settings/`) lives globally and creates agents; **products** (`.claude/agents/`) are compiled per-project. All agents reference CLAUDE.md rather than duplicating context.

## Key Directories

- `user_level_settings/agents/` - Meta-agent (`agent-author.md`) that guides agent creation
- `user_level_settings/skills/` - 13 factory skills (installed to `~/.claude/skills/`)
- `docs/` - Progressive disclosure documentation (architecture, workflow, tech-stack, getting-started)
- `.claude/` - Local permissions config (`settings.local.json`)

## Installation

```bash
# Copy (or symlink for auto-updates via git pull)
cp -r user_level_settings/agents ~/.claude/
cp -r user_level_settings/skills ~/.claude/

# Symlink alternative (keeps in sync with repo)
ln -sf "$(pwd)/user_level_settings/agents" ~/.claude/agents
ln -sf "$(pwd)/user_level_settings/skills" ~/.claude/skills
```

## Standards

- **Agent files**: 50-100 lines, YAML frontmatter with `name` (kebab-case noun), `description`, `model`, `tools`, `color`
- **Skill files**: 100-200 lines, YAML frontmatter with `user-invocable: true` and `name` in gerund form (`creating-foo`)
- **80% rule**: every instruction must apply to 80%+ of sessions for that agent; move niche content to `docs/`
- **Reference, don't duplicate**: agents point to CLAUDE.md and `docs/`; never copy content across files
- **150 instruction limit**: Claude Code's system prompt uses ~50; CLAUDE.md + all agents share the remaining ~100

## Notes

- NEVER add `Co-Authored-By` lines to commits (explicitly forbidden in `committing-changes` skill)
- Symlinks are preferred over copying—`git pull` then propagates updates to all machines automatically
- When adding a new skill, place it under `user_level_settings/skills/<gerund-name>/SKILL.md`
- Skills listed in `system-reminder` are live; changes take effect immediately without restart

## Additional Documentation

Before specific tasks, read relevant documentation:
- Full workflow and skill descriptions: `README.md`
- Agent authoring patterns: `user_level_settings/agents/agent-author.md`
- Architecture deep-dive: `docs/architecture.md`
- Installation and setup: `docs/getting-started.md`
- Planner/builder workflow: `docs/workflow.md`
- YAML format and constraints: `docs/tech-stack.md`
- Docs overview: `docs/index.md`
