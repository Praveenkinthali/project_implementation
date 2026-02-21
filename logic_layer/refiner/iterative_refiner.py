from typing import Tuple, List
from logic_layer.controller.policy_controller import PolicyController


class IterativeRefiner:

    def __init__(self, max_iterations: int = 3):
        self.controller = PolicyController()
        self.max_iterations = max_iterations

    def get_prompt_signature(self, prompt: str) -> dict:
        return {
            "length": len(prompt.split()),
            "sections": prompt.count("\n\n"),
            "bullets": prompt.count("- "),
            "constraints": prompt.lower().count("must"),
            "examples": prompt.lower().count("example"),
        }

    def signature_delta(self, sig1: dict, sig2: dict) -> float:
        return sum(abs(sig1[k] - sig2[k]) for k in sig1)

    def refine(self, prompt: str) -> Tuple[str, List[str]]:

        current_prompt = prompt
        applied_history = set()
        last_signature = self.get_prompt_signature(prompt)
        total_used = []

        for _ in range(self.max_iterations):

            optimized_prompt, used_primitives = self.controller.optimize(current_prompt)

            # Remove primitives already used
            used_primitives = [
                p for p in used_primitives if p not in applied_history
            ]

            if not used_primitives:
                break

            applied_history.update(used_primitives)
            total_used.extend(used_primitives)

            new_signature = self.get_prompt_signature(optimized_prompt)

            delta = self.signature_delta(last_signature, new_signature)

            if delta < 3:  # convergence threshold
                break

            current_prompt = optimized_prompt
            last_signature = new_signature

        return current_prompt, total_used
