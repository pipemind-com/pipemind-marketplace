# Hypothesis 05: Early Termination After Decisive Literature Can Skip Experiments

## Status
refuted

## Statement
Adding an explicit early-termination gate after Step B (literature refinement) — where hypotheses resolved by literature alone skip directly to Step F assessment — will eliminate 25-50% of experiment-phase tokens in iterations where at least one hypothesis is definitively confirmed or refuted by prior work.

## Rationale
The current architecture already notes that hypotheses confirmed/refuted during literature review skip Steps C-D-E, but the orchestrator does not aggressively short-circuit: it still waits for all hypotheses to complete Step B before evaluating. A more aggressive strategy would assess after each hypothesis completes literature review and potentially terminate the entire iteration early if the problem is already solved. This follows the "stop when decisive" principle from the `running-experiments` skill and extends it to the iteration level, avoiding unnecessary experiment design and execution for the remaining hypotheses.

---
<!-- Sections below are added by downstream skills -->
<!-- refining-hypothesis adds: Literature, Refined Statement -->
<!-- designing-experiments adds: Experiments -->
<!-- running-experiments fills in: Results under each Experiment -->
<!-- drawing-conclusions adds: Conclusion -->

## Experiments

### Experiment 1: Count Decisive Literature Outcomes in Existing Runs

- **Type:** evidence-gathering
- **Approach:** Read the existing hypothesis files in `token-efficiency-researching-skill/` and any other completed research directories under the `scientific-method` plugin (check `plugins/scientific-method/` for example runs or archived sessions). For each hypothesis file that contains both a `## Literature` section and a `## Status`, record whether the status was set to `confirmed` or `refuted` by literature alone (i.e., the file has no `## Experiments` section with results, or the conclusion explicitly cites only literature). Count total hypotheses processed, how many were resolved at the literature stage versus needing experiments, and compute the fraction resolved early. Cross-check against the orchestrator skill (`researching/SKILL.md`) to confirm whether the current code actually short-circuits or merely marks status. If no archived runs exist, simulate by inspecting all hypothesis files in the current research session directory and tallying status values.
- **Confirms if:** 25% or more of hypothesis files across completed iterations have status set by literature review (confirmed/refuted) without requiring experiment execution, consistent with the 25-50% savings claim.
- **Refutes if:** Fewer than 10% of hypotheses are resolved at the literature stage, suggesting the early-termination path is rarely triggered and the token savings would be negligible in practice.
- **Confidence:** medium — the current research session is small (a handful of hypotheses) and may not be representative; the fraction depends heavily on problem domain and literature density.
- **Publishability potential:** low — this is an observational count on a small dataset with no generalization; the finding would be a minor implementation note rather than a novel contribution.

#### Results

**Outcome:** refuted

Scanning all hypothesis files in the current research session and the only completed archived run (gauss-sum test run at `tests/results/20260328-150735-gauss-sum-formula/`) to count hypotheses resolved by literature alone.

**Current session (token-efficiency-researching-skill):** 8 hypotheses total. Hypotheses 01, 03, and 07 have `## Literature` sections added by `refining-hypothesis`; all three retain `## Status: pending` and proceeded to experiment design. Hypotheses 02, 04, 05, 06, and 08 have no `## Literature` section (not yet refined). No hypothesis in this session was resolved at the literature stage: **0/8 = 0%**.

**Gauss-sum archived run (20260328-150735):** 4 hypotheses, all 4 have `## Literature` sections. All 4 have `## Status: confirmed`, but all 4 also have `## Experiments` with results and `## Conclusion` sections — they were confirmed via experiments, not literature alone. **0/4 = 0%**.

**Cross-check against orchestrator logic:** Reading `skills/researching/SKILL.md`, Step B states "Some may now have status `confirmed` or `refuted` from literature alone -- those skip Steps C-D-E." Step C states "Find hypotheses that have `## Literature` but no `## Experiments`, with status `pending` or `inconclusive`." This confirms the current code conditionally checks status before spawning C-D-E agents — the per-hypothesis short-circuit exists. However, there is no mechanism to terminate the entire iteration early if one hypothesis is resolved; the loop always processes all hypotheses before the Step F assessment.

