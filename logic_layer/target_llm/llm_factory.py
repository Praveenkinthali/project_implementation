from .groq_llm import GroqLLM


def get_llm(provider: str, config: dict):

    if provider == "groq":
        return GroqLLM(
            api_key=config["api_key"],
            model_name=config.get(
                "model_name",
                "llama-3.1-8b-instant"   # Updated working model
            )
        )

    raise ValueError(f"Unsupported provider: {provider}")