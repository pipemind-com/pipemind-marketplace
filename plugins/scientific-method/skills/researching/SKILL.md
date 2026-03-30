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
model: opus
color: cyan
---

# Researching

Orchestrator for the scientific method loop. The entire loop runs fully autonomously — no operator interaction is required after invocation. It refines the problem, generates hypotheses, researches, experiments, concludes, and loops until the problem is solved or 5 iterations pass.

**CRITICAL: You must execute the ENTIRE pipeline (Phase 1 through Step F) in a single session. After each step completes, immediately proceed to the next step — do NOT produce a text-only response or stop until `findings.md` and `article-abstract.md` have been written. Every intermediate step MUST be followed by a tool call for the next step.**

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
Phase 1 (autonomous):  Refine problem -> problem.md

Phase 2 (autonomous):
  while not solved and iteration < MAX_ITERATIONS:
    A: Generate hypotheses
    B: Refine hypotheses via literature (parallel)
    C-D-E: Design, run, and conclude experiments (parallel, one agent per hypothesis)
    F: Assess -- solved, refine problem and loop, or stop
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
| Any hypothesis with `## Literature` but no `## Conclusion`, and status `pending` or `inconclusive` | Steps C-D-E |
| All hypotheses have conclusions | Step F |
| `findings.md` exists but `article-abstract.md` does not | Write `article-abstract.md` from findings |

A hypothesis is "resolved" if its status is `confirmed` or `refuted`. Hypotheses resolved by literature alone (confirmed/refuted during Step B without needing experiments) skip Steps C-D-E entirely.

**Note:** The orchestrator never reads `experiments/` for resume detection. Hypothesis files are the sole state checkpoint.

---

## Phase 1: Refine Problem (autonomous)

If `problem.md` does not exist, spawn a Task agent to refine the problem:

> You are a problem-refinement agent. Sharpen a rough problem statement into a precise, research-ready formulation. You are fully autonomous — do NOT ask questions or wait for input.
>
> Arguments: slug=`<slug>`, initial-description=`<initial-description>`
>
> Workflow:
> 1. Create `<slug>/references/` directory.
> 2. Launch 2-3 background literature research Tasks (scope, prior work, boundary angles). Each Task should use the inline literature agent prompt from the "Literature Research Prompt" section below.
> 3. Write initial `problem.md` draft using problem-template.md structure (Problem Statement, Scope, Key Unknowns, Success Criteria, Novelty Required: TBD, Constraints, Background: pending).
> 4. Autonomous refinement loop (max 3 iterations): wait for literature agents, update Background section, assess quality (clear research question? testable success criteria? appropriate scope?), refine if needed.
> 5. Auto-determine novelty (yes/no) from literature landscape; update Novelty Required field. Output path to problem.md.

Wait for the Task to complete before proceeding.

After `problem.md` is written, proceed to Phase 2.

---

## Phase 2: Autonomous Research Loop

Track the current iteration by counting completed loops (A through F). A loop is complete when every hypothesis generated in that iteration has a conclusion.

### Step A: Generate hypotheses

```
Skill("generating-hypotheses", args="<problem-dir>")
```

This skill reads prior conclusions and generates fresh hypotheses that build on what was learned. If no new files appear, verify the directory path against `problem.md`, then try once more.

### Step B: Refine hypotheses (parallel)

Find all hypothesis files with status `pending` and no `## Literature` section. Read each file's full content — you will embed it in the Task prompt to avoid redundant reads by sub-agents.

Spawn one Task per hypothesis **in a single response** so they run in parallel. Each Task prompt should be:

> You are a hypothesis-refinement agent. Deepen a hypothesis with targeted literature research.
>
> Hypothesis file: `<hypothesis-file>`
>
> Hypothesis content:
> ```
> <contents of the hypothesis file, read by the orchestrator before spawning>
> ```
>
> Workflow:
> 1. If the hypothesis already has a `## Literature` section, stop (already refined). Read problem.md and references.md for context.
> 2. Build 3 search queries: (a) the claim itself, (b) the underlying mechanism, (c) known counterexamples.
> 3. Spawn 3 parallel literature research Tasks (one per query) using the inline literature agent prompt from the "Literature Research Prompt" section below.
> 4. Run one additional broad literature search to fill recency/landmark gaps.
> 5. Assess literature: identify supporting and challenging sources. Determine if hypothesis is already resolved by prior work.
> 6. Append ## Literature and ## Refined Statement sections to hypothesis file. If resolved, update ## Status to confirmed/refuted.

Wait for all tasks before proceeding. Parallelism here is important because literature research is the slowest step and hypotheses are independent of each other.

After tasks complete, re-read each hypothesis. Some may now have status `confirmed` or `refuted` from literature alone -- those skip Steps C-D-E.

### Steps C-D-E: Design, run, and conclude experiments (parallel)

Find hypotheses that have `## Literature` but no `## Conclusion`, with status `pending` or `inconclusive`. Read each file's full content — you will embed it in the Task prompt to avoid redundant reads by sub-agents.

Spawn one Task per hypothesis **in a single response** so they run in parallel. Each Task completes all three phases (design, run, conclude) sequentially for its hypothesis, avoiding re-reading the hypothesis file between phases.

Each Task prompt should be:

