import os
import requests


class HuggingFaceLLM:
    """
    HuggingFace Router API Wrapper (Updated)
    ----------------------------------------
    Uses the new router endpoint.
    """

    def __init__(self, model="google/gemma-2b-it"):
        self.api_token = os.getenv("HF_TOKEN")

        if not self.api_token:
            raise ValueError("HF_TOKEN environment variable not set.")

        self.model = model
        self.api_url = f"https://router.huggingface.co/hf-inference/models/{model}"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def generate(self, prompt: str, temperature=0.2, max_tokens=200):

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "return_full_text": False
            }
        }

        response = requests.post(
            self.api_url,
            headers=self.headers,
            json=payload
        )

        if response.status_code != 200:
            raise Exception(f"Inference error: {response.text}")

        result = response.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"].strip()

        raise Exception(f"Unexpected response: {result}")
