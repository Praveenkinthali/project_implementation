class IterativeRefiner:

    def __init__(self):
        self.abstractor = SemanticAbstraction()
        self.controller = PolicyController()

    def refine(self, prompt):

        prompt = self.abstractor.abstract(prompt)

        for i in range(3):

            refined_prompt, meta = self.controller.optimize(prompt)

            response = run_llm(refined_prompt)

            score = evaluate(response)

            if score > 0.8:
                break

            prompt = refined_prompt

        return refined_prompt