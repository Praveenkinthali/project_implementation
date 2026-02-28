import os
from pprint import pprint

from logic_layer.target_llm.llm_factory import get_llm
from logic_layer.evaluation.metrics.hallucination_metrics import HallucinationMetrics


def run_hallucination_test():

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

    hallucination_metrics = HallucinationMetrics()

    prompt = "Explain solar panel efficiency."

    print("\n" + "=" * 100)
    print("HALLUCINATION METRICS TEST")
    print("=" * 100)

    # Generate response
    result = llm.generate(prompt)
    response = result["output"]

    print("\nMODEL RESPONSE:\n")
    print(response)

    # Compute hallucination risk
    metrics = hallucination_metrics.compute(response)

    print("\nHALLUCINATION METRICS OUTPUT:\n")
    pprint(metrics)


if __name__ == "__main__":
    run_hallucination_test()