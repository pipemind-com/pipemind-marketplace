# Getting Started

> **AI Context Summary**: The marketplace is installed via `claude plugin marketplace add` (native) or
> `./install.sh` (manual). Symlink installs are strongly preferred — they auto-update on `git pull`.
> Prerequisites are minimal: `jq` (for `release.sh`) and Claude Code. New plugins require a
> `.claude-plugin/plugin.json` manifest before `install.sh` will recognize them.

## Prerequisites

| Tool | Required for | Install |
|------|-------------|---------|
| Claude Code | Running agents and skills | `npm install -g @anthropic-ai/claude-code` |
| `jq` | `release.sh` only | `apt install jq` / `brew install jq` |
| `bash` 4+ | `install.sh`, `release.sh` | Pre-installed on Linux/macOS |

## Installing the Marketplace

### Native (recommended)

```bash
claude plugin marketplace add pipemind-com/pipemind-marketplace
claude plugin install spec-driven-development@pipemind-marketplace
claude plugin install rust-lsp@pipemind-marketplace
claude plugin install typescript-lsp@pipemind-marketplace
```

### Manual (via this repo)

```bash
git clone <repo-url>
cd claude-agentic

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

1. Create the plugin directory with the required structure:

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

3. Add the plugin entry to `.claude-plugin/marketplace.json`:

```json
{
  "name": "<name>",
  "source": "./plugins/<name>",
  "version": "0.1.0",
  "description": "One-line description"
}
```

4. Add agents (`plugins/<name>/agents/*.md`) and skills (`plugins/<name>/skills/<gerund>/SKILL.md`) as needed.

5. Test install: `./install.sh <name> --symlink`

## Releasing a Plugin

```bash
# Requires clean working tree
./release.sh <plugin-name> patch   # 0.1.0 → 0.1.1
./release.sh <plugin-name> minor   # 0.1.0 → 0.2.0
./release.sh <plugin-name> major   # 0.1.0 → 1.0.0
```

`release.sh` bumps both the plugin manifest and the marketplace registry, commits, tags, and pushes.

## Cross-References

- Plugin structure and file formats: [tech-stack.md](./tech-stack.md)
- Architecture and install flow: [architecture.md](./architecture.md)
