# Spec: spec-driven-development — Project Compilation Pipeline
**Source:** plugins/spec-driven-development/ (brownfield reverse-engineering)
**Epic:** E-B
**Glossary:** specs/glossary.md
**Generated:** 2026-03-22
**Status:** DRAFT — requires operator review

---

## System Constraints

- **SC-01**: All compilation skills are idempotent — re-running a skill on a project that already has the target artifact updates the artifact to reflect the current codebase state rather than failing or duplicating.
- **SC-02**: CLAUDE.md must not exceed approximately 100 lines; every instruction it contains must apply to 80%+ of sessions (the 80% rule).
- **SC-03**: The combined instruction count of CLAUDE.md and all active agent files must remain within the ~100 instructions available after Claude Code's system prompt (~50 instructions) consumes its share of the 150-instruction limit.
- **SC-04**: Agent files must reference CLAUDE.md and docs/ for shared context — they must never duplicate content that already exists in those files.
- **SC-05**: All compilation skills require the operator to be inside a git repository; skills that check for this will fail if the git requirement is not met.
- **SC-06**: Compiled agent files must contain valid YAML frontmatter at the top of the file with required fields: name, description, model, tools, color.
- **SC-07**: Agent files target 50-100 lines; skill files target 100-200 lines; docs/ files target 80-300 lines. Files outside these ranges must be flagged during validation.
- **SC-08**: Agent names use kebab-case nouns; skill names use gerunds (present participles). Names that do not follow these conventions are invalid.

---

## F-01: Full Workflow Compilation | MUST

**F-01.1: Full sequence executes in dependency order (happy path)**
- **GIVEN** an operator invokes /compiling-agentic-workflow in a git repository with no prior compilation artifacts
- **WHEN** the skill begins execution
- **THEN** it runs /compiling-project-settings, then /compiling-project-docs, then /compiling-planner-agent, then /compiling-builder-agent in that exact order; each step completes before the next begins

**F-01.2: Idempotent re-run updates existing artifacts**
- **GIVEN** a project already has CLAUDE.md, docs/, planner.md, and builder.md
- **WHEN** the operator re-runs /compiling-agentic-workflow
- **THEN** all four artifacts are updated to reflect the current codebase state; the skill does not fail or duplicate content

**F-01.3: Sub-skill failure halts the pipeline**
- **GIVEN** /compiling-project-settings succeeds but /compiling-project-docs encounters an error
- **WHEN** the pipeline reaches the failing sub-skill
- **THEN** execution halts at that point; the skill reports the failure and which subsequent steps were skipped; it does not attempt to compile agents without their docs/ prerequisites

**F-01.4: Not in a git repository (pre-flight failure)**
- **GIVEN** the operator invokes /compiling-agentic-workflow outside a git repository
- **WHEN** the skill performs its pre-flight check
- **THEN** the skill reports that a git repository is required and halts without creating any files

**F-01.5: User arguments forwarded to sub-skills context-aware**
- **GIVEN** the operator passes customization arguments to /compiling-agentic-workflow (e.g., --focus "testing")
- **WHEN** the skill delegates to sub-skills
- **THEN** it routes arguments selectively based on each sub-skill's known interface: --focus routes to /compiling-project-settings; topic include/skip args route to /compiling-project-docs; customization notes route to agent compilation skills; an argument is not forwarded to a sub-skill that does not accept it

**F-01.6: Completion report lists artifact status**
- **GIVEN** all four sub-skills complete successfully
- **WHEN** the skill produces its final output
- **THEN** it reports the status (created or updated) and approximate line count for each artifact: CLAUDE.md, docs/ (file count), planner.md, builder.md

---

## F-02: Project Settings Compilation | MUST

**F-02.1: CLAUDE.md generated from codebase analysis (happy path)**
- **GIVEN** an operator invokes /compiling-project-settings in a git repository with no existing CLAUDE.md
- **WHEN** the skill analyzes the codebase
- **THEN** it produces a CLAUDE.md containing these sections: Mission, Project Context (About This Project), Key Directories, Commands, Standards, Notes, and Additional Documentation; the file is 50-100 lines

