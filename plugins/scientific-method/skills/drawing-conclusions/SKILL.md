---
name: drawing-conclusions
description: "Synthesize experiment results for a hypothesis into a verdict: confirmed, refuted, or inconclusive. Writes conclusion into the hypothesis file. Use this skill after running-experiments has filled in results, or whenever the user wants to evaluate whether a hypothesis held up, assess experiment outcomes, or decide what a research iteration means for the original problem."
user-invocable: true
argument-hint: "path to hypothesis file (e.g., './dark-matter/hypothesis-01.md')"
allowed-tools:
  - Read
  - Write
  - Edit
model: sonnet
color: purple
---

# Drawing Conclusions

This is the judgment step of the scientific method loop. After experiments have run and produced results, this skill reads the evidence honestly and delivers a verdict. The goal is intellectual honesty: a confirmed hypothesis that was never seriously challenged is worthless, and a refuted hypothesis that narrows the search space is valuable. The verdict must follow from the evidence, not from what would be convenient.

---

## Arguments

- **Hypothesis file** -- path to `hypothesis-NN.md`

---

## Workflow

### Step 0: Check state

Read the hypothesis file. If it already contains a `## Conclusion` section with a verdict, stop -- this hypothesis has already been concluded. The file is the checkpoint.

### Step 1: Read and assess all results

For each experiment in the hypothesis file, extract:
- **Outcome**: confirmed / refuted / inconclusive / not-runnable / skipped
- **Evidence strength**: strong / moderate / weak
- **Key finding**: one sentence capturing what was actually observed

Then determine the aggregate verdict. The reasoning here matters more than a mechanical formula, but these principles guide the judgment:

- **Confirmed**: The weight of evidence supports the hypothesis. At least one experiment produced a confirmed outcome with strong evidence, and nothing contradicts it with comparable strength. Multiple weak confirmations without any strong signal do not add up to a strong confirmation -- note that honestly.
- **Refuted**: A single strong counterexample is enough to refute a hypothesis, even if other experiments seemed to support it. This asymmetry is fundamental to the scientific method -- it is easier to disprove than to prove. If the refuting evidence is moderate rather than strong, weigh it against any confirming evidence and explain the tension.
- **Inconclusive**: The honest answer when the evidence does not clearly point either way. This includes: mixed results with no dominant signal, all-weak evidence in any direction, all experiments not-runnable or skipped, or contradictory strong results that cannot be reconciled. Inconclusive is not a failure -- it is information about what the next iteration needs to address.

If every experiment was skipped or not-runnable, the verdict is inconclusive with a clear note that the hypothesis could not be tested with available tools.

### Step 2: Connect the verdict to the problem

Read `problem.md` in the parent directory. The conclusion is only useful if it feeds back into the original problem, so ground the verdict in the problem's success criteria:

- **If confirmed**: Does this hypothesis, as confirmed, satisfy the problem's success criteria? Fully, partially, or as one component of a larger solution? Be precise about what has actually been established versus what remains assumed.
- **If refuted**: What does ruling this out mean for the problem? Ruling out a plausible explanation narrows the solution space, which is genuine progress. Name what has been eliminated and why it matters.
- **If inconclusive**: What specific gap prevented a clear result? What would a follow-up hypothesis or experiment need to do differently to resolve it? This is the most important part of an inconclusive conclusion -- it turns an ambiguous result into a concrete direction.

### Step 3: Write the conclusion

Append to the hypothesis file:

**If verdict is `confirmed`:**

```
## Conclusion

**Verdict:** confirmed

**Reasoning:** <2-4 sentences explaining why this verdict follows from the experiment results. Be specific -- cite which experiments and what their evidence strengths were. Do not just summarize outcomes; explain why the aggregate picture leads to this verdict.>

**Implication for the problem:** <What this means for the original problem. Connect back to the success criteria from problem.md.>

**Rigor:** <1-3 sentences assessing whether the evidence meets publication-grade standards: reproducibility of methodology, honesty of reporting, appropriate statistical treatment, and any methodological limitations.>

**Novelty:** <1-2 sentences assessing whether the confirmed result reproduces existing knowledge or contributes something new. Draw from the **Novelty:** tags recorded in experiment Results sections; if none were recorded, assess directly from the Literature section. Use the scale: novel / incremental / replication.>

**Follow-up questions:**
- <Question raised by this result that the next iteration should address>
- <...>
```

**If verdict is `refuted` or `inconclusive`:**

```
## Conclusion

**Verdict:** <refuted | inconclusive>

**Reasoning:** <2-4 sentences explaining why this verdict follows from the experiment results. Be specific -- cite which experiments and what their evidence strengths were. Do not just summarize outcomes; explain why the aggregate picture leads to this verdict.>

**Implication for the problem:** <What this means for the original problem. Connect back to the success criteria from problem.md.>

**Rigor:** <1-3 sentences assessing whether the evidence meets publication-grade standards: reproducibility of methodology, honesty of reporting, appropriate statistical treatment, and any methodological limitations.>

**Follow-up questions:**
- <Question raised by this result that the next iteration should address>
- <...>
```

### Step 4: Update status

Update the `## Status` line in the hypothesis file to reflect the verdict:

```
## Status
<confirmed | refuted | inconclusive>
```

Use `Edit` to find and replace the current status value. Do not modify any other content.
