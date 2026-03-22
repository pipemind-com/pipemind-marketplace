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
3. **Be honest about limits.** Some experiments genuinely cannot run with the available tools (missing hardware, paywalled data, domain expertise gaps). Mark these `not-runnable` with a clear explanation rather than attempting unreliable workarounds — a clean "I can't test this" is more valuable than a misleading result.
4. **Stop when you have a decisive answer.** If an early experiment produces strong confirmation or refutation, running the rest wastes time and adds noise. Mark remaining experiments as `skipped` with a pointer to the decisive result.

## Workflow

### Step 0: Check state

Read the hypothesis file. For each experiment, check whether `#### Results` already has content beyond the comment placeholder. Skip experiments that already have results — the file is the checkpoint.

If all experiments already have results, report that experiments are complete and exit.

### Step 1: Run each pending experiment

Work through pending experiments in order. For each experiment type, follow the approach below. After each experiment, if the outcome is `confirmed` or `refuted` with `strong` evidence, skip remaining experiments (see the results template in Step 2 for how to record skipped experiments).

**Code experiments (type: code):**
- Write the code to a temporary file (in `<problem-dir>/tmp/` or inline via Bash)
- Execute via Bash, capturing stdout, stderr, and exit code
- Check for required dependencies first (`which <tool>` or `<tool> --version`) — an experiment that fails because of a missing dependency is not a refutation, it is a setup problem
- Record: what code was run, the full output, and your assessment of the outcome

**Math proof experiments (type: math-proof):**
- Work through the proof step by step, stating each step as a numbered line (premise, transformation, or deduction)
- If the proof succeeds: state the conclusion as "QED" with the full chain
- If you find a counterexample: state it explicitly with the specific values that break the claim
- If the proof requires knowledge or techniques beyond what is available: state the gap precisely

**Evidence-gathering experiments (type: evidence-gathering):**
- Run 2-3 targeted WebSearch queries to find direct evidence
- WebFetch the most relevant sources
- Quote or summarize the key passages, referencing REF IDs from `references.md` where available
- Assess whether the gathered sources support, contradict, or leave the hypothesis unresolved

**Data-analysis experiments (type: data-analysis):**
- Search for available datasets relevant to the hypothesis (WebSearch)
- Fetch accessible data (WebFetch or Bash download)
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

**Outcome:** <confirmed | refuted | inconclusive | not-runnable>

<Detailed narrative of what was done and what was found. Include code outputs, proof steps, quoted evidence, statistics, or error messages. The reader should be able to verify your conclusion from this record alone.>

**Evidence strength:** <strong | moderate | weak>
```

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