**F-02.2: Tech stack detected from project files**
- **GIVEN** a project contains recognizable stack indicators (e.g., package.json, requirements.txt, Cargo.toml, go.mod, Gemfile)
- **WHEN** the skill analyzes the codebase
- **THEN** it identifies the primary language, framework, and package manager from those files and incorporates stack-specific commands and conventions into CLAUDE.md

**F-02.3: Workflow section included conditionally**
- **GIVEN** a project has .claude/agents/planner.md and .claude/agents/builder.md
- **WHEN** CLAUDE.md is generated
- **THEN** a Workflow section describing the planner/builder pattern is included; if these agent files do not exist, the Workflow section is omitted

**F-02.4: 80% rule enforced — niche content excluded**
- **GIVEN** the codebase contains patterns that apply only to rare edge cases (e.g., a migration script used once)
- **WHEN** the skill decides what to include in CLAUDE.md
- **THEN** instructions for that content are excluded from CLAUDE.md; only instructions relevant to 80%+ of typical sessions are included

**F-02.5: Existing CLAUDE.md — unconditional update**
- **GIVEN** a CLAUDE.md already exists
- **WHEN** the operator re-runs /compiling-project-settings
- **THEN** the skill updates the file unconditionally to reflect the current codebase state and reports "updated" rather than "created" in its summary; it does not prompt for confirmation

**F-02.6: Line count exceeding 100 flagged**
- **GIVEN** the generated CLAUDE.md would exceed 100 lines
- **WHEN** the skill validates its output
- **THEN** it trims or moves niche content to docs/ references rather than producing an oversized file; the final CLAUDE.md stays at or under ~100 lines

**F-02.7: Not in a git repository (failure)**
- **GIVEN** the skill is invoked outside a git repository
- **WHEN** it attempts to analyze the codebase
- **THEN** it reports the git requirement and halts without creating CLAUDE.md

**F-02.8: --focus argument narrows emphasis**
- **GIVEN** the operator passes --focus "testing" (or another area)
- **WHEN** CLAUDE.md is generated
- **THEN** the testing conventions and commands receive additional detail relative to other sections; all other sections remain present

---

## F-03: Project Documentation Compilation | MUST

**Requires:** F-02 (Project Settings Compilation)

**F-03.0: CLAUDE.md missing — hard failure**
- **GIVEN** CLAUDE.md does not exist
- **WHEN** /compiling-project-docs is invoked
- **THEN** it fails immediately and directs the operator to run /compiling-project-settings first; no docs/ files are created; this matches the behavior of all other compilation skills

**F-03.1: docs/ directory generated with detected topics (happy path)**
- **GIVEN** an operator invokes /compiling-project-docs in a project with CLAUDE.md
- **WHEN** the skill analyzes the codebase
- **THEN** it generates a docs/ directory; each detected topic with >30% signal confidence gets its own markdown file; docs/index.md is always generated last as a navigation overview

**F-03.2: Document generation follows dependency order**
- **GIVEN** the skill generates multiple docs/ files
- **WHEN** determining the generation sequence
- **THEN** docs/architecture.md is generated first (referenced by all agents), followed by topic-specific files, with docs/index.md last

**F-03.3: Each document includes AI Context Summary**
- **GIVEN** any docs/ file is generated
- **WHEN** the file is written
- **THEN** it contains an AI Context Summary at the top: a 1-3 sentence description that allows an agent to decide whether it needs to read the full file without reading the full file

**F-03.4: No placeholder text in generated files**
- **GIVEN** the skill is generating a document for a detected topic
- **WHEN** content is produced
- **THEN** no [TODO], [FILL IN], or equivalent placeholder strings appear in the output; all sections contain actual content derived from the codebase

**F-03.5: Code snippets include file paths**
- **GIVEN** a generated document includes a code example
- **WHEN** the snippet is written
- **THEN** the snippet is annotated with the source file path so agents can locate the referenced code in the project

**F-03.6: Topic not detected — file not generated**
- **GIVEN** the codebase contains no signals for a topic (e.g., no Terraform files for a deployment.md)
- **WHEN** the skill evaluates whether to generate that document
- **THEN** the document is not generated; the skill does not produce empty or placeholder docs for absent topics

**F-03.7: User override — include specific topic**
- **GIVEN** the operator passes an include argument (e.g., "include: security")
- **WHEN** the skill generates docs/
- **THEN** a security.md is generated even if signal confidence is below 30%; the content is based on whatever relevant patterns exist in the codebase

