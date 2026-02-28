import json
import os
from typing import Dict, List


class AdaptiveLearningEngine:
    """
    Tracks historical evaluation results and updates:

    - Aggregation weights
    - Primitive priority scores
    """

    def __init__(self, storage_path="logic_layer/evaluation/learning_log.json"):
        self.storage_path = storage_path
        self._initialize_storage()

    # ============================================================
    # STORAGE INITIALIZATION
    # ============================================================

    def _initialize_storage(self):
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, "w") as f:
                json.dump({
                    "history": [],
                    "primitive_scores": {}
                }, f)

    def _load(self):
        with open(self.storage_path, "r") as f:
            return json.load(f)

    def _save(self, data):
        with open(self.storage_path, "w") as f:
            json.dump(data, f, indent=4)

    # ============================================================
    # RECORD SESSION RESULT
    # ============================================================

    def record(
        self,
        primitives_used: List[str],
        final_score: float,
        user_rating: int = None
    ):

        data = self._load()

        data["history"].append({
            "primitives": primitives_used,
            "final_score": final_score,
            "user_rating": user_rating
        })

        # Update primitive performance averages
        for p in primitives_used:
            if p not in data["primitive_scores"]:
                data["primitive_scores"][p] = {
                    "count": 0,
                    "avg_score": 0
                }

            entry = data["primitive_scores"][p]
            entry["count"] += 1
            entry["avg_score"] = (
                (entry["avg_score"] * (entry["count"] - 1) + final_score)
                / entry["count"]
            )

        self._save(data)

    # ============================================================
    # GET PRIMITIVE RANKING
    # ============================================================

    def get_ranked_primitives(self):

        data = self._load()

        scores = data["primitive_scores"]

        ranked = sorted(
            scores.items(),
            key=lambda x: x[1]["avg_score"],
            reverse=True
        )

        return ranked