from typing import Dict, Tuple, List
from logic_layer.primitives.base import Primitive
import re


class Simplify(Primitive):
    """
    Simplify Primitive (FINAL VERIFIED VERSION)
    ------------------------------------------
    Removes conversational filler while preserving grammatical integrity.
    """

    FILLER_PATTERNS = [
        r"\bplease\b",
        r"\bcan you\b",
        r"\bcould you\b",
        r"\bwould you\b",
        r"\bkindly\b",
        r"\bi want to\b",
        r"\bi would like to\b",
        r"\bbasically\b",
        r"\bactually\b",
        r"\bin a simple way\b",
        r"\bso that i can understand\b",
        r"\bi am confused\b",
        r"\bi am preparing for (my )?exams\b",
        r"\bi am preparing for interview\b",
    ]

    def apply(self, prompt: str, intent: Dict) -> Tuple[str, Dict]:
        style = intent.get("style", {})

        if not style.get("is_verbose", False):
            return prompt, {
                "primitive": "simplify",
                "applied": False,
                "reason": "Prompt is not verbose"
            }

        updated_prompt = prompt
        removed_phrases: List[str] = []

        # ---------- Remove filler phrases ----------
        for pattern in self.FILLER_PATTERNS:
            matches = re.findall(pattern, updated_prompt, flags=re.IGNORECASE)
            if matches:
                removed_phrases.extend(matches)
                updated_prompt = re.sub(
                    pattern, "", updated_prompt, flags=re.IGNORECASE
                )

        # ---------- Cleanup dangling conjunctions ----------
        updated_prompt = re.sub(r"^\s*and\s+", "", updated_prompt, flags=re.IGNORECASE)
        updated_prompt = re.sub(r"\s+and\s+", " ", updated_prompt, flags=re.IGNORECASE)

        # ---------- Remove orphaned 'about ...' fragments ----------
        updated_prompt = re.sub(
            r"\babout\s+[a-zA-Z\s]+[,\.]?\s*(?=[^a-zA-Z]|$)",
            "",
            updated_prompt,
            flags=re.IGNORECASE
        )

        # ---------- Remove orphaned 'it' ----------
        updated_prompt = re.sub(
            r"\bit\s+(clearly|properly)?\b",
            "",
            updated_prompt,
            flags=re.IGNORECASE
        )

        # ---------- Normalize whitespace & punctuation ----------
        updated_prompt = re.sub(r"\s+", " ", updated_prompt)
        updated_prompt = re.sub(r"\s+([?.!,])", r"\1", updated_prompt)
        updated_prompt = updated_prompt.strip()

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
            "notes": "Conversational filler removed with grammatical cleanup"
        }
