from typing import Dict, List


class PromptRefiner:
    """
    Controlled LLM-Based Prompt Refiner
    -----------------------------------
    Generates a single, continuous, improved prompt
    using applied primitive metadata.
    """

    def __init__(self, llm_generate_function):
        self.llm = llm_generate_function

    def refine(
        self,
        original_prompt: str,
        intent: Dict,
        applied_primitives: List[str]
    ) -> str:

        rewrite_instruction = f"""
Instruction:
Rewrite the following prompt into a single clear,
well-structured instruction. Preserve meaning.
Do not add extra commentary.

Prompt:
{original_prompt}

Refined:
"""


        refined_prompt = self.llm(
            rewrite_instruction,
            temperature=0.2,
            max_tokens=200
        )

        return refined_prompt.strip()
