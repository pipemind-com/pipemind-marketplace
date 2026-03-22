# Spec: scientific-method Plugin
**Source:** Plugin design conversation + implemented skill files
**Epic:** N/A — single spec
**Glossary:** specs/glossary.md
**Generated:** 2026-03-22
**Status:** DRAFT — requires operator review

## System Constraints

- **SC-01**: Every skill must be idempotent. Re-running a skill on the same file must detect completed work and skip it. File state is the sole checkpoint — no in-memory state persists across sessions.
- **SC-02**: After the operator confirms `problem.md`, the autonomous loop must not prompt or block on operator input. The only exception is if MAX_ITERATIONS is reached, at which point the loop exits and reports.
- **SC-03**: Hypothesis numbering must be globally sequential across all iterations. Once `hypothesis-03.md` exists, the next hypothesis is always `hypothesis-04.md`, regardless of which iteration created it.
- **SC-04**: Every literature source must receive a stable REF-NNN identifier in `references.md`. Skills reference sources by these IDs. IDs must never be reused or reassigned.
- **SC-05**: Experiment results must record what was actually observed, not what was expected. Fabricated or simulated results are prohibited. If an experiment cannot be executed, the result must be `not-runnable` with an explanation.
- **SC-06**: The research loop must terminate after at most 5 full iterations (Steps A through F). On termination, `findings.md` must be written regardless of outcome.
- **SC-07**: Each skill must operate on a single problem directory. All file reads and writes are scoped to that directory. Skills must not read or modify files outside the problem directory (except reading their own skill instructions).
- **SC-08**: Parallel sub-agents must be independent. No hypothesis refinement, experiment, or conclusion agent may read or modify another hypothesis's file.

## Features

### F-01: Problem Refinement | MUST

**F-01.1: Initial problem setup (happy path)**
- **GIVEN** an operator with a rough problem statement and a problem slug
- **WHEN** the operator invokes `/refining-problem` with the slug and description
- **THEN** a problem directory is created, background literature research agents are launched in parallel, and the operator is asked their first refinement question

**F-01.2: Background literature informs refinement**
- **GIVEN** background research agents are running while the operator answers questions
- **WHEN** the agents complete and return findings
- **THEN** relevant findings are surfaced in subsequent questions to the operator, not dumped as a raw list

**F-01.3: Operator confirms problem statement**
- **GIVEN** a draft `problem.md` has been written after 3-5 questions
- **WHEN** the operator confirms the problem statement
- **THEN** `problem.md` is finalized and the skill exits, signaling readiness for the autonomous loop

**F-01.4: Operator requests adjustments**
- **GIVEN** a draft `problem.md` has been presented
- **WHEN** the operator selects "Needs adjustments"
- **THEN** the operator is asked what to change, the file is updated, and confirmation is requested again

**F-01.5: Operator starts over**
- **GIVEN** a draft `problem.md` has been presented
- **WHEN** the operator selects "Start over"
- **THEN** the existing file is cleared and refinement returns to the question phase

**F-01.6: Resume from existing problem.md**
- **GIVEN** `problem.md` already exists in the problem directory
- **WHEN** the operator invokes `/refining-problem`
- **THEN** the existing file is read and the operator is asked to re-confirm without re-drafting

**F-01.7: Missing initial description on first run (failure)**
- **GIVEN** no `problem.md` exists and no initial description is provided
- **WHEN** the operator invokes `/refining-problem` with only a slug
- **THEN** the skill proceeds but generates questions from the slug alone, producing a less-informed first draft [ASSUMPTION]

### F-02: Hypothesis Generation | MUST

**Requires:** F-01 (Problem Refinement)

**F-02.1: First-iteration hypothesis generation (happy path)**
- **GIVEN** a confirmed `problem.md` exists and no hypothesis files exist
- **WHEN** `/generating-hypotheses` is invoked on the problem directory
- **THEN** 2-5 hypothesis stub files are created (`hypothesis-01.md` through `hypothesis-NN.md`), each containing a falsifiable statement, rationale, and `pending` status

**F-02.2: Subsequent-iteration hypothesis generation**
- **GIVEN** hypothesis files from prior iterations exist, some with `confirmed`, `refuted`, or `inconclusive` conclusions
- **WHEN** `/generating-hypotheses` is invoked
- **THEN** new hypotheses are generated that build on prior conclusions, do not duplicate confirmed or refuted claims, and are numbered sequentially after the last existing file

