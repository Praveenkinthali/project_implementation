import re
from typing import Dict


class ResponseMetrics:
    """
    Evaluates response quality improvements between
    original and optimized responses.

    Deterministic evaluation only.
    """

    # ============================================================
    # PUBLIC ENTRY
    # ============================================================

    def compute(
        self,
        original_prompt: str,
        optimized_prompt: str,
        original_response: str,
        optimized_response: str
    ) -> Dict:

        return {
            "length_metrics": self._length_metrics(original_response, optimized_response),
            "structure_metrics": self._structure_metrics(original_response, optimized_response),
            "relevance_metrics": self._relevance_metrics(optimized_prompt, optimized_response),
            "instruction_adherence": self._instruction_adherence(optimized_prompt, optimized_response),
            "completeness_metrics": self._completeness_metrics(optimized_prompt, optimized_response),
            "hallucination_proxies": self._hallucination_proxies(optimized_response),
            "coherence_indicators": self._coherence_indicators(optimized_response)
        }

    # ============================================================
    # LENGTH & EXPANSION
    # ============================================================

    def _length_metrics(self, original: str, optimized: str) -> Dict:

        orig_len = len(original.split())
        opt_len = len(optimized.split())

        return {
            "original_word_count": orig_len,
            "optimized_word_count": opt_len,
            "length_delta": opt_len - orig_len
        }

    # ============================================================
    # STRUCTURE IMPROVEMENT
    # ============================================================

    def _structure_metrics(self, original: str, optimized: str) -> Dict:

        def count_lists(text):
            return len(re.findall(r"\n\d+\.|\n- |\n\*", text))

        return {
            "paragraph_delta": optimized.count("\n") - original.count("\n"),
            "list_structure_delta": count_lists(optimized) - count_lists(original),
            "code_block_presence": "```" in optimized
        }

    # ============================================================
    # RELEVANCE METRICS
    # ============================================================

    def _relevance_metrics(self, prompt: str, response: str) -> Dict:

        prompt_words = set(prompt.lower().split())
        response_words = set(response.lower().split())

        overlap = prompt_words.intersection(response_words)

        relevance_score = len(overlap) / len(prompt_words) if prompt_words else 0

        return {
            "keyword_overlap_score": round(relevance_score, 4)
        }

    # ============================================================
    # INSTRUCTION ADHERENCE
    # ============================================================

    def _instruction_adherence(self, prompt: str, response: str) -> Dict:

        instruction_verbs = [
            "explain", "describe", "list", "analyze",
            "compare", "generate", "create", "summarize"
        ]

        prompt_instructions = [
            v for v in instruction_verbs if v in prompt.lower()
        ]

        adherence_hits = sum(
            1 for v in prompt_instructions if v in response.lower()
        )

        adherence_score = (
            adherence_hits / len(prompt_instructions)
            if prompt_instructions else 0
        )

        return {
            "detected_instructions": prompt_instructions,
            "instruction_adherence_score": round(adherence_score, 4)
        }

    # ============================================================
    # COMPLETENESS METRICS
    # ============================================================

    def _completeness_metrics(self, prompt: str, response: str) -> Dict:
        """
        Estimates whether structured subtasks were addressed.
        """

        numbered_tasks = re.findall(r"\d+\.", prompt)

        if not numbered_tasks:
            return {"task_completion_estimate": None}

        completed_sections = len(re.findall(r"\n\d+\.", response))

        completion_ratio = completed_sections / len(numbered_tasks)

        return {
            "expected_sections": len(numbered_tasks),
            "detected_sections": completed_sections,
            "task_completion_estimate": round(completion_ratio, 4)
        }

    # ============================================================
    # HALLUCINATION PROXY METRICS
    # ============================================================

    def _hallucination_proxies(self, response: str) -> Dict:

        overconfidence_markers = [
            "definitely", "always", "guaranteed", "proven"
        ]

        marker_count = sum(
            1 for m in overconfidence_markers
            if m in response.lower()
        )

        numeric_density = (
            len(re.findall(r"\d+", response)) /
            max(len(response.split()), 1)
        )

        return {
            "overconfidence_marker_count": marker_count,
            "numeric_density_ratio": round(numeric_density, 4)
        }

    # ============================================================
    # COHERENCE INDICATORS
    # ============================================================

    def _coherence_indicators(self, response: str) -> Dict:

        transitional_phrases = [
            "however", "therefore", "in addition",
            "for example", "on the other hand"
        ]

        transition_count = sum(
            1 for t in transitional_phrases
            if t in response.lower()
        )

        avg_sentence_length = self._avg_sentence_length(response)

        return {
            "transition_usage_count": transition_count,
            "avg_sentence_length": round(avg_sentence_length, 2)
        }

    def _avg_sentence_length(self, text: str) -> float:

        sentences = re.split(r"[.!?]", text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return 0

        total_words = sum(len(s.split()) for s in sentences)

        return total_words / len(sentences)