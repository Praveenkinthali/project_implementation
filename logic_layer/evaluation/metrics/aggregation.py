from typing import Dict, Optional


class AggregationEngine:
    """
    Multi-objective scoring engine for SRPP Studio.

    Combines:
    - Prompt metrics
    - Primitive metrics
    - Response metrics
    - Semantic metrics
    - LLM Judge scores
    - Hallucination risk penalty

    Produces:
    - Normalized component scores
    - Final composite score
    """

    def __init__(self, weights: Optional[Dict] = None):

        self.weights = weights or {
            "prompt": 0.20,
            "primitive": 0.15,
            "response": 0.25,
            "semantic": 0.20,
            "judge": 0.20
        }

    # ============================================================
    # PUBLIC ENTRY
    # ============================================================

    def compute_final_score(self, metrics_bundle: Dict) -> Dict:

        prompt_score = self._score_prompt(metrics_bundle.get("prompt_metrics", {}))
        primitive_score = self._score_primitive(metrics_bundle.get("primitive_metrics", {}))
        response_score = self._score_response(metrics_bundle.get("response_metrics", {}))
        semantic_score = self._score_semantic(metrics_bundle.get("semantic_metrics", {}))
        judge_score = self._score_judge(metrics_bundle.get("judge_metrics", {}))

        hallucination_penalty = self._hallucination_penalty(
            metrics_bundle.get("response_metrics", {})
        )

        final_score = (
            self.weights["prompt"] * prompt_score +
            self.weights["primitive"] * primitive_score +
            self.weights["response"] * response_score +
            self.weights["semantic"] * semantic_score +
            self.weights["judge"] * judge_score
        )

        final_score = max(final_score - hallucination_penalty, 0)

        return {
            "component_scores": {
                "prompt_score": round(prompt_score, 4),
                "primitive_score": round(primitive_score, 4),
                "response_score": round(response_score, 4),
                "semantic_score": round(semantic_score, 4),
                "judge_score": round(judge_score, 4),
                "hallucination_penalty": round(hallucination_penalty, 4)
            },
            "final_composite_score": round(final_score, 4)
        }

    # ============================================================
    # PROMPT SCORE
    # ============================================================

    def _score_prompt(self, prompt_metrics: Dict) -> float:

        structural = prompt_metrics.get("structural_metrics", {}).get(
            "structural_change_score", 0
        )

        instruction_delta = prompt_metrics.get(
            "instruction_metrics", {}
        ).get("instruction_density_delta", 0)

        constraint_delta = prompt_metrics.get(
            "constraint_metrics", {}
        ).get("constraint_delta", 0)

        base = structural + max(instruction_delta, 0) * 0.1 + max(constraint_delta, 0) * 0.1

        return min(base, 1.0)

    # ============================================================
    # PRIMITIVE SCORE
    # ============================================================

    def _score_primitive(self, primitive_metrics: Dict) -> float:

        diversity = primitive_metrics.get(
            "diversity_metrics", {}
        ).get("diversity_score", 0)

        overuse_flag = primitive_metrics.get(
            "overuse_metrics", {}
        ).get("overuse_flag", False)

        penalty = 0.2 if overuse_flag else 0

        score = diversity - penalty

        return max(min(score, 1.0), 0)

    # ============================================================
    # RESPONSE SCORE
    # ============================================================

    def _score_response(self, response_metrics: Dict) -> float:

        relevance = response_metrics.get(
            "relevance_metrics", {}
        ).get("keyword_overlap_score", 0)

        adherence = response_metrics.get(
            "instruction_adherence", {}
        ).get("instruction_adherence_score", 0)

        structure_bonus = 0.1 if response_metrics.get(
            "structure_metrics", {}
        ).get("list_structure_delta", 0) > 0 else 0

        return min(relevance * 0.5 + adherence * 0.4 + structure_bonus, 1.0)

    # ============================================================
    # SEMANTIC SCORE
    # ============================================================

    def _score_semantic(self, semantic_metrics: Dict) -> float:

        prompt_similarity = semantic_metrics.get("prompt_semantic_similarity", 0)
        alignment = semantic_metrics.get("prompt_response_alignment", 0)

        return min((prompt_similarity * 0.5 + alignment * 0.5), 1.0)

    # ============================================================
    # JUDGE SCORE (Improved)
    # ============================================================

    def _score_judge(self, judge_metrics: Dict) -> float:

        if not judge_metrics:
            return 0

        clarity = judge_metrics.get("clarity", 0)
        relevance = judge_metrics.get("relevance", 0)
        completeness = judge_metrics.get("completeness", 0)
        factual = judge_metrics.get("factual_reliability", 0)

        if clarity == relevance == completeness == factual == 0:
            return 0

        avg = (clarity + relevance + completeness + factual) / 4

        return min(avg / 10, 1.0)

    # ============================================================
    # HALLUCINATION PENALTY
    # ============================================================

    def _hallucination_penalty(self, response_metrics: Dict) -> float:

        proxies = response_metrics.get("hallucination_proxies", {})

        overconfidence = proxies.get("overconfidence_marker_count", 0)
        numeric_density = proxies.get("numeric_density_ratio", 0)

        penalty = (overconfidence * 0.05) + (numeric_density * 0.1)

        return min(penalty, 0.15)