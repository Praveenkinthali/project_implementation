from typing import List, Dict


class CanonicalPrompt:
    """
    Model-agnostic canonical prompt representation.
    """

    def __init__(
        self,
        role: str,
        tasks: List[str],
        constraints: List[str],
        expectations: List[str],
    ):
        self.role = role
        self.tasks = tasks
        self.constraints = constraints
        self.expectations = expectations

    def to_dict(self) -> Dict:
        return {
            "role": self.role,
            "tasks": self.tasks,
            "constraints": self.constraints,
            "expectations": self.expectations,
        }
