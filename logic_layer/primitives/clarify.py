from typing import Dict, Tuple, List
import re
from logic_layer.primitives.base import Primitive


class Clarify(Primitive):
    """
    Clarify Primitive (Fully Idempotent Version)
    -------------------------------------------
    Inserts clarification cues only when ambiguity exists.
    Prevents recursive insertion and duplicate clarify tags.
    """

    def _replace_word_outside_clarify(self, text: str, word: str, replacement: str) -> str:
        """
        Replace a word only outside existing [clarify: ...] blocks.
        """
        segments = re.split(r"(\[clarify:.*?\])", text)
        for i in range(len(segments)):
            if not segments[i].startswith("[clarify:"):
                pattern = r"\b" + re.escape(word) + r"\b"
                segments[i] = re.sub(pattern, replacement, segments[i], flags=re.IGNORECASE)
        return "".join(segments)

    def apply(self, prompt: str, intent: Dict) -> Tuple[str, Dict]:

        # Prevent repeated clarification passes
        if "[clarify:" in prompt:
            return prompt, {
                "primitive": "clarify",
                "applied": False,
                "reason": "Clarification already present"
            }

        ambiguity = intent.get("ambiguity", {})
        updated_prompt = prompt.strip()
        insertions: List[str] = []
        clarification_types: List[str] = []

        # Vague pronouns
        if ambiguity.get("vague_pronouns", False):
            updated_prompt = self._replace_word_outside_clarify(
                updated_prompt,
                "it",
                "it [clarify: specify what 'it' refers to]"
            )
            insertions.append("clarify vague references")
            clarification_types.append("reference")

        # Missing domain
        if ambiguity.get("missing_domain", False):
            updated_prompt += " [clarify: specify the domain or subject area]"
            insertions.append("clarify domain")
            clarification_types.append("domain")

        # Underspecified object
        if ambiguity.get("underspecified_object", False):
            updated_prompt += " [clarify: specify the exact topic or concept]"
            insertions.append("clarify object")
            clarification_types.append("object")

        # Missing comparison criteria
        if ambiguity.get("missing_comparison_criteria", False):
            updated_prompt += (
                " [clarify: specify comparison criteria such as time complexity, "
                "space usage, or use-case]"
            )
            insertions.append("clarify comparison criteria")
            clarification_types.append("criteria")

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
            "notes": "Clarification cues inserted safely"
        }
