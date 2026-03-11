import json
import os
from datetime import datetime
from typing import Optional, List


class FeedbackStore:

    def __init__(self):

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
        )

        self.file_path = os.path.join(
            base_dir,
            "logic_layer",
            "evaluation",
            "feedback_log.json"
        )

        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

    def _load(self):
        with open(self.file_path, "r") as f:
            return json.load(f)

    def _save(self, data):
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    # ------------------------------------------------

    def store(
        self,
        session_id: str,
        final_score: float,
        primitives: Optional[List[str]] = None,
        user_rating: Optional[int] = None,
        comment: Optional[str] = None
    ):

        data = self._load()

        entry = {
            "session_id": session_id,
            "final_score": final_score,
            "primitives": primitives if primitives else [],
            "user_rating": user_rating,
            "comment": comment,
            "timestamp": datetime.utcnow().isoformat()
        }

        data.append(entry)

        self._save(data)

        print("SESSION STORED:", entry)

    # ------------------------------------------------

    def get_latest(self):

        data = self._load()

        if not data:
            return None

        return data[-1]

    # ------------------------------------------------
    # NEW FUNCTION (needed for PolicyUpdater)
    # ------------------------------------------------

    def get_average_user_rating(self):

        data = self._load()

        ratings = [
            entry["user_rating"]
            for entry in data
            if entry.get("user_rating") is not None
        ]

        if not ratings:
            return 3  # neutral default

        return sum(ratings) / len(ratings)