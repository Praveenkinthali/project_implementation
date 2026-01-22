from typing import Dict, Tuple
from logic_layer.primitives.base import Primitive


class ConstrainOutput(Primitive):
    """
    ConstrainOutput Primitive
    ------------------------
    Explicitly specifies output length, style, and structure
    when they are not provided by the user.
    """

    def apply(self, prompt: str, intent: Dict) -> Tuple[str, Dict]:
        constraints = intent.get("constraints", {})

        additions = []

        # Length constraint
        if not constraints.get("has_limit", False):
            additions.append(
                "Limit the response to approximately 150–200 words."
            )

        # Format / structure constraint
        if not constraints.get("has_format", False):
            additions.append(
                "Structure the response clearly using headings or bullet points."
            )

        # If nothing to add, do nothing
        if not additions:
            return prompt, {
                "primitive": "constrain_output",
                "applied": False,
                "reason": "Output constraints already specified"
            }

        updated_prompt = prompt.strip() + "\n\n" + "\n".join(additions)

        return updated_prompt, {
            "primitive": "constrain_output",
            "applied": True,
            "constraints_added": additions,
            "notes": "Explicit output constraints added for better LLM control"
        }
