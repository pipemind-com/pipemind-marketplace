---
name: creating-devops-agent
description: Creates project-specific DevOps agent for infrastructure and CI/CD
user-invocable: true
argument-hint: "optional: cloud provider (AWS/GCP/Azure) or specific toolchain"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - WebFetch
  - WebSearch
model: sonnet
color: orange
---

# Creating DevOps Agent

Creates a project-specific `devops.md` agent file customized for your infrastructure toolchain, CI/CD platform, and deployment workflows.

**IMPORTANT**: This skill creates a **PROJECT-level** agent at `<project>/.claude/agents/devops.md` (relative to current working directory), NOT in user-level settings (`~/.claude/`). This agent is specific to the current project's infrastructure.

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
   - Verify YAML frontmatter is valid
   - Check all required sections are present
   - Ensure no placeholder text like `[PROJECT_NAME]` remains
   - Validate section content is populated
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

## Agent Template Sections

The generated `devops.md` agent will include:

### 1. Role & Constraints
- Site Reliability Engineer (SRE) role definition
- **Critical constraint**: Never modify application source code
- Only change configuration files (Dockerfiles, YAML, .tf files)
- Always validate before suggesting changes

### 2. Detected Toolchain
For each detected tool, include:
- **Commands**: Core commands with examples
- **Best Practices**: Industry-standard patterns
- **Security**: Scanning, credential management, hardening
- **Optimization**: Performance and cost reduction

### 3. Workflow
DevOps agent's process:
1. Read relevant configuration files
2. Analyze for issues (security, performance, best practices)
3. Propose changes with rationale
4. Validate syntax/configuration
5. Test changes
6. Document improvements

### 4. Common Tasks
Organized by detected tools:
- **Docker**: Optimize Dockerfile, fix build issues, add security scanning
- **Terraform**: Refactor into modules, security hardening, cost optimization
- **CI/CD**: Debug workflows, optimize build times, add missing steps
- **Kubernetes**: Resource optimization, security policies, health checks

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
   • Role: SRE specializing in Docker + GitHub Actions
   • Sections: 4/4 populated
   • Lines: 243

✅ Template Validation
   ✅ YAML frontmatter valid
   ✅ All sections present
   ✅ No placeholders remaining
   ✅ Docker commands included
   ✅ GitHub Actions patterns included

📊 Results
   ✅ Created: .claude/agents/devops.md
   🛠️  Tools: Docker, GitHub Actions
   📝 Sections: Role & Constraints, Docker Toolchain,
              GitHub Actions Toolchain, Workflow, Common Tasks
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
   • Found: terraform/variables.tf
   • AWS provider detected in configs
   • Detected: Terraform, AWS

🌐 Smart Context Loading
   • User specified: AWS (prioritizing AWS patterns)
   • Fetching: Terraform AWS best practices
   • Fetching: AWS security patterns (IAM, encryption)
   • Fetching: AWS cost optimization strategies

📝 Generating DevOps Agent (AWS-focused)
   • Creating: .claude/agents/devops.md
   • Role: SRE specializing in Terraform + AWS
   • AWS sections: Security, Cost Optimization, HA patterns
   • Lines: 287

✅ Template Validation Passed
📊 Created: .claude/agents/devops.md
   🛠️  Tools: Terraform, AWS
   ☁️  Cloud: Amazon Web Services
   📝 Includes: IAM patterns, encryption at rest, multi-AZ HA
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
   ℹ️  Will create generic DevOps agent

🌐 Smart Context Loading
   • Fetching: General DevOps best practices
   • Fetching: Infrastructure-as-Code overview
   • Fetching: CI/CD platform comparison

📝 Generating DevOps Agent (Generic)
   • Creating: .claude/agents/devops.md
   • Role: General SRE for infrastructure setup
   • Focus: Exploration and tooling recommendations
   • Lines: 198

✅ Template Validation Passed
📊 Created: .claude/agents/devops.md (generic)
   ℹ️  No infrastructure detected
   💡 Agent will help identify and set up appropriate tooling
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
