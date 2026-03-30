#!/usr/bin/env python3
"""
Experiment 1: Token Count Audit of All Eight SKILL.md Files

Uses a character-based approximation for token counts (chars / 4 ~ tokens).
This is a well-known rule-of-thumb for GPT-style tokenizers.

For each SKILL.md, we count:
  (a) total tokens
  (b) frontmatter tokens (YAML between --- delimiters)
  (c) type-specific section tokens (sections that only apply to a specific experiment type)
  (d) universal workflow tokens (sections applicable regardless of experiment type)

For the representative invocation (running-experiments, code-type experiment):
  - Frontmatter is skipped overhead
  - math-proof, evidence-gathering, data-analysis, logical-deduction sections are skipped overhead
  - argument-parsing/argument-hint sections are skipped overhead

We then:
  1. Report per-file reduction percentage
  2. Compute aggregate reduction for a minimum 4-hypothesis run
"""

import os
import re

SKILLS_DIR = "/home/fence/.claude-equine/plugins/marketplaces/pipemind-marketplace/plugins/scientific-method/skills"

# Approximate tokens from character count
def approx_tokens(text):
    return len(text) / 4.0

def extract_frontmatter(content):
    """Return (frontmatter_text, body_text) split on YAML --- delimiters."""
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            fm = content[:end+3]
            body = content[end+3:]
            return fm, body
    return "", content

def split_into_sections(body):
    """
    Split markdown body into a dict mapping section header -> section content.
    Sections are delimited by lines starting with ### or #### (level 3+).
    Returns list of (header, content) tuples preserving order.
    """
    lines = body.split("\n")
    sections = []
    current_header = "__preamble__"
    current_lines = []
    for line in lines:
        if re.match(r'^#{2,}\s+', line):
            sections.append((current_header, "\n".join(current_lines)))
            current_header = line.strip()
            current_lines = []
        else:
            current_lines.append(line)
    sections.append((current_header, "\n".join(current_lines)))
    return sections

# Keywords that mark type-specific sections (i.e., instructions for non-code experiment types)
# These are the sections that a code-experiment invocation does NOT need
TYPE_SPECIFIC_KEYWORDS = [
    "math-proof",
    "math proof",
    "evidence-gathering",
    "evidence gathering",
    "data-analysis",
    "data analysis",
    "logical-deduction",
    "logical deduction",
]

# Keywords that mark argument-parsing sections (overhead even for code invocations)
ARG_SECTION_KEYWORDS = [
    "## arguments",
    "## argument",
]

def classify_sections(sections, skill_name):
    """
    For each section, classify as: frontmatter | type_specific | universal
    Returns dict with 'universal', 'type_specific', 'frontmatter' token totals.
    """
    universal_tokens = 0
    type_specific_tokens = 0

    for header, content in sections:
        section_text = header + "\n" + content
        n_tokens = approx_tokens(section_text)

        header_lower = header.lower()

        # Check if this section is type-specific (only relevant for non-code experiment types)
        is_type_specific = any(kw in header_lower for kw in TYPE_SPECIFIC_KEYWORDS)

        # Also check section content for type-specific markers (e.g., a section discussing math-proof)
        # We check the first 200 chars of content after header
        content_snippet = content[:300].lower()
        if not is_type_specific:
            is_type_specific = any(kw in content_snippet for kw in TYPE_SPECIFIC_KEYWORDS)
            # But verify: if a section mentions multiple types (like "Experiment types" enum),
            # it's universal (universal reference list)
            if is_type_specific:
                # If section mentions >= 3 experiment types, it's a universal enum, not type-specific
                count_types = sum(1 for kw in TYPE_SPECIFIC_KEYWORDS if kw in content_snippet)
                if count_types >= 3:
                    is_type_specific = False

        # Argument sections are also skippable (overhead)
        is_arg_section = any(kw in header_lower for kw in ARG_SECTION_KEYWORDS)

        if is_arg_section or is_type_specific:
            type_specific_tokens += n_tokens
        else:
            universal_tokens += n_tokens

    return universal_tokens, type_specific_tokens


