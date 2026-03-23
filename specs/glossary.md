# Domain Glossary

## Actors

**Plugin Developer**
Creates and publishes plugins to the marketplace. Writes agents, skills, and manifests. Runs `release.sh` to cut versions. Has direct access to the repository.
*Cannot:* modify a user's `~/.claude/` directory remotely; guarantee that a user's Claude Code version supports all skill features.

**Plugin User**
Installs plugins into their local `~/.claude/` directory and invokes agents and skills within their own projects. Interacts with `install.sh` and Claude Code's `/skill` and `--agent` interfaces.
*Cannot:* publish or release plugins; modify marketplace registry; alter plugin source files through installation.

**Claude Agent**
An autonomous AI subprocess spawned by Claude Code that reads agent instruction files and follows them to perform tasks. Consumes agents, skills, CLAUDE.md, and docs/ as inputs.
*Cannot:* modify its own instruction files; bypass tool permission restrictions defined in YAML frontmatter; access files outside the allowed tool set.

**Planner Agent**
A compiled project-specific agent (.claude/agents/planner.md) that designs solutions and writes task files. Thinks analytically; reads CLAUDE.md and docs/ to understand the project before planning.
*Cannot:* write production code, make implementation decisions, run tests, or modify its own definition.

**Builder Agent**
A compiled project-specific agent (.claude/agents/builder.md) that implements code according to task file specifications. Executes mechanically; must pass a quality gate before declaring work complete.
*Cannot:* make design decisions, modify task specs, skip the /reviewing-code-quality gate, or push to remote.

**Security Agent**
A compiled project-specific agent (.claude/agents/security.md) that performs adversarial red-team security audits against the project's stack-specific vulnerabilities.
*Cannot:* fix application logic or modify production code; only finds and reports vulnerabilities with proof-of-concept commands.

**DevOps Agent**
A compiled project-specific agent (.claude/agents/devops.md) that manages infrastructure configuration — Docker, CI/CD, Terraform, Kubernetes.
*Cannot:* modify application code under any circumstances; operates exclusively on infrastructure configuration files.

**Agent Author**
A meta-agent (agents/agent-author.md) installed globally that guides operators through creating new agents and skills. Teaches patterns and delegates to compilation skills.
*Cannot:* compile agents directly; only provides guidance, validates output, and references compilation skills.

**Orchestrator**
The /orchestrating-workflow skill that decomposes multi-part features into sub-tasks and coordinates parallel planner/builder pipelines.
*Cannot:* write production code or make design decisions; all code changes flow through builder subagents.

## Key Terms

**Plugin**
A self-contained directory under `plugins/<name>/` shipping agents, skills, and configuration. Identified by its manifest file (`.claude-plugin/plugin.json`).

**Marketplace Registry**
The authoritative index file (`.claude-plugin/marketplace.json`) listing all available plugins with name, version, source path, and description.

**Agent**
A markdown file with YAML frontmatter (`name`, `description`, `model`, `tools`, `color`) containing instructions for a Claude Agent subprocess. Installed to `~/.claude/agents/`. Invoked via `claude --agent <name>`.

**Skill**
A markdown file (`SKILL.md`) with YAML frontmatter (`name`, `description`, `user-invocable`) inside a gerund-named directory. Installed to `~/.claude/skills/<name>/`. Invoked via `/skill-name` in Claude Code.

**Manifest**
The JSON metadata file for a plugin at `.claude-plugin/plugin.json`, declaring name, version, description, author, agents, skills, and dependencies.

**Symlink Install**
Installation mode where agents and skills are symbolically linked from the plugin source to `~/.claude/`. Changes to source propagate automatically via `git pull`.

**Copy Install**
Installation mode where agents and skills are copied into `~/.claude/`. Source changes do not propagate; reinstallation is required.

**Semver Tag**
A git tag in the format `<plugin-name>/v<MAJOR>.<MINOR>.<PATCH>` created by `release.sh` to mark a published version.

**YAML Frontmatter**
A YAML block delimited by `---` at the top of a markdown file, declaring structured metadata consumed by Claude Code's agent and skill loaders.

**Progressive Disclosure**
The pattern where CLAUDE.md stays lean (50-100 lines) and references `docs/` files for detail. Agents load docs on demand rather than carrying all context inline.

**80% Rule**
The authoring constraint that every instruction in an agent or skill must apply to 80%+ of sessions. Instructions below this threshold belong in `docs/`.