**F-03.8: User override — skip specific topic**
- **GIVEN** the operator passes a skip argument (e.g., "skip: api")
- **WHEN** the skill generates docs/
- **THEN** docs/api.md is not generated even if the codebase has strong API signals

**F-03.9: Cross-reference links valid**
- **GIVEN** a generated document contains links to other docs/ files
- **WHEN** the skill validates its output
- **THEN** all referenced files either exist or are being generated in the same run; broken cross-reference links are not left in generated files

---

## F-04: Planner Agent Compilation | MUST

**Requires:** F-02 (Project Settings Compilation), F-03 (Project Documentation Compilation)

**F-04.1: planner.md generated with project-specific context (happy path)**
- **GIVEN** an operator invokes /compiling-planner-agent and CLAUDE.md exists
- **WHEN** the skill reads CLAUDE.md and docs/
- **THEN** it generates .claude/agents/planner.md with these sections: YAML frontmatter, Mission, Before Any Task (with doc references), Design Constraints, Workflow, Task Description Must Include, Output Format, Quality Check, References; the file is 50-100 lines

**F-04.2: CLAUDE.md missing — hard failure**
- **GIVEN** CLAUDE.md does not exist
- **WHEN** the skill is invoked
- **THEN** it fails immediately with an error directing the operator to run /compiling-project-settings first; no agent file is created

**F-04.3: Doc references are conditional on file existence**
- **GIVEN** docs/workflow.md exists but docs/security.md does not
- **WHEN** the Before Any Task section is generated
- **THEN** only docs/workflow.md is referenced; docs/security.md is not referenced since it doesn't exist; the agent does not reference files that don't exist in the project

**F-04.4: No docs/ directory — references omitted without failure**
- **GIVEN** CLAUDE.md exists but no docs/ directory has been generated
- **WHEN** the planner agent is compiled
- **THEN** the agent is generated without doc references in Before Any Task; the skill does not fail, but it may warn that docs/ is missing

**F-04.5: Task description template includes architectural fields**
- **GIVEN** the planner agent is being compiled
- **WHEN** the Task Description Must Include section is generated
- **THEN** it specifies fields for: current state analysis, proposed solution, files to modify (with line numbers), implementation steps, dependencies, and expected errors — sufficient for a builder to execute mechanically

**F-04.6: Content not duplicated from CLAUDE.md**
- **GIVEN** CLAUDE.md contains the project's key directories and commands
- **WHEN** the planner agent is compiled
- **THEN** the agent file references CLAUDE.md for that context rather than restating it; no content present in CLAUDE.md appears inline in the agent file

**F-04.7: Existing planner.md — unconditional update**
- **GIVEN** .claude/agents/planner.md already exists
- **WHEN** the skill is invoked
- **THEN** the skill updates the file unconditionally and reports "updated" in its summary; it does not fail, prompt for confirmation, or create a duplicate

---

## F-05: Builder Agent Compilation | MUST

**Requires:** F-02 (Project Settings Compilation), F-03 (Project Documentation Compilation)

**F-05.1: builder.md generated with quality gate (happy path)**
- **GIVEN** an operator invokes /compiling-builder-agent and CLAUDE.md exists
- **WHEN** the skill reads CLAUDE.md and docs/
- **THEN** it generates .claude/agents/builder.md containing: YAML frontmatter, Mission, Before Any Task, Workflow (with /reviewing-code-quality gate step), Quality Principles, Rules, Output Format, Anti-Patterns table, References; the file is 50-100 lines

**F-05.2: CLAUDE.md missing — hard failure**
- **GIVEN** CLAUDE.md does not exist
- **WHEN** the skill is invoked
- **THEN** it fails immediately and directs the operator to run /compiling-project-settings first; no agent file is created

**F-05.3: /reviewing-code-quality gate present in workflow**
- **GIVEN** the builder agent workflow is being generated
- **WHEN** the Workflow section is written
- **THEN** /reviewing-code-quality appears as a mandatory gate step that the builder must pass before declaring work complete; its omission is a compilation defect

**F-05.4: Quality Principles section present**
- **GIVEN** the builder agent is being compiled
- **WHEN** the Quality Principles section is generated
- **THEN** it contains writing defaults (e.g., test every function, prefer readability) that are embedded as first principles — not an after-the-fact rubric

