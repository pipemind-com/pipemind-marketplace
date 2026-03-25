# Spec: mcp-semantic-scholar — Semantic Scholar MCP Server
**Source:** Implementation plan at .claude/plans/starry-honking-crescent.md and built codebase
**Epic:** N/A — single spec
**Glossary:** specs/glossary.md
**Generated:** 2026-03-24
**Status:** REVIEWED — operator approved 2026-03-24

---

## System Constraints

- **SC-01**: The server MUST NOT start or accept tool calls without a valid, non-empty S2_API_KEY environment variable.
- **SC-02**: The server MUST NOT emit any output to stdout other than JSON-RPC messages. All diagnostic output goes to stderr.
- **SC-03**: Every tool response MUST end with the Attribution Footer, regardless of success or failure.
- **SC-04**: The server MUST NOT exceed 1 outbound request per 1.05 seconds to the Semantic Scholar API, measured across all tools.
- **SC-05**: The server MUST NOT expose raw JSON from the upstream API to the LLM Client. All output is formatted markdown.
- **SC-06**: The server MUST NOT persist any state between requests. It is fully stateless.
- **SC-07**: The API key MUST NOT appear in any tool response, log output, or error message.
- **SC-08**: The server binary MUST compile and run without any system-level runtime dependencies (no OpenSSL, no dynamic linking to system TLS). [ASSUMPTION: rustls is sufficient for all Semantic Scholar API endpoints]

---

## Feature Specs

### F-01: API Key Validation at Startup | MUST

**F-01.1: Server starts with valid key**
- **GIVEN** the environment variable S2_API_KEY is set to a non-empty string
- **WHEN** the server process starts
- **THEN** the server initializes the MCP protocol, responds to `initialize` JSON-RPC, and reports its name as "mcp-semantic-scholar" with tool capabilities enabled

**F-01.2: Server refuses to start without key**
- **GIVEN** the environment variable S2_API_KEY is unset
- **WHEN** the server process starts
- **THEN** the server prints an error to stderr containing the URL to obtain a key and instructions for where to configure it, then exits with code 1 without writing anything to stdout

**F-01.3: Server refuses to start with empty key**
- **GIVEN** the environment variable S2_API_KEY is set to an empty string
- **WHEN** the server process starts
- **THEN** the behavior is identical to F-01.2

---

### F-02: Paper Search | MUST

**F-02.1: Successful keyword search**
- **GIVEN** a valid API key and a connected LLM Client
- **WHEN** the LLM Client calls `search_papers` with query "neural scaling laws" and limit 3
- **THEN** the server returns a markdown response containing a numbered list of up to 3 papers, each showing title, authors, year, citation count, influential citation count, and S2 paper ID, ending with the Attribution Footer

**F-02.2: Search with pagination**
- **GIVEN** a search query that returns more results than the requested limit
- **WHEN** the LLM Client calls `search_papers` with limit 5
- **THEN** the response includes a "next page" line indicating the offset value to pass for the next page of results

**F-02.3: Search with no results**
- **GIVEN** a search query that matches no papers in the corpus
- **WHEN** the LLM Client calls `search_papers` with that query
- **THEN** the server returns a markdown response showing "0 results" — not an error — ending with the Attribution Footer

**F-02.4: Search with default parameters**
- **GIVEN** the LLM Client calls `search_papers` with only a query and no limit or offset
- **WHEN** the server processes the request
- **THEN** limit defaults to 10 and offset defaults to 0

**F-02.5: Search limit is clamped**
- **GIVEN** the LLM Client calls `search_papers` with limit 500
- **WHEN** the server processes the request
- **THEN** the limit is silently clamped to 100 (the API maximum)

**F-02.6: Empty or whitespace-only query is rejected**
- **GIVEN** the LLM Client calls `search_papers` with an empty string or whitespace-only query
- **WHEN** the server processes the request
- **THEN** the server returns an error message "Search query cannot be empty" without making an API call, ending with the Attribution Footer

---

### F-03: Paper Detail Lookup | MUST

**F-03.1: Lookup by S2 paper ID**
- **GIVEN** a valid S2 paper ID
- **WHEN** the LLM Client calls `get_paper` with that ID
- **THEN** the server returns full paper details in markdown, including abstract when available, ending with the Attribution Footer

**F-03.2: Lookup by DOI**
- **GIVEN** a paper identifier in the format "DOI:10.xxx/xxx"
- **WHEN** the LLM Client calls `get_paper` with that identifier
- **THEN** the server resolves it to the correct paper and returns its details

