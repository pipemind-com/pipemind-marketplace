#!/usr/bin/env bash
# E2E smoke test for the scientific-method plugin.
# Runs a headless /researching session on a small-scope problem,
# then validates the output with validate-research.sh.
#
# Usage: ./e2e-smoke.sh
#
# Results are written to tests/results/<timestamp>-<slug>/
# and are gitignored.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"
RESULTS_DIR="$SCRIPT_DIR/results"

SLUG="gauss-sum-formula"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
RUN_DIR="$RESULTS_DIR/$TIMESTAMP-$SLUG"

mkdir -p "$RUN_DIR"

printf "\033[1mE2E Smoke Test: scientific-method\033[0m\n"
printf "Problem: %s\n" "$SLUG"
printf "Output:  %s\n\n" "$RUN_DIR"

# Sync dev skills into ALL marketplace cache versions so the marketplace-installed
# version picks up our changes (marketplace takes precedence over symlinks).
CACHE_DIR="$HOME/.claude/plugins/cache/pipemind-marketplace/scientific-method"
if [[ -d "$CACHE_DIR" ]]; then
  printf "Syncing dev skills into marketplace cache...\n"
  for version_dir in "$CACHE_DIR"/*/; do
    version_skills="$version_dir/skills"
    [[ -d "$version_skills" ]] || continue
    ver=$(basename "$version_dir")
    for skill_dir in "$PLUGIN_DIR/skills"/*/; do
      name=$(basename "$skill_dir")
      if [[ -d "$version_skills/$name" ]]; then
        cp -r "$skill_dir"/* "$version_skills/$name/"
        printf "  [%s] synced %s\n" "$ver" "$name"
      fi
    done
  done
  printf "\n"
fi

# Run the full research loop headless.
# The problem is small-scope and provable in 1 iteration via math-proof + code.
printf "Running /researching (headless)...\n"
printf "This will take several minutes.\n\n"

PROBLEM_DIR="$RUN_DIR/$SLUG"
mkdir -p "$PROBLEM_DIR/references"
cd "$PROBLEM_DIR"

SKILL_FILE="$PLUGIN_DIR/skills/researching/SKILL.md"
DESCRIPTION="Prove or disprove: the sum of the first N natural numbers equals N*(N+1)/2. Test with both a formal proof and a code experiment."

claude -p --dangerously-skip-permissions --max-turns 200 \
  "Read the skill file at $SKILL_FILE and follow its instructions EXACTLY. Do NOT ask any questions — the entire pipeline is fully autonomous. Arguments: slug=$SLUG, initial-description='$DESCRIPTION'. All sub-skills are in sibling directories under $PLUGIN_DIR/skills/." \
  2>&1 | tee "$RUN_DIR/claude-output.log"

EXIT_CODE=${PIPESTATUS[0]}

printf "\n\033[1mClaude exit code: %d\033[0m\n\n" "$EXIT_CODE"

if [[ $EXIT_CODE -ne 0 ]]; then
  printf "\033[31mClaude exited with error. Check %s/claude-output.log\033[0m\n" "$RUN_DIR"
  exit 1
fi

# Check for AskUserQuestion failures in the log (would error in headless mode)
if rg -qi "AskUserQuestion" "$RUN_DIR/claude-output.log" 2>/dev/null; then
  printf "\033[31mWARNING: AskUserQuestion appeared in output — autonomy violation\033[0m\n"
fi

# Detect where research files landed (LLM may use CWD or create slug subdir)
if [[ -f "$PROBLEM_DIR/problem.md" ]]; then
  RESEARCH_DIR="$PROBLEM_DIR"
elif [[ -f "$PROBLEM_DIR/$SLUG/problem.md" ]]; then
  RESEARCH_DIR="$PROBLEM_DIR/$SLUG"
else
  printf "\033[31mNo problem.md found in expected locations\033[0m\n"
  printf "Checked: %s\n" "$PROBLEM_DIR"
  printf "Checked: %s\n" "$PROBLEM_DIR/$SLUG"
  ls -laR "$RUN_DIR"
  exit 1
fi

# Validate the research output
printf "\n\033[1mValidating output at: %s\033[0m\n" "$RESEARCH_DIR"
"$SCRIPT_DIR/validate-research.sh" "$RESEARCH_DIR"
