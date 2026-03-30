#!/usr/bin/env python3
"""
Experiment 1 (corrected analysis): Token Count Audit with Bold-Header Awareness

The first pass (exp1.py) only split at markdown heading levels (##, ###, ####).
However, running-experiments uses bold-text pseudo-headers like:
  **Code experiments (type: code):**
  **Math proof experiments (type: math-proof):**
  etc.

These are embedded inside the ### Step 1 markdown section and were counted as
a single "universal" block. This script fixes that by also detecting and
classifying bold-text pseudo-headers within sections.

This gives a corrected per-skill token audit and updated hypothesis verdict.
"""

import os
import re

SKILLS_DIR = "/home/fence/.claude-equine/plugins/marketplaces/pipemind-marketplace/plugins/scientific-method/skills"

def approx_tokens(text):
    return len(text) / 4.0

def extract_frontmatter(content):
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            fm = content[:end+3]
            body = content[end+3:]
            return fm, body
    return "", content

# Experiment type keywords — content about these types is skippable
# for a code-type invocation
NON_CODE_TYPE_KEYWORDS = [
    "math-proof",
    "math proof",
    "evidence-gathering",
    "evidence gathering",
    "data-analysis",
    "data analysis",
    "logical-deduction",
    "logical deduction",
]

# Argument section keywords
ARG_SECTION_KEYWORDS = ["## arguments", "## argument"]


def split_into_logical_blocks(body):
    """
    Split body into logical blocks at BOTH markdown headings (##, ###, ####)
    AND bold-text pseudo-headers (**...**:).

    Returns list of (kind, header, content) tuples where kind is 'heading' or 'bold'.
    """
    lines = body.split("\n")
    blocks = []
    current_header = "__preamble__"
    current_kind = "heading"
    current_lines = []

    for line in lines:
        # Markdown heading?
        if re.match(r'^#{2,}\s+', line):
            blocks.append((current_kind, current_header, "\n".join(current_lines)))
            current_header = line.strip()
            current_kind = "heading"
            current_lines = []
        # Bold pseudo-header? (line like **Something experiments (type: foo):**)
        elif re.match(r'^\*\*[^*]+\*\*[:.]?\s*$', line):
            blocks.append((current_kind, current_header, "\n".join(current_lines)))
            current_header = line.strip()
            current_kind = "bold"
            current_lines = []
        else:
            current_lines.append(line)

    blocks.append((current_kind, current_header, "\n".join(current_lines)))
    return blocks


def is_type_specific_block(header, content):
    """
    Returns True if this block is only relevant for non-code experiment types.
    """
    header_lower = header.lower()
    content_snippet = content[:300].lower()

    # Check for non-code type keywords in the header
    if any(kw in header_lower for kw in NON_CODE_TYPE_KEYWORDS):
        return True

    # Check first 300 chars of content
    if any(kw in content_snippet for kw in NON_CODE_TYPE_KEYWORDS):
        # But if many types are mentioned (enum/list context), it's universal
        count_types = sum(1 for kw in NON_CODE_TYPE_KEYWORDS if kw in content_snippet)
        if count_types >= 3:
            return False
        return True

    return False


def is_arg_section(header):
    header_lower = header.lower()
    return any(kw in header_lower for kw in ARG_SECTION_KEYWORDS)


def audit_skill(skill_name):
    skill_path = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
    if not os.path.exists(skill_path):
        return None

    with open(skill_path, "r") as f:
        content = f.read()

    total_tokens = approx_tokens(content)
    total_chars = len(content)

    frontmatter, body = extract_frontmatter(content)
    fm_tokens = approx_tokens(frontmatter)

    blocks = split_into_logical_blocks(body)

    universal_tokens = 0
    type_specific_tokens = 0

    for kind, header, content_block in blocks:
        block_text = header + "\n" + content_block
        n_tokens = approx_tokens(block_text)

        if is_arg_section(header):
            type_specific_tokens += n_tokens
        elif is_type_specific_block(header, content_block):
            type_specific_tokens += n_tokens
        else:
            universal_tokens += n_tokens

    skippable_tokens = fm_tokens + type_specific_tokens
    skippable_pct = (skippable_tokens / total_tokens * 100) if total_tokens > 0 else 0

    return {
        "skill": skill_name,
        "total_tokens": total_tokens,
        "total_chars": total_chars,
        "frontmatter_tokens": fm_tokens,
        "type_specific_tokens": type_specific_tokens,
        "universal_tokens": universal_tokens,
        "skippable_tokens": skippable_tokens,
        "skippable_pct": skippable_pct,
    }


