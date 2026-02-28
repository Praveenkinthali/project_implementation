from typing import Dict
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None


class SemanticMetrics:
    """
    Embedding-based semantic evaluation.

    Measures:
    - Prompt intent preservation
    - Response improvement
    - Prompt-response alignment
    - Semantic drift detection
    """

    _model = None  # shared across instances

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):

        if SentenceTransformer is None:
            raise ImportError(
                "sentence-transformers not installed. "
                "Run: pip install sentence-transformers"
            )

        if SemanticMetrics._model is None:
            SemanticMetrics._model = SentenceTransformer(model_name)

        self.model = SemanticMetrics._model

    # ============================================================
    # PUBLIC ENTRY
    # ============================================================

    def compute(
        self,
        original_prompt: str,
        optimized_prompt: str,
        original_response: str,
        optimized_response: str
    ) -> Dict:

        prompt_similarity = self._cosine(original_prompt, optimized_prompt)
        response_similarity = self._cosine(original_response, optimized_response)

        prompt_response_alignment = self._cosine(
            optimized_prompt,
            optimized_response
        )

        semantic_drift = 1 - prompt_similarity

        return {
            "prompt_semantic_similarity": round(prompt_similarity, 4),
            "response_semantic_similarity": round(response_similarity, 4),
            "prompt_response_alignment": round(prompt_response_alignment, 4),
            "semantic_drift_score": round(semantic_drift, 4)
        }

    # ============================================================
    # COSINE SIMILARITY
    # ============================================================

    def _cosine(self, text_a: str, text_b: str) -> float:

        embeddings = self.model.encode([text_a, text_b])

        vec_a, vec_b = embeddings[0], embeddings[1]

        numerator = np.dot(vec_a, vec_b)
        denominator = (
            np.linalg.norm(vec_a) * np.linalg.norm(vec_b)
        )

        if denominator == 0:
            return 0.0

        return float(numerator / denominator)