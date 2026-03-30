# Hypothesis 06: Inline Task Prompts Eliminate Redundant Skill File Reads

## Status
refuted

## Statement
Replacing the current pattern of Task agents reading full SKILL.md files ("Read the skill at <path>, then follow its instructions") with inline task prompts that embed only the essential workflow steps directly in the Task prompt will reduce per-task instruction overhead by 60-70% by eliminating frontmatter, examples, and sections irrelevant to the specific invocation.

## Rationale
Each Task agent currently receives a prompt telling it to read a SKILL.md file, which it then loads in full. This means every agent ingests the complete skill including frontmatter, argument parsing, examples, and all workflow steps — even when only a subset applies. For instance, a `running-experiments` task for a code experiment does not need the math-proof or evidence-gathering instructions. Inline prompts tailored to the specific hypothesis and experiment type could carry only the relevant instructions. This mirrors the intent-driven dynamic prompt assembly from REF-009 that reduced token consumption 40-60%.

---
<!-- Sections below are added by downstream skills -->
<!-- refining-hypothesis adds: Literature, Refined Statement -->
<!-- designing-experiments adds: Experiments -->
<!-- running-experiments fills in: Results under each Experiment -->
<!-- drawing-conclusions adds: Conclusion -->

## Experiments

### Experiment 1: Token Count Audit of All Eight SKILL.md Files

- **Type:** code
- **Approach:** Write and run a Python script (no external dependencies beyond `tiktoken` or a character-based approximation) that reads each of the 8 SKILL.md files under `/home/fence/.claude-equine/plugins/marketplaces/pipemind-marketplace/plugins/scientific-method/skills/`. For each file, count: (a) total tokens, (b) tokens in the YAML frontmatter block, (c) tokens in sections that are only relevant to specific experiment types (e.g., `math-proof`, `evidence-gathering` instructions inside `running-experiments`), and (d) tokens in the "Workflow" section that applies universally. Compute the percentage of each file that is type-specific or otherwise non-universal. Then, for a representative invocation (a `running-experiments` call for a single `code`-type experiment), sum the tokens that would be skipped under an inline prompt: frontmatter + irrelevant-type sections + argument-parsing sections. Report: per-file reduction percentage, and the aggregate reduction across all skills loaded in a minimum 4-hypothesis run (37,000-word baseline from problem.md).
- **Confirms if:** The skippable content (frontmatter + type-irrelevant sections) accounts for 60–70% or more of total SKILL.md tokens across a representative invocation set.
- **Refutes if:** Skippable content accounts for fewer than 60% of tokens — meaning the core universal workflow instructions dominate and inline prompts would yield less than the claimed savings.
- **Confidence:** high — token counts are deterministic; the only judgment call is classifying sections as universal vs. type-specific, which is mechanical for structured markdown files.
- **Publishability potential:** low — this is a measurement of a specific plugin's internal structure, not a generalizable empirical result relative to prior art on prompt compression.

#### Results

**Artifact:** experiments/hypothesis-06/exp1.py (initial classifier), experiments/hypothesis-06/exp2.py (corrected bold-header-aware classifier)

**Outcome:** refuted

Two scripts were written and executed. The first (`exp1.py`) split SKILL.md files only at markdown heading levels (`##`, `###`, `####`), producing a 13.8% aggregate skippable estimate for a 4-hypothesis run. However, manual inspection revealed that `running-experiments` embeds its type-specific instructions as bold-text pseudo-headers (`**Math proof experiments (type: math-proof):**`, etc.) inside a single `### Step 1` markdown section — meaning the first classifier incorrectly counted all of Step 1 as universal.

The corrected script (`exp2.py`) added bold-text pseudo-header detection. Results:

**Per-file breakdown (corrected):**

| Skill | Total tok | Frontmatter | Type-specific | Skip% |
|---|---|---|---|---|
| designing-experiments | 1,096 | 125 | 124 | 22.7% |
| drawing-conclusions | 1,542 | 149 | 18 | 10.8% |
| generating-hypotheses | 1,100 | 79 | 23 | 9.3% |
| refining-hypothesis | 1,316 | 130 | 18 | 11.2% |
| refining-problem | 1,348 | 108 | 44 | 11.2% |
| researching | 2,902 | 166 | 45 | 7.3% |
| researching-literature | 1,733 | 212 | 47 | 14.9% |
| running-experiments | 2,368 | 219 | 540 | 32.0% |

