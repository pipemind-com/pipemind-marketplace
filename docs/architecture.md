# Architecture

> **AI Context Summary**: The agentic-marketplace is a two-tier plugin distribution system with no runtime
> dependencies. The **registry tier** (`.claude-plugin/marketplace.json`) tracks plugin versions and metadata.
> The **plugin tier** (`plugins/<name>/`) holds self-contained agents, skills, and docs installed into
> `~/.claude/` via `install.sh`. Two plugin layouts coexist: legacy (`pm-workflow`, root `plugin.json`) and
> current (`.claude-plugin/plugin.json`).

## System Overview

```
agentic-marketplace/
├── .claude-plugin/
│   └── marketplace.json          ← registry index (source of truth for versions)
├── .claude/
│   └── agents/                   ← project-specific planner + builder agents
├── plugins/
│   ├── pm-workflow/              ← LEGACY layout (plugin.json at root)
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
│   └── scientific-method/        ← CURRENT layout (skills only, no agents)
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── skills/               ← research loop skills (refining, hypotheses, etc.)
├── specs/                        ← behavioral specs and domain glossary
├── install.sh                    ← CLI installer (symlink or copy)
└── release.sh                    ← version bump + git tag + push
```

## Plugin Layouts

### Current Layout (new plugins)

Manifest lives at `plugins/<name>/.claude-plugin/plugin.json`. `install.sh` requires this file. LSP plugins additionally have a `.lsp.json` at plugin root.

```json
// plugins/rust-lsp/.claude-plugin/plugin.json
{
  "name": "rust-lsp",
  "version": "0.1.1",
  "description": "...",
  "agents": [],
  "skills": [],
  "dependencies": []
}
```

### Legacy Layout (pm-workflow only)

Manifest lives at `plugins/pm-workflow/plugin.json`. `install.sh` reads from `.claude-plugin/plugin.json` which does not exist for `pm-workflow` — install for pm-workflow is handled separately. See `plugins/pm-workflow/README.md` for details.

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
      ├─ git commit + tag <plugin>/v<version>
      └─ git push --follow-tags
```

Tags follow the format `<plugin>/v<semver>` (e.g., `pm-workflow/v1.0.2`).

## Registry

`.claude-plugin/marketplace.json` is the authoritative registry. It lists all plugins with name, version, source path, and description. `release.sh` is the only tool that should mutate versions in this file.

## Cross-References

- Setup: [getting-started.md](./getting-started.md)
- Plugin file formats: [tech-stack.md](./tech-stack.md)
- Agent/skill authoring: `plugins/pm-workflow/agents/agent-author.md`
