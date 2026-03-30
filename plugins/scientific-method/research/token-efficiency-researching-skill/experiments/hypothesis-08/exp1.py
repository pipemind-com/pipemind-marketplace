"""
Experiment 1: Measure Search Result Overlap Across Query Strategies

Computes Jaccard overlap between the 4-search (current refining-hypothesis)
strategy and the 2-search (proposed) strategy for three representative topics.

Data collected manually via Semantic Scholar MCP queries (10 results each):
  - Q1: targeted claim search
  - Q2: mechanism/explanation search
  - Q3: counterexample/failure-mode search
  - Q4: gap-fill broad search
  - Q1': targeted search (same as Q1)
  - Q2': broad search

Paper IDs used are Semantic Scholar S2 IDs.
"""

from collections import Counter

# ─── Topic 1: LLM Prompt Compression ───────────────────────────────────────
# Q1: "LLM prompt compression token reduction accuracy"
t1_q1 = {
    "3bbf541c2a3ce0ffaed3703cd486f0e1b2febb27",  # Token-Budget-Aware LLM Reasoning
    "f8d6c67a825d43790df36d8f93f728772e3d8420",  # Compression Method Matters
    "4c101e9b3a84a793b00d3ed00c5232435420142c",  # SCOPE
    "d4cbbe9b30332ee613ac31d11f16ace95a75f4bd",  # BatchGEMBA
    "65bf6c02c6683ed78291c6e90ef32bd10f88a80d",  # PromptOptMe
    "0b957220f36da0853daf61e896c3251e63a74ce5",  # Compression Paradox
    "7a4f8771974498f20574bfce4352cb88b2b6cd8c",  # Context-Aware Sentence Encoding
    "d54197aa83c4e1972af6003e09b632f8358f8435",  # CompactPrompt
    "93e0e493cca485a05a864cbfd7d471b9a5c80380",  # ProCut
    "88637a2c392f1c185bc282d4abaccc221a0bb291",  # Token-Efficient Prompt Injection
}

# Q2: "prompt compression mechanism token pruning large language models"
t1_q2 = {
    "d9c75a3516464a30d87691f77bdb83523927423b",  # Vision Token Reduction via Attention
    "cbf326517d8983aeb3c4c12d68b4444582c0307a",  # Hybrid-Level Instruction Injection
    "0cad365e499bbcbe6cc4fff828ff616bc3cffcd8",  # ZSPAPrune
    "134a66cc64344b9ef913e0f25c2fab6f4ff92c94",  # ATP-LLaVA
    "399db703de1cf0f6a21aacf3e46dab24e19d58b4",  # OmniZip
    "2eef16d55ce8271dcc1c777f8ec1b1c9e7b75b96",  # AdaTP
    "07cae77b1aae2e30b9b761dab74f0dc203aada20",  # Saliency-driven Dynamic Token Pruning
    "1fd79d93a09e7ddc60982c9d80eb2e574c0c5960",  # Adversarial Robustness VLMs
    "8a37094080af2fd6f3d38c3ff9b19a278a488857",  # A Glimpse to Compress
    "d5ab7aad1a1f7b651b735d956c48473fc94164b2",  # 500xCompressor
}

# Q3: "prompt compression failure modes accuracy degradation counterexample"
t1_q3 = {
    "b2e3af5518fb6ad8082401996bcd241b43c3ef88",  # DIQ-H (VLM hallucination)
    "f31f3a1511ae6da503b7443fa2fde18bae4424f9",  # bitumen-stone (off-topic)
    "2fe0d2c79a94a04d8e7fa098aae5d260fb0a5259",  # impact-induced damage (off-topic)
    "27754f38bff92f75ce606a6342d26e8bf2cfb8bd",  # Post-buckling (off-topic)
    "4db6ca41b3d12bf47e5e7cb57343cb0d04066909",  # Steel-concrete columns (off-topic)
    "abe3b6d260939e1d93a77c04c9fd8b535b61ae22",  # PEEM
    "01e5624c773b65785f5677c900359acc432c0bd8",  # Damage constitutive model (off-topic)
    "bd061be24a6452f14f31267ed1bf01d393353838",  # Automotive hairpin stator (off-topic)
    "6e61c4de33cb1e2bc970385ea6d7488a5d5265d1",  # Optimization Instability Agentic (partial)
    "fcf64da9fa94b04d8e7fa098aae5d260fb0a5259",  # Unstable Prompts Unreliable Seg
}

