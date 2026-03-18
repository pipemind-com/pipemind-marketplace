# Design: `release.sh` — Plugin Version Bump Script

**Date:** 2026-03-18
**Status:** Approved

## Summary

A shell script (`release.sh`) that bumps a plugin's semver version, syncs it to the marketplace registry, commits, tags, and pushes — all in one command.

## Invocation

```bash
./release.sh <plugin-name> <patch|minor|major>
```

Examples:
```bash
./release.sh pm-workflow patch   # 1.0.0 → 1.0.1
./release.sh pm-workflow minor   # 1.0.0 → 1.1.0
./release.sh pm-workflow major   # 1.0.0 → 2.0.0
```

## Key Paths

```bash
PLUGIN_JSON="plugins/$PLUGIN/.claude-plugin/plugin.json"
MARKETPLACE_JSON=".claude-plugin/marketplace.json"
```

`AGENTS_SRC` and `SKILLS_SRC` in `install.sh` remain at `plugins/<plugin>/agents/` and `plugins/<plugin>/skills/` — those are correct and do not change.

## Files Modified

| File | Change |
|------|--------|
| `plugins/<plugin>/.claude-plugin/plugin.json` | `"version"` field updated |
| `.claude-plugin/marketplace.json` | matching `plugins[].version` entry updated |

## Steps

1. **Root anchor** — `cd "$(dirname "$0")"` so all relative paths resolve correctly regardless of invocation location
2. **Validate args** — plugin dir exists, bump type is `patch`, `minor`, or `major`; bail with usage on failure
3. **Check prerequisites** — `jq` is installed; bail with clear message if not
4. **Check clean tree** — `git diff --exit-code && git diff --cached --exit-code`; bail if dirty
5. **Read current version** — `jq -r .version "$PLUGIN_JSON"`
6. **Compute new version** — split `major.minor.patch`, increment target component, zero lower ones
7. **Check tag does not exist** — `git tag -l "<plugin>/v<new-version>"` must be empty; bail if tag already exists (prevents orphaned release commits)
8. **Verify marketplace entry exists** — `jq -e --arg name "$PLUGIN" '.plugins[] | select(.name == $name)' "$MARKETPLACE_JSON"` must succeed; bail if no matching entry (prevents silent no-op write)
9. **Write plugin.json** — jq to temp file, then `mv`
10. **Write marketplace.json** — same idiom, using select-by-name filter
11. **Commit** — `git add "$PLUGIN_JSON" "$MARKETPLACE_JSON"`, commit: `release(<plugin>): bump to v<version>`
12. **Tag** — `git tag <plugin>/v<version>`
13. **Push** — `git push --follow-tags`

## Shell Requirements

```bash
set -euo pipefail
cd "$(dirname "$0")"
```

### jq write idiom

```bash
tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT

jq --arg v "$NEW_VERSION" '.version = $v' "$PLUGIN_JSON" > "$tmp" && mv "$tmp" "$PLUGIN_JSON"

# map/if form — safe on jq 1.5 and 1.6+
jq --arg name "$PLUGIN" --arg v "$NEW_VERSION" \
  '.plugins = [.plugins[] | if .name == $name then .version = $v else . end]' \
  "$MARKETPLACE_JSON" > "$tmp" && mv "$tmp" "$MARKETPLACE_JSON"
```

## `install.sh` Fix (in scope)

Two references in `install.sh` use the stale path `plugin.json` (without `.claude-plugin/`):

- **Line 17** — the usage-listing loop: `jq -r '.description' "$dir/plugin.json"` → `"$dir/.claude-plugin/plugin.json"`
- **Lines 25–27** — the existence check path and its error message string: both `"$PLUGIN_DIR/plugin.json"` occurrences → `"$PLUGIN_DIR/.claude-plugin/plugin.json"`

`AGENTS_SRC` and `SKILLS_SRC` (lines 30–31) remain unchanged — those paths are correct.

## Error Handling

| Condition | Behavior |
|-----------|----------|
| Missing plugin dir | Print usage, exit 1 |
| Invalid bump type | Print usage, exit 1 |
| `jq` not found | Clear message, exit 1 |
| Dirty working tree | Bail before touching files |
| Tag already exists | Bail before committing |
| Plugin missing from marketplace.json | Bail before writing (step 8 pre-flight check) |
| Push failure | No rollback; `--follow-tags` keeps tag/commit in sync |
| First jq write succeeds, second fails | `plugin.json` modified, `marketplace.json` not — tree left dirty; user must fix and re-run (acknowledged, no automated rollback) |

## Design Decisions

- **Root anchor** — invocation-location-agnostic
- **`jq` for JSON** — clean diffs, no Python
- **Temp-file + `trap`** — safe write idiom; avoids truncation, cleans up temp files
- **`set -euo pipefail`** — consistent with `install.sh`
- **Tag-exists check before commit** — never orphaned release commits
- **`--follow-tags`** — tag only pushed if its commit was pushed
- **Auto-push** — no prompt
- **Tag format** `<plugin>/v<version>` — namespaced for multi-plugin repos
- **Commit format** `release(<plugin>): bump to v<version>` — conventional commits
- **No marketplace-level version** — only plugin versions tracked
