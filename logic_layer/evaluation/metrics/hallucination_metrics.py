import re
from typing import Dict


class HallucinationMetrics:
    """
    Heuristic-based hallucination risk estimation.
    """

    def compute(self, response: str) -> Dict:

        overconfidence_markers = [
            "definitely", "always", "guaranteed",
            "never fails", "proven fact"
        ]

        marker_count = sum(
            1 for m in overconfidence_markers
            if m in response.lower()
        )

        numeric_density = (
            len(re.findall(r"\d+", response))
            / max(len(response.split()), 1)
        )

        citation_presence = bool(
            re.search(r"\[\w+,\s*\d{4}\]", response)
        )

        hallucination_risk_score = (
            marker_count * 0.3
            + numeric_density * 0.2
            - (0.2 if citation_presence else 0)
        )

        return {
            "overconfidence_markers": marker_count,
            "numeric_density": round(numeric_density, 4),
            "citation_detected": citation_presence,
            "hallucination_risk_score": round(max(hallucination_risk_score, 0), 4)
        }