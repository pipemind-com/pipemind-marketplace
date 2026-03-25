# mcp-semantic-scholar

MCP server that wraps the [Semantic Scholar API](https://api.semanticscholar.org/), giving Claude structured access to 200M+ academic papers with citation counts, open-access PDFs, and citation graph traversal.

**This is a BYOK (Bring Your Own Key) system.** You must supply your own free Semantic Scholar API key. The server will not start without one.

## Quick Start

### 1. Get your API key (free, takes ~1 minute)

Go to [semanticscholar.org/product/api](https://www.semanticscholar.org/product/api#api-key-form) and request a key. Approval is typically instant.

### 2. Build

```bash
cd plugins/mcp-semantic-scholar
cargo build --release
```

### 3. Install

```bash
./install.sh mcp-semantic-scholar --symlink
```

The installer will prompt for your API key and save it to `~/.claude/settings.json`. If you skip, the server is registered but won't work until you add the key.

## Adding or Changing Your API Key

Edit `~/.claude/settings.json` and set the key in the MCP server's `env` block:

```json
{
  "mcpServers": {
    "mcp-semantic-scholar": {
      "command": "/path/to/bin/mcp-semantic-scholar",
      "args": [],
      "env": {
        "S2_API_KEY": "YOUR_KEY_HERE"
      }
    }
  }
}
```

Restart Claude Code after changing the key.

**Never commit your API key to git.** The key lives only in `~/.claude/settings.json`, which is a local user config file outside the repo.

## Tools

### search_papers
Search for papers by keyword or natural language query. Returns titles, authors, citation counts, and open-access PDF links.

### get_paper
Get detailed information about a specific paper. Accepts Semantic Scholar ID, `DOI:10.xxx/xxx`, `ArXiv:2301.xxxxx`, or `CorpusId:12345`.

### get_references
Get papers cited BY a given paper (backward citation snowball). Useful for finding foundational work.

### get_citations
Get papers that CITE a given paper (forward citation snowball). Useful for finding recent follow-on work.

## Rate Limits

With a key, Semantic Scholar allows **1 request per second** across all endpoints. The server enforces this proactively (sleeps between requests) and also handles 429 responses with exponential backoff (1s, 2s, 4s + jitter, up to 3 retries).

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `S2_API_KEY` | **Yes** | Your Semantic Scholar API key |
| `RUST_LOG` | No | Log level for stderr diagnostics (default: `warn`) |

## Attribution

All tool responses include "Data provided by Semantic Scholar" per the [API license terms](https://www.semanticscholar.org/product/api/license).
