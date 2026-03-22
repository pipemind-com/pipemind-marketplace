---
name: designing-experiments
description: "This skill should be used when the user asks to 'design experiments', 'plan tests for a hypothesis', 'create experiment paths', or 'figure out how to test this hypothesis'. Designs 1–3 experiment paths to verify or falsify a hypothesis and writes them into the hypothesis file."
user-invocable: true
argument-hint: "path to hypothesis file (e.g., './dark-matter/hypothesis-01.md')"
allowed-tools:
  - Read
  - Write
  - Edit
model: sonnet
color: cyan
---

# Designing Experiments

Read a refined hypothesis and design 1–3 distinct experiment paths to verify or falsify it. Each experiment specifies what to do, what result confirms the hypothesis, and what result refutes it.

Design experiments to be as executable as possible with available tools. Prefer experiments that can be attempted now -- code to run, math to prove, data to gather, evidence to find -- over experiments that require external resources unavailable to the research agent.

---

## Arguments

- **Hypothesis file** -- path to `hypothesis-NN.md`

---

## Workflow

### Step 0: Check state

Read the hypothesis file. If it already contains a `## Experiments` section with content, skip -- already designed. The file is the checkpoint.

If `## Status` is already `confirmed` or `refuted` (set by literature review), skip experiment design. Note that the hypothesis was resolved by prior work and no experiments are needed.

Read `problem.md` in the parent directory for constraints and success criteria.

### Step 1: Assess what is testable

From the refined hypothesis statement (or original if not yet refined), determine:
- What **type** of evidence would prove or disprove the claim
- What tools are available: Bash (run code), WebSearch/WebFetch (gather evidence), mathematical reasoning, logical deduction, data analysis
- What the minimum viable test looks like -- the simplest thing that would produce a decisive signal

**Experiment types:**
- `code` -- write and run code to test the claim
- `math-proof` -- work through a formal or informal proof or derivation
- `evidence-gathering` -- search for empirical evidence, studies, or data online
- `data-analysis` -- fetch a dataset and analyze it
- `logical-deduction` -- reason from stated premises to a conclusion

### Step 2: Design 1–3 experiments

Order experiments from **simplest and most decisive to most involved**:

- **1 experiment**: one clean test is sufficient
- **2 experiments**: two independent approaches cross-validate
- **3 experiments**: the hypothesis is complex or no single test is decisive

Each experiment must specify:
- **Title**: concise name (5–8 words)
- **Type**: one of the types listed above
- **Approach**: precise narrative of what to do, described with enough detail that an agent can execute without making behavioral decisions
- **Confirms if**: specific result that would support the hypothesis
- **Refutes if**: specific result that would contradict the hypothesis
- **Confidence**: how decisive a positive/negative result would be (high / medium / low) -- be honest about limitations

### Step 3: Write experiment designs into hypothesis file

Append to the hypothesis file after the existing content:

```
## Experiments

### Experiment 1: <Title>

- **Type:** <type>
- **Approach:** <precise narrative of what to do>
- **Confirms if:** <expected result if the hypothesis is true>
- **Refutes if:** <expected result if the hypothesis is false>
- **Confidence:** <high | medium | low>

#### Results
<!-- To be filled by running-experiments -->

---

### Experiment 2: <Title>
...
```

Use `Edit` to append -- never overwrite existing content.
