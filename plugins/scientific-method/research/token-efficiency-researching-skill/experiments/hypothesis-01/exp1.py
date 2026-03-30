"""
Experiment 3: Prototype Orchestrator Measuring Before/After Instruction-Token Load

Simulates Step B orchestration token loads for two architectures:
  - Current: each of N invocations receives the full skill file
  - Proposed: skill file is loaded once into a shared prefix; invocations reference it
"""

import os

SKILL_PATH = (
    "/home/fence/.claude-equine/plugins/marketplaces/pipemind-marketplace"
    "/plugins/scientific-method/skills/researching-literature/SKILL.md"
)

N_HYPOTHESES = 4
SEARCHES_PER_HYPOTHESIS = 4
N = N_HYPOTHESES * SEARCHES_PER_HYPOTHESIS  # 16 invocations

# Generated content estimate from problem.md: 800 words/invocation x 1.33 tokens/word
GENERATED_WORDS_PER_INVOCATION = 800
TOKENS_PER_WORD = 1.33


def count_tokens(text: str) -> float:
    """Approximate token count: word count * 1.33."""
    return len(text.split()) * TOKENS_PER_WORD


def main():
    # (1) Read skill file and measure token count
    with open(SKILL_PATH, "r") as f:
        skill_text = f.read()

    skill_words = len(skill_text.split())
    skill_tokens = count_tokens(skill_text)

    # (2) Simulate current architecture: each invocation embeds the full skill file
    current_instruction_tokens = N * skill_tokens

    # (3) Simulate proposed architecture: skill file loaded once (shared prefix)
    proposed_instruction_tokens = skill_tokens  # loaded exactly once

    # (4) Estimated generated-content tokens (same in both architectures)
    generated_tokens_per_invocation = GENERATED_WORDS_PER_INVOCATION * TOKENS_PER_WORD
    total_generated_tokens = N * generated_tokens_per_invocation

    # (5) Total Step B tokens
    current_total = current_instruction_tokens + total_generated_tokens
    proposed_total = proposed_instruction_tokens + total_generated_tokens

    absolute_saving = current_total - proposed_total
    pct_saving = absolute_saving / current_total * 100
    in_target_range = 40.0 <= pct_saving <= 60.0

    # Fraction of total Step B tokens saved
    step_b_baseline_words = 19400  # from problem.md
    step_b_baseline_tokens = step_b_baseline_words * TOKENS_PER_WORD
    saving_vs_baseline = absolute_saving / step_b_baseline_tokens * 100

    print("=" * 65)
    print("Step B Instruction-Token Load: Current vs. Proposed Architecture")
    print("=" * 65)
    print(f"Skill file word count:               {skill_words:>10,}")
    print(f"Skill file token count (x1.33):      {skill_tokens:>10,.1f}")
    print(f"N invocations (4 hyp x 4 searches):  {N:>10,}")
    print(f"Generated tokens/invocation (est):   {generated_tokens_per_invocation:>10,.1f}")
    print(f"Total generated tokens:              {total_generated_tokens:>10,.1f}")
    print()
    print(f"{'':35} {'Current':>12} {'Proposed':>12}")
    print(f"{'-'*60}")
    print(f"{'Instruction tokens':35} {current_instruction_tokens:>12,.1f} {proposed_instruction_tokens:>12,.1f}")
    print(f"{'Generated tokens':35} {total_generated_tokens:>12,.1f} {total_generated_tokens:>12,.1f}")
    print(f"{'Total tokens':35} {current_total:>12,.1f} {proposed_total:>12,.1f}")
    print()
    print(f"Absolute saving (tokens):            {absolute_saving:>10,.1f}")
    print(f"Percentage saving (of current total):{pct_saving:>10.1f}%")
    print(f"Saving vs. problem.md baseline:      {saving_vs_baseline:>10.1f}%")
    print(f"In target range [40%, 60%]:          {str(in_target_range):>10}")
    print()
    if pct_saving >= 40:
        print("RESULT: CONFIRMS — instruction-only saving from prefix deduplication")
        print(f"        is {pct_saving:.1f}% of Step B total (>= 40% threshold).")
        if pct_saving > 60:
            print(f"        NOTE: {pct_saving:.1f}% exceeds the 60% upper bound of the claimed")
            print("        range, indicating the refined statement underestimates savings.")
    else:
        print("RESULT: REFUTES — instruction-only saving is insufficient.")


if __name__ == "__main__":
    main()
