from typing import Dict, Tuple
from logic_layer.primitives.base import Primitive


class ScopeAlign(Primitive):
    """
    ScopeAlign Primitive (Improved Version)
    --------------------------------------
    Narrows overly broad short explanation prompts.
    """

    def apply(self, prompt: str, intent: Dict) -> Tuple[str, Dict]:

        task_type = intent.get("task_type", "")
        complexity = intent.get("complexity", {})

        word_count = len(prompt.split())

        broad_short_explanation = (
            task_type == "explanation"
            and word_count <= 6
            and not complexity.get("multi_intent", False)
        )

        if not broad_short_explanation:
            return prompt, {
                "primitive": "scope_align",
                "applied": False,
                "reason": "Prompt scope acceptable"
            }

        updated_prompt = (
            prompt.strip() +
            "\n\nFocus specifically on core principles, key components, and practical applications."
        )

        return updated_prompt, {
            "primitive": "scope_align",
            "applied": True,
            "notes": "Scope narrowed for overly broad explanation"
        }
