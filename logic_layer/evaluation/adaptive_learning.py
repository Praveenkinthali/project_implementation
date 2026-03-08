import json
import os


class AdaptiveLearningEngine:

    def __init__(self):

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
        )

        self.storage_path = os.path.join(
            base_dir,
            "logic_layer",
            "evaluation",
            "learning_log.json"
        )

        self._initialize_storage()

    # ------------------------------------------------

    def _initialize_storage(self):

        directory = os.path.dirname(self.storage_path)
        os.makedirs(directory, exist_ok=True)

        if not os.path.exists(self.storage_path):

            with open(self.storage_path, "w") as f:
                json.dump({}, f, indent=2)

    # ------------------------------------------------

    def _load(self):

        if not os.path.exists(self.storage_path):
            return {}

        with open(self.storage_path, "r") as f:
            return json.load(f)

    # ------------------------------------------------

    def _save(self, data):

        with open(self.storage_path, "w") as f:
            json.dump(data, f, indent=2)

    # ------------------------------------------------
    # RECORD PRIMITIVE PERFORMANCE
    # ------------------------------------------------

    def record(self, primitives_used, score):

        if not primitives_used:
            print("No primitives used — skipping learning record")
            return

        data = self._load()

        for primitive in primitives_used:

            if primitive not in data:

                data[primitive] = {
                    "count": 0,
                    "total_score": 0
                }

            data[primitive]["count"] += 1
            data[primitive]["total_score"] += score

        self._save(data)

        print("Primitive learning updated:", primitives_used)

    # ------------------------------------------------
    # PRIMITIVE RANKING
    # ------------------------------------------------

    def get_ranked_primitives(self):

        data = self._load()

        ranking = []

        for primitive, stats in data.items():

            if primitive == "global_feedback":
                continue

            count = stats.get("count", 0)
            total = stats.get("total_score", 0)

            avg = total / count if count else 0

            ranking.append(
                (
                    primitive,
                    {
                        "count": count,
                        "avg_score": avg
                    }
                )
            )

        ranking.sort(key=lambda x: x[1]["avg_score"], reverse=True)

        return ranking

    # ------------------------------------------------
    # RL USER FEEDBACK
    # ------------------------------------------------

    def update_reward(self, primitives_used, reward):

        data = self._load()

        if primitives_used:

            for primitive in primitives_used:

                if primitive not in data:

                    data[primitive] = {
                        "count": 0,
                        "total_score": 0
                    }

                data[primitive]["count"] += 1
                data[primitive]["total_score"] += reward

        if "global_feedback" not in data:

            data["global_feedback"] = {
                "count": 0,
                "total_reward": 0
            }

        data["global_feedback"]["count"] += 1
        data["global_feedback"]["total_reward"] += reward

        self._save(data)

        print("RL feedback updated:", primitives_used, reward)
    
        # ------------------------------------------------
    # GET STATS FOR UCB CONTROLLER
    # ------------------------------------------------

    def get_learning_stats(self):

        data = self._load()

        stats = {}
        total_count = 0

        for primitive, values in data.items():

            if primitive == "global_feedback":
                continue

            count = values.get("count", 0)
            total_score = values.get("total_score", 0)

            avg = total_score / count if count else 0

            stats[primitive] = {
                "count": count,
                "avg_reward": avg
            }

            total_count += count

        return stats, max(total_count, 1)