> You are an experiment agent. You will design experiments, run them, and draw conclusions for a single hypothesis — all in one session.
>
> Hypothesis file: `<hypothesis-file>`
>
> Hypothesis content:
> ```
> <contents of the hypothesis file, read by the orchestrator before spawning>
> ```
>
> **Phase 1 — Design experiments:** Read problem.md. If `## Experiments` already exists in the hypothesis, skip to Phase 2. Otherwise, assess what is testable (code, math-proof, evidence-gathering, data-analysis, logical-deduction). Design 1-3 experiments ordered simplest-to-most-involved. Each needs: Title, Type, Approach, Confirms if, Refutes if, Confidence, Publishability potential. Append `## Experiments` section with `#### Results` placeholders to the hypothesis file.
>
> **Phase 2 — Run experiments:** For each experiment with empty `#### Results`, execute it: run code to `experiments/<hypothesis-slug>/exp<N>.<ext>`, work through proofs, gather evidence, or analyze data. Record what actually happened — do not narrate. If an early experiment is decisive, mark remaining as `skipped`. Fill in each `#### Results` with: Artifact (if applicable), Outcome (confirmed/refuted/inconclusive/not-runnable), detailed narrative, Evidence strength (strong/moderate/weak). For confirmed outcomes with a Literature section, run novelty assessment and append Novelty tag.
>
> **Phase 3 — Draw conclusions:** Read all experiment results. Determine aggregate verdict (confirmed/refuted/inconclusive). Connect verdict to problem.md success criteria. Append `## Conclusion` with: Verdict, Reasoning, Implication for the problem, Rigor, Novelty (if confirmed), Follow-up questions. Update `## Status` to match the verdict.

### Step F: Assess -- solved or loop

Read all hypothesis files from this iteration. Check their verdicts.

**Solved condition**: at least one hypothesis has status `confirmed`, and the confirmed claim satisfies the success criteria defined in `problem.md`. Read `problem.md` to verify this -- a confirmed hypothesis that does not address the core question does not count as solved.

**Novelty gate** (check only when solved condition passes): read `problem.md` for the `Novelty required:` field. If the value is `yes` AND the confirmed hypothesis's conclusion contains `**Novelty:** replication`, the problem is NOT solved -- the replication is noted as useful context and the loop continues to the next iteration seeking a novel or incremental contribution.

- **Solved**: write `findings.md` and `article-abstract.md` (formats below) and stop.
- **Not solved, iterations remain**: append a refinement addendum to `problem.md` (format below), then return to Step A. The generating-hypotheses skill will read prior conclusions and the addendum to propose new angles informed by what was ruled out and what was learned.
- **Not solved, MAX_ITERATIONS reached**: write `findings.md` and `article-abstract.md` with outcome "inconclusive after N iterations" and stop.

---

## Literature Research Prompt

When spawning literature research Tasks (in Phase 1, Step B, or anywhere literature search is needed), use this inline prompt instead of referencing the `researching-literature` SKILL.md file. This eliminates redundant skill file reads across parallel agents.

> You are a literature research agent. Search for relevant academic and technical sources on a topic, build a structured bibliography in references.md, and download available articles.
>
> Topic: "<topic>"
> Problem directory: "<problem-dir>"
>
> Workflow:
> 1. Create `references/` dir if needed. Read existing `references.md`; note highest REF-NNN and existing URLs.
> 2. Search using dual-track strategy — use `mcp__mcp-semantic-scholar__search_papers` if available (3-4 calls: 2 recency-track, 1-2 landmark-track, plus citation snowball on top 2-3 papers via `get_references`/`get_citations`), otherwise 4-6 WebSearch queries (2-3 recency-track, 2-3 landmark-track). For recency-track sources, keep only last 3 years; discard older unless they also appear in landmark track. No date filter on landmark track. Deduplicate against existing references.md URLs.
> 3. For each new source (up to 10): apply quality gate (peer-reviewed/conference/technical reports only — drop blog posts, press releases, opinion pieces), assess relevance, extract metadata (title, authors, year, type), write 2-3 sentence relevance summary, attempt PDF download to `references/`.
> 4. Append new entries to `references.md` as: `## REF-NNN: <Title>` with Authors, Year, Type, URL, Downloaded, Relevance fields.
> 5. Report: N new sources added, N skipped, N downloaded.

---

## Refinement Addendum Format

When the loop does not solve the problem and iterations remain, append a new section to `problem.md` using `Edit`:

```
## Refinement Addendum: Iteration N

**Hypotheses tested this iteration:** <list hypothesis titles and their verdicts>

**Key findings:** <2-4 sentences summarizing what was learned -- confirmed mechanisms, refuted approaches, narrowed scope>

**Remaining gaps:** <1-3 specific gaps or open questions that the next iteration should target>

**Suggested direction:** <1-2 sentences recommending what angle the next round of hypotheses should explore, informed by what was ruled out>
```

Addenda accumulate across iterations (Iteration 1, Iteration 2, etc.) and serve as context for `/generating-hypotheses` to produce better-targeted hypotheses in subsequent rounds.

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

---

## article-abstract.md Format

Write `<problem-dir>/article-abstract.md` whenever `findings.md` is written (both solved and inconclusive outcomes). This is a concise, publishable abstract suitable for submission to a conference or journal.

```
# Abstract: <Problem Title>

## Background
<2-3 sentences establishing the research context, the gap in knowledge, and the motivation for the investigation. Draw from problem.md and references.md.>

## Methods
<2-3 sentences describing the methodology: how many hypotheses were tested, what experiment types were used, what literature was consulted. Be specific about the approach without exhaustive detail.>

## Results
<3-5 sentences summarizing the key findings: which hypotheses were confirmed or refuted, the strength of evidence, and any surprising outcomes. Include quantitative results where available.>

## Conclusions
<2-3 sentences stating the main conclusion, its implications for the field, limitations of the study, and directions for future work.>

---
**Keywords:** <5-8 domain-relevant keywords>
**Hypotheses tested:** <N>
**Iterations completed:** <N>
**Outcome:** <solved | inconclusive>
```

Write in formal academic style. Total length: 200-350 words.
