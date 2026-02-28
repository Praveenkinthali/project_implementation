from logic_layer.evaluation.metrics.response_metrics import ResponseMetrics
from pprint import pprint


def print_section(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def display_clean_metrics(result):
    print("\n📊 LENGTH METRICS")
    pprint(result["length_metrics"])

    print("\n📐 STRUCTURE METRICS")
    pprint(result["structure_metrics"])

    print("\n🎯 RELEVANCE METRICS")
    pprint(result["relevance_metrics"])

    print("\n📝 INSTRUCTION ADHERENCE")
    pprint(result["instruction_adherence"])

    print("\n✅ COMPLETENESS METRICS")
    pprint(result["completeness_metrics"])

    print("\n⚠️ HALLUCINATION PROXIES")
    pprint(result["hallucination_proxies"])

    print("\n🧠 COHERENCE INDICATORS")
    pprint(result["coherence_indicators"])


def run_test_cases():

    rm = ResponseMetrics()

    test_cases = [

        # ----------------------------------------------------------
        # 1. Structured Improvement
        # ----------------------------------------------------------
        {
            "name": "Structured Response Improvement",
            "original_prompt": "Explain AI.",
            "optimized_prompt": "Explain AI using bullet points.",
            "original_response": "AI is computer intelligence that mimics humans.",
            "optimized_response": """AI refers to artificial intelligence.
- Definition
- Applications
- Benefits"""
        },

        # ----------------------------------------------------------
        # 2. Instruction Adherence
        # ----------------------------------------------------------
        {
            "name": "Instruction Adherence",
            "original_prompt": "Explain AI.",
            "optimized_prompt": "Explain AI and compare it with machine learning.",
            "original_response": "AI is intelligence.",
            "optimized_response": """AI is artificial intelligence.
It compares to machine learning because ML is a subset of AI."""
        },

        # ----------------------------------------------------------
        # 3. Completeness with Numbered Tasks
        # ----------------------------------------------------------
        {
            "name": "Completeness Detection",
            "original_prompt": "1. Define AI\n2. Give examples",
            "optimized_prompt": "1. Define AI\n2. Give examples",
            "original_response": "AI is intelligence.",
            "optimized_response": """1. AI is artificial intelligence.
2. Examples include robotics and NLP."""
        },

        # ----------------------------------------------------------
        # 4. Hallucination Risk
        # ----------------------------------------------------------
        {
            "name": "Hallucination Risk Case",
            "original_prompt": "Explain solar panels.",
            "optimized_prompt": "Explain solar panels.",
            "original_response": "Solar panels generate energy.",
            "optimized_response": """Solar panels definitely always produce 100% efficient energy.
They are proven to never fail."""
        },

        # ----------------------------------------------------------
        # 5. Weak Relevance
        # ----------------------------------------------------------
        {
            "name": "Low Relevance Response",
            "original_prompt": "Explain neural networks.",
            "optimized_prompt": "Explain neural networks.",
            "original_response": "Neural networks are models.",
            "optimized_response": "Italian pasta recipes are very popular in Europe."
        }
    ]

    for case in test_cases:

        print_section(f"🧪 TEST CASE: {case['name']}")

        result = rm.compute(
            case["original_prompt"],
            case["optimized_prompt"],
            case["original_response"],
            case["optimized_response"]
        )

        print("\n🔹 ORIGINAL RESPONSE:")
        print(case["original_response"])

        print("\n🔹 OPTIMIZED RESPONSE:")
        print(case["optimized_response"])

        display_clean_metrics(result)


if __name__ == "__main__":
    run_test_cases()