import difflib
import re
from typing import Dict


class PromptMetrics:
    """
    Evaluates transformation quality between
    original and optimized prompts.

    This module focuses ONLY on prompt-level changes.
    No LLM dependency.
    Deterministic + fast.
    """

    # ============================================================
    # PUBLIC ENTRY POINT
    # ============================================================

    def compute(self, original: str, optimized: str) -> Dict:
        """
        Returns structured prompt evaluation metrics.
        """

        return {
            "length_metrics": self._length_metrics(original, optimized),
            "structural_metrics": self._structural_metrics(original, optimized),
            "instruction_metrics": self._instruction_metrics(original, optimized),
            "constraint_metrics": self._constraint_metrics(original, optimized),
            "formatting_metrics": self._formatting_metrics(original, optimized),
            "specificity_metrics": self._specificity_metrics(original, optimized),
            "over_modification_risk": self._over_modification_score(original, optimized)
        }

    # ============================================================
    # LENGTH & COMPRESSION METRICS
    # ============================================================

    def _length_metrics(self, original: str, optimized: str) -> Dict:
        orig_len = len(original.split())
        opt_len = len(optimized.split())

        return {
            "original_word_count": orig_len,
            "optimized_word_count": opt_len,
            "length_delta": opt_len - orig_len,
            "compression_ratio": round(opt_len / orig_len, 4) if orig_len else 0
        }

    # ============================================================
    # STRUCTURAL TRANSFORMATION
    # ============================================================

    def _structural_metrics(self, original: str, optimized: str) -> Dict:
        similarity = difflib.SequenceMatcher(None, original, optimized).ratio()

        return {
            "similarity_ratio": round(similarity, 4),
            "structural_change_score": round(1 - similarity, 4),
            "line_count_change": optimized.count("\n") - original.count("\n")
        }

    # ============================================================
    # INSTRUCTION QUALITY
    # ============================================================

    def _instruction_metrics(self, original: str, optimized: str) -> Dict:
        instruction_verbs = [
            "explain", "describe", "list", "analyze",
            "compare", "generate", "create", "summarize"
        ]

        def count_verbs(text):
            return sum(1 for v in instruction_verbs if v in text.lower())

        return {
            "original_instruction_count": count_verbs(original),
            "optimized_instruction_count": count_verbs(optimized),
            "instruction_density_delta":
                count_verbs(optimized) - count_verbs(original)
        }

    # ============================================================
    # CONSTRAINT REINFORCEMENT
    # ============================================================

    def _constraint_metrics(self, original: str, optimized: str) -> Dict:
        constraint_markers = [
            "must", "only", "strictly", "limit",
            "format", "do not", "avoid", "ensure"
        ]

        def count_constraints(text):
            return sum(1 for c in constraint_markers if c in text.lower())

        return {
            "original_constraint_count": count_constraints(original),
            "optimized_constraint_count": count_constraints(optimized),
            "constraint_delta":
                count_constraints(optimized) - count_constraints(original)
        }

    # ============================================================
    # FORMATTING ENFORCEMENT
    # ============================================================

    def _formatting_metrics(self, original: str, optimized: str) -> Dict:
        formatting_patterns = [
            r"\n\d+\.",   # numbered lists
            r"\n- ",      # bullet points
            r"\n\*",      # star bullets
            r"```",       # code blocks
        ]

        def count_format_patterns(text):
            return sum(len(re.findall(p, text)) for p in formatting_patterns)

        return {
            "original_format_markers": count_format_patterns(original),
            "optimized_format_markers": count_format_patterns(optimized),
            "format_enforcement_delta":
                count_format_patterns(optimized) - count_format_patterns(original)
        }

    # ============================================================
    # SPECIFICITY METRICS
    # ============================================================

    def _specificity_metrics(self, original: str, optimized: str) -> Dict:
        """
        Detect increase in specificity via:
        - numbers
        - conditional statements
        - structured constraints
        """

        def count_numbers(text):
            return len(re.findall(r"\d+", text))

        def count_conditionals(text):
            return sum(1 for w in ["if", "when", "unless"] if w in text.lower())

        return {
            "number_delta": count_numbers(optimized) - count_numbers(original),
            "conditional_delta":
                count_conditionals(optimized) - count_conditionals(original)
        }

    # ============================================================
    # OVER-MODIFICATION DETECTION
    # ============================================================

    def _over_modification_score(self, original: str, optimized: str) -> float:
        """
        If similarity drops too low, we risk changing intent.
        This flags aggressive transformations.
        """

        similarity = difflib.SequenceMatcher(None, original, optimized).ratio()

        if similarity < 0.3:
            return 1.0  # High risk
        elif similarity < 0.5:
            return 0.5  # Moderate risk
        else:
            return 0.0  # Safe