"""
Experiment 2: Count Unique Sources in Existing Hypothesis Literature Sections

Analyzes hypothesis files in token-efficiency-researching-skill/ that have
## Literature sections, counting unique references per hypothesis, cross-
hypothesis overlap, and the redundancy ratio.

Also inspects the refining-hypothesis skill to confirm search invocation count.
"""

import re
from pathlib import Path
from collections import Counter, defaultdict

PROBLEM_DIR = Path("/home/fence/src/pipemind/claude-agentic/plugins/scientific-method/token-efficiency-researching-skill")
SKILL_PATH = Path("/home/fence/src/pipemind/claude-agentic/plugins/scientific-method/skills/refining-hypothesis/SKILL.md")

# ─── Step 1: Parse the refining-hypothesis skill ─────────────────────────────
with open(SKILL_PATH) as f:
    skill_text = f.read()

# Count parallel Task spawns (Step 2: 3 agents) + Step 2b: 1 agent = 4 total
task_count = skill_text.count("Run /researching-literature")
parallel_count_mention = "3 Task agents" in skill_text
step2b_mention = "Step 2b" in skill_text or "Gap assessment" in skill_text

print("=== refining-hypothesis skill analysis ===")
print(f"  Total '/researching-literature' invocations described: {task_count}")
print(f"  Mentions '3 Task agents in a single response': {parallel_count_mention}")
print(f"  Has Step 2b gap-fill pass: {step2b_mention}")
print(f"  Conclusion: {task_count} total literature searches per hypothesis (3 parallel + 1 gap-fill)")
print()

# ─── Step 2: Parse hypothesis files for REF citations ────────────────────────
hyp_files = sorted(PROBLEM_DIR.glob("hypothesis-*.md"))

hyp_refs = {}  # filename -> set of REF-NNN
for hf in hyp_files:
    text = hf.read_text()
    if "## Literature" not in text:
        continue
    # Extract only from the Literature section onward
    lit_section = text[text.index("## Literature"):]
    refs = set(re.findall(r"REF-\d+", lit_section))
    hyp_refs[hf.name] = refs

print("=== Hypothesis literature sections found ===")
for name, refs in sorted(hyp_refs.items()):
    print(f"  {name}: {len(refs)} unique REFs: {sorted(refs)}")
print()

if len(hyp_refs) < 2:
    print("Not enough hypothesis files with Literature sections for cross-hypothesis analysis.")
else:
    # ─── Step 3: Cross-hypothesis overlap ────────────────────────────────────
    ref_to_hypotheses = defaultdict(set)
    for name, refs in hyp_refs.items():
        for ref in refs:
            ref_to_hypotheses[ref].add(name)

    shared_refs = {ref: hyps for ref, hyps in ref_to_hypotheses.items() if len(hyps) > 1}
    all_unique_refs = set(ref_to_hypotheses.keys())

    print("=== Cross-hypothesis reference overlap ===")
    print(f"  Total unique REF IDs across all hypothesis Literature sections: {len(all_unique_refs)}")
    print(f"  REFs appearing in more than one hypothesis: {len(shared_refs)}")
    if shared_refs:
        for ref, hyps in sorted(shared_refs.items()):
            print(f"    {ref}: shared by {sorted(hyps)}")
    print()

    # ─── Step 4: Redundancy ratio ─────────────────────────────────────────────
    # Total "reference slots" = sum of unique refs per hypothesis
    # Redundancy ratio = total slots / total unique refs
    total_slots = sum(len(refs) for refs in hyp_refs.values())
    total_unique = len(all_unique_refs)
    redundancy_ratio = total_slots / total_unique if total_unique > 0 else 0

    print("=== Redundancy analysis ===")
    for name, refs in sorted(hyp_refs.items()):
        print(f"  {name}: {len(refs)} unique refs in Literature section")
    print(f"  Total reference slots (sum across hypotheses): {total_slots}")
    print(f"  Total unique REF IDs: {total_unique}")
    print(f"  Cross-hypothesis redundancy ratio: {redundancy_ratio:.2f}")
    print(f"  Fraction of refs shared across hypotheses: {len(shared_refs)/total_unique:.1%}")
    print()

    # ─── Step 5: Estimate search-angle coverage ───────────────────────────────
    # The refining-hypothesis skill runs 4 searches per hypothesis.
    # If we could only run 2, we'd expect to capture 50% of the queries.
    # With high overlap across queries, the 2-search coverage of unique papers would be high.
    # With low overlap, the 2-search strategy misses the Q3/Q4 exclusive papers.

    # What fraction of refs per hypothesis could plausibly come only from Q3 or Q4?
    # We can't know without execution logs, but we can note:
    # - shared refs across hypotheses likely come from foundational papers surfaced by Q1/Q2
    # - unique-to-one-hypothesis refs are more likely from Q3/Q4 angles

    single_hyp_refs = {ref for ref, hyps in ref_to_hypotheses.items() if len(hyps) == 1}
    print(f"  REFs unique to a single hypothesis (likely Q3/Q4 specific): {len(single_hyp_refs)}")
    print(f"  As fraction of total unique refs: {len(single_hyp_refs)/total_unique:.1%}")
    print()
    print("=== Conclusion for Experiment 2 ===")
    print(f"  The redundancy ratio of {redundancy_ratio:.2f} indicates that on average each unique")
    print(f"  reference appears in {redundancy_ratio:.2f} hypothesis files.")

    if redundancy_ratio >= 1.5:
        print("  This SUPPORTS the hypothesis (redundancy ratio >= 1.5 threshold met).")
    else:
        print("  This does NOT support the hypothesis (redundancy ratio < 1.5 threshold).")

    # What fraction of single-hypothesis refs could be missed by 2-search?
    print()
    print(f"  {len(single_hyp_refs)}/{total_unique} = {len(single_hyp_refs)/total_unique:.1%} of refs are hypothesis-specific.")
    print(f"  These are the refs that Q3/Q4 angles would most likely find.")
    print(f"  If 2 searches miss ~half of these, coverage drops by ~{len(single_hyp_refs)/total_slots/2:.1%} of total slots.")
