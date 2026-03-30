"""
Hypothesis 05, Experiment 2: Token Budget Simulation of Early vs. Late Termination.

Models token cost per hypothesis phase using actual skill word counts, then
computes total session tokens under Scenario A (no early termination) and
Scenario B (fraction F of hypotheses resolved at Step B) as a function of F.
Solves for the F required to achieve 25% and 50% session-level savings.
"""

# --- Actual skill word counts (from wc -w) ---
SKILL_WORDS = {
    "refining-problem":       752,
    "generating-hypotheses":  625,
    "refining-hypothesis":    758,
    "researching-literature": 1021,
    "designing-experiments":  664,
    "running-experiments":    1344,
    "drawing-conclusions":    906,
    "researching":            1632,
}

TOKENS_PER_WORD = 1.33  # Standard prose approximation

def words_to_tokens(w):
    return w * TOKENS_PER_WORD

# --- Per-iteration per-hypothesis phase costs (instruction tokens only) ---
#
# Step B: refining-hypothesis spawns 3 parallel researching-literature tasks
#         + 1 gap-fill = 4 researching-literature invocations, plus the
#         refining-hypothesis skill itself.
# Per-hypothesis Step B instruction tokens:
#   = refining-hypothesis + 4 * researching-literature
step_b_per_hyp = words_to_tokens(
    SKILL_WORDS["refining-hypothesis"] + 4 * SKILL_WORDS["researching-literature"]
)

# Step C: designing-experiments (1 invocation per hypothesis)
step_c_per_hyp = words_to_tokens(SKILL_WORDS["designing-experiments"])

# Step D: running-experiments (1 invocation per hypothesis)
step_d_per_hyp = words_to_tokens(SKILL_WORDS["running-experiments"])

# Step E: drawing-conclusions (1 invocation per hypothesis)
step_e_per_hyp = words_to_tokens(SKILL_WORDS["drawing-conclusions"])

# Fixed iteration costs (Steps A, F, orchestrator overhead per iteration)
# Step A: generating-hypotheses (1 invocation)
# Orchestrator (researching skill): loaded once per session, amortised here
step_a_fixed  = words_to_tokens(SKILL_WORDS["generating-hypotheses"])
orchestrator  = words_to_tokens(SKILL_WORDS["researching"])
phase1_fixed  = words_to_tokens(SKILL_WORDS["refining-problem"])

N_HYPOTHESES = 4  # minimum per iteration

# Full per-iteration token cost (Scenario A: no early termination)
# All N hypotheses complete Steps B-C-D-E
cost_step_b_total = N_HYPOTHESES * step_b_per_hyp
cost_step_cde_total = N_HYPOTHESES * (step_c_per_hyp + step_d_per_hyp + step_e_per_hyp)
cost_fixed = phase1_fixed + step_a_fixed + orchestrator

total_A = cost_fixed + cost_step_b_total + cost_step_cde_total

print("=" * 65)
print("TOKEN BUDGET SIMULATION — Hypothesis 05, Experiment 2")
print("=" * 65)
print()
print("--- Skill word counts and per-invocation token costs ---")
for skill, words in SKILL_WORDS.items():
    print(f"  {skill:<30}: {words:>5} words  ({words_to_tokens(words):>8.0f} tokens)")
print()
print("--- Per-hypothesis phase costs (instruction tokens) ---")
print(f"  Step B (refining-hypothesis + 4 lit searches): {step_b_per_hyp:>8.0f} tokens")
print(f"  Step C (designing-experiments):                {step_c_per_hyp:>8.0f} tokens")
print(f"  Step D (running-experiments):                  {step_d_per_hyp:>8.0f} tokens")
print(f"  Step E (drawing-conclusions):                  {step_e_per_hyp:>8.0f} tokens")
print(f"  C+D+E combined per hypothesis:                 {step_c_per_hyp+step_d_per_hyp+step_e_per_hyp:>8.0f} tokens")
print()
print(f"--- Scenario A: N={N_HYPOTHESES} hypotheses, NO early termination ---")
print(f"  Fixed (Phase 1 + Step A + orchestrator):  {cost_fixed:>10.0f} tokens")
print(f"  Step B total ({N_HYPOTHESES} hypotheses):             {cost_step_b_total:>10.0f} tokens")
print(f"  Steps C-D-E total ({N_HYPOTHESES} hypotheses):       {cost_step_cde_total:>10.0f} tokens")
print(f"  TOTAL (Scenario A):                        {total_A:>10.0f} tokens")
print()
print(f"  Step B share of total: {100*cost_step_b_total/total_A:.1f}%")
print(f"  Steps C-D-E share:     {100*cost_step_cde_total/total_A:.1f}%")
print(f"  Fixed share:           {100*cost_fixed/total_A:.1f}%")
print()

