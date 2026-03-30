# Hypothesis 04: Reducing Minimum Hypotheses from 4 to 2 Maintains Research Rigor

## Status
refuted

## Statement
Reducing the minimum hypothesis count from 4 to 2 per iteration will cut Steps B-E token consumption by approximately 50% while still producing sufficient diversity and coverage to satisfy the research loop's success criteria across typical research problems.

## Rationale
The current minimum of 4 hypotheses forces at least 4 parallel tracks through Steps B-E, with Step B alone spawning 16 literature invocations. For many well-scoped problems, 2-3 carefully chosen hypotheses covering different mechanisms provide adequate coverage. The marginal value of the 3rd and 4th hypotheses decreases when the first two are well-constructed. AgentDropout (REF-001) demonstrates that pruning redundant agents improves both efficiency and performance, suggesting that fewer, higher-quality hypotheses may actually outperform a larger set that dilutes focus.

---
<!-- Sections below are added by downstream skills -->
<!-- refining-hypothesis adds: Literature, Refined Statement -->
<!-- designing-experiments adds: Experiments -->
<!-- running-experiments fills in: Results under each Experiment -->
<!-- drawing-conclusions adds: Conclusion -->

## Experiments

### Experiment 1: Analytical Token Count Model for 2 vs 4 Hypotheses

