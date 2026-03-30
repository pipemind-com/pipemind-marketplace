# References

Topic: Prompt engineering token reduction, agentic workflows, context window management, LLM cost reduction

---

## REF-001: Prompt Compression for Large Language Models: A Survey

- **Authors:** Zongqian Li, Yinhong Liu, Yixuan Su, Nigel Collier
- **Year:** 2024
- **Type:** Peer-reviewed article (Conference, Review)
- **URL:** https://arxiv.org/abs/2410.12388
- **Downloaded:** li-2024-prompt-compression-survey.pdf

**Relevance:** Comprehensive survey (53 citations) covering the full taxonomy of prompt compression methods for LLMs, including token pruning, soft prompt tuning, and generative compression. Serves as the definitive entry point for understanding the landscape of token reduction techniques and their trade-offs across different task types.

---

## REF-002: Active Context Compression: Autonomous Memory Management in LLM Agents

- **Authors:** Nikhil Verma
- **Year:** 2026
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2601.07190
- **Downloaded:** verma-2026-active-context-compression.pdf

**Relevance:** Introduces active context compression where LLM agents autonomously decide which information to preserve or discard, rather than relying on passive truncation or static summarization. Directly addresses the core challenge of context window management in agentic workflows operating over extended interactions.

---

## REF-003: TACO-RL: Task Aware Prompt Compression Optimization with Reinforcement Learning

- **Authors:** Shivam Shandilya, Menglin Xia, Supriyo Ghosh, Huiqiang Jiang, Jue Zhang, Qianhui Wu, Victor Ruhle
- **Year:** 2024
- **Type:** Peer-reviewed article (Conference)
- **URL:** https://arxiv.org/abs/2409.13035
- **Downloaded:** shandilya-2024-taco-rl.pdf

**Relevance:** Uses reinforcement learning to optimize prompt compression in a task-aware manner, learning which tokens are expendable for a given downstream task. Demonstrates that compression ratios can be significantly improved when the compressor is trained with task-specific reward signals rather than generic information-theoretic objectives.

---

## REF-004: In-Context Distillation with Self-Consistency Cascades: A Simple, Training-Free Way to Reduce LLM Agent Costs

- **Authors:** Vishnu Sarukkai, Asanshay Gupta, James Hong, Michael Gharbi, Kayvon Fatahalian
- **Year:** 2025
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2512.02543
- **Downloaded:** sarukkai-2025-in-context-distillation.pdf

**Relevance:** Presents a training-free method using self-consistency cascades to reduce LLM agent costs. Smaller models handle initial requests, escalating to larger models only when self-consistency checks fail. Directly targets cost reduction in agentic deployments without requiring fine-tuning or retraining.

---

## REF-005: Structured Distillation for Personalized Agent Memory: 11x Token Reduction with Retrieval Preservation

- **Authors:** S. Lewis
- **Year:** 2026
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2603.13017
- **Downloaded:** lewis-2026-structured-distillation-agent-memory.pdf

**Relevance:** Demonstrates 11x token reduction in agent memory systems by distilling conversation history into structured representations while preserving retrieval effectiveness. Directly applicable to long-running agentic workflows where accumulated context becomes a major cost driver.

---

## REF-006: Contextual Memory Virtualisation: DAG-Based State Management and Structurally Lossless Trimming for LLM Agents

- **Authors:** C. Santoni
- **Year:** 2026
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2602.22402
- **Downloaded:** santoni-2026-contextual-memory-virtualisation.pdf

**Relevance:** Proposes a DAG-based approach to managing agent state, replacing linear context accumulation with branching state graphs that enable structurally lossless trimming. Particularly relevant for multi-step agentic workflows with branching decision paths, offering an architectural alternative to compression-based approaches.

---

## REF-007: Behavior-Equivalent Token: Single-Token Replacement for Long Prompts in LLMs

- **Authors:** Jiancheng Dong, Pengyue Jia, Jingyu Peng, Maolin Wang, Yuhao Wang, Lixin Su, Xin Sun, Shuaiqiang Wang, Dawei Yin, Xiangyu Zhao
- **Year:** 2025
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2511.23271
- **Downloaded:** dong-2025-behavior-equivalent-token.pdf

**Relevance:** Pushes prompt compression to the extreme by replacing entire long prompts with a single learned token that preserves behavioral equivalence. Relevant to reducing the cost of repetitive system prompts and lengthy instruction sets that appear in every agentic turn.

---

## REF-008: Concise and Precise Context Compression for Tool-Using Language Models

- **Authors:** Yang Xu, ylfeng, Honglin Mu, Yutai Hou, Yitong Li, Xinghao Wang, Wanjun Zhong, Zhongyang Li, Dandan Tu, Qingfu Zhu, Min Zhang, Wanxiang Che
- **Year:** 2024
- **Type:** Peer-reviewed article (Conference)
- **URL:** https://arxiv.org/abs/2407.02043
- **Downloaded:** xu-2024-concise-precise-context-compression.pdf

**Relevance:** Specifically targets context compression for tool-using LLM agents, addressing the problem that tool documentation consumes large portions of the context window on every call. Achieves up to 16x compression via selective retention of key information (tool/parameter names) and block-wise variable-length compression. Directly applicable to agentic workflows that invoke external tools.

---

## REF-009: xRAG: Extreme Context Compression for Retrieval-augmented Generation with One Token

- **Authors:** Xin Cheng, Xun Wang, Xingxing Zhang, Tao Ge, Si-Qing Chen, Furu Wei, Huishuai Zhang, Dongyan Zhao
- **Year:** 2024
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2405.13792
- **Downloaded:** cheng-2024-xrag.pdf

**Relevance:** Achieves extreme context compression by reinterpreting dense retrieval embeddings as a modality fused directly into the language model, reducing retrieved documents to single-token representations. Reduces FLOPs by 3.53x while matching uncompressed performance. Foundational work (94 citations) for understanding how retrieval context can be radically compressed in RAG-based agent architectures.

---

## REF-010: SCOPE: A Generative Approach for LLM Prompt Compression

- **Authors:** Tinghui Zhang, Yifan Wang, Daisy Zhe Wang
- **Year:** 2025
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2508.15813
- **Downloaded:** zhang-2025-scope.pdf

**Relevance:** Introduces a generative approach to prompt compression that rewrites prompts into shorter but semantically equivalent forms, as opposed to token-pruning or embedding-based methods. Represents a distinct paradigm (natural language rewriting) for reducing token counts that can be applied without model modifications, making it practical for agentic workflows using API-based LLMs.

