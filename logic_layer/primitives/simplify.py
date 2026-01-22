from typing import Dict, Tuple, List
from logic_layer.primitives.base import Primitive
import re


class Simplify(Primitive):
    """
    Simplify Primitive
    ------------------
    Removes politeness, filler phrases, and redundant language
    while preserving the original task intent.
    """

    FILLER_PATTERNS = [
        r"\bplease\b",
        r"\bcan you\b",
        r"\bcould you\b",
        r"\bwould you\b",
        r"\bkindly\b",
        r"\bi want to\b",
        r"\bi would like to\b",
        r"\bi am\b",
        r"\bi'm\b",
        r"\bbasically\b",
        r"\bactually\b",
        r"\bin a simple way\b",
        r"\bso that i can understand\b",
        r"\bi am confused\b",
        r"\bi am preparing for\b.*?\b",
    ]

    def apply(self, prompt: str, intent: Dict) -> Tuple[str, Dict]:
        style = intent.get("style", {})

        # Only simplify verbose prompts
        if not style.get("is_verbose", False):
            return prompt, {
                "primitive": "simplify",
                "applied": False,
                "reason": "Prompt is not verbose"
            }

        updated_prompt = prompt
        removed_phrases: List[str] = []

        for pattern in self.FILLER_PATTERNS:
            matches = re.findall(pattern, updated_prompt, flags=re.IGNORECASE)
            if matches:
                removed_phrases.extend(matches)
                updated_prompt = re.sub(
                    pattern, "", updated_prompt, flags=re.IGNORECASE
                )

        # Normalize whitespace
        updated_prompt = re.sub(r"\s+", " ", updated_prompt).strip()

        # If nothing was removed, do nothing
        if not removed_phrases:
            return prompt, {
                "primitive": "simplify",
                "applied": False,
                "reason": "No removable filler detected"
            }

        return updated_prompt, {
            "primitive": "simplify",
            "applied": True,
            "removed_phrases": removed_phrases,
            "notes": "Politeness and filler language removed"
        }
