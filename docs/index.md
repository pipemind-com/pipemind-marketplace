# Documentation Index

Reference documentation for the pipemind-marketplace repo. Read `CLAUDE.md` first for project context, then load whichever doc is relevant to your current task.

## Documents

| Document | When to read |
|----------|-------------|
| [architecture.md](./architecture.md) | Understanding plugin types, layout, install flow, registry structure |
| [getting-started.md](./getting-started.md) | Adding a new plugin (markdown or Rust MCP server), releasing |
| [tech-stack.md](./tech-stack.md) | Agent/skill/manifest file formats, MCP server manifest, 80% rule, 150-instruction limit |
| [workflow.md](./workflow.md) | Developing plugins using planner/builder agents, MCP server dev loop, release workflow |

## spec-driven-development Plugin Docs

The `spec-driven-development` plugin has its own detailed docs at `plugins/spec-driven-development/docs/`:

| Document | Content |
|----------|---------|
| `architecture.md` | Factory vs product tier, component breakdown |
| `workflow.md` | Planner/builder task file format and patterns |
| `getting-started.md` | Installing and using spec-driven-development |
| `tech-stack.md` | Agent/skill YAML format constraints |
