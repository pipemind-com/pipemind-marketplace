---
name: researching-literature
description: "Search for relevant academic and technical sources on a topic, build a structured bibliography in references.md, and download available articles. Use this skill whenever the user wants to find papers, survey existing research, build a reading list, gather citations, do a literature review, or explore what's been published on a topic -- even if they don't say 'literature review' explicitly."
user-invocable: false
argument-hint: "topic query and problem directory (e.g., 'quantum error correction ./my-research')"
allowed-tools:
  - WebSearch
  - WebFetch
  - Read
  - Write
  - Glob
  - Bash
  - mcp__mcp-semantic-scholar__search_papers
  - mcp__mcp-semantic-scholar__get_paper
  - mcp__mcp-semantic-scholar__get_references
  - mcp__mcp-semantic-scholar__get_citations
model: sonnet
color: blue
---

# Researching Literature

Searches for relevant sources on a given topic, builds a structured bibliography in `references.md`, and downloads available articles to `references/`. Works standalone or as a step in a larger research pipeline.

`references.md` is the single source of truth for all sources in a problem directory. Every source gets a stable REF-NNN ID that other skills and documents can cite.

---

## Arguments

Parse from the skill argument:
- **Topic query** -- the search subject (required)
- **Problem directory** -- where to write outputs (default: current working directory)

---

## Workflow

### Step 1: Prepare the workspace

Create `references/` if it does not exist:
```
bash -c "mkdir -p <problem-dir>/references"
```

Read existing `<problem-dir>/references.md` if present. Note the highest REF-NNN number so new entries continue the sequence. Collect all URLs already listed so you skip duplicates in later steps. If no file exists, start from REF-001.

### Step 2: Search using dual-track strategy

**Tool selection**: If `mcp__mcp-semantic-scholar__search_papers` is available (test by calling it — if it errors or is missing, fall back), use the **MCP path** below. Otherwise use the **WebSearch path**. Both paths feed the same Step 3.

#### MCP path (preferred when available)

Run **3-4 `search_papers` calls** across two tracks:

**Recency track** (2 calls, limit 10 each):
- The topic as stated
- Topic narrowed by methodology or subfield

After fetching sources (Step 3), keep only those published in the last 3 years. Older sources found here are discarded unless they surface in the landmark track.

**Landmark track** (1-2 calls, limit 10 each):
- Topic + "survey" or "review"
- Topic + "limitations" or "challenges"

No date filter — any source that directly advances understanding qualifies.

**Citation snowball** (MCP-only bonus): For the 2-3 most relevant papers found so far, call `get_references` (backward snowball) and `get_citations` (forward snowball) with limit 5-10. This surfaces connected papers that keyword search misses. Deduplicate against papers already collected.

For any paper where `search_papers` returned incomplete metadata, call `get_paper` with its ID to fill in authors, year, and open-access PDF links.

#### WebSearch path (fallback)

Run **4-6 WebSearch queries** across two tracks. Both tracks use standard queries — no date operators. Recency is determined post-hoc in Step 3 by reading the publication year from each fetched source.

**Recency track** (target: cutting-edge work from the last 3 years)
Run 2-3 queries approaching the topic from different angles:
- The topic as stated
- Topic + "peer reviewed" or "systematic review"
- Topic + "empirical study" or "experimental results"

After fetching sources for this track (Step 3), keep only those published in the last 3 years. Sources older than 3 years found during this track are discarded unless they surface in the landmark track.

**Landmark track** (target: foundational papers with no recency filter)
Run 2-3 queries that surface older, definitional work:
- Topic + "foundational" or "seminal"
- Topic + "limitations" or "challenges" — surfaces critical and contrarian literature
- Topic + an adjacent domain if the topic is interdisciplinary

The landmark track applies no date filter. Any source that directly advances understanding of the topic qualifies, regardless of age.

#### After either path

Collect all result URLs across both tracks. Deduplicate against URLs already in `references.md`.

### Step 3: Fetch and evaluate each source

For each new source (up to 10 per run):

**Quality gate:** Before recording any source, assess its type. Peer-reviewed journal articles, conference papers, and established technical reports are included. Blog posts, opinion pieces, press releases, and low-signal web pages are silently dropped — they do not appear in `references.md` and no exclusion log is kept. Prefer depth over breadth: 5 authoritative sources outweigh 10 mediocre ones. Every included source must directly advance understanding of the topic.

**If source came from MCP** (`search_papers`, `get_references`, `get_citations`): metadata (title, authors, year, citation count, open-access URL) is already structured. Skip to relevance assessment (step 2 below). Use `get_paper` only if critical fields are missing.

**If source came from WebSearch**: follow the full fetch pipeline below.

1. **WebFetch** the URL to retrieve content
2. **Assess relevance** -- is this directly useful to the topic? Skip tangential results. A smaller, high-quality reference list is far more valuable than a padded one, because downstream work treats every entry as worth reading
3. **Extract metadata**: title, authors, year, source type (peer-reviewed / preprint / web resource / book)
4. **Write a 2-3 sentence relevance summary**: what it covers and why it matters to this specific topic
5. **Attempt PDF download** if the URL points to a PDF or a download link is visible on the page (MCP results often include an `openAccessPdf` URL — use it when present):
   - Construct a filename: `<first-author-lastname>-<year>-<slug>.pdf`
   - Fetch and write to `<problem-dir>/references/<filename>`
   - If the download fails or returns non-PDF content, record the URL for manual access instead. Many publishers block automated downloads -- this is expected, not an error

### Step 4: Update references.md

Append new entries to `<problem-dir>/references.md`. If the file does not exist, create it with a header first.

Each entry format:

```
## REF-NNN: <Title>

- **Authors:** <names, or "Unknown">
- **Year:** <year, or "n.d.">
- **Type:** <Peer-reviewed article | Preprint | Web resource | Book | Other>
- **URL:** <url>
- **Downloaded:** <filename in references/ | Not available>

**Relevance:** <2-3 sentences: what this covers and why it matters to the topic>

---
```

### Step 5: Report

Output a summary:
- N new sources added (list their REF IDs and titles)
- N sources already present (skipped)
- N articles downloaded to `references/`
