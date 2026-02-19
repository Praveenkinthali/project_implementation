from typing import Dict, Tuple
from logic_layer.primitives.base import Primitive


class AddExample(Primitive):
    """
    AddExample Primitive (Stable Version)
    -------------------------------------
    Adds example instruction only for single-intent explanation tasks.
    """

    def apply(self, prompt: str, intent: Dict) -> Tuple[str, Dict]:

        task_type = intent.get("task_type", "")
        constraints = intent.get("constraints", {})
        complexity = intent.get("complexity", {})

        # Skip if example already requested
        if constraints.get("has_example", False):
            return prompt, {
                "primitive": "add_example",
                "applied": False,
                "reason": "User already requested example"
            }

        # Skip if multi-intent
        if complexity.get("multi_intent", False):
            return prompt, {
                "primitive": "add_example",
                "applied": False,
                "reason": "Multi-intent task"
            }

        # Apply ONLY for pure explanation tasks
        if task_type != "explanation":
            return prompt, {
                "primitive": "add_example",
                "applied": False,
                "reason": "Not a pure explanation task"
            }

        # Avoid trivial short prompts
        if len(prompt.split()) < 5:
            return prompt, {
                "primitive": "add_example",
                "applied": False,
                "reason": "Prompt too short"
            }

        updated_prompt = (
            prompt.strip() +
            "\n\nAfter explaining, include one clear, minimal illustrative example."
        )

        return updated_prompt, {
            "primitive": "add_example",
            "applied": True,
            "notes": "Example instruction appended"
        }
