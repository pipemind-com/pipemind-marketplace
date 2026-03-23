# Spec: spec-driven-development --- Installation & Distribution
**Source:** plugins/spec-driven-development/ (brownfield reverse-engineering)
**Epic:** E-A
**Glossary:** specs/glossary.md
**Generated:** 2026-03-22
**Status:** DRAFT --- requires operator review

## System Constraints

- **SC-01**: The installer runs as a Bash script requiring a POSIX-compatible shell with `set -euo pipefail`; it is not portable to PowerShell or Cmd natively
- **SC-02**: The target directory defaults to `$HOME/.claude/` and may be overridden via the `CLAUDE_DIR` environment variable
- **SC-03**: The installer validates a plugin by checking for `<plugin-dir>/.claude-plugin/plugin.json`; a plugin without this manifest is considered nonexistent
- **SC-04**: Skills must reside in a gerund-named directory containing a file named exactly `SKILL.md`; Claude Code will not discover skills with any other naming
- **SC-05**: Agents must be markdown files in `~/.claude/agents/`; Claude Code discovers them by filename and invokes them via `claude --agent <stem>`
- **SC-06**: The spec-driven-development factory comprises exactly 14 skill directories and 1 agent file at the time of this writing
- **SC-07**: Claude Code imposes a 150-instruction limit across its system prompt, CLAUDE.md, and all loaded agents combined; the system prompt consumes approximately 50, leaving approximately 100 for user-controlled files
- **SC-08**: Factory skills are listed in the system-reminder and take effect immediately upon file change when installed via symlink; no Claude Code restart is required for skill changes
- **SC-09**: Version is tracked in both `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`; `release.sh` bumps both atomically and creates a semver git tag in the format `<plugin-name>/v<MAJOR>.<MINOR>.<PATCH>`

---

### F-01: Global Factory Installation | MUST

#### F-01.1: Symlink installation succeeds with valid plugin

GIVEN the operator is in the root of the agentic-marketplace repository
AND `plugins/spec-driven-development/.claude-plugin/plugin.json` exists
AND `~/.claude/` is writable (or `CLAUDE_DIR` points to a writable directory)
WHEN the operator runs `./install.sh spec-driven-development --symlink`
THEN `~/.claude/agents/` contains a symbolic link for each markdown file in `plugins/spec-driven-development/agents/`
AND `~/.claude/skills/` contains a symbolic link for each subdirectory in `plugins/spec-driven-development/skills/`
AND each agent symlink points to the absolute path of its source file
AND each skill symlink points to the absolute path of its source directory
AND the installer prints a confirmation line for every linked agent and skill
AND the installer prints verification commands referencing `$CLAUDE_DIR`

#### F-01.2: Copy installation succeeds with valid plugin

GIVEN the same preconditions as F-01.1
WHEN the operator runs `./install.sh spec-driven-development` (without `--symlink`)
THEN all agent markdown files are recursively copied into `~/.claude/agents/`
AND all skill directories are recursively copied into `~/.claude/skills/`
AND no symbolic links are created
AND the installer prints a confirmation line for agents and skills

#### F-01.3: Target directory is auto-created when absent

GIVEN `~/.claude/agents/` and `~/.claude/skills/` do not yet exist
WHEN the operator runs `./install.sh spec-driven-development --symlink` (or without `--symlink`)
THEN the installer creates `~/.claude/agents/` and `~/.claude/skills/` via `mkdir -p` before writing any files
AND installation proceeds normally

#### F-01.4: Installation fails when plugin manifest is missing

GIVEN the operator runs `./install.sh spec-driven-development`
AND `plugins/spec-driven-development/.claude-plugin/plugin.json` does not exist
WHEN the installer checks for the manifest
THEN the installer exits with a non-zero status
AND prints an error message identifying the missing manifest path

#### F-01.5: Installation fails when no plugin name is provided

GIVEN the operator runs `./install.sh` with no arguments
WHEN the installer parses its arguments
THEN the installer exits with a non-zero status
AND prints a usage message listing all available plugins with their descriptions read from each plugin's manifest

#### F-01.6: Symlink overwrites existing targets

