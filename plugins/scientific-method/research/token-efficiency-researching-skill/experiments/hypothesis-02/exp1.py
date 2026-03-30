#!/usr/bin/env python3
"""
Experiment 2: Side-by-Side Hypothesis Generation Comparison (Opus vs Sonnet)
Hypothesis 02 - Token Efficiency: Downgrading Generating-Hypotheses to Sonnet Preserves Quality

Approach:
- Use urllib to call the Anthropic Messages API directly (no SDK dependency)
- Call claude-opus-4-5 and claude-sonnet-4-5 with identical prompts
- Prompt mirrors the generating-hypotheses skill's input: problem statement + empty prior conclusions
- Score each output on specificity, falsifiability, and diversity (1-3 scale each)
- Compute mean scores, quality delta, and token counts
- Calculate cost ratio using standard per-million-token pricing (Opus: $15/$75 input/output, Sonnet: $3/$15)
"""

import json
import os
import time
import urllib.request
import urllib.error

# Minimal problem statement derived from problem.md (simulating what generating-hypotheses reads)
PROBLEM_SUMMARY = """
# Problem: Token Efficiency of Scientific Method Research Skill

## Problem Statement
A scientific-method research loop consumes excessive tokens due to multiplicative agent spawning,
redundant skill loading, verbose prompts, and suboptimal model routing. Goal: identify concrete
optimizations to reduce token consumption without degrading research quality.

## Key unknowns
1. Which skills require opus-tier reasoning vs sonnet/haiku?
2. Can literature searches be batched across hypotheses?
3. What is the minimum viable hypothesis count for robust research?

## Success criteria
- Identify ≥8 distinct implementable optimizations with quantified token savings
- Combined optimizations target 40-60% total token reduction
- No compromise of scientific rigor
"""

GENERATING_HYPOTHESES_PROMPT = f"""Read this problem statement and generate exactly 4 testable hypotheses.

{PROBLEM_SUMMARY}

For each hypothesis, produce a stub in this exact format:
# Hypothesis NN: <Concise title (5-10 words)>

## Statement
<1-2 sentences: a precise, falsifiable claim>

## Rationale
<2-3 sentences: why this is worth testing>

Requirements for the set as a whole:
- Each hypothesis must be falsifiable (state a clear refutation condition)
- Each must be specific (name a concrete measurable outcome)
- The 4 hypotheses must cover DIFFERENT mechanisms (not variations of the same idea)
- Order from most to least promising

Generate hypotheses 01 through 04."""

MODELS = {
    "opus": "claude-opus-4-5",
    "sonnet": "claude-sonnet-4-5",
}

# Standard per-million-token pricing (2025)
PRICING = {
    "opus":   {"input": 15.0, "output": 75.0},
    "sonnet": {"input": 3.0,  "output": 15.0},
}


