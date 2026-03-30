# Hypothesis 08: Reducing Literature Searches Per Hypothesis from 4 to 2 Maintains Coverage

## Status
refuted

## Statement
Reducing the `refining-hypothesis` skill's literature search invocations from 4 (3 parallel targeted + 1 gap-fill) to 2 (1 targeted + 1 broad) per hypothesis will cut Step B's literature token consumption by 50% while retaining at least 80% of the unique relevant sources discovered.

## Rationale
The current `refining-hypothesis` skill spawns 3 parallel `researching-literature` tasks (for the claim, mechanism, and counterexamples) plus 1 gap-fill search — 4 invocations per hypothesis, each loading the full 1,021-word skill. With overlapping search results across queries (especially for niche topics), the marginal yield of the 3rd and 4th searches is likely low. The TCRA-LLM work (REF-006) found that summarization-based compression achieved 65% token reduction with only 0.3% accuracy loss, suggesting that fewer but broader searches can capture most of the signal. A 2-search strategy (one targeted, one broad) would still cover the hypothesis from multiple angles while halving the literature instruction loading.

---
<!-- Sections below are added by downstream skills -->
<!-- refining-hypothesis adds: Literature, Refined Statement -->
<!-- designing-experiments adds: Experiments -->
<!-- running-experiments fills in: Results under each Experiment -->
<!-- drawing-conclusions adds: Conclusion -->

## Experiments

### Experiment 1: Measure Search Result Overlap Across Query Strategies

- **Type:** code
- **Approach:** Select 2–3 representative research topics drawn from hypotheses in the `token-efficiency-researching-skill/` directory (e.g., "LLM prompt compression token reduction", "multi-agent communication efficiency", "semantic caching LLM systems"). For each topic, issue 4 Semantic Scholar searches mirroring the current refining-hypothesis strategy: (Q1) targeted claim search, (Q2) mechanism/explanation search, (Q3) counterexample/failure-mode search, (Q4) gap-fill broad search. Then issue the 2-search strategy: (Q1') one targeted search, (Q2') one broad search. Collect the paper IDs returned by each query (up to 10 results per query). Compute: (a) Jaccard overlap between Q1∪Q2∪Q3∪Q4 and Q1'∪Q2', expressed as fraction of 4-search corpus covered by 2-search; (b) count of unique papers per strategy; (c) count of papers appearing in 3+ of the 4 original queries (high-redundancy papers). Write results as a comparison table. Repeat for each topic and average the coverage fraction.
- **Confirms if:** The 2-search strategy retrieves ≥80% of the unique papers found by the 4-search strategy across all tested topics, confirming that marginal yield of searches 3 and 4 is low.
- **Refutes if:** The 2-search strategy retrieves <80% of unique papers on average, or if searches 3 and 4 consistently surface unique, non-overlapping papers that searches 1–2 miss entirely.
- **Confidence:** high — paper ID overlap is a direct, objective measurement of the coverage claim. The main limitation is that Semantic Scholar results may not fully proxy actual LLM-driven literature synthesis quality.
- **Publishability potential:** low — direct query overlap measurement is a practical engineering validation, not a novel academic contribution; similar search redundancy analyses exist in information retrieval literature.

#### Results

**Artifact:** experiments/hypothesis-08/exp1.py

**Outcome:** refuted

Semantic Scholar searches were run manually for three representative topics drawn from this research session: (1) LLM Prompt Compression, (2) Multi-Agent Communication Efficiency, and (3) Semantic Caching LLM Systems. For each topic, four queries were issued mirroring the current `refining-hypothesis` strategy (Q1: targeted claim, Q2: mechanism/explanation, Q3: counterexample/failure-mode, Q4: gap-fill broad) and two queries for the proposed 2-search strategy (Q1': targeted, Q2': broad). Each query returned up to 10 results from Semantic Scholar. Paper IDs (S2 IDs) were collected and set operations performed to compute coverage fractions.

Results summary:

