---
name: refining-hypothesis
description: "Deepen a hypothesis with targeted literature research. Use whenever a hypothesis file needs supporting evidence, counterexamples, or a sharpened claim — including after generating-hypotheses or when a user asks to refine, strengthen, or research a specific hypothesis."
user-invocable: true
argument-hint: "path to hypothesis file (e.g., './dark-matter/hypothesis-01.md')"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
model: sonnet
color: yellow
---

# Refining Hypothesis

Takes a hypothesis stub and expands it through targeted literature research. Searches for supporting evidence, counterexamples, and related work, then sharpens the hypothesis into a precise, research-grounded claim ready for experimentation.

The orchestrator runs this skill in parallel across all hypotheses in the current iteration. Each invocation is independent and works on a single hypothesis file.

---

## Arguments

- **Hypothesis file** -- path to `hypothesis-NN.md`

---

## Workflow

### Step 0: Check state (idempotent checkpoint)

Read the hypothesis file. If it already contains a `## Literature` section, this hypothesis has already been refined -- report "Already refined: <hypothesis title>" and stop. The file itself is the checkpoint, so re-running is safe.

Identify the problem directory from the file path (its parent directory). Read `problem.md` to understand the broader research context. Read `references.md` if it exists to know which sources are already in the bibliography -- this prevents the literature agents from re-searching known material.

### Step 1: Build search queries

Derive **3 targeted search queries** from the hypothesis statement and rationale. Each query targets a different angle because a single search would only surface one facet of the literature:

1. **The claim itself** -- look for direct confirmation or refutation of this specific hypothesis
2. **The underlying mechanism** -- what would need to be true for this hypothesis to hold? Search for evidence about that prerequisite
3. **Known counterexamples** -- cases where similar claims have failed or been disproven

### Step 2: Run literature research in parallel

Spawn **3 Task agents in a single response** (one per query). Each Task runs `/researching-literature` targeting the problem directory.

Task prompt format for each:
```
Run /researching-literature with:
- Topic: "<search query>"
- Problem directory: "<absolute path to problem directory>"
```

Wait for all three to complete. Then read the updated `references.md` to identify which new REF IDs were added. Note the relevant ones for this hypothesis.

### Step 2b: Gap assessment and full dual-track search

Read the updated `references.md`. Assess coverage along two dimensions:

- **Recency gap**: are any sources from the last 3 years present? If all found sources are older than 3 years, recent work is underrepresented.
- **Landmark gap**: are any foundational or definitional sources present? If all found sources are very recent, foundational context is missing.

Run one full `/researching-literature` invocation to fill gaps. Always run this step — the three parallel searches in Step 2 are targeted and narrow; this invocation provides broad dual-track coverage.

Task prompt format:
```
Run /researching-literature with:
- Topic: "<broader query derived from the hypothesis topic, not the specific claim>"
- Problem directory: "<absolute path to problem directory>"
```

Wait for the invocation to complete, then read `references.md` again to identify additional REF IDs added.

### Step 3: Sharpen the hypothesis

With the literature findings in hand, assess the hypothesis through these lenses:

- **Supporting sources** -- which REF IDs provide evidence for the claim?
- **Challenging sources** -- which REF IDs complicate, contradict, or narrow the claim?
- **Adjustment needed?** -- does the original statement need narrowing (too broad), broadening (too narrow), or reframing (wrong angle)?
- **Already resolved?** -- if the literature definitively confirms or refutes the hypothesis through prior work, note this clearly. It changes the downstream pipeline: confirmed/refuted hypotheses skip experiment design.

### Step 4: Update hypothesis file

Append to the hypothesis file after the existing content. Preserve the original `## Statement` and `## Rationale` sections unchanged -- they serve as a historical record of the initial thinking.

Use `Edit` to append (never overwrite existing sections).

Append the following sections:

**Literature section:**

```
## Literature

Relevant sources: REF-NNN, REF-NNN, ...

### Supporting evidence
- <finding> (REF-NNN)
- <finding> (REF-NNN)

### Challenges and counterexamples
- <finding that complicates or contradicts this hypothesis> (REF-NNN)
```

**Refined statement section:**

```
## Refined Statement
<Updated hypothesis if the original needed adjustment. If unchanged, write "Unchanged -- original statement holds.">
```

If the hypothesis is already resolved by literature (definitively confirmed or refuted by prior work), add a note explaining this and update `## Status` from `pending` to `confirmed` or `refuted` accordingly. Use `Edit` to change the status line.
