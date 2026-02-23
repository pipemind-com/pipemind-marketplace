---
name: initializing-project-docs
description: "Generates docs/ for progressive disclosure from CLAUDE.md. Use after /initializing-project-settings to create detailed reference documentation that agents load on demand."
user-invocable: true
argument-hint: "optional: 'include: topic1, topic2; skip: topic3' or 'full' for all topics"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Bash
model: sonnet
color: blue
---

# Creating Project Documentation

Generates `docs/` directory with detailed documentation serving as **progressive disclosure** from your lean CLAUDE.md. CLAUDE.md stays at 50-100 lines; `docs/` holds the detail agents load on demand.

**Run `/initializing-project-settings` first**, then this skill to generate the docs it references.

## When Invoked

**1. Pre-Flight Validation**:
   - Verify git repository (FAIL if not)
   - Check `CLAUDE.md` exists (WARN if missing — suggest `/initializing-project-settings`)
   - Create `docs/` directory if needed
   - Parse user arguments for include/skip overrides

**2. Topic Discovery**:
   - Auto-detect topics from codebase signals (see detection matrix)
   - Include topics with >30% confidence; apply user overrides

**3. Codebase Analysis**:
   - For each topic, read relevant files (limited sample)
   - Extract patterns, conventions, key code paths

**4. Document Generation**:
   - Generate in dependency order: `architecture.md` first, `index.md` last
   - Follow template structure below; consult `references/doc-templates.md` for per-topic content requirements
   - Include code snippets with file paths, cross-references between documents

**5. Quality Validation**:
   - AI Context Summary present in each document
   - Code snippets include file paths (e.g., `src/auth/jwt.ts:42`)
   - No placeholder text (`[TODO]`, `[FILL IN]`)
   - Line counts within 50-150% of targets
   - Cross-reference links valid

**6. Report**: Document count, line totals, topics detected, cross-reference count.

## Arguments

| Argument | Effect |
|----------|--------|
| `include: topic1, topic2` | Force-include topics regardless of detection |
| `skip: topic1, topic2` | Skip topics even if detected |
| `full` | Generate all topics |
| (none) | Auto-detect with >30% confidence threshold |

## Topic Detection Matrix

| Topic | Signals | Output |
|-------|---------|--------|
| architecture | Always | `docs/architecture.md` |
| getting-started | Always | `docs/getting-started.md` |
| authentication | JWT, OAuth, session, auth middleware | `docs/authentication.md` |
| testing | `*.test.*`, `tests/`, jest/pytest configs | `docs/testing.md` |
| database | `migrations/`, ORM, Prisma/SQLAlchemy | `docs/database.md` |
| api | `/api/`, controllers, routes, OpenAPI | `docs/api.md` |
| frontend | React/Vue/Angular, `components/`, `pages/` | `docs/frontend.md` |
| backend | Express/FastAPI/Django, server configs | `docs/backend.md` |
| deployment | Dockerfile, K8s, Terraform, CI/CD | `docs/deployment.md` |
| security | CORS, CSP, rate limiting, security headers | `docs/security.md` |
| tech-stack | `package.json`, `requirements.txt`, `Cargo.toml` | `docs/tech-stack.md` |
| workflow | Planner/builder agent pattern | `docs/workflow.md` |

## Document Template

Every generated document follows this structure:

```markdown
# [Topic Title]

> **AI Context Summary**: [2-3 sentences. What this does, key patterns, critical constraints.
> Agents read this first to decide if they need the full document.]

## Overview
[3-5 paragraphs max]

## Key Concepts
- **[Name]** — [Brief desc] (`path/to/file.ts:42`)

## [Topic-Specific Sections]

## Cross-References
- Related: [docs/other.md](./other.md)
```

**AI Context Summary**: Agents read this first — dense, actionable, 2-3 sentences. Include what the system does, key patterns, and critical constraints.

## Line Targets

| Document | Lines | Purpose |
|----------|-------|---------|
| `architecture.md` | 150-250 | System structure, data flow |
| `getting-started.md` | 80-120 | Setup, prerequisites |
| `tech-stack.md` | 100-150 | Language, framework, tools |
| `testing.md` | 100-150 | Test strategy, commands |
| `deployment.md` | 100-180 | Build, deploy, infra |
| `workflow.md` | 80-120 | Planner/builder patterns |
| `index.md` | 50-80 | Navigation, overview |
| Other topic docs | 120-200 | Topic-specific detail |

For detailed per-document content requirements, see `references/doc-templates.md`.

## Writing Guidelines

1. Reference exact file paths and line numbers
2. Code snippets over lengthy descriptions
3. Tables for structured data, ASCII for relationships
4. Max 3 paragraphs per subsection, 15-20 line code snippets
5. No filler phrases ("It is important to note that...")
6. Every section helps the reader do something

## Generation Order

1. `architecture.md` — foundational, referenced by all others
2. `getting-started.md` — references architecture
3. Topic-specific docs in detection order
4. `index.md` — last, links to all generated docs

## Error Handling

- **Not a git repo**: FAIL with message to run `git init`
- **No CLAUDE.md**: WARN, proceed with degraded context, recommend `/initializing-project-settings`
- **Placeholder text detected**: Report as validation failure
- **Under 50% of target line count**: Flag for manual review
