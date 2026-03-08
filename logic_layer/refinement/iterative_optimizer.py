from logic_layer.abstraction.semantic_abstraction import SemanticAbstraction
from logic_layer.controller.policy_controller import PolicyController
from logic_layer.evaluation.evaluator import Evaluator
from logic_layer.evaluation.adaptive_learning import AdaptiveLearningEngine
from logic_layer.evaluation.feedback_store import FeedbackStore
from logic_layer.learning.reward_engine import RewardEngine

class IterativeOptimizer:
    """
    Iterative Prompt Optimization Engine

    Features:
    - Self-refinement loop
    - Evaluation feedback
    - Primitive learning
    - Iteration awareness
    - Early stopping
    """

    def __init__(self, llm, max_iterations=3):

        self.llm = llm

        self.abstractor = SemanticAbstraction()
        self.controller = PolicyController()

        self.evaluator = Evaluator(llm=llm)

        self.learning = AdaptiveLearningEngine()
        self.feedback_store = FeedbackStore()

        self.max_iterations = max_iterations

        self.reward_engine = RewardEngine()

    # ------------------------------------------------
    # MAIN OPTIMIZATION LOOP
    # ------------------------------------------------

    def optimize(self, prompt: str):

        original_prompt = prompt

        # Step 1 — semantic abstraction
        current_prompt = self.abstractor.abstract(prompt)

        best_prompt = current_prompt
        best_score = 0

        history = []

        for iteration in range(self.max_iterations):

            print("\n==============================")
            print(f"ITERATION {iteration + 1}")
            print("==============================")

            previous_primitives = []

            if history:
                previous_primitives = history[-1]["primitives"]

            # ------------------------------------------------
            # Controller optimization
            # ------------------------------------------------

            optimized_prompt, metadata = self.controller.optimize(
                current_prompt,
                previous_primitives=previous_primitives
            )

            primitives_used = metadata.get("applied_primitives", [])

            print("Applied primitives:", primitives_used)
            print("\nOptimized prompt:\n", optimized_prompt)

            # ------------------------------------------------
            # Stop if nothing changed
            # ------------------------------------------------

            if not primitives_used:
                print("\nNo further transformations possible. Stopping.")
                break

            # ------------------------------------------------
            # Generate responses
            # ------------------------------------------------

            original_response = self._generate(original_prompt)
            optimized_response = self._generate(optimized_prompt)

            # ------------------------------------------------
            # Evaluation
            # ------------------------------------------------

            result = self.evaluator.evaluate(
                original_prompt,
                optimized_prompt,
                original_response,
                optimized_response,
                metadata
            )

            score = result["final_score"]

            print("\nEvaluation Score:", score)

            # ------------------------------------------------
            # RL Learning Signal (FIXED)
            # ------------------------------------------------

            reward = self.reward_engine.compute_reward(score)

            self.learning.record(
                primitives_used=primitives_used,
                final_score=reward
            )

            # ------------------------------------------------
            # Feedback storage placeholder
            # ------------------------------------------------

            self.feedback_store.store(
                session_id=str(iteration),
                final_score=score,
                primitives=primitives_used,
                user_rating=None,
                comment=None
            )

            # ------------------------------------------------
            # Track best prompt
            # ------------------------------------------------

            if score > best_score:
                best_score = score
                best_prompt = optimized_prompt

            history.append({
                "iteration": iteration + 1,
                "score": score,
                "primitives": primitives_used
            })

            # ------------------------------------------------
            # Stop condition from evaluator
            # ------------------------------------------------

            if not result["should_iterate"]:
                print("\nStopping optimization (quality threshold reached).")
                break

            # ------------------------------------------------
            # Minimal improvement stop
            # ------------------------------------------------

            if len(history) > 1:
                prev_score = history[-2]["score"]
                if abs(score - prev_score) < 0.01:
                    print("\nMinimal improvement detected. Stopping.")
                    break

            current_prompt = optimized_prompt

        return {
            "best_prompt": best_prompt,
            "best_score": best_score,
            "history": history
        }

    # ------------------------------------------------
    # LLM Wrapper
    # ------------------------------------------------

    def _generate(self, prompt):

        result = self.llm.generate(prompt)

        return result.get("output", "")