from typing import Dict, Optional

# Metric Modules
from .metrics.prompt_metrics import PromptMetrics
from .metrics.primitive_metrics import PrimitiveMetrics
from .metrics.response_metrics import ResponseMetrics
from .metrics.semantic_metrics import SemanticMetrics
from .metrics.aggregation import AggregationEngine

# Optional LLM Judge
from .llm_judge import LLMJudge


class Evaluator:
    """
    Master Evaluation Controller for SRPP Studio.

    Orchestrates:
        - Deterministic metrics
        - Semantic metrics
        - LLM-as-judge scoring
        - Multi-objective aggregation
        - Iteration decision logic
    """

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(
        self,
        llm=None,
        enable_semantic: bool = True,
        enable_judge: bool = True,
        quality_threshold: float = 0.65
    ):

        self.prompt_metrics = PromptMetrics()
        self.primitive_metrics = PrimitiveMetrics()
        self.response_metrics = ResponseMetrics()

        self.semantic_metrics = SemanticMetrics() if enable_semantic else None
        self.judge = LLMJudge(llm) if (enable_judge and llm) else None

        self.aggregator = AggregationEngine()

        self.quality_threshold = quality_threshold

    # ============================================================
    # MAIN EVALUATION PIPELINE
    # ============================================================

    def evaluate(
        self,
        original_prompt: str,
        optimized_prompt: str,
        original_response: str,
        optimized_response: str,
        metadata: Optional[Dict] = None
    ) -> Dict:

        metadata = metadata or {}

        # -------------------------
        # 1. Prompt Metrics
        # -------------------------
        prompt_metrics = self.prompt_metrics.compute(
            original_prompt,
            optimized_prompt
        )

        # -------------------------
        # 2. Primitive Metrics
        # -------------------------
        primitive_metrics = self.primitive_metrics.compute(metadata)

        # -------------------------
        # 3. Response Metrics
        # -------------------------
        response_metrics = self.response_metrics.compute(
            original_prompt,
            optimized_prompt,
            original_response,
            optimized_response
        )

        # -------------------------
        # 4. Semantic Metrics
        # -------------------------
        semantic_metrics = {}
        if self.semantic_metrics:
            semantic_metrics = self.semantic_metrics.compute(
                original_prompt,
                optimized_prompt,
                original_response,
                optimized_response
            )

        # -------------------------
        # 5. LLM Judge
        # -------------------------
        judge_metrics = {}
        if self.judge:
            judge_metrics = self.judge.evaluate(
                optimized_prompt,
                optimized_response
            )

        # -------------------------
        # 6. Aggregation
        # -------------------------
        metrics_bundle = {
            "prompt_metrics": prompt_metrics,
            "primitive_metrics": primitive_metrics,
            "response_metrics": response_metrics,
            "semantic_metrics": semantic_metrics,
            "judge_metrics": judge_metrics
        }

        aggregation_result = self.aggregator.compute_final_score(metrics_bundle)

        # -------------------------
        # 7. Iteration Decision
        # -------------------------
        final_score = aggregation_result["final_composite_score"]

        should_iterate = final_score < self.quality_threshold

        return {
            "metrics": metrics_bundle,
            "aggregation": aggregation_result,
            "final_score": final_score,
            "quality_threshold": self.quality_threshold,
            "should_iterate": should_iterate
        }