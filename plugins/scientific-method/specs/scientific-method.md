# Spec: scientific-method Plugin
**Source:** Plugin design conversation + implemented skill files
**Epic:** N/A — single spec
**Glossary:** specs/glossary.md
**Generated:** 2026-03-22
**Status:** DRAFT — requires operator review

## System Constraints

- **SC-01**: Every skill must be idempotent. Re-running a skill on the same file must detect completed work and skip it. File state is the sole checkpoint — no in-memory state persists across sessions.
- **SC-02**: After `problem.md` is written by the autonomous refinement loop, the research loop must not prompt or block on operator input. No skill in the pipeline uses `AskUserQuestion`. The only exception is if MAX_ITERATIONS is reached, at which point the loop exits and reports.
- **SC-03**: Hypothesis numbering must be globally sequential across all iterations. Once `hypothesis-03.md` exists, the next hypothesis is always `hypothesis-04.md`, regardless of which iteration created it. Hypothesis filenames are immutable once created — no skill may rename or renumber an existing hypothesis file. This preserves the integrity of artifact paths recorded in Results sections.
- **SC-04**: Every literature source must receive a stable REF-NNN identifier in `references.md`. Skills reference sources by these IDs. IDs must never be reused or reassigned.
- **SC-05**: Experiment results must record what was actually observed, not what was expected. Fabricated or simulated results are prohibited. If an experiment cannot be executed, the result must be `not-runnable` with an explanation.
- **SC-06**: The research loop must terminate after at most 5 full iterations (Steps A through F) per invocation. On termination, `findings.md` must be written regardless of outcome. The operator can re-invoke `/researching` to start a new 5-iteration session that resumes from existing state.
- **SC-07**: Each skill must operate on a single problem directory. All file reads and writes are scoped to that directory. Skills must not read or modify files outside the problem directory (except reading their own skill instructions).
- **SC-08**: Parallel sub-agents must be independent. No hypothesis refinement, experiment, or conclusion agent may read or modify another hypothesis's file.
- **SC-09**: Experiment artifacts (code files, downloaded datasets, analysis outputs) must be written to `<problem-dir>/experiments/<hypothesis-slug>/` exclusively by the `/running-experiments` skill. `/designing-experiments` writes nothing to `experiments/`. Each hypothesis gets its own subdirectory, ensuring parallel agents never collide. Artifact files are numbered globally and sequentially per hypothesis across all iterations (`exp1.py`, `exp2.py`, …) — the extension matches the language or format chosen by the running agent based on hypothesis context (e.g., `.py`, `.sh`, `.js`, `.csv`). Numbers never reset and existing files are never overwritten. The `Results` section of the hypothesis file must include a line `**Artifact:** experiments/<hypothesis-slug>/exp<N>.<ext>` for every file written, so readers can locate artifacts without scanning the directory. The hypothesis file remains the sole authoritative state checkpoint; the orchestrator never reads `experiments/` for resume detection. If an experiment produces no persistent artifact (math-proof, logical-deduction, inline evidence-gathering), nothing is written to `experiments/`. Fetched literature content continues to go to `references/` as always. Failed experiments (non-zero exit, import error) leave their artifact in place — the artifact is evidence, not a success signal. **Safety invariant**: experiment code must not write files outside `<problem-dir>/` and must not spawn persistent background processes; any experiment that would require doing so must be recorded as `not-runnable`.

- **SC-10**: Literature sources must meet a quality bar before inclusion in `references.md`. Prefer peer-reviewed journal articles, conference papers, and established technical reports. Actively exclude blog posts, opinion pieces, press releases, and low-signal web pages unless no higher-quality source exists for a critical claim. A smaller set of authoritative sources is always preferred over a padded list — 5 high-quality sources outweigh 10 mediocre ones. Every included source must earn its place by directly advancing understanding of the topic.
- **SC-11**: Literature search must use a dual-track strategy: one search pass filtered to the last 3 years to capture cutting-edge work, and one unfiltered pass to surface landmark papers that define the field. Both tracks contribute to `references.md`. The `Year` field on each entry lets downstream agents distinguish recent from foundational sources.
- **SC-12**: Experiment results must meet publication-grade rigor: reproducible methodology, clearly documented procedure, honest reporting of all outcomes (including negative results), and appropriate statistical treatment where quantitative data is involved. Novelty relative to existing literature is desirable and should be assessed, but is not always achievable — rigor is the non-negotiable floor.
- **SC-13**: MCP tool integration is strictly optional. Skills that support `mcp-semantic-scholar` tools must detect availability at runtime by attempting a call — not by reading configuration. If the call fails or the tool is absent, the skill must fall back to WebSearch/WebFetch transparently. The research loop must produce correct output in both modes. MCP presence is an enhancement only; its absence must never degrade core functionality.