**F-02.3: All prior hypotheses still pending (warning)**
- **GIVEN** existing hypothesis files all have status `pending` (none concluded)
- **WHEN** `/generating-hypotheses` is invoked
- **THEN** a warning is issued that untested hypotheses already exist, and the operator is asked whether to proceed or abort

**F-02.4: No problem.md exists (failure)**
- **GIVEN** the problem directory has no `problem.md`
- **WHEN** `/generating-hypotheses` is invoked
- **THEN** the skill stops with an error directing the operator to run `/refining-problem` first

### F-03: Hypothesis Refinement | MUST

**Requires:** F-02 (Hypothesis Generation), F-07 (Literature Research)

**F-03.1: Literature-backed refinement (happy path)**
- **GIVEN** a hypothesis file exists with status `pending` and no `## Literature` section
- **WHEN** `/refining-hypothesis` is invoked on that file
- **THEN** three parallel literature searches are launched (claim, mechanism, counterexamples), and the hypothesis file is expanded with supporting evidence, challenges, and a refined statement

**F-03.2: Literature resolves hypothesis without experiments**
- **GIVEN** a hypothesis file exists with status `pending`
- **WHEN** literature research reveals the hypothesis is definitively confirmed or refuted by prior published work
- **THEN** the hypothesis status is updated to `confirmed` or `refuted` with a note explaining the literature basis, and the hypothesis skips experiment design, execution, and conclusion

**F-03.3: Already-refined hypothesis (idempotent skip)**
- **GIVEN** a hypothesis file already contains a `## Literature` section
- **WHEN** `/refining-hypothesis` is invoked
- **THEN** the skill reports the hypothesis was already refined and exits without modification

**F-03.4: New sources added to shared bibliography**
- **GIVEN** literature research finds new sources
- **WHEN** the literature agents complete
- **THEN** all new sources are appended to the problem directory's `references.md` with sequential REF-NNN IDs, and the hypothesis file references them by ID

### F-04: Experiment Design | MUST

**Requires:** F-03 (Hypothesis Refinement)

**F-04.1: Design experiments for a refined hypothesis (happy path)**
- **GIVEN** a hypothesis file has a `## Literature` section, no `## Experiments` section, and status `pending` or `inconclusive`
- **WHEN** `/designing-experiments` is invoked
- **THEN** 1-3 experiment paths are appended to the hypothesis file, each specifying type, approach, confirmation criteria, refutation criteria, and confidence level

**F-04.2: Hypothesis already resolved by literature (skip)**
- **GIVEN** a hypothesis file has status `confirmed` or `refuted`
- **WHEN** `/designing-experiments` is invoked
- **THEN** the skill notes the hypothesis was already resolved and exits without adding experiments

**F-04.3: Experiments already designed (idempotent skip)**
- **GIVEN** a hypothesis file already contains a `## Experiments` section
- **WHEN** `/designing-experiments` is invoked
- **THEN** the skill exits without modification

### F-05: Experiment Execution | MUST

**Requires:** F-04 (Experiment Design)

**F-05.1: Code experiment execution (happy path)**
- **GIVEN** a hypothesis file has a code-type experiment with an empty `#### Results` section
- **WHEN** `/running-experiments` is invoked
- **THEN** the code is written, executed, and the actual output is recorded as the result along with an outcome and evidence strength assessment

**F-05.2: Math proof experiment execution**
- **GIVEN** a hypothesis file has a math-proof-type experiment with an empty `#### Results` section
- **WHEN** `/running-experiments` is invoked
- **THEN** the proof is worked through step by step and the result records either a completed proof (QED), a counterexample, or the specific gap that prevented completion

**F-05.3: Evidence-gathering experiment execution**
- **GIVEN** a hypothesis file has an evidence-gathering-type experiment with an empty `#### Results` section
- **WHEN** `/running-experiments` is invoked
- **THEN** web searches are conducted, sources are fetched, and the result records quoted or summarized findings with REF-NNN citations and an assessment of aggregate signal

**F-05.4: Data-analysis experiment execution**
- **GIVEN** a hypothesis file has a data-analysis-type experiment with an empty `#### Results` section
- **WHEN** `/running-experiments` is invoked
- **THEN** datasets are searched, fetched, and analyzed, with key statistics and patterns recorded as the result

**F-05.5: Logical-deduction experiment execution**
- **GIVEN** a hypothesis file has a logical-deduction-type experiment with an empty `#### Results` section
- **WHEN** `/running-experiments` is invoked
- **THEN** the deductive chain is worked through with numbered premises, and the result records where the argument holds, requires assumptions, or breaks

