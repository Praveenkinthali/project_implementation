from typing import Dict, Tuple
from logic_layer.primitives.base import Primitive


class ConstrainOutput(Primitive):
    """
    ConstrainOutput Primitive (Final Stable Version)
    ------------------------------------------------
    Adds dynamic length and structural constraints.
    Activation is controlled by the Controller.
    """

    def apply(self, prompt: str, intent: Dict) -> Tuple[str, Dict]:

        constraints = intent.get("constraints", {})
        task_type = intent.get("task_type", "")
        complexity = intent.get("complexity", {})

        additions = []

        # -----------------------------
        # Length Constraint
        # -----------------------------
        if not constraints.get("has_limit", False):

            if task_type == "definition":
                additions.append("Keep the response concise (80–120 words).")

            elif task_type == "comparison":
                additions.append("Limit the response to approximately 200–300 words.")

            elif task_type == "procedure":
                additions.append("Keep explanations brief and focused (150–200 words).")

            else:
                additions.append("Limit the response to approximately 150–250 words.")

        # -----------------------------
        # Structure Constraint
        # -----------------------------
        if not constraints.get("has_format", False):

            if task_type == "comparison":
                additions.append(
                    "Present differences clearly using bullet points."
                )

            elif task_type == "procedure":
                additions.append("Present steps in a numbered list.")

            elif task_type == "code_generation":
                additions.append(
                    "Provide the solution inside a properly formatted code block."
                )

            else:
                additions.append(
                    "Structure the response clearly using headings or bullet points."
                )

        # -----------------------------
        # Multi-intent Handling
        # -----------------------------
        if complexity.get("multi_intent", False):
            additions.append("Address each part of the question separately.")

        # -----------------------------
        # Nothing to add
        # -----------------------------
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
            "notes": "Dynamic output constraints injected"
        }
