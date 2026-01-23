---
name: creating-claude-settings
description: Generates comprehensive CLAUDE.md with architecture, patterns, and workflows
user-invocable: true
argument-hint: "optional: focus areas or additional sections to include"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - WebFetch
  - WebSearch
  - Bash
model: sonnet
color: green
---

# Creating Claude Settings

Analyzes your codebase and generates a comprehensive `CLAUDE.md` file documenting architecture, development workflows, coding patterns, testing strategies, and deployment procedures.

## When Invoked

This skill will:

**1. ✅ Pre-Flight Validation** (#1):
   - Check if in a git repository (FAIL if not)
   - Check if `CLAUDE.md` already exists (WARN but allow override)
   - Verify codebase has sufficient files to analyze
   - Report validation status

**2. 🔍 Codebase Analysis**:
   - Detect tech stack from project files:
     - `package.json` → Node.js/JavaScript/TypeScript
     - `requirements.txt`, `pyproject.toml` → Python
     - `Cargo.toml` → Rust
     - `go.mod` → Go
     - `pom.xml`, `build.gradle` → Java
   - Identify framework (React, Next.js, FastAPI, Django, etc.)
   - Discover architecture patterns (monolith, microservices, layered, etc.)
   - Map directory structure
   - Find configuration files

**3. 🌐 Smart Context Loading** (#4):
   - Search web for framework-specific best practices
   - Fetch official documentation for detected frameworks
   - Load modern architectural patterns
   - Gather testing conventions

**4. 📖 Code Exploration**:
   - Read key configuration files
   - Sample implementation files from each layer
   - Identify existing patterns and conventions
   - Extract environment variables and integration points

**5. 📝 Generate CLAUDE.md**:
   Create comprehensive documentation with all 9 core sections:
   1. Development Commands
   2. Architecture Overview
   3. Data Flow
   4. Key Integration Points
   5. Important Patterns and Constraints
   6. Architecture Patterns (detailed)
   7. Deployment Strategy
   8. Testing Strategy
   9. Common Gotchas

**6. ✅ Content Validation** (#3):
   - Verify all 9 sections are present and populated
   - Check for placeholder text
   - Ensure code examples are included
   - Validate architecture diagram syntax
   - Report validation results

**7. 📊 Report Results**:
   - Confirm file creation location
   - List detected tech stack
   - Summarize included sections
   - Report any warnings or gaps

## Arguments

**Optional**: Focus areas or additional sections
- Example: `"Focus on microservices communication patterns"`
- Example: `"Include detailed Docker deployment workflow"`
- Example: `"Add Redis caching architecture"`
- Default: Generates all standard sections based on auto-detected stack

## CLAUDE.md Sections

### 1. Development Commands
Commands for each layer/stack:
- `npm run dev`, `python manage.py runserver`, etc.
- Build commands
- Test commands
- Deployment commands
- Database migration commands

### 2. Architecture Overview
- **Tech stack diagram** showing all layers and communication
- Key components in each layer
- Clear explanation of architecture pattern (e.g., layered, microservices)
- **NOT** MVVM unless actually used

### 3. Data Flow
- **Diagram** key workflows with actual file paths
- Show how data moves through layers
- Include concrete examples:
  - User input → API → database → response
  - Background job processing
  - Real-time updates

### 4. Key Integration Points
- External services (authentication providers, payment gateways, etc.)
- Database configuration
- API integrations
- Environment variables required
- Configuration files and their purpose

### 5. Important Patterns and Constraints
- Core patterns used (cache-aside, repository pattern, etc.)
- Algorithm constraints or business rules
- Database schema considerations
- Performance requirements
- Security constraints

### 6. Architecture Patterns (Detailed)
- **Explain primary pattern** with clear rules
- **Code examples** showing correct vs incorrect usage
- **Table of Anti-Patterns** to avoid:

  | ❌ Anti-Pattern | ✅ Correct Pattern |
  |----------------|-------------------|
  | Business logic in controllers | Move to service layer |
  | Direct database access from UI | Use repository pattern |

### 7. Deployment Strategy
- **Critical deployment order** with rationale
- Rollback considerations
- Environment-specific concerns (dev, staging, prod)
- Database migration timing
- Feature flag usage

### 8. Testing Strategy
- **Test pyramid** showing layers
- What to test at each layer (unit, integration, E2E)
- Testing frameworks for each stack
- Code coverage requirements
- Test organization patterns

### 9. Common Gotchas
- Framework-specific pitfalls with examples
- State management confusion
- Deployment/configuration issues
- Algorithm/business logic edge cases
- Performance bottlenecks

## Output

Creates `CLAUDE.md` with:
- All 9 core sections fully populated
- Tech-stack-specific patterns and examples
- Concrete code examples for critical patterns
- Architecture diagrams using ASCII/mermaid
- Actionable guidance (developers know WHAT and HOW)
- Cross-file concerns requiring system understanding

## Examples

### Basic Usage
```
/creating-claude-settings
```

**Expected Output:**
```
✅ Pre-Flight Validation
   ✅ Git repository detected
   ⚠️  CLAUDE.md already exists - will override
   ✅ Codebase has 127 files to analyze

🔍 Codebase Analysis
   • Detected: Python 3.12, FastAPI 0.109
   • Framework: FastAPI with Supabase backend
   • Architecture: API-first, layered architecture
   • Database: PostgreSQL via Supabase
   • Directory structure: src/, tests/, migrations/

🌐 Smart Context Loading
   • Fetching: FastAPI best practices
   • Fetching: Supabase Python patterns
   • Fetching: PostgreSQL schema design

📖 Code Exploration
   • Config: pyproject.toml, .env.example
   • API routes: src/api/v1/
   • Services: src/services/
   • Models: src/models/
   • Tests: tests/ (pytest)

📝 Generating CLAUDE.md
   • Section 1: Development Commands ✓
   • Section 2: Architecture Overview ✓
   • Section 3: Data Flow ✓
   • Section 4: Integration Points ✓
   • Section 5: Patterns & Constraints ✓
   • Section 6: Architecture Patterns ✓
   • Section 7: Deployment Strategy ✓
   • Section 8: Testing Strategy ✓
   • Section 9: Common Gotchas ✓

✅ Content Validation
   ✅ All 9 sections present
   ✅ Code examples included (12 snippets)
   ✅ Architecture diagrams present (3)
   ✅ No placeholders remaining
   ✅ Anti-patterns table populated

📊 Results
   ✅ Created: CLAUDE.md (487 lines)
   📦 Tech Stack: Python, FastAPI, PostgreSQL, Supabase
   📐 Architecture: API-first, layered (routes → services → models)
   📝 Sections: 9/9 complete with examples
```

### With Customization
```
/creating-claude-settings "Focus on Redis caching patterns and background job processing"
```

**Expected Output:**
```
✅ Pre-Flight Validation Passed
🔍 Codebase Analysis
   • Additional detection: Redis, Celery
🌐 Smart Context Loading
   • Added: Redis caching patterns
   • Added: Celery best practices
📝 Generating CLAUDE.md (with custom sections)
   • Added: Redis cache-aside pattern examples
   • Added: Background job workflow diagrams
✅ Content Validation Passed
📊 Created: CLAUDE.md (523 lines)
   • Added Redis architecture section
   • Added Celery job patterns
```

### Error Case
```
/creating-claude-settings
```

**Output when not in git repo:**
```
❌ Pre-Flight Validation Failed
   ❌ Not in a git repository

ERROR: Cannot create CLAUDE.md outside a git repository
Run 'git init' first, then try again.
```

## Critical Philosophy

**CLAUDE.md is the single source of truth for project architecture.**

All agents (planner, builder, etc.) reference CLAUDE.md to understand:
- How the system works
- What patterns to follow
- How to test correctly
- How to deploy safely

Keep it updated as the project evolves.

## Tips

- **First Time Setup**: Run this before creating planner/builder agents
- **Updates**: Re-run when architecture changes significantly
- **Customization**: Use arguments to emphasize specific patterns
- **Review Generated File**: Always validate accuracy for your specific project
- **Keep Current**: Update CLAUDE.md manually as patterns evolve
- **Code Examples**: Ensure examples match actual codebase conventions

## Integration

This skill is designed to be:
1. **First step** in `bootstrap-agentic.sh`
2. **Prerequisite** for `/creating-planner-agent` and `/creating-builder-agent`
3. **Referenced** by all project-specific agents

The workflow:
```
/creating-claude-settings
  ↓
/creating-planner-agent
  ↓
/creating-builder-agent
  ↓
Ready for agentic workflow!
```
