# Workflow

> **AI Context Summary**: Developing marketplace plugins follows a spec-first, agent-assisted pattern.
> The `pm-workflow` plugin's planner/builder agents apply to the marketplace itself — use them to plan
> and implement new plugins or skill additions. Skills are live the moment files change (no restart).
> Agent changes require re-installing the plugin to take effect.

## Developing the Marketplace

### Adding a Skill to pm-workflow

1. Plan with the planner agent:
   ```bash
   claude --agent planner
   # "Add a skill for <purpose> to pm-workflow"
   ```

2. Implement with the builder agent:
   ```bash
   claude --agent builder
   # reads the task file, creates plugins/pm-workflow/skills/<gerund>/SKILL.md
   ```

3. Skills are live immediately — no reinstall needed. Verify in `system-reminder` context.

### Adding a New Agent

1. Author the agent file following the 50-100 line constraint with YAML frontmatter
2. Place at `plugins/<name>/agents/<name>.md`
3. Reinstall to pick up changes:
   ```bash
   ./install.sh <plugin> --symlink
   ```

### Adding a New Plugin

See [getting-started.md](./getting-started.md) for the full plugin creation checklist.

## Planner → Builder Pattern

The `pm-workflow` plugin's agents apply to developing the marketplace itself:

```
You (main thread)
    │
    ├─► claude --agent planner
    │       Reads CLAUDE.md + docs/
    │       Analyzes existing plugins
    │       Returns task description in conversation
    │
    └─► claude --agent builder
            Receives task description via prompt
            Creates plugin files exactly as specified
            Returns completion status
```

| Agent | Role | Output |
|-------|------|--------|
| **planner** | Designs plugin/skill structure, all file paths and frontmatter | Task description in conversation |
| **builder** | Implements mechanically from task description | Plugin files |

## Release Workflow

```bash
# 1. Implement and commit changes
git add plugins/<name>/...
git commit -m "feat: add <feature>"

# 2. Cut release (bumps version, tags, pushes)
./release.sh <plugin-name> patch
```

Release requires a clean working tree. See `release.sh` for full validation steps.

## Symlink Update Propagation

With symlink installs, changes propagate automatically:

```bash
git pull          # pulls latest plugin files
                  # symlinks already point to updated files
                  # skills live immediately; agents need claude restart
```

## Cross-References

- Architecture and install flow: [architecture.md](./architecture.md)
- Plugin formats: [tech-stack.md](./tech-stack.md)
- pm-workflow workflow details: `plugins/pm-workflow/docs/workflow.md`