## Features

### F-01: Problem Refinement | MUST

**F-01.1: Autonomous problem setup (happy path)**
- **GIVEN** a problem slug and initial description
- **WHEN** the orchestrator invokes `/refining-problem`
- **THEN** a problem directory is created, background `/researching-literature` agents are launched in parallel (inheriting dual-track search and quality gate from F-07), and an initial draft of `problem.md` is written from the initial description

**F-01.2: Background literature informs autonomous refinement**
- **GIVEN** background `/researching-literature` agents complete while the initial draft exists
- **WHEN** the agents return findings
- **THEN** findings are synthesized into the Background section of `problem.md`, and the skill assesses the problem definition against three quality criteria: clear research question, testable success criteria, and appropriate scope

**F-01.3: Autonomous refinement iteration**
- **GIVEN** the problem definition fails one or more quality criteria
- **WHEN** refinement iterations remain (max 3)
- **THEN** the deficient sections of `problem.md` are refined, 1-2 targeted `/researching-literature` Tasks are launched to fill knowledge gaps, and the quality assessment is repeated

**F-01.4: Autonomous novelty determination**
- **GIVEN** the problem definition passes quality criteria (or 3 refinement iterations have elapsed)
- **WHEN** the skill finalizes `problem.md`
- **THEN** the `Novelty required:` field is auto-determined from the literature landscape: `yes` if existing published solutions substantially cover the problem space, `no` if the space is largely unexplored or preliminary. Once set, this field is immutable for the duration of the research session

**F-01.5: Resume from existing problem.md**
- **GIVEN** `problem.md` already exists in the problem directory
- **WHEN** `/refining-problem` is invoked
- **THEN** the existing file is read and the skill skips to the quality assessment step without re-drafting

**F-01.6: Missing initial description on first run (failure)**
- **GIVEN** no `problem.md` exists and no initial description is provided
- **WHEN** `/refining-problem` is invoked with only a slug
- **THEN** the skill proceeds but infers the problem from the slug alone, producing a less-informed first draft [ASSUMPTION]

### F-02: Hypothesis Generation | MUST

**Requires:** F-01 (Problem Refinement)

**F-02.1: First-iteration hypothesis generation (happy path)**
- **GIVEN** a confirmed `problem.md` exists and no hypothesis files exist
- **WHEN** `/generating-hypotheses` is invoked on the problem directory
- **THEN** hypothesis stub files are created (minimum 4, as many as the problem space warrants), each containing a falsifiable statement, rationale, and `pending` status

**F-02.2: Subsequent-iteration hypothesis generation**
- **GIVEN** hypothesis files from prior iterations exist, some with `confirmed`, `refuted`, or `inconclusive` conclusions
- **WHEN** `/generating-hypotheses` is invoked
- **THEN** new hypotheses are generated that build on prior conclusions, do not duplicate confirmed or refuted claims, and are numbered sequentially after the last existing file

**F-02.3: All prior hypotheses still pending (skip)**
- **GIVEN** existing hypothesis files all have status `pending` (none concluded)
- **WHEN** `/generating-hypotheses` is invoked
- **THEN** the skill skips generation and reports that pending hypotheses must be tested first

**F-02.4: No problem.md exists (failure)**
- **GIVEN** the problem directory has no `problem.md`
- **WHEN** `/generating-hypotheses` is invoked
- **THEN** the skill stops with an error directing the operator to run `/refining-problem` first

### F-03: Hypothesis Refinement | MUST

**Requires:** F-02 (Hypothesis Generation), F-07 (Literature Research)

