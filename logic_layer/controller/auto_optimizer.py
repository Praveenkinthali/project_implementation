class AutoOptimizer:
    """
    Internal Automatic Refinement Loop (Stable Version)
    ---------------------------------------------------
    Prevents repeated primitive re-application and score inflation.
    """

    def __init__(self, controller, threshold=0.75, max_iterations=3):
        self.controller = controller
        self.threshold = threshold
        self.max_iterations = max_iterations

    # -------------------------------------------------
    # Structural Quality Score
    # -------------------------------------------------
    def compute_score(self, intent):
        ambiguity = intent.get("ambiguity", {})
        complexity = intent.get("complexity", {})
        risk = intent.get("risk", {})
        style = intent.get("style", {})

        score = 0.0

        # No ambiguity
        if not any(ambiguity.values()):
            score += 0.3

        # Not multi-intent
        if not complexity.get("multi_intent", False):
            score += 0.2

        # Low risk
        if risk.get("output_risk_level") == "low":
            score += 0.2

        # Not verbose
        if not style.get("is_verbose", False):
            score += 0.15

        return round(score, 3)

    # -------------------------------------------------
    # Iterative Refinement (Safe)
    # -------------------------------------------------
    def refine(self, prompt):

        current_prompt = prompt
        all_used_primitives = []
        previous_score = 0.0

        for iteration in range(self.max_iterations):

            intent = self.controller.analyzer.analyze(current_prompt)
            score = self.compute_score(intent)

            print(f"[Iteration {iteration+1}] Score: {score}")

            # Stop if good enough
            if score >= self.threshold:
                return current_prompt, all_used_primitives

            # Stop if score not improving
            if score <= previous_score:
                return current_prompt, all_used_primitives

            previous_score = score

            refined_prompt, used = self.controller.optimize(current_prompt)

            # Stop if no new primitives applied
            if not used:
                return current_prompt, all_used_primitives

            # Prevent re-application of same primitives
            new_used = [p for p in used if p not in all_used_primitives]

            if not new_used:
                return current_prompt, all_used_primitives

            all_used_primitives.extend(new_used)
            current_prompt = refined_prompt

        return current_prompt, all_used_primitives
