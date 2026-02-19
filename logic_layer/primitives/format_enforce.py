from typing import Dict, Tuple
from logic_layer.primitives.base import Primitive


class FormatEnforce(Primitive):
    """
    FormatEnforce Primitive (Final Fixed Version)
    ---------------------------------------------
    Enforces strict output structure only when required.
    """

    def apply(self, prompt: str, intent: Dict) -> Tuple[str, Dict]:

        constraints = intent.get("constraints", {})
        task_type = intent.get("task_type", "")

        additions = []

        # -----------------------------
        # Explicit user format request
        # -----------------------------
        if constraints.get("has_format", False):
            additions.append("Strictly follow the requested output format.")

        # -----------------------------
        # Comparison → Table
        # -----------------------------
        elif task_type == "comparison":
            additions.append(
                "Return the comparison strictly in a structured table format."
            )

        # -----------------------------
        # Procedure → Numbered Steps
        # -----------------------------
        elif task_type == "procedure":
            additions.append(
                "Return the solution strictly as a numbered step-by-step list."
            )

        # -----------------------------
        # Code generation → Code block
        # -----------------------------
        elif task_type == "code_generation":
            additions.append(
                "Return only the final solution inside a properly formatted code block."
            )

        else:
            return prompt, {
                "primitive": "format_enforce",
                "applied": False,
                "reason": "No strict format enforcement required"
            }

        updated_prompt = prompt.strip() + "\n\n" + "\n".join(additions)

        return updated_prompt, {
            "primitive": "format_enforce",
            "applied": True,
            "format_rules_added": additions,
            "notes": "Strict output format enforced"
        }