**F-05.6: Early exit on decisive result**
- **GIVEN** an experiment produces a `confirmed` or `refuted` outcome with `strong` evidence
- **WHEN** subsequent experiments remain pending in the same hypothesis
- **THEN** remaining experiments are marked `skipped` with a reference to the decisive result

**F-05.7: Experiment not runnable (failure)**
- **GIVEN** an experiment cannot be executed with available tools (missing dependencies, paywalled data, domain expertise gap)
- **WHEN** `/running-experiments` attempts to run it
- **THEN** the result is recorded as `not-runnable` with a clear explanation of the limitation

**F-05.8: Missing dependency is not a refutation (edge case)**
- **GIVEN** a code experiment fails because a required tool or library is not installed
- **WHEN** the execution error is analyzed
- **THEN** the result is recorded as `not-runnable` with a note that this is a setup problem, not evidence against the hypothesis

### F-06: Conclusion Drawing | MUST

**Requires:** F-05 (Experiment Execution)

**F-06.1: Confirmed verdict (happy path)**
- **GIVEN** a hypothesis file has experiment results and no `## Conclusion` section
- **WHEN** the weight of evidence supports the hypothesis with at least one strong confirmation and no strong contradiction
- **THEN** the conclusion section is appended with verdict `confirmed`, reasoning citing specific experiments, implication for the problem, and follow-up questions

**F-06.2: Refuted verdict**
- **GIVEN** a hypothesis file has experiment results
- **WHEN** any experiment produced a `refuted` outcome with `strong` evidence
- **THEN** the conclusion records verdict `refuted`, noting that a single strong counterexample overrides weak support

**F-06.3: Inconclusive verdict**
- **GIVEN** a hypothesis file has experiment results
- **WHEN** evidence is mixed, all weak, all not-runnable, or contradictory without clear dominance
- **THEN** the conclusion records verdict `inconclusive` with specific guidance on what the next iteration needs to address

**F-06.4: All experiments skipped or not-runnable (edge case)**
- **GIVEN** every experiment in a hypothesis was either `skipped` or `not-runnable`
- **WHEN** `/drawing-conclusions` is invoked
- **THEN** the verdict is `inconclusive` with a note that the hypothesis could not be tested with available tools

**F-06.5: Status line updated to match verdict**
- **GIVEN** a conclusion has been written
- **WHEN** the conclusion step completes
- **THEN** the `## Status` line in the hypothesis file is updated from `pending` to the verdict value

### F-07: Literature Research | MUST

**F-07.1: Source discovery and bibliography (happy path)**
- **GIVEN** a topic query and a problem directory
- **WHEN** `/researching-literature` is invoked
- **THEN** 3-5 web searches are conducted from different angles, up to 10 new sources are evaluated, and relevant sources are appended to `references.md` with sequential REF-NNN IDs, metadata, and relevance summaries

**F-07.2: PDF download when available**
- **GIVEN** a source URL points to a PDF or has a visible PDF download link
- **WHEN** the source is being processed
- **THEN** the PDF is downloaded to `references/<author-year-slug>.pdf` and the filename is recorded in `references.md`

**F-07.3: PDF download fails gracefully (failure)**
- **GIVEN** a PDF download is attempted but the publisher blocks it or content is non-PDF
- **WHEN** the download fails
- **THEN** the URL is recorded for manual access and the skill continues without error

**F-07.4: Duplicate source detection (edge case)**
- **GIVEN** a URL is found in search results that already exists in `references.md`
- **WHEN** the source is evaluated
- **THEN** it is silently skipped without creating a duplicate entry

**F-07.5: Standalone invocation**
- **GIVEN** an operator invokes `/researching-literature` outside any research session
- **WHEN** there is no existing `references.md` in the target directory
- **THEN** the file is created with a header and sources are added starting from REF-001

### F-08: Research Loop Orchestration | MUST

**Requires:** F-01, F-02, F-03, F-04, F-05, F-06

**F-08.1: Full loop from scratch (happy path)**
- **GIVEN** an operator invokes `/researching` with a slug and description and no prior state exists
- **WHEN** the orchestrator runs
- **THEN** Phase 1 (problem refinement) involves the operator, then Phase 2 runs autonomously through hypothesis generation, refinement, experimentation, conclusion, and assessment without operator interaction

