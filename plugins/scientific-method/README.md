# scientific-method

A domain-agnostic scientific method research plugin for Claude Code. Guides any problem through autonomous refinement, hypothesis generation, literature research, experimentation, and conclusion — looping autonomously until solved.

## Install

```bash
./install.sh scientific-method --symlink
```

## Usage

Start a full research session:

```
/researching dark-matter "What accounts for the missing mass in galaxy rotation curves?"
```

Sub-skills (`/refining-problem`, `/generating-hypotheses`, etc.) are internal to the orchestrator and are not user-invocable. Use `/researching` to run the full pipeline.

## File Structure

Each research session lives in a directory named after the problem slug:

```
<problem-slug>/
├── problem.md               # refined problem statement (refined autonomously)
├── hypothesis-01.md         # hypothesis + literature + experiments + results + conclusion
├── hypothesis-02.md
├── ...
├── findings.md              # final summary written when the loop exits
├── article-abstract.md      # publishable abstract written when the loop exits
├── references.md            # bibliography — all sources with REF-NNN IDs
└── references/              # downloaded articles and PDFs
    └── author-2024-title.pdf
```

Hypothesis files accumulate across iterations — numbering is sequential and never resets.

## Skills

| Skill | Model | Purpose |
|---|---|---|
| `/researching` | opus | Full loop orchestrator — idempotent, resumes from file state |
| `refining-problem` | opus | Autonomous problem refinement with background literature agents |
| `generating-hypotheses` | opus | Generate testable hypotheses (minimum 4) informed by prior conclusions |
| `refining-hypothesis` | sonnet | Deepen one hypothesis with parallel literature research |
| `designing-experiments` | sonnet | Design 1–3 experiment paths per hypothesis |
| `running-experiments` | opus | Execute or prove experiments — code, math, evidence, data |
| `drawing-conclusions` | sonnet | Synthesize results into confirmed / refuted / inconclusive verdict |
| `researching-literature` | sonnet | Web search + download sources → references.md + references/ |

## The Loop

```
[Fully autonomous]
  Step 1: Refine problem autonomously → problem.md

[Fully autonomous — iterates until solved]
  while not solved (max 5 iterations):
    Step 2: Generate hypotheses from problem + prior conclusions
    Step 3: Refine each hypothesis in parallel (literature research)
    Step 4: Design experiments for each hypothesis
    Step 5: Run / prove experiments in parallel
    Step 6: Draw conclusions — confirmed / refuted / inconclusive
    Step 7: Solved? → write findings.md + article-abstract.md and stop
             Not solved? → append refinement addendum to problem.md, loop
```

The orchestrator (`/researching`) is idempotent: re-running it reads the current file state and resumes from wherever the previous run left off.

## Hypothesis File Structure

Each `hypothesis-NN.md` is built incrementally by the pipeline:

```markdown
# Hypothesis NN: <Title>
## Status        ← updated to confirmed/refuted/inconclusive when concluded
## Statement     ← written by generating-hypotheses
## Rationale     ← written by generating-hypotheses
## Literature    ← added by refining-hypothesis
## Refined Statement  ← added by refining-hypothesis
## Experiments   ← added by designing-experiments (with Results filled by running-experiments)
## Conclusion    ← added by drawing-conclusions
```
