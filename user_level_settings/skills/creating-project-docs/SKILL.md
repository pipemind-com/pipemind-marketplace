---
name: creating-project-docs
description: Generates multi-file project documentation in /docs/ for humans and AI agents
user-invocable: true
argument-hint: "optional: 'include: topic1, topic2; skip: topic3' or 'full' for all topics"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - WebFetch
  - WebSearch
model: sonnet
color: cyan
---

# Creating Project Documentation

Generates comprehensive, multi-file project documentation in `/docs/**/*.md` with auto-detection of relevant topics, compact formatting, and AI context summaries optimized for dual human/AI consumption.

**IMPORTANT**: This skill creates documentation at `<project>/docs/*.md` (relative to current working directory). Each document includes an AI Context Summary header optimized for LLM context injection.

## When Invoked

This skill will:

**1. Pre-Flight Validation**:
   - Check if current directory is a git repository (FAIL if not)
   - Check if `CLAUDE.md` exists (WARN if missing, proceed with degraded context)
   - Create `docs/` directory if it doesn't exist
   - Parse user arguments for include/skip overrides
   - Report validation status

**2. Topic Discovery**:
   - Auto-detect documentation topics based on codebase signals
   - Apply confidence threshold (>30%) for topic inclusion
   - Handle user overrides (include/skip/full)
   - Report detected topics with confidence scores

**3. Codebase Analysis**:
   - For each detected topic, read relevant files (limited sample)
   - Extract patterns, conventions, key code paths
   - Store context for document generation

**4. Document Generation**:
   - Generate documents in dependency order
   - Apply compact formatting and document templates
   - Include code snippets with file paths
   - Add cross-references between documents

**5. Quality Validation**:
   - Verify all required sections present
   - Check line counts within bounds
   - Ensure no placeholder text
   - Validate cross-reference links

**6. Report Results**:
   - Output summary with document counts, line totals
   - List detected topics and confidence scores
   - Report cross-reference count

## Arguments

**Optional**: Control which topics to document

| Argument | Description |
|----------|-------------|
| `include: topic1, topic2` | Force include specific topics regardless of detection |
| `skip: topic1, topic2` | Skip specific topics even if detected |
| `full` | Generate all topics regardless of detection confidence |
| (none) | Auto-detect topics with >30% confidence |

**Examples**:
```bash
/creating-project-docs
/creating-project-docs "include: security, deployment"
/creating-project-docs "skip: frontend"
/creating-project-docs "full"
/creating-project-docs "include: api; skip: testing"
```

## Topic Detection Matrix

The following topics are auto-detected based on codebase signals:

| Topic | Detection Signals | Generated Document |
|-------|-------------------|-------------------|
| architecture | Always generated | `docs/architecture.md` |
| getting-started | Always generated | `docs/getting-started.md` |
| authentication | `JWT`, `OAuth`, `session`, auth middleware, `passport`, `auth0` | `docs/authentication.md` |
| testing | `*.test.*`, `tests/`, `__tests__/`, `*.spec.*`, jest/mocha/pytest configs | `docs/testing.md` |
| database | `migrations/`, ORM files, database configs, Prisma/SQLAlchemy/TypeORM | `docs/database.md` |
| api | `/api/`, controllers, routes, OpenAPI/Swagger, REST/GraphQL patterns | `docs/api.md` |
| frontend | React/Vue/Angular/Svelte/Next.js detected, `components/`, `pages/` | `docs/frontend.md` |
| backend | Express/FastAPI/Django/Rails/NestJS detected, server configs | `docs/backend.md` |
| deployment | Dockerfile, K8s manifests, Terraform, CI/CD configs, PM2, systemd | `docs/deployment.md` |
| security | CORS, CSP, rate limiting, security headers, helmet, sanitization | `docs/security.md` |

**Confidence threshold**: Topics with >30% confidence are included by default.

## Document Template Structure

Each generated document follows this structure:

