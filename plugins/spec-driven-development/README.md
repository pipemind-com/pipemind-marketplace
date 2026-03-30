# spec-driven-development

A self-replicating agentic workflow factory. Install once globally, then compile custom planner and builder agents tailored to each project's tech stack.

## Install

```bash
claude plugin marketplace add pipemind-com/pipemind-marketplace
claude plugin install spec-driven-development@pipemind-marketplace
```

## Setup a Project

Navigate to any git repo and run:

```
/compiling-agentic-workflow
```

This generates `CLAUDE.md`, `docs/`, and `.claude/agents/planner.md` + `builder.md` in one pass. Idempotent — re-run when your stack changes.

Or step through manually:

```
/compiling-project-settings   → CLAUDE.md
/compiling-project-docs       → docs/
/compiling-planner-agent      → .claude/agents/planner.md
/compiling-builder-agent      → .claude/agents/builder.md
```

Optional specialists:

```
/compiling-security-agent     → .claude/agents/security.md
/compiling-devops-agent       → .claude/agents/devops.md
```

## Skills

| Skill | Purpose |
|---|---|
| `/compiling-agentic-workflow` | Full project setup in one command |
| `/compiling-project-settings` | Generate `CLAUDE.md` |
| `/compiling-project-docs` | Generate `docs/` |
| `/compiling-planner-agent` | Compile project planner |
| `/compiling-builder-agent` | Compile project builder |
| `/compiling-security-agent` | Compile security auditor |
| `/compiling-devops-agent` | Compile DevOps specialist |
| `/defining-specs` | Turn PRDs into behavioral specs |
| `/defining-test-scenarios` | Expand specs into test scenarios |
| `/orchestrating-workflow` | Decompose features, plan and build in parallel |
| `/reviewing-code-quality` | Score code across 6 quality axes |
| `/stress-testing` | Adversarial property-based tests |
| `/git-commit-changes` | Split changes into atomic commits |
| `/conducting-post-mortem` | Extract lessons, propose CLAUDE.md updates |

Meta-agent: `agent-author` — expert guide for creating custom agents and skills.

## Agents

```bash
claude --agent planner   # Design solutions, write task files
claude --agent builder   # Implement from task files
claude --agent security  # Red-team audit (optional)
claude --agent devops    # Infrastructure review (optional)
```
