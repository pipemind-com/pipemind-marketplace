# Project Context

**Mission:** Ship a self-replicating agentic workflow factory that developers install once globally and use to compile project-specific Claude Code agents for any codebase.

This plugin lives at `plugins/spec-driven-development/` in the pipemind-marketplace repo. It installs to `~/.claude/` (global factory tier) and compiles per-project agents (product tier). Pure markdown/YAML — no build pipeline, no runtime dependencies.

## About This Project

Markdown + YAML system. Factory tier: `agents/` (meta-agent) + `skills/` (14 compilation/utility skills). Product tier: compiled `.claude/agents/planner.md`, `builder.md`, etc. per project. Skills use YAML frontmatter (`user-invocable: true`), agents use YAML frontmatter with `model`/`tools`/`color`.

## Key Directories

- `agents/` — Factory meta-agents (agent-author.md)
- `skills/<gerund-name>/SKILL.md` — 14 skills; each in its own subdirectory
- `docs/` — Progressive-disclosure reference docs
- `specs/` — Behavioral specs for the plugin itself

## Standards

- **Agent files**: 50-100 lines, YAML frontmatter: `name` (kebab noun), `model`, `tools`, `color`
- **Skill files**: 100-200 lines, YAML frontmatter: `name` (gerund), `user-invocable: true`
- **80% rule**: every instruction must apply to 80%+ of sessions — move niche content to `docs/`
- **150 instruction limit**: CLAUDE.md + all loaded agents share ~100 instructions; stay lean
- **No Co-Authored-By** lines in commits

## Notes

- No package manager, no build step — edit markdown files directly
- New skills go in `skills/<gerund-name>/SKILL.md`; new agents go in `agents/<kebab-noun>.md`
- Symlink install preferred: `git pull` propagates changes to all machines automatically
- The `agent-author` meta-agent guides creation of new agents and skills — use it

## Additional Documentation

Before specific tasks, read the relevant doc:
- System design and data flow: `docs/architecture.md`
- YAML frontmatter formats, model selection, tool tiers: `docs/tech-stack.md`
- Planner/builder pattern, skill invocation: `docs/workflow.md`
- Install and verification: `docs/getting-started.md`
- Agent authoring guide: `agents/agent-author.md`
