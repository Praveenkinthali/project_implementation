from logic_layer.refiner.single_pass_refiner import SinglePassRefiner
from logic_layer.controller.policy_controller import PolicyController


def separator():
    print("\n" + "=" * 80 + "\n")


def print_result(title, original, refined, used):
    separator()
    print(f"TEST CASE: {title}")
    separator()

    print("🔹 Original Prompt:")
    print(original.strip())

    print("\n🔹 Refined Prompt:")
    print(refined.strip())

    print("\n🔹 Primitives Applied:")
    print(used)

    print("\n🔹 Stats:")
    print(f"Original Length: {len(original.split())} words")
    print(f"Refined Length : {len(refined.split())} words")
    print(f"Change         : {len(refined.split()) - len(original.split())} words")

    separator()


def run_tests():

    refiner = SinglePassRefiner()
    controller = PolicyController()

    # ============================================================
    # 1️⃣ Simple Explanation
    # ============================================================
    simple_prompt = "Explain binary search."
    refined, used = refiner.refine(simple_prompt)
    print_result("Simple Explanation", simple_prompt, refined, used)

    # ============================================================
    # 2️⃣ Vague Prompt
    # ============================================================
    vague_prompt = "Explain it properly."
    refined, used = refiner.refine(vague_prompt)
    print_result("Vague Prompt", vague_prompt, refined, used)

    # ============================================================
    # 3️⃣ Ambiguous Prompt
    # ============================================================
    ambiguous_prompt = "Explain Python performance."
    refined, used = refiner.refine(ambiguous_prompt)
    print_result("Ambiguous Prompt", ambiguous_prompt, refined, used)

    # ============================================================
    # 4️⃣ Complex Multi-Intent
    # ============================================================
    complex_prompt = """
    Compare binary search and linear search.
    Include time complexity.
    Provide Python implementation.
    Add examples.
    """
    refined, used = refiner.refine(complex_prompt)
    print_result("Complex Multi-Intent", complex_prompt, refined, used)

    # ============================================================
    # 5️⃣ Analysis Task
    # ============================================================
    analysis_prompt = "Analyze the advantages and limitations of logistic regression."
    refined, used = refiner.refine(analysis_prompt)
    print_result("Analysis Prompt", analysis_prompt, refined, used)

    # ============================================================
    # 6️⃣ Code Generation
    # ============================================================
    code_prompt = "Write a Python program to implement binary search."
    refined, used = refiner.refine(code_prompt)
    print_result("Code Generation", code_prompt, refined, used)

    # ============================================================
    # 7️⃣ Procedural Task
    # ============================================================
    procedure_prompt = "Provide step by step instructions to install Docker."
    refined, used = refiner.refine(procedure_prompt)
    print_result("Procedure Prompt", procedure_prompt, refined, used)

    # ============================================================
    # 8️⃣ Stability Check (Run Twice)
    # ============================================================
    stability_prompt = "Explain gradient descent."
    refined1, used1 = refiner.refine(stability_prompt)
    refined2, used2 = refiner.refine(refined1)

    separator()
    print("STABILITY CHECK")
    separator()

    print("First Pass Primitives :", used1)
    print("Second Pass Primitives:", used2)

    print(f"First Length  : {len(refined1.split())}")
    print(f"Second Length : {len(refined2.split())}")
    print(f"Delta         : {len(refined2.split()) - len(refined1.split())}")

    separator()

    # ============================================================
    # 9️⃣ Controller Utility Debug (Optional)
    # ============================================================
    debug_prompt = "Explain neural networks."
    intent = controller.analyzer.analyze(debug_prompt)
    utility_scores = controller.score_primitives(intent, debug_prompt)

    separator()
    print("UTILITY SCORES DEBUG")
    separator()
    print("Prompt:", debug_prompt)
    print("\nUtility Scores:")
    for k, v in utility_scores.items():
        print(f"{k:15s} → {round(v, 3)}")

    separator()


if __name__ == "__main__":
    run_tests()
