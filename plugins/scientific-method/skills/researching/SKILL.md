---
name: researching
description: "Run a full scientific method research loop: refine problem, generate hypotheses, research literature, experiment, conclude, and iterate until solved. Use this skill whenever someone wants to investigate a question, debug a mysterious issue, explore a hypothesis, do a literature review, or solve any open-ended problem methodically — even if they don't say 'research' explicitly."
user-invocable: true
argument-hint: "problem-slug and initial description (e.g., 'dark-matter \"What accounts for missing mass in galaxy rotation?\"')"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
  - Task
  - AskUserQuestion
model: opus
color: cyan
---

# Researching

Orchestrator for the scientific method loop. The operator participates only in Phase 1 (problem refinement). After that, the loop runs fully autonomously — generating hypotheses, researching, experimenting, concluding, and looping until the problem is solved or 5 iterations pass.

**Idempotent**: re-running resumes where it left off by reading file state, so no work is duplicated and interrupted sessions recover cleanly.

---

## Arguments

- **Problem slug** -- kebab-case directory name (required)
- **Initial description** -- rough problem statement (required on first run, optional when resuming)

---

## Constants

- **MAX_ITERATIONS**: 5

---

## Loop Overview

```
Phase 1 (operator involved):  Refine problem -> problem.md

Phase 2 (autonomous):
  while not solved and iteration < MAX_ITERATIONS:
    A: Generate hypotheses
    B: Refine hypotheses via literature (parallel)
    C: Design experiments (parallel)
    D: Run experiments (parallel)
    E: Draw conclusions (parallel)
    F: Assess -- solved or loop
```

---

## Step 0: Resume Detection

Read the problem directory to figure out where to pick up. This matters because the loop can be interrupted at any point and must resume without redoing work.

Use `Glob` for `<slug>/hypothesis-*.md`, then `Read` each file to check section presence and `## Status` values. Apply the first matching rule:

| Condition | Resume at |
|-----------|-----------|
| No `problem.md` | Phase 1 |
| No `hypothesis-*.md` files | Step A |
| Any hypothesis with status `pending` and no `## Literature` | Step B |
| Any hypothesis with `## Literature`, no `## Experiments`, and status `pending` or `inconclusive` | Step C |
| Any hypothesis with `## Experiments` containing an empty `#### Results` and status not resolved | Step D |
| Any hypothesis with results but no `## Conclusion` | Step E |
| All hypotheses have conclusions | Step F |

A hypothesis is "resolved" if its status is `confirmed` or `refuted`. Hypotheses resolved by literature alone (confirmed/refuted during Step B without needing experiments) skip Steps C-D-E entirely.

**Note:** The orchestrator never reads `experiments/` for resume detection. Hypothesis files are the sole state checkpoint.

---

## Phase 1: Refine Problem (operator involved)

If `problem.md` does not exist, invoke the refining-problem skill:

```
Skill("refining-problem", args="<slug> <initial-description>")
```

After `problem.md` is confirmed, proceed to Phase 2. This is the last operator interaction -- everything after runs autonomously.

---

## Phase 2: Autonomous Research Loop

Track the current iteration by counting completed loops (A through F). A loop is complete when every hypothesis generated in that iteration has a conclusion.

### Step A: Generate hypotheses

```
Skill("generating-hypotheses", args="<problem-dir>")
```

This skill reads prior conclusions and generates fresh hypotheses that build on what was learned. If no new files appear, verify the directory path against `problem.md`, then try once more.

### Step B: Refine hypotheses (parallel)

Find all hypothesis files with status `pending` and no `## Literature` section.

Spawn one Task per hypothesis **in a single response** so they run in parallel. Each Task prompt should be:

> Read the skill at `<path-to-refining-hypothesis/SKILL.md>`, then follow its instructions to refine the hypothesis at `<hypothesis-file>`.

Wait for all tasks before proceeding. Parallelism here is important because literature research is the slowest step and hypotheses are independent of each other.

