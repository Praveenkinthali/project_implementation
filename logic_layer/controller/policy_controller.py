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
    Stable Policy-Based Prompt Controller
    --------------------------------------
    - Deterministic scoring
    - Numeric scores only
    - Activation threshold controlled
    """

    def __init__(self, activation_threshold: float = 0.5):
        self.analyzer = IntentAnalyzer()
        self.activation_threshold = activation_threshold

        self.primitives = {
            "clarify": Clarify(),
            "scope_align": ScopeAlign(),
            "simplify": Simplify(),
            "decompose": Decompose(),
            "add_example": AddExample(),
            "constrain": ConstrainOutput(),
            "format_enforce": FormatEnforce(),
            "self_reflect": SelfReflect(),
        }

    # =====================================================
    # 1️⃣ Scoring Function (FLOAT ONLY)
    # =====================================================
    def score_primitives(self, intent: Dict) -> Dict[str, float]:

        scores = {}

        ambiguity = intent.get("ambiguity", {})
        complexity = intent.get("complexity", {})
        style = intent.get("style", {})
        constraints = intent.get("constraints", {})
        risk = intent.get("risk", {})
        task_type = intent.get("task_type", "")

        # Clarify
        scores["clarify"] = 1.0 if any(ambiguity.values()) else 0.0

        # Scope Align
        scores["scope_align"] = 0.7 if task_type == "explanation" else 0.0

        # Simplify
        scores["simplify"] = 0.7 if style.get("is_verbose", False) else 0.0

        # Decompose
        scores["decompose"] = 0.8 if complexity.get("multi_intent", False) else 0.0

        # Add Example
        if task_type in {"explanation", "analysis"} and not constraints.get("has_example", False):
            scores["add_example"] = 0.7
        else:
            scores["add_example"] = 0.0

        # Constrain
        if (
            risk.get("output_risk_level") in {"medium", "high"}
            or complexity.get("multi_intent", False)
            or task_type in {"comparison", "procedure"}
        ):
            scores["constrain"] = 0.6
        else:
            scores["constrain"] = 0.0

        # Format Enforce
        scores["format_enforce"] = 0.8 if task_type in {"comparison", "code_generation"} else 0.0

        # Self Reflect
        if task_type in {"analysis", "comparison"} or complexity.get("multi_intent", False):
            scores["self_reflect"] = 0.7
        else:
            scores["self_reflect"] = 0.0

        return scores

    # =====================================================
    # 2️⃣ Primitive Selection
    # =====================================================
    def select_primitives(self, intent: Dict) -> List[str]:

        scores = self.score_primitives(intent)

        return [
            name
            for name, score in scores.items()
            if float(score) >= self.activation_threshold
        ]

    # =====================================================
    # 3️⃣ Optimization Pipeline
    # =====================================================
    def optimize(self, prompt: str) -> Tuple[str, List[str]]:

        intent = self.analyzer.analyze(prompt)
        selected = self.select_primitives(intent)

        execution_order = [
            "clarify",
            "scope_align",
            "simplify",
            "decompose",
            "add_example",
            "constrain",
            "format_enforce",
            "self_reflect",
        ]

        current_prompt = prompt
        used_primitives = []

        for name in execution_order:
            if name in selected:
                primitive = self.primitives[name]
                updated_prompt, meta = primitive.apply(current_prompt, intent)

                if meta.get("applied", False):
                    current_prompt = updated_prompt
                    used_primitives.append(name)

        return current_prompt, used_primitives