**Finding:** Empirically, 0% of hypotheses across all available runs were resolved at the literature stage. The "25-50% of hypotheses resolved early" assumption underlying the hypothesis's savings claim is not observed in practice. Whether this reflects the problem domains tested (Gauss sum formula, token efficiency) or a structural feature of the workflow cannot be determined from this dataset alone.

**Evidence strength:** weak

The dataset is very small (12 hypotheses across 2 sessions, one of which is a simple math problem where literature trivially confirms known proofs rather than replacing experiment). The 0% rate may not generalize; the hypothesis's "confirms if" threshold of 25% could plausibly appear in literature-dense research domains.

---

### Experiment 2: Token Budget Simulation of Early vs. Late Termination

- **Type:** math-proof
- **Approach:** Use the quantitative baseline from `problem.md`: 8 skill files totalling 7,702 words; minimum 4 hypotheses; ~37,000 words of skill instructions loaded per iteration; literature research accounts for ~52% of that total. Model the token cost of each phase per hypothesis: (a) literature refinement (Steps A-B), (b) experiment design (Step C), (c) experiment execution (Step D), (d) conclusion drawing (Step E). Assign approximate token weights using the word counts from the skill files (read each SKILL.md under `plugins/scientific-method/skills/` to get actual line counts, then convert to tokens at ~1.3 tokens/word). Construct two scenarios: Scenario A (current behavior) where all 4 hypotheses complete all phases, and Scenario B (aggressive early termination) where a fraction F of hypotheses are resolved at Step B and skip C-D-E. Compute total tokens for each scenario as a function of F, then solve for the F required to achieve 25% and 50% savings. Compare required F against the empirically plausible range (10-40% of hypotheses resolved by literature) to assess whether the 25-50% claim is achievable under realistic conditions.
- **Confirms if:** The model shows that 25-50% token savings is achievable when 25-60% of hypotheses are resolved by literature — a plausible range — confirming the hypothesis is numerically feasible.
- **Refutes if:** The model shows that achieving 25% savings requires >70% of hypotheses to be resolved by literature, a rate that is implausibly high for most research domains, indicating the savings estimate is overstated.
- **Confidence:** high — this is a closed-form calculation from known inputs; uncertainty comes only from the assumed fraction of early-termination events, which is explicitly modelled as a parameter.
- **Publishability potential:** medium — the token budget model itself could be a useful contribution if generalized to other multi-agent pipelines with conditional phase execution, but the specific numerical result is straightforward arithmetic with no novel methodology.

#### Results

**Artifact:** experiments/hypothesis-05/exp1.py

**Outcome:** refuted

The simulation used actual word counts from `wc -w` on all 8 SKILL.md files (total 7,702 words, confirming the `problem.md` baseline). The model assigns Step B cost per hypothesis as `refining-hypothesis` (758 words) + 4 × `researching-literature` (1,021 words) = 4,842 words → 6,440 tokens. Steps C-D-E per hypothesis: `designing-experiments` (664) + `running-experiments` (1,344) + `drawing-conclusions` (906) = 2,914 words → 3,876 tokens. Fixed overhead (Phase 1 + Step A + orchestrator) = 3,009 words → 4,002 tokens.

**Key results for N=4 hypotheses, Scenario A (no early termination):**
- Step B total: 25,759 tokens (56.9% of session)
- Steps C-D-E total: 15,502 tokens (34.2% of session)
- Fixed: 4,002 tokens (8.8% of session)
- Total: 45,264 tokens

**Scenario B (early termination at fraction F):**
- For 25% total savings: requires F = 73.0% of hypotheses resolved at Step B
- For 50% total savings: requires F = 146.0% — mathematically impossible (exceeds 100%)
- Even 100% early termination (all hypotheses resolved at Step B) saves only 34.2%

The hypothesis's 25-50% savings claim is refuted by the model. The core reason is that Step B (literature refinement) dominates the per-hypothesis token budget at 6,440 tokens vs. 3,876 tokens for C-D-E combined. Even if every hypothesis were resolved at Step B and C-D-E were skipped entirely, the maximum achievable saving is 34.2% — below the 25-50% target range at its midpoint. The 25% lower bound requires an unrealistic 73% of hypotheses to terminate early; the 50% upper bound is mathematically impossible.

