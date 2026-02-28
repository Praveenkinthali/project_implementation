import os
from pprint import pprint

from logic_layer.target_llm.llm_factory import get_llm
from logic_layer.evaluation.llm_judge import LLMJudge


def run_llm_judge_test():

    groq_key = os.getenv("GROQ_API_KEY")

    if not groq_key:
        raise ValueError("GROQ_API_KEY not set.")

    judge_llm = get_llm(
        provider="groq",
        config={
            "api_key": groq_key,
            "model_name": "llama-3.1-8b-instant"
        }
    )

    judge = LLMJudge(judge_llm)

    prompt = "Explain the effects of deforestation."

    response = """
Deforestation leads to biodiversity loss,
climate change acceleration,
soil erosion, and disruption of water cycles.
"""

    print("\n" + "=" * 100)
    print("LLM JUDGE TEST")
    print("=" * 100)

    print("\nPROMPT:\n")
    print(prompt)

    print("\nRESPONSE:\n")
    print(response)

    result = judge.evaluate(prompt, response)

    print("\nJUDGE SCORES:\n")
    pprint(result)

    print("\nOverall Quality Score:", result["overall_quality"])


if __name__ == "__main__":
    run_llm_judge_test()