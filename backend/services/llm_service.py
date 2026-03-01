from core.config import get_settings
from logic_layer.target_llm.llm_factory import get_llm


class LLMService:
    """
    Centralized LLM manager.
    Responsible only for model initialization and generation.
    """

    def __init__(self):
        settings = get_settings()

        self.llm = get_llm(
            provider="groq",
            config={
                "api_key": settings.groq_api_key,
                "model_name": "llama-3.1-8b-instant"
            }
        )

    def generate(self, prompt: str):
        return self.llm.generate(prompt)