# Project Documentation

> **AI Context Summary**: Documentation for the agentic workflow factory—a two-tier markdown/YAML
> system that installs once globally and compiles project-specific Claude Code agents on demand.
> 4 documents covering architecture, setup, workflow, and tech stack. Start with
> `getting-started.md` to install, then `workflow.md` to understand agent orchestration.

## Documents

| Document | Description |
|----------|-------------|
| [Architecture](./architecture.md) | Two-tier factory/product design, component breakdown, data flow |
| [Getting Started](./getting-started.md) | Installation (symlink/copy), verification, common issues |
| [Workflow](./workflow.md) | Planner→Builder pattern, skill invocation, task file structure |
| [Tech Stack](./tech-stack.md) | YAML frontmatter format, model selection, tool tiers, size limits |

## Suggested Reading Order

1. **[Getting Started](./getting-started.md)** — Install the factory to `~/.claude/`
2. **[Architecture](./architecture.md)** — Understand the two-tier system
3. **[Workflow](./workflow.md)** — Learn the planner/builder pattern
4. **[Tech Stack](./tech-stack.md)** — Reference for authoring agents and skills

## Quick Links

- Full workflow and usage examples: `README.md`
- Agent authoring guide: `agents/agent-author.md`
- Skill source files: `skills/<gerund-name>/SKILL.md`
