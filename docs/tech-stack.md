# Tech Stack

> **AI Context Summary**: Most plugins are pure markdown/YAML/JSON with no build step — agents and skills are
> markdown files with YAML frontmatter. MCP server plugins (e.g., `mcp-semantic-scholar`) are Rust crates
> that compile to binaries deployed via GitHub Actions. The 80% rule and 150-instruction limit are the primary
> engineering constraints when authoring agent/skill content.

## Languages and File Types

| Type | Format | Location |
|------|--------|----------|
| Agent files | Markdown + YAML frontmatter | `plugins/<name>/agents/*.md` |
| Skill files | Markdown + YAML frontmatter | `plugins/<name>/skills/<gerund>/SKILL.md` |
| Plugin manifest | JSON | `plugins/<name>/.claude-plugin/plugin.json` |
| Registry | JSON | `.claude-plugin/marketplace.json` |
| LSP config | JSON | `plugins/<name>/.lsp.json` |
| MCP server source | Rust | `plugins/<name>/src/` + `Cargo.toml` |
| MCP server binary | ELF/PE | `plugins/<name>/bin/` (committed, built by CI) |
| Installer | Bash | `install.sh`, `release.sh` |

## Agent File Format

```yaml
---
name: builder
description: Implements tasks from task files mechanically without design decisions
model: claude-opus-4-5
tools:
  - Read
  - Edit
  - Write
  - Bash
  - Glob
  - Grep
color: blue
---

# Agent instructions (markdown)
```

Constraints: 50-100 lines total. Model defaults to `claude-opus-4-5` for builders; `claude-sonnet-4-5` for planners.

## Skill File Format

```yaml
---
user-invocable: true
name: compiling-project-settings
description: Generates lean CLAUDE.md for any project
---

# Skill instructions (markdown)
```

Constraints: 100-200 lines. Name must be gerund form (e.g., `compiling-`, `defining-`, `reviewing-`). Stored at `plugins/<name>/skills/<gerund-name>/SKILL.md`.

## Plugin Manifest Format

### Markdown/YAML Plugin

```json
{
  "name": "spec-driven-development",
  "version": "1.1.2",
  "description": "...",
  "agents": ["planner", "builder"],
  "skills": ["compiling-project-settings"],
  "dependencies": []
}
```

### MCP Server Plugin

```json
{
  "name": "mcp-semantic-scholar",
  "version": "0.2.2",
  "description": "...",
  "agents": [],
  "skills": [],
  "dependencies": [],
  "mcpServers": {
    "mcp-semantic-scholar": {
      "command": "${CLAUDE_PLUGIN_ROOT}/bin/mcp-semantic-scholar",
      "env": { "S2_API_KEY": "${S2_API_KEY}" }
    }
  }
}
```

The `mcpServers` field wires the binary as an MCP server in Claude Code. `${CLAUDE_PLUGIN_ROOT}` resolves to the plugin's install directory.

Common fields:
- `name`: kebab-case, matches directory name
- `agents[]`: agent names without `.md` extension
- `skills[]`: skill directory names
- `dependencies[]`: other plugin names this depends on
- `optionalDependencies[]`: optional plugins that enhance behavior

## The 150-Instruction Limit

Claude Code reliably follows ~150 instructions total:
- System prompt: ~50 instructions (fixed overhead)
- CLAUDE.md + all loaded agents: ~100 remaining

**Impact on authoring**: CLAUDE.md targets 50-100 lines. Each agent targets 50-100 lines. Move niche content to `docs/` and reference it — agents load docs on demand.

## The 80% Rule

Every instruction in an agent or skill must apply to 80%+ of sessions. Instructions that apply to a minority of cases belong in `docs/`, loaded only when needed.

## Cross-References

- Architecture overview: [architecture.md](./architecture.md)
- Adding plugins: [getting-started.md](./getting-started.md)
- Agent authoring guide: `plugins/spec-driven-development/agents/agent-author.md`
