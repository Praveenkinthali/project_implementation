
import json
import re


class LLMJudge:
    """
    LLM-based evaluation module.

    Uses an external LLM to evaluate:
    - Clarity
    - Relevance
    - Completeness
    - Factual reliability
    - Overall quality

    Returns structured numeric scores.
    """

    def __init__(self, llm):
        self.llm = llm

    # ----------------------------------------------------------
    # Public API
    # ----------------------------------------------------------

    def evaluate(self, prompt: str, response: str):

        judge_prompt = self._build_judge_prompt(prompt, response)

        result = self.llm.generate(judge_prompt)

        raw_output = result["output"]

        parsed = self._parse_output(raw_output)

        return parsed

    # ----------------------------------------------------------
    # Judge Prompt Builder
    # ----------------------------------------------------------

    def _build_judge_prompt(self, prompt: str, response: str):

        return f"""
You are an expert AI evaluator.

Evaluate the quality of the response based on the following criteria.
Give each score from 1 to 10.

Criteria:
1. Clarity
2. Relevance to prompt
3. Completeness
4. Factual reliability
5. Overall quality

Return ONLY a valid JSON object in this format:

{{
  "clarity": <number>,
  "relevance": <number>,
  "completeness": <number>,
  "factual_reliability": <number>,
  "overall_quality": <number>,
  "feedback": "<brief feedback>"
}}

Prompt:
{prompt}

Response:
{response}
"""

    # ----------------------------------------------------------
    # Robust JSON Parsing
    # ----------------------------------------------------------

    def _parse_output(self, text: str):

        try:
            # Extract JSON block from text
            json_match = re.search(r"\{.*\}", text, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
            else:
                raise ValueError("No JSON detected")

        except Exception:
            # Fallback default
            parsed = {
                "clarity": 5,
                "relevance": 5,
                "completeness": 5,
                "factual_reliability": 5,
                "overall_quality": 5,
                "feedback": "Parsing failed. Default scores applied."
            }

        return parsed