---

## REF-011: Multi-Agent Collaboration Mechanisms: A Survey of LLMs

- **Authors:** Khanh-Tung Tran, Dung Dao, Minh-Duong Nguyen, Quoc-Viet Pham, Barry O'Sullivan, Hoang D. Nguyen
- **Year:** 2025
- **Type:** Peer-reviewed article (Survey)
- **URL:** https://arxiv.org/abs/2501.06322
- **Downloaded:** Not available

**Relevance:** Comprehensive survey (357 citations) characterizing collaboration mechanisms in LLM-based multi-agent systems across key dimensions: actors, types (cooperation, competition, coopetition), structures (peer-to-peer, centralized, distributed), strategies, and coordination protocols. Directly maps the design space for understanding where redundancy arises in multi-agent coordination and which structural patterns affect delegation efficiency.

---

## REF-012: A survey on LLM-based multi-agent systems: workflow, infrastructure, and challenges

- **Authors:** Xinyi Li, Sai Wang, Siqi Zeng, Yu Wu, Yi Yang
- **Year:** 2024
- **Type:** Peer-reviewed article (Survey)
- **URL:** https://doi.org/10.1007/s44336-024-00009-2
- **Downloaded:** Not available

**Relevance:** Highly cited survey (372 citations) presenting a unified five-component framework (profile, perception, self-action, mutual interaction, evolution) for LLM-based MAS. Identifies infrastructure-level challenges including communication overhead and redundant processing between agents, providing theoretical grounding for redundancy elimination strategies in multi-agent workflows.

---

## REF-013: KVFlow: Efficient Prefix Caching for Accelerating LLM-Based Multi-Agent Workflows

- **Authors:** Zaifeng Pan, Ajjkumar Patel, Zhengding Hu, Yipeng Shen, Yue Guan, Wanlu Li, Lianhui Qin, Yida Wang, Yufei Ding
- **Year:** 2025
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2507.07400
- **Downloaded:** Not available

**Relevance:** Directly addresses redundant computation in multi-agent workflows via workflow-aware KV cache management. Introduces Agent Step Graphs to predict future agent activation and a steps-to-execution eviction policy, achieving up to 2.19x speedup over baseline. Core contribution to eliminating redundant prefix computation when multiple agents share context in parallel delegation patterns.

---

## REF-014: KVCOMM: Online Cross-context KV-cache Communication for Efficient LLM-based Multi-agent Systems

- **Authors:** Hancheng Ye, Zhengqing Gao, Mingyuan Ma, Qinsi Wang, Yuzhe Fu, M. Chung, Yueqian Lin, Zhijian Liu, Jianyi Zhang, Danyang Zhuo, Yiran Chen
- **Year:** 2025
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2510.12872
- **Downloaded:** Not available

**Relevance:** Tackles the core problem of repeated reprocessing of overlapping contexts across agents in multi-agent pipelines. Proposes a training-free framework that reuses KV-caches across agents with diverging prefixes by aligning cache offsets via anchor pools, achieving over 70% reuse rate and up to 7.8x speedup. Directly relevant to eliminating redundant computation in parallel sub-agent delegation.

---

## REF-015: DroidSpeak: KV Cache Sharing for Cross-LLM Communication and Multi-LLM Serving

- **Authors:** Yuhan Liu, Yuyang Huang, Jiayi Yao, Shaoting Feng, Zhuohan Gu, Kuntai Du, Hanchen Li, Yihua Cheng, Junchen Jiang, Shan Lu, Madan Musuvathi, Esha Choukse
- **Year:** 2024
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2411.02820
- **Downloaded:** Not available

**Relevance:** First system enabling KV cache reuse across different LLMs sharing the same architecture -- directly applicable to multi-agent systems where heterogeneous specialized models process overlapping context. Achieves up to 4x throughput improvement and 3.1x faster prefill with negligible quality loss, establishing feasibility of cross-model redundancy elimination.

---

## REF-016: Tree Training: Accelerating Agentic LLMs Training via Shared Prefix Reuse

- **Authors:** Shaojie Wang, Jinghui Wang, Yinghan Cui, Xuxing Chen, Chao Wang, Liang Huang, Xiaojiang Zhang, Junyi Peng, Lihua Wan, Haotian Zhang, Bin Chen
- **Year:** 2025
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2511.00413
- **Downloaded:** Not available

**Relevance:** Addresses redundancy at the training level for agentic LLMs where multi-turn trajectories branch into tree-structured paths from shared prefixes. The Gradient Restoration technique computes each shared prefix exactly once while remaining mathematically equivalent to independent training, achieving 6.2x speedup. Demonstrates that tree-structured modeling of agent execution paths is key to eliminating redundant computation.

---

## REF-017: Hear Both Sides: Efficient Multi-Agent Debate via Diversity-Aware Message Retention

- **Authors:** M. Nguyen, A. Nguyen, D. Nguyen, S. Venkatesh, Hung Le
- **Year:** 2026
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2603.20640
- **Downloaded:** Not available

**Relevance:** Directly addresses noise and redundancy in multi-agent communication by selectively retaining only maximally diverse agent responses rather than broadcasting all messages. The Diversity-Aware Retention (DAR) framework demonstrates that filtering redundant inter-agent messages improves both efficiency and reasoning quality as agent count scales -- a key insight for sub-agent coordination efficiency.

---

## REF-018: Beyond Self-Talk: A Communication-Centric Survey of LLM-Based Multi-Agent Systems

- **Authors:** Bingyu Yan, Xiaoming Zhang, Litian Zhang, Lian Zhang, Ziyi Zhou, Dezhuang Miao, Chaozhuo Li
- **Year:** 2025
- **Type:** Peer-reviewed article (Survey)
- **URL:** https://arxiv.org/abs/2502.14321
- **Downloaded:** Not available

**Relevance:** Survey analyzing LLM-MAS from a communication-centric perspective, integrating system-level communication (architecture, goals, protocols) with internal communication (strategies, paradigms, content). Identifies communication efficiency as a key challenge and analyzes how different communication patterns affect coordination overhead -- directly informing the design of redundancy-minimizing delegation patterns.

---

## REF-019: MegaAgent: A Large-Scale Autonomous LLM-based Multi-Agent System Without Predefined SOPs

