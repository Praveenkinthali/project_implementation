from typing import List, Dict
import re


class PromptSynthesizer:
    """
    Deterministic Prompt Synthesis Engine
    --------------------------------------
    Converts primitive outputs into a single clean,
    continuous optimized prompt.
    """

    def __init__(self):
        pass

    def _clean_whitespace(self, text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    def _merge_sentences(self, sentences: List[str]) -> str:
        merged = " ".join(s.strip() for s in sentences if s.strip())
        return self._clean_whitespace(merged)

    def refine(
        self,
        original_prompt: str,
        applied_primitives: List[str],
        intent: Dict
    ) -> str:

        base_prompt = original_prompt.strip()

        enhancements = []

        task_type = intent.get("task_type", "")
        ambiguity = intent.get("ambiguity", {})
        complexity = intent.get("complexity", {})

        # -------------------------------
        # Clarify
        # -------------------------------
        if "clarify" in applied_primitives:

            if ambiguity.get("vague_pronouns"):
                enhancements.append(
                    "Clearly define any ambiguous references."
                )

            if ambiguity.get("missing_domain"):
                enhancements.append(
                    "Specify the relevant domain or context."
                )

        # -------------------------------
        # Scope Align
        # -------------------------------
        if "scope_align" in applied_primitives:
            enhancements.append(
                "Focus specifically on core principles, key components, and practical applications."
            )

        # -------------------------------
        # Decompose
        # -------------------------------
        if "decompose" in applied_primitives:
            enhancements.append(
                "Address each part of the request separately and organize the response logically."
            )

        # -------------------------------
        # Add Example
        # -------------------------------
        if "add_example" in applied_primitives:
            enhancements.append(
                "Include one clear and minimal illustrative example."
            )

        # -------------------------------
        # Constrain
        # -------------------------------
        if "constrain" in applied_primitives:

            if task_type == "comparison":
                enhancements.append(
                    "Present the comparison concisely (200–300 words) in a structured format."
                )
            elif task_type == "procedure":
                enhancements.append(
                    "Provide concise step-by-step instructions (150–200 words)."
                )
            else:
                enhancements.append(
                    "Keep the explanation concise (150–250 words) and well-structured."
                )

        # -------------------------------
        # Format Enforce
        # -------------------------------
        if "format_enforce" in applied_primitives:
            if task_type == "comparison":
                enhancements.append(
                    "Present differences clearly in a structured table."
                )
            elif task_type == "code_generation":
                enhancements.append(
                    "Return the solution inside a properly formatted code block."
                )

        # -------------------------------
        # Self Reflect
        # -------------------------------
        if "self_reflect" in applied_primitives:
            enhancements.append(
                "Ensure logical consistency and clearly state key assumptions."
            )

        # ----------------------------------
        # Merge everything into single flow
        # ----------------------------------

        if enhancements:
            refined_prompt = self._merge_sentences(
                [base_prompt] + enhancements
            )
        else:
            refined_prompt = base_prompt

        return refined_prompt
