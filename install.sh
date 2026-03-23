#!/usr/bin/env bash
# Usage: ./install.sh <plugin-name> [--symlink]
# Example: ./install.sh spec-driven-development --symlink

set -euo pipefail

PLUGIN="${1:-}"
MODE="${2:-}"
CLAUDE_DIR="${CLAUDE_DIR:-$HOME/.claude}"

if [[ -z "$PLUGIN" ]]; then
  echo "Usage: $0 <plugin-name> [--symlink]"
  echo ""
  echo "Available plugins:"
  for dir in plugins/*/; do
    name=$(basename "$dir")
    desc=$(jq -r '.description' "$dir/.claude-plugin/plugin.json" 2>/dev/null || echo "(no description)")
    echo "  $name — $desc"
  done
  exit 1
fi

PLUGIN_DIR="plugins/$PLUGIN"

if [[ ! -f "$PLUGIN_DIR/.claude-plugin/plugin.json" ]]; then
  echo "Error: plugin '$PLUGIN' not found (missing $PLUGIN_DIR/.claude-plugin/plugin.json)"
  exit 1
fi

AGENTS_SRC="$(pwd)/$PLUGIN_DIR/agents"
SKILLS_SRC="$(pwd)/$PLUGIN_DIR/skills"

mkdir -p "$CLAUDE_DIR/agents" "$CLAUDE_DIR/skills"

if [[ "$MODE" == "--symlink" ]]; then
  echo "Installing $PLUGIN via symlinks into $CLAUDE_DIR ..."

  if [[ -d "$AGENTS_SRC" ]]; then
    for agent in "$AGENTS_SRC"/*.md; do
      [[ -e "$agent" ]] || continue
      ln -sf "$agent" "$CLAUDE_DIR/agents/$(basename "$agent")"
      echo "  linked agents/$(basename "$agent")"
    done
  fi

  if [[ -d "$SKILLS_SRC" ]]; then
    for skill_dir in "$SKILLS_SRC"/*/; do
      [[ -d "$skill_dir" ]] || continue
      name=$(basename "$skill_dir")
      rm -rf "$CLAUDE_DIR/skills/$name"
      ln -sf "$skill_dir" "$CLAUDE_DIR/skills/$name"
      echo "  linked skills/$name"
    done
  fi
else
  echo "Installing $PLUGIN (copy) into $CLAUDE_DIR ..."

  if [[ -d "$AGENTS_SRC" ]]; then
    cp -r "$AGENTS_SRC/." "$CLAUDE_DIR/agents/"
    echo "  copied agents/"
  fi

  if [[ -d "$SKILLS_SRC" ]]; then
    cp -r "$SKILLS_SRC/." "$CLAUDE_DIR/skills/"
    echo "  copied skills/"
  fi
fi

echo ""
echo "Done. Verify with:"
echo "  ls $CLAUDE_DIR/agents/"
echo "  ls $CLAUDE_DIR/skills/"