- **Authors:** Qian Wang, Tianyu Wang, Zhenheng Tang, Qinbin Li, Nuo Chen, Jingsheng Liang, Bingsheng He
- **Year:** 2024
- **Type:** Peer-reviewed article (ACL 2025 Findings)
- **URL:** https://arxiv.org/abs/2408.09955
- **Downloaded:** Not available

**Relevance:** Demonstrates dynamic task decomposition and parallel execution at scale (up to 590 agents) without predefined Standard Operating Procedures. MegaAgent's approach to generating agents based on task complexity and enabling efficient communication establishes practical patterns for delegating tasks to sub-agents while minimizing coordination overhead and redundant work at scale.

---

## REF-020: Talk to Right Specialists: Routing and Planning in Multi-agent System for Question Answering

- **Authors:** Feijie Wu, Zitao Li, Fei Wei, Yaliang Li, Bolin Ding, Jing Gao
- **Year:** 2025
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2501.07813
- **Downloaded:** Not available

**Relevance:** Proposes RopMura with intelligent routing that selects only the most relevant specialist agents based on knowledge boundaries, plus a planner that decomposes complex queries into manageable steps. This routing-first approach directly eliminates redundancy by avoiding unnecessary agent invocations, reducing retrieval overhead in cross-domain coordination of parallel sub-agents.

---

## REF-021: From Static Templates to Dynamic Runtime Graphs: A Survey of Workflow Optimization for LLM Agents

- **Authors:** Ling Yue, Kushal Raj Bhandari, Ching-Yun Ko, Dhaval Patel, Shuxin Lin, Nianjun Zhou, Jianxi Gao, Pin-Yu Chen, Shaowu Pan
- **Year:** 2026
- **Type:** Review (Survey)
- **URL:** https://arxiv.org/abs/2603.22386
- **Downloaded:** Not available

**Relevance:** Most recent survey treating LLM agent workflows as agentic computation graphs (ACGs), distinguishing static vs. dynamic workflow structures and analyzing optimization along three dimensions: when structure is determined, what is optimized, and which evaluation signals guide optimization. Introduces structure-aware evaluation incorporating execution cost -- directly relevant to measuring and reducing redundancy in parallel task delegation.

---

## REF-023: LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression

- **Authors:** Zhuoshi Pan, Qianhui Wu, Huiqiang Jiang, Menglin Xia, et al.
- **Year:** 2024
- **Type:** Peer-reviewed article (Conference)
- **URL:** https://arxiv.org/abs/2403.12968
- **Downloaded:** Not available

**Relevance:** Definitive paper on task-agnostic extractive prompt compression (230 citations). Formulates compression as token classification using a bidirectional Transformer encoder. Achieves 2x-5x compression ratios with 1.6x-2.9x end-to-end latency improvement. Directly supports the claim that extractive compression preserves task performance at moderate compression ratios — the same approach applicable to skill instruction files.

---

## REF-024: Separating Constraint Compliance from Semantic Accuracy: A Novel Benchmark for Evaluating Instruction-Following Under Compression

- **Authors:** Rahul Baxi
- **Year:** 2025
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2512.17920
- **Downloaded:** Not available

**Relevance:** Introduces the CDCT benchmark separating constraint compliance from semantic accuracy under 5 compression levels. Finds a universal U-curve: constraint violations peak at medium compression (~27 words, c=0.5), not at extreme compression. RLHF-trained helpfulness is the dominant cause of compliance failures (removing helpfulness signals improves CC by 598%). Directly challenges naive compression approaches by showing that the 40% reduction target sits near the compliance-violation danger zone for automated compression. Key counterexample for the hypothesis.

---

## REF-025: The Compression Paradox in LLM Inference: Provider-Dependent Energy Effects of Prompt Compression

- **Authors:** Warren Johnson
- **Year:** 2026
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2603.23528
- **Downloaded:** Not available

**Relevance:** Empirical study across 28,421 API trials showing compression ratios of 0.7 cause pass rates to drop from 26% to 1.5% on standard benchmarks (HumanEval, MBPP, GSM8K, MATH, MMLU). Also finds output expansion under heavy compression can increase total token count by up to +2,140%. Establishes that input-token reduction alone is unreliable; model selection and output-length control are more effective. Provides a strong counterexample to automated compression claims at the 40% level.

---

## REF-026: Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing

- **Authors:** Dujian Ding, Ankur Mallick, Chi Wang, Robert Sim, Subhabrata Mukherjee, Victor Rühle, L. Lakshmanan, A. Awadallah
- **Year:** 2024
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2404.14618
- **Downloaded:** Not available

**Relevance:** Proposes routing queries between a small (cheap) and large (capable) LLM based on predicted query difficulty and a tunable quality threshold. Achieves up to 40% fewer calls to the large model with no drop in response quality. Directly evidences that task-complexity-aware model selection preserves quality while reducing cost — the core mechanism underlying Hypothesis 02's claim that structured generation tasks can be routed to Sonnet without quality loss.

---

## REF-027: FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance

- **Authors:** Lingjiao Chen, M. Zaharia, James Y. Zou
- **Year:** 2023
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2305.05176
- **Downloaded:** Not available

**Relevance:** Foundational work (504 citations) on LLM cascade strategies for cost reduction. Demonstrates that combining LLMs with an adaptive cascade can match GPT-4 performance with up to 98% cost reduction. Establishes that model-tier selection is the highest-leverage optimization for LLM inference cost — directly supporting the premise that routing generating-hypotheses from Opus to Sonnet is sufficient for pattern-following tasks.

---

## REF-028: Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey

- **Authors:** Yasmin Moslem, John D. Kelleher
- **Year:** 2026
- **Type:** Review (Survey)
- **URL:** https://arxiv.org/abs/2603.04445
- **Downloaded:** Not available

**Relevance:** Comprehensive 2026 survey of multi-LLM routing and cascading paradigms, including query-difficulty, uncertainty quantification, and reinforcement learning approaches. Establishes the theoretical framework that static model deployment is suboptimal and that routing systems leveraging specialized model capabilities outperform even the most powerful individual models. Directly contextualizes the model downgrade hypothesis within the broader routing literature.

---

## REF-029: Doing More with Less: A Survey on Routing Strategies for Resource Optimisation in LLM-Based Systems

- **Authors:** C. Varangot-Reille, Christophe Bouvard, Antoine Gourru, Mathieu Ciancone, Marion Schaeffer, François Jacquenet
- **Year:** 2025
- **Type:** Review (Survey)
- **URL:** https://arxiv.org/abs/2502.00409
- **Downloaded:** Not available