GIVEN `~/.claude/agents/agent-author.md` already exists (as a regular file or a stale symlink)
WHEN the operator runs `./install.sh spec-driven-development --symlink`
THEN the existing file or symlink is replaced by the new symlink (the installer uses `ln -sf`)
AND no interactive confirmation is requested

#### F-01.7: Symlink overwrites existing skill directories

GIVEN `~/.claude/skills/compiling-planner-agent/` already exists
WHEN the operator runs `./install.sh spec-driven-development --symlink`
THEN the existing skill directory is removed (via `rm -rf`) before the new symlink is created
AND the new symlink points to the source skill directory

#### F-01.8: Verification of installed artifacts

GIVEN installation completed successfully (symlink or copy)
WHEN the operator runs `ls ~/.claude/agents/agent-author.md`
THEN the file exists
WHEN the operator counts files matching `~/.claude/skills/*/SKILL.md`
THEN the count equals 14

#### F-01.9: Plugin with no agents directory installs only skills

GIVEN a plugin whose source has a `skills/` directory but no `agents/` directory
WHEN the operator runs the installer for that plugin
THEN only skills are installed
AND no error is raised about missing agents

#### F-01.10: Plugin with no skills directory installs only agents

GIVEN a plugin whose source has an `agents/` directory but no `skills/` directory
WHEN the operator runs the installer for that plugin
THEN only agents are installed
AND no error is raised about missing skills

#### F-01.11: Permission error halts installation

GIVEN `~/.claude/` exists but the operator lacks write permission to it
WHEN the operator runs `./install.sh spec-driven-development --symlink`
THEN the installer exits with a non-zero status due to `set -euo pipefail`
AND a system-level permission error is surfaced
AND no partial installation artifacts are guaranteed to be cleaned up [ASSUMPTION]

---

### F-02: Two-Tier Architecture Enforcement | MUST

#### F-02.1: Factory tier contains only reusable, project-agnostic content

GIVEN the factory is installed at `~/.claude/`
WHEN any operator inspects the factory tier contents
THEN `~/.claude/agents/` contains only the `agent-author.md` meta-agent
AND `~/.claude/skills/` contains only the 14 factory skill directories
AND no project-specific CLAUDE.md, no project-specific docs/, and no compiled planner, builder, security, or devops agents reside in the factory tier

#### F-02.2: Product tier resides within each project root

GIVEN the operator has compiled agents for a project
WHEN the operator inspects the project root
THEN `CLAUDE.md` exists at the project root (50 to 100 lines, governed by the 80% rule)
AND `docs/` exists at the project root containing detailed documentation files
AND `.claude/agents/` exists containing project-specific compiled agents (at minimum planner and builder)
AND none of these product files exist inside `~/.claude/`

#### F-02.3: Product compilation cannot modify the factory

GIVEN a factory skill is invoked within a project (for example `/compiling-planner-agent`)
WHEN the skill executes and generates output
THEN all generated files are written to the project's local directories (project root, `docs/`, `.claude/agents/`)
AND no files in `~/.claude/` are created, modified, or deleted by the skill invocation

#### F-02.4: Factory skills follow naming and size constraints

GIVEN any skill file in the factory tier
WHEN the skill is inspected
THEN the skill resides in a directory named with a gerund (present participle) form
AND the skill file is named `SKILL.md`
AND the skill file contains YAML frontmatter with `user-invocable: true` and a gerund-form `name`
AND the skill file is between 100 and 200 lines

#### F-02.5: Agent files follow size constraints

GIVEN any agent file in either the factory or product tier
WHEN the agent file is inspected
THEN the file is between 50 and 100 lines
AND contains YAML frontmatter with `name`, `description`, `model`, `tools`, and `color` fields

#### F-02.6: Factory editing in symlink mode affects all future compilations

GIVEN the factory was installed via symlink
AND the operator edits a skill file in `plugins/spec-driven-development/skills/`
WHEN any project subsequently invokes that skill
THEN the modified version of the skill is used
AND existing product artifacts in other projects remain unchanged until explicitly re-compiled

#### F-02.7: Product editing in one project does not affect other projects

