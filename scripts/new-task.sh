#!/bin/bash
# Usage: ./scripts/new-task.sh "add-cache-invalidation"
NAME=$1

if [ -z "$NAME" ]; then
  echo "Usage: ./scripts/new-task.sh 'task-name-kebab-case'"
  exit 1
fi

# Find next number
LAST_NUM=$(ls tasks/*.md 2>/dev/null | grep -E '[0-9]{3}' | sort | tail -n 1 | awk -F'/' '{print $2}' | cut -c 1-3)
if [ -z "$LAST_NUM" ]; then LAST_NUM="000"; fi
NEXT_NUM=$(printf "%03d" $((10#$LAST_NUM + 1)))

FILENAME="tasks/${NEXT_NUM}-${NAME}.md"
cp tasks/TEMPLATE.md "$FILENAME"

echo "🚀 Created: $FILENAME"
echo "Next: Open this file and have the Planner fill it out."
