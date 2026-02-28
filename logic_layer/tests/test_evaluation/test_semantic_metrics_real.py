import os
from pprint import pprint

from logic_layer.target_llm.llm_factory import get_llm
from logic_layer.evaluation.metrics.semantic_metrics import SemanticMetrics


def run_semantic_test():

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

    semantic_metrics = SemanticMetrics()

    prompt = "Explain solar panel efficiency."
    optimized_prompt = prompt + "\nInclude statistics."

    original_response = llm.generate(prompt)["output"]
    optimized_response = llm.generate(optimized_prompt)["output"]

    print("\n" + "=" * 100)
    print("SEMANTIC METRICS TEST")
    print("=" * 100)

    result = semantic_metrics.compute(
        prompt,
        optimized_prompt,
        original_response,
        optimized_response
    )

    pprint(result)


if __name__ == "__main__":
    run_semantic_test()