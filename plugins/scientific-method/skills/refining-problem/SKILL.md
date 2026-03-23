---
name: refining-problem
description: "Refine a problem statement into a research-ready formulation. Creates problem.md through structured dialogue, defines a research question, and sharpens a problem statement backed by background literature research."
user-invocable: true
argument-hint: "problem-slug and initial description (e.g., 'dark-matter \"What accounts for missing mass in galaxy rotation?\"')"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Task
  - AskUserQuestion
model: opus
color: green
---

# Refining Problem

Sharpen a rough problem statement into a precise, research-ready formulation through structured dialogue with the operator, backed by real-time background literature research. Produce `problem.md` as the source of truth for all downstream autonomous steps.

The operator remains in full control until `problem.md` is confirmed. After confirmation, the autonomous loop runs without interruption.

## Arguments

- **Problem slug** -- kebab-case directory name (required)
- **Initial description** -- rough problem statement (required on first run, optional when resuming)

## Workflow

### Step 0: Setup

Create the problem directory and references subdirectory:
```
bash -c "mkdir -p <problem-slug>/references"
```

If `problem.md` already exists and the operator has not requested re-refinement, read it and skip to Step 4 to re-confirm. The file is the checkpoint.

### Step 1: Launch background research agents

Immediately launch **2-3 background Task agents** (run_in_background: true) to map the problem space before asking any questions. Focus each on a different angle:

- **Scope agent**: Search for canonical definitions, existing frameworks, or established formulations of this problem. Run `/researching-literature` with the topic and problem directory.
- **Prior work agent**: Search for existing solutions, known attempts, and related work. Run `/researching-literature`.
- **Boundary agent**: Search for edge cases, known failure modes, and adjacent problems. Run `/researching-literature`.

Launch all three in a single response before asking any questions.

### Step 2: Ask refinement questions

While background agents run, ask the operator **one question per round** via `AskUserQuestion`. Work through these in order, adapting based on answers:

1. **Goals** -- What outcome would constitute "solving" this problem? What does success look like?
2. **Scope** -- What is explicitly in scope? What should this research NOT address?
3. **Constraints** -- Are there constraints (domain, tools, resources, time) the research must respect?
4. **Prior knowledge** -- What does the operator already know or have tried? What approaches have failed?
5. **Success criteria** -- How will the operator verify a solution? What would a definitive answer look like?

For each question:
- Provide 3-4 concrete answer choices reflecting the most likely interpretations
- Always include a free-text option for custom answers
- After each answer, fold it into a running internal formulation of the problem

### Step 3: Integrate background research

After 2-3 questions, check whether background agents have completed. Read `references.md` for their findings.

For each significant finding, evaluate:
- Does it reframe the problem?
- Does it reveal an existing solution or partial solution?
- Does it expose a hidden assumption or scope issue?

Surface relevant findings as context in the next question: *"Background research found X -- does this change how you'd define the scope?"* Only surface findings that are genuinely useful; do not dump the full literature list.

Continue asking questions, now incorporating both operator answers and literature context.

### Step 4: Write problem.md

After 3-5 questions (or earlier if the problem is already well-defined), write `<problem-slug>/problem.md` using the structure in `references/problem-template.md`. Leave 'Novelty required' as a placeholder — the operator sets it during Step 5 confirmation.

### Step 5: Confirm with operator

Ask via `AskUserQuestion`:

> "Here is the refined problem statement. Does this capture what you're trying to solve?"

Options: "Yes, this is correct", "Needs adjustments", "Start over"

- **Adjustments**: Ask what to change, update the file, re-confirm.
- **Start over**: Clear the file, return to Step 2.
- **Confirmed**: Proceed to the novelty question below before finalizing.

**Novelty question (after "Yes, this is correct" only):** Ask via `AskUserQuestion`:

> "Does this research require a novel solution, or is confirming an existing result acceptable?"

Options: "Novel solution required (replications do not count as solved)", "Replications accepted (confirming known results is a valid outcome)"

Set `Novelty required: yes` or `Novelty required: no` in `problem.md` based on the answer. Once set, this field is immutable for the duration of the research session.

Output the path to `problem.md` and confirm the autonomous loop is ready.

Once confirmed, do not involve the operator again unless explicitly invoked.

## References

- `references/problem-template.md` -- Structure template for problem.md output
