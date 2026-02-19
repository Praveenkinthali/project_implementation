import re
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration


class HybridPromptRefiner:
    """
    Hybrid Semantic + Deterministic Prompt Refiner
    ---------------------------------------------
    1. Uses T5-small for controlled rewrite
    2. Injects primitive constraints deterministically
    3. Produces single continuous refined instruction
    """

    def __init__(self):

        '''self.tokenizer = T5Tokenizer.from_pretrained("t5-small")
        self.model = T5ForConditionalGeneration.from_pretrained("t5-small")'''
        self.tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
        self.model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

        self.model.eval()

    # ---------------------------------------------------
    # Step 1 — Controlled Rewrite
    # ---------------------------------------------------
    def semantic_rewrite(self, prompt: str) -> str:

        instruction = (
            "Rewrite the following task into a clear, professional instruction. "
            "Keep the same meaning. Do not repeat the instruction template.\n\n"
            f"{prompt}"
        )

        inputs = self.tokenizer(
            instruction,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=120,
                temperature=0.3,
                do_sample=False
            )

        rewritten = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        return rewritten.strip()

    # ---------------------------------------------------
    # Step 2 — Constraint Injection
    # ---------------------------------------------------
    def inject_constraints(self, base_prompt, applied_primitives, intent):

        additions = []

        task_type = intent.get("task_type", "")

        if "add_example" in applied_primitives:
            additions.append("Include one clear illustrative example.")

        if "decompose" in applied_primitives:
            additions.append("Address each component of the request separately.")

        if "constrain" in applied_primitives:

            if task_type == "comparison":
                additions.append(
                    "Present the comparison concisely (200–300 words) in a structured format."
                )
            elif task_type == "procedure":
                additions.append(
                    "Provide concise step-by-step instructions (150–200 words)."
                )
            else:
                additions.append(
                    "Keep the explanation concise (150–250 words) and well structured."
                )

        if "format_enforce" in applied_primitives:
            additions.append("Use a clearly structured format where appropriate.")

        if "self_reflect" in applied_primitives:
            additions.append(
                "Ensure logical consistency and clearly state key assumptions."
            )

        if additions:
            base_prompt = base_prompt.rstrip(".")
            base_prompt += ". " + " ".join(additions)

        return base_prompt.strip()

    # ---------------------------------------------------
    # Step 3 — Full Refinement Pipeline
    # ---------------------------------------------------
    def refine(self, original_prompt, applied_primitives, intent):

        rewritten = self.semantic_rewrite(original_prompt)

        final_prompt = self.inject_constraints(
            rewritten,
            applied_primitives,
            intent
        )

        return final_prompt