| Topic | 4-search unique | 2-search unique | Coverage | Q3/Q4-exclusive |
|---|---|---|---|---|
| LLM Prompt Compression | 40 | 17 | 17.5% | 20 papers |
| Multi-Agent Communication | 39 | 20 | 51.3% | 19 papers |
| Semantic Caching LLM | 35 | 19 | 54.3% | 15 papers |
| **Average** | **38** | **19** | **41.0%** | — |

The 2-search strategy covered only **41.0%** of papers found by the 4-search strategy on average — well below the 80% threshold required to confirm the hypothesis. The refutation is robust: even the best-performing topic (Semantic Caching) only achieved 54.3% coverage.

Noteworthy finding: Q3 for the prompt compression topic ("prompt compression failure modes accuracy degradation counterexample") returned predominantly off-topic papers from materials science (bitumen fatigue tests, composite panels, steel-concrete columns), indicating that the counterexample query angle is noisy. Despite this noisiness, those off-topic Q3 papers still appear in the 4-search corpus and are missed by the 2-search strategy — the coverage metric includes them. When restricting to on-topic papers only, coverage for Topic 1 rises from 17.5% to 20.6%, still far below 80%.

Across all three topics, Q3 and Q4 together contributed 14–20 unique papers not found by Q1 or Q2 alone — a consistent pattern showing that searches 3 and 4 do surface substantially different material. The lack of high-overlap papers appearing in 3 or more of the 4 queries (high-redundancy count = 0 for all topics) further refutes the hypothesis's premise that marginal yield of searches 3 and 4 is low.

The principal limitation is that Semantic Scholar result ordering may not fully replicate the queries an LLM would generate; nonetheless, the queries were designed to mirror the skill's stated strategy as closely as possible.

**Evidence strength:** strong — paper ID overlap is a direct, objective measurement of coverage; the result is reproducible given fixed queries, and all three topics show the same directional outcome far below the 80% threshold.

---

### Experiment 2: Count Unique Sources in Existing Hypothesis Literature Sections

- **Type:** data-analysis
- **Approach:** Scan all hypothesis files in `token-efficiency-researching-skill/` that already have a `## Literature` section (added by `refining-hypothesis`). For each such file: (a) extract all cited references (by REF-NNN tag or URL); (b) cross-reference with `references.md` to determine which unique sources appear; (c) identify how many references in each hypothesis file are shared with other hypothesis files in the same research session (overlap across hypotheses). Also inspect the `refining-hypothesis` skill file at `plugins/scientific-method/skills/refining-hypothesis/SKILL.md` to count exactly how many parallel literature search invocations it spawns and what query strategies it uses for each. Compute: total unique references per hypothesis, fraction of references that are shared across hypotheses (indicating redundancy), and the ratio of total reference slots to unique references (redundancy ratio).
- **Confirms if:** The redundancy ratio is ≥1.5 (i.e., many references appear across multiple search invocations), and fewer than 20% of references would be missed if only 2 of the 4 query angles were used.
- **Refutes if:** Each of the 4 searches surfaces a largely disjoint set of unique references (redundancy ratio near 1.0), meaning each search angle is essential.
- **Confidence:** medium — this measures actual output of the current system, but cannot directly separate which search invocation was responsible for each reference without execution logs. It provides strong circumstantial evidence.
- **Publishability potential:** low — this is an internal system audit; findings are specific to this plugin's architecture and not a general academic contribution.

#### Results

**Artifact:** experiments/hypothesis-08/exp2.py

**Outcome:** skipped

Experiment 1 produced a decisive refuted result with strong evidence. Further testing is unnecessary.

---

### Experiment 3: Logical Derivation of Token Savings Under Overlap Assumptions