**150-Instruction Limit**
Claude Code reliably follows ~150 instructions total. The system prompt uses ~50, leaving ~100 shared across CLAUDE.md and all loaded agents.

**Factory**
The global tier of the two-tier architecture, installed at `~/.claude/`. Contains the agent-author meta-agent and 14 reusable skills. Installed once per machine via symlink or copy.

**Product**
The local tier of the two-tier architecture, generated per project. Includes CLAUDE.md, docs/, and .claude/agents/ (planner, builder, and optional security/devops agents). Compiled by factory skills against a specific codebase.

**Compilation**
The process of analyzing a codebase and generating project-specific agents, settings, or documentation from factory skill templates. Each compilation skill reads CLAUDE.md and the codebase, then produces a tailored artifact.

**Task File**
A markdown document (tasks/NNN-name.md) written by the planner agent and read by the builder agent. Serves as the contract between planning and implementation — contains requirements, problem analysis, files to modify, and implementation steps.

**Quality Gate**
The mandatory /reviewing-code-quality invocation in the builder workflow. Builder agents must pass this gate before declaring work complete. Reviews code across 6 axes: purity, testability, abstraction, readability, documentation, robustness.

**Atomic Commit**
A single git commit containing exactly one logical unit of change — one feature, fix, refactor, or chore. Created by /git-commit-changes which splits all uncommitted work into grouped, well-described commits.

**Behavioral Spec**
An implementation-agnostic specification describing observable state changes in GIVEN-WHEN-THEN format. Generated by /defining-specs from source documents (PRDs, briefs, feature requests). Contains no code, no architecture, no tech stack assumptions.

**Test Scenario**
An exhaustive expansion of a single behavioral spec feature into granular, testable variations. Generated by /defining-test-scenarios. Each scenario tests exactly one behavior with deterministic entity labels.

**Property-Based Test**
An adversarial test generated by /stress-testing that uses random inputs (100+) to find edge cases. Uses hypothesis (Python), fast-check (JS/TS), or proptest (Rust) to verify invariants like round-trip, idempotence, and conservation.

**Post-Mortem**
A lessons-learned extraction performed by /conducting-post-mortem after task completion. Identifies gotchas and proposes specific CLAUDE.md updates to prevent recurrence — the mechanism by which agents get smarter over time.

**Research Session**
A problem directory (`<problem-slug>/`) containing the full state of a scientific method investigation: `problem.md`, `hypothesis-NN.md` files, `references.md`, `references/` downloads, `experiments/` artifacts, and `findings.md`.

**Experiment Artifacts**
Files produced during experiment execution — code scripts, downloaded datasets, analysis outputs — stored in `<problem-dir>/experiments/<hypothesis-slug>/`. Named `exp<N>.<ext>` (e.g., `hypothesis-01/exp1.py`). Numbered globally and sequentially per hypothesis across all iterations; numbers never reset. Each hypothesis gets its own subdirectory so parallel agents never collide. Artifacts accumulate across all iterations and are never deleted by the loop, including artifacts from failed runs. The path to each artifact is recorded inline in the hypothesis file's `Results` section. Experiments that produce no persistent artifact (math-proof, logical-deduction, inline evidence-gathering) write nothing here. Distinct from experiment plans, which remain inline in hypothesis files.

**Problem Statement**
The refined, operator-confirmed formulation in `problem.md`. Includes scope, constraints, key unknowns, and success criteria. Serves as the sole source of truth for all autonomous research steps.

**Hypothesis**
A testable, falsifiable claim in `hypothesis-NN.md`. Progresses through a lifecycle: `pending` → refined with literature → experiments designed → experiments run → concluded (`confirmed` / `refuted` / `inconclusive`).

**Verdict**
The conclusion about a hypothesis after experiments: `confirmed` (evidence supports it), `refuted` (counterexample found), or `inconclusive` (insufficient or contradictory evidence).

**Experiment**
A designed verification path within a hypothesis file. Types: `code`, `math-proof`, `evidence-gathering`, `data-analysis`, `logical-deduction`. Each specifies approach, confirmation criteria, and refutation criteria.

**REF-NNN**
A stable identifier assigned to each source in `references.md`. Sequential, never reused. All skills cite sources by this ID.

**Findings**
The terminal output of the research loop (`findings.md`). Written when the loop exits — either because a hypothesis was confirmed and satisfies success criteria, or because MAX_ITERATIONS was reached.