**F-03.3: Lookup by ArXiv ID**
- **GIVEN** a paper identifier in the format "ArXiv:2301.xxxxx"
- **WHEN** the LLM Client calls `get_paper` with that identifier
- **THEN** the server resolves it to the correct paper and returns its details

**F-03.4: Lookup of nonexistent paper**
- **GIVEN** a paper identifier that does not exist in the Semantic Scholar corpus
- **WHEN** the LLM Client calls `get_paper` with that identifier
- **THEN** the server returns an error message in the response content (isError: false) indicating the paper was not found, ending with the Attribution Footer. The LLM can reason about the message and try a different identifier.

---

### F-04: Backward Citation Snowball (References) | MUST

**F-04.1: Successful reference retrieval**
- **GIVEN** a paper with known references
- **WHEN** the LLM Client calls `get_references` with that paper's ID and limit 5
- **THEN** the server returns a markdown list of up to 5 papers that the target paper cites, each with citation counts and metadata, ending with the Attribution Footer

**F-04.2: References with default limit**
- **GIVEN** the LLM Client calls `get_references` with only a paper_id
- **WHEN** the server processes the request
- **THEN** limit defaults to 20

**F-04.3: References for paper with no references**
- **GIVEN** a paper that cites no other papers
- **WHEN** the LLM Client calls `get_references` for that paper
- **THEN** the server returns a markdown response showing 0 references — not an error

**F-04.4: Reference limit is clamped**
- **GIVEN** the LLM Client calls `get_references` with limit 5000
- **WHEN** the server processes the request
- **THEN** the limit is silently clamped to 1000

---

### F-05: Forward Citation Snowball (Citations) | MUST

**F-05.1: Successful citation retrieval**
- **GIVEN** a paper that has been cited by other papers
- **WHEN** the LLM Client calls `get_citations` with that paper's ID and limit 5
- **THEN** the server returns a markdown list of up to 5 papers that cite the target, each with citation counts and metadata, ending with the Attribution Footer

**F-05.2: Citations with default limit**
- **GIVEN** the LLM Client calls `get_citations` with only a paper_id
- **WHEN** the server processes the request
- **THEN** limit defaults to 20

**F-05.3: Citations for paper with no citations**
- **GIVEN** a newly published paper that has not yet been cited
- **WHEN** the LLM Client calls `get_citations` for that paper
- **THEN** the server returns a markdown response showing 0 citations — not an error

**F-05.4: Citation limit is clamped**
- **GIVEN** the LLM Client calls `get_citations` with limit 5000
- **WHEN** the server processes the request
- **THEN** the limit is silently clamped to 1000

---

### F-06: Proactive Rate Limiting | MUST

**F-06.1: Sequential requests are throttled**
- **GIVEN** the LLM Client sends two tool calls in rapid succession (< 1 second apart)
- **WHEN** the server processes both
- **THEN** the second outbound API request is delayed until at least 1.05 seconds have elapsed since the first, and both return successful results

**F-06.2: Throttle is shared across tool types**
- **GIVEN** the LLM Client calls `search_papers` followed immediately by `get_paper`
- **WHEN** the server processes both
- **THEN** the proactive throttle applies across both tools — the get_paper request waits for the minimum interval after the search_papers request completed

---

### F-07: Reactive Rate Limit Handling | MUST

**Requires:** F-06 (Proactive Rate Limiting)

**F-07.1: Single 429 is retried transparently**
- **GIVEN** the upstream API returns HTTP 429 on the first attempt
- **WHEN** the server retries after a backoff delay
- **THEN** the successful response is returned to the LLM Client with no indication that a retry occurred

**F-07.2: All retries exhausted**
- **GIVEN** the upstream API returns HTTP 429 on all 4 attempts (1 initial + 3 retries)
- **WHEN** the server has no more retries remaining
- **THEN** the server returns a human-readable error message to the LLM Client explaining that the rate limit was exceeded and suggesting the user try again, ending with the Attribution Footer

**F-07.3: Network failure is retried**
- **GIVEN** a transient network failure (connection reset, DNS timeout) on the first attempt
- **WHEN** the server retries
- **THEN** the behavior follows the same retry schedule as F-07.1

---

### F-08: Output Formatting Contract | MUST