After tasks complete, re-read each hypothesis. Some may now have status `confirmed` or `refuted` from literature alone -- those skip Steps C-D-E.

### Step C: Design experiments (parallel)

Find hypotheses that have `## Literature` but no `## Experiments`, with status `pending` or `inconclusive`.

Spawn one Task per hypothesis in a single response:

> Read the skill at `<path-to-designing-experiments/SKILL.md>`, then follow its instructions to design experiments for the hypothesis at `<hypothesis-file>`.

### Step D: Run experiments (parallel)

Find hypotheses that have `## Experiments` with at least one empty `#### Results` section and status not yet resolved.

Spawn one Task per hypothesis in a single response:

> Read the skill at `<path-to-running-experiments/SKILL.md>`, then follow its instructions to run experiments for the hypothesis at `<hypothesis-file>`.

### Step E: Draw conclusions (parallel)

Find hypotheses that have experiment results but no `## Conclusion`.

Spawn one Task per hypothesis in a single response:

> Read the skill at `<path-to-drawing-conclusions/SKILL.md>`, then follow its instructions to draw conclusions for the hypothesis at `<hypothesis-file>`.

### Step F: Assess -- solved or loop

Read all hypothesis files from this iteration. Check their verdicts.

**Solved condition**: at least one hypothesis has status `confirmed`, and the confirmed claim satisfies the success criteria defined in `problem.md`. Read `problem.md` to verify this -- a confirmed hypothesis that does not address the core question does not count as solved.

**Novelty gate** (check only when solved condition passes): read `problem.md` for the `Novelty required:` field. If the value is `yes` AND the confirmed hypothesis's conclusion contains `**Novelty:** replication`, the problem is NOT solved -- the replication is noted as useful context and the loop continues to the next iteration seeking a novel or incremental contribution.

- **Solved**: write `findings.md` (format below) and stop.
- **Not solved, iterations remain**: return to Step A. The generating-hypotheses skill will read prior conclusions and propose new angles informed by what was ruled out.
- **Not solved, MAX_ITERATIONS reached**: write `findings.md` with outcome "inconclusive after N iterations" and report to the operator.

---

## findings.md Format

Write `<problem-dir>/findings.md` when the loop exits. Use this structure:

**Header**: `# Research Findings: <Problem Title>`

**Sections** (in order):

1. **Outcome** -- either "solved" or "inconclusive after N iterations"
2. **Solution** -- (only if solved) summary of the confirmed hypothesis and how it satisfies the success criteria
3. **What was ruled out** -- refuted hypotheses and what they tell us about the problem space
4. **Open questions** -- unresolved questions and follow-up directions raised by the research
5. **Iterations completed** -- N iterations, M hypotheses tested
6. **Confirmed hypotheses** -- list with titles and one-line summaries
7. **Refuted hypotheses** -- list with titles and one-line summaries of what was ruled out
8. **Publishability Assessment** -- evaluates three dimensions and concludes with a publishability verdict

### Publishability Assessment Content

Evaluate three dimensions in order:

1. **Rigor** -- whether the methodology, evidence collection, and statistical treatment meet publication-grade standards
2. **Novelty** -- whether the results advance beyond the literature: `novel` (no prior art), `incremental` (extends prior work), or `replication` (reproduces known findings). Note incremental contributions as potentially suitable for workshop papers or short communications; fully novel contributions may warrant a full paper
3. **Significance** -- whether the findings address a meaningful question with practical or theoretical impact

Each dimension receives a brief assessment (2-4 sentences). The section concludes with a verdict: `publishable`, `publishable-with-revisions`, or `not-publishable`. For `publishable-with-revisions` and `not-publishable` verdicts, include 2-3 concrete, actionable improvement suggestions (e.g., "gather additional data on X", "compare results against <method> from REF-NNN", "narrow scope to <specific aspect> where the contribution is clearest").

This section appears in findings.md for both solved and inconclusive outcomes.
