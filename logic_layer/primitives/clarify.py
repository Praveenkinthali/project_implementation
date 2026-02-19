from typing import Dict, Tuple, List
import re
from logic_layer.primitives.base import Primitive


class Clarify(Primitive):
    """
    Clarify Primitive (FINAL VERIFIED VERSION)
    -----------------------------------------
    Adds clarification cues ONLY when semantic ambiguity exists.
    """

    def _replace_word(self, text: str, word: str, replacement: str) -> str:
        pattern = r"\b" + re.escape(word) + r"\b"
        return re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    def apply(self, prompt: str, intent: Dict) -> Tuple[str, Dict]:
        ambiguity = intent.get("ambiguity", {})
        updated_prompt = prompt.strip()
        insertions: List[str] = []
        clarification_types: List[str] = []

        # 1️⃣ Vague pronouns
        if ambiguity.get("vague_pronouns", False):
            updated_prompt = self._replace_word(
                updated_prompt, "this",
                "this [clarify: specify what 'this' refers to]"
            )
            updated_prompt = self._replace_word(
                updated_prompt, "that",
                "that [clarify: specify what 'that' refers to]"
            )
            updated_prompt = self._replace_word(
                updated_prompt, "it",
                "it [clarify: specify what 'it' refers to]"
            )
            insertions.append("clarify vague references")
            clarification_types.append("reference")

        # 2️⃣ Missing domain
        if ambiguity.get("missing_domain", False) and "domain" not in updated_prompt.lower():
            updated_prompt += " [clarify: specify the domain or subject area]"
            insertions.append("clarify domain")
            clarification_types.append("domain")

        # 3️⃣ Underspecified object
        if ambiguity.get("underspecified_object", False):
            updated_prompt += " [clarify: specify the exact topic or concept]"
            insertions.append("clarify object")
            clarification_types.append("object")

        # 4️⃣ Missing comparison criteria
        if ambiguity.get("missing_comparison_criteria", False):
            updated_prompt += (
                " [clarify: specify comparison criteria such as time complexity, "
                "space usage, or use-case]"
            )
            insertions.append("clarify comparison criteria")
            clarification_types.append("criteria")

        # Ask audience ONLY when scope/depth ambiguity exists
        if any(t in {"domain", "object"} for t in clarification_types):
            updated_prompt += (
                " [clarify: specify target audience "
                "(beginner / intermediate / advanced)]"
            )

        if not insertions:
            return prompt, {
                "primitive": "clarify",
                "applied": False,
                "reason": "No hard ambiguity detected"
            }

        return updated_prompt, {
            "primitive": "clarify",
            "applied": True,
            "insertions": insertions,
            "clarification_types": clarification_types,
            "notes": "Clarification cues inserted for prompt reframing"
        }
