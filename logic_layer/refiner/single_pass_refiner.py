from logic_layer.abstraction.semantic_abstraction import SemanticAbstraction
from logic_layer.controller.policy_controller import PolicyController
from logic_layer.refinement.iterative_optimizer import IterativeOptimizer


class SinglePassRefiner:

    def __init__(self, llm=None, use_iterative=True, max_iterations=3):

        self.abstractor = SemanticAbstraction()
        self.controller = PolicyController()

        self.use_iterative = use_iterative

        if self.use_iterative:
            self.iterative_optimizer = IterativeOptimizer(
                llm=llm,
                max_iterations=max_iterations
            )

    def refine(self, prompt: str):

        # -------------------------------
        # Iterative Optimization Path
        # -------------------------------
        if self.use_iterative:

            result = self.iterative_optimizer.optimize(prompt)

            optimized_prompt = result["best_prompt"]

            metadata = {
                "score": result["best_score"],
                "history": result["history"],
                "method": "iterative"
            }

            return optimized_prompt, metadata

        # -------------------------------
        # Original Single Pass
        # -------------------------------
        abstracted = self.abstractor.abstract(prompt)

        optimized_prompt, metadata = self.controller.optimize(abstracted)

        return optimized_prompt, metadata