GIVEN two projects (Project-A and Project-B) both have compiled products
WHEN the operator edits `Project-A/.claude/agents/planner.md`
THEN `Project-B/.claude/agents/planner.md` remains unchanged
AND the factory tier at `~/.claude/` remains unchanged

---

### F-03: Factory Update Propagation | SHOULD

#### F-03.1: Symlink mode propagates updates on git pull

GIVEN the factory was installed via `./install.sh spec-driven-development --symlink`
AND `~/.claude/skills/compiling-planner-agent` is a symbolic link pointing to the source repository
WHEN the operator runs `git pull` in the source repository and the pull modifies a factory skill
THEN the skill at `~/.claude/skills/compiling-planner-agent/SKILL.md` reflects the updated content immediately
AND no re-installation step is required

#### F-03.2: Symlink mode skill changes take effect without restart

GIVEN a skill is installed via symlink and is listed in the system-reminder
WHEN the source file for that skill is modified (via git pull or direct edit)
THEN the next invocation of that skill in any Claude Code session uses the updated content
AND no Claude Code restart or reinstallation is required

#### F-03.3: Copy mode does not propagate updates

GIVEN the factory was installed via `./install.sh spec-driven-development` (copy mode)
WHEN the operator runs `git pull` in the source repository and the pull modifies a factory skill
THEN `~/.claude/skills/` still contains the old version of the skill
AND the operator must re-run `./install.sh spec-driven-development` or manually copy files to update

#### F-03.4: Version is tracked and tagged via release.sh

GIVEN the operator wants to release a new version of spec-driven-development
AND the git working tree is clean
WHEN the operator runs `./release.sh spec-driven-development patch` (or `minor` or `major`)
THEN the version in `.claude-plugin/plugin.json` is bumped according to semver rules
AND the version in `.claude-plugin/marketplace.json` is bumped to the same value
AND a git commit is created with message `chore: release spec-driven-development v<NEW_VERSION>`
AND a git tag `spec-driven-development/v<NEW_VERSION>` is created
AND the commit and tag are pushed to the remote

#### F-03.5: Release fails when working tree is dirty

GIVEN the operator has uncommitted changes in the repository
WHEN the operator runs `./release.sh spec-driven-development patch`
THEN the script exits with a non-zero status
AND prints an error instructing the operator to commit or stash changes
AND no version bump, commit, or tag is created

#### F-03.6: Release fails when tag already exists

GIVEN the target semver tag already exists in the git history
WHEN the operator runs `./release.sh spec-driven-development patch`
THEN the script exits with a non-zero status
AND prints an error identifying the duplicate tag
AND no files are modified

#### F-03.7: Release fails when plugin is not in marketplace registry

GIVEN `spec-driven-development` is absent from `.claude-plugin/marketplace.json`
WHEN the operator runs `./release.sh spec-driven-development patch`
THEN the script exits with a non-zero status
AND prints an error identifying the missing marketplace entry

#### F-03.8: Symlink survives across terminal sessions

GIVEN the factory was installed via symlink
WHEN the operator closes and reopens their terminal (or opens a new shell session)
THEN the symlinks in `~/.claude/agents/` and `~/.claude/skills/` remain intact
AND skills and agents are still discoverable by Claude Code

#### F-03.9: Symlink breaks if source repository is moved or deleted

GIVEN the factory was installed via symlink from `/path/to/agentic-marketplace`
WHEN the operator moves or deletes `/path/to/agentic-marketplace`
THEN the symlinks in `~/.claude/` become dangling (point to nonexistent targets)
AND Claude Code will fail to load the affected skills and agents
AND the operator must re-install from the new location to restore functionality [ASSUMPTION]

---

### F-04: Multi-Project Support | MUST

#### F-04.1: Single factory installation serves multiple projects

GIVEN the factory is installed at `~/.claude/` (via either symlink or copy)
WHEN the operator navigates to Project-A (a git repository) and invokes `/compiling-agentic-workflow`
AND then navigates to Project-B (a different git repository) and invokes `/compiling-agentic-workflow`
THEN both projects receive independently compiled products
AND the factory at `~/.claude/` is not modified by either compilation
AND each project's `.claude/agents/planner.md` contains instructions specific to that project's tech stack

#### F-04.2: Products are isolated between projects

