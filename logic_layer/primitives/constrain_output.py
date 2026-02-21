from typing import Dict, Tuple
from logic_layer.primitives.base import Primitive


class ConstrainOutput(Primitive):
    """
    ConstrainOutput Primitive (Fully Idempotent Version)
    ----------------------------------------------------
    Adds output constraints without stacking or duplication.
    """

    def apply(self, prompt: str, intent: Dict) -> Tuple[str, Dict]:

        existing = prompt.lower()

        # Prevent duplication
        if (
            "limit the response" in existing
            or "structure the response clearly" in existing
            or "address each part of the question separately" in existing
        ):
            return prompt, {
                "primitive": "constrain_output",
                "applied": False,
                "reason": "Constraints already present"
            }

        constraints = intent.get("constraints", {})
        task_type = intent.get("task_type", "")
        complexity = intent.get("complexity", {})

        additions = []

        # Length constraint
        if not constraints.get("has_limit", False):
            if task_type == "comparison":
                additions.append("Limit the response to approximately 200–300 words.")
            elif task_type == "procedure":
                additions.append("Keep explanations brief and focused (150–200 words).")
            else:
                additions.append("Limit the response to approximately 150–250 words.")

        # Structure constraint
        if not constraints.get("has_format", False):
            if task_type == "comparison":
                additions.append("Present differences clearly using bullet points.")
            elif task_type == "procedure":
                additions.append("Present steps in a numbered list.")
            else:
                additions.append("Structure the response clearly using headings or bullet points.")

        # Multi-intent
        if complexity.get("multi_intent", False):
            additions.append("Address each part of the question separately.")

        if not additions:
            return prompt, {
                "primitive": "constrain_output",
                "applied": False,
                "reason": "No constraints required"
            }

        updated_prompt = prompt.strip() + "\n\n" + "\n".join(additions)

        return updated_prompt, {
            "primitive": "constrain_output",
            "applied": True,
            "constraints_added": additions,
            "notes": "Constraints safely injected"
        }
