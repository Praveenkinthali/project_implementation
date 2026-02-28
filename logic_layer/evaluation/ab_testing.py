from typing import Dict, Optional


class ABTestingEngine:
    """
    Compares two evaluation results and selects winner.
    """

    def compare_scores(
        self,
        result_a: Dict,
        result_b: Dict
    ) -> Dict:

        score_a = result_a.get("final_score", 0)
        score_b = result_b.get("final_score", 0)

        if score_a > score_b:
            winner = "A"
        elif score_b > score_a:
            winner = "B"
        else:
            winner = "Tie"

        return {
            "score_A": score_a,
            "score_B": score_b,
            "winner": winner
        }

    def compare_with_judge(
        self,
        judge_result_a: Dict,
        judge_result_b: Dict
    ) -> Dict:

        score_a = judge_result_a.get("overall_quality", 0)
        score_b = judge_result_b.get("overall_quality", 0)

        if score_a > score_b:
            winner = "A"
        elif score_b > score_a:
            winner = "B"
        else:
            winner = "Tie"

        return {
            "judge_score_A": score_a,
            "judge_score_B": score_b,
            "winner": winner
        }