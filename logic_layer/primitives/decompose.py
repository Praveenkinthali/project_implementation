from typing import Dict, Tuple, List
from logic_layer.primitives.base import Primitive
import re


class Decompose(Primitive):
    """
    Decompose Primitive (FINAL FIX)
    -------------------------------
    Safely decomposes multi-intent prompts using sentence-first strategy.
    """

    def apply(self, prompt: str, intent: Dict) -> Tuple[str, Dict]:
        complexity = intent.get("complexity", {})

        if not complexity.get("multi_intent", False):
            return prompt, {
                "primitive": "decompose",
                "applied": False,
                "reason": "Single-intent prompt"
            }

        # ---------- Step 1: Sentence-level split ----------
        sentences = [
            s.strip()
            for s in re.split(r'[.!?]', prompt)
            if s.strip()
        ]

        subtasks: List[str] = []

        # ---------- Step 2: Clause-level split (careful) ----------
        for sentence in sentences:
            # Split only if sentence clearly contains multiple intents
            if " and " in sentence.lower():
                clauses = [
                    c.strip()
                    for c in sentence.split(" and ")
                    if c.strip()
                ]
                subtasks.extend(clauses)
            else:
                subtasks.append(sentence)

        # If decomposition is not meaningful, abort
        if len(subtasks) <= 1:
            return prompt, {
                "primitive": "decompose",
                "applied": False,
                "reason": "Unable to safely decompose"
            }

        # Build readable decomposed prompt
        decomposed_lines = [
            f"Task {i+1}: {task}"
            for i, task in enumerate(subtasks)
        ]

        updated_prompt = "\n".join(decomposed_lines)

        return updated_prompt, {
            "primitive": "decompose",
            "applied": True,
            "subtasks": subtasks,
            "notes": "Sentence-aware multi-intent decomposition"
        }