**F-03.1: Literature-backed refinement (happy path)**
- **GIVEN** a hypothesis file exists with status `pending` and no `## Literature` section
- **WHEN** `/refining-hypothesis` is invoked on that file
- **THEN** three lightweight parallel searches are launched (1-2 queries each for claim, mechanism, counterexamples), followed by one full dual-track `/researching-literature` invocation to fill gaps in coverage. All searches inherit the quality gate from F-07. The hypothesis file is expanded with supporting evidence, challenges, and a refined statement. All sources flow through `references.md` with REF-NNN IDs

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
- **THEN** 1-3 experiment paths are appended to the hypothesis file, each specifying type, approach, confirmation criteria, refutation criteria, confidence level, and a `**Publishability potential:**` note assessing whether this experiment, if successful, could yield a novel contribution relative to the prior art in the Literature section. When multiple experiment types are equally valid for testing the hypothesis, the design should lean toward the type with higher publishability potential — but never sacrifice scientific validity for publishability. No files are written to `experiments/`

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
- **THEN** the code is written to `<problem-dir>/experiments/<hypothesis-slug>/exp<N>.<ext>`, executed, and the actual output is recorded inline in the hypothesis file as the result along with an outcome and evidence strength assessment

**F-05.2: Math proof experiment execution**
- **GIVEN** a hypothesis file has a math-proof-type experiment with an empty `#### Results` section
- **WHEN** `/running-experiments` is invoked
- **THEN** the proof is worked through step by step and the result records either a completed proof (QED), a counterexample, or the specific gap that prevented completion

**F-05.3: Evidence-gathering experiment execution**
- **GIVEN** a hypothesis file has an evidence-gathering-type experiment with an empty `#### Results` section
- **WHEN** `/running-experiments` is invoked
- **THEN** searches are conducted — preferring `search_papers` for academic queries when MCP tools are available, falling back to WebSearch otherwise — sources are fetched, and the result records quoted or summarized findings with REF-NNN citations and an assessment of aggregate signal

**F-05.4: Data-analysis experiment execution**
- **GIVEN** a hypothesis file has a data-analysis-type experiment with an empty `#### Results` section
- **WHEN** `/running-experiments` is invoked
- **THEN** datasets are fetched and saved to `<problem-dir>/experiments/<hypothesis-slug>/`, analysis scripts are written and run from there, and key statistics and patterns are recorded inline in the hypothesis file as the result

**F-05.5: Logical-deduction experiment execution**
- **GIVEN** a hypothesis file has a logical-deduction-type experiment with an empty `#### Results` section
- **WHEN** `/running-experiments` is invoked
- **THEN** the deductive chain is worked through with numbered premises, and the result records where the argument holds, requires assumptions, or breaks

**F-05.5a: Artifact path recorded in Results**
- **GIVEN** an experiment writes one or more files to `experiments/<hypothesis-slug>/`
- **WHEN** the `#### Results` section is filled in
- **THEN** the Results section includes `**Artifact:** experiments/<hypothesis-slug>/exp<N>.<ext>` for each file written, preceding the narrative

**F-05.5b: Failed code experiment keeps artifact**
- **GIVEN** a code experiment file is written to `experiments/<hypothesis-slug>/` but execution fails (non-zero exit code, import error, syntax error)
- **WHEN** the result is recorded
- **THEN** the artifact file is retained, the Results section records the full error output and the artifact path, outcome is `inconclusive` or `not-runnable` as appropriate, and the failure is not treated as evidence against the hypothesis unless the failure itself is informative

**F-05.5c: Publication-grade rigor in results**
- **GIVEN** an experiment has been executed and results are being recorded
- **WHEN** the `#### Results` section is written
- **THEN** the methodology is documented clearly enough to be reproduced, all outcomes are reported honestly (including negative or unexpected results), quantitative data includes appropriate statistical context, and the evidence assessment distinguishes between what was observed and what was inferred

**F-05.5d: Novelty assessment with targeted search**
- **GIVEN** an experiment produces a `confirmed` outcome and the hypothesis file has a `## Literature` section
- **WHEN** the result is recorded
- **THEN** 1-2 targeted searches are run comparing the confirmed result against existing published solutions — preferring `search_papers` when MCP tools are available, otherwise WebSearch (e.g., querying for the specific method or finding). The Results section includes a `**Novelty:**` tag using a 3-level scale: `novel` (no prior art found for this result), `incremental` (extends or improves on prior work), or `replication` (reproduces known findings). Only the `replication` tag signals the orchestrator (F-08) that the result may not satisfy success criteria when `Novelty required: yes` is set in `problem.md`. The novelty comparison cites any newly discovered prior art by URL. If the literature section has fewer than 3 sources, the novelty search is especially important to avoid false novelty claims

**F-05.6: Early exit on decisive result**
- **GIVEN** an experiment produces a `confirmed` or `refuted` outcome with `strong` evidence
- **WHEN** subsequent experiments remain pending in the same hypothesis
- **THEN** remaining experiments are marked `skipped` with a reference to the decisive result