**Relevance:** Formalizes LLM routing as a performance-cost optimization problem and surveys similarity-based, supervised, RL-based, and generative routing methods. Notes that generalist LLMs (explicitly naming Claude-Sonnet) perform well across a wide range of tasks but incur disproportionate cost for simpler queries. Provides the empirical and theoretical grounding for distinguishing which tasks require large-model capability vs. which are well-served by mid-tier models.

---

## REF-030: AdaptEvolve: Improving Efficiency of Evolutionary AI Agents through Adaptive Model Selection

- **Authors:** Pretam Ray, P. Brahma, Zicheng Liu, E. Barsoum
- **Year:** 2026
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2602.11931
- **Downloaded:** Not available

**Relevance:** Applies confidence-driven adaptive model selection in evolutionary agentic systems (which repeatedly invoke LLMs). Achieves 37.9% cost reduction while retaining 97.5% of large-model accuracy by routing only low-confidence steps to the large model. Provides direct empirical evidence that iterative/creative agentic tasks (akin to hypothesis generation) can tolerate small-model routing with minimal quality loss when the task structure is well-defined.

---

## REF-022: A Survey on LLM-based Multi-Agent System: Recent Advances and New Frontiers in Application

- **Authors:** Shuaihang Chen, Yuanxing Liu, Wei Han, Weinan Zhang, Ting Liu
- **Year:** 2024
- **Type:** Review (Survey)
- **URL:** https://arxiv.org/abs/2412.17481
- **Downloaded:** Not available

**Relevance:** Comprehensive survey (50 citations) covering the definition, framework, and applications of LLM-MAS across complex task solving, scenario simulation, and generative agent evaluation. Highlights challenges in scaling multi-agent coordination and provides the applications-oriented perspective complementing the infrastructure-focused surveys in this collection.

---

## REF-031: Can LLMs Generate Novel Research Ideas? A Large-Scale Human Study with 100+ NLP Researchers

- **Authors:** Chenglei Si, Diyi Yang, Tatsunori Hashimoto
- **Year:** 2024
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2409.04109
- **Downloaded:** Not available

**Relevance:** Large-scale human study (314 citations, 26 influential) showing LLM-generated research ideas are judged more novel than human expert ideas, but explicitly identifies "lack of diversity in generation" as a key open problem in LLM research agents. Directly relevant to hypothesis count calibration: fewer hypotheses exacerbate the known diversity deficit in LLM ideation, suggesting that reducing from 4 to 2 hypotheses risks converging on a narrow cluster of related ideas.

---

## REF-032: Hypothesis Generation with Large Language Models

- **Authors:** Yangqiaoyu Zhou, Haokun Liu, Tejes Srivastava, Hongyuan Mei, Chenhao Tan
- **Year:** 2024
- **Type:** Peer-reviewed article (Conference)
- **URL:** https://arxiv.org/abs/2404.04326
- **Downloaded:** Not available

**Relevance:** Demonstrates that LLM hypothesis generation quality depends critically on an exploration-exploitation tradeoff informed by multi-armed bandit reward signals. With too few hypotheses (exploitation-heavy), the search space is underexplored; quality gains require iterative expansion across diverse hypothesis candidates. The paper's bandit-inspired update mechanism implicitly relies on a sufficient pool of initial hypotheses to achieve meaningful coverage improvements.

---

## REF-033: A Survey on Hypothesis Generation for Scientific Discovery in the Era of Large Language Models

- **Authors:** A. Alkan et al.
- **Year:** 2025
- **Type:** Peer-reviewed article (Review)
- **URL:** https://arxiv.org/abs/2504.05496
- **Downloaded:** Not available

**Relevance:** Comprehensive survey of LLM hypothesis generation methods (10 citations), covering novelty-boosting and structured reasoning techniques for improving hypothesis quality. Identifies hypothesis diversity as a distinct quality dimension from novelty and correctness — meaning fewer hypotheses do not simply reduce cost proportionally but can degrade coverage of the mechanism space even when each remaining hypothesis is individually high-quality.

---

## REF-034: Hypothesis Hunting with Evolving Networks of Autonomous Scientific Agents

- **Authors:** Tennison Liu, Silas Ruhrberg Estévez, David Bentley, M. Schaar
- **Year:** 2025
- **Type:** Peer-reviewed article (Review)
- **URL:** https://arxiv.org/abs/2510.08619
- **Downloaded:** Not available

**Relevance:** Demonstrates that effective autonomous scientific discovery requires accumulation of results along the "diversity-quality-novelty frontier" through sustained broad exploration. Agents with heterogeneous behaviors self-organizing into evolving networks outperform homogeneous or minimally-structured systems. Directly challenges the hypothesis that 2 hypotheses are sufficient: the diversity dimension of research quality requires maintaining multiple independent exploratory tracks.

---

## REF-035: Rethinking the Value of Multi-Agent Workflow: A Strong Single Agent Baseline

- **Authors:** Jiawei Xu, A. Koesdwiady, Sisong Bei, Yan Han, Baixiang Huang, Dakuo Wang, Yutong Chen, Z. Wang, Peihao Wang, Pan Li, Ying Ding
- **Year:** 2026
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2601.12307
- **Downloaded:** Not available

**Relevance:** Demonstrates that homogeneous multi-agent workflows (where all agents share the same base LLM) can be collapsed into a single-agent multi-turn conversation with KV cache reuse, matching workflow accuracy at lower inference cost. Introduces OneFlow, an algorithm that automatically converts multi-agent workflows into single-agent execution, directly evidencing that spawning multiple sub-agents for a shared-model workflow incurs unnecessary overhead compared to sequential single-agent execution with shared context.

---

## REF-036: DynTaskMAS: A Dynamic Task Graph-driven Framework for Asynchronous and Parallel LLM-based Multi-Agent Systems

- **Authors:** Junwei Yu, Yepeng Ding, Hiroyuki Sato
- **Year:** 2025
- **Type:** Peer-reviewed article (Conference)
- **URL:** https://arxiv.org/abs/2503.07675
- **Downloaded:** Not available

**Relevance:** Introduces a Dynamic Task Graph Generator that decomposes tasks while preserving logical dependencies, enabling async parallel execution across agents. Achieves 21–33% reduction in execution time (larger gains for more complex tasks) and near-linear throughput scaling to 16 concurrent agents. Establishes that dependency-aware task graph scheduling — rather than naive sequential spawning — is the key mechanism for eliminating redundant sequential overhead in multi-step pipelines.

