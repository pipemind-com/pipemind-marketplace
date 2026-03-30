# mcp-semantic-scholar

MCP server that wraps the [Semantic Scholar API](https://api.semanticscholar.org/), giving Claude structured access to 200M+ academic papers with citation counts, open-access PDFs, and citation graph traversal.

**This is a BYOK (Bring Your Own Key) system.** You must supply your own free Semantic Scholar API key. The server will not start without one.

## Quick Start

### 1. Get your API key (free, takes ~1 minute)

Go to [semanticscholar.org/product/api](https://www.semanticscholar.org/product/api#api-key-form) and request a key. Approval is typically instant.

### 2. Add your API key to `~/.bashrc`

```bash
echo 'export S2_API_KEY=your_key_here' >> ~/.bashrc
source ~/.bashrc
```

Replace `your_key_here` with your actual key.

### 3. Install via the marketplace

```bash
claude plugin marketplace add pipemind-com/pipemind-marketplace
claude plugin install mcp-semantic-scholar@pipemind-marketplace
```

**Never commit your API key to git.**

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
