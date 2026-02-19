import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


class GraniteLLM:
    """
    Granite Instruct Model Wrapper
    ------------------------------
    Stable for prompt rewriting.
    """

    def __init__(self, model_name="ibm-granite/granite-3.3-2b-instruct"):

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32
        )

        self.model.eval()

    def generate(self, prompt: str, temperature=0.2, max_tokens=200):

        inputs = self.tokenizer(prompt, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True,
                top_p=0.9
            )

        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Remove the original prompt portion if echoed
        return generated_text[len(prompt):].strip()
