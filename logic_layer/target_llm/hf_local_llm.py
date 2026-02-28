import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from .base_llm import BaseLLM


class HFLocalLLM(BaseLLM):

    def __init__(
        self,
        model_name: str = "microsoft/phi-2",
        device: str = None,
        max_new_tokens: int = 512
    ):

        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.max_new_tokens = max_new_tokens

        print(f"Loading model {model_name} on {self.device}...")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        ).to(self.device)

        self.model.eval()

    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        top_p: float = 0.9
    ):

        start_time = time.time()

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=True
            )

        latency = time.time() - start_time

        generated_text = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        tokens_used = outputs[0].shape[0]

        return {
            "output": generated_text[len(prompt):].strip(),
            "latency": latency,
            "tokens_used": tokens_used
        }