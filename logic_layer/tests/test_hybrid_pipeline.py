from logic_layer.intent.intent_analyzer import IntentAnalyzer
from logic_layer.controller.policy_controller import PolicyController
from logic_layer.refiner.hybrid_prompt_refiner import HybridPromptRefiner


def run_test(prompt: str):

    print("\n" + "=" * 120)
    print("ORIGINAL PROMPT:\n")
    print(prompt.strip())

    # =====================================================
    # 1️⃣ Intent Analysis
    # =====================================================
    analyzer = IntentAnalyzer()
    intent = analyzer.analyze(prompt)

    print("\n--- INTENT SUMMARY ---")
    print("Task Type        :", intent.get("task_type"))
    print("Ambiguity        :", intent.get("ambiguity"))
    print("Complexity       :", intent.get("complexity"))
    print("Risk Level       :", intent.get("risk", {}).get("output_risk_level"))

    # =====================================================
    # 2️⃣ Policy Controller
    # =====================================================
    controller = PolicyController()

    selected = controller.select_primitives(intent)
    print("\n--- SELECTED PRIMITIVES ---")
    print(selected)

    refined_intermediate, used_primitives = controller.optimize(prompt)

    print("\n--- APPLIED PRIMITIVES ---")
    print(used_primitives)

    # =====================================================
    # 3️⃣ Hybrid Refiner
    # =====================================================
    refiner = HybridPromptRefiner()

    final_prompt = refiner.refine(
        original_prompt=prompt,
        applied_primitives=used_primitives,
        intent=intent
    )

    print("\nFINAL HYBRID REFINED PROMPT:\n")
    print(final_prompt)

    print("=" * 120)


# ==============================================================
# TEST CASES
# ==============================================================

if __name__ == "__main__":

    test_prompts = [

        # Simple prompt
        "Explain artificial intelligence.",

        # Ambiguous prompt
        "Explain this.",

        # Multi-intent complex task
        """Design a distributed microservices system.
        Compare REST and GraphQL.
        Analyze scalability trade-offs and justify architectural decisions.""",

        # Comparison task
        "Compare CNNs and Transformers for image classification.",

        # Procedure task
        "Provide step-by-step instructions to deploy a Node.js app using Docker in production.",

        # Verbose real-world student prompt
        "Can you please explain in a simple way how binary search works because I am preparing for exams and I am confused?"
    ]

    for prompt in test_prompts:
        run_test(prompt)
