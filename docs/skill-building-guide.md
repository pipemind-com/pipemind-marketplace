Here is a complete and exhaustive extraction of the principles, technical requirements, design patterns, and deployment strategies from Anthropic's guide.

Given the focus on architecting reliable, composable workflows, this breakdown emphasizes the structural mechanics, programmatic API controls, and multi-tool orchestration required to build robust agentic capabilities.

### 1. Core Architecture and Mechanics

A skill is a packaged folder containing instructions that teach Claude how to execute specific workflows, preventing the need to re-prompt complex domain expertise in every session.

* **Progressive Disclosure:** Skills manage context windows efficiently using a three-level system:
* 
**Level 1 (YAML Frontmatter):** Always loaded in the system prompt to dictate when the skill triggers.


* 
**Level 2 (SKILL.md Body):** Loaded into context only when Claude determines the skill is relevant.


* 
**Level 3 (Linked Files):** Bundled scripts or reference documents that Claude can navigate to dynamically.




* 
**Composability & Portability:** Claude can load multiple skills simultaneously. A skill authored once works identically across the API, Claude Code, and Claude.ai.


* 
**The Skills vs. MCP Paradigm:** If Model Context Protocol (MCP) represents the "professional kitchen" providing raw access to tools and data, skills are the "recipes". MCP defines *what* Claude can do (connectivity), while skills define *how* Claude should do it (knowledge and methodology).



### 2. Technical and Structural Requirements

Strict adherence to file and naming conventions is required for a skill to compile and trigger correctly.

* **Folder and File Structure:**
* The primary file must be named exactly `SKILL.md` (case-sensitive).


* The skill folder name must use kebab-case (e.g., `notion-project-setup`), with no spaces or capital letters.


* Do not include a `README.md` inside the skill folder itself; all documentation goes into `SKILL.md` or a `references/` directory.




* **YAML Frontmatter Rules:**
* 
**Required Fields:** `name` (must match folder kebab-case) and `description`.


* 
**The Description Field:** Must clearly state *what* the skill does and *when* to use it (including specific user trigger phrases), staying under 1024 characters.


* 
**Strict Security Restrictions:** You must absolutely avoid using XML angle brackets (`<` or `>`) in the YAML frontmatter, as this could lead to system prompt injection. Additionally, skill names cannot contain "claude" or "anthropic".




* 
**Writing Instructions:** * Use specific, actionable language and reference bundled scripts or guides clearly.


* Provide explicit error-handling steps (e.g., how to resolve an "MCP Connection Failed" error).





### 3. Core Use Cases and Design Patterns

When building the execution logic, the guide outlines two mental models: **Problem-first** (users describe outcomes, the skill orchestrates tools) and **Tool-first** (users have a tool connected, the skill provides the optimal workflow).

**Three Primary Categories:**

* 
**Document & Asset Creation:** Formatting code, documents, or UI designs using internal capabilities.


* 
**Workflow Automation:** Step-by-step processes with validation gates.


* 
**MCP Enhancement:** Providing the necessary logic to sequence tool calls effectively.



**Five Execution Patterns:**

1. 
**Sequential Workflow Orchestration:** Explicit step ordering with strict dependencies and rollback instructions.


2. 
**Multi-MCP Coordination:** Passing data sequentially across multiple isolated services (e.g., from Figma, to Drive, to Linear, to Slack).


3. 
**Iterative Refinement:** Generating a draft, executing a local validation script (`scripts/check_report.py`), and looping regeneration until quality thresholds are met.


4. 
**Context-Aware Tool Selection:** Using decision trees to select the right tool based on file type or context (e.g., routing code files to GitHub vs. large files to cloud storage).


5. 
**Domain-Specific Intelligence:** Embedding compliance checks or gating logic before an action is permitted.



### 4. Testing, Iteration, and Telemetry

Testing frameworks scale based on the deployment surface: manual (Claude.ai), scripted automated tests (Claude Code), or programmatic evaluation suites (Skills API).

* **Testing Protocol:**
* 
**Triggering Tests:** Ensure the skill loads on obvious and paraphrased tasks, but explicitly ignores unrelated queries.


* 
**Functional Tests:** Verify complete workflows with zero API failures and proper edge-case handling.


* 
**Performance Benchmarks:** Track token consumption and total tool calls against a baseline run without the skill enabled.




* 
**The skill-creator Tool:** Anthropic provides a native skill that can interactively generate frontmatter, suggest triggers, and flag structural vulnerabilities in about 15-30 minutes.



### 5. Deployment and API Integration

While individuals can manually upload zipped skills to the Claude UI, larger system deployments rely on the API.

* 
**API Execution:** Managing skills programmatically utilizes the `/v1/skills` endpoint and the `container.skills` parameter within the Messages API.


* 
*Note:* API deployment currently requires the Code Execution Tool beta to provide a secure runtime environment.


* 
**Distribution Best Practices:** Host the open-source skill in a public GitHub repository with a clear repository-level README, then explicitly link to the skill within your external MCP server documentation.



### 6. Troubleshooting and Optimization

* 
**Upload Failures:** Often caused by a typo in `SKILL.md` casing, missing YAML delimiters, or unclosed string quotes.


* 
**Over-triggering:** If a skill activates erroneously, add specific negative triggers to the description (e.g., "Do NOT use for simple data exploration").


* 
**Instruction Adherence Failures:** If Claude ignores steps, move critical instructions to the top, bundle a deterministic validation script instead of relying on language logic, or add explicit operational encouragement (e.g., "Take your time to do this thoroughly").


* 
**Context Bloat:** If responses degrade, push detailed reference text into the `references/` folder and keep the main `SKILL.md` strictly under 5,000 words.



---

Would you like me to draft a template `SKILL.md` applying the "Iterative Refinement" and "Multi-MCP Coordination" patterns for one of the specialized agents you are developing?
