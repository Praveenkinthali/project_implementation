from typing import Dict, Tuple
from logic_layer.primitives.base import Primitive


class SelfReflect(Primitive):
    """
    SelfReflect Primitive (Stable Version)
    -------------------------------------
    Adds reasoning reflection only for analytical and comparison tasks.
    """

    def apply(self, prompt: str, intent: Dict) -> Tuple[str, Dict]:

        task_type = intent.get("task_type", "")
        complexity = intent.get("complexity", {})
        risk = intent.get("risk", {})

        requires_reflection = (
            task_type in {"analysis", "comparison"}
            or (
                complexity.get("multi_intent", False)
                and task_type not in {"procedure"}
            )
            or risk.get("output_risk_level") == "high"
        )

        if not requires_reflection:
            return prompt, {
                "primitive": "self_reflect",
                "applied": False,
                "reason": "No analytical reflection required"
            }

        updated_prompt = (
            prompt.strip() +
            "\n\nBefore concluding, briefly verify the reasoning steps "
            "and state any key assumptions."
        )

        return updated_prompt, {
            "primitive": "self_reflect",
            "applied": True,
            "notes": "Analytical reflection instruction appended"
        }