---

## REF-037: Flow: Modularized Agentic Workflow Automation

- **Authors:** Boye Niu, Yiliao Song, Kai Lian, Yifan Shen, Yu Yao, Kun Zhang, Tongliang Liu
- **Year:** 2025
- **Type:** Peer-reviewed article (Conference, ICLR 2025)
- **URL:** https://arxiv.org/abs/2501.07834
- **Downloaded:** Not available

**Relevance:** Models multi-agent workflows as activity-on-vertex (AOV) graphs and enables dynamic subtask allocation via continuous workflow refinement based on historical performance. Emphasizes modularity by evaluating parallelism and dependency complexity, enabling efficient concurrent subtask execution. Directly relevant to task merging: the AOV formulation makes explicit which steps can be merged (low parallelism, low dependency cost) versus which must remain distinct agents.

---

## REF-038: ALAS: Transactional and Dynamic Multi-Agent LLM Planning

- **Authors:** Longling Geng, Edward Y. Chang
- **Year:** 2025
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2511.03094
- **Downloaded:** Not available

**Relevance:** Achieves 60% token reduction and 1.82× speedup in multi-agent planning by using localized repair (editing only the minimal affected subgraph on failure) instead of global recomputation, and by isolating validation context to prevent mid-context attrition. The workflow IR (mapping to Amazon States Language / Argo Workflows) enables precise identification of which sub-tasks can share context versus which require independent execution, directly informing task-merging boundary decisions.

---

## REF-039: Astraea: A State-Aware Scheduling Engine for LLM-Powered Agents

- **Authors:** Hongqiu Ni, Jiabao Zhang, Guopeng Li, Zilong Wang, Ruiqi Wu, Chi Zhang, Haisheng Tan
- **Year:** 2025
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2512.14142
- **Downloaded:** Not available

**Relevance:** Proposes workflow-level (rather than per-segment) scheduling for LLM agents whose multi-step pipelines alternate between compute and I/O phases. Uses a state-aware hierarchical scheduler with request history and future prediction to classify I/O-intensive vs. compute-intensive steps, reducing average job completion time by 25.5%. Directly relevant to understanding the per-step overhead structure in agentic pipelines and how scheduling granularity affects end-to-end latency.

---

## REF-040: AOrchestra: Automating Sub-Agent Creation for Agentic Orchestration

- **Authors:** Jianhao Ruan, Zhihao Xu, Yiran Peng, Fashen Ren, Zhaoyang Yu, Xinbing Liang, Jinyu Xiang, Bang Liu, Chenglin Wu, Yuyu Luo, Jiayi Zhang
- **Year:** 2026
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2602.03786
- **Downloaded:** Not available

**Relevance:** Introduces a unified sub-agent abstraction (Instruction, Context, Tools, Model tuple) enabling on-the-fly agent creation with explicit performance-cost tradeoffs approaching Pareto efficiency. Achieves 16.28% relative improvement on GAIA/SWE-Bench/Terminal-Bench by spawning specialized executors only when needed, rather than pre-defining a fixed agent topology. Provides the theoretical framing for deciding when task merging (avoiding a spawn) is preferable to delegation, based on task complexity and context overlap.

---

## REF-041: Reasoning on a Budget: A Survey of Adaptive and Controllable Test-Time Compute in LLMs

- **Authors:** Mohammad Ali Alomrani, Yingxue Zhang, Derek Li, Qianyi Sun, Soumyasundar Pal, Zhanguang Zhang, Yaochen Hu, Rohan Deepak Ajwani, Antonios Valkanas, Raika Karimi, Peng Cheng, Yunzhou Wang, Pengyi Liao, Han Huang, Bin Wang, Jianye Hao, Mark Coates
- **Year:** 2025
- **Type:** Review (Survey)
- **URL:** https://arxiv.org/abs/2507.02076
- **Downloaded:** alomrani-2025-reasoning-on-a-budget.pdf

**Relevance:** Comprehensive survey of efficient test-time compute strategies for LLMs, introducing a two-tiered taxonomy: L1-controllability (fixed budget methods) and L2-adaptiveness (dynamic scaling based on input difficulty or model confidence). Directly maps the design space for early-termination and budget-aware stopping criteria applicable to agentic research pipelines. Benchmarks show adaptive approaches reduce token usage substantially without performance loss when confidence-based halt signals are reliable.

---

## REF-042: Think Only When You Need with Large Hybrid-Reasoning Models

- **Authors:** Lingjie Jiang, Xun Wu, Shaohan Huang, Qingxiu Dong, Zewen Chi, Li Dong, Xingxing Zhang, Tengchao Lv, Lei Cui, Furu Wei
- **Year:** 2025
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2505.14631
- **Downloaded:** jiang-2025-think-only-when-you-need.pdf

**Relevance:** Introduces Large Hybrid-Reasoning Models (LHRMs) that adaptively determine whether extended reasoning is needed for a given query, learning to skip expensive computation on simpler problems via two-stage training. The core insight — that a gate can reliably route tasks to bypass expensive downstream phases without quality loss — is directly analogous to a post-literature-review gate that skips experiment design and execution for hypotheses already resolved by prior work.

---

## REF-043: DOVA: Deliberation-First Multi-Agent Orchestration for Autonomous Research Automation

- **Authors:** Aaron Shen, Alfred Shen
- **Year:** 2026
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2603.13327
- **Downloaded:** shen-2026-dova.pdf

**Relevance:** Presents DOVA, a multi-agent research automation system with a six-level adaptive token-budget allocation scheme that reduces inference cost by 40-60% on simple tasks while preserving full reasoning for complex ones. The deliberation-first orchestration pattern — where meta-reasoning gates subsequent tool invocations — is the closest published analog to the hypothesis-05 early-termination gate after literature refinement. Directly supports the feasibility of the 25-50% token reduction claim.

---

## REF-044: CoRefine: Confidence-Guided Self-Refinement for Adaptive Test-Time Compute

- **Authors:** Chen Jin, Ryutaro Tanno, Tom Diethe, P. Teare
- **Year:** 2026
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2602.08948
- **Downloaded:** Not available

