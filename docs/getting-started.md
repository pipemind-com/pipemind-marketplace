# Getting Started

> **AI Context Summary**: The marketplace is installed via `claude plugin marketplace add` (native) or
> `./install.sh` (manual). Symlink installs are strongly preferred — they auto-update on `git pull`.
> Prerequisites are minimal: `jq` (for `release.sh`) and Claude Code. New plugins require a
> `.claude-plugin/plugin.json` manifest before `install.sh` will recognize them. MCP server plugins
> additionally require pre-built binaries in `bin/` (built by GitHub Actions on release).

## Prerequisites

| Tool | Required for | Install |
|------|-------------|---------|
| Claude Code | Running agents and skills | `npm install -g @anthropic-ai/claude-code` |
| `jq` | `release.sh` only | `apt install jq` / `brew install jq` |
| `bash` 4+ | `install.sh`, `release.sh` | Pre-installed on Linux/macOS |
| Rust + Cargo | Developing MCP server plugins locally | `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \| sh` |

## Installing the Marketplace

### Native (recommended)

```bash
claude plugin marketplace add pipemind-com/pipemind-marketplace
claude plugin install spec-driven-development@pipemind-marketplace
claude plugin install rust-lsp@pipemind-marketplace
claude plugin install typescript-lsp@pipemind-marketplace
claude plugin install mcp-semantic-scholar@pipemind-marketplace
```

### Manual (via this repo)

```bash
git clone <repo-url>
cd pipemind-marketplace

# Symlink install (recommended — git pull auto-updates)
./install.sh spec-driven-development --symlink

# Copy install
./install.sh spec-driven-development
```

Verify the install:
```bash
ls ~/.claude/agents/
ls ~/.claude/skills/
```

## Adding a New Plugin

### Markdown/YAML Plugin (agents + skills)

1. Create the plugin directory:

```bash
mkdir -p plugins/<name>/.claude-plugin
mkdir -p plugins/<name>/agents
mkdir -p plugins/<name>/skills
```

2. Create `.claude-plugin/plugin.json`:

```json
{
  "name": "<kebab-case-name>",
  "version": "0.1.0",
  "description": "One-line description",
  "agents": [],
  "skills": [],
  "dependencies": []
}
```

3. Add the plugin entry to `.claude-plugin/marketplace.json`.

4. Add agents (`plugins/<name>/agents/*.md`) and skills (`plugins/<name>/skills/<gerund>/SKILL.md`).

5. Test install: `./install.sh <name> --symlink`

### MCP Server Plugin (Rust binary)

1. Create the plugin directory and scaffold the Rust crate:

```bash
mkdir -p plugins/<name>/.claude-plugin
cd plugins/<name>
cargo init --name <name>
```

2. Add the `mcpServers` field to `.claude-plugin/plugin.json`:

```json
{
  "name": "<name>",
  "version": "0.1.0",
  "description": "...",
  "agents": [],
  "skills": [],
  "dependencies": [],
  "mcpServers": {
    "<name>": {
      "command": "${CLAUDE_PLUGIN_ROOT}/bin/<name>",
      "env": {}
    }
  }
}
```

3. Build locally and commit the binary:

```bash
cd plugins/<name>
cargo build --release
mkdir -p bin
cp target/release/<name> bin/<name>
git add bin/<name>
```

4. GitHub Actions will rebuild binaries automatically on each release tag.

## Releasing a Plugin

```bash
# Requires clean working tree
./release.sh <plugin-name> patch   # 0.1.0 → 0.1.1
./release.sh <plugin-name> minor   # 0.1.0 → 0.2.0
./release.sh <plugin-name> major   # 0.1.0 → 1.0.0
```

`release.sh` bumps both the plugin manifest and the marketplace registry, syncs `Cargo.toml` if present, commits, tags, and pushes. For MCP server plugins, GitHub Actions then builds and commits platform binaries.

## Cross-References

- Plugin structure and file formats: [tech-stack.md](./tech-stack.md)
- Architecture and install flow: [architecture.md](./architecture.md)
