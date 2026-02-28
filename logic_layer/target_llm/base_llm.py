from abc import ABC, abstractmethod
from typing import Dict

class BaseLLM(ABC):

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> Dict:
        """
        Must return:
        {
            "output": str,
            "latency": float,
            "tokens_used": int
        }
        """
        pass