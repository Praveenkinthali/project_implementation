import time
import requests
from .base_llm import BaseLLM


class HFOnlineLLM(BaseLLM):

    def __init__(self, model_name: str, api_token: str):
        self.model_name = model_name
        self.api_token = api_token

        self.api_url = f"https://router.huggingface.co/hf-inference/models/{model_name}"

        self.headers = {
            "Authorization": f"Bearer {api_token}"
        }

    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 200,
        temperature: float = 0.7
    ):

        start_time = time.time()

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_new_tokens,
                "temperature": temperature
            }
        }

        response = requests.post(
            self.api_url,
            headers=self.headers,
            json=payload
        )

        latency = time.time() - start_time

        if response.status_code != 200:
            raise Exception(f"HF API Error: {response.text}")

        result = response.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            output_text = result[0]["generated_text"]
        else:
            output_text = str(result)

        return {
            "output": output_text,
            "latency": latency,
            "tokens_used": None
        }