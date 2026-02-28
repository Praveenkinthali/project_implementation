import os
from pprint import pprint

from logic_layer.target_llm.llm_factory import get_llm
from logic_layer.evaluation.metrics.response_metrics import ResponseMetrics


def run_response_metrics_test():

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

    response_metrics = ResponseMetrics()

    original_prompt = "Explain climate change."
    optimized_prompt = original_prompt + "\nUse bullet points and structured format."

    original_response = llm.generate(original_prompt)["output"]
    optimized_response = llm.generate(optimized_prompt)["output"]

    print("\n" + "=" * 100)
    print("RESPONSE METRICS TEST")
    print("=" * 100)

    result = response_metrics.compute(
        original_prompt,
        optimized_prompt,
        original_response,
        optimized_response
    )

    pprint(result)


if __name__ == "__main__":
    run_response_metrics_test()