# --- Scenario B: fraction F of hypotheses resolved at Step B, skip C-D-E ---
print("--- Scenario B: early termination after Step B ---")
print("  F = fraction of hypotheses resolved at Step B (skipping C-D-E)")
print()
print(f"  {'F':>6} | {'Total B tokens':>14} | {'Total B (tokens)':>16} | {'Scenario B total':>16} | {'Savings %':>10}")
print(f"  {'-'*6}-+-{'-'*14}-+-{'-'*16}-+-{'-'*16}-+-{'-'*10}")

savings_targets = {0.25: None, 0.50: None}

for f_pct in range(0, 101, 5):
    f = f_pct / 100.0
    # Hypotheses that clear Step B and go to C-D-E
    n_proceed = N_HYPOTHESES * (1 - f)
    cost_cde_B = n_proceed * (step_c_per_hyp + step_d_per_hyp + step_e_per_hyp)
    total_B = cost_fixed + cost_step_b_total + cost_cde_B
    savings_pct = 100.0 * (total_A - total_B) / total_A
    marker = ""
    if abs(savings_pct - 25) < 3:
        marker = " <-- ~25% savings"
    if abs(savings_pct - 50) < 3:
        marker = " <-- ~50% savings"
    print(f"  {f_pct:>5}% | {cost_step_b_total:>14.0f} | {cost_cde_B:>16.0f} | {total_B:>16.0f} | {savings_pct:>9.1f}%{marker}")

print()

# Solve analytically for F given savings target T
# Savings = F * N * (C + D + E) / total_A = T
# => F = T * total_A / (N * cost_cde_per_hyp)
cost_cde_per_hyp = step_c_per_hyp + step_d_per_hyp + step_e_per_hyp
for target in [0.25, 0.50]:
    f_required = target * total_A / (N_HYPOTHESES * cost_cde_per_hyp)
    print(f"  F required for {int(target*100)}% total savings: {f_required*100:.1f}% of hypotheses resolved at Step B")

print()
print("--- Plausibility assessment ---")
print("  Empirical range from Experiment 1: 0% of hypotheses resolved at Step B")
print("  (0/8 hypotheses in current session; 0/4 in gauss-sum test run)")
print()
print("  For 25% savings: need ~{:.0f}% early termination — IMPLAUSIBLE given 0% observed".format(
    100 * (0.25 * total_A / (N_HYPOTHESES * cost_cde_per_hyp))))
print("  For 50% savings: need ~{:.0f}% early termination — IMPLAUSIBLE given 0% observed".format(
    100 * (0.50 * total_A / (N_HYPOTHESES * cost_cde_per_hyp))))
print()
print("CONCLUSION:")
f_25 = 0.25 * total_A / (N_HYPOTHESES * cost_cde_per_hyp)
f_50 = 0.50 * total_A / (N_HYPOTHESES * cost_cde_per_hyp)
if f_25 <= 0.60:
    print(f"  25% savings requires F={f_25*100:.1f}% — within plausible range (10-40%): CONFIRMS 25% target feasibility")
else:
    print(f"  25% savings requires F={f_25*100:.1f}% — EXCEEDS plausible range: REFUTES 25% target feasibility")
if f_50 <= 0.60:
    print(f"  50% savings requires F={f_50*100:.1f}% — within plausible range: CONFIRMS 50% target feasibility")
else:
    print(f"  50% savings requires F={f_50*100:.1f}% — EXCEEDS plausible range: REFUTES 50% target feasibility")
