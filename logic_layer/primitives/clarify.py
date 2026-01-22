from typing import Dict, Tuple, List
import re
from logic_layer.primitives.base import Primitive


class Clarify(Primitive):
    """
    Clarify Primitive (FINAL)
    ------------------------
    Adds clarification cues ONLY when semantic ambiguity exists.
    """

    def _replace_word(self, text: str, word: str, replacement: str) -> str:
        pattern = r"\b" + re.escape(word) + r"\b"
        return re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    def apply(self, prompt: str, intent: Dict) -> Tuple[str, Dict]:
        ambiguity = intent.get("ambiguity", {})
        updated_prompt = prompt.strip()
        insertions: List[str] = []

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

        # 2️⃣ Missing domain
        if ambiguity.get("missing_domain", False):
            updated_prompt += " [clarify: specify the domain or subject area]"
            insertions.append("clarify domain")

        # 3️⃣ Underspecified object
        if ambiguity.get("underspecified_object", False):
            updated_prompt += " [clarify: specify the exact topic or concept]"
            insertions.append("clarify object")

        # 🔴 4️⃣ Missing comparison criteria (KEY FIX)
        if ambiguity.get("missing_comparison_criteria", False):
            updated_prompt += (
                " [clarify: specify comparison criteria such as time complexity, "
                "space usage, or use-case]"
            )
            insertions.append("clarify comparison criteria")

        # Ask audience only when hard ambiguity exists
        if insertions:
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
            "notes": "Clarification cues inserted for prompt reframing"
        }