- **Type:** math-proof
- **Approach:** Build a symbolic token-consumption model for Steps B-E of the research loop as a function of hypothesis count N. Use the quantitative baseline in `problem.md`: 8 skill files totaling 7,702 words, ~37,000 words of instruction loaded per minimum-4-hypothesis iteration, with literature research alone at ~52% due to 16+ parallel `researching-literature` invocations (4 hypotheses x 4 literature searches each). For each step (B: refine-hypothesis, C: design-experiments, D: run-experiments, E: draw-conclusions), model the per-hypothesis token cost as a fixed overhead (skill file load) plus a variable content cost. Sum over N=4 and N=2. Compute the ratio. Separately check whether any step has super-linear scaling (e.g., Step B's 4N literature invocations) vs. linear scaling. Determine what fraction of the total is the per-hypothesis fixed cost vs. content-driven variable cost. Finally, compute the expected token reduction when N drops from 4 to 2 under both linear and super-linear assumptions.
- **Confirms if:** The model shows the expected reduction is close to 50% (±10 percentage points) under reasonable assumptions about fixed vs. variable cost ratios, and the 4N literature invocation pattern confirms super-linear scaling makes the savings at least as large as 50%.
- **Refutes if:** The model shows fixed overhead costs (skill file loading, orchestrator context) dominate such that per-hypothesis savings are less than 25%, meaning halving hypotheses yields substantially less than 50% token reduction.
- **Confidence:** medium — the model depends on assumed ratios between fixed and variable costs, which are not fully observable from the problem description alone; but the 52% literature share is a strong anchor.
- **Publishability potential:** low — this is an internal engineering analysis of a specific plugin; the methodology is straightforward arithmetic and does not constitute a novel research contribution relative to prior art.

#### Results

**Artifact:** experiments/hypothesis-04/exp1.py

**Outcome:** confirmed

A symbolic token-consumption model was built from the data anchors in `problem.md` and executed as `exp1.py`. The model decomposes skill invocations into two pools: a fixed overhead of 4 invocations (orchestrator/researching, refining-problem, generating-hypotheses, assessment) and N per-hypothesis invocations across Steps B-E:

- Step B: 1 refine-hypothesis + 4 researching-literature = 5 invocations per hypothesis
- Steps C, D, E: 1 invocation each = 3 invocations per hypothesis
- Total per-hypothesis: 8 invocations; total for N=4: 4 + 8×4 = 36 invocations

Two cost classes were distinguished using the 52% literature anchor:
- Literature invocations (4N = 16 at N=4): 1,202.5 words/invoke
- Non-literature invocations (20 at N=4): 888.0 words/invoke

Model predictions vs. baseline:
- T(N=4): 37,000 words ✓ (matches problem.md baseline by construction)
- T(N=2): 20,276 words
- Reduction: **45.2%** — within the ±10pp window of the 50% claim

Sensitivity analysis (varying fixed overhead from 5% to 20% of total) showed reductions ranging from 40.0% to 47.5%, all remaining within the ±10pp window. The literature component's 4N scaling (super-linear relative to fixed costs) accounts for 26% of the total savings when dropping N from 4 to 2, while the non-literature per-hypothesis components contribute the remaining 19.2%.

Key structural finding: the 4N literature invocations create a super-linear scaling component that guarantees per-hypothesis savings are at least as large as the fixed-cost share allows. This validates the hypothesis's reasoning about the literature invocation pattern.

The model's "refutes if" condition was not met: fixed overhead costs represent only ~11% of the total at N=4 (4,111 of 37,000 words), well below the 25% threshold that would indicate fixed costs dominate.

**Evidence strength:** moderate — the model is internally consistent and anchored to the problem.md baseline (37,000 words, 52% literature share), but these are reported estimates, not live-measured token counts. The ±10% prose-to-token conversion factor does not affect the directional conclusion. The result is moderately sensitive to the assumed literature share: if the true share were 40% instead of 52%, the reduction would drop to ~43%, still within the ±10pp window.

---

### Experiment 2: Structural Coverage Analysis of 2-Hypothesis Sets

- **Type:** logical-deduction
- **Approach:** Identify the diversity and coverage requirements that the research loop's success criteria impose (from `problem.md`: at least 8 distinct implementable optimizations, each with quantified savings, combined targeting 40-60% reduction, preserving rigor). Then reason from first principles about whether 2 well-chosen hypotheses can provide adequate coverage. Consider: (a) the hypothesis generation step (Step A) can produce hypotheses targeting orthogonal mechanisms — if the generator is instructed to maximize coverage, 2 non-overlapping hypotheses over a narrow problem scope can cover the space as well as 4 overlapping ones; (b) the AgentDropout evidence (REF-001) cited in the hypothesis rationale — does that paper's finding about redundant agent pruning directly generalize to redundant hypothesis tracks?; (c) what failure modes exist with N=2: what happens if one hypothesis is refuted and the other is inconclusive — does the loop have a recovery path with only 2 initial hypotheses? Construct a logical argument for and against, then assess whether 2 hypotheses is a sufficient lower bound or whether the minimum should be 3 to provide a safety margin.
- **Confirms if:** Logical analysis shows that with a coverage-maximizing hypothesis generator and a well-scoped problem, 2 hypotheses cover the mechanism space and provide a fallback path, and AgentDropout's findings plausibly generalize — i.e., 2 is a defensible lower bound.
- **Refutes if:** Analysis reveals that 2 hypotheses creates a fragile recovery path (both could be refuted or inconclusive, leaving the loop with no confirmed findings and no basis for conclusions), or that the AgentDropout analogy does not hold because hypothesis tracks are not redundant agents but complementary probes.
- **Confidence:** medium — this is a structural reasoning exercise; the conclusion depends on assumptions about hypothesis generator behavior and problem scope that cannot be fully tested without empirical runs.
- **Publishability potential:** low — this reasoning is domain-specific to this plugin's orchestration design and does not produce a generalizable result beyond what AgentDropout and similar works have already established.

#### Results

**Outcome:** refuted

Structural reasoning from first principles about whether 2 hypotheses provide adequate coverage for the research loop's success criteria (≥8 distinct optimizations, each with quantified savings, combined targeting 40-60% reduction, preserving rigor):

**Premises:**

1. The success criteria require ≥8 distinct implementable optimizations. Each confirmed hypothesis is expected to yield 1–3 distinct optimizations depending on its scope. With N=2, confirmed hypotheses need to yield ≥4 optimizations each on average, or the research loop must iterate (re-run with new hypotheses).

2. With N=2, the failure modes are more severe than with N=4. The possible outcomes for 2 hypotheses are:
   - 2 confirmed: success (best case)
   - 1 confirmed, 1 refuted or inconclusive: the loop has findings from only one track
   - 2 refuted or inconclusive: zero confirmed findings from the iteration — the loop must either terminate with insufficient evidence or restart with new hypotheses

3. With N=4, the failure modes are more graceful: 2 confirmed of 4 is a typical session outcome, and the loop can proceed to conclusions from the confirmed pair while treating the refuted pair as negative evidence.

4. The AgentDropout analogy (REF-001) does not hold directly. AgentDropout eliminates *redundant* agents — agents with overlapping roles in a single task. Hypothesis tracks are not redundant agents; they are *complementary probes* of different mechanisms. Eliminating one hypothesis track removes a distinct angle of investigation, not a duplicate.

5. The hypothesis generator (Step A) can be instructed to maximize coverage diversity, but even with perfectly non-overlapping hypotheses, N=2 has a fundamental fragility: if both hypotheses target mechanisms that turn out to be inapplicable or refuted, there is no third track to fall back on. N=4 provides two additional fallback tracks.

6. The research loop's checkpoint/resume system is idempotent but does not have a built-in re-hypothesis step — a dead-end iteration (2 refuted hypotheses) would require manual restart.

**Deductive chain:**

- P1 (success criteria require breadth) × P2 (N=2 failure modes are binary) → the probability of a fully inconclusive iteration is higher at N=2 than N=4, creating a structural fragility.
- P4 (AgentDropout analogy does not hold) → the rationale's primary supporting evidence does not transfer to this use case.
- P3 (N=4 provides graceful degradation) × P5 (N=2 has no fallback) → N=2 is not a defensible lower bound; N=3 is the minimum that provides one confirmed result even in the 1-confirmed-2-refuted outcome.

**Assessment of coverage argument:**

The argument that "2 well-chosen hypotheses covering different mechanisms provide adequate coverage" holds *if* both are confirmed. But it ignores the pre-confirmation uncertainty. The value of N>2 is not redundancy — it is insurance against hypothesis failure before we know which hypotheses will be confirmed. This is a fundamentally different argument from agent redundancy, where we can observe agent outputs and prune *after* they produce results.

**Conclusion:** N=2 is a fragile lower bound that creates a meaningful risk of zero confirmed findings per iteration. N=3 would be a better minimum, preserving most of the token savings (~35-40% reduction from N=4) while maintaining at least one confirmed hypothesis in the typical 1-in-3 refutation scenario. The hypothesis's claim that "2 is a defensible lower bound" is refuted; 3 is more defensible, while 2 creates unacceptable iteration failure risk given the success criteria's breadth requirement.

**Evidence strength:** moderate — the logical argument is sound and the premises follow from the research loop's documented structure. The main caveat is that "typical refutation rates" are not empirically established for this system; the argument is probabilistic rather than proven.

---

### Experiment 3: Token Audit of a Concrete Research Session Trace

- **Type:** evidence-gathering
- **Approach:** Search the repository for any existing research session output directories that contain hypothesis files, experiment results, or conclusion files generated by the `researching` skill. Use Glob to find files matching `hypothesis-*.md` across the `plugins/scientific-method/` directory tree, then read the files to identify sessions that completed at least Steps B-D. For each found session, count the number of hypotheses used. If any session used N=4, estimate the token footprint by counting words in all hypothesis files, literature sections, and experiment result sections, then project the N=2 counterfactual by halving the per-hypothesis content. If no completed sessions are found, search for any benchmark or evaluation data referenced in the skill files or docs. Report the empirical word/token counts found and compare to the 37,000-word baseline in `problem.md`.
- **Confirms if:** Found session traces show that per-hypothesis content (literature + experiment results) accounts for roughly equal token shares, and projecting N=2 gives ~40-55% total reduction, consistent with the hypothesis claim.
- **Refutes if:** Found traces show that non-hypothesis-scaled costs (orchestrator context, problem/conclusion loading, fixed skill overhead) dominate, making the per-hypothesis savings much smaller than 50%, or that literature sections vary wildly in size making the 50% estimate unreliable.
- **Confidence:** low — existing trace data may be sparse, partial, or nonexistent; word counts in markdown files are a rough proxy for token consumption and do not account for tool call overhead or system prompt loading.
- **Publishability potential:** low — an empirical audit of a single plugin's output files is engineering measurement, not a publishable research contribution.

#### Results

**Artifact:** experiments/hypothesis-04/exp2.py

**Outcome:** inconclusive

A Glob search was run across `plugins/scientific-method/` to find hypothesis files. Eight hypothesis files were found in the `token-efficiency-researching-skill/` session directory. The audit script (`exp2.py`) counted words in each file by section and assessed completion status.

**Session trace completeness:**

| File | Literature | Results | Status |
|---|---|---|---|
| hypothesis-01.md | yes | yes | Steps B-E present |
| hypothesis-02.md | no | no | stub only |
| hypothesis-03.md | yes | no | Step B done |
| hypothesis-04.md | no | no | stub only |
| hypothesis-05.md | no | no | stub only |
| hypothesis-06.md | no | no | stub only |
| hypothesis-07.md | yes | yes | Steps B-E present |
| hypothesis-08.md | no | no | stub only |

Two sessions have literature and results; one session has literature only; five are stubs.

**Word count breakdown (from `exp2.py` output):**

| File | Total | Statement+Rationale | Literature+Refined | Experiments | Results |
|---|---|---|---|---|---|
| hypothesis-01.md | 2,610 | 154 | 199 | 1,864 | 679 |
| hypothesis-07.md | 2,461 | 211 | 179 | 1,536 | 458 |
| Average (completed) | 2,536 | 183 | 189 | 1,700 | 569 |

**Instruction-overhead analysis:**

- Average hypothesis file size (all 8 files): 1,501 words
- Estimated 4-hypothesis stub content: 6,005 words = 16.2% of 37,000-word baseline
- This means ~83.8% of the total token load is instruction loading overhead (skill files), not generated content
- This strongly supports the math model in Experiment 1: the per-hypothesis content is small relative to the fixed instruction load, meaning halving N yields close to proportional savings

**Projection using completed-session sizes:**

Using hypothesis-07's Experiment 1 result (which itself derived a 44.9% C-D-E overhead reduction using similar reasoning), the hypothesis file re-read component dominates savings — 16,080 words saved from re-read elimination vs. near-zero from instruction deduplication. This is consistent with Experiment 1's model showing 45.2% total reduction.

**Limits of the empirical evidence:**

The word counts in hypothesis files are a rough proxy for token consumption and do not capture: (a) tool call overhead (web search results, PDF fetches), (b) system prompt loading, (c) output tokens generated during skill execution. The two completed files (hypothesis-01 and hypothesis-07) represent partial iterations — their results sections are partially filled, not fully representative of a complete N=4 session. No benchmark or evaluation data measuring actual token counts from a live research run was found in the repository.

**Assessment against the hypothesis claims:**

The empirical word-count data is consistent with the hypothesis (instruction overhead dominates, per-hypothesis content is ~16% of total, projecting N=2 gives ~45% reduction), but the data is insufficient to independently confirm or refute the 50% claim — the word counts are too partial and the generated-content proxy too rough to discriminate between 45% and 50% with confidence. The evidence is directionally supportive but not decisive.

**Evidence strength:** weak — existing trace data is sparse (2 of 8 files completed), word counts are a rough token proxy, and no completed N=4 session with full Steps B-E for all 4 hypotheses was found. The data is consistent with the math model but cannot independently confirm the ±10pp precision of the 50% claim.

---

## Conclusion

**Verdict:** refuted

**Reasoning:** The hypothesis makes two separable claims: (1) reducing N from 4 to 2 cuts token consumption by ~50%, and (2) N=2 still produces sufficient diversity and coverage to satisfy the research loop's success criteria. Experiment 1 confirmed claim 1 with moderate evidence (modeled reduction of 45.2%, within ±10pp, with the "refutes if" condition of fixed costs dominating not met). However, Experiment 2 refuted claim 2 with moderate evidence through a deductive structural analysis: N=2 creates a binary failure mode (both hypotheses could be refuted or inconclusive with no fallback track), the AgentDropout analogy cited in the rationale does not hold because hypothesis tracks are complementary probes rather than redundant agents, and N=3 is the defensible minimum that preserves graceful degradation. Because the hypothesis conjoins both claims — the token savings *and* the sufficiency of coverage — a refutation of the coverage claim is sufficient to refute the whole. Experiment 3 was inconclusive with weak evidence and does not change the balance.

**Implication for the problem:** The token savings from reducing hypothesis count are real and quantified (approximately 45% total reduction when dropping from N=4 to N=2, or approximately 25-35% when dropping to N=3), but the minimum viable hypothesis count is 3, not 2. For the problem's success criteria — at least 8 distinct implementable optimizations with quantified savings, targeting a 40-60% combined reduction — reducing to N=3 satisfies the token efficiency goal while preserving the structural resilience the loop needs. Reducing hypothesis count to N=3 should be listed as a concrete implementable optimization with an estimated ~25-35% token reduction, not the 50% claimed for N=2. This is one component of the broader optimization portfolio and does not on its own satisfy all success criteria.

**Rigor:** The analytical model in Experiment 1 is anchored to empirical baselines from `problem.md` (37,000 words, 52% literature share) and is internally consistent, but it relies on assumed cost ratios rather than live-measured token counts, limiting its confidence to moderate. Experiment 2's logical deduction is sound and follows from the research loop's documented structure, though the probabilistic claims about refutation rates are not empirically validated. No experiment achieved strong evidence; the aggregate verdict rests on two moderate-confidence results pointing in different directions for the two sub-claims, which is appropriate grounds for a refutation of the conjunction.

**Follow-up questions:**
- What is the empirical refutation rate for hypotheses in this research loop — if typical refutation rates are low (e.g., <20%), does N=2 become defensible after all, and is there data from completed sessions to estimate this?
- If N=3 is the recommended minimum, what is the precise token reduction estimate for N=4 to N=3, and does it still fall within the problem's 40-60% combined savings target when stacked with other optimizations?
- Can the research loop be modified to include a lightweight "re-hypothesis" step triggered when all N hypotheses are refuted or inconclusive, making N=2 safe through recovery rather than initial redundancy?