- **Type:** math-proof
- **Approach:** Model the token cost of the current 4-search strategy vs. the proposed 2-search strategy formally. Let C_skill = token cost of loading `researching-literature` skill once (estimate from word count of SKILL.md × ~1.33 tokens/word). Let C_query = average tokens per search execution (prompt + result). Current cost per hypothesis: 4 × (C_skill + C_query). Proposed cost: 2 × (C_skill + C_query). Derive the theoretical token reduction as a fraction: (4 − 2) / 4 = 50%, confirming the 50% claim is exactly correct under the assumption that each invocation costs the same. Then stress-test the model: (a) if searches 3 and 4 have lower result utility (fewer relevant papers), does that change the cost calculation? No — token cost is incurred regardless of result quality. (b) Does Step B's total share of session tokens matter? Compute: if literature research is 52% of session tokens (as stated in problem.md), then Step B's 50% reduction yields a 26% total session reduction. State the conclusion: the 50% Step-B reduction claim is derivable from first principles and is not contingent on empirical data; the 80% coverage retention claim is the only empirically uncertain part.
- **Confirms if:** The derivation produces a clean 50% Step-B token reduction under equal-cost-per-invocation assumption, and the total session impact computes to ~26% — consistent with the hypothesis's quantitative claim.
- **Refutes if:** The derivation reveals a structural asymmetry (e.g., searches 3–4 use cheaper sub-skills, or the gap-fill search has a different cost profile) that makes the actual reduction substantially different from 50%.
- **Confidence:** high for the token-reduction half of the hypothesis; the derivation is deterministic given the cost model. Coverage retention (the 80% claim) is not addressable by this experiment alone.
- **Publishability potential:** low — this is a straightforward arithmetic derivation specific to one plugin's architecture; it does not produce a novel research contribution.

#### Results

**Outcome:** skipped

Experiment 1 produced a decisive refuted result with strong evidence. Further testing is unnecessary.

---

## Conclusion

**Verdict:** refuted

**Reasoning:** Experiment 1 produced a decisive, strongly-evidenced refutation. The 2-search strategy covered only 41.0% of papers found by the 4-search strategy on average across three representative topics — far below the 80% coverage-retention threshold required to confirm the hypothesis. This is not a borderline result: even the best-performing topic (Semantic Caching) reached only 54.3%, and the worst (LLM Prompt Compression) reached 17.5%. Critically, zero papers appeared in 3 or more of the 4 original queries (redundancy count = 0), directly refuting the hypothesis's foundational premise that searches 3 and 4 have low marginal yield. Experiments 2 and 3 were skipped as unnecessary given the decisive outcome of Experiment 1.

**Implication for the problem:** This hypothesis targeted the single largest token cost in the research loop — literature search, which accounts for ~52% of session tokens. Its refutation confirms that the 4-search strategy is not redundant: each search angle (claim, mechanism, counterexample, gap-fill) surfaces substantially different material. Reducing to 2 searches would cut token costs by 50% on this step but would sacrifice roughly 59% of discovered sources on average, compromising the literature coverage that underpins hypothesis quality and scientific rigor. This eliminates a tempting but unsound optimization, narrowing the solution space toward other strategies (prompt compression, model downgrading, caching) that do not reduce search breadth. The problem's success criterion 4 — no optimization should compromise scientific rigor — rules out this approach. The finding is nevertheless valuable progress: it establishes that search count reduction is not a viable path, directing attention to compression of the skill instruction text itself or caching of shared search results across hypotheses rather than reducing per-hypothesis search invocations.

**Rigor:** Experiment 1 is methodologically sound: paper ID overlap is a direct, objective measurement with no subjective interpretation required, and the result was consistent across all three topics tested. The principal limitation is that Semantic Scholar result ordering may not perfectly replicate the queries an LLM would generate in practice, and the topics selected are a small sample. However, the margin of failure (41% vs. 80% threshold) is large enough that sampling variation is unlikely to reverse the conclusion. The counterexample query's off-topic results (materials science papers for Topic 1) were noted and sensitivity-tested; even excluding them, coverage remained far below threshold.

**Follow-up questions:**
- Can the `researching-literature` skill instruction text itself be compressed (e.g., from ~1,021 words to ~400 words) without degrading search quality, capturing instruction-loading savings without reducing search count?
- Is cross-hypothesis caching of search results viable — i.e., if two hypotheses in the same session share a topic area, can their search results be shared to avoid redundant invocations?
- Do searches 3 (counterexample) and 4 (gap-fill) contribute disproportionately to research quality relative to their token cost, suggesting they should be protected while compressing searches 1 and 2 instead?