def audit_skill(skill_name):
    skill_path = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
    if not os.path.exists(skill_path):
        return None

    with open(skill_path, "r") as f:
        content = f.read()

    total_tokens = approx_tokens(content)

    frontmatter, body = extract_frontmatter(content)
    fm_tokens = approx_tokens(frontmatter)

    sections = split_into_sections(body)
    universal_tokens, type_specific_tokens = classify_sections(sections, skill_name)

    # Skippable = frontmatter + type-specific/arg sections
    skippable_tokens = fm_tokens + type_specific_tokens
    skippable_pct = (skippable_tokens / total_tokens * 100) if total_tokens > 0 else 0

    return {
        "skill": skill_name,
        "total_tokens": total_tokens,
        "frontmatter_tokens": fm_tokens,
        "type_specific_tokens": type_specific_tokens,
        "universal_tokens": universal_tokens,
        "skippable_tokens": skippable_tokens,
        "skippable_pct": skippable_pct,
        "total_chars": len(content),
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

    print("=" * 80)
    print("TOKEN COUNT AUDIT OF ALL EIGHT SKILL.md FILES")
    print("Method: character-based approximation (chars / 4 ≈ tokens)")
    print("=" * 80)
    print()

    results = []
    for skill in skills:
        r = audit_skill(skill)
        if r:
            results.append(r)

    # Print per-file breakdown
    print(f"{'Skill':<30} {'Total':>8} {'Frontmatter':>12} {'Type-Specific':>14} {'Universal':>10} {'Skip%':>8}")
    print("-" * 90)
    for r in results:
        print(f"{r['skill']:<30} {r['total_tokens']:>8.0f} {r['frontmatter_tokens']:>12.0f} "
              f"{r['type_specific_tokens']:>14.0f} {r['universal_tokens']:>10.0f} "
              f"{r['skippable_pct']:>7.1f}%")

    print()
    print("=" * 80)
    print("REPRESENTATIVE INVOCATION ANALYSIS")
    print("Scenario: running-experiments called for a single code-type experiment")
    print("Skills loaded: all 8 (orchestrator + 5 hypothesis-level skills + 2 support)")
    print()

    # In the scientific method loop, which skills are loaded per hypothesis?
    # A typical 4-hypothesis run loads:
    #   - researching (orchestrator): 1x
    #   - refining-problem: 1x
    #   - generating-hypotheses: 1x
    #   - refining-hypothesis: 4x (one per hypothesis)
    #   - designing-experiments: 4x
    #   - running-experiments: 4x
    #   - drawing-conclusions: 4x
    #   - researching-literature: ~12x (3 per hypothesis refine call)
    #
    # For simplicity, we analyze the per-invocation overhead for running-experiments
    # (most relevant to the hypothesis), then aggregate across the minimum 4-hypothesis run.

    # Per-skill aggregates for a 4-hypothesis run (minimum per problem.md)
    # "5 skills that are invoked per hypothesis" = refining-hypothesis, designing-experiments,
    # running-experiments, drawing-conclusions, researching-literature
    per_hypothesis_skills = {
        "refining-hypothesis",
        "designing-experiments",
        "running-experiments",
        "drawing-conclusions",
        "researching-literature",
    }

    total_run_tokens = 0
    total_run_skippable = 0

    print(f"{'Skill':<30} {'×':>3} {'Total Load':>12} {'Skippable Load':>15} {'Skip%':>8}")
    print("-" * 75)

    # Orchestrator-level skills (loaded once)
    once_skills = ["researching", "refining-problem", "generating-hypotheses"]
    for skill_name in once_skills:
        r = next((x for x in results if x["skill"] == skill_name), None)
        if r:
            load_tokens = r["total_tokens"] * 1
            skip_tokens = r["skippable_tokens"] * 1
            total_run_tokens += load_tokens
            total_run_skippable += skip_tokens
            print(f"{skill_name:<30} {'×1':>3} {load_tokens:>12.0f} {skip_tokens:>15.0f} "
                  f"{(skip_tokens/load_tokens*100) if load_tokens else 0:>7.1f}%")

    # Per-hypothesis skills (loaded 4x for a 4-hypothesis run)
    # Note: researching-literature is called ~3x per hypothesis in refining-hypothesis
    # but each call loads the SKILL.md once
    per_hyp_count = {
        "refining-hypothesis": 4,
        "designing-experiments": 4,
        "running-experiments": 4,
        "drawing-conclusions": 4,
        "researching-literature": 12,  # ~3 searches per hypothesis
    }
    for skill_name, count in per_hyp_count.items():
        r = next((x for x in results if x["skill"] == skill_name), None)
        if r:
            load_tokens = r["total_tokens"] * count
            skip_tokens = r["skippable_tokens"] * count
            total_run_tokens += load_tokens
            total_run_skippable += skip_tokens
            print(f"{skill_name:<30} {f'×{count}':>3} {load_tokens:>12.0f} {skip_tokens:>15.0f} "
                  f"{(skip_tokens/load_tokens*100) if load_tokens else 0:>7.1f}%")

    print("-" * 75)
    total_skip_pct = (total_run_skippable / total_run_tokens * 100) if total_run_tokens > 0 else 0
    print(f"{'TOTAL (4-hypothesis run)':<30} {'':>3} {total_run_tokens:>12.0f} {total_run_skippable:>15.0f} "
          f"{total_skip_pct:>7.1f}%")

    print()
    print("=" * 80)
    print("HYPOTHESIS VERDICT")
    print(f"Aggregate skippable content: {total_skip_pct:.1f}%")
    print(f"Hypothesis claims 60-70% skippable.")
    if total_skip_pct >= 60:
        print(f"RESULT: CONFIRMS the hypothesis ({total_skip_pct:.1f}% >= 60%)")
    else:
        print(f"RESULT: REFUTES the hypothesis ({total_skip_pct:.1f}% < 60%)")

    print()
    print("=" * 80)
    print("RUNNING-EXPERIMENTS DETAIL (most type-branching skill)")
    re_result = next((x for x in results if x["skill"] == "running-experiments"), None)
    if re_result:
        print(f"  Total chars: {re_result['total_chars']}")
        print(f"  Total approx tokens: {re_result['total_tokens']:.0f}")
        print(f"  Frontmatter tokens: {re_result['frontmatter_tokens']:.0f}")
        print(f"  Type-specific section tokens: {re_result['type_specific_tokens']:.0f}")
        print(f"  Universal workflow tokens: {re_result['universal_tokens']:.0f}")
        print(f"  Skippable for code-experiment invocation: {re_result['skippable_pct']:.1f}%")

    print()
    print("NOTE: Token counts are approximate (chars/4). Actual subword tokenizer")
    print("counts may vary ±10-15%, but the proportional skippable percentages are")
    print("robust to this variation since the approximation applies uniformly.")


if __name__ == "__main__":
    main()
