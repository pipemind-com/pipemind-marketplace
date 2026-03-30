# Problem: Token Efficiency of the Scientific Method Researching Skill

## Problem Statement

The scientific-method plugin's `researching` skill orchestrates a multi-phase autonomous research loop (refine problem, generate hypotheses, refine via literature, design experiments, run experiments, draw conclusions, assess). A single research session consumes an excessive number of tokens due to multiplicative agent spawning, redundant skill re-loading, verbose prompt templates, and suboptimal model routing. The goal is to identify concrete, implementable optimizations that substantially reduce token consumption without degrading research quality or the rigor of the scientific method loop.

Quantitative baseline: the 8 skill files total 7,702 words of instructions. A single iteration with the minimum 4 hypotheses loads skill instructions approximately 37,000 words worth across all spawned agents — before accounting for generated content, tool outputs, or file reads. Literature research alone accounts for ~52% of this due to 16+ parallel `researching-literature` invocations per iteration (4 hypotheses x 4 literature searches each).

## Scope

**In scope:**
- Prompt/skill instruction compression and restructuring
- Agent spawning patterns and parallelism strategy
- Model selection (opus vs sonnet vs haiku) per skill
- Hypothesis count calibration
- Literature search redundancy reduction
- File I/O and context loading patterns
- Early termination and short-circuit strategies
- Structural changes to the orchestration architecture

**Out of scope:**
- Changes to the underlying LLM API or pricing
- Modifications to the Claude Code runtime or Task system
- Quality degradation that would compromise scientific rigor
- Removing entire phases of the scientific method

## Key Unknowns

1. What fraction of total tokens comes from skill instruction loading vs. generated content vs. tool I/O?
2. Which optimizations yield the largest token reduction with the least quality impact?
3. Can literature searches be batched or shared across hypotheses without losing coverage?
4. What is the minimum viable hypothesis count that still produces robust research?
5. Which skills genuinely require opus-tier reasoning vs. which can use sonnet or haiku?

## Success Criteria

1. Identify at least 8 distinct, implementable optimizations
2. Each optimization must have a quantified or estimated token savings
3. Combined optimizations should target a 40-60% reduction in total token consumption
4. No optimization should compromise the scientific rigor (falsifiability, honest evidence, independent verification) of the research output
5. Optimizations must be backward-compatible with the existing file-based checkpoint/resume system

## Novelty Required
no

## Constraints

- The plugin is pure markdown/YAML — no build pipeline or runtime dependencies
- Skills are loaded as system prompts by Claude Code; each skill file goes into agent context
- The Task tool spawns sub-agents that each load a full skill file independently
- The checkpoint system relies on hypothesis files as state — changes must preserve this
- The orchestrator must remain idempotent and resumable

## Background

Recent literature on LLM multi-agent token efficiency identifies several established optimization strategies:

**Agent pruning and dynamic elimination**: AgentDropout (REF-001) achieves 21.6% prompt token reduction by dynamically eliminating redundant agents via adjacency matrix optimization, without quality loss. AgentBalance (REF-008) jointly optimizes heterogeneous model selection and communication topology under explicit token budgets.

**Prompt compression**: LLMLingua-2 (REF-005) achieves 2x-5x task-agnostic prompt compression via token classification. 500xCompressor (REF-004) demonstrates extreme compression ratios (6x-480x) while retaining 62-73% capability. Extractive compression often outperforms other methods at up to 10x compression (REF-010).

**Communication optimization**: Optima (REF-002) achieves 2.8x performance gain using <10% of tokens through learned communication policies. Semantic caching with intent-driven dynamic prompt assembly reduces token consumption by 40-60% in production multi-agent systems (REF-009).

**Architecture selection**: Hierarchical architectures occupy the best cost-accuracy Pareto position; hybrid configurations with semantic caching recover 89% of gains at 1.15x cost (REF-007). Dynamic workflow graphs outperform static templates for token efficiency (REF-011).

**Task-aware compression**: AgentCompress (REF-003) routes queries to appropriately sized models based on task complexity, achieving 68.3% cost reduction while preserving 96.2% success rate.

These findings suggest multiple viable optimization paths: reducing agent count, compressing prompts, caching repeated instructions, routing to cheaper models by task complexity, and restructuring the orchestration topology.