**F-08.2: Problem solved in first iteration**
- **GIVEN** the autonomous loop completes Step E and at least one hypothesis is `confirmed`
- **WHEN** the confirmed hypothesis satisfies the success criteria in `problem.md`
- **THEN** `findings.md` is written with outcome "solved" and the loop stops

**F-08.3: Problem not solved, iteration continues**
- **GIVEN** the autonomous loop completes Step E and no hypothesis is confirmed (all refuted or inconclusive)
- **WHEN** fewer than 5 iterations have completed
- **THEN** the loop returns to Step A, and `/generating-hypotheses` reads prior conclusions to produce new angles

**F-08.4: Maximum iterations reached (termination)**
- **GIVEN** 5 full iterations have completed without a confirmed solution
- **WHEN** Step F assesses the state
- **THEN** `findings.md` is written with outcome "inconclusive after 5 iterations" including what was ruled out and open questions, and the operator is notified

**F-08.5: Confirmed hypothesis does not satisfy success criteria (edge case)**
- **GIVEN** a hypothesis is `confirmed` but the confirmed claim does not address the success criteria in `problem.md`
- **WHEN** Step F assesses the state
- **THEN** the problem is not considered solved and the loop continues to the next iteration

**F-08.6: Parallel step execution**
- **GIVEN** multiple hypotheses need the same step (refinement, experiment design, execution, or conclusion)
- **WHEN** the orchestrator reaches that step
- **THEN** one sub-agent is spawned per hypothesis in a single response so they run concurrently

**F-08.7: Hypotheses resolved by literature skip experiment pipeline**
- **GIVEN** a hypothesis was confirmed or refuted during Step B (literature refinement) without experiments
- **WHEN** the orchestrator reaches Steps C, D, or E
- **THEN** that hypothesis is excluded from the experiment pipeline

### F-09: Idempotent State Recovery | MUST

**Requires:** F-08 (Research Loop Orchestration)

**F-09.1: Resume after interruption at any step**
- **GIVEN** the orchestrator was interrupted mid-loop (crash, timeout, operator abort)
- **WHEN** the operator re-invokes `/researching` with the same slug
- **THEN** the orchestrator reads file state, determines the furthest incomplete step, and resumes from that point without re-executing completed work

**F-09.2: Resume detection precedence**
- **GIVEN** the problem directory contains files at various stages of completion
- **WHEN** the orchestrator checks state
- **THEN** it applies resume rules in order: no problem.md → Phase 1; no hypotheses → Step A; unrefined hypotheses → Step B; undesigned → Step C; unrun → Step D; unconcluded → Step E; all concluded → Step F

**F-09.3: Individual skill idempotency**
- **GIVEN** a skill has already produced its output section in a hypothesis file
- **WHEN** the skill is invoked again on the same file
- **THEN** the skill detects the existing section and exits without modification

### F-10: Findings Generation | MUST

**Requires:** F-06 (Conclusion Drawing)

**F-10.1: Solved findings (happy path)**
- **GIVEN** the loop exits because a hypothesis was confirmed and satisfies success criteria
- **WHEN** `findings.md` is written
- **THEN** it contains: outcome "solved", solution summary, what was ruled out, open questions, iteration count, and lists of confirmed and refuted hypotheses

**F-10.2: Inconclusive findings (termination)**
- **GIVEN** the loop exits because MAX_ITERATIONS was reached
- **WHEN** `findings.md` is written
- **THEN** it contains: outcome "inconclusive after N iterations", what was ruled out, open questions with concrete follow-up directions, iteration count, and lists of confirmed and refuted hypotheses

## Open Questions

- OQ-01: Should the operator be able to configure MAX_ITERATIONS per session, or is 5 always the cap?
- OQ-02: Should findings.md include a cost/token summary of the research session?
- OQ-03: What happens if the operator re-invokes `/refining-problem` after the autonomous loop has already started — should it reset the entire session or only update problem.md?

## Assumptions

- A-01: [ASSUMPTION] If no initial description is provided on first run, the skill will generate questions based solely on the slug name. The operator can always provide more context in their answers.
- A-02: [ASSUMPTION] The `/researching-literature` skill can fetch content from any publicly accessible URL. Paywalled or gated content is handled gracefully by recording the URL for manual access.
- A-03: [ASSUMPTION] All hypothesis files within a single problem directory follow the same structural contract. Third-party files placed in the directory that do not conform are ignored by the orchestrator.
