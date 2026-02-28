import os
from logic_layer.target_llm.llm_factory import get_llm


# 🔹 Simple Enhancement Function (Mock Transform)
def enhance_prompt(original_prompt: str) -> str:
    """
    Simulates SIPP transformation layer.
    Later this will be replaced by your PTL transforms.
    """
    enhanced = (
        original_prompt
        + "\n\n"
        + "Instructions:\n"
        + "- Present the answer clearly.\n"
        + "- Use bullet points.\n"
        + "- Keep it concise.\n"
        + "- Provide structured explanation."
    )
    return enhanced


def run_test():

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

    # 🔹 Original Prompt
    original_prompt = "Explain the effects of deforestation."

    # 🔹 Generate Original Output
    original_result = llm.generate(original_prompt)

    # 🔹 Enhanced Prompt
    enhanced_prompt = enhance_prompt(original_prompt)

    # 🔹 Generate Enhanced Output
    enhanced_result = llm.generate(enhanced_prompt)

    # ===============================
    # 🔥 PRINT COMPARISON
    # ===============================

    print("\n" + "=" * 80)
    print("ORIGINAL PROMPT:\n")
    print(original_prompt)

    print("\n--- GENERATED OUTPUT (Original Prompt) ---\n")
    print(original_result["output"])
    print("\nLatency:", original_result["latency"])
    print("Tokens:", original_result["tokens_used"])

    print("\n" + "=" * 80)
    print("ENHANCED PROMPT:\n")
    print(enhanced_prompt)

    print("\n--- GENERATED OUTPUT (Enhanced Prompt) ---\n")
    print(enhanced_result["output"])
    print("\nLatency:", enhanced_result["latency"])
    print("Tokens:", enhanced_result["tokens_used"])
    print("=" * 80)


if __name__ == "__main__":
    run_test()