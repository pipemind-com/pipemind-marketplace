---
name: running-experiments
description: "Execute experiments from a hypothesis file — run code, work through proofs, gather evidence, analyze data, and write results back. Use this skill whenever a hypothesis file has designed experiments with empty Results sections, when the user says 'run the experiments', 'test the hypothesis', 'try it', or 'execute the experiments', or when the next step in a scientific-method workflow is to actually attempt the experiments."
user-invocable: true
argument-hint: "path to hypothesis file (e.g., './dark-matter/hypothesis-01.md')"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebSearch
  - WebFetch
  - mcp__mcp-semantic-scholar__search_papers
  - mcp__mcp-semantic-scholar__get_paper
  - mcp__mcp-semantic-scholar__get_references
  - mcp__mcp-semantic-scholar__get_citations
model: opus
color: red
---

# Running Experiments

This is the "actually try" step in the scientific method workflow. The goal is genuine execution — running code, working through math, fetching real data — not describing what would happen. Every result must reflect what was actually observed, because the entire research loop depends on honest evidence to decide whether a hypothesis holds.

## Arguments

- **Hypothesis file** — path to `hypothesis-NN.md`

## Guiding Principles

These principles exist because the research loop only works when experiment results are trustworthy. A fabricated or simulated result poisons every downstream decision.

1. **Execute, don't narrate.** Run the code. Work the proof. Fetch the data. The difference between this skill and a planning skill is that this one produces real artifacts and real output. If you find yourself writing "this would likely show..." you've slipped into narration.
2. **Record what happened, not what was expected.** Confirmation bias is the enemy of good research. Write down the actual output, even when it surprises you.
3. **Be honest about limits.** Some experiments genuinely cannot run with the available tools (missing hardware, missing software dependencies, paywalled data, domain expertise gaps). Mark these `not-runnable` with a clear explanation rather than attempting unreliable workarounds — a clean "I can't test this" is more valuable than a misleading result.
4. **Stop when you have a decisive answer.** If an early experiment produces strong confirmation or refutation, running the rest wastes time and adds noise. Mark remaining experiments as `skipped` with a pointer to the decisive result.

## Workflow

### Step 0: Check state

Read the hypothesis file. For each experiment, check whether `#### Results` already has content beyond the comment placeholder. Skip experiments that already have results — the file is the checkpoint.

If all experiments already have results, report that experiments are complete and exit.

### Step 1: Run each pending experiment

Work through pending experiments in order. For each experiment type, follow the approach below. After each experiment, if the outcome is `confirmed` or `refuted` with `strong` evidence, skip remaining experiments (see the results template in Step 2 for how to record skipped experiments).

**Code experiments (type: code):**
- Write code to `<problem-dir>/experiments/<hypothesis-slug>/exp<N>.<ext>` where `<N>` is the next globally sequential integer for that directory (check existing files to determine it), and `<ext>` matches the language (`.py`, `.sh`, `.js`, `.csv`, etc.). Create the directory if it does not exist. Numbers never reset and existing files are never overwritten.
- The slug is derived from the hypothesis filename (e.g., `hypothesis-01.md` → `hypothesis-01`).
- Execute via Bash, capturing stdout, stderr, and exit code.
- Check for required dependencies first (`which <tool>` or `<tool> --version`). A missing dependency means outcome `not-runnable`, not a refutation of the hypothesis.
- **Safety invariant**: experiment code must not write files outside `<problem-dir>/` and must not spawn persistent background processes. If an experiment requires either, record it as `not-runnable` with an explanation instead of running it.
- **Failed experiments**: if execution fails (non-zero exit, import error, syntax error), keep the artifact file — it is evidence, not a success signal. Record the full error output and artifact path in Results. Use outcome `inconclusive` or `not-runnable` as appropriate. A failure is not evidence against the hypothesis unless the failure itself is informative.

**Math proof experiments (type: math-proof):**
- Work through the proof step by step, stating each step as a numbered line (premise, transformation, or deduction)
- If the proof succeeds: state the conclusion as "QED" with the full chain
- If you find a counterexample: state it explicitly with the specific values that break the claim
- If the proof requires knowledge or techniques beyond what is available: state the gap precisely