**Relevance:** Demonstrates that LLM confidence dynamics reliably signal when to halt refinement, achieving 92.6% precision on confident-halt decisions and approximately 190x token reduction versus exhaustive parallel sampling baselines. The confidence-as-control-signal principle applies directly to agentic pipelines: a post-literature gate using resolution confidence (definitive confirmation or refutation) can short-circuit downstream experiment phases with high reliability, supporting the mechanism proposed in hypothesis-05.

---

## REF-045: Early-Exit Deep Neural Networks: A Comprehensive Survey

- **Authors:** Haseena Rahmath P, Vishal Srivastava, Kuldeep Chaurasia, R. G. Pacheco, R. S. Couto
- **Year:** 2024
- **Type:** Peer-reviewed article (Survey)
- **URL:** https://dl.acm.org/doi/10.1145/3698767
- **Downloaded:** Not available

**Relevance:** Comprehensive survey (53 citations) of multi-exit architectures that stop inference at intermediate layers when confidence is sufficient, covering benefits (speedup, overthinking reduction) and design challenges (threshold miscalibration, training difficulty, performance degradation from premature exits). The documented failure modes — exits firing on false confidence, quality degradation from miscalibrated thresholds — are concrete counterexamples for aggressive early-termination gate designs and must inform threshold-setting in any literature-resolution gate.

---

## REF-046: CIFLEX: Contextual Instruction Flow for Sub-task Execution in Multi-Turn Interactions with a Single On-Device LLM

- **Authors:** Juntae Lee, Jihwan Bang, Seunghan Yang, Simyung Chang
- **Year:** 2025
- **Type:** Peer-reviewed article (Conference)
- **URL:** https://arxiv.org/abs/2510.01239
- **Downloaded:** lee-2025-ciflex.pdf

**Relevance:** Directly addresses the overhead of reprocessing full context when switching between tasks: CIFLEX injects only task-specific instructions into isolated side paths while reusing the KV cache from the main task, then rolls back via cached context after sub-task completion. This is the closest published analog to inline prompt injection for sub-task agents — it demonstrates that selective instruction delivery significantly reduces computational overhead without degrading task performance, directly supporting the mechanism proposed in Hypothesis 06.

---

## REF-047: Agent Primitives: Reusable Latent Building Blocks for Multi-Agent Systems

- **Authors:** Haibo Jin, Kuang Peng, Ye Yu, Xiaopeng Yuan, Haohan Wang
- **Year:** 2026
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2602.03695
- **Downloaded:** jin-2026-agent-primitives.pdf

**Relevance:** Proposes decomposing MAS architectures into reusable primitives (Review, Voting, Planning and Execution) that communicate via KV cache rather than natural-language text, achieving 3-4x token reduction and 12-16.5% accuracy improvement over single-agent baselines. Directly supports the hypothesis that replacing full skill-file loading with structured reuse (here via latent primitives rather than inline prompts) substantially reduces instruction overhead.

---

## REF-048: LLMs Get Lost In Multi-Turn Conversation

- **Authors:** Philippe Laban, Hiroaki Hayashi, Yingbo Zhou, Jennifer Neville
- **Year:** 2025
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2505.06120
- **Downloaded:** laban-2025-llms-get-lost-multi-turn.pdf

**Relevance:** Large-scale study (184 citations) finding all top LLMs exhibit 39% average performance drop in multi-turn vs. single-turn settings, driven primarily by increased unreliability rather than aptitude loss. A key counterexample for inline prompt injection: if Task agents receive only a stripped-down subset of instructions, they may make early wrong assumptions and fail to recover — the same failure mode documented here for underspecified conversational contexts.

---

## REF-049: An Empirical Study on the Effects of System Prompts in Instruction-Tuned Models for Code Generation

- **Authors:** Zaiyu Cheng, Andrea Mastropaolo
- **Year:** 2026
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2602.15228
- **Downloaded:** cheng-2026-system-prompts-code-generation.pdf

**Relevance:** Empirically demonstrates across 360 configurations that increasing system-prompt constraint specificity does not monotonically improve correctness — effectiveness is configuration-dependent and can help or hinder based on alignment with task requirements. Directly challenges the hypothesis that shorter, more targeted inline prompts will always outperform full skill files: task-specific tailoring can degrade performance for some model/task/language combinations.

---

## REF-050: System Prompt Optimization with Meta-Learning

- **Authors:** Yumin Choi, Jinheon Baek, Sung Ju Hwang
- **Year:** 2025
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2505.09666
- **Downloaded:** choi-2025-system-prompt-optimization-meta-learning.pdf

**Relevance:** Shows that a single optimized task-agnostic system prompt (meta-learned across diverse tasks) generalizes effectively to unseen tasks, requiring fewer optimization steps at test time while achieving improved performance. Relevant counterpoint to inline injection: rather than dynamically assembling per-invocation inline prompts, a well-optimized compressed skill file may achieve comparable efficiency through compression rather than fragmentation.

---

## REF-051: LLM Task Interference: An Initial Study on the Impact of Task-Switch in Conversational History

- **Authors:** Akash Gupta, Ivaxi Sheth, Vyas Raina, Mark J. F. Gales, Mario Fritz
- **Year:** 2024
- **Type:** Peer-reviewed article (Conference)
- **URL:** https://arxiv.org/abs/2402.18216
- **Downloaded:** gupta-2024-llm-task-interference.pdf

**Relevance:** Demonstrates that task-switches in conversational history cause significant performance degradation across 15 switch configurations with popular LLMs. A counterexample for inline prompt injection: when agents receive task-specific instructions injected mid-context rather than a coherent full skill file, they may experience task-interference effects that reduce instruction-following reliability.

---

## REF-052: Hierarchical Caching for Agentic Workflows: A Multi-Level Architecture to Reduce Tool Execution Overhead

- **Authors:** Farhana Begum, C. Scott, K. Nyarko, M. Jeihani, F. Khalifa
- **Year:** 2026
- **Type:** Peer-reviewed article (Journal)
- **URL:** https://doi.org/10.3390/make8020030
- **Downloaded:** Not available

**Relevance:** Proposes a multi-level caching architecture for agentic workflows operating at both workflow and tool granularity, achieving 76.5% caching efficiency, 13.3x query processing time reduction, and 73.3% cost reduction. While focused on tool-call caching rather than instruction loading, its architectural patterns for capturing redundancy at different granularities directly apply to whether repeated skill-file reads can be eliminated through structural caching rather than inline injection.

---

## REF-053: AgentDropout: Dynamic Agent Elimination for Token-Efficient and High-Performance LLM-Based Multi-Agent Collaboration

