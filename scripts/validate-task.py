import re
import sys
from pathlib import Path


def parse_structure(file_path):
    """Extracts the header structure (##, ###) from a markdown file."""
    with open(file_path, "r") as f:
        lines = f.readlines()

    # We only care about headers that aren't instructional/examples (usually fixed names)
    # This regex captures "## Planner", "### Requirements", etc.
    headers = [line.strip() for line in lines if line.startswith("#")]

    # Filter out headers that look like user-fillable slots if any (e.g., "# Phase [1]")
    # For now, we assume the template headers are the mandatory schema.
    return set(headers)


def validate(task_file, template_file="tasks/TEMPLATE.md"):
    print(f"🔍 Validating {task_file} against {template_file}...")

    required_headers = parse_structure(template_file)
    task_headers = parse_structure(task_file)

    # Check 1: Structure Match
    missing = required_headers - task_headers
    if missing:
        print("❌ Validation Failed. Missing sections:")
        for m in missing:
            print(f"   - {m}")
        return False

    # Check 2: Code Block Existence (Heuristic)
    with open(task_file, "r") as f:
        content = f.read()

    # We expect at least 2 code blocks (one for before/after or implementation)
    code_blocks = len(re.findall(r"```", content)) / 2
    if code_blocks < 1:
        print(
            f"⚠️  Warning: Only {int(code_blocks)} code blocks found. Plans usually need code snippets."
        )
        # We don't fail here, just warn, as some tasks might be pure config.

    print("✅ Task validates against Template schema.")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate_task.py <task_file>")
        sys.exit(1)

    success = validate(sys.argv[1])
    sys.exit(0 if success else 1)
