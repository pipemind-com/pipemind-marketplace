---
name: refining-problem
description: "Refine a problem statement into a research-ready formulation. Creates problem.md through autonomous self-refinement backed by literature research."
user-invocable: false
argument-hint: "problem-slug and initial description (e.g., 'dark-matter \"What accounts for missing mass in galaxy rotation?\"')"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Task
model: sonnet
color: green
---

# Refining Problem

Sharpen a rough problem statement into a precise, research-ready formulation through autonomous self-refinement backed by literature research. Produce `problem.md` as the source of truth for all downstream steps.

**CRITICAL: This skill is fully autonomous. You MUST NOT ask questions, wait for user input, or request clarification. You have all the information you need: the problem slug and the initial description. Infer everything else from the description and from literature findings. Proceed through every step without stopping.**

The skill writes an initial draft from the provided description, uses literature findings to assess and improve it, and auto-determines novelty requirements based on the literature landscape.

## Arguments

- **Problem slug** -- kebab-case directory name (required)
- **Initial description** -- rough problem statement (required on first run, optional when resuming)

## Workflow

### Step 0: Setup

Create the problem directory and references subdirectory:
```
bash -c "mkdir -p <problem-slug>/references"
```

If `problem.md` already exists, read it and skip to Step 3 for assessment. The file is the checkpoint.

### Step 1: Launch background research agents

Immediately launch **2-3 background Task agents** (run_in_background: true) to map the problem space. Focus each on a different angle:

- **Scope agent**: Search for canonical definitions, existing frameworks, or established formulations of this problem. Run `/researching-literature` with the topic and problem directory.
- **Prior work agent**: Search for existing solutions, known attempts, and related work. Run `/researching-literature`.
- **Boundary agent**: Search for edge cases, known failure modes, and adjacent problems. Run `/researching-literature`.

Launch all three in a single response.

### Step 2: Write initial problem.md draft

Using the initial description, write `<problem-slug>/problem.md` using the structure in `references/problem-template.md`. Fill in each section based on what can be inferred from the initial description:

- **Problem Statement**: expand the initial description into 1-3 precise paragraphs
- **Scope**: infer in-scope and out-of-scope boundaries from the description
- **Key Unknowns**: identify the core unknowns implied by the description
- **Success Criteria**: derive testable success criteria directly from the initial description
- **Novelty Required**: set to `TBD` (determined in Step 4)
- **Constraints**: note any constraints implied by the description
- **Background**: set to `Pending literature review` (filled in Step 3)

### Step 3: Autonomous refinement loop (max 3 iterations)

Wait for background literature agents from Step 1 to complete. Read `references.md` for their findings.

For each refinement iteration (up to 3):

**3a. Update background section**: Synthesize literature findings into the `## Background` section of `problem.md` using `Edit`. Incorporate relevant definitions, prior work, and known boundary conditions discovered by the research agents.

**3b. Assess problem definition quality**: Evaluate `problem.md` against three criteria:
- **Clear research question**: Does the Problem Statement articulate a specific, answerable question -- not vague, compound, or circular?
- **Testable success criteria**: Are the Success Criteria specific enough that an experiment could confirm or refute them?
- **Appropriate scope**: Is the scope neither too broad (would take unbounded effort) nor too narrow (trivially answerable)?

**3c. Decision**:
- If all three criteria pass: proceed to Step 4.
- If any criterion fails and iterations remain: identify the specific deficiency, refine `problem.md` to address it, launch 1-2 additional targeted `/researching-literature` Tasks to fill knowledge gaps related to the deficiency, wait for results, and loop back to 3a.
- If 3 iterations pass without all criteria met: proceed to Step 4 with the best available formulation. Note any remaining deficiencies in the Background section.

### Step 4: Auto-determine novelty and finalize

Assess the novelty landscape from literature findings in `references.md`:
- If existing published solutions substantially cover the problem space (multiple papers addressing the same question with confirmed results): set `Novelty required: yes` -- replications of known work will not satisfy the research goal.
- If the space is largely unexplored (few or no papers directly addressing the question, or existing work is preliminary/inconclusive): set `Novelty required: no` -- confirming or replicating findings is a valid outcome.

Update the `Novelty required:` field in `problem.md` from `TBD` to `yes` or `no` using `Edit`. Once set, this field is immutable for the duration of the research session.

Output the path to `problem.md` and confirm the autonomous loop is ready to proceed.

## References

- `references/problem-template.md` -- Structure template for problem.md output
