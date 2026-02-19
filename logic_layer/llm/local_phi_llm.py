import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


class LocalPhiLLM:
    """
    Local Lightweight Instruct Model
    ---------------------------------
    Uses microsoft/phi-2 for controlled rewriting.
    """

    def __init__(self, model_name="microsoft/phi-2"):

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32
        )

        self.model.eval()

    def generate(self, prompt: str, temperature=0.2, max_tokens=150):

        inputs = self.tokenizer(prompt, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True,
                top_p=0.9
            )

        text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Remove original prompt if echoed
        if text.startswith(prompt):
            text = text[len(prompt):]

        return text.strip()
