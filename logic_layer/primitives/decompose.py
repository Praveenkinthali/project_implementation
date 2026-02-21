from typing import Dict, Tuple, List
from logic_layer.primitives.base import Primitive
import spacy

# Load spaCy once
nlp = spacy.load("en_core_web_sm")


class Decompose(Primitive):
    """
    Decompose Primitive (Safe & Stable Version)
    -------------------------------------------
    Decomposes multi-intent prompts strictly at sentence boundaries.
    Avoids clause-level splitting to prevent semantic corruption.

    This prevents incorrect splits like:
    - "advantages and limitations"
    - "security and scalability"
    - "REST and GraphQL"
    """

    def apply(self, prompt: str, intent: Dict) -> Tuple[str, Dict]:

        complexity = intent.get("complexity", {})
        task_type = intent.get("task_type", "")

        # Only decompose when multi-intent AND not simple explanation
        if not complexity.get("multi_intent", False) or task_type == "explanation":
            return prompt, {
                "primitive": "decompose",
                "applied": False,
                "reason": "Single-intent or explanation task"
            }

        doc = nlp(prompt)

        # Sentence-level splitting only
        sentences: List[str] = [
            sent.text.strip()
            for sent in doc.sents
            if sent.text.strip()
        ]

        # If only one sentence, no safe decomposition possible
        if len(sentences) <= 1:
            return prompt, {
                "primitive": "decompose",
                "applied": False,
                "reason": "Only one sentence detected"
            }

        # Build structured task format
        updated_prompt = "\n".join(
            f"Task {i + 1}: {sentence}"
            for i, sentence in enumerate(sentences)
        )

        return updated_prompt, {
            "primitive": "decompose",
            "applied": True,
            "subtasks": sentences,
            "notes": "Safe sentence-level decomposition applied"
        }
