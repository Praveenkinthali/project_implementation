from abc import ABC, abstractmethod
from typing import Dict, Tuple


class Primitive(ABC):
    """
    Base class for all prompt transformation primitives.
    """

    @abstractmethod
    def apply(self, prompt: str, intent: Dict) -> Tuple[str, Dict]:
        """
        Apply a transformation to the prompt.

        Returns:
            updated_prompt (str)
            metadata (dict): information about what was applied
        """
        pass