**Evidence-gathering experiments (type: evidence-gathering):**
- If `search_papers` is available, prefer it for academic evidence queries — it returns structured results with citation counts and open-access links. Use `get_references`/`get_citations` to follow citation chains from key papers. Fall back to WebSearch for non-academic sources or if MCP tools are unavailable.
- Otherwise run 2-3 targeted WebSearch queries to find direct evidence
- WebFetch the most relevant sources (or use metadata from MCP results directly)
- Quote or summarize the key passages, referencing REF IDs from `references.md` where available
- Assess whether the gathered sources support, contradict, or leave the hypothesis unresolved

**Data-analysis experiments (type: data-analysis):**
- Search for available datasets relevant to the hypothesis (use `search_papers` if available to find papers with linked datasets, otherwise WebSearch)
- Fetch accessible data (WebFetch or Bash download). Save fetched datasets and analysis scripts to `<problem-dir>/experiments/<hypothesis-slug>/` using the same `exp<N>.<ext>` naming convention.
- Analyze with Bash for structured data (CSV, JSON, etc.) — use Grep to search through local files when relevant
- Report key statistics, patterns, or anomalies and explain what they mean for the hypothesis

**Logical-deduction experiments (type: logical-deduction):**
- State all premises explicitly, numbered
- Work through the deductive chain step by step
- Identify where the argument is valid, where it requires additional assumptions, and where it breaks
- Conclude: does the deduction confirm the hypothesis, refute it, or reveal a gap?

### Step 2: Write results

For each completed experiment, fill in the `#### Results` section using Edit. Do not modify the experiment design above it.

**Results template:**
```
#### Results

**Artifact:** experiments/<hypothesis-slug>/exp<N>.<ext>

**Outcome:** <confirmed | refuted | inconclusive | not-runnable>

<Detailed narrative of what was done and what was found. Include code outputs, proof steps, quoted evidence, statistics, or error messages. The reader must be able to reproduce the methodology from this record alone. Report all outcomes honestly, including negative or unexpected results. For quantitative data, include appropriate statistical context (e.g., sample size, confidence interval, p-value). Distinguish between what was directly observed and what was inferred.>

**Evidence strength:** <strong | moderate | weak>
```

The `**Artifact:**` line is only included when the experiment wrote files to `experiments/`. Math-proof, logical-deduction, and evidence-gathering experiments that produce no persistent artifact omit this line.

Evidence strength guidance:
- **strong** — the result is decisive and reproducible (code ran with clear output, proof is complete, multiple independent sources agree)
- **moderate** — the result points in a direction but has caveats (partial data, proof with assumptions, single source)
- **weak** — the result is suggestive but not conclusive (indirect evidence, incomplete analysis, significant uncertainty)

**For skipped experiments** (when an earlier experiment was decisive):
```
#### Results

**Outcome:** skipped

Experiment <N> produced a decisive <confirmed|refuted> result with strong evidence. Further testing is unnecessary.
```

### Step 3: Novelty assessment

**Only for experiments with `confirmed` outcome where the hypothesis file contains a `## Literature` section.**

Run 1-2 targeted searches comparing the confirmed result against existing published work (prefer `search_papers` if available, otherwise WebSearch). Search for the specific method, finding, or mechanism confirmed — not general background.

If the literature section has fewer than 3 sources, this search is especially important to avoid false novelty claims.

After the search, append a `**Novelty:**` tag immediately after `**Evidence strength:**` in the Results section:

```
**Novelty:** <novel | incremental | replication> — <one sentence of rationale, citing any newly discovered prior art by URL>
```

Novelty scale:
- `novel` — no prior art found for this specific result
- `incremental` — extends or improves on prior work
- `replication` — reproduces known findings

The `replication` tag signals the orchestrator that this result may not satisfy success criteria when `Novelty required: yes` is in `problem.md`.

If no `## Literature` section exists in the hypothesis file, skip this step entirely.
