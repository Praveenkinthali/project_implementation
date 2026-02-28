from logic_layer.evaluation.metrics.prompt_metrics import PromptMetrics
from pprint import pprint


def print_section(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def display_clean_metrics(result):
    print("\n📊 LENGTH METRICS")
    pprint(result["length_metrics"])

    print("\n📐 STRUCTURAL METRICS")
    pprint(result["structural_metrics"])

    print("\n📝 INSTRUCTION METRICS")
    pprint(result["instruction_metrics"])

    print("\n🔒 CONSTRAINT METRICS")
    pprint(result["constraint_metrics"])

    print("\n📦 FORMATTING METRICS")
    pprint(result["formatting_metrics"])

    print("\n🎯 SPECIFICITY METRICS")
    pprint(result["specificity_metrics"])

    print("\n⚠️ OVER-MODIFICATION RISK")
    pprint(result["over_modification_risk"])


def run_test_cases():

    pm = PromptMetrics()

    test_cases = [

        # ----------------------------------------------------------
        # 1. Basic Expansion
        # ----------------------------------------------------------
        {
            "name": "Basic Expansion",
            "original": "Explain AI.",
            "optimized": "Explain artificial intelligence in detail with real-world examples."
        },

        # ----------------------------------------------------------
        # 2. Format Enforcement
        # ----------------------------------------------------------
        {
            "name": "Bullet Format Enforcement",
            "original": "Explain AI.",
            "optimized": "Explain AI using bullet points.\n- Definition\n- Applications\n- Benefits"
        },

        # ----------------------------------------------------------
        # 3. Constraint Injection
        # ----------------------------------------------------------
        {
            "name": "Constraint Added",
            "original": "Write about climate change.",
            "optimized": "Write about climate change. You must limit the response to 150 words and include 2 examples."
        },

        # ----------------------------------------------------------
        # 4. Instruction Density Increase
        # ----------------------------------------------------------
        {
            "name": "Multiple Instructions",
            "original": "AI.",
            "optimized": "Explain AI, compare it with machine learning, and summarize key differences."
        },

        # ----------------------------------------------------------
        # 5. Over Modification Risk
        # ----------------------------------------------------------
        {
            "name": "Intent Drift",
            "original": "Explain neural networks.",
            "optimized": "Discuss Italian pasta recipes in detail."
        }
    ]

    for case in test_cases:

        print_section(f"🧪 TEST CASE: {case['name']}")

        result = pm.compute(case["original"], case["optimized"])

        print("\n🔹 ORIGINAL PROMPT:")
        print(case["original"])

        print("\n🔹 OPTIMIZED PROMPT:")
        print(case["optimized"])

        display_clean_metrics(result)


if __name__ == "__main__":
    run_test_cases()