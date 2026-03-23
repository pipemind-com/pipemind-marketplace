# pipemind-marketplace

A marketplace of Claude Code plugins. Install plugins once globally (`~/.claude/`), then use them across all your projects.

## Plugins

| Plugin | Description | Docs |
|--------|-------------|------|
| **spec-driven-development** | Self-replicating agentic workflow factory — compiles project-specific agents for any codebase | [README](plugins/spec-driven-development/README.md) |

## Installation

```bash
# Marketplace
claude plugin marketplace add pipemind-com/pipemind-marketplace

# Plugins
claude plugin install spec-driven-development@pipemind-marketplace
claude plugin install rust-lsp@pipemind-marketplace
claude plugin install typescript-lsp@pipemind-marketplace
```


## Support

For issues with Claude Code itself: https://github.com/anthropics/claude-code
