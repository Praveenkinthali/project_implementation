from typing import Dict, Tuple
from logic_layer.primitives.base import Primitive


class AddExample(Primitive):
    """
    AddExample Primitive 
    ----------------------------------------------
    Adds example instruction safely without stacking.
    """

    def apply(self, prompt: str, intent: Dict) -> Tuple[str, Dict]:

        existing = prompt.lower()

        if "illustrative example" in existing:
            return prompt, {
                "primitive": "add_example",
                "applied": False,
                "reason": "Example instruction already present"
            }

        task_type = intent.get("task_type", "")
        complexity = intent.get("complexity", {})
        constraints = intent.get("constraints", {})

        if constraints.get("has_example", False):
            return prompt, {"primitive": "add_example", "applied": False}

        if complexity.get("multi_intent", False):
            return prompt, {"primitive": "add_example", "applied": False}

        if task_type != "explanation":
            return prompt, {"primitive": "add_example", "applied": False}

        if len(prompt.split()) < 5:
            return prompt, {"primitive": "add_example", "applied": False}

        updated_prompt = (
            prompt.strip() +
            "\n\nAfter explaining, include one clear, minimal illustrative example."
        )

        return updated_prompt, {
            "primitive": "add_example",
            "applied": True,
            "notes": "Example instruction safely added"
        }
