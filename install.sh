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

# --- MCP server registration ---
PLUGIN_ROOT="$(cd "$PLUGIN_DIR" && pwd)"
MANIFEST="$PLUGIN_DIR/.claude-plugin/plugin.json"
MCP_SERVERS=$(jq -r '.mcpServers // empty | keys[]' "$MANIFEST" 2>/dev/null || true)

if [[ -n "$MCP_SERVERS" ]]; then
  SETTINGS_FILE="${CLAUDE_DIR}/settings.json"
  [[ -f "$SETTINGS_FILE" ]] || echo '{}' > "$SETTINGS_FILE"

  for server_name in $MCP_SERVERS; do
    raw_cmd=$(jq -r ".mcpServers[\"$server_name\"].command" "$MANIFEST")
    resolved_cmd="${raw_cmd//\$\{CLAUDE_PLUGIN_ROOT\}/$PLUGIN_ROOT}"

    # Prompt for API key if this is the semantic scholar server
    S2_KEY=""
    if [[ "$server_name" == "mcp-semantic-scholar" ]]; then
      echo ""
      echo "  Semantic Scholar requires an API key (free)."
      echo "  Get one at: https://www.semanticscholar.org/product/api#api-key-form"
      echo ""
      read -rp "  Enter your S2 API key (or press Enter to skip): " S2_KEY
      if [[ -z "$S2_KEY" ]]; then
        echo ""
        echo "  No key entered. The MCP server will be registered but will not"
        echo "  work until you add your key. See instructions below."
      fi
    fi

    # Register MCP server with env block
    jq --arg name "$server_name" --arg cmd "$resolved_cmd" --arg key "${S2_KEY:-}" \
      '.mcpServers[$name] = {"command": $cmd, "args": [], "env": {"S2_API_KEY": $key}}' \
      "$SETTINGS_FILE" > "${SETTINGS_FILE}.tmp" && mv "${SETTINGS_FILE}.tmp" "$SETTINGS_FILE"

    echo "  registered MCP server: $server_name -> $resolved_cmd"
  done

  echo ""
  echo "MCP server registered in $SETTINGS_FILE"
  if [[ -z "$S2_KEY" ]]; then
    echo ""
    echo "  To add your API key later, edit $SETTINGS_FILE:"
    echo '    "mcpServers": { "mcp-semantic-scholar": { "env": { "S2_API_KEY": "YOUR_KEY" } } }'
  fi
fi

# --- Optional dependency hints ---
MARKETPLACE=".claude-plugin/marketplace.json"
OPT_DEPS=$(jq -r --arg name "$PLUGIN" '.plugins[] | select(.name == $name) | .optionalDependencies // [] | .[].name' "$MARKETPLACE" 2>/dev/null || true)

if [[ -n "$OPT_DEPS" ]]; then
  SETTINGS_FILE="${CLAUDE_DIR}/settings.json"
  for dep in $OPT_DEPS; do
    dep_desc=$(jq -r --arg name "$PLUGIN" --arg dep "$dep" '.plugins[] | select(.name == $name) | .optionalDependencies[] | select(.name == $dep) | .description' "$MARKETPLACE")
    # Check if the dependency is installed as an MCP server or as a plugin
    dep_installed=false
    if [[ -f "$SETTINGS_FILE" ]] && jq -e ".mcpServers[\"$dep\"]" "$SETTINGS_FILE" >/dev/null 2>&1; then
      dep_installed=true
    elif [[ -d "plugins/$dep" ]]; then
      # Plugin exists in marketplace but may not be installed
      if [[ -f "$SETTINGS_FILE" ]] && jq -e ".mcpServers[\"$dep\"]" "$SETTINGS_FILE" >/dev/null 2>&1; then
        dep_installed=true
      fi
    fi

    if [[ "$dep_installed" == "false" ]]; then
      echo ""
      echo "  Optional: install '$dep' for enhanced functionality."
      [[ -n "$dep_desc" ]] && echo "    $dep_desc"
      if [[ -d "plugins/$dep" ]]; then
        echo "    Run: ./install.sh $dep --symlink"
      fi
    fi
  done
fi

echo ""
echo "Done. Verify with:"
echo "  ls $CLAUDE_DIR/agents/"
echo "  ls $CLAUDE_DIR/skills/"