**4-hypothesis run aggregate** (1× orchestrator skills, 4× per-hypothesis skills, 12× researching-literature):
- Total loaded tokens: ~51,431
- Skippable (frontmatter + type-specific + argument sections): ~8,857
- **Aggregate skippable: 17.2%**

The running-experiments skill, the one most relevant to the hypothesis, achieves 32% skippable — the highest of all skills — because it genuinely has 4 non-code experiment type subsections (math-proof, evidence-gathering, data-analysis, logical-deduction) that a code-type invocation does not need. But this is the best-case skill.

The dominant overhead in a 4-hypothesis run comes from `researching-literature` (×12 calls, 20,796 tokens loaded), which has only 14.9% skippable content — its workflow instructions are universally applicable regardless of experiment type. Similarly, `drawing-conclusions` (10.8%), `refining-hypothesis` (11.2%), and `generating-hypotheses` (9.3%) contain almost no type-specific content because they do not branch on experiment type at all.

The 60–70% claim implicitly assumed that type-specific branching is the dominant source of SKILL.md token overhead. The measurement shows the opposite: most of each SKILL.md's content is universal workflow logic (step sequences, output format templates, guiding principles) that must be read regardless of invocation context. Frontmatter is a small fraction (7–15%) and actual type-specific sections are even smaller (most skills: 0–2% of total).

Token counts use chars/4 approximation. Actual subword tokenizer counts may vary ±10–15%, but the gap between the measured 17.2% and the claimed 60% is 42+ percentage points — far outside this uncertainty margin. A ±15% swing on total counts would shift the aggregate to ~15–20%, not 60%.

**Evidence strength:** strong — token counts are deterministic; the classification logic was validated by inspecting the actual section content of each skill file; the approximation method applies uniformly so relative proportions are robust.

---

### Experiment 2: Structural Coverage Analysis Per Invocation Type

- **Type:** logical-deduction
- **Approach:** For each of the 5 skills that are invoked per hypothesis (`refining-hypothesis`, `designing-experiments`, `running-experiments`, `drawing-conclusions`, and `researching-literature`), enumerate every numbered step and sub-section in the Workflow. Then, for three representative invocation scenarios — (A) a `code` experiment, (B) an `evidence-gathering` experiment, and (C) a `math-proof` experiment — mark each section as "required" (agent must read it to execute correctly) or "irrelevant" (pertains to a different experiment type or already-satisfied precondition). Count required vs. irrelevant tokens for each scenario. Finally, construct the minimal inline prompt for scenario A by extracting only the required sections and estimate its token count. Compute the reduction ratio: `(original_tokens - inline_tokens) / original_tokens`. Compare this ratio against the 60–70% claim.
- **Confirms if:** The minimal inline prompt for at least 2 of the 3 scenarios is 60–70% smaller than the full SKILL.md, and the required sections alone are sufficient to reproduce the full workflow without behavioral gaps.
- **Refutes if:** The required sections for any scenario exceed 40% of the full file, placing the achievable reduction below 60%, or critical workflow logic is interleaved with type-specific instructions in a way that makes clean extraction impossible.
- **Confidence:** medium — the analysis is systematic but requires judgment about which sections are truly irrelevant vs. conditionally relevant; two reviewers might disagree on borderline sections.
- **Publishability potential:** low — the finding is specific to this plugin's markdown architecture; the methodology (coverage analysis per invocation type) could generalize but is not novel relative to prior art on task-aware prompt compression (REF-003, REF-009).

#### Results

**Outcome:** skipped

Experiment 1 produced a decisive refuted result with strong evidence. The aggregate skippable content across a 4-hypothesis run is 17.2%, far below the 60% threshold. Further structural analysis will not change this finding — the dominant skills by token load (researching-literature, drawing-conclusions, refining-hypothesis) contain no type-specific branching and thus cannot yield the claimed savings.

---

### Experiment 3: Synthetic Inline Prompt Construction and Token Differential