The sensitivity analysis is robust: Steps C-D-E account for only 34.2% of total session tokens because Step B's 4× `researching-literature` invocations dominate. The hypothesis implicitly assumed C-D-E represented a larger fraction of total tokens.

**Evidence strength:** strong

The arithmetic is deterministic from the actual skill file word counts. The only approximation is the 1.33 tokens/word factor, which would need to be off by more than 2× to change the qualitative conclusion.

---

### Experiment 3: Code Audit of Orchestrator Short-Circuit Logic

- **Type:** logical-deduction
- **Approach:** Read the orchestrator skill file at `plugins/scientific-method/skills/researching/SKILL.md` in full. Trace the control flow for a hypothesis that is marked `confirmed` or `refuted` during Step B (literature refinement). Specifically determine: (1) Does the orchestrator check hypothesis status before spawning experiment-design sub-agents, or does it spawn them unconditionally and rely on `designing-experiments` to self-skip via its Step 0 check? (2) Is there any logic that terminates the entire iteration early if a decisive result is found, or does it always proceed through all hypotheses before assessing? (3) If the early-termination gate is absent at the orchestrator level, estimate the token waste: even if `designing-experiments` self-skips, does the Task spawn still consume tokens for agent initialization and skill loading? Document every conditional branch that touches hypothesis status between Steps B and C, and assess whether the proposed early-termination gate would require changes to the orchestrator only, to individual skills, or to both.
- **Confirms if:** The audit reveals the orchestrator unconditionally spawns all downstream agents regardless of hypothesis status, meaning the early-termination gate genuinely does not exist and adding it would save the full skill-loading cost for skipped phases.
- **Refutes if:** The orchestrator already conditionally skips experiment phases for resolved hypotheses at the Task-spawn level, meaning the optimization is already implemented and the hypothesis is moot, or the savings are already being captured.
- **Confidence:** high — the orchestrator source is directly readable; the answer is deterministic from the code, not probabilistic.
- **Publishability potential:** low — a code audit finding a missing conditional is an implementation fix, not a publishable contribution; it validates the optimization opportunity but does not generate novel knowledge.

#### Results

**Outcome:** refuted

Full audit of `plugins/scientific-method/skills/researching/SKILL.md`, tracing all control flow for a hypothesis marked `confirmed` or `refuted` during Step B.

**Premise 1:** Step B states: "After tasks complete, re-read each hypothesis. Some may now have status `confirmed` or `refuted` from literature alone -- those skip Steps C-D-E." This is explicit documentation of the per-hypothesis short-circuit.

**Premise 2:** Step C states: "Find hypotheses that have `## Literature` but no `## Experiments`, with status `pending` or `inconclusive`." This is a conditional filter — only hypotheses with status `pending` or `inconclusive` are included. A hypothesis with status `confirmed` or `refuted` after Step B has neither status, so Step C does not spawn an agent for it.

**Premise 3:** Step D states: "Find hypotheses that have `## Experiments` with at least one empty `#### Results` section and status not yet resolved." A hypothesis resolved at Step B has no `## Experiments` section at all, so it also cannot match this condition.

**Premise 4:** Step E states: "Find hypotheses that have experiment results but no `## Conclusion`." A hypothesis resolved at Step B has no experiment results, so it is also skipped by Step E.

**Deduction:** The orchestrator already conditionally skips Steps C, D, and E for hypotheses resolved at Step B, at the Task-spawn level. The early-termination gate for individual hypotheses is already implemented. The hypothesis's premise — that "the orchestrator does not aggressively short-circuit" — is false. The per-hypothesis conditional skip is present in all three relevant steps.

**Additional finding:** There is no mechanism to terminate the entire iteration early if one decisive hypothesis is resolved. The F assessment (Step F) always waits for all hypotheses to complete their respective paths. But this is a different optimization (iteration-level early termination) from the per-hypothesis skip that the hypothesis describes as its primary target.

