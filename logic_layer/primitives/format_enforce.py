from typing import Dict, Tuple
from logic_layer.primitives.base import Primitive


class FormatEnforce(Primitive):
    """
    FormatEnforce Primitive (Fully Idempotent Version)
    --------------------------------------------------
    Enforces strict formatting only when required and prevents stacking.
    """

    def apply(self, prompt: str, intent: Dict) -> Tuple[str, Dict]:

        existing = prompt.lower()

        if "strictly" in existing and "format" in existing:
            return prompt, {
                "primitive": "format_enforce",
                "applied": False,
                "reason": "Format enforcement already present"
            }

        task_type = intent.get("task_type", "")

        if task_type == "comparison":
            rule = "Return the comparison strictly in a structured table format."
        elif task_type == "procedure":
            rule = "Return the solution strictly as a numbered step-by-step list."
        elif task_type == "code_generation":
            rule = "Return only the final solution inside a properly formatted code block."
        else:
            return prompt, {
                "primitive": "format_enforce",
                "applied": False,
                "reason": "No strict format required"
            }

        updated_prompt = prompt.strip() + "\n\n" + rule

        return updated_prompt, {
            "primitive": "format_enforce",
            "applied": True,
            "notes": "Format rule safely enforced"
        }