def call_anthropic(model_id: str, prompt: str, max_tokens: int = 2000) -> dict:
    """Call the Anthropic Messages API directly using urllib."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set")

    payload = json.dumps({
        "model": model_id,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}]
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_hypotheses(text: str) -> list:
    """Split model output into individual hypothesis blocks."""
    parts = []
    current = []
    for line in text.split("\n"):
        if line.startswith("# Hypothesis") and current:
            parts.append("\n".join(current))
            current = [line]
        else:
            current.append(line)
    if current:
        parts.append("\n".join(current))
    return [p.strip() for p in parts if "## Statement" in p]


def score_hypothesis(hyp_text: str, all_hypotheses: list, hyp_index: int) -> dict:
    """
    Score a single hypothesis on three dimensions (1-3 scale each):

    Specificity (1-3):
      1 = vague claim with no quantitative or mechanism anchor
      2 = names a mechanism without measurable outcome
      3 = names mechanism AND quantitative or measurable outcome

    Falsifiability (1-3):
      1 = no refutation condition anywhere
      2 = implicit refutation (e.g., "preserve quality" implies failure if quality drops)
      3 = explicit refutation condition stated (keywords: "fail", "does not", "refuted if", comparison operators)

    Diversity (1-3):
      1 = nearly duplicate mechanism of another hypothesis (≥2 shared keywords)
      2 = overlapping but different angle (1 shared keyword)
      3 = distinct mechanism from all others (0 shared keywords)
    """
    lower = hyp_text.lower()

    # Specificity
    has_quant = any(c.isdigit() for c in hyp_text) or "%" in hyp_text or " x " in lower or "fold" in lower
    mechanism_kws = ["compress", "batch", "cache", "rout", "model selection", "token", "context",
                     "parallel", "skip", "early", "prune", "reduc", "aggregat", "summar", "chunk",
                     "deduplic", "haiku", "sonnet", "opus", "literatured", "hypothes"]
    has_mechanism = any(kw in lower for kw in mechanism_kws)
    if has_quant and has_mechanism:
        specificity = 3
    elif has_mechanism:
        specificity = 2
    else:
        specificity = 1

    # Falsifiability
    explicit_kws = ["refut", "fail", "does not", "cannot", "below", "above", "exceed",
                    "less than", "greater than", "worse", "degrad", "drop", "if not", "unless"]
    implicit_kws = ["without", "preserve", "maintain", "equivalent", "comparable", "same", "parity", "match"]
    if any(kw in lower for kw in explicit_kws):
        falsifiability = 3
    elif any(kw in lower for kw in implicit_kws):
        falsifiability = 2
    else:
        falsifiability = 1

    # Diversity
    core_mechanisms = ["compress", "batch", "cache", "rout", "haiku", "sonnet",
                       "parallel", "skip", "prune", "aggregat", "summar", "chunk", "deduplic"]
    my_mechs = {kw for kw in core_mechanisms if kw in lower}

    other_hypotheses = [h for i, h in enumerate(all_hypotheses) if i != hyp_index and h]
    max_overlap = 0
    for other in other_hypotheses:
        other_lower = other.lower()
        other_mechs = {kw for kw in core_mechanisms if kw in other_lower}
        overlap = len(my_mechs & other_mechs)
        if overlap > max_overlap:
            max_overlap = overlap

    if max_overlap == 0:
        diversity = 3
    elif max_overlap == 1:
        diversity = 2
    else:
        diversity = 1

    return {"specificity": specificity, "falsifiability": falsifiability, "diversity": diversity}


def run_model(model_key: str, model_id: str) -> dict:
    """Run one model and return scored results."""
    print(f"\n[{model_key.upper()}] Calling {model_id}...")
    start = time.time()
    resp = call_anthropic(model_id, GENERATING_HYPOTHESES_PROMPT)
    elapsed = time.time() - start

    text = resp["content"][0]["text"]
    usage = resp["usage"]
    input_tokens = usage["input_tokens"]
    output_tokens = usage["output_tokens"]

    print(f"[{model_key.upper()}] Done in {elapsed:.1f}s. Input: {input_tokens}, Output: {output_tokens}")
    print(f"[{model_key.upper()}] Output:\n{text}")

    hypotheses = parse_hypotheses(text)
    print(f"[{model_key.upper()}] Parsed {len(hypotheses)} hypotheses")

    scores_list = []
    for i, hyp in enumerate(hypotheses):
        s = score_hypothesis(hyp, hypotheses, i)
        scores_list.append(s)
        print(f"  Hyp {i+1}: spec={s['specificity']} fals={s['falsifiability']} div={s['diversity']}")

    mean_spec = sum(s["specificity"] for s in scores_list) / len(scores_list) if scores_list else 0.0
    mean_fals = sum(s["falsifiability"] for s in scores_list) / len(scores_list) if scores_list else 0.0
    mean_div  = sum(s["diversity"]  for s in scores_list) / len(scores_list) if scores_list else 0.0

    p = PRICING[model_key]
    cost = (input_tokens / 1_000_000 * p["input"]) + (output_tokens / 1_000_000 * p["output"])

    return {
        "model_id": model_id,
        "text": text,
        "hypothesis_texts": hypotheses,
        "scores": scores_list,
        "mean_specificity": mean_spec,
        "mean_falsifiability": mean_fals,
        "mean_diversity": mean_div,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost_usd": cost,
    }


def main():
    results = {}
    for model_key, model_id in MODELS.items():
        results[model_key] = run_model(model_key, model_id)

    opus   = results["opus"]
    sonnet = results["sonnet"]

    delta_spec = abs(opus["mean_specificity"] - sonnet["mean_specificity"])
    delta_fals = abs(opus["mean_falsifiability"] - sonnet["mean_falsifiability"])
    delta_div  = abs(opus["mean_diversity"] - sonnet["mean_diversity"])
    max_delta  = max(delta_spec, delta_fals, delta_div)

    if opus["cost_usd"] > 0:
        cost_savings_pct = (opus["cost_usd"] - sonnet["cost_usd"]) / opus["cost_usd"] * 100
    else:
        cost_savings_pct = 0.0

    print("\n" + "=" * 65)
    print("SUMMARY")
    print("=" * 65)
    fmt = f"{'Metric':<32} {'Opus':>10} {'Sonnet':>10} {'Delta':>10}"
    print(fmt)
    print("-" * 65)
    print(f"{'Mean Specificity':<32} {opus['mean_specificity']:>10.2f} {sonnet['mean_specificity']:>10.2f} {delta_spec:>10.2f}")
    print(f"{'Mean Falsifiability':<32} {opus['mean_falsifiability']:>10.2f} {sonnet['mean_falsifiability']:>10.2f} {delta_fals:>10.2f}")
    print(f"{'Mean Diversity':<32} {opus['mean_diversity']:>10.2f} {sonnet['mean_diversity']:>10.2f} {delta_div:>10.2f}")
    print(f"{'Input Tokens':<32} {opus['input_tokens']:>10} {sonnet['input_tokens']:>10}")
    print(f"{'Output Tokens':<32} {opus['output_tokens']:>10} {sonnet['output_tokens']:>10}")
    print(f"{'Cost USD':<32} {opus['cost_usd']:>10.5f} {sonnet['cost_usd']:>10.5f}")
    print(f"{'Cost Savings (%)':<32} {cost_savings_pct:>10.1f}%")
    print()
    print(f"Max quality delta across dimensions: {max_delta:.2f}  (confirm threshold: ≤0.3, refute: >0.3)")
    print(f"Cost savings: {cost_savings_pct:.1f}%  (confirm: ≥75%, refute: <60%)")
    print()

    if max_delta <= 0.3 and cost_savings_pct >= 75:
        verdict = "CONFIRMED"
        reason = f"Quality delta {max_delta:.2f} ≤ 0.3 and cost savings {cost_savings_pct:.1f}% ≥ 75%"
    elif max_delta > 0.3:
        verdict = "REFUTED (quality)"
        reason = f"Quality delta {max_delta:.2f} > 0.3 on at least one dimension"
    elif cost_savings_pct < 60:
        verdict = "REFUTED (cost)"
        reason = f"Cost savings {cost_savings_pct:.1f}% < 60%"
    else:
        verdict = "INCONCLUSIVE"
        reason = f"Quality acceptable (delta {max_delta:.2f} ≤ 0.3) but savings {cost_savings_pct:.1f}% between 60-75%"

    print(f"OUTCOME: {verdict}")
    print(f"Reason: {reason}")

    # Save results
    out_path = "/home/fence/src/pipemind/claude-agentic/plugins/scientific-method/token-efficiency-researching-skill/experiments/hypothesis-02/exp1_results.json"
    with open(out_path, "w") as f:
        save = {}
        for k, v in results.items():
            save[k] = {kk: vv for kk, vv in v.items() if kk != "text"}
            save[k]["text_snippet"] = v["text"][:500]
        json.dump(save, f, indent=2)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
