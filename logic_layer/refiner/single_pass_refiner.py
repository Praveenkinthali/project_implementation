from logic_layer.abstraction.semantic_abstraction import SemanticAbstraction
from logic_layer.controller.policy_controller import PolicyController


class SinglePassRefiner:

    def __init__(self):
        self.abstractor = SemanticAbstraction()
        self.controller = PolicyController()

    def refine(self, prompt: str):
        abstracted = self.abstractor.abstract(prompt)
        return self.controller.optimize(abstracted)

