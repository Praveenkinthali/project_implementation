import os
from pprint import pprint

from logic_layer.target_llm.llm_factory import get_llm
from logic_layer.evaluation.metrics.prompt_metrics import PromptMetrics


def run_prompt_metrics_test():

    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        raise ValueError("GROQ_API_KEY not set.")

    llm = get_llm(
        provider="groq",
        config={
            "api_key": groq_key,
            "model_name": "llama-3.1-8b-instant"
        }
    )

    prompt_metrics = PromptMetrics()

    original_prompt = "Explain the effects of deforestation."
    optimized_prompt = (
        original_prompt +
        "\n\nUse bullet points and provide 2 real-world examples."
    )

    print("\n" + "=" * 100)
    print("PROMPT METRICS TEST")
    print("=" * 100)

    result = prompt_metrics.compute(original_prompt, optimized_prompt)

    pprint(result)


if __name__ == "__main__":
    run_prompt_metrics_test()