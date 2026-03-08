from typing import Dict, List
import random
import math

from logic_layer.intent.intent_analyzer import IntentAnalyzer
from logic_layer.primitives.clarify import Clarify
from logic_layer.primitives.decompose import Decompose
from logic_layer.primitives.simplify import Simplify
from logic_layer.primitives.constrain_output import ConstrainOutput
from logic_layer.primitives.add_example import AddExample
from logic_layer.primitives.scope_align import ScopeAlign
from logic_layer.primitives.self_reflect import SelfReflect
from logic_layer.primitives.format_enforce import FormatEnforce

from logic_layer.evaluation.adaptive_learning import AdaptiveLearningEngine


class PolicyController:

    def __init__(self):

        self.analyzer = IntentAnalyzer()
        self.learning_engine = AdaptiveLearningEngine()

        self.primitives = {
            "clarify": Clarify(),
            "simplify": Simplify(),
            "scope_align": ScopeAlign(),
            "decompose": Decompose(),
            "add_example": AddExample(),
            "constrain": ConstrainOutput(),
            "format_enforce": FormatEnforce(),
            "self_reflect": SelfReflect(),
        }

        self.benefit_weights = {
            "clarify": 1.0,
            "simplify": 0.8,
            "scope_align": 0.7,
            "decompose": 0.9,
            "add_example": 0.6,
            "constrain": 0.8,
            "format_enforce": 0.8,
            "self_reflect": 1.0,
        }

        self.structural_cost = {
            "clarify": 0.2,
            "simplify": 0.1,
            "scope_align": 0.3,
            "decompose": 0.5,
            "add_example": 0.3,
            "constrain": 0.7,
            "format_enforce": 0.8,
            "self_reflect": 0.9,
        }

        self.meta_primitives = {"constrain", "format_enforce", "self_reflect"}

        self.max_primitives = 3
        self.exploration_rate = 0.15

    # -------------------------------------------------
    # Learning weights (existing logic unchanged)
    # -------------------------------------------------

    def _get_learning_weights(self):

        ranked = self.learning_engine.get_ranked_primitives()

        learning_weights = {p: 1.0 for p in self.primitives}

        for name, stats in ranked:
            learning_weights[name] = 1 + stats.get("avg_score", 0)

        return learning_weights

    # -------------------------------------------------
    # UCB helper (NEW)
    # -------------------------------------------------

    def _ucb_bonus(self, primitive, stats, total_count, c=1.4):

        if primitive not in stats:
            return 2.0  # strong exploration for unseen primitives

        count = stats[primitive]["count"]
        avg = stats[primitive]["avg"]

        if count == 0:
            return 2.0

        return c * math.sqrt(math.log(total_count + 1) / count)

    # -------------------------------------------------
    # Load learning stats (NEW)
    # -------------------------------------------------

    def _get_learning_stats(self):

        data = self.learning_engine._load()

        stats = {}
        total = 0

        for primitive, values in data.items():

            if primitive == "global_feedback":
                continue

            count = values.get("count", 0)
            total_score = values.get("total_score", 0)

            avg = total_score / count if count else 0

            stats[primitive] = {
                "count": count,
                "avg": avg
            }

            total += count

        return stats, max(total, 1)

    # -------------------------------------------------
    # Primitive scoring (UPDATED WITH UCB)
    # -------------------------------------------------

    def score_primitives(self, intent, prompt, previous_primitives=None):

        previous_primitives = previous_primitives or []

        benefit_scores = {name: 0.0 for name in self.primitives}

        if intent["ambiguity"]:
            benefit_scores["clarify"] = self.benefit_weights["clarify"]

        if intent["complexity"]["multi_intent"]:
            benefit_scores["decompose"] = self.benefit_weights["decompose"]

        if intent["task_type"] == "explanation":
            benefit_scores["scope_align"] = self.benefit_weights["scope_align"]

        learning_weights = self._get_learning_weights()

        learning_stats, total_count = self.learning_engine.get_learning_stats()

        utility_scores = {}

        for name in benefit_scores:

            base_score = (
                benefit_scores[name] * learning_weights.get(name, 1.0)
            ) - self.structural_cost[name]

            # NEW: UCB exploration
            ucb = self._ucb_bonus(name, learning_stats, total_count)

            score = base_score + ucb

            if name in previous_primitives:
                score *= 0.6

            utility_scores[name] = score

        return utility_scores

    # -------------------------------------------------

    def select_primitives(self, utility_scores):

        if random.random() < self.exploration_rate:

            candidates = list(self.primitives.keys())
            random.shuffle(candidates)
            return candidates[:self.max_primitives]

        candidates = [
            (name, score)
            for name, score in utility_scores.items()
            if score > 0
        ]

        candidates.sort(key=lambda x: x[1], reverse=True)

        selected = []
        meta_count = 0

        for name, score in candidates:

            if name in self.meta_primitives:
                if meta_count >= 1:
                    continue
                meta_count += 1

            selected.append(name)

            if len(selected) >= self.max_primitives:
                break

        return selected

    # -------------------------------------------------

    def optimize(self, prompt, previous_primitives=None):

        intent = self.analyzer.analyze(prompt)

        utility_scores = self.score_primitives(
            intent,
            prompt,
            previous_primitives
        )

        selected = self.select_primitives(utility_scores)

        execution_order = [
            "clarify",
            "simplify",
            "scope_align",
            "decompose",
            "add_example",
            "constrain",
            "format_enforce",
            "self_reflect",
        ]

        current_prompt = prompt
        applied = []

        for name in execution_order:

            if name in selected:

                primitive = self.primitives[name]

                updated_prompt, meta = primitive.apply(current_prompt, intent)

                if meta.get("applied", False):
                    current_prompt = updated_prompt
                    applied.append(name)

        metadata = {
            "scores": utility_scores,
            "selected_primitives": selected,
            "applied_primitives": applied,
        }

        return current_prompt, metadata