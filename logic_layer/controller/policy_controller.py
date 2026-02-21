from typing import Dict, List, Tuple
from logic_layer.intent.intent_analyzer import IntentAnalyzer
from logic_layer.primitives.clarify import Clarify
from logic_layer.primitives.decompose import Decompose
from logic_layer.primitives.simplify import Simplify
from logic_layer.primitives.constrain_output import ConstrainOutput
from logic_layer.primitives.add_example import AddExample
from logic_layer.primitives.scope_align import ScopeAlign
from logic_layer.primitives.self_reflect import SelfReflect
from logic_layer.primitives.format_enforce import FormatEnforce


class PolicyController:
    """
    Research-Grade Utility-Based Controller
    ---------------------------------------
    - Benefit-weight configurable
    - Structural-cost configurable
    - Prompt-length aware
    - Meta-primitive capped
    - Max 3 activations
    """

    def __init__(self):

        self.analyzer = IntentAnalyzer()

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

        # -----------------------------
        # Benefit Weights (Tunable)
        # -----------------------------
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

        # -----------------------------
        # Structural Costs (Tunable)
        # -----------------------------
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

    # -------------------------------------------------
    # Utility Computation
    # -------------------------------------------------
    def score_primitives(self, intent: Dict, prompt: str) -> Dict[str, float]:

        ambiguity = intent["ambiguity"]
        complexity = intent["complexity"]
        style = intent["style"]
        constraints = intent["constraints"]
        task_type = intent["task_type"]
        risk = intent["risk"]

        prompt_length = len(prompt.split())

        benefit_scores = {name: 0.0 for name in self.primitives}

        # ---------------- Benefit Conditions ----------------

        if any(ambiguity.values()):
            benefit_scores["clarify"] = self.benefit_weights["clarify"]

        if style["is_verbose"]:
            benefit_scores["simplify"] = self.benefit_weights["simplify"]

        if task_type == "explanation" and prompt_length <= 6:
            benefit_scores["scope_align"] = self.benefit_weights["scope_align"]

        if complexity["multi_intent"]:
            benefit_scores["decompose"] = self.benefit_weights["decompose"]
            benefit_scores["constrain"] = self.benefit_weights["constrain"]

        if (
            task_type == "explanation"
            and not constraints["has_example"]
            and not any(ambiguity.values())
        ):
            benefit_scores["add_example"] = self.benefit_weights["add_example"]

        if risk["output_risk_level"] == "high":
            benefit_scores["constrain"] = self.benefit_weights["constrain"]

        if task_type in {"comparison", "code_generation"}:
            benefit_scores["format_enforce"] = self.benefit_weights["format_enforce"]

        if task_type == "analysis":
            benefit_scores["self_reflect"] = self.benefit_weights["self_reflect"]

        if task_type == "comparison":
            benefit_scores["self_reflect"] = 0.8

        # ---------------- Prompt-Length Scaling ----------------

        if prompt_length <= 5:
            for p in self.meta_primitives:
                benefit_scores[p] *= 0.2

        elif prompt_length <= 12:
            benefit_scores["self_reflect"] *= 0.6
            benefit_scores["constrain"] *= 0.7
            
        # Additional semantic heuristics
        if prompt.lower().count(" i ") > 0:
            benefit_scores["simplify"] += 0.4

        if prompt.count(" and ") > 1:
            benefit_scores["decompose"] += 0.3

        if prompt_length < 6:
            benefit_scores["clarify"] += 0.4

        # ---------------- Utility = Benefit - Cost ----------------

        utility_scores = {}
        for name in benefit_scores:
            utility_scores[name] = benefit_scores[name] - self.structural_cost[name]

        return utility_scores

    # -------------------------------------------------
    # Primitive Selection
    # -------------------------------------------------
    def select_primitives(self, intent: Dict, prompt: str) -> List[str]:

        utility_scores = self.score_primitives(intent, prompt)

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
    # Single-Pass Optimization
    # -------------------------------------------------
    def optimize(self, prompt: str):

        intent = self.analyzer.analyze(prompt)

        scores = self.score_primitives(intent, prompt)
        selected = self.select_primitives(intent, prompt)

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
            "scores": scores,
            "selected_primitives": selected,
            "applied_primitives": applied,
        }

        return current_prompt, metadata