- **Authors:** Zhexuan Wang, Yutong Wang, Xuebo Liu, Liang Ding, Miao Zhang, Jie Liu, Min Zhang
- **Year:** 2025
- **Type:** Peer-reviewed article (Conference)
- **URL:** https://arxiv.org/abs/2503.18891
- **Downloaded:** Not available

**Relevance:** Dynamically eliminates redundant agents and communication edges by optimizing adjacency matrices of communication graphs, achieving 21.6% reduction in prompt token consumption and 18.4% in completion token consumption with a simultaneous performance improvement. The 21.6% figure provides an empirical upper bound for agent-elimination alone without structural redesign, directly calibrating the plausibility of the hypothesis's 50% target and establishing that batching must be paired with additional optimizations to reach it.

---

## REF-054: CodeAgents: A Token-Efficient Framework for Codified Multi-Agent Reasoning in LLMs

- **Authors:** Bruce Yang, Xinfeng He, Huan Gao, Yifan Cao, Xiaofan Li, D. Hsu
- **Year:** 2025
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2507.03254
- **Downloaded:** Not available

**Relevance:** Codifies multi-agent interaction (tasks, plans, feedback, tool invocations) into structured pseudocode with control structures and typed variables, achieving 55-87% reduction in input tokens and 41-70% in output tokens across three benchmarks. The gains come from representation restructuring rather than search consolidation — a challenging counterexample establishing that the >50% target is achievable but via a different mechanism than the one the hypothesis proposes.

---

## REF-055: ICaRus: Identical Cache Reuse for Efficient Multi Model Inference

- **Authors:** Sunghyeon Woo, J. Kil, Hoseung Kim, Minsub Kim, Joonghoon Kim, A. Seo, Sungjae Lee, M. Jo, Jiwon Ryu, Baeseong Park, Sehoon Kwon, Dongsoo Lee
- **Year:** 2026
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2603.13281
- **Downloaded:** Not available

**Relevance:** Enables shared KV cache reuse across multiple specialized models in multi-agent workflows by freezing the logical encoder and fine-tuning only the logical decoder, achieving 11.1x lower P95 latency and 3.8x higher throughput across 8 concurrent models. Supports the hypothesis's core premise that redundant skill reloading is a real and large inefficiency — while challenging its mechanism: the fix is infrastructure-level cache sharing, not application-level search batching.

---

## REF-056: RCR-Router: Efficient Role-Aware Context Routing for Multi-Agent LLM Systems with Structured Memory

- **Authors:** Jun Liu, Zhenglun Kong, Changdi Yang, Fan Yang, Tianqi Li, Peiyan Dong, Joannah Nanjekye, Hao Tang, Geng Yuan, Wei Niu, Wenbin Zhang, Pu Zhao, Xue Lin, Dong-Xu Huang, Yanzhi Wang
- **Year:** 2025
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2508.04903
- **Downloaded:** Not available

**Relevance:** Dynamically selects semantically relevant memory subsets per agent based on role and task stage, reducing token usage up to 30% on multi-hop QA benchmarks while improving or maintaining answer quality. Provides a structural alternative to the batching hypothesis: comparable token reductions come from routing the right context to each agent rather than merging their searches, and this approach preserves the independence of each agent's retrieval context.

---

## REF-057: When Does Divide and Conquer Work for Long Context LLM? A Noise Decomposition Framework

- **Authors:** Zhen Xu, Shang Zhu, Jue Wang, Junlin Wang, Ben Athiwaratkun, Chi Wang, James Zou, Ce Zhang
- **Year:** 2025
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2506.16411
- **Downloaded:** Not available

**Relevance:** Provides a theoretical framework distinguishing three failure modes for long-context tasks: cross-chunk dependence (task noise), model fidelity decay with input length (model noise), and aggregation error. Establishes conditions under which multi-agent chunking is beneficial versus harmful. Directly applicable to Hypothesis 07: C-D-E have high sequential cross-chunk dependence (E needs D's results, D needs C's designs), which creates aggregation error if kept separate but accumulates context if merged. The framework's prediction: merging is net-positive when sequential dependency is structured (not scattered), which matches the C-D-E pattern.

---

## REF-058: The Limits of Long-Context Reasoning in Automated Bug Fixing

- **Authors:** Ravi Raju, Mengmeng Ji, Shubhangi Upasani, Bo Li, Urmish Thakker
- **Year:** 2026
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2602.16069
- **Downloaded:** Not available

**Relevance:** Key counterexample: empirically finds that successful agentic trajectories remain under 20k-30k tokens and that longer accumulated contexts correlate with lower success rates. At 64k tokens, models degrade sharply (7% resolve rate). Concludes that agentic success arises from task decomposition into short-context steps, not from long-context reasoning. Challenges Hypothesis 07: a merged C-D-E agent accumulates hypothesis + experiment design + execution results + conclusions. For complex experiments with substantial output, this may exceed the 20-30k reliability threshold and degrade conclusion quality.

---

## REF-059: MAS-Orchestra: Understanding and Improving Multi-Agent Reasoning Through Holistic Orchestration and Controlled Benchmarks

- **Authors:** Zixuan Ke, Yifei Ming, Austin Xu, Ryan Chin, Xuan-Phi Nguyen, Prathyusha Jwalapuram, Jiayu Wang, Semih Yavuz, Caiming Xiong, Shafiq Joty
- **Year:** 2026
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2601.14652
- **Downloaded:** Not available

**Relevance:** Empirically establishes that MAS gains over single-agent systems depend critically on task structure (Depth, Horizon, Breadth, Parallel, Robustness) — not universal. For Hypothesis 07: high-Depth tasks (complex experiment design requiring multi-step reasoning) and high-Robustness requirements (independent verification of conclusions) may still favor multi-agent separation even when cross-hypothesis parallelism is the only structural parallelism needed. The MASBENCH framework enables principled prediction of which hypothesis types can safely use merged C-D-E.

---

## REF-060: AnyMAC: Cascading Flexible Multi-Agent Collaboration via Next-Agent Prediction

- **Authors:** Song Wang, Zhen Tan, Zihan Chen, Shuang Zhou, Tianlong Chen, Jundong Li
- **Year:** 2025
- **Type:** Conference
- **URL:** https://arxiv.org/abs/2506.17784
- **Downloaded:** Not available

