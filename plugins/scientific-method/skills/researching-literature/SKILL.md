---
name: researching-literature
description: "Search for relevant academic and technical sources on a topic, build a structured bibliography in references.md, and download available articles. Use this skill whenever the user wants to find papers, survey existing research, build a reading list, gather citations, do a literature review, or explore what's been published on a topic -- even if they don't say 'literature review' explicitly."
user-invocable: true
argument-hint: "topic query and problem directory (e.g., 'quantum error correction ./my-research')"
allowed-tools:
  - WebSearch
  - WebFetch
  - Read
  - Write
  - Glob
  - Bash
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

### Step 2: Search from multiple angles

A single query gives you one slice of the literature. Run **3-5 WebSearch queries** that approach the topic from different directions to surface diverse perspectives:

- The topic as stated by the user
- Topic + "peer reviewed" or "systematic review" -- surfaces high-confidence work
- Topic + "empirical study" or "experimental results" -- surfaces data-driven work
- Topic + "limitations" or "challenges" -- surfaces contrarian and critical literature (this is important because confirmation bias is the default failure mode of literature searches)
- Topic + an adjacent domain if the topic is interdisciplinary

Collect all result URLs. Deduplicate against URLs already in `references.md`.

### Step 3: Fetch and evaluate each source

For each new URL (up to 10 per run):

1. **WebFetch** the URL to retrieve content
2. **Assess relevance** -- is this directly useful to the topic? Skip tangential results. A smaller, high-quality reference list is far more valuable than a padded one, because downstream work treats every entry as worth reading
3. **Extract metadata**: title, authors, year, source type (peer-reviewed / preprint / web resource / book)
4. **Write a 2-3 sentence relevance summary**: what it covers and why it matters to this specific topic
5. **Attempt PDF download** if the URL points to a PDF or a download link is visible on the page:
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
