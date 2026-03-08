from fastapi import APIRouter
from pydantic import BaseModel
import json
import os
from datetime import datetime

from logic_layer.learning.reward_engine import RewardEngine
from logic_layer.evaluation.adaptive_learning import AdaptiveLearningEngine

router = APIRouter()

reward_engine = RewardEngine()
learning_engine = AdaptiveLearningEngine()


class FeedbackRequest(BaseModel):
    message_index: int
    rating: int


def get_feedback_path():

    base_dir = os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )

    return os.path.join(
        base_dir,
        "logic_layer",
        "evaluation",
        "feedback_log.json"
    )


@router.post("/feedback")
def receive_feedback(data: FeedbackRequest):

    rating = data.rating
    message_index = data.message_index

    log_path = get_feedback_path()

    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    if not os.path.exists(log_path):

        with open(log_path, "w") as f:
            json.dump([], f)

    with open(log_path, "r") as f:
        logs = json.load(f)

    if len(logs) == 0:
        return {"status": "no sessions found"}

    logs[-1]["user_rating"] = rating
    logs[-1]["timestamp"] = datetime.utcnow().isoformat()

    with open(log_path, "w") as f:
        json.dump(logs, f, indent=2)

    final_score = logs[-1].get("final_score", 0.5)
    primitives = logs[-1].get("primitives", [])

    reward = reward_engine.compute_reward(final_score, rating)

    learning_engine.update_reward(primitives, reward)

    print("Feedback stored:", rating)
    print("Primitives used:", primitives)
    print("Reward computed:", reward)

    return {
        "status": "feedback stored",
        "reward": reward
    }