**F-05.7: Experiment not runnable (failure)**
- **GIVEN** an experiment cannot be executed with available tools (missing dependencies, paywalled data, domain expertise gap, or would require writing outside `<problem-dir>/` or spawning persistent processes)
- **WHEN** `/running-experiments` attempts to run it
- **THEN** the result is recorded as `not-runnable` with a clear explanation of the limitation; no artifact file is written

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

**F-06.4a: Rigor assessment in every conclusion**
- **GIVEN** a conclusion is being written for any verdict
- **WHEN** the conclusion section is appended
- **THEN** it includes a `**Rigor:**` assessment noting whether the evidence meets publication-grade standards: reproducibility of methodology, honesty of reporting, appropriate statistical treatment, and any methodological limitations

**F-06.4b: Novelty note for confirmed hypotheses**
- **GIVEN** a hypothesis receives a `confirmed` verdict
- **WHEN** the conclusion section is written
- **THEN** it includes a `**Novelty:**` note assessing whether the confirmed result reproduces existing knowledge or contributes something new relative to the literature reviewed in the hypothesis file

**F-06.5: Status line updated to match verdict**
- **GIVEN** a conclusion has been written
- **WHEN** the conclusion step completes
- **THEN** the `## Status` line in the hypothesis file is updated from `pending` to the verdict value

### F-07: Literature Research | MUST

**F-07.1: Dual-track source discovery (happy path)**
- **GIVEN** a topic query and a problem directory
- **WHEN** `/researching-literature` is invoked
- **THEN** two search tracks run: (1) a recency track targeting cutting-edge work from the last 3 years, and (2) a landmark track targeting foundational papers with no date filter. The skill first attempts the **MCP path** (see F-07.1c): if `search_papers` is available, 3-4 structured academic searches replace the equivalent WebSearch queries. If MCP tools are unavailable, the **WebSearch path** runs instead: 4-6 web searches across both tracks using standard queries, with recency determined post-hoc from publication year. Regardless of path, only authoritative sources pass the quality gate (F-07.1a) and are appended to `references.md` with sequential REF-NNN IDs, metadata, and relevance summaries

**F-07.1a: Quality gate on source inclusion**
- **GIVEN** candidate sources have been found by searches
- **WHEN** each source is evaluated for inclusion
- **THEN** peer-reviewed journal articles, conference papers, and established technical reports are preferred. Blog posts, opinion pieces, press releases, and low-signal web pages are silently dropped — they do not appear in `references.md` and no log of excluded sources is kept. The final reference list prioritizes depth over breadth — 5 authoritative sources are preferred over 10 mediocre ones

**F-07.1b: Recency and landmark balance**
- **GIVEN** both search tracks have returned results
- **WHEN** the final source list is assembled
- **THEN** the list includes both recent work (last 3 years) and older sources where they are relevant. The landmark track applies no special criteria beyond relevance and the quality gate — any older source that directly advances understanding of the topic qualifies. The `Year` field on each entry allows downstream agents to distinguish cutting-edge from foundational sources

**F-07.1c: Citation snowball via MCP (MCP path only)**
- **GIVEN** `search_papers` is available and 2-3 highly relevant papers have been identified
- **WHEN** `/researching-literature` runs after the initial search
- **THEN** `get_references` (backward: papers the target cites) and `get_citations` (forward: papers that cite the target) are called for those papers with limit 5-10, surfacing connected works that keyword search alone would miss. Results are deduplicated against already-collected sources and evaluated through the same quality gate

**F-07.1d: MCP metadata shortcut (MCP path only)**
- **GIVEN** a source came from `search_papers`, `get_references`, or `get_citations`
- **WHEN** the source is processed for inclusion in `references.md`
- **THEN** title, authors, year, citation count, and open-access PDF URL are taken directly from the structured MCP response without a WebFetch call. `get_paper` is called only when critical metadata fields are missing from the search result

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
- **THEN** Phase 1 (problem refinement) runs autonomously, then Phase 2 runs autonomously through hypothesis generation, refinement, experimentation, conclusion, and assessment — no operator interaction at any point

**F-08.2: Problem solved in first iteration**
- **GIVEN** the autonomous loop completes Step E and at least one hypothesis is `confirmed`
- **WHEN** the confirmed hypothesis satisfies the success criteria in `problem.md`
- **THEN** `findings.md` is written with outcome "solved" and the loop stops

