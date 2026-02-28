import json
import os
from datetime import datetime
from typing import Optional, Dict


class FeedbackStore:
    """
    Stores user feedback and evaluation outcomes.
    Used for adaptive learning and analysis.
    """

    def __init__(self, file_path="logic_layer/evaluation/feedback_log.json"):
        self.file_path = file_path
        self._initialize()

    # ---------------------------
    # Initialization
    # ---------------------------

    def _initialize(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

    # ---------------------------
    # Store Feedback
    # ---------------------------

    def store(
        self,
        session_id: str,
        final_score: float,
        user_rating: Optional[int] = None,
        comment: Optional[str] = None
    ):

        data = self._load()

        entry = {
            "session_id": session_id,
            "final_score": final_score,
            "user_rating": user_rating,
            "comment": comment,
            "timestamp": datetime.utcnow().isoformat()
        }

        data.append(entry)

        self._save(data)

    # ---------------------------
    # Retrieval
    # ---------------------------

    def get_all(self) -> list:
        return self._load()

    def get_average_user_rating(self) -> float:
        data = self._load()
        ratings = [d["user_rating"] for d in data if d["user_rating"]]

        if not ratings:
            return 0.0

        return sum(ratings) / len(ratings)

    # ---------------------------
    # Internal
    # ---------------------------

    def _load(self):
        with open(self.file_path, "r") as f:
            return json.load(f)

    def _save(self, data):
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)