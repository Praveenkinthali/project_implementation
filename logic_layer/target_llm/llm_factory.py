from .groq_llm import GroqLLM


def get_llm(provider: str, config: dict):

    if provider == "groq":
        return GroqLLM(
            api_key=config["api_key"],
            model_name=config.get("model_name", "llama3-8b-8192")
        )

    raise ValueError(f"Unsupported provider: {provider}")