**F-08.3: Problem not solved, iteration continues with refinement addendum**
- **GIVEN** the autonomous loop completes Step E and no hypothesis is confirmed (all refuted or inconclusive)
- **WHEN** fewer than 5 iterations have completed
- **THEN** a refinement addendum is appended to `problem.md` summarizing hypotheses tested, key findings, remaining gaps, and suggested direction. The loop then returns to Step A, and `/generating-hypotheses` reads prior conclusions and the addendum to produce new angles

**F-08.4: Maximum iterations reached (termination)**
- **GIVEN** 5 full iterations have completed without a confirmed solution
- **WHEN** Step F assesses the state
- **THEN** `findings.md` is written with outcome "inconclusive after 5 iterations" including what was ruled out and open questions, and the operator is notified

**F-08.5: Confirmed hypothesis does not satisfy success criteria (edge case)**
- **GIVEN** a hypothesis is `confirmed` but the confirmed claim does not address the success criteria in `problem.md`
- **WHEN** Step F assesses the state
- **THEN** the problem is not considered solved and the loop continues to the next iteration

**F-08.5a: Replication does not satisfy novel-solution criteria (edge case)**
- **GIVEN** a hypothesis is `confirmed` but its Results section contains `**Novelty: replication**` and `problem.md` has `Novelty required: yes`
- **WHEN** Step F assesses the state
- **THEN** the replication is noted as useful context but the problem is not considered solved, and the loop continues to the next iteration seeking a novel or incremental contribution

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
- **THEN** it contains: outcome "solved", solution summary, what was ruled out, open questions, iteration count, lists of confirmed and refuted hypotheses, and a `## Publishability Assessment` section. An `article-abstract.md` is also written alongside

**F-10.2: Inconclusive findings (termination)**
- **GIVEN** the loop exits because MAX_ITERATIONS was reached
- **WHEN** `findings.md` is written
- **THEN** it contains: outcome "inconclusive after N iterations", what was ruled out, open questions with concrete follow-up directions, iteration count, lists of confirmed and refuted hypotheses, and a `## Publishability Assessment` section. An `article-abstract.md` is also written alongside

**F-10.3: Publishability assessment in all findings**
- **GIVEN** `findings.md` is being written (solved or inconclusive)
- **WHEN** the `## Publishability Assessment` section is generated
- **THEN** it evaluates three dimensions: (1) **Rigor** — whether the methodology, evidence collection, and statistical treatment meet publication-grade standards, (2) **Novelty** — whether the results advance beyond what the literature already establishes, distinguishing between `novel` (no prior art), `incremental` (extends prior work), and `replication` (reproduces known findings). Incremental contributions are noted as potentially suitable for workshop papers or short communications, while fully novel contributions may warrant a full paper, (3) **Significance** — whether the findings address a meaningful question with practical or theoretical impact. Each dimension receives a brief assessment. The section concludes with a verdict: `publishable`, `publishable-with-revisions`, or `not-publishable`. For `publishable-with-revisions` and `not-publishable` verdicts, the assessment includes 2-3 concrete, actionable suggestions for improving publishability (e.g., "gather additional data on X", "compare results against <method> from REF-NNN", "narrow scope to <specific aspect> where the contribution is clearest")

**F-10.4: article-abstract.md written alongside findings**
- **GIVEN** `findings.md` is being written (solved or inconclusive)
- **WHEN** the loop exits
- **THEN** `article-abstract.md` is written with a formal academic abstract (Background, Methods, Results, Conclusions), 200-350 words in length, suitable for conference or journal submission. It includes keywords, hypothesis count, iteration count, and outcome metadata

## Open Questions

- ~~OQ-01~~: Resolved — fixed at 5 per invocation. Operator can re-invoke for another 5-iteration session.
- OQ-02: Should findings.md include a cost/token summary of the research session?
- ~~OQ-03~~: Resolved — `/refining-problem` is no longer user-invocable. The orchestrator is the sole entry point.

## Assumptions

- A-01: [ASSUMPTION] If no initial description is provided on first run, the skill will infer the problem from the slug name alone, producing a less-informed first draft.
- A-02: [ASSUMPTION] The `/researching-literature` skill can fetch content from any publicly accessible URL. Paywalled or gated content is handled gracefully by recording the URL for manual access.
- A-03: [ASSUMPTION] All hypothesis files within a single problem directory follow the same structural contract. Third-party files placed in the directory that do not conform are ignored by the orchestrator.