GIVEN Project-A is a Python/FastAPI project with compiled agents
AND Project-B is a Rust/Tokio project with compiled agents
WHEN the operator modifies `Project-A/CLAUDE.md`
THEN `Project-B/CLAUDE.md` is unaffected
AND `Project-B/.claude/agents/builder.md` still references Rust-specific tooling
AND the factory tier is unaffected

#### F-04.3: New project compilation requires a git repository

GIVEN the operator navigates to a directory that is not a git repository
WHEN the operator invokes a compilation skill (for example `/compiling-project-settings`)
THEN the skill reports an error indicating that a git repository is required [ASSUMPTION]
AND no product files are generated

#### F-04.4: Re-compilation is idempotent

GIVEN Project-A already has compiled products (CLAUDE.md, docs/, .claude/agents/)
WHEN the operator re-runs `/compiling-agentic-workflow` in Project-A
THEN existing product files are overwritten with freshly compiled versions
AND the project remains in a valid state
AND no orphaned or duplicate files are created

#### F-04.5: Projects do not require awareness of each other

GIVEN three projects exist on the same machine, all using the same factory
WHEN the operator works in Project-C
THEN no skill or agent references or reads files from Project-A or Project-B
AND no shared state exists between projects outside the factory tier

#### F-04.6: Factory removal affects all projects

GIVEN three projects are using the factory installed at `~/.claude/`
WHEN the operator deletes `~/.claude/skills/` and `~/.claude/agents/`
THEN all three projects lose access to factory skills (slash-commands stop working)
AND all three projects lose access to the agent-author meta-agent
AND existing compiled product files in each project remain intact and functional for planner/builder workflows

#### F-04.7: Compilation order matters for correct product generation

GIVEN the operator navigates to a new project with no existing products
WHEN the operator invokes `/compiling-builder-agent` before `/compiling-project-settings`
THEN the builder agent may be generated without proper project context
AND the resulting agent may produce generic rather than stack-specific output [ASSUMPTION]
AND the operator should instead use `/compiling-agentic-workflow` which enforces correct ordering automatically

---

## Open Questions

- **OQ-01**: The install.sh script does not validate that the source repository is a git repository before installation. Should it? The getting-started.md mentions `git rev-parse --is-inside-work-tree` as a prerequisite for factory skills, but this check is not enforced at install time.
- **OQ-02**: When using copy mode, there is no mechanism to detect version drift between the installed copy and the source. Should the installer record the installed version somewhere in `~/.claude/` to allow drift detection?

**Version drift between factory and compiled project agents:** WON'T (this milestone). Operators are expected to re-compile project agents after updating the factory. No automated detection or warning is specified.
- **OQ-03**: The install.sh script uses `rm -rf` on existing skill directories before creating symlinks (F-01.7). If the existing directory contains operator customizations that were not backed up, those are silently destroyed. Should the installer warn before overwriting?
- **OQ-04**: The spec-driven-development CLAUDE.md notes a "legacy layout" for spec-driven-development using root `plugin.json`, but the actual codebase has `.claude-plugin/plugin.json`. This inconsistency in documentation should be resolved.
- **OQ-05**: There is no uninstall command. Operators must manually remove symlinks or copied files from `~/.claude/`. Should `install.sh` support an `--uninstall` flag?

## Assumptions

- **A-01**: The installer does not perform cleanup of partial installations on failure. If `set -euo pipefail` causes an exit mid-installation, some agents or skills may be installed while others are not. This is flagged in F-01.11.
- **A-02**: Factory skills enforce the git repository prerequisite at invocation time, not at install time. This is referenced in the getting-started docs but not directly verified in the installer script. Flagged in F-04.3.
- **A-03**: Compilation skills will produce degraded (generic) output rather than hard-fail when invoked out of order (for example, compiling a builder before compiling project settings). Flagged in F-04.7.
- **A-04**: Claude Code discovers skills and agents by scanning `~/.claude/skills/` and `~/.claude/agents/` on session start or on-demand. The exact discovery mechanism is not specified in the source material.
- **A-05**: Dangling symlinks (from a moved or deleted source repository) cause Claude Code to fail to load the affected resources rather than silently ignoring them. Flagged in F-03.9.
