---
name: creating-security-agent
description: Generates security auditor agent customized for project's tech stack
user-invocable: true
argument-hint: "optional: compliance standard (e.g. OWASP, SOC2)"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - WebFetch
  - WebSearch
model: sonnet
color: red
---

# Creating Security Agent

Creates a project-specific `security.md` agent file customized for your tech stack, acting as an adversarial "Red Teamer" specialized for your codebase.

**IMPORTANT**: This skill creates a **PROJECT-level** agent at `<project>/.claude/agents/security.md` (relative to current working directory), NOT in user-level settings (`~/.claude/`). This agent is specific to the current project's security concerns.

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

**3. 🌐 Smart Context Loading** (#4):
   - Search web for latest OWASP guidelines and Top 10 updates
   - Fetch framework-specific security advisories
   - Load compliance standard documentation (if specified: SOC2, HIPAA, PCI-DSS)
   - Incorporate modern security testing methodologies
   - Retrieve CVE databases for known vulnerabilities in detected stack

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
   - Verify YAML frontmatter is valid
   - Check all 7 required sections are present
   - Ensure security tools match detected stack
   - Validate checklist completeness
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

## Agent Template Sections

The generated `security.md` agent will include these 7 core sections:

### 1. Mission & Tech Stack
Adversarial security mindset and project-specific stack information:
- Language and framework
- Authentication mechanism
- Database and ORM
- Security focus areas

### 2. Security Tools
Stack-specific automated scanning tools:
- **Python**: bandit, pip-audit, safety, trufflehog
- **Node.js**: npm audit, snyk, eslint-plugin-security
- **Rust**: cargo-audit, cargo-clippy
- **Go**: gosec, nancy
- Commands to run each tool

### 3. Vulnerability Checklist
Tailored checklist based on application type and framework:
- OWASP Top 10 (API or Web)
- Framework-specific vulnerabilities
- Authentication/Authorization checks
- Data protection requirements
- Input validation patterns

### 4. Attack Scenarios
Concrete security testing scenarios:
- BOLA (Broken Object Level Authorization) tests
- SQL injection attempts
- JWT token tampering
- XSS payload testing
- Rate limiting verification

### 5. Workflow
Security audit process:
1. Read CLAUDE.md (understand architecture)
2. Scan with automated tools
3. Manual code review (auth, authorization, input validation)
4. Test attack scenarios
5. Document findings with severity levels

### 6. Output Format
Security report template:
- Summary with severity counts
- Critical/High/Medium/Low issues
- Location, PoC, and recommendations for each
- Compliance checklist (if applicable)

### 7. Compliance Requirements
If compliance standard specified (SOC2, HIPAA, PCI-DSS):
- Standard-specific checklist items
- Audit logging requirements
- Data encryption requirements
- Access control verification

## Critical Philosophy

**Security agent thinks adversarially, not constructively.**

- Builder creates features → Security agent breaks them
- Planner designs systems → Security agent finds flaws
- Goal: Find vulnerabilities before attackers do
- Mindset: Hostile code reviewer, red teamer, penetration tester

## Output

Creates `.claude/agents/security.md` with:
- Complete YAML frontmatter (name, description, tools, model, color)
- All 7 core sections fully populated
- Tech stack-specific security tools and commands
- Vulnerability checklist customized for framework
- Attack scenarios relevant to application type
- Security report template
- Compliance requirements (if specified)

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
   • Security tools: bandit, pip-audit, trufflehog, safety
   • Checklist: 23 items (OWASP + FastAPI-specific)
   • Attack scenarios: 8 scenarios
   • Sections: 7/7 populated
   • Lines: 312

✅ Template Validation
   ✅ YAML frontmatter valid
   ✅ All 7 sections present
   ✅ Security tools match Python stack
   ✅ Checklist complete

📊 Results
   ✅ Created: .claude/agents/security.md
   🔴 Security Focus: OWASP API Top 10
   🛠️ Tools: bandit, pip-audit, trufflehog, safety
   ✅ Attack scenarios: BOLA, SQLi, JWT tampering, XSS
```

### With Compliance Standard

```bash
/creating-security-agent SOC2
```

**Expected Output:**
```
✅ Pre-Flight Validation Passed
📖 Reading Project Context
🌐 Smart Context Loading
   • Fetching: SOC2 Trust Service Criteria
   • Fetching: Access control best practices
   • Fetching: Audit logging patterns
🛡️ Vulnerability Matrix
   • Standard: SOC2 compliance
   • Added: Access control audit
   • Added: Audit logging verification
   • Added: Data encryption checks
📝 Generating Security Agent (with SOC2 requirements)
✅ Template Validation Passed
📊 Created: .claude/agents/security.md (347 lines)
   • Added SOC2 section (access control, audit logs, encryption)
   • Added compliance checklist (12 additional items)
   • Sections: 7/7 populated
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

## Tips

- **First Time Setup**: Run this after creating `CLAUDE.md`
- **Updates**: Re-run when tech stack changes or new security requirements emerge
- **Compliance**: Use argument to add specific compliance standards
- **Integration**: Invoke security agent before deploying to production
- **Regular Audits**: Run security agent periodically, not just once
- **False Positives**: Security agent may be overly cautious - review findings carefully
- **Web Access**: Skill fetches latest OWASP guidelines and CVE databases
- **Stack-Specific**: Generated agent includes tools for your exact tech stack