**F-05.5: Anti-patterns capped at 5 entries**
- **GIVEN** the codebase and tech stack suggest several anti-patterns to avoid
- **WHEN** the Anti-Patterns section is generated
- **THEN** at most 5 entries are included; the most impactful patterns are selected and lower-priority ones are omitted to stay within the line limit

**F-05.6: Builder does not make design decisions**
- **GIVEN** the builder agent encounters an ambiguous requirement in a task file
- **WHEN** the agent is compiled
- **THEN** its Workflow section specifies that it reports blockers to the operator rather than inventing solutions; the compiled agent is explicitly instructed not to make design decisions

**F-05.7: Content not duplicated from CLAUDE.md or docs/**
- **GIVEN** CLAUDE.md contains the tech stack and testing framework
- **WHEN** the builder agent is compiled
- **THEN** the agent references CLAUDE.md and docs/ for that context; it does not inline stack-specific patterns that are already present in referenced files

**F-05.8: Monorepo with multiple stacks — both stacks included**
- **GIVEN** the codebase is a monorepo with multiple tech stacks detected (e.g., Python backend and JavaScript frontend)
- **WHEN** the builder agent is compiled
- **THEN** the agent includes patterns, test commands, and conventions for all detected stacks; instructions are organized by directory context so the builder knows which patterns apply to which part of the codebase

---

## F-06: Security Agent Compilation | SHOULD

**Requires:** F-02 (Project Settings Compilation)

**F-06.1: security.md generated with stack-specific checks (happy path)**
- **GIVEN** an operator invokes /compiling-security-agent and CLAUDE.md exists
- **WHEN** the skill reads CLAUDE.md and detects the tech stack
- **THEN** it generates .claude/agents/security.md with stack-specific vulnerability checks — not generic OWASP descriptions; the top 5 checks target the detected stack's known attack surface

**F-06.2: CLAUDE.md missing — hard failure**
- **GIVEN** CLAUDE.md does not exist
- **WHEN** the skill is invoked
- **THEN** it fails immediately and directs the operator to run /compiling-project-settings first; no agent file is created

**F-06.3: Auth mechanism auto-detected**
- **GIVEN** the codebase uses JWT authentication
- **WHEN** the skill scans the project
- **THEN** it identifies the auth mechanism and includes JWT-specific checks (e.g., algorithm confusion, missing expiry validation) in the security agent's Top 5 Checks

**F-06.4: Proof-of-concept commands required**
- **GIVEN** a vulnerability check is included in the security agent
- **WHEN** the Attack Tests section is generated
- **THEN** each check includes an actual runnable PoC command (e.g., a curl command testing the vulnerability), not just a prose description of what to check

**F-06.5: Stack-specific scanner command included**
- **GIVEN** the tech stack has a known security scanner (e.g., npm audit, cargo audit, bandit)
- **WHEN** the security agent is compiled
- **THEN** the Quick Scan section contains the exact command to run that scanner against the project

**F-06.6: Compliance focus applied when specified**
- **GIVEN** the operator passes a compliance standard as argument (e.g., SOC2, HIPAA, PCI-DSS)
- **WHEN** the security agent is compiled
- **THEN** the checks are scoped to that compliance standard's requirements for the detected stack; generic checks are deprioritized in favor of compliance-mandated ones

**F-06.7: Unrecognizable stack — generic but still functional**
- **GIVEN** the codebase uses a stack with no recognized patterns
- **WHEN** the security agent is compiled
- **THEN** the agent is generated with the most broadly applicable checks; the skill notes that stack-specific tuning was not possible and recommends manual review

---

## F-07: DevOps Agent Compilation | COULD

**F-07.1: devops.md generated for detected infrastructure (happy path)**
- **GIVEN** an operator invokes /compiling-devops-agent in a project with infrastructure files (e.g., Dockerfile, .github/workflows/)
- **WHEN** the skill scans for infrastructure artifacts
- **THEN** it generates .claude/agents/devops.md containing only commands for detected tools; undetected tools are not included; the file is 50-80 lines

**F-07.2: CLAUDE.md missing — hard failure**
- **GIVEN** CLAUDE.md does not exist
- **WHEN** the skill is invoked
- **THEN** the skill fails immediately and directs the operator to run /compiling-project-settings first; consistent with all other agent compilation skills

**F-07.3: Never-modify-application-code constraint always present**
- **GIVEN** the devops agent is being compiled
- **WHEN** the Constraint section is generated
- **THEN** an explicit hard constraint stating the agent must never modify application code appears in the agent file; its omission is a compilation defect

**F-07.4: No speculative tooling**
- **GIVEN** the project has no Terraform files
- **WHEN** the skill generates the devops agent
- **THEN** Terraform commands are not included in the agent; only tools with evidence in the codebase are referenced

**F-07.5: Cloud provider focus applied when specified**
- **GIVEN** the operator passes a cloud provider argument (e.g., AWS)
- **WHEN** the devops agent is compiled
- **THEN** AWS-specific patterns, CLI commands, and service names are emphasized over generic equivalents; GCP/Azure patterns are omitted unless also detected

**F-07.6: Existing devops.md — unconditional update**
- **GIVEN** .claude/agents/devops.md already exists
- **WHEN** the skill is invoked
- **THEN** the skill updates the file unconditionally and reports "updated" in its summary; consistent with all other compilation skills

---

## F-08: Compilation Constraint Enforcement | MUST

**F-08.1: 80% rule validation — shows violations, asks to confirm removal**
- **GIVEN** a compiled artifact (CLAUDE.md or agent file) contains instructions that appear to apply to fewer than 80% of sessions
- **WHEN** the skill validates its output
- **THEN** it identifies the niche instructions, presents them to the operator with a reason for each (e.g., "this applies only to the migration tooling used once"), and asks whether to remove or keep each before writing the final artifact

**F-08.2: 80% rule applied to agent content**
- **GIVEN** the skill is deciding whether to include an instruction in a compiled agent
- **WHEN** the instruction applies to fewer than 80% of that agent's typical tasks
- **THEN** the instruction is excluded from the agent file; if the context is needed, a reference to docs/ is provided instead

**F-08.3: 150-instruction budget respected**
- **GIVEN** CLAUDE.md and all agent files are generated
- **WHEN** the total instruction count is approximated
- **THEN** CLAUDE.md and all compiled agent files together stay within ~100 lines of instruction content, leaving room for Claude Code's ~50-instruction system prompt share

**F-08.4: Reference-not-duplicate enforced**
- **GIVEN** project context exists in CLAUDE.md (e.g., key directories, commands)
- **WHEN** an agent is compiled and needs that context
- **THEN** the agent references CLAUDE.md rather than copying the content; duplicated content is treated as a compilation defect

**F-08.5: Agent naming convention enforced**
- **GIVEN** a compilation skill generates an agent file
- **WHEN** the YAML frontmatter name field is set
- **THEN** the name is a kebab-case noun (e.g., code-reviewer, task-planner); gerunds and non-kebab-case names are invalid

**F-08.6: Skill naming convention enforced**
- **GIVEN** an agent-author session creates a new skill
- **WHEN** the skill name is determined
- **THEN** the name is a gerund in kebab-case (e.g., reviewing-code, compiling-planner-agent); noun names and non-gerund forms are invalid

---

## Open Questions

*(All open questions resolved.)*

## Assumptions

- **A-01**: [ASSUMPTION] /compiling-project-docs requires CLAUDE.md to exist (same as agent compilers) even though the source does not explicitly state a hard failure if it's missing.
- **A-02**: [ASSUMPTION] All compilation skills perform git repository verification, not just /compiling-agentic-workflow; the source documents this for the orchestrator but implies it for sub-skills.
- **A-03**: [ASSUMPTION] "Idempotent" means the output is functionally equivalent when re-run on an unchanged codebase; re-running on a changed codebase updates the artifact to match.
- **A-04**: [ASSUMPTION] The devops agent's softer pre-flight (WARN vs FAIL) for missing CLAUDE.md is intentional — infrastructure detection from filesystem artifacts alone is sufficient for minimal viability.
- **A-05**: [ASSUMPTION] Conditional doc references in agent files (only reference docs/ files that exist) are validated at write time, not at agent runtime; the compilation skill scans the actual docs/ directory.
- **A-05b**: [ASSUMPTION] /compiling-security-agent auto-detects the auth mechanism by scanning source code for patterns like "jwt", "bearer", "session" rather than reading a dedicated config file.
