import os
from openai import OpenAI


class OpenAILLM:
    """
    OpenAI LLM Wrapper for Prompt Refinement
    ----------------------------------------
    Uses GPT-4o-mini for stable semantic rewriting.
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable not set."
            )

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, temperature=0.2, max_tokens=200):

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert prompt optimization engine."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content.strip()