**F-08.1: Null fields are omitted**
- **GIVEN** the upstream API returns a paper with null abstract, null DOI, and null fieldsOfStudy
- **WHEN** the server formats the response
- **THEN** the markdown output does not contain "null", "N/A", "Unknown", or empty lines for those fields — they are simply absent from the output

**F-08.2: Open access information is included**
- **GIVEN** a paper where isOpenAccess is true and openAccessPdf contains a URL, status "GREEN", and license "CC-BY"
- **WHEN** the server formats the response
- **THEN** the output includes an "Open Access" line showing the status, license, and a markdown link to the PDF

**F-08.3: External identifiers are displayed**
- **GIVEN** a paper with DOI, ArXiv ID, and PubMed ID
- **WHEN** the server formats the response
- **THEN** all three identifiers appear on an "IDs" line, separated by pipes

**F-08.4: Citation counts always present**
- **GIVEN** any paper returned by any tool
- **WHEN** the server formats the response
- **THEN** the output includes a "Citations" line showing total citation count and influential citation count, even when both are zero

**F-08.5: Attribution footer on every response including errors**
- **GIVEN** any tool response — success, error, or rate-limit exhaustion
- **WHEN** the response is returned to the LLM Client
- **THEN** the final line of the text content is "*Data provided by Semantic Scholar*" preceded by a horizontal rule

**F-08.6: Publisher disclaimers are suppressed**
- **GIVEN** the upstream API returns a paper with a `disclaimer` field in the openAccessPdf object
- **WHEN** the server formats the response
- **THEN** the disclaimer text is not included in the output — the open access status field already communicates availability

---

### F-09: Installation and Key Configuration | SHOULD

**F-09.1: Interactive install with key**
- **GIVEN** an Installer runs `./install.sh mcp-semantic-scholar --symlink`
- **WHEN** prompted for the API key and enters a valid key
- **THEN** the MCP server is registered in ~/.claude/settings.json with the key stored in the env block, and the server command points to the launcher script

**F-09.2: Interactive install without key**
- **GIVEN** an Installer runs `./install.sh mcp-semantic-scholar --symlink`
- **WHEN** prompted for the API key and presses Enter (skips)
- **THEN** the MCP server is registered in ~/.claude/settings.json with an empty S2_API_KEY, and the installer prints instructions for how to add the key later

**F-09.3: Key is never in the repository**
- **GIVEN** any state of the repository after installation
- **WHEN** an observer inspects all tracked files
- **THEN** no file contains an API key value — the key exists only in ~/.claude/settings.json which is outside the repository

---

### F-10: Launcher Script | SHOULD

**F-10.1: First run auto-build**
- **GIVEN** no compiled binary exists in target/release/ or target/debug/
- **WHEN** the launcher script is executed
- **THEN** it runs `cargo build --release`, then executes the resulting binary, with build output going to stderr

**F-10.2: Dev build override**
- **GIVEN** a debug binary exists at target/debug/mcp-semantic-scholar
- **WHEN** the launcher script is executed without S2_USE_RELEASE set
- **THEN** it uses the debug binary directly, skipping the release build

**F-10.3: No cargo available**
- **GIVEN** no binary exists and cargo is not on PATH
- **WHEN** the launcher script is executed
- **THEN** it prints an error to stderr and exits with a non-zero code

---

### F-11: MCP Protocol Compliance | MUST

**F-11.1: Initialize handshake**
- **GIVEN** a fresh server process with a valid key
- **WHEN** the LLM Client sends an `initialize` JSON-RPC request
- **THEN** the server responds with protocol version, server info (name: "mcp-semantic-scholar"), and capabilities listing tools as enabled

**F-11.2: Tool discovery**
- **GIVEN** an initialized MCP session
- **WHEN** the LLM Client sends a `tools/list` request
- **THEN** the server returns exactly 4 tools: search_papers, get_paper, get_references, get_citations, each with a description and input schema

**F-11.3: All logging to stderr**
- **GIVEN** a running server with RUST_LOG=info
- **WHEN** the server processes requests and logs diagnostic information
- **THEN** all log lines appear on stderr, and stdout contains only valid JSON-RPC messages

---

### F-12: Invalid or Revoked API Key Detection | MUST

**F-12.1: Revoked key returns actionable error**
- **GIVEN** a server running with an API key that has been revoked or is invalid
- **WHEN** the LLM Client calls any tool and the upstream API returns HTTP 401 or 403
- **THEN** the server returns a specific error message stating the API key appears invalid or revoked, includes the URL to obtain a new key, and does NOT retry (unlike 429 handling), ending with the Attribution Footer

