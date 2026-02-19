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


class RLController:
    """
    Reinforcement-Based Prompt Controller (Final Stable Version)
    ------------------------------------------------------------
    - Controller selects primitives at high level
    - Primitives perform fine-grained filtering
    - Clean separation of concerns
    """

    def __init__(self, learning_rate: float = 0.05):
        self.analyzer = IntentAnalyzer()
        self.learning_rate = learning_rate

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

        self.policy = {name: 1.0 for name in self.primitives}

    # -------------------------------------------------
    # Primitive Selection Policy
    # -------------------------------------------------
    def select_primitives(self, intent: Dict) -> List[str]:

        selected = []

        ambiguity = intent.get("ambiguity", {})
        complexity = intent.get("complexity", {})
        style = intent.get("style", {})
        risk = intent.get("risk", {})
        task_type = intent.get("task_type", "")

        # 1️⃣ Clarify
        if any(ambiguity.values()):
            selected.append("clarify")

        # 2️⃣ ScopeAlign
        if task_type == "explanation":
            selected.append("scope_align")

        # 3️⃣ Simplify
        if style.get("is_verbose", False):
            selected.append("simplify")

        # 4️⃣ Decompose
        if complexity.get("multi_intent", False):
            selected.append("decompose")

        # 5️⃣ AddExample (pure explanation only)
        if task_type == "explanation":
            selected.append("add_example")

        # 6️⃣ ConstrainOutput
        if (
            risk.get("output_risk_level") in {"medium", "high"}
            or complexity.get("multi_intent", False)
            or task_type in {"comparison", "procedure"}
        ):
            selected.append("constrain")

        # 7️⃣ FormatEnforce
        if task_type in {"comparison", "procedure", "code_generation"}:
            selected.append("format_enforce")

        # 8️⃣ SelfReflect
        if (
            task_type in {"analysis", "comparison"}
            or complexity.get("multi_intent", False)
        ):
            selected.append("self_reflect")

        return selected

    # -------------------------------------------------
    # Optimization Pipeline
    # -------------------------------------------------
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

    # -------------------------------------------------
    # RL Policy Update
    # -------------------------------------------------
    def update_policy(self, used_primitives: List[str], reward: float):

        for name in used_primitives:
            if name in self.policy:
                self.policy[name] += self.learning_rate * reward

        # Prevent weight collapse
        for name in self.policy:
            self.policy[name] = max(0.1, self.policy[name])
