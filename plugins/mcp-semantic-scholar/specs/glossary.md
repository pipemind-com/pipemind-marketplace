# Domain Glossary

## Actors

**End User**
A human who installs the mcp-semantic-scholar plugin into their Claude Code environment. Responsible for obtaining and configuring their own Semantic Scholar API key. Interacts with the server indirectly through Claude's tool-calling interface.
*Cannot:* invoke MCP tools directly (only the LLM client does); modify server behavior at runtime; share their API key through the server.

**LLM Client**
The Claude model instance that connects to the MCP server over stdio and invokes tools via JSON-RPC. The primary consumer of all tool output. Sends structured tool calls and receives markdown responses.
*Cannot:* bypass rate limiting; access the API key value; modify server configuration; send requests outside the 4 defined tools.

**Semantic Scholar API**
The upstream external service at api.semanticscholar.org providing the Academic Graph API. Enforces its own rate limits (1 request per second per key), returns structured JSON, and requires attribution in downstream outputs.
*Cannot:* be controlled by this server; guarantee uptime or response times; be assumed to return all fields for all papers.

**Installer**
The human or script running `./install.sh mcp-semantic-scholar` to register the server in the Claude Code environment. May or may not have an API key at install time.
*Cannot:* skip MCP server registration (it always registers); install without `jq` available on PATH.

## Key Terms

**BYOK (Bring Your Own Key)**
The distribution model where the server ships without any embedded API credentials. Each end user must obtain their own free Semantic Scholar API key and configure it in their local Claude settings.

**Proactive Throttle**
The server-side rate limiter that enforces a minimum interval (1.05 seconds) between outbound API requests, preventing 429 responses before they occur. Operates via a shared mutex tracking the timestamp of the last request.

**Reactive Backoff**
The retry mechanism triggered when the upstream API returns HTTP 429. Retries up to 3 times with exponential delay (1s, 2s, 4s) plus random jitter per attempt.

**Attribution Footer**
The mandatory text `\n---\n*Data provided by Semantic Scholar*` appended to every tool response, per Semantic Scholar's API license terms.

**Paper Identifier**
A string that resolves to a single paper in the Semantic Scholar corpus. Accepted formats: raw S2 paper ID, `DOI:10.xxx/xxx`, `ArXiv:2301.xxxxx`, `CorpusId:12345`.

**Citation Snowball**
The technique of traversing a paper's citation graph. *Backward snowball* follows references (papers cited by the target). *Forward snowball* follows citations (papers that cite the target).

**Open Access Status**
The Semantic Scholar classification of a paper's availability: `GREEN` (author-hosted), `BRONZE` (free on publisher site), `GOLD` (open-access journal), `HYBRID`, or `CLOSED`. When available, includes a direct PDF URL and license identifier.
