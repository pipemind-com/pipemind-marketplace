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

## Files Modified

| File | Change |
|------|--------|
| `plugins/<plugin>/.claude-plugin/plugin.json` | `"version"` field updated |
| `.claude-plugin/marketplace.json` | `plugins[].version` for matching plugin updated |

## Steps

1. **Validate args** — plugin dir exists, bump type is `patch`, `minor`, or `major`
2. **Check prerequisites** — `jq` is installed, working tree is clean (bail if dirty)
3. **Read current version** — `jq -r .version` from `plugin.json`
4. **Compute new version** — split `major.minor.patch`, increment target component, zero lower ones
5. **Write plugin.json** — `jq` in-place update of `"version"`
6. **Write marketplace.json** — `jq` in-place update of the matching plugin entry's `"version"`
7. **Commit** — `git add` both files, commit message: `release(<plugin>): bump to v<version>`
8. **Tag** — `git tag <plugin>/v<version>`
9. **Push** — `git push && git push --tags`

## Error Handling

- Missing plugin dir → print usage, exit 1
- Invalid bump type → print usage, exit 1
- `jq` not found → clear message, exit 1
- Dirty working tree → bail before touching any files

## Design Decisions

- **`jq` for JSON** — clean diffs, no formatting surprises, no Python
- **Dirty tree check** — prevents unrelated changes from leaking into the release commit
- **Auto-push** — YOLO, no prompt
- **Tag format** `<plugin>/v<version>` — namespaced so multi-plugin repos stay clean
- **Commit format** `release(<plugin>): bump to v<version>` — conventional commit style
- **No marketplace-level version** — only plugin versions are tracked
