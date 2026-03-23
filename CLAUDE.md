# Project Context

**Mission:** Ship a curated marketplace of Claude Code plugins (agents + skills) that any developer can install once globally and use across all their projects.

This repo is the **agentic-marketplace**: self-contained plugins installable into `~/.claude/`. Each plugin lives under `plugins/<name>/` and ships its own agents, skills, and docs.

## About This Project

Pure markdown/YAML system — no build pipeline, no runtime dependencies. The `install.sh` CLI handles symlink or copy installs. Plugins use a `.claude-plugin/plugin.json` manifest; legacy `spec-driven-development` uses `plugin.json` at the plugin root.

## Key Directories

- `plugins/` - All marketplace plugins
- `plugins/spec-driven-development/` - Agentic workflow factory (agents + skills + docs); legacy layout
- `plugins/rust-lsp/` - Rust LSP config plugin (`.claude-plugin/` layout)
- `plugins/typescript-lsp/` - TypeScript LSP config plugin (`.claude-plugin/` layout)
- `plugins/scientific-method/` - Scientific method research loop plugin (`.claude-plugin/` layout)
- `.claude-plugin/marketplace.json` - Authoritative registry of all published plugins
- `.claude/agents/` - Project-specific planner and builder agents
- `specs/` - Behavioral specs and domain glossary
- `install.sh` - CLI installer (symlink or copy)
- `release.sh` - Version bump and tag helper

## Commands

```bash
./install.sh <plugin> --symlink  # Install plugin as symlink (recommended)
./install.sh <plugin>            # Install plugin as copy
./release.sh                     # Cut a release
```

## Standards

- **Plugin manifest**: `.claude-plugin/plugin.json` with `name` (kebab-case), `version`, `description`, `agents[]`, `skills[]`, `dependencies[]`
- **Agent files**: 50-100 lines, YAML frontmatter with `name`, `description`, `model`, `tools`, `color`
- **Skill files**: 100-200 lines, YAML frontmatter with `user-invocable: true`, `name` in gerund form
- **80% rule**: every instruction must apply to 80%+ of sessions; move niche content to `docs/`
- **150 instruction limit**: Claude Code's system prompt uses ~50; CLAUDE.md + agents share the remaining ~100

## Notes

- NEVER add `Co-Authored-By` lines to commits
- Symlinks are preferred — `git pull` propagates updates to all machines
- Skills listed in `system-reminder` are live; changes take effect immediately without restart
- When adding a skill to `spec-driven-development`, place it under `plugins/spec-driven-development/skills/<gerund-name>/SKILL.md`
- New plugins: use `.claude-plugin/plugin.json`; `spec-driven-development` uses legacy root `plugin.json`

## Workflow

When implementing multi-part features (new plugin, new skill set, complex refactor):
1. Spawn a planner agent (`claude --agent planner`) with the feature request
2. Planner designs structure, returns a task description with exact file paths and specs
3. Spawn a builder agent (`claude --agent builder`) with the task description
4. Builder creates files exactly as specified; reports blockers rather than guessing

## Additional Documentation

Before specific tasks, read the relevant doc:
- Architecture and install flow: `docs/architecture.md`
- Adding plugins, releasing: `docs/getting-started.md`
- Agent/skill/manifest formats: `docs/tech-stack.md`
- Developing plugins with planner/builder agents: `docs/workflow.md`
- spec-driven-development agent authoring: `plugins/spec-driven-development/agents/agent-author.md`
- Full workflow and skill descriptions: `README.md`
