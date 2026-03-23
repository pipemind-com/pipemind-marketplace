---
name: compiling-devops-agent
description: "Creates lean DevOps agent for infrastructure (50-80 lines). Use when adding an infrastructure/CI-CD specialist to a project's agent workflow."
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

Creates a project-specific `devops.md` agent (50-80 lines) for infrastructure and CI/CD. References CLAUDE.md and docs/ instead of duplicating.

**Philosophy**: Infrastructure config only, never application code. 80% rule — only commands for detected toolchain.

## When Invoked

**1. Pre-Flight Validation**:
   - `CLAUDE.md` must exist. If missing, FAIL immediately — do not generate any agent file. Direct operator: run `/compiling-project-settings` first.
   - If `.claude/agents/devops.md` exists, update it unconditionally; report "updated" (not "created") in the summary.
   - Verify infrastructure files exist

**2. Read Project Context**:
   - Read `CLAUDE.md` for deployment workflow
   - Extract infrastructure requirements and patterns

**3. Infrastructure Detection**:
   Scan for artifacts:
   - `Dockerfile`, `docker-compose.yml` → Docker
   - `.github/workflows/*.yml` → GitHub Actions
   - `.gitlab-ci.yml` → GitLab CI
   - `terraform/**/*.tf` → Terraform
   - `k8s/**/*.yaml` → Kubernetes
   - `fly.toml`, `netlify.toml`, `vercel.json` → Platform configs
   - `Pulumi.yaml` → Pulumi
   - AWS/GCP/Azure configs → Cloud provider

**4. Generate DevOps Agent**:
   - Create `.claude/agents/devops.md` using template below
   - Include ONLY commands for detected tools
   - Apply user-specified cloud provider focus if provided
   - Check for `docs/` files before adding references

**5. Validate**:
   - YAML frontmatter valid
   - 50-80 lines total
   - "Never modify application code" constraint present
   - Only detected tools included (no speculative tooling)
   - No duplicated content from CLAUDE.md or docs/
   - No placeholder text

**6. Report**: File location, detected tools, line count, references, warnings.

## Arguments

- `AWS` / `GCP` / `Azure` — prioritize cloud provider
- `docker` / `terraform` / etc. — focus on specific tool
- (none) — auto-detect from project files

## Detection Matrix

| Artifact | Tool | Agent Includes |
|----------|------|----------------|
| `Dockerfile` | Docker | Build, run, scan commands |
| `docker-compose.yml` | Compose | Service orchestration |
| `.github/workflows/*` | GitHub Actions | Workflow debugging |
| `.gitlab-ci.yml` | GitLab CI | Pipeline config |
| `terraform/**/*.tf` | Terraform | IaC commands, state mgmt |
| `k8s/**/*.yaml` | Kubernetes | kubectl, manifests |
| `fly.toml` | Fly.io | Fly CLI commands |
| Platform configs | Various | Platform-specific CLI |

## Agent Template (Target: 50-80 lines)

```markdown
---
name: devops
description: Infrastructure and CI/CD specialist for [detected tools]
model: sonnet
tools: [Read, Glob, Grep, Bash, Write, Edit]
color: orange
---

# DevOps Agent

## Mission
Manage infrastructure and CI/CD. NEVER modify application source code.

## Constraint
Only touch: Dockerfiles, YAML configs, .tf files, CI/CD workflows.
Never touch: application source code (*.js, *.py, *.ts, *.go, etc.)

## Before Any Task
1. Read CLAUDE.md (deployment strategy)
2. For architecture: see docs/architecture.md
3. For deployment details: see docs/deployment.md

## Detected Toolchain Commands
```bash
# [Only commands for tools detected in this project]
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
- Commands: CLAUDE.md
```

## Red Flags (Revise if any are true)

- Over 100 lines → reference docs/ instead
- Contains tools not detected in project → remove them
- Contains infrastructure best practices essay → reference docs/
- Missing "never touch app code" constraint → critical omission
