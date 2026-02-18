---
name: committing-changes
description: Splits all git changes into atomic commits of related changes
user-invocable: true
argument-hint: "none required - analyzes current working tree"
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
model: sonnet
color: green
---

# Committing Changes

Split all uncommitted git changes into atomic, well-described commits grouped by logical relationship.

## Rules

- NEVER include `Co-Authored-By` lines in commit messages
- NEVER amend existing commits
- NEVER push to remote
- Each commit must be a single logical unit: one feature, one fix, one refactor, one chore
- Prefer more smaller commits over fewer large ones

## Process

**1. Survey all changes**

Run in parallel:
- `git status` (staged, unstaged, untracked)
- `git diff` (unstaged changes)
- `git diff --cached` (staged changes)

If the working tree is clean, say so and stop.

**2. Understand the changes**

Read changed files as needed. Group changes into atomic units by asking: *"If I had to revert one thing without affecting anything else, what's the smallest coherent set?"*

Grouping heuristics (in priority order):
1. **Same concern**: Changes to a function and its tests belong together
2. **Same feature**: Related changes across files for one feature
3. **Same type**: Pure renames, pure formatting, pure dependency bumps
4. **Config/chore**: Lock files, CI config, tooling changes

**3. Plan the commit sequence**

Print a numbered plan before committing:
```
Plan:
1. [type] Short description — file1, file2
2. [type] Short description — file3
...
```

Wait for user confirmation. If the user says nothing or approves, proceed.

**4. Execute commits**

For each planned commit:
- `git add <specific files>` (use `-p` via Bash only if a file contains changes for multiple commits)
- `git commit -m "<type>: <concise description>"` using conventional commit types (feat, fix, refactor, chore, docs, test, style)
- Commit message body (if needed) explains *why*, not *what*

**5. Verify**

Run `git log --oneline -n <count>` to show the new commits.