def main():
    skills = [
        "designing-experiments",
        "drawing-conclusions",
        "generating-hypotheses",
        "refining-hypothesis",
        "refining-problem",
        "researching",
        "researching-literature",
        "running-experiments",
    ]

    print("=" * 90)
    print("TOKEN COUNT AUDIT (CORRECTED): BOLD-HEADER-AWARE SECTION CLASSIFICATION")
    print("Method: chars/4 approximation; type-specific = non-code experiment type blocks")
    print("Skippable for code-type invocation = frontmatter + type-specific + arg sections")
    print("=" * 90)
    print()

    results = []
    for skill in skills:
        r = audit_skill(skill)
        if r:
            results.append(r)

    # Per-file table
    print(f"{'Skill':<30} {'Total tok':>10} {'Frontmatter':>12} {'Type-Spec':>10} {'Universal':>10} {'Skip%':>8}")
    print("-" * 85)
    for r in results:
        print(f"{r['skill']:<30} {r['total_tokens']:>10.0f} {r['frontmatter_tokens']:>12.0f} "
              f"{r['type_specific_tokens']:>10.0f} {r['universal_tokens']:>10.0f} "
              f"{r['skippable_pct']:>7.1f}%")

    print()

    # 4-hypothesis run aggregation
    # Skills and their invocation counts for a minimum 4-hypothesis run:
    #   researching (orchestrator): ×1
    #   refining-problem: ×1
    #   generating-hypotheses: ×1
    #   refining-hypothesis: ×4
    #   designing-experiments: ×4
    #   running-experiments: ×4
    #   drawing-conclusions: ×4
    #   researching-literature: ×12 (3 searches per hypothesis × 4 hypotheses)
    invocation_counts = {
        "researching": 1,
        "refining-problem": 1,
        "generating-hypotheses": 1,
        "refining-hypothesis": 4,
        "designing-experiments": 4,
        "running-experiments": 4,
        "drawing-conclusions": 4,
        "researching-literature": 12,
    }

    print("=" * 90)
    print("AGGREGATE: 4-HYPOTHESIS RUN (minimum per problem.md baseline)")
    print()
    print(f"{'Skill':<30} {'×N':>4} {'Total Loaded':>14} {'Skippable':>12} {'Skip%':>8}")
    print("-" * 75)

    total_run_tokens = 0
    total_run_skippable = 0

    for skill_name, count in invocation_counts.items():
        r = next((x for x in results if x["skill"] == skill_name), None)
        if r:
            load = r["total_tokens"] * count
            skip = r["skippable_tokens"] * count
            total_run_tokens += load
            total_run_skippable += skip
            print(f"{skill_name:<30} {f'×{count}':>4} {load:>14.0f} {skip:>12.0f} "
                  f"{r['skippable_pct']:>7.1f}%")

    print("-" * 75)
    total_skip_pct = (total_run_skippable / total_run_tokens * 100) if total_run_tokens > 0 else 0
    print(f"{'TOTAL':<30} {'':>4} {total_run_tokens:>14.0f} {total_run_skippable:>12.0f} "
          f"{total_skip_pct:>7.1f}%")

    print()
    print("=" * 90)
    print("RUNNING-EXPERIMENTS DETAIL (key skill for hypothesis)")
    re_result = next((x for x in results if x["skill"] == "running-experiments"), None)
    if re_result:
        # Do detailed block-by-block analysis
        skill_path = os.path.join(SKILLS_DIR, "running-experiments", "SKILL.md")
        with open(skill_path) as f:
            content = f.read()
        frontmatter, body = extract_frontmatter(content)
        blocks = split_into_logical_blocks(body)
        print()
        print(f"  {'Header':<60} {'Tokens':>8} {'Classification':<20}")
        print(f"  {'-'*90}")
        fm_tok = approx_tokens(frontmatter)
        print(f"  {'[FRONTMATTER]':<60} {fm_tok:>8.0f} {'skippable':<20}")
        for kind, header, content_block in blocks:
            block_text = header + "\n" + content_block
            n_tok = approx_tokens(block_text)
            if n_tok < 2:
                continue
            if is_arg_section(header):
                classification = "skippable (args)"
            elif is_type_specific_block(header, content_block):
                classification = "skippable (type-specific)"
            else:
                classification = "universal"
            h_display = header[:58] if len(header) <= 58 else header[:55] + "..."
            print(f"  {h_display:<60} {n_tok:>8.0f} {classification:<20}")

        print()
        print(f"  Total tokens: {re_result['total_tokens']:.0f}")
        print(f"  Skippable (frontmatter + type-specific): {re_result['skippable_tokens']:.0f}")
        print(f"  Skip percentage: {re_result['skippable_pct']:.1f}%")

    print()
    print("=" * 90)
    print("VERDICT")
    print(f"  Aggregate skippable across 4-hypothesis run: {total_skip_pct:.1f}%")
    print(f"  Hypothesis claims 60-70% skippable.")
    print()
    if total_skip_pct >= 60:
        print(f"  -> CONFIRMS the hypothesis ({total_skip_pct:.1f}% >= 60%)")
    elif total_skip_pct >= 50:
        print(f"  -> INCONCLUSIVE ({total_skip_pct:.1f}%: below 60% but within measurement uncertainty)")
    else:
        print(f"  -> REFUTES the hypothesis ({total_skip_pct:.1f}% << 60%)")

    print()
    print("NOTE: Chars/4 approximation has ~10-15% uncertainty. The gap between")
    print(f"the measured {total_skip_pct:.1f}% and the claimed 60% is too large to")
    print("be explained by tokenizer differences alone.")


if __name__ == "__main__":
    main()