# Q4: "token efficiency large language model inference cost reduction"
t1_q4 = {
    "afe3a62e473de50835a7ac478e045869e6443309",  # AIBrix
    "1d67e41d0304aa9a339f92cabe61c2354f01e739",  # TRIM
    "0fa443adf81f204a3907257e4ed97c83b081a59a",  # JointCloud LLM
    "b87fa52aa23fc6141ee0d1e05aa2ec169bc97b51",  # ARS
    "f5eef12edea8a77e55a1ef27b4101d724c8774b7",  # VISion On Request
    "d8219fad04e941c344dba7a7004276eb36458a07",  # ReGATE
    "d5c358380b2b2fb9c0e8be6212158e0a01dacb16",  # TCRA-LLM
    "fd539b0c6279997a8b8aaf6ff1f2677cc9e011bd",  # Energy Considerations LLM
    "ed74720bdae9a6ac326ec526e9916b44dd3a7ca2",  # DAM
    "cc1adc975d62a3559fa363fed4f8338bb0d05397",  # CITER
}

# Q1': "LLM prompt compression token reduction" (targeted, same focus as Q1)
t1_q1p = {
    "f8d6c67a825d43790df36d8f93f728772e3d8420",  # Compression Method Matters
    "d4cbbe9b30332ee613ac31d11f16ace95a75f4bd",  # BatchGEMBA
    "65bf6c02c6683ed78291c6e90ef32bd10f88a80d",  # PromptOptMe
    "0b957220f36da0853daf61e896c3251e63a74ce5",  # Compression Paradox
    "3bbf541c2a3ce0ffaed3703cd486f0e1b2febb27",  # Token-Budget-Aware
    "e28d8590ae5d94dcc3f25a05c28a9e5934a72742",  # Behavior-Equivalent Token
    "a16265c84356dd0f39ae3d1f1fa62464f06b8119",  # Perplexity Paradox
    "38a49095776064e6b8f8efa7f88594f65926bfdd",  # LLM as Token Compressor
    "4c101e9b3a84a793b00d3ed00c5232435420142c",  # SCOPE
    "7a4f8771974498f20574bfce4352cb88b2b6cd8c",  # Context-Aware Sentence Encoding
}

# Q2': "prompt compression survey LLM efficiency techniques" (broad)
t1_q2p = {
    "4c101e9b3a84a793b00d3ed00c5232435420142c",  # SCOPE
    "15737902d9a9548fdb0a37a387e6486813aa69cc",  # CompressionAttack
    "7a4f8771974498f20574bfce4352cb88b2b6cd8c",  # Context-Aware Sentence Encoding
    "b6a00f903a49be138522c8ee08c2a53bdb5b69bf",  # Enhancing LLM Efficiency: Prompt Opt
    "0b957220f36da0853daf61e896c3251e63a74ce5",  # Compression Paradox
    "91d7605a00b58e1f9c454992c98b3ac60cb654e8",  # Prompt Compression Survey (Li 2024)
    "3d45fc603e34934fc589b9547307815f7723de34",  # LLMLingua-2
    "1bf55c3454a2f6e0ed2f7f60f5e1076075bd1348",  # From Prompt Injections to Protocol Exploits
    "505168cee83aec4ebe338fc994fe6b00540b5a85",  # PIS
    "5d8d9bd53a4573fe025a678c0d9b416c1dc3d49e",  # Survey Model Scale KD
}

# ─── Topic 2: Multi-Agent Communication Efficiency ─────────────────────────
# Q1: "multi-agent communication efficiency token overhead reduction"
t2_q1 = {
    "c98b22964aea62c73cd7e330496b07191425da96",  # SafeSieve
    "ee552989a03693a441863af4c29dc594bfcd1ab5",  # AgentDropout
    "0db8ee4c82cb700af1f96df72a8218cb3511c2d9",  # G-Designer
    "6f5ac8532d955118adbbaef5f60edd1d82eca3b6",  # Revisiting Communication Efficiency MARL
    "dd271bb7cf626ba614ffc6781b77853e02c7a550",  # Edge Collaborative Caching
    "aebfeb42bbd155c1541a67fddf0a6e2bc5d6ae34",  # Cut the Crap
    "1487ff63c991f8a76029471ab902dc5931d71eb8",  # AutoHMA-LLM
    "e76309e44ae2e7aa29c75a860b9011c08841df53",  # M3Prune
    "d3d564cd891f2a0b4c5232e0b1ec3ab0136712a0",  # Optimizing Field-of-View MAPF
    "92658eaf0eaf6665c1bfc2bb3c57755e82926bf8",  # LEO-MINI
}