```markdown
# [Topic Title]

> **AI Context Summary**: [2-3 sentence summary optimized for LLM context injection.
> Describes what this system does, key patterns, and critical constraints.]

## Overview
[High-level explanation - 3-5 paragraphs maximum]

## Key Concepts
| Concept | Description | Location |
|---------|-------------|----------|
| [Name]  | [Brief desc] | `path/to/file.ts:42` |

## [Topic-Specific Sections]
[Implementation details with code snippets including file paths]

## Cross-References
- Related: [docs/other.md](./other.md)
```

## Document Length Guidelines

| Document | Target Lines | Purpose |
|----------|-------------|---------|
| `architecture.md` | 150-250 | System structure, components, data flow |
| `getting-started.md` | 80-120 | Setup, prerequisites, first run |
| `authentication.md` | 120-200 | Auth flows, tokens, session management |
| `api.md` | 150-300 | Endpoints, request/response formats |
| `database.md` | 120-200 | Schema, migrations, queries |
| `testing.md` | 100-150 | Test strategy, running tests, coverage |
| `deployment.md` | 100-180 | Build, deploy, infrastructure |
| `frontend.md` | 120-200 | Components, state, routing |
| `backend.md` | 120-200 | Server architecture, middleware |
| `security.md` | 120-200 | Security measures, configurations |
| `index.md` | 50-80 | Navigation, document overview |

## Prompting Strategy for Accuracy + Compactness

Follow these guidelines when generating documentation:

1. **Specificity**: Reference exact file paths and line numbers where possible
2. **Show, don't tell**: Prefer code snippets over lengthy descriptions
3. **Compression**: Use tables for structured data, ASCII diagrams for relationships
4. **Limits**: Maximum 3 paragraphs per subsection, 15-20 line code snippets
5. **No filler**: Avoid phrases like "It is important to note that...", "As mentioned above..."
6. **Actionable**: Every section should help the reader do something

## Quality Validation Criteria

**Required for each document:**
- AI Context Summary at top (after H1 title)
- At least one code snippet with file path
- Cross-references to related docs (where applicable)
- No placeholder text (`[TODO]`, `[FILL IN]`, `[PLACEHOLDER]`)

**Validation failures (will be reported):**
- Under 50% of minimum line count for document type
- Missing AI Context Summary
- Code snippets without file paths
- Broken internal links to other docs
- Placeholder text detected

## Generation Order

Documents are generated in dependency order:

1. `architecture.md` - Foundational, referenced by all others
2. `getting-started.md` - Setup, references architecture
3. Topic-specific docs (in detection order) - Reference architecture
4. `index.md` - Generated last, links to all docs

## Output

Creates documentation files at `<project>/docs/`:
- `docs/index.md` - Navigation and overview
- `docs/architecture.md` - System architecture (always)
- `docs/getting-started.md` - Setup guide (always)
- `docs/*.md` - Topic-specific docs based on detection

## Examples

### Basic Usage (Auto-Detect)

```bash
/creating-project-docs
```

**Expected Output:**
```
 Pre-Flight Validation
    Git repository detected
    CLAUDE.md exists
    docs/ directory created

 Topic Discovery
    architecture (core - always included)
    getting-started (core - always included)
    authentication (87% - JWT patterns found in src/auth/)
    api (95% - REST controllers in src/routes/)
    database (92% - PostgreSQL + Prisma migrations)
    testing (78% - Jest config + 47 test files)
    deployment (65% - Dockerfile + GitHub Actions)
   Skip frontend (23% - below 30% threshold)
   Skip security (18% - minimal security patterns)

 Codebase Analysis
    Analyzing architecture patterns...
    Analyzing authentication flow...
    Analyzing API endpoints...
    Analyzing database schema...
    Analyzing test structure...
    Analyzing deployment config...

 Generating Documents
    docs/architecture.md (187 lines)
    docs/getting-started.md (94 lines)
    docs/authentication.md (156 lines)
    docs/api.md (248 lines)
    docs/database.md (148 lines)
    docs/testing.md (112 lines)
    docs/deployment.md (134 lines)
    docs/index.md (62 lines)

 Quality Validation
    All documents have AI Context Summary
    All code snippets include file paths
    Cross-references validated (18 internal links)
    No placeholder text detected

 Results
   Generated: 8 documents (1,141 total lines)
   Topics: 7 detected, 7 generated
   Location: docs/
```

