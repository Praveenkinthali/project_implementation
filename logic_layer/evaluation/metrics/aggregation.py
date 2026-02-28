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

    Produces:
    - Normalized component scores
    - Final composite score
    """

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(self, weights: Optional[Dict] = None):

        # Default weights (can tune experimentally)
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
        """
        metrics_bundle should contain:
        {
            "prompt_metrics": {...},
            "primitive_metrics": {...},
            "response_metrics": {...},
            "semantic_metrics": {...},
            "judge_metrics": {...}
        }
        """

        prompt_score = self._score_prompt(metrics_bundle.get("prompt_metrics", {}))
        primitive_score = self._score_primitive(metrics_bundle.get("primitive_metrics", {}))
        response_score = self._score_response(metrics_bundle.get("response_metrics", {}))
        semantic_score = self._score_semantic(metrics_bundle.get("semantic_metrics", {}))
        judge_score = self._score_judge(metrics_bundle.get("judge_metrics", {}))

        final_score = (
            self.weights["prompt"] * prompt_score +
            self.weights["primitive"] * primitive_score +
            self.weights["response"] * response_score +
            self.weights["semantic"] * semantic_score +
            self.weights["judge"] * judge_score
        )

        return {
            "component_scores": {
                "prompt_score": round(prompt_score, 4),
                "primitive_score": round(primitive_score, 4),
                "response_score": round(response_score, 4),
                "semantic_score": round(semantic_score, 4),
                "judge_score": round(judge_score, 4)
            },
            "final_composite_score": round(final_score, 4)
        }

    # ============================================================
    # PROMPT SCORE
    # ============================================================

    def _score_prompt(self, prompt_metrics: Dict) -> float:

        structural = prompt_metrics.get("structural_metrics", {}).get("structural_change_score", 0)
        instruction_delta = prompt_metrics.get("instruction_metrics", {}).get("instruction_density_delta", 0)
        constraint_delta = prompt_metrics.get("constraint_metrics", {}).get("constraint_delta", 0)

        base = structural + max(instruction_delta, 0) * 0.1 + max(constraint_delta, 0) * 0.1

        return min(base, 1.0)

    # ============================================================
    # PRIMITIVE SCORE
    # ============================================================

    def _score_primitive(self, primitive_metrics: Dict) -> float:

        diversity = primitive_metrics.get("diversity_metrics", {}).get("diversity_score", 0)

        overuse_flag = primitive_metrics.get("overuse_metrics", {}).get("overuse_flag", False)

        penalty = 0.2 if overuse_flag else 0

        score = diversity - penalty

        return max(min(score, 1.0), 0)

    # ============================================================
    # RESPONSE SCORE
    # ============================================================

    def _score_response(self, response_metrics: Dict) -> float:

        relevance = response_metrics.get("relevance_metrics", {}).get("keyword_overlap_score", 0)

        adherence = response_metrics.get("instruction_adherence", {}).get("instruction_adherence_score", 0)

        structure_bonus = 0.1 if response_metrics.get("structure_metrics", {}).get("list_structure_delta", 0) > 0 else 0

        return min(relevance * 0.5 + adherence * 0.4 + structure_bonus, 1.0)

    # ============================================================
    # SEMANTIC SCORE
    # ============================================================

    def _score_semantic(self, semantic_metrics: Dict) -> float:

        prompt_similarity = semantic_metrics.get("prompt_semantic_similarity", 0)
        alignment = semantic_metrics.get("prompt_response_alignment", 0)

        return min((prompt_similarity * 0.5 + alignment * 0.5), 1.0)

    # ============================================================
    # JUDGE SCORE
    # ============================================================

    def _score_judge(self, judge_metrics: Dict) -> float:

        if not judge_metrics or "overall_quality" not in judge_metrics:
            return 0

        return min(judge_metrics["overall_quality"] / 10, 1.0)