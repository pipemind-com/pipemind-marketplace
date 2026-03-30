"""
Experiment 1: Analytical Token Count Model for 2 vs 4 Hypotheses

Data anchors from problem.md:
- 8 skill files, 7,702 words total
- ~37,000 words loaded per minimum-4-hypothesis iteration (N=4)
- Literature research accounts for ~52% of the 37,000 words
- 16+ parallel literature invocations = 4 hypotheses × 4 literature searches each

Model:
  Total(N) = Fixed_overhead + N * Per_hypothesis_cost

Steps B-E map to these skills (8 total):
  Step B (refine-hypothesis):         1 skill file load per hypothesis   -> N invocations
  Step B (researching-literature):    4 skill file loads per hypothesis  -> 4N invocations
  Step C (designing-experiments):     1 skill file load per hypothesis   -> N invocations
  Step D (running-experiments):       1 skill file load per hypothesis   -> N invocations
  Step E (draw-conclusions):          1 skill file load per hypothesis   -> N invocations

Plus fixed overhead (not scaled per hypothesis):
  - Orchestrator/researching skill:   1 invocation (fixed)
  - refining-problem:                 1 invocation (fixed)
  - generating-hypotheses:            1 invocation (fixed)
  - Final assessment step:            1 invocation (fixed)

Total skill invocations = 4 (fixed) + N * (1+4+1+1+1) = 4 + 8N

For N=4: invocations = 4 + 8*4 = 36
But problem says 37,000 words total. Let's back-calculate average words per invocation.
"""

# Data anchors
total_words_N4 = 37000
N4 = 4
lit_fraction = 0.52  # literature research share

# Skill invocation counts
# Fixed (not scaled per hypothesis):
# - researching orchestrator, refining-problem, generating-hypotheses, assessment step
fixed_invocations = 4

# Per-hypothesis Steps B-E:
# Step B: refine-hypothesis (1 invoke) + researching-literature (4 invokes) = 5
# Step C: designing-experiments (1 invoke)
# Step D: running-experiments (1 invoke)
# Step E: draw-conclusions (1 invoke)
per_hypothesis_invocations = 8  # = 5 + 1 + 1 + 1

total_invocations_N4 = fixed_invocations + per_hypothesis_invocations * N4
print(f"Total skill invocations for N=4: {total_invocations_N4}")

# Average words per invocation
avg_words_per_invocation = total_words_N4 / total_invocations_N4
print(f"Average words per invocation: {avg_words_per_invocation:.1f}")

# The literature (Step B researching-literature) accounts for 52% of total
lit_words_N4 = lit_fraction * total_words_N4
print(f"\nLiterature invocations for N=4: {4 * N4} = 16")
print(f"Literature words N=4: {lit_words_N4:.0f}")
lit_words_per_invoke = lit_words_N4 / (4 * N4)
print(f"Words per literature invocation: {lit_words_per_invoke:.1f}")

# Non-literature words
non_lit_words_N4 = total_words_N4 - lit_words_N4
non_lit_invocations_N4 = total_invocations_N4 - 4 * N4
print(f"\nNon-literature invocations for N=4: {non_lit_invocations_N4}")
print(f"Non-literature words N=4: {non_lit_words_N4:.0f}")
non_lit_words_per_invoke = non_lit_words_N4 / non_lit_invocations_N4
print(f"Words per non-literature invocation: {non_lit_words_per_invoke:.1f}")

# Model: separate lit and non-lit costs
# Let w_lit = words per literature invocation
# Let w_nonlit = words per non-literature invocation
w_lit = lit_words_per_invoke
w_nonlit = non_lit_words_per_invoke

def total_words(N, w_lit, w_nonlit, fixed_invocations, fixed_words_per_invoke=None):
    """Total word cost for N hypotheses."""
    if fixed_words_per_invoke is None:
        fixed_words_per_invoke = w_nonlit
    lit_invokes = 4 * N
    # Per-hypothesis non-lit: refine(1) + design(1) + run(1) + conclude(1) = 4
    per_hyp_nonlit = 4
    nonlit_invokes = fixed_invocations + per_hyp_nonlit * N
    return lit_invokes * w_lit + nonlit_invokes * w_nonlit

