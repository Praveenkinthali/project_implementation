from typing import Dict
from .feedback_store import FeedbackStore


class PolicyUpdater:
    """
    Adjusts aggregation weights based on feedback trends.
    """

    def __init__(self, aggregation_engine):
        self.feedback_store = FeedbackStore()
        self.aggregation_engine = aggregation_engine

    def update_weights_from_feedback(self):

        avg_rating = self.feedback_store.get_average_user_rating()

        # Normalize 1-5 rating to 0-1
        normalized = avg_rating / 5

        # If users rate low, increase judge weight
        if normalized < 0.6:
            self.aggregation_engine.weights["judge"] += 0.05
            self.aggregation_engine.weights["semantic"] += 0.05

        # Normalize total weight
        total = sum(self.aggregation_engine.weights.values())

        for k in self.aggregation_engine.weights:
            self.aggregation_engine.weights[k] /= total

        return self.aggregation_engine.weights