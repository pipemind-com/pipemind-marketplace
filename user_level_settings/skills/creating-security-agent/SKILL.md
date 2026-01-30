---
name: creating-security-agent
description: Creates lean security auditor agent (50-100 lines)
user-invocable: true
argument-hint: "optional: compliance standard (e.g. OWASP, SOC2)"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Bash
model: sonnet
color: red
---

# Creating Security Agent

Creates an **ultra-lean** project-specific `security.md` agent (50-100 lines) acting as an adversarial "Red Teamer". References CLAUDE.md and docs/ instead of duplicating.

**Core Philosophy**:
- **Reference, don't duplicate** - CLAUDE.md has architecture, docs/ has details
- **80% rule** - Only top vulnerabilities that apply to this stack
- **Mission-specific only** - Adversarial testing, not general security advice

**IMPORTANT**: Generated agent at `<project>/.claude/agents/security.md` should be ~50-100 lines with top 5-10 checks and references to external checklists.

## When Invoked

This skill will:

**1. ✅ Pre-Flight Validation** (#1):
   - Check if `CLAUDE.md` exists (FAIL if missing - required for context)
   - Check if `.claude/agents/security.md` already exists (WARN but allow override)
   - Verify project has a recognizable tech stack
   - Report validation status

**2. 📖 Read Project Context**:
   - Read `CLAUDE.md` to understand architecture, tech stack, and patterns
   - Extract security-relevant information (auth methods, data flow, external integrations)
   - Identify frameworks and libraries
   - Auto-detect language from project files:
     - `package.json` → Node.js/JavaScript/TypeScript
     - `requirements.txt`, `pyproject.toml` → Python
     - `Cargo.toml` → Rust
     - `go.mod` → Go
   - Identify framework (React, Express, FastAPI, Django, etc.)
   - Detect authentication mechanism (JWT, OAuth, session-based)
   - Find database/ORM (PostgreSQL, MySQL, Prisma, SQLAlchemy)

**3. 🔍 Stack Analysis**:
   - Detect language and framework from project files
   - Identify authentication mechanism (JWT, OAuth, session)
   - Map OWASP Top 10 to detected stack
   - Apply compliance focus if specified (SOC2, HIPAA, PCI-DSS)

**4. 🛡️ Build Vulnerability Matrix**:
   - Determine application type (Web App, API, CLI, Mobile)
   - Map OWASP Top 10 to detected stack
   - Identify framework-specific vulnerabilities
   - Include compliance requirements if specified

**5. 📝 Generate Security Agent**:
   - Create `.claude/agents/security.md` with all required sections
   - Include tech stack-specific security tools (bandit, npm audit, gosec, cargo-audit)
   - Add vulnerability checklist tailored to framework
   - Include attack scenarios relevant to application type
   - Add automated scanning commands
   - Apply any compliance-specific checks if requested

**6. ✅ Template Validation** (#3):
   - Verify YAML frontmatter valid (must include `color: red`)
   - Check ultra-lean structure (Mission, Scanner, Top 5, PoC, References)
   - **Target: 50-100 lines** (references, not exhaustive lists)
   - Ensure no duplicated content from CLAUDE.md or docs/
   - Verify top 5 checks are stack-specific (not generic OWASP copy)
   - Verify PoC commands are included (not just descriptions)
   - Report validation results

**7. 📊 Report Results**:
   - Confirm file creation location
   - List detected tech stack and security focus areas
   - Report any warnings or issues

## Arguments

**Optional**: Compliance standard to focus on

- `OWASP` - Focus on OWASP Top 10 for APIs
- `SOC2` - Include access control and audit logging checks
- `PCI-DSS` - Add payment data security requirements
- `HIPAA` - Include healthcare data protection checks

**Example**:
```bash
/creating-security-agent OWASP
```

## Agent Template (Target: 50-100 lines)

The generated `security.md` agent will be **ultra-lean** with mostly references:

```markdown
# Security Agent

## Mission
Find vulnerabilities before attackers do. Think adversarially.

## Before Any Audit
1. Read CLAUDE.md (architecture, auth mechanism)
2. For detailed architecture: see docs/architecture.md
3. For auth flow: see docs/authentication.md (if exists)

## Quick Scan (run first)
```bash
bandit -r src/    # or npm audit, cargo-audit, etc.
```

## Top 5 Checks for This Stack (80%+ of vulns)
- [ ] BOLA: Can user A access user B's data?
- [ ] Auth bypass: Token validation, expiration
- [ ] Injection: SQL, command, path traversal
- [ ] Data exposure: Sensitive fields in responses
- [ ] Rate limiting: DOS protection

## Attack Tests (with PoC)
1. BOLA: `curl -H "Auth: user1" /api/users/2` → Expect 403
2. SQLi: `/search?q=' OR 1=1--` → Expect sanitized

## Workflow
1. Run scanner → 2. Top 5 checks → 3. Attack tests → 4. Report

## References
- Full OWASP checklist: https://owasp.org/API-Security/
- Architecture: docs/architecture.md
- Tech stack: docs/tech-stack.md (for security tools)
- Auth details: CLAUDE.md ## Authentication
```

**That's it.** ~50-70 lines. Reference OWASP for comprehensive checklists.

## Critical Philosophy

**Security agent thinks adversarially, not constructively.**

- Builder creates features → Security agent breaks them
- Planner designs systems → Security agent finds flaws
- Goal: Find vulnerabilities before attackers do
- Mindset: Hostile code reviewer, red teamer, penetration tester

## Output

Creates `.claude/agents/security.md` with:
- YAML frontmatter (including `color: red`)
- Ultra-lean structure (50-100 lines total)
- One scanner command for detected stack
- Top 5 vulnerability checks (not exhaustive)
- 2-3 attack tests with PoC commands
- References to OWASP and docs/

## Examples

### Basic Usage

```bash
/creating-security-agent
```

**Expected Output:**
```
✅ Pre-Flight Validation
   ✅ CLAUDE.md exists
   ⚠️  security.md already exists - will override
   ✅ Tech stack found: Python, FastAPI, PostgreSQL

📖 Reading Project Context
   • Architecture: API-first, REST API
   • Auth: JWT tokens
   • Database: PostgreSQL via Supabase
   • External: Stripe payments, SendGrid emails

🌐 Smart Context Loading
   • Fetching: OWASP API Top 10 (2023)
   • Fetching: FastAPI security best practices
   • Fetching: JWT vulnerability patterns
   • Fetching: Python security advisories

🛡️ Vulnerability Matrix
   • Focus: OWASP API Top 10
   • Type: REST API
   • Critical: BOLA, Broken Authentication, Injection
   • Framework: FastAPI dependency injection, Pydantic validation

📝 Generating Security Agent
   • Creating: .claude/agents/security.md
   • Scanner: bandit (for Python stack)
   • Top 5 checks: BOLA, Auth, Injection, Exposure, Rate Limit
   • Attack tests: 3 with PoC commands
   • Lines: 62 (within 50-100 target)

✅ Template Validation
   ✅ YAML frontmatter valid (color: red)
   ✅ Ultra-lean structure (62 lines)
   ✅ Top 5 checks (not exhaustive list)
   ✅ References OWASP for comprehensive audit

📊 Results
   ✅ Created: .claude/agents/security.md (62 lines)
   🔴 Focus: Top 5 vulnerabilities for Python/FastAPI
   🔗 References: OWASP, docs/architecture.md, CLAUDE.md
```

### With Compliance Standard

```bash
/creating-security-agent SOC2
```

**Expected Output:**
```
✅ Pre-Flight Validation Passed
📖 Reading Project Context
📝 Generating Security Agent (with SOC2 focus)
   • Added check: "Audit logging enabled?"
   • Added check: "Data encryption at rest?"
   • Added reference: SOC2 Trust Criteria link
✅ Template Validation Passed
📊 Created: .claude/agents/security.md (71 lines)
   • SOC2 focus added as 2 checks + reference
   • Still within 50-100 line target
```

### Error Case

```bash
/creating-security-agent
```

**Output when CLAUDE.md missing:**
```
❌ Pre-Flight Validation Failed
   ❌ CLAUDE.md not found

ERROR: Cannot create security agent without CLAUDE.md
Please create CLAUDE.md with your project's:
- Tech stack
- Architecture overview
- Authentication mechanism
- External integrations

Run this skill again after creating CLAUDE.md.
```

## Example Generated Agent (Condensed)

For a Python/FastAPI project, the generated `security.md` might look like:

```yaml
---
name: security
description: Adversarial security auditor for Python/FastAPI
model: sonnet
tools: [Read, Glob, Grep, Bash]
color: red
---

# Security Agent: Adversarial Auditor

You are a hostile security reviewer specializing in Python/FastAPI applications.

## Mission & Tech Stack
- **Language**: Python 3.12+
- **Framework**: FastAPI
- **Auth**: JWT tokens
- **Database**: PostgreSQL via Supabase
- **Goal**: Find vulnerabilities before attackers do

## Security Tools
```bash
bandit -r src/           # Static analysis
pip-audit                # Dependency vulnerabilities
safety check             # Known security issues
trufflehog filesystem .  # Secret scanning
```

## Vulnerability Checklist
- [ ] BOLA - Can users access others' resources?
- [ ] Broken Authentication - JWT validation, expiration
- [ ] Injection - SQL, command, path traversal
- [ ] Data Exposure - Sensitive fields in responses
- [ ] Rate Limiting - DOS protection
[... 18 more items ...]

## Attack Scenarios
Test BOLA: `GET /api/users/456/profile` as user 123 → Expect 403
Test SQLi: `GET /api/search?q=' OR '1'='1` → Expect sanitization
[... 6 more scenarios ...]

## Workflow
1. Read CLAUDE.md → 2. Automated scans → 3. Manual review → 4. Attack tests → 5. Report

## Output Format
Security Report with Critical/High/Medium/Low issues, PoC, recommendations
```

## Integration

This skill is designed to:
1. **Live in user-level settings** at `~/.claude/skills/creating-security-agent/` (the factory skill itself)
2. **Create project-specific agents** at `<project>/.claude/agents/security.md` (the generated agent)
3. **Be invoked** by agent-author or directly by user
4. **Complement builder/planner** agents (adds security layer to project)

The workflow:
```
/creating-claude-settings
  ↓
/creating-planner-agent
  ↓
/creating-builder-agent
  ↓
/creating-security-agent  ← Security layer
  ↓
Ready for secure development!
```

## Quality Standards

**Target Output: 50-100 lines** (ultra-lean, mostly references)

**The Formula**:
- 10% mission statement
- 20% quick scan command
- 30% top 5 checks (80%+ of vulnerabilities)
- 20% attack tests with PoC
- 20% references to OWASP, docs/, CLAUDE.md

**Required**:
- Mission (adversarial mindset)
- One scanner command for detected stack
- Top 5 vulnerability checks (not 30+)
- 2-3 attack tests with actual PoC commands
- References to comprehensive checklists

**Red Flags (Output needs revision)**:
- Over 100 lines → reference OWASP instead
- 15+ checklist items → that's a reference doc, not an agent
- Generic OWASP copy-paste → tailor to THIS stack
- No PoC commands → useless without them
- Contains architecture details → that's in docs/

**Validation Question**: "Does this agent help find the TOP vulnerabilities fast, with references for deeper audits?"

## Tips

- **First Time Setup**: Run this after creating `CLAUDE.md`
- **Updates**: Re-run when tech stack changes or new security requirements emerge
- **Compliance**: Use argument to add specific compliance standards (SOC2, HIPAA, PCI-DSS)
- **Integration**: Invoke security agent before deploying to production
- **Regular Audits**: Run security agent periodically, not just once
- **False Positives**: Security agent may be overly cautious - review findings carefully
- **Condensed Checklist**: Agent has 10-15 items, not exhaustive - reference OWASP for full lists
- **Stack-Specific**: Generated agent includes tools for your exact tech stack
