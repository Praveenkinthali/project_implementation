from logic_layer.abstraction.semantic_abstraction import SemanticAbstraction
from logic_layer.controller.policy_controller import PolicyController
from logic_layer.evaluation.evaluator import Evaluator
from logic_layer.evaluation.adaptive_learning import AdaptiveLearningEngine
from logic_layer.evaluation.feedback_store import FeedbackStore
from logic_layer.learning.reward_engine import RewardEngine


class IterativeOptimizer:
    """
    Iterative Prompt Optimization Engine
    """

    def __init__(self, llm=None, max_iterations=3):

        self.llm = llm

        self.abstractor = SemanticAbstraction()
        self.controller = PolicyController()

        self.evaluator = Evaluator(llm=llm)

        self.learning = AdaptiveLearningEngine()
        self.feedback_store = FeedbackStore()

        self.reward_engine = RewardEngine()

        self.max_iterations = max_iterations

    # ------------------------------------------------
    # MAIN OPTIMIZATION LOOP
    # ------------------------------------------------

    def optimize(self, prompt: str):

        original_prompt = prompt

        current_prompt = self.abstractor.abstract(prompt)

        best_prompt = current_prompt
        best_score = 0

        history = []

        # Generate original response once (performance improvement)
        original_response = self._generate(original_prompt)

        for iteration in range(self.max_iterations):

            print("\n==============================")
            print(f"ITERATION {iteration + 1}")
            print("==============================")

            previous_primitives = []

            if history:
                previous_primitives = history[-1]["primitives"]

            # -----------------------------------------
            # Controller Optimization
            # -----------------------------------------

            optimized_prompt, metadata = self.controller.optimize(
                current_prompt,
                previous_primitives=previous_primitives
            )

            primitives_used = metadata.get("applied_primitives", [])

            # Prevent repeating same primitive
            primitives_used = [
                p for p in primitives_used if p not in previous_primitives
            ]

            print("Applied primitives:", primitives_used)
            print("\nOptimized prompt:\n", optimized_prompt)

            # -----------------------------------------
            # Stop if nothing changed
            # -----------------------------------------

            if not primitives_used:
                print("\nNo new primitives available. Stopping optimization.")
                break

            # -----------------------------------------
            # Generate optimized response
            # -----------------------------------------

            optimized_response = self._generate(optimized_prompt)

            # -----------------------------------------
            # Evaluation
            # -----------------------------------------

            result = self.evaluator.evaluate(
                original_prompt,
                optimized_prompt,
                original_response,
                optimized_response,
                metadata
            )

            score = result["final_score"]

            print("\nEvaluation Score:", score)

            # -----------------------------------------
            # Learning signal
            # -----------------------------------------

            reward = self.reward_engine.compute_reward(score)

            # FIXED: correct parameters
            if primitives_used:
                self.learning.record(
                    primitives_used,
                    score
                )
            else:
                print("No primitives used — skipping learning record")

            # -----------------------------------------
            # Feedback Store
            # -----------------------------------------

            self.feedback_store.store(
                session_id=str(iteration),
                final_score=score,
                primitives=primitives_used,
                user_rating=None,
                comment=None
            )

            # -----------------------------------------
            # Track best prompt
            # -----------------------------------------

            if score > best_score:
                best_score = score
                best_prompt = optimized_prompt

            history.append({
                "iteration": iteration + 1,
                "score": score,
                "primitives": primitives_used
            })

            # -----------------------------------------
            # Stop if evaluator says stop
            # -----------------------------------------

            if not result.get("should_iterate", True):
                print("\nStopping optimization (quality threshold reached).")
                break

            # -----------------------------------------
            # Stop if improvement too small
            # -----------------------------------------

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

        if not self.llm:
            return ""

        result = self.llm.generate(prompt)

        return result.get("output", "")