# Q2: "multi-agent LLM communication protocol efficiency"
t2_q2 = {
    "dd40dc99b4ec38d4f8560a926f9e345f6a9e9909",  # Manager-Executor
    "e3751924ef0253c9f3d51609a591020b41568692",  # Dual-Agent Collaboration Nursing
    "ed131ad898f1e9ef0b420e4d3f605abfe055b5f3",  # OSC
    "750212f3622acde7262c031e6ba1c11804974c7f",  # Parallelism Meets Adaptiveness
    "86fcbae58aa690dde38665fff09c700ae18a8386",  # Information Propagation Effects
    "356b85ae926b2a8b4cd794e10fe8f37891ebf8d7",  # SagaLLM
    "f7a636f9fba4e3e2107569a68580ed1acbb5f639",  # Self-Resource Allocation
    "8be6b0b0c7af16da10938c252db05cd8dd2f74d0",  # Agents Under Siege
    "794bf13836bdbeccca94084fb3e96f9c094f6b85",  # CONSENSAGENT
    "8b686ee0b8c7dc8da3f04aee1eb9ad3e4f38df0c",  # Collaborating Action by Action
}

# Q3: "multi-agent LLM communication failure redundancy inefficiency"
t2_q3 = {
    "c4d644583e3d06e48d4b029afd4540e29345b969",  # Silo-Bench
    "aebfeb42bbd155c1541a67fddf0a6e2bc5d6ae34",  # Cut the Crap (also in Q1)
    "5c04e42a0c6509f76144932f38257fdcede42ff8",  # LDP
    "05d6976649da50f09f7b629f0e819ef3f0db5bd0",  # Reducing data redundancy MAS
    "a648198cd9c82484a9648601cb3b7f67745310c3",  # CTHA
    "aac384e3f80127908d21c2df47778ad2dc025af6",  # Risk Analysis Governed LLM MAS
    "471de4fab0885f45dffb717512741128775bcbaa",  # KVCOMM
    "337b32fa3b7f428267c683db33ae60c1c1d31bb6",  # CommCP
    "850be973d3b5f76a01119aadffcaae43df8c4ebf",  # COLLAB-LLM
    "1c613a8c1fcd38d605433b7ff716c6bc949552fb",  # Dynamic Consensus Communication
}

# Q4: "LLM agent token cost overhead benchmark"
t2_q4 = {
    "a08050fd27c509f25d2a510f7ca2945a8bfbbb5b",  # Systematic Study LLM Patching
    "85d2768efec4831346827a3e106eaf67567d3035",  # Learning to Evict KV Cache
    "6d519601d1b308acfb8940e9108fc2d30028bee9",  # Evaluating LLM Agent Adherence Safety
    "51afd5f081fe7591285d85dd41c9b3e8bd2cde8e",  # KeBugFix
    "80458b49e294c7b046ca1d60274e58177d86655b",  # Token Coherence MESI
    "361e68a489b714660ef6459952b9e40d88f76f90",  # HackSynth
    "59e2d317142cae98c075b0caac54222c2c5f6e4d",  # Hypergraph Multi-LLM Recommender
    "e918e201ecef33b8a118ec0bd45526eb2d3aedd2",  # RepoAudit
    "742d9c80b2ca4d01f8a8675cfe98487e0783d3d7",  # Group-in-Group Policy
    "e19a6909ad61958866e3845db8443dc9d95b758c",  # MemoPhishAgent
}

# Q1': "multi-agent communication efficiency token overhead reduction" (same as Q1)
t2_q1p = t2_q1.copy()

# Q2': "multi-agent LLM communication protocol efficiency" (same as Q2 = broad)
t2_q2p = t2_q2.copy()

# ─── Topic 3: Semantic Caching LLM Systems ──────────────────────────────────
# Q1: "semantic caching LLM systems inference cost"
t3_q1 = {
    "d40f43fcc2db511b722633927c31b66b19207e13",  # Semantic Caching for Low-Cost LLM
    "8d4b594c2bcb0ac9c65c3c3d6b540076d928a6f6",  # vCache
    "0bd19063460980eadababdccebcac543402f7550",  # Semantic Caching Mitigating Latency
    "e016e7a3311586f1ffa425dba38ee774a93277c0",  # Ensemble Embedding Semantic Caching
    "2c3c9d94cf0bb60797a78d663386d888587b61e7",  # GuardCache
    "e2ea3627decdfb839d7a01081478c1c734a9518b",  # SentenceKV
    "641a8b01dc986ede5d894765b24c5fed6ad15462",  # Cortex
    "3e48aa3ceb36b6cad4bd1aaa907ec7f8607b9212",  # AdaBlock-dLLM
    "36da8b983358464fbea7d332a1af58add0be0fb3",  # Asynchronous Verified Semantic Caching
    "db6a4569e992d912f4bcd0996c8b482bfe590d27",  # Throughput-Oriented LLM KV-Activation
}

# Q2: "semantic similarity caching mechanism large language models"
t3_q2 = {
    "7a3903f590bc6ba555c68f3cafa1c5b9694dcaeb",  # System Design Incident (off-topic)
    "5b35fff3afa7004938138f7bc73d2f2139ba9bf5",  # LLMCache Layer-Wise
    "4b20b13f3fd164c461cd2690c2e3fae11dd28a0d",  # Cache Poisoning LLM
    "2e877363041e8040dc24664c33b8e262e3aab561",  # New Performance Analysis Semantic Caching
    "a24b410204822d4faf61b9f3135be6ef39c5a617",  # dLLM-Cache
    "54209f5f495d7074a5e105f667ec367a622e9d45",  # SimMark
    "5c08a205733821700187a4cecca6c903ffdda4da",  # Children's scientific drawing (off-topic)
    "a6c4c667242f0ae280da5057fb2bf46f8f467d09",  # Enhancing Semantic Consistency LLM
    "d82f4c0e8fa1d43d7352e8dbf12af231b17b2a81",  # Annotating Training Data Semantic STS
    "3837c2d181306d501c27022ff9d289581b81eb3d",  # SCALM
}

# Q3: "semantic caching failure cache miss accuracy LLM"
t3_q3 = {
    "e016e7a3311586f1ffa425dba38ee774a93277c0",  # Ensemble Embedding Semantic Caching
    "2acd4d26a0b469c20ef95f7c7173348ef576e452",  # Category-Aware Semantic Caching
    "087d9aeb81d56bfcc526888bd002ccf956b0ac63",  # ClusterKV
    "2d6748433cce2b073eece7169df1e86216e95de9",  # MeanCache
    "36da8b983358464fbea7d332a1af58add0be0fb3",  # Asynchronous Verified Semantic Caching
    "0157b57c4207489da0f0e67d9dcbdcda577ec550",  # GPT Semantic Cache
    "d61584d23e617852cc52d1b8ed3f0c0e033d551b",  # From Exact Hits to Close Enough
    "e2ea3627decdfb839d7a01081478c1c734a9518b",  # SentenceKV
    "641a8b01dc986ede5d894765b24c5fed6ad15462",  # Cortex
    "cd9726fa32158bf27d0b3614187cb56c664c4eb8",  # Semantic Caching Intent-Driven
}

# Q4: "LLM inference caching cost optimization survey"
t3_q4 = {
    "119b6cc86eced3d3a37ab40390875a44d49818a0",  # Survey Inference Engines LLM
    "6d2fee68aef566c75bf4678c2f7ae176d5314a44",  # Q-Infer
    "0fa443adf81f204a3907257e4ed97c83b081a59a",  # JointCloud LLM
    "da156ec149acbf473174f457292b8b4652938704",  # InferLog
    "db6a4569e992d912f4bcd0996c8b482bfe590d27",  # Throughput-Oriented LLM KV-Activation
    "6eb9ffb3144ede9f37a0245abb6fd21de091841c",  # Tail-Optimized Caching
    "5814cca92325e0644a15e1c7e8df5ad2922b9f77",  # Survey of LLM Inference Systems
    "b360df674a686258da0b6932cb9646453f7c1234",  # DOTS (placeholder S2 ID)
    "14003bb8b5236f4abb12963745c04a6c6610cc5d",  # KVTuner
    "8f3d959238e67bf6b9bc9818025d0d2e403e478f",  # DuoAttention
}

# Q1': "semantic caching LLM systems inference cost" (same as Q1)
t3_q1p = t3_q1.copy()

# Q2': "LLM inference caching cost optimization survey" (same as Q4 = broad)
t3_q2p = t3_q4.copy()


def jaccard(set_a, set_b):
    if not set_a and not set_b:
        return 1.0
    return len(set_a & set_b) / len(set_a | set_b)


def coverage(two_search_union, four_search_union):
    """Fraction of 4-search corpus captured by 2-search strategy."""
    if not four_search_union:
        return 1.0
    return len(two_search_union & four_search_union) / len(four_search_union)


def redundancy_count(sets):
    """Count papers appearing in 3+ of the 4 queries."""
    counter = Counter()
    for s in sets:
        for paper in s:
            counter[paper] += 1
    return sum(1 for c in counter.values() if c >= 3), counter


topics = [
    {
        "name": "LLM Prompt Compression",
        "q1": t1_q1, "q2": t1_q2, "q3": t1_q3, "q4": t1_q4,
        "q1p": t1_q1p, "q2p": t1_q2p,
    },
    {
        "name": "Multi-Agent Communication Efficiency",
        "q1": t2_q1, "q2": t2_q2, "q3": t2_q3, "q4": t2_q4,
        "q1p": t2_q1p, "q2p": t2_q2p,
    },
    {
        "name": "Semantic Caching LLM Systems",
        "q1": t3_q1, "q2": t3_q2, "q3": t3_q3, "q4": t3_q4,
        "q1p": t3_q1p, "q2p": t3_q2p,
    },
]

print(f"{'Topic':<38} | {'4-search'} | {'2-search'} | {'Coverage'} | {'High-redund'}")
print("-" * 90)

coverage_fractions = []
for t in topics:
    four_union = t["q1"] | t["q2"] | t["q3"] | t["q4"]
    two_union = t["q1p"] | t["q2p"]
    cov = coverage(two_union, four_union)
    coverage_fractions.append(cov)
    high_redund, _ = redundancy_count([t["q1"], t["q2"], t["q3"], t["q4"]])
    print(
        f"{t['name']:<38} | {len(four_union):8} | {len(two_union):8} | "
        f"{cov:>8.1%} | {high_redund:>11}"
    )

avg_cov = sum(coverage_fractions) / len(coverage_fractions)
print("-" * 90)
print(f"{'AVERAGE':<38} | {'':8} | {'':8} | {avg_cov:>8.1%} |")
print()
print(f"Hypothesis 80% threshold met: {avg_cov >= 0.80}")
print()

# Per-topic detailed breakdown
for t in topics:
    four_union = t["q1"] | t["q2"] | t["q3"] | t["q4"]
    two_union = t["q1p"] | t["q2p"]
    missed = four_union - two_union
    _, counter = redundancy_count([t["q1"], t["q2"], t["q3"], t["q4"]])

    print(f"=== {t['name']} ===")
    print(f"  4-search unique papers: {len(four_union)}")
    print(f"  2-search unique papers: {len(two_union)}")
    print(f"  Overlap (in both):      {len(two_union & four_union)}")
    print(f"  Missed by 2-search:     {len(missed)}")
    print(f"  Coverage:               {coverage(two_union, four_union):.1%}")
    q3_exclusive = t["q3"] - t["q1"] - t["q2"]
    q4_exclusive = t["q4"] - t["q1"] - t["q2"]
    q34_exclusive = (t["q3"] | t["q4"]) - t["q1"] - t["q2"]
    print(f"  Papers unique to Q3 only (not in Q1 or Q2): {len(q3_exclusive)}")
    print(f"  Papers unique to Q4 only (not in Q1 or Q2): {len(q4_exclusive)}")
    print(f"  Papers unique to Q3|Q4 (not in Q1 or Q2):   {len(q34_exclusive)}")
    print()