- **Type:** code
- **Approach:** For the `running-experiments` skill (the largest skill by word count and the one with the most type-specific branching), manually construct an inline prompt for a `code`-type experiment invocation. The inline prompt should contain: the essential workflow steps for code experiments only, the output format specification, and the checkpoint/file-write instructions — but omit frontmatter, argument-parsing instructions, non-code experiment type sections, and all examples. Use a script to count tokens in (a) the full `running-experiments` SKILL.md, (b) the constructed inline prompt, and (c) a Task-tool invocation wrapper that embeds the inline prompt (i.e., `"Run this experiment: <inline_prompt>\n\nHypothesis: <hypothesis_content>"`). Report the three token counts and the reduction ratios. Then repeat for `designing-experiments` and `drawing-conclusions` to check consistency of the savings estimate across skills.
- **Confirms if:** The inline prompt for `running-experiments` is 60–70% smaller than the full SKILL.md, and the same ratio holds within ±10 percentage points for the other two skills — supporting the claim that 60–70% is a reliable cross-skill estimate.
- **Refutes if:** The inline prompt savings vary widely across skills (e.g., 70% for one and 35% for another), indicating the 60–70% figure is not a reliable aggregate estimate, even if it holds for individual cases.
- **Confidence:** high — token counts are deterministic once the inline prompt is constructed; the main uncertainty is whether the constructed inline prompt is truly complete (covers all required logic).
- **Publishability potential:** medium — constructing and empirically validating minimal inline prompts as a compression technique for multi-agent skill-file architectures could contribute a concrete implementation pattern to the literature on intent-driven prompt assembly (REF-009), particularly for checkpoint-based orchestration systems.

#### Results

**Outcome:** skipped

Experiment 1 produced a decisive refuted result with strong evidence. Constructing synthetic inline prompts for running-experiments and two other skills would not alter the aggregate finding: the savings from type-specific pruning in running-experiments (~32%) are diluted to ~17% across the full run because most skills have no type-specific branching to prune.

---

## Conclusion

**Verdict:** refuted

**Reasoning:** Experiment 1 produced a strong-evidence refuted outcome that is dispositive on its own. Deterministic token counts across all 8 SKILL.md files showed that aggregate skippable content — frontmatter plus type-specific sections — amounts to only 17.2% of tokens loaded in a representative 4-hypothesis run, against the claimed 60–70%. The 42+ percentage-point gap is far outside the ±10–15% approximation uncertainty. Experiments 2 and 3 were correctly skipped because no structural analysis or synthetic prompt construction could recover savings from skills that contain no type-specific branching to prune: `researching-literature` (×12 calls, 40% of all loaded tokens) yields only 14.9% skippable, and `drawing-conclusions`, `refining-hypothesis`, and `generating-hypotheses` are each below 12%.

**Implication for the problem:** Inline task prompt assembly targeting type-specific section elimination does not constitute a viable optimization under the problem's success criteria. The 40–60% combined reduction target requires addressing where tokens actually accumulate: the universal workflow logic in high-frequency skills (especially `researching-literature`) and total call volume — not type-specific branching. This rules out one candidate optimization from the search space and sharpens focus toward strategies with higher leverage: reducing the number of `researching-literature` invocations per iteration (literature search batching/sharing across hypotheses, key unknown #3 in problem.md), applying prompt compression to the universal workflow sections of high-frequency skills, or model-routing `researching-literature` calls to a smaller model (problem.md key unknowns #2 and #5). The savings from inline prompts are real but small (~17%), so this approach might still be worth implementing as one component of a combined optimization, but it cannot anchor a strategy that claims 60–70% reduction.

**Rigor:** The methodology is sound: token counts are deterministic given the character/4 approximation, the classification logic was validated against the actual section content of each skill file, and the approximation method applies uniformly so relative proportions are robust. The main limitation is that subword tokenizer counts could differ from the character-based approximation by ±10–15%, but this does not affect the conclusion — the 42-point gap to the 60% threshold is structurally robust. The classification of "type-specific" vs. "universal" sections required judgment for borderline cases, but this judgment was conservative (generous toward the hypothesis): even under lenient classification, running-experiments — the best-case skill — reached only 32%.

**Follow-up questions:**
- Can `researching-literature` calls be batched or shared across hypotheses (e.g., one literature search per research topic rather than 4×4=16)? This is the highest-leverage target: 40% of total instruction tokens with a call multiplier of ×12.
- What fraction of `researching-literature`'s 1,733-token universal workflow is actually necessary for the median literature search call, and could LLMLingua-style extractive compression reduce it without loss of coverage quality?
- Would routing `researching-literature` (and other sub-1,500-token skills) to haiku rather than sonnet preserve result quality, given that the task is structured information retrieval rather than deep reasoning?
- Is there a minimum viable literature search count per hypothesis below 4 that still produces acceptable bibliographic coverage — reducing call volume rather than per-call token cost?
