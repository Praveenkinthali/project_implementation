from logic_layer.evaluation.metrics.semantic_metrics import SemanticMetrics
from pprint import pprint


def print_section(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def display_clean_metrics(result):
    print("\n🧠 SEMANTIC METRICS")
    pprint(result)


def run_test_cases():

    sm = SemanticMetrics()

    test_cases = [

        # ----------------------------------------------------------
        # 1. High Semantic Similarity (Rephrase)
        # ----------------------------------------------------------
        {
            "name": "Rephrased Prompt",
            "original_prompt": "Explain neural networks.",
            "optimized_prompt": "Describe artificial neural network models.",
            "original_response": "Neural networks are computing systems inspired by biology.",
            "optimized_response": "Artificial neural networks are computational models inspired by the human brain."
        },

        # ----------------------------------------------------------
        # 2. Low Semantic Similarity (Intent Drift)
        # ----------------------------------------------------------
        {
            "name": "Intent Drift",
            "original_prompt": "Explain neural networks.",
            "optimized_prompt": "Discuss Italian pasta recipes.",
            "original_response": "Neural networks are machine learning models.",
            "optimized_response": "Pasta recipes include carbonara and bolognese."
        },

        # ----------------------------------------------------------
        # 3. Strong Prompt-Response Alignment
        # ----------------------------------------------------------
        {
            "name": "Strong Prompt-Response Alignment",
            "original_prompt": "Explain solar panel efficiency.",
            "optimized_prompt": "Explain solar panel efficiency in detail.",
            "original_response": "Solar panel efficiency measures energy conversion.",
            "optimized_response": "Solar panel efficiency refers to how effectively sunlight is converted into electricity."
        }
    ]

    for case in test_cases:

        print_section(f"🧪 TEST CASE: {case['name']}")

        result = sm.compute(
            case["original_prompt"],
            case["optimized_prompt"],
            case["original_response"],
            case["optimized_response"]
        )

        print("\n🔹 ORIGINAL PROMPT:")
        print(case["original_prompt"])

        print("\n🔹 OPTIMIZED PROMPT:")
        print(case["optimized_prompt"])

        print("\n🔹 OPTIMIZED RESPONSE:")
        print(case["optimized_response"])

        display_clean_metrics(result)


if __name__ == "__main__":
    run_test_cases()