from typing import Dict, Tuple, List
from logic_layer.primitives.base import Primitive
import re
import spacy

# Load spaCy once (not inside apply)
nlp = spacy.load("en_core_web_sm")


class Decompose(Primitive):
    """
    Decompose Primitive (Fully Corrected Version)
    --------------------------------------------
    Safely decomposes multi-intent prompts by:

    1. Splitting by sentence boundaries
    2. Splitting clauses ONLY when that specific sentence
       contains multiple action-level verbs

    Prevents incorrect splits such as:
    - "Compare REST and GraphQL"
    - "Node.js and Docker"
    """

    def apply(self, prompt: str, intent: Dict) -> Tuple[str, Dict]:

        complexity = intent.get("complexity", {})

        # Only consider decomposition if multi-intent detected
        if not complexity.get("multi_intent", False) or intent.get("task_type") == "explanation":
            return prompt, {
                "primitive": "decompose",
                "applied": False,
                "reason": "Single-intent prompt"
            }

        # -----------------------------
        # Step 1️⃣ Sentence-level split
        # -----------------------------
        doc = nlp(prompt)
        sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]

        subtasks: List[str] = []

        # -----------------------------
        # Step 2️⃣ Verb-aware clause split
        # -----------------------------
        for sentence in sentences:

            doc_sentence = nlp(sentence)
            sentence_verbs = [tok for tok in doc_sentence if tok.pos_ == "VERB"]

            # Only split if THIS sentence has multiple verbs
            if len(sentence_verbs) >= 2 and re.search(r"\band\b", sentence, re.IGNORECASE):
                clauses = [
                    c.strip()
                    for c in re.split(r"\band\b", sentence, flags=re.IGNORECASE)
                    if c.strip()
                ]
                subtasks.extend(clauses)
            else:
                subtasks.append(sentence)

        # If decomposition didn't meaningfully expand tasks, abort
        if len(subtasks) <= 1:
            return prompt, {
                "primitive": "decompose",
                "applied": False,
                "reason": "Unable to safely decompose"
            }

        # -----------------------------
        # Step 3️⃣ Construct structured output
        # -----------------------------
        updated_prompt = "\n".join(
            f"Task {i + 1}: {task}"
            for i, task in enumerate(subtasks)
        )

        return updated_prompt, {
            "primitive": "decompose",
            "applied": True,
            "subtasks": subtasks,
            "notes": "Sentence-aware, verb-level multi-intent decomposition"
        }