**F-12.2: Revoked key is not retried**
- **GIVEN** the upstream API returns HTTP 401 or 403
- **WHEN** the server evaluates whether to retry
- **THEN** no retry is attempted — the error is returned immediately because retrying with the same invalid key is futile

---

### F-13: Plugin Integration Contract | SHOULD

**F-13.1: Optional dependency declaration**
- **GIVEN** the `scientific-method` plugin is installed
- **WHEN** a user inspects `plugins/scientific-method/.claude-plugin/plugin.json`
- **THEN** an `optionalDependencies` array lists `mcp-semantic-scholar` with a human-readable description of the capabilities it enables (structured academic search, citation graphs, reference snowballing)

**F-13.2: Install hint when optional dependency is absent**
- **GIVEN** a user runs `./install.sh scientific-method [--symlink]`
- **WHEN** `mcp-semantic-scholar` is not found in `~/.claude/settings.json` as a registered MCP server
- **THEN** the installer prints a hint naming the optional dependency, describing what it adds, and showing the exact install command (`./install.sh mcp-semantic-scholar --symlink`). The hint must not block or fail the install — `scientific-method` installs successfully regardless

**F-13.3: Tool naming convention**
- **GIVEN** the `mcp-semantic-scholar` server is registered in `~/.claude/settings.json`
- **WHEN** a consuming skill's `allowed-tools` list includes these tools
- **THEN** each tool is named using the convention `mcp__mcp-semantic-scholar__<tool-name>`, for all four tools: `search_papers`, `get_paper`, `get_references`, `get_citations`

**F-13.4: Transparent fallback in consuming skills**
- **GIVEN** a skill includes `mcp__mcp-semantic-scholar__search_papers` in its `allowed-tools`
- **WHEN** the skill attempts a call and the tool is not available (server not installed, key missing, or server failed to start)
- **THEN** the skill falls back to WebSearch without surfacing an error to the user. The absence of MCP tools must never degrade the core research loop — it only means the enhanced academic search path is unavailable for that session

---

## Negative Scope (WON'T — this version)

- **W-01**: PDF downloading or full-text content retrieval
- **W-02**: Author search, author profiles, or author-level analytics
- **W-03**: Paper recommendations (the /recommendations endpoint)
- **W-04**: Caching of results between requests or across sessions
- **W-05**: Batch or bulk paper lookups in a single tool call
- **W-06**: Write operations (bookmarks, collections, annotations)
- **W-07**: Unauthenticated operation without an API key

---

## Open Questions

- OQ-01: ~~Should the attribution footer also appear on error responses?~~ **RESOLVED: Yes, always.** See F-08.5.
- OQ-02: Should the server log the paper_id being looked up in diagnostic output, or is that considered user data that should not appear in logs? [ASSUMPTION: paper IDs are not sensitive and may be logged at info level]
- OQ-03: ~~Should the disclaimer field in openAccessPdf be surfaced?~~ **RESOLVED: No, suppress it.** See F-08.6.
- OQ-04: DOI strings like `DOI:10.1145/1234.5678` contain colons and slashes. The current URL encoding percent-encodes these when building the API path. Needs verification that S2 API correctly resolves percent-encoded DOI path segments. If not, DOI/ArXiv-prefixed IDs may need special handling (e.g. passed as-is without encoding the prefix). **Flag for integration testing.**

## Assumptions

- A-01: rustls is sufficient for all HTTPS connections to api.semanticscholar.org — no need for system OpenSSL (referenced in SC-08)
- A-02: The S2 API returns HTTP 404 for unknown paper identifiers, and this is wrapped as a tool-level string error (not an MCP protocol error) (referenced in F-03.4). **CONFIRMED by operator.**
- A-03: ~~The attribution footer is included on all tool responses including errors~~ **RESOLVED — no longer an assumption.** Confirmed by operator as spec'd behavior. See F-08.5.
- A-04: Paper identifiers are not sensitive data and may appear in stderr logs (referenced in OQ-02)
- A-05: Paper identifier format is NOT validated by the server. Any string is passed through to the S2 API, which returns 404 or an error for invalid IDs. This keeps the server thin and avoids maintaining format rules that could drift from S2's accepted formats. **CONFIRMED by operator.**
- A-06: No startup health-check probe. Invalid keys are detected on the first tool call via F-12 (401/403 handling). **CONFIRMED by operator.**