T_N4 = total_words(4, w_lit, w_nonlit, fixed_invocations)
T_N2 = total_words(2, w_lit, w_nonlit, fixed_invocations)

print("\n--- Model Predictions ---")
print(f"Model T(N=4): {T_N4:.0f} words (expected: ~{total_words_N4})")
print(f"Model T(N=2): {T_N2:.0f} words")
print(f"Reduction factor: {(T_N4 - T_N2) / T_N4 * 100:.1f}%")

# Verify: check the 52% literature fraction at N=2
lit_N2 = 4 * 2 * w_lit
total_N2_full = total_words(2, w_lit, w_nonlit, fixed_invocations)
print(f"\nLiterature fraction at N=2: {lit_N2 / total_N2_full * 100:.1f}%")

# Linear assumption: what if cost scales purely linearly (no super-linear)?
# Under pure linear scaling, each hypothesis has equal weight
# per_hyp_cost = (T_N4 - fixed_cost) / 4
# But we need to estimate fixed_cost differently
# Pure linear: T(N) = F + N * C_per_hyp
# T(4) = F + 4C = 37000
# Assume fixed invocations cost same as per-invoke average
F_linear = fixed_invocations * avg_words_per_invocation
C_per_hyp = (total_words_N4 - F_linear) / N4
T_N2_linear = F_linear + 2 * C_per_hyp
print(f"\n--- Linear Scaling Model (sanity check) ---")
print(f"Fixed overhead: {F_linear:.0f} words")
print(f"Per-hypothesis cost: {C_per_hyp:.0f} words")
print(f"T(N=2) under linear: {T_N2_linear:.0f} words")
print(f"Reduction under linear: {(total_words_N4 - T_N2_linear) / total_words_N4 * 100:.1f}%")

# Super-linear analysis: literature invocations are 4N (linear in N, but literature
# accounts for 52% at N=4). At N=2, literature invocations drop to 8 (from 16),
# a 50% reduction in the highest-cost component.
print(f"\n--- Super-linear (literature-dominant) Analysis ---")
print(f"Literature cost at N=4: {4*N4*w_lit:.0f} words ({4*N4} invocations)")
print(f"Literature cost at N=2: {4*2*w_lit:.0f} words ({4*2} invocations)")
print(f"Literature savings: {(4*N4*w_lit - 4*2*w_lit):.0f} words")
print(f"Literature savings as % of total T(N=4): {(4*N4*w_lit - 4*2*w_lit)/total_words_N4*100:.1f}%")

# Non-literature savings at N=2
nonlit_save = ((4 * N4) - (4 * 2)) * w_nonlit  # per-hyp non-lit steps
print(f"Non-literature per-hyp savings: {nonlit_save:.0f} words")
print(f"Total savings: {(T_N4 - T_N2):.0f} words")
print(f"Total reduction: {(T_N4 - T_N2)/T_N4*100:.1f}%")

# Sensitivity: what if fixed overhead is larger?
print(f"\n--- Sensitivity Analysis ---")
for fixed_frac in [0.05, 0.10, 0.15, 0.20]:
    F = fixed_frac * total_words_N4
    C = (total_words_N4 - F) / N4
    T2 = F + 2 * C
    reduction = (total_words_N4 - T2) / total_words_N4 * 100
    print(f"Fixed overhead = {fixed_frac*100:.0f}% of total: T(N=2) reduction = {reduction:.1f}%")

print("\n--- Conclusion ---")
print(f"Under the literature-dominant model (52% lit anchor):")
print(f"  T(N=4) = {T_N4:.0f} words")
print(f"  T(N=2) = {T_N2:.0f} words")
print(f"  Reduction = {(T_N4 - T_N2)/T_N4*100:.1f}%")
print(f"  This is {'within' if abs((T_N4-T_N2)/T_N4*100 - 50) <= 10 else 'outside'} the ±10pp of 50% claimed by the hypothesis.")
