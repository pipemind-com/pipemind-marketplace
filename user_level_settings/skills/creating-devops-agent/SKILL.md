---
name: creating-devops-agent
description: Creates lean DevOps agent for infrastructure (50-80 lines)
user-invocable: true
argument-hint: "optional: cloud provider (AWS/GCP/Azure) or specific toolchain"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Bash
model: sonnet
color: orange
---

# Creating DevOps Agent

Creates an **ultra-lean** project-specific `devops.md` agent (50-80 lines) for infrastructure and CI/CD. References CLAUDE.md and docs/ instead of duplicating.

**Core Philosophy**:
- **Reference, don't duplicate** - CLAUDE.md has deployment context, docs/ has details
- **80% rule** - Only commands for detected toolchain
- **Mission-specific only** - Infrastructure config, never application code

**IMPORTANT**: Generated agent at `<project>/.claude/agents/devops.md` should be ~50-80 lines with toolchain commands and references.

## When Invoked

This skill will:

**1. ✅ Pre-Flight Validation** (#1):
   - Check if `CLAUDE.md` exists (WARN if missing - helpful but not required)
   - Check if `.claude/agents/devops.md` already exists (WARN but allow override)
   - Verify project has infrastructure files to analyze
   - Report validation status

**2. 📖 Read Project Context**:
   - Read `CLAUDE.md` (if exists) for deployment workflow
   - Extract infrastructure requirements
   - Identify existing DevOps patterns

**3. 🔍 Infrastructure Detection**:
   - Search for infrastructure artifacts:
     - `Dockerfile`, `docker-compose.yml` → Docker
     - `.github/workflows/*.yml` → GitHub Actions
     - `.gitlab-ci.yml` → GitLab CI
     - `terraform/**/*.tf` → Terraform
     - `k8s/**/*.yaml` → Kubernetes
     - `fly.toml`, `netlify.toml`, `vercel.json` → Platform configs
     - `Pulumi.yaml` → Pulumi
   - Detect cloud provider from configs (AWS, GCP, Azure)
   - Identify CI/CD platform

**4. 🌐 Smart Context Loading** (#4):
   - Auto-detect infrastructure stack from project files
   - Search web for detected toolchain best practices:
     - Docker security and optimization
     - Terraform/IaC patterns
     - CI/CD workflow optimization
     - Cloud provider-specific guidance
   - Fetch official documentation patterns
   - Incorporate modern DevOps practices

**5. 📝 Generate DevOps Agent**:
   - Create `.claude/agents/devops.md` with all required sections
   - Customize content based on detected infrastructure
   - Include toolchain-specific commands and best practices
   - Apply any user-provided customization notes

**6. ✅ Template Validation** (#3):
   - Verify YAML frontmatter is valid and complete
   - Check ultra-lean structure (Mission, Constraint, Commands, Workflow, References)
   - Ensure no placeholder text like `[PROJECT_NAME]` remains
   - **Target: 50-80 lines** (references, not exhaustive content)
   - Verify toolchain commands are specific to detected stack only
   - Check "never modify app code" constraint is included
   - Ensure no duplicated content from CLAUDE.md or docs/
   - Report validation results

**7. 📊 Report Results**:
   - Confirm file creation location
   - List detected infrastructure tools
   - Report any warnings or issues

## Arguments

**Optional**: Cloud provider or specific toolchain focus
- Example: `"AWS"` - Prioritize AWS best practices
- Example: `"docker"` - Focus on containerization
- Example: `"terraform"` - Emphasize IaC patterns
- Default: Auto-detect from project files

## Detection Matrix

| Artifact | Tool Detected | Agent Includes |
|----------|---------------|----------------|
| `Dockerfile` | Docker | Build, run, scan commands; multi-stage patterns |
| `docker-compose.yml` | Docker Compose | Compose workflow, service orchestration |
| `.github/workflows/*.yml` | GitHub Actions | Workflow debugging, optimization patterns |
| `.gitlab-ci.yml` | GitLab CI | Pipeline configuration, job patterns |
| `terraform/**/*.tf` | Terraform | IaC commands, state management, validation |
| `k8s/**/*.yaml` | Kubernetes | kubectl commands, manifest patterns, RBAC |
| `fly.toml` | Fly.io | Fly CLI, deployment commands |
| `netlify.toml` | Netlify | Netlify CLI, configuration patterns |
| `vercel.json` | Vercel | Vercel CLI, deployment patterns |
| `Pulumi.yaml` | Pulumi | Pulumi IaC patterns, stack management |
| AWS configs | Amazon Web Services | IAM, security groups, encryption patterns |
| GCP configs | Google Cloud | Cloud IAM, service accounts, security |
| Azure configs | Microsoft Azure | Resource management, security best practices |

## Agent Template (Target: 50-80 lines)

The generated `devops.md` agent will be **ultra-lean**:

```markdown
# DevOps Agent

## Mission
Manage infrastructure and CI/CD. NEVER modify application source code.

## Constraint
Only touch: Dockerfiles, YAML configs, .tf files, CI/CD workflows.
Never touch: *.js, *.py, *.ts, *.go (application code)

## Before Any Task
1. Read CLAUDE.md (deployment strategy)
2. For architecture: see docs/architecture.md
3. For deployment details: see docs/deployment.md

## Detected Toolchain Commands
```bash
# Docker (if detected)
docker build -t app .
docker-compose up -d

# Terraform (if detected)
terraform plan
terraform apply
```

## Workflow
1. Read config files
2. Identify issue
3. Propose change with rationale
4. Validate syntax
5. Test

## References
- Deployment: docs/deployment.md
- Architecture: docs/architecture.md
- Commands: CLAUDE.md ## Commands
```

**That's it.** ~50-60 lines. Toolchain commands only.

## Critical Philosophy

**DevOps agent focuses ONLY on infrastructure, never application logic.**

- Application code (*.js, *.py, *.go) is off-limits
- Configuration files (Dockerfile, YAML, .tf) are the domain
- Always validate before making changes
- Security and reliability are primary concerns

## Output

Creates `.claude/agents/devops.md` with:
- Complete YAML frontmatter (name, description, tools, model)
- Role definition and strict constraints
- Toolchain-specific commands and patterns
- Best practices for detected infrastructure
- Security and optimization guidelines
- Workflow integration

## Examples

### Basic Usage
```
/creating-devops-agent
```

**Expected Output:**
```
✅ Pre-Flight Validation
   ⚠️  CLAUDE.md not found (will create generic agent)
   ℹ️  devops.md doesn't exist - creating new

🔍 Infrastructure Detection
   • Found: Dockerfile
   • Found: docker-compose.yml
   • Found: .github/workflows/ci.yml
   • Detected: Docker, GitHub Actions
   • Cloud provider: None detected

🌐 Smart Context Loading
   • Detected stack: Docker, GitHub Actions
   • Fetching: Docker security best practices
   • Fetching: GitHub Actions workflow optimization
   • Fetching: Container image optimization patterns

📝 Generating DevOps Agent
   • Creating: .claude/agents/devops.md
   • Detected: Docker, GitHub Actions
   • Lines: 54 (within 50-80 target)

✅ Template Validation
   ✅ YAML frontmatter valid
   ✅ Ultra-lean structure (54 lines)
   ✅ "Never touch app code" constraint included
   ✅ Only detected tools (Docker, GH Actions)

📊 Results
   ✅ Created: .claude/agents/devops.md (54 lines)
   🛠️ Tools: Docker, GitHub Actions (commands only)
   🔗 References: docs/deployment.md, CLAUDE.md
```

### With Cloud Provider
```
/creating-devops-agent "AWS"
```

**Expected Output:**
```
✅ Pre-Flight Validation
   ✅ CLAUDE.md exists
   ⚠️  devops.md already exists - will override

🔍 Infrastructure Detection
   • Found: terraform/main.tf
   • AWS provider detected
   • Detected: Terraform, AWS

📝 Generating DevOps Agent
   • Creating: .claude/agents/devops.md
   • Detected tools: Terraform commands
   • AWS reference added to References section
   • Lines: 61

✅ Template Validation Passed
📊 Created: .claude/agents/devops.md (61 lines)
   🛠️ Tools: Terraform (commands only)
   🔗 References: docs/deployment.md, AWS docs
```

### No Infrastructure Detected
```
/creating-devops-agent
```

**Expected Output:**
```
✅ Pre-Flight Validation
   ⚠️  CLAUDE.md not found
   ℹ️  devops.md doesn't exist

🔍 Infrastructure Detection
   ⚠️  No infrastructure files detected
   ℹ️  Will create minimal starter agent

📝 Generating DevOps Agent (Starter)
   • Creating: .claude/agents/devops.md
   • Role: Infrastructure setup guidance
   • Focus: Help identify appropriate tooling
   • Lines: 45 (minimal starter)

✅ Template Validation Passed
📊 Created: .claude/agents/devops.md (starter)
   ℹ️  No infrastructure detected
   💡 Agent references docs/deployment.md for patterns
   💡 Consider adding: Dockerfile, CI/CD configs, or IaC files
```

### Error Case
```
/creating-devops-agent
```

**Output when write permission denied:**
```
✅ Pre-Flight Validation Passed
🔍 Infrastructure Detection Passed
🌐 Smart Context Loading Passed
📝 Generating DevOps Agent
   ❌ Failed to write .claude/agents/devops.md

ERROR: Permission denied
Ensure .claude/agents/ directory exists and is writable.
Run: mkdir -p .claude/agents
```

## Edge Cases

### Multiple Cloud Providers Detected
If AWS + GCP configs both found:
- Include sections for both cloud providers
- Organize by provider subsections
- Note multi-cloud considerations
- Flag potential complexity issues

### Conflicting IaC Tools
If both Terraform and Pulumi detected:
- Include both in agent knowledge
- Note which appears primary (based on file count)
- Suggest consolidating to one tool

### User Override vs Detection
If user specifies tool not detected in project:
- Honor user specification
- Add note: "Configured for [TOOL] (user-specified)"
- Still include any auto-detected tools

## Quality Standards

**Target Output: 50-80 lines** (ultra-lean, mostly references)

**The Formula**:
- 10% mission + constraint (never touch app code)
- 30% detected toolchain commands
- 20% workflow (5 steps)
- 40% references to docs/deployment.md, CLAUDE.md

**Required**:
- Mission (infrastructure only)
- Critical constraint: "NEVER modify application source code"
- Commands for DETECTED tools only (not all possible tools)
- References to docs/deployment.md

**Red Flags (Output needs revision)**:
- Over 100 lines → too much, reference docs/ instead
- Contains tools not detected → remove them
- Contains infrastructure best practices essay → reference docs/
- Missing "never touch app code" constraint → critical omission

**Validation Question**: "Does this agent have ONLY the commands for detected tools + references?"

## Tips

- **First Time Setup**: Run after creating `CLAUDE.md` for best results
- **Updates**: Re-run when infrastructure tooling changes
- **Customization**: Use argument to prioritize specific tools or cloud providers
- **Validation**: Review generated agent to ensure accuracy
- **Integration**: DevOps agent references `CLAUDE.md` for deployment context
- **Pairing**: Complements planner/builder agents for complete workflow
- **Security Focus**: Agent emphasizes security scanning and best practices

## Integration

This skill is designed to:
1. **Live in user-level settings** at `~/.claude/skills/creating-devops-agent/` (the factory skill itself)
2. **Create project-specific agents** at `<project>/.claude/agents/devops.md` (the generated agent)
3. **Complement** existing planner/builder agents (specializes in infrastructure)
4. **Reference** `CLAUDE.md` for deployment strategy
5. **Separate** infrastructure changes from application logic

The workflow:
```
/creating-claude-settings
  ↓
/creating-planner-agent
/creating-builder-agent
/creating-devops-agent  ← Infrastructure specialist
  ↓
Complete agentic workflow with specialized roles!
```