### Force Include Topics

```bash
/creating-project-docs "include: security, frontend"
```

**Expected Output:**
```
 Pre-Flight Validation
    Git repository detected
    CLAUDE.md exists

 Topic Discovery
    architecture (core)
    getting-started (core)
    authentication (87%)
    api (95%)
    database (92%)
    testing (78%)
    deployment (65%)
    security (18% + forced include)
    frontend (23% + forced include)

 Generating Documents
    docs/architecture.md (187 lines)
    docs/getting-started.md (94 lines)
    docs/authentication.md (156 lines)
    docs/api.md (248 lines)
    docs/database.md (148 lines)
    docs/testing.md (112 lines)
    docs/deployment.md (134 lines)
    docs/security.md (89 lines)  Limited content - low detection confidence
    docs/frontend.md (76 lines)  Limited content - low detection confidence
    docs/index.md (72 lines)

 Results
   Generated: 10 documents (1,306 total lines)
```

### Skip Topics

```bash
/creating-project-docs "skip: testing, deployment"
```

**Expected Output:**
```
 Topic Discovery
    architecture (core)
    getting-started (core)
    authentication (87%)
    api (95%)
    database (92%)
   Skip testing (user requested)
   Skip deployment (user requested)

 Generating Documents
    docs/architecture.md (187 lines)
    docs/getting-started.md (94 lines)
    docs/authentication.md (156 lines)
    docs/api.md (248 lines)
    docs/database.md (148 lines)
    docs/index.md (52 lines)

 Results
   Generated: 6 documents (885 total lines)
```

### Full Documentation

```bash
/creating-project-docs "full"
```

**Expected Output:**
```
 Topic Discovery (full mode - all topics)
    architecture (core)
    getting-started (core)
    authentication (87%)
    api (95%)
    database (92%)
    testing (78%)
    deployment (65%)
    frontend (23% - included in full mode)
    backend (45% - included in full mode)
    security (18% - included in full mode)

 Generating Documents
    docs/architecture.md (187 lines)
    docs/getting-started.md (94 lines)
    docs/authentication.md (156 lines)
    docs/api.md (248 lines)
    docs/database.md (148 lines)
    docs/testing.md (112 lines)
    docs/deployment.md (134 lines)
    docs/frontend.md (76 lines)
    docs/backend.md (142 lines)
    docs/security.md (89 lines)
    docs/index.md (82 lines)

 Results
   Generated: 11 documents (1,468 total lines)
   Topics: 10 (full mode)
```

### Error Case - Not a Git Repository

```bash
/creating-project-docs
```

**Output when not in git repo:**
```
 Pre-Flight Validation
    Not a git repository

 FAILED: This skill requires a git repository
Please initialize git with: git init
```

### Warning Case - No CLAUDE.md

```bash
/creating-project-docs
```

**Output when CLAUDE.md missing:**
```
 Pre-Flight Validation
    Git repository detected
    CLAUDE.md not found - proceeding with degraded context
    docs/ directory exists

 Topic Discovery
   ...

Note: Documentation quality may be reduced without CLAUDE.md context.
Consider creating CLAUDE.md first for better results.
```

## Document Content Guidelines

### architecture.md

Must include:
- System overview diagram (ASCII or description)
- Component breakdown with responsibilities
- Data flow between components
- Technology stack summary
- Directory structure explanation

```markdown
# Architecture

> **AI Context Summary**: This system uses [pattern] architecture with [key components].
> Data flows from [entry] through [processing] to [storage]. Critical constraint: [constraint].

## System Overview

[ASCII diagram or description]

## Components

| Component | Responsibility | Location |
|-----------|---------------|----------|
| API Server | Handle HTTP requests | `src/server/` |
| Auth Module | JWT validation | `src/auth/` |
...
```

