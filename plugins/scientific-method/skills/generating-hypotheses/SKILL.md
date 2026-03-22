---
name: generating-hypotheses
description: "Generate testable hypotheses from a problem statement and prior conclusions. Writes stub hypothesis files."
user-invocable: true
argument-hint: "path to problem directory (e.g., './dark-matter')"
allowed-tools:
  - Read
  - Write
  - Glob
model: opus
color: yellow
---

# Generating Hypotheses

Reads a refined problem statement and any conclusions from prior iterations, then generates 2-5 new testable hypotheses. Each hypothesis gets its own stub file for downstream skills (refining, experimentation, conclusion).

Hypothesis files accumulate across iterations -- numbering never resets.

Do NOT use this skill to revise existing hypotheses. Use `/refining-hypothesis` instead.

---

## Arguments

- **Problem directory** -- path to the directory containing `problem.md`

---

## Workflow

### Step 0: Check state

Glob `<problem-dir>/hypothesis-*.md`. If existing files all have `## Status` of `pending` (none concluded yet), warn: hypotheses already exist that haven't been tested. Ask whether to proceed or abort.

If `<problem-dir>/problem.md` does not exist, stop with an error -- problem must be refined first via `/refining-problem`.

### Step 1: Read problem context

Read `<problem-dir>/problem.md`. This is the sole source of truth for what is being investigated.

### Step 2: Read prior iteration context

For each existing `hypothesis-*.md`, read:
- `## Statement` (what was claimed)
- `## Status` (confirmed / refuted / inconclusive / pending)
- `## Conclusion` section if present (what was learned)

Build a summary of what has already been tried:
- **Confirmed** -- do not re-propose
- **Refuted** -- do not re-propose; note what was ruled out
- **Inconclusive** -- may re-propose with narrower or different framing

### Step 3: Determine next hypothesis numbers

Count existing hypothesis files. New hypotheses continue from the next number. If `hypothesis-03.md` is the last file, new hypotheses start at `hypothesis-04.md`.

### Step 4: Generate 2-5 new hypotheses

Synthesize the problem statement, success criteria, constraints, and prior conclusions into **2-5 new, distinct, testable hypotheses**.

**Each hypothesis must:**
- Be a clear, falsifiable claim that can be confirmed or refuted through experiment
- Contribute meaningfully to solving the problem if true (not a trivial observation)
- Not duplicate any previously confirmed or refuted hypothesis
- Build on inconclusive prior results by narrowing scope or changing approach

**The set as a whole must:**
- Cover different mechanisms or explanations (not variations of the same idea)
- Span a range of confidence levels -- include likely and less-obvious explanations
- Be ordered from most to least promising based on available evidence

**Quality check each hypothesis:**
- Specific enough to be experimentally testable or logically provable?
- Bounded -- avoids solving the entire problem in one claim?
- Respects constraints and scope from `problem.md`?

### Step 5: Write hypothesis stub files

For each new hypothesis, write `<problem-dir>/hypothesis-NN.md` (two-digit zero-padded):

```
# Hypothesis NN: <Concise title (5-10 words)>

## Status
pending

## Statement
<1-2 sentences: a precise, falsifiable claim>

## Rationale
<2-3 sentences: why this hypothesis is worth testing -- connection to the problem, prior knowledge, or what prior conclusions suggest>

---
<!-- Sections below are added by downstream skills -->
<!-- refining-hypothesis adds: Literature, Refined Statement -->
<!-- designing-experiments adds: Experiments -->
<!-- running-experiments fills in: Results under each Experiment -->
<!-- drawing-conclusions adds: Conclusion -->
```

Only write files that do not already exist. Skip existing hypothesis numbers (idempotent).

### Step 6: Report

Output a summary table:

| File | Title | Rationale (one line) |
|------|-------|---------------------|
| hypothesis-NN.md | ... | ... |

State total hypotheses in the problem directory (existing + new) and suggest running `/refining-hypothesis` next.
