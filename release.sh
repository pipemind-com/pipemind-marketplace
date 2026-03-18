#!/usr/bin/env bash
# Usage: ./release.sh <plugin-name> <patch|minor|major>
# Example: ./release.sh pm-workflow patch

set -euo pipefail
cd "$(dirname "$0")"

PLUGIN="${1:-}"
BUMP="${2:-}"

PLUGIN_DIR="plugins/$PLUGIN"
PLUGIN_JSON="$PLUGIN_DIR/.claude-plugin/plugin.json"
MARKETPLACE_JSON=".claude-plugin/marketplace.json"

usage() {
  echo "Usage: $0 <plugin-name> <patch|minor|major>"
  echo ""
  echo "Available plugins:"
  for dir in plugins/*/; do
    name=$(basename "$dir")
    desc=$(jq -r '.description' "$dir/.claude-plugin/plugin.json" 2>/dev/null || echo "(no description)")
    echo "  $name — $desc"
  done
  exit 1
}

# Validate args
[[ -z "$PLUGIN" || -z "$BUMP" ]] && usage
[[ -d "$PLUGIN_DIR" ]] || { echo "Error: plugin '$PLUGIN' not found"; usage; }
[[ "$BUMP" == "patch" || "$BUMP" == "minor" || "$BUMP" == "major" ]] || {
  echo "Error: bump type must be patch, minor, or major (got '$BUMP')"
  usage
}

# Check prerequisites
if ! command -v jq &>/dev/null; then
  echo "Error: jq is required but not installed. Install it and try again."
  exit 1
fi

# Check clean working tree
if ! git diff --exit-code --quiet || ! git diff --cached --exit-code --quiet; then
  echo "Error: working tree is dirty. Commit or stash changes before releasing."
  exit 1
fi

# Verify plugin exists in marketplace.json
if ! jq -e --arg name "$PLUGIN" '.plugins[] | select(.name == $name)' "$MARKETPLACE_JSON" > /dev/null; then
  echo "Error: plugin '$PLUGIN' not found in $MARKETPLACE_JSON"
  exit 1
fi

# Read current version
CURRENT=$(jq -r --arg name "$PLUGIN" '.plugins[] | select(.name == $name) | .version' "$MARKETPLACE_JSON")
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"

# Compute new version
case "$BUMP" in
  major) MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0 ;;
  minor) MINOR=$((MINOR + 1)); PATCH=0 ;;
  patch) PATCH=$((PATCH + 1)) ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"
TAG="$PLUGIN/v$NEW_VERSION"

echo "Releasing $PLUGIN: $CURRENT → $NEW_VERSION"

# Check tag does not already exist
if [[ -n "$(git tag -l "$TAG")" ]]; then
  echo "Error: tag '$TAG' already exists. Was this version already released?"
  exit 1
fi

echo "All checks passed. Writing version $NEW_VERSION..."

jq --arg name "$PLUGIN" --arg version "$NEW_VERSION" \
  '.plugins = [.plugins[] | if .name == $name then .version = $version else . end]' \
  "$MARKETPLACE_JSON" > "_marketplace.json"
mv "_marketplace.json" "$MARKETPLACE_JSON"

git add "$MARKETPLACE_JSON"
git commit -m "chore: release $PLUGIN v$NEW_VERSION"
git tag "$TAG"
git push
git push --follow-tags
