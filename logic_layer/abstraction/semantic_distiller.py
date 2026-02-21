from typing import Tuple
import re
import spacy
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

nlp = spacy.load("en_core_web_sm")


class SemanticDistiller:
    """
    Hybrid Semantic Distiller v2 (Strong Mode)
    -------------------------------------------
    Converts narrative / story-like input into
    concise imperative task instructions.
    """

    def __init__(self, use_llm_fallback: bool = True):
        self.use_llm_fallback = use_llm_fallback

        if use_llm_fallback:
            self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
            self.model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

    # -------------------------------------------------
    # Rewrite Trigger (Stronger)
    # -------------------------------------------------
    def _needs_rewrite(self, prompt: str) -> bool:

        lower = prompt.lower()

        narrative_markers = [
            "i am", "i'm", "i was", "i have",
            "i need", "i want", "i'm trying",
            "i am trying", "i am confused",
            "i'm confused", "because",
            "the reason", "i feel", "i think"
        ]

        if any(marker in lower for marker in narrative_markers):
            return True

        # Multiple sentences + conversational tone
        doc = nlp(prompt)
        if len(list(doc.sents)) > 1:
            if any(tok.text.lower() == "i" for tok in doc):
                return True

        return False

    # -------------------------------------------------
    # Strong Rewrite Instruction
    # -------------------------------------------------
    def _llm_rewrite(self, prompt: str) -> str:

        instruction = (
            "Rewrite the following user input as a clear, concise, "
            "task-oriented instruction.\n"
            "- Remove self-references (e.g., 'I am', 'I want').\n"
            "- Remove narrative or emotional language.\n"
            "- Preserve all important technical details.\n"
            "- Do NOT add new requirements.\n"
            "- Convert to direct imperative instruction.\n\n"
            f"User Input:\n{prompt}\n\n"
            "Optimized Instruction:"
        )

        inputs = self.tokenizer(
            instruction,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=120,
            do_sample=False
        )

        rewritten = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        return rewritten.strip()

    # -------------------------------------------------
    # Light Deterministic Cleaning
    # -------------------------------------------------
    def _basic_clean(self, prompt: str) -> str:
        prompt = re.sub(r"\s+", " ", prompt).strip()
        return prompt

    # -------------------------------------------------
    # Main Distill
    # -------------------------------------------------
    def distill(self, prompt: str) -> str:

        cleaned = self._basic_clean(prompt)

        if not self.use_llm_fallback:
            return cleaned

        if self._needs_rewrite(cleaned):
            try:
                rewritten = self._llm_rewrite(cleaned)
                return rewritten
            except Exception:
                return cleaned

        return cleaned
