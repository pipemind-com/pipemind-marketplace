# Architecture

> **AI Context Summary**: The pipemind-marketplace is a two-tier plugin distribution system.
> The **registry tier** (`.claude-plugin/marketplace.json`) tracks plugin versions and metadata.
> The **plugin tier** (`plugins/<name>/`) holds self-contained agents, skills, docs, and optionally compiled
> binaries, installed into `~/.claude/` via `install.sh`. Three plugin types coexist: markdown/YAML plugins
> (agents + skills), LSP config plugins (`.lsp.json`), and MCP server plugins (Rust binaries built via CI).

## System Overview

```
pipemind-marketplace/
├── .claude-plugin/
│   └── marketplace.json          ← registry index (source of truth for versions)
├── .claude/
│   └── agents/                   ← project-specific planner + builder agents
├── plugins/
│   ├── spec-driven-development/              ← LEGACY layout (plugin.json at root)
│   │   ├── plugin.json
│   │   ├── agents/               ← .md agent files installed to ~/.claude/agents/
│   │   ├── skills/               ← skill dirs installed to ~/.claude/skills/
│   │   └── docs/                 ← markdown docs (not installed, for reading)
│   ├── rust-lsp/                 ← CURRENT layout (.claude-plugin/ manifest)
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   └── .lsp.json             ← LSP server configuration
│   ├── typescript-lsp/           ← CURRENT layout
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   └── .lsp.json
│   ├── scientific-method/        ← CURRENT layout (skills only, no agents)
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   └── skills/               ← research loop skills
│   └── mcp-semantic-scholar/     ← CURRENT layout (Rust MCP server)
│       ├── .claude-plugin/
│       │   └── plugin.json       ← includes mcpServers field
│       ├── src/                  ← Rust source
│       ├── Cargo.toml
│       └── bin/                  ← pre-compiled binaries committed to repo
├── specs/                        ← behavioral specs and domain glossary
├── install.sh                    ← CLI installer (symlink or copy)
└── release.sh                    ← version bump + tag + push (+ Cargo.toml sync)
```

## Plugin Types

### Markdown/YAML Plugins (agents + skills)

`spec-driven-development`, `scientific-method`. Pure markdown files with YAML frontmatter. No build step.

### LSP Config Plugins

`rust-lsp`, `typescript-lsp`. A `.lsp.json` configures the LSP server for the language. No build step.

### MCP Server Plugins (Rust binary)

`mcp-semantic-scholar`. A Rust crate that compiles to a binary installed into `~/.claude/` as an MCP server.
The manifest includes a `mcpServers` field that wires the binary as an MCP server in Claude Code:

```json
// plugins/mcp-semantic-scholar/.claude-plugin/plugin.json
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

Pre-compiled binaries live in `bin/` and are committed to the repo. GitHub Actions rebuilds them on each release tag.

## Plugin Layouts

### Current Layout (new plugins)

Manifest at `plugins/<name>/.claude-plugin/plugin.json`. `install.sh` requires this file. LSP plugins additionally have `.lsp.json` at plugin root. MCP server plugins additionally have `bin/` with pre-compiled artifacts.

### Legacy Layout (spec-driven-development only)

Manifest at `plugins/spec-driven-development/plugin.json`. Install is handled separately — see `plugins/spec-driven-development/README.md`.

## Install Flow

```
install.sh <plugin> [--symlink]
      │
      ├─ reads plugins/<plugin>/.claude-plugin/plugin.json (validates existence)
      ├─ resolves agents/ and skills/ source dirs
      │
      ├─ --symlink mode:
      │     ln -sf <plugin>/agents/*.md ~/.claude/agents/<name>.md
      │     ln -sf <plugin>/skills/<dir>/ ~/.claude/skills/<dir>/
      │
      └─ copy mode:
            cp -r agents/ ~/.claude/agents/
            cp -r skills/ ~/.claude/skills/
```

Symlink mode is preferred: `git pull` propagates changes to all machines with zero reinstall.

## Release Flow

```
release.sh <plugin> <patch|minor|major>
      │
      ├─ validates clean git tree
      ├─ validates plugin in .claude-plugin/marketplace.json
      ├─ bumps version in .claude-plugin/marketplace.json
      ├─ bumps version in plugins/<plugin>/.claude-plugin/plugin.json
      ├─ syncs Cargo.toml version (if Cargo.toml present)
      ├─ git commit + tag <plugin>/v<version>
      └─ git push --follow-tags
             │
             └─ GitHub Actions (release.yml) triggers on tag push
                   ├─ detects Cargo.toml → builds Rust binary
                   ├─ cross-compiles for linux-x64 and windows-x64
                   └─ commits binaries to plugins/<name>/bin/
```

Tags follow the format `<plugin>/v<semver>` (e.g., `mcp-semantic-scholar/v0.2.2`).

## Registry

`.claude-plugin/marketplace.json` is the authoritative registry. It lists all plugins with name, version, source path, and description. `release.sh` is the only tool that should mutate versions in this file.

## Cross-References

- Setup: [getting-started.md](./getting-started.md)
- Plugin file formats: [tech-stack.md](./tech-stack.md)
- Agent/skill authoring: `plugins/spec-driven-development/agents/agent-author.md`