**Relevance:** Proposes replacing static or graph-based inter-agent topologies with a sequential cascade using next-agent prediction and selective per-step context access. The sequential cascade is precisely the internal structure of C→D→E within a hypothesis. This paper validates that a cascade within a single agent handles the same workflow with less overhead than three independent spawns, and that selective context access (each step reads only what it needs from prior steps) mitigates the long-context accumulation risk identified in REF-058 — pointing toward selective rather than full-context merging.

---

## REF-061: The Effect of Multiple Query Representations on Information Retrieval System Performance

- **Authors:** N. Belkin, Colleen Cool, W. Bruce Croft, Jamie Callan
- **Year:** 1993
- **Type:** Peer-reviewed article (Conference)
- **URL:** https://www.semanticscholar.org/paper/64cabac9ca53a6a31dac409d2d8c5a69c5a7da40
- **Downloaded:** Not available

**Relevance:** Landmark paper (213 citations, 28 influential) establishing that combining multiple distinct query representations of the same information need improves retrieval performance over any single query. Provides foundational evidence that query diversity captures coverage a single search cannot, and that the improvement from diversity has diminishing returns as queries overlap. Directly informs how many parallel searches are needed before coverage saturates — the core mechanism hypothesis 08 relies upon.

---

## REF-062: Can ChatGPT Write a Good Boolean Query for Systematic Review Literature Search?

- **Authors:** Shuai Wang, Harrisen Scells, B. Koopman, G. Zuccon
- **Year:** 2023
- **Type:** Peer-reviewed article (Conference)
- **URL:** https://arxiv.org/abs/2302.03495
- **Downloaded:** wang-2023-chatgpt-boolean-query-systematic-review.pdf

**Relevance:** Highly cited study (229 citations) evaluating LLM-generated queries for systematic review literature search. Finds that LLM queries achieve high precision but trade off recall — fewer, higher-precision queries reduce document retrieval volume but risk missing relevant studies. Directly relevant to hypothesis 08's claim that a 2-search strategy retains 80%+ coverage: the results demonstrate that precision-recall tradeoffs are real and depend on topic complexity, and that rapid/reduced searches are appropriate only when recall requirements are modest.

---

## REF-063: Optimal Database Combinations for Literature Searches in Systematic Reviews

- **Authors:** W. Bramer, M. Rethlefsen, J. Kleijnen, O. Franco
- **Year:** 2017
- **Type:** Peer-reviewed article (Review)
- **URL:** https://doi.org/10.1186/s13643-017-0644-y
- **Downloaded:** Not available

**Relevance:** Large empirical study (1,632 citations, 44 influential) measuring how combining multiple search sources affects recall in systematic reviews. Key finding: 16% of included references were found in only one source; a 4-source combination was needed to achieve 95%+ recall in 72% of reviews. Directly challenges hypothesis 08's 80% coverage retention claim — even 4 combined strategies fell below 95% recall in 28% of reviews, and halving to 2 sources risks substantially greater coverage loss, especially for niche or cross-disciplinary topics.

---

## REF-064: SPARC-RAG: Adaptive Sequential-Parallel Scaling with Context Management for Retrieval-Augmented Generation

- **Authors:** Yuxin Yang, Gangda Deng, Ömer Faruk Akgül, Nima Chitsazan, Yash Govilkar, Akasha Tigalappanavara, Shixiong Zhang, Sambit Sahu, Viktor K. Prasanna
- **Year:** 2026
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2602.00083
- **Downloaded:** yang-2026-sparc-rag.pdf

**Relevance:** Introduces adaptive sequential-parallel RAG scaling, explicitly finding that "naive scaling causes context contamination and scaling inefficiency, leading to diminishing or negative returns despite increased computation." Uses targeted, complementary sub-queries per parallel branch for diverse coverage and +6.2 F1 improvement under lower inference cost. Supports the mechanism of hypothesis 08 (complementary queries add value) while warning that naive reduction without adaptive selection risks coverage gaps.

---

## REF-065: DMQR-RAG: Diverse Multi-Query Rewriting for RAG

- **Authors:** Zhicong Li, Jiahao Wang, Zhishu Jiang, Hangyu Mao, Zhongxia Chen, Jiazhen Du, Yuanxing Zhang, Fuzheng Zhang, Di Zhang, Yong Liu
- **Year:** 2024
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2411.13154
- **Downloaded:** li-2024-dmqr-rag.pdf

**Relevance:** Proposes four query rewriting strategies at different levels of information granularity for RAG, plus an adaptive method that minimizes the number of rewrites while optimizing performance. Key finding: diverse queries at varying granularity retrieve complementary document sets that a single rewrite misses; an adaptive 2-strategy approach can optimize coverage-per-query. Directly addresses the core mechanism of hypothesis 08: diverse, well-chosen query designs could approximate 4-query coverage with 2 queries, but uniform reduction without diversity would not.

---

## REF-066: CompactRAG: Reducing LLM Calls and Token Overhead in Multi-Hop Question Answering

- **Authors:** Hao Yang, Zhiyu Yang, Xupeng Zhang, Wei Wei, Yunjie Zhang, Lin Yang
- **Year:** 2026
- **Type:** Preprint
- **URL:** https://arxiv.org/abs/2602.05728
- **Downloaded:** Not available

**Relevance:** Demonstrates that invoking the LLM only twice (sub-question decomposition + final synthesis) achieves competitive accuracy while substantially reducing token consumption versus iterative multi-call RAG baselines. Provides supporting evidence that a small, fixed number of well-structured calls can match more expensive multi-call strategies — the core claim of hypothesis 08 — but requires careful structural design (offline preprocessing + decomposition planning) rather than simple count reduction.

---

## REF-067: Two Heads Are Better Than One: Improving Search Effectiveness Through LLM-Generated Query Variants

- **Authors:** Kun Ran, Marwah Alaofi, Mark Sanderson, Damiano Spina
- **Year:** 2025
- **Type:** Peer-reviewed article (Conference)
- **URL:** https://www.semanticscholar.org/paper/dd5a34880d0686afbdacf638ea80e82284d4df2e
- **Downloaded:** Not available

**Relevance:** Empirically validates that fusing results from LLM-generated query variants with the original user query significantly improves retrieval, especially for low-quality queries. The study focuses on 2-query fusion and demonstrates its benefit, but does not characterize whether a 3rd or 4th variant adds proportional value. Supports the claim that a targeted + broad 2-query design can meaningfully improve coverage over a single query, but leaves open whether 2 queries match the coverage of 4 complementary queries.

---