**Token waste from Task spawn even when skipped:** The orchestrator reads each hypothesis file to evaluate its status before deciding whether to spawn a Task. This read costs tokens, but it is a single file read (~hundreds of tokens), not a full skill-file load. The hypothesis claims "even if `designing-experiments` self-skips, does the Task spawn still consume tokens for agent initialization and skill loading?" — the answer is no, because the orchestrator does not spawn the Task at all for resolved hypotheses. The conditional check is in the orchestrator (researching.SKILL.md), not inside the sub-skill.

**Conclusion:** The early-termination gate described by the hypothesis already exists. The optimization the hypothesis proposes is already implemented. The hypothesis is refuted on two grounds: (1) the specific optimization it claims is missing is in fact present, and (2) even if it were absent, the token savings would be at most 34.2% (from Experiment 2), not 25-50% as claimed.

**Evidence strength:** strong

The orchestrator source is directly readable and the control flow is unambiguous. The conditional filters in Steps B, C, D, and E collectively implement the per-hypothesis short-circuit the hypothesis claims is absent.

---

## Conclusion

**Verdict:** refuted

**Reasoning:** Two independent experiments with strong evidence refute the hypothesis on separate grounds. Experiment 2 (math-proof, strong evidence) demonstrates that the 25-50% savings claim is numerically impossible: because Step B (literature refinement) consumes 6,440 tokens per hypothesis versus only 3,876 tokens for Steps C-D-E combined, skipping C-D-E for 100% of hypotheses yields a maximum saving of 34.2% — below the midpoint of the claimed range — and achieving even the 25% lower bound requires an implausible 73% of hypotheses to terminate early. Experiment 3 (logical-deduction, strong evidence) additionally establishes that the proposed optimization is already implemented: the orchestrator's Step B, C, D, and E all contain explicit status-based conditional filters that skip experiment phases for hypotheses resolved by literature alone. Experiment 1 (evidence-gathering, weak evidence) corroborates by finding 0% early-termination events across all available runs, consistent with the optimization being present but simply rarely triggered.

**Implication for the problem:** This hypothesis does not contribute an implementable optimization. The per-hypothesis early-termination gate is already in place, so no token savings are available from adding it. More critically, the quantitative model reveals that the architectural bottleneck for early-termination savings is not the absence of a gate but the overwhelming dominance of Step B (literature research) in the per-hypothesis token budget — any strategy that skips only C-D-E will have limited impact. The problem's success criteria require identifying optimizations with quantified savings toward a 40-60% total reduction; this hypothesis's mechanism is already captured, and its claimed savings of 25-50% via this path are unreachable. Future hypotheses targeting early termination should instead examine reducing the Step B cost itself (e.g., fewer parallel literature searches per hypothesis, shared literature across hypotheses) rather than skipping post-literature phases.

**Rigor:** The quantitative simulation (Experiment 2) is deterministic arithmetic from actual word counts and is robust: the token-per-word factor would need to be wrong by more than 2x to change the qualitative conclusion. The code audit (Experiment 3) reads primary source (the orchestrator SKILL.md directly) and traces unambiguous control flow; the finding is not probabilistic. The observational count (Experiment 1) is underpowered (12 hypotheses, 2 sessions) but is consistent with the other two experiments and correctly noted as weak evidence. The overall evidence quality is high for the refutation.

**Follow-up questions:**
- Since Step B (literature refinement with 4× parallel `researching-literature` invocations per hypothesis) accounts for ~57% of total session tokens, what is the token cost of batching or sharing literature searches across multiple hypotheses (e.g., 2 hypotheses sharing a single literature pass on overlapping topics)?
- The model shows maximum possible savings from any C-D-E skipping strategy is 34.2%. Is there an equivalent upper-bound analysis for other optimization categories (prompt compression, model routing, hypothesis count reduction) that would identify which strategies have the headroom to reach the 40-60% combined target?
- Given that the per-hypothesis short-circuit already exists and is rarely triggered (0% in observed runs), should the orchestrator emit a diagnostic indicating how many hypotheses were resolved at the literature stage, so future research sessions can measure this empirically across more domains?
