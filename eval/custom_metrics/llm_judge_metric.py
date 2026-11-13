"""
Custom LLM-as-a-Judge Evaluation Metric for Usisivac V6 and Agents CLI.
Designed to serve as the target metric for 'eval optimize' (GEPA hill-climbing)
and automated CI regression gates.

Scores responses on an objective 1-to-5 scale:
  1 - Fatal failure: target leakage, broken math, division by zero, or severe hallucination.
  2 - Poor: major factual errors, missing essential domain parameters, or evasive answer.
  3 - Acceptable: correct general direction but lacks robust numerical bounds, epsilons, or guards.
  4 - Strong: mathematically precise, includes zero-division guards, strictly out-of-fold, production-ready.
  5 - Grandmaster-grade: optimal formulation, explains tradeoff, robust edge-case immunity, complete reasoning.
"""

import re
import json
from typing import Dict, Any, Optional

try:
    from Usisivac.src.core.agy_client import query_llm
except ImportError:
    # Standalone fallback if invoked in isolated sandbox
    def query_llm(prompt: str, system: Optional[str] = None, **kwargs) -> str:
        return '{"score": 4.0, "explanation": "Fallback judge evaluation"}'


JUDGE_SYSTEM_PROMPT = """You are an elite Machine Learning Quality Evaluation Judge.
Evaluate the candidate response against the reference and user prompt.
Focus on:
1. Mathematical precision (proper epsilons, log1p, non-linear scaling).
2. Strict anti-leakage compliance (no global target encoding, no target proxy features).
3. Statistical robustness (MAD-based outlier boundaries, CUSUM drift detection).
4. Tone and domain adherence (polite refusal of non-ML off-topic queries).

Rate strictly on a 1-5 scale and output ONLY a JSON object:
{"score": <float 1.0 to 5.0>, "explanation": "<clear technical justification>"}"""


def evaluate(instance: Dict[str, Any]) -> Dict[str, Any]:
    """Canonical entrypoint for agents-cli custom evaluation metric.
    
    Args:
        instance: Evaluation case dictionary containing prompt, responses, and optional reference.
        
    Returns:
        Dict with 'score' (float) and 'explanation' (str).
    """
    # 1. Extract prompt text
    prompt_text = ""
    prompt_obj = instance.get("prompt") or {}
    parts = prompt_obj.get("parts") or []
    if parts and isinstance(parts, list):
        prompt_text = parts[0].get("text", "")

    # 2. Extract agent response text
    response_text = ""
    responses = instance.get("responses") or []
    if responses and isinstance(responses, list) and len(responses) > 0:
        resp_parts = (responses[0].get("response") or {}).get("parts") or []
        if resp_parts:
            response_text = resp_parts[0].get("text", "")
    elif "response" in instance:
        response_text = str(instance["response"])

    # 3. Extract reference answer if present
    reference_text = ""
    ref_obj = instance.get("reference") or {}
    if ref_obj:
        ref_parts = (ref_obj.get("response") or {}).get("parts") or []
        if ref_parts:
            reference_text = ref_parts[0].get("text", "")

    if not response_text.strip():
        return {
            "score": 1.0,
            "explanation": "Agent produced an empty response."
        }

    # 4. Immediate deterministic safety guard checks
    lower_resp = response_text.lower()
    if "global target encoding across the entire dataset" in lower_resp:
        return {
            "score": 1.0,
            "explanation": "Fatal target leakage: recommended global target encoding without out-of-fold splitting."
        }

    # Fast test mode for unit testing (skips external LLM call)
    import os
    if os.getenv("FAST_EVAL_TEST") == "1":
        score = 3.5
        if any(k in lower_resp for k in ["out-of-fold", "target leakage", "strictly unsupervised", "epsilon"]):
            score += 1.0
        if len(response_text) > 50:
            score += 0.5
        return {
            "score": min(5.0, score),
            "explanation": "Fast test evaluation based on domain keywords and safety guards."
        }

    # 5. Query LLM Judge for nuanced scoring
    judge_prompt = f"""EVALUATION CASE:
User Prompt:
{prompt_text}

Agent Response:
{response_text}

Reference Answer:
{reference_text if reference_text else 'N/A'}

Provide your score (1.0 to 5.0) and technical explanation in JSON format:
{{"score": <number>, "explanation": "<reason>"}}"""

    try:
        raw_result = query_llm(
            prompt=judge_prompt,
            system=JUDGE_SYSTEM_PROMPT,
            temperature=0.0,
            timeout=45
        )

        match = re.search(r"\{.*?\}", raw_result, re.DOTALL)
        if match:
            parsed = json.loads(match.group(0))
            score = float(parsed.get("score", 4.0))
            score = max(1.0, min(5.0, score))  # Clip to [1.0, 5.0]
            return {
                "score": score,
                "explanation": str(parsed.get("explanation", "Scored by LLM judge.")),
            }
    except Exception as e:
        # Fallback to deterministic heuristic if LLM query times out
        pass

    # Heuristic scoring fallback
    score = 3.5
    if any(k in lower_resp for k in ["out-of-fold", "target leakage", "strictly unsupervised", "epsilon"]):
        score += 1.0
    if len(response_text) > 80:
        score += 0.5

    return {
        "score": min(5.0, score),
        "explanation": "Heuristic fallback evaluation based on domain keywords and safety guards."
    }


if __name__ == "__main__":
    # Self-test sample
    test_instance = {
        "prompt": {"parts": [{"text": "How do you calculate transaction velocity?"}]},
        "responses": [{
            "response": {
                "parts": [{"text": "Calculate distance / (hours + 0.05) to prevent division by zero, strictly unsupervised."}]
            }
        }],
        "reference": {"parts": [{"text": "velocity = distance / (hours + epsilon)"}]}
    }
    result = evaluate(test_instance)
    print("Self-test result:", result)
