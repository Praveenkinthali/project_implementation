import time
from groq import Groq
from .base_llm import BaseLLM


class GroqLLM(BaseLLM):

    def __init__(self, api_key: str, model_name: str = "llama-3.1-8b-instant"):
        self.client = Groq(api_key=api_key)
        self.model_name = model_name

    def generate(self, prompt: str, temperature: float = 0.7):

        start_time = time.time()

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )

        latency = time.time() - start_time

        output_text = response.choices[0].message.content

        return {
            "output": output_text,
            "latency": latency,
            "tokens_used": response.usage.total_tokens
        }