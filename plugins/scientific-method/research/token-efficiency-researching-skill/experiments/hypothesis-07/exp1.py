#!/usr/bin/env python3
"""
Experiment 2 for Hypothesis 07: Count actual tokens in split vs. merged skill instruction sets.

Reads the three skill files for Steps C (designing-experiments), D (running-experiments),
and E (drawing-conclusions), counts tokens using tiktoken (cl100k_base), simulates both
split and merged architectures for N=4 hypotheses, and reports savings.
"""

import sys

try:
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    def count_tokens(text):
        return len(enc.encode(text))
    token_method = "tiktoken cl100k_base"
except ImportError:
    def count_tokens(text):
        return len(text) // 4
    token_method = "character-count proxy (len/4)"
    print(f"NOTE: tiktoken not available; using proxy: {token_method}")

SKILL_DIR = "/home/fence/.claude-equine/plugins/marketplaces/pipemind-marketplace/plugins/scientific-method/skills"
HYPOTHESIS_FILE = "/home/fence/src/pipemind/claude-agentic/plugins/scientific-method/token-efficiency-researching-skill/hypothesis-07.md"

skill_paths = {
    "designing-experiments (Step C)": f"{SKILL_DIR}/designing-experiments/SKILL.md",
    "running-experiments (Step D)": f"{SKILL_DIR}/running-experiments/SKILL.md",
    "drawing-conclusions (Step E)": f"{SKILL_DIR}/drawing-conclusions/SKILL.md",
}

# Read skill files
skill_contents = {}
skill_tokens = {}
for name, path in skill_paths.items():
    with open(path, "r") as f:
        content = f.read()
    skill_contents[name] = content
    skill_tokens[name] = count_tokens(content)

# Read hypothesis file
with open(HYPOTHESIS_FILE, "r") as f:
    hypothesis_content = f.read()
hypothesis_tokens = count_tokens(hypothesis_content)

# Merged instruction set: concatenate with minimal section headers
merged_content = "\n\n---\n\n".join([
    f"# Step C: Designing Experiments\n\n{skill_contents['designing-experiments (Step C)']}",
    f"# Step D: Running Experiments\n\n{skill_contents['running-experiments (Step D)']}",
    f"# Step E: Drawing Conclusions\n\n{skill_contents['drawing-conclusions (Step E)']}",
])
merged_tokens = count_tokens(merged_content)

N = 4  # number of hypotheses

# Architecture A: split — 3N agents, each loads one skill + reads hypothesis file
split_skill_tokens = sum(skill_tokens.values()) * N  # each step's skill loaded N times
split_hypothesis_reads = hypothesis_tokens * 3 * N   # each of 3N agents reads hypothesis
split_total = split_skill_tokens + split_hypothesis_reads

# Architecture B: merged — N agents, each loads merged skill + reads hypothesis file once
merged_skill_tokens_total = merged_tokens * N
merged_hypothesis_reads = hypothesis_tokens * N  # each of N agents reads hypothesis once
merged_total = merged_skill_tokens_total + merged_hypothesis_reads

# Savings
absolute_savings = split_total - merged_total
pct_savings = (absolute_savings / split_total) * 100 if split_total > 0 else 0

# Skill-only savings (ignoring hypothesis re-reads)
skill_only_split = split_skill_tokens
skill_only_merged = merged_skill_tokens_total
skill_savings_abs = skill_only_split - skill_only_merged
skill_savings_pct = (skill_savings_abs / skill_only_split) * 100 if skill_only_split > 0 else 0

# Deduplication in merged set
naive_concat_tokens = sum(skill_tokens.values())
actual_merged_single = merged_tokens  # merged content for 1 agent
dedup_pct = (1 - actual_merged_single / naive_concat_tokens) * 100 if naive_concat_tokens > 0 else 0

print(f"\n{'='*60}")
print(f"Token Counting Method: {token_method}")
print(f"{'='*60}")
print(f"\n--- Individual Skill File Token Counts ---")
for name, tokens in skill_tokens.items():
    print(f"  {name}: {tokens:,} tokens")
print(f"  Sum of three skills: {sum(skill_tokens.values()):,} tokens")
print(f"  Merged (concatenated with headers): {merged_tokens:,} tokens")
print(f"  Deduplication in merge: {dedup_pct:.1f}%")

print(f"\n--- Hypothesis File ---")
print(f"  hypothesis-07.md: {hypothesis_tokens:,} tokens")

print(f"\n--- Architecture Comparison (N={N} hypotheses) ---")
print(f"  SPLIT (3N={3*N} agents):")
print(f"    Skill instruction loads: {split_skill_tokens:,} tokens ({3*N} loads)")
print(f"    Hypothesis re-reads:     {split_hypothesis_reads:,} tokens ({3*N} reads)")
print(f"    Total overhead:          {split_total:,} tokens")
print(f"\n  MERGED (N={N} agents):")
print(f"    Skill instruction loads: {merged_skill_tokens_total:,} tokens ({N} loads)")
print(f"    Hypothesis re-reads:     {merged_hypothesis_reads:,} tokens ({N} reads)")
print(f"    Total overhead:          {merged_total:,} tokens")

print(f"\n--- Savings ---")
print(f"  Absolute reduction:  {absolute_savings:,} tokens")
print(f"  Percentage savings:  {pct_savings:.1f}%")
print(f"  Skill-only savings:  {skill_savings_abs:,} tokens ({skill_savings_pct:.1f}%)")

print(f"\n--- Hypothesis ---")
if pct_savings >= 30:
    verdict = "CONFIRMED (savings >= 30%)"
elif pct_savings >= 20:
    verdict = "CONFIRMED but below ~40% target"
else:
    verdict = "REFUTED (savings < 20%)"
print(f"  Verdict: {verdict}")
print(f"  Target was ~40% reduction; measured: {pct_savings:.1f}%")
print(f"{'='*60}\n")