### getting-started.md

Must include:
- Prerequisites (versions, tools)
- Installation steps (copy-paste ready)
- Environment setup
- First run verification
- Common issues and solutions

```markdown
# Getting Started

> **AI Context Summary**: Setup requires [tools]. Install dependencies with [command],
> configure [env vars], then run [start command]. First-time setup takes ~[X] steps.

## Prerequisites

- Node.js 18+
- PostgreSQL 14+
...

## Installation

```bash
git clone [repo]
cd [project]
npm install
cp .env.example .env
```
...
```

### api.md

Must include:
- Base URL and versioning
- Authentication requirements
- Endpoint table with methods, paths, descriptions
- Request/response examples
- Error response format

### database.md

Must include:
- Database technology and version
- Schema overview (key tables/collections)
- Relationship diagram or description
- Migration workflow
- Query patterns and examples

### testing.md

Must include:
- Test framework and configuration
- Running tests commands
- Test file organization
- Coverage requirements
- Writing new tests guide

### deployment.md

Must include:
- Build process
- Environment configurations
- Deployment commands/workflow
- Infrastructure requirements
- Monitoring and logging setup

### authentication.md

Must include:
- Auth flow diagram
- Token/session management
- Protected routes pattern
- User roles/permissions
- Security considerations

### frontend.md

Must include:
- Framework and key libraries
- Component organization
- State management approach
- Routing structure
- Build and development workflow

### backend.md

Must include:
- Server framework
- Middleware stack
- Request lifecycle
- Error handling
- Configuration management

### security.md

Must include:
- Security measures implemented
- Input validation approach
- Authentication/authorization
- Data protection
- Security headers/CORS

### index.md

Must include:
- Project name and one-line description
- Quick links to all docs
- Document descriptions
- Suggested reading order

```markdown
# Project Documentation

> **AI Context Summary**: Documentation for [project]. Start with [getting-started.md]
> for setup, [architecture.md] for system overview. [X] documents covering [topics].

## Documents

| Document | Description |
|----------|-------------|
| [Architecture](./architecture.md) | System design and components |
| [Getting Started](./getting-started.md) | Setup and installation |
...

## Suggested Reading Order

1. Getting Started - Setup your environment
2. Architecture - Understand the system
3. [Topic-specific based on your role]
```

## Tips

- **Run after CLAUDE.md**: Best results when `CLAUDE.md` exists with project context
- **Use include/skip**: Customize output for your needs
- **Regenerate periodically**: Re-run when codebase changes significantly
- **Review and edit**: Generated docs are a starting point - refine as needed
- **Cross-references**: Documents link to each other - keep the set together
- **AI summaries**: The AI Context Summary headers are specifically for LLM consumption
- **Compact format**: Documents are intentionally concise - expand specific sections as needed

## Integration

This skill complements other project setup skills:

```
/creating-claude-settings
  |
/creating-planner-agent
  |
/creating-builder-agent
  |
/creating-security-agent
  |
/creating-project-docs  <-- Generates documentation
  |
Ready for development!
```

The generated documentation serves both:
1. **Human developers**: Onboarding, reference, troubleshooting
2. **AI agents**: Context injection via AI Context Summary headers

## Quality Standards

**Minimum Requirements:**
- All documents have AI Context Summary
- Code snippets include file paths (e.g., `src/auth/jwt.ts:42`)
- Cross-references use relative links (`./other.md`)
- No placeholder text
- Line counts within 50-150% of targets

**Warning Signs (may need manual review):**
- Documents under 50% of target line count
- Topics with <30% confidence forced via include
- Missing code examples
- Generic descriptions without project-specific details

**Gold Standard:**
- Accurate file paths and line numbers
- Code snippets from actual codebase
- Project-specific terminology and patterns
- Useful cross-references
- Actionable content in every section
