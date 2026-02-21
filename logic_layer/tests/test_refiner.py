from logic_layer.refiner.iterative_refiner import IterativeRefiner


def print_separator():
    print("\n" + "=" * 80 + "\n")


def print_test_result(title, original, refined, used):
    print_separator()
    print(f"TEST CASE: {title}")
    print_separator()

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

    print_separator()


def run_tests():

    refiner = IterativeRefiner(max_iterations=3)

    # ============================================================
    # 1️⃣ Simple Prompt
    # ============================================================
    simple_prompt = "Explain binary search."

    refined, used = refiner.refine(simple_prompt)
    print_test_result("Simple Prompt", simple_prompt, refined, used)


    # ============================================================
    # 2️⃣ Complex Multi-Intent Prompt
    # ============================================================
    complex_prompt = """
    Compare binary search and linear search.
    Include time complexity.
    Provide Python implementation.
    Add examples.
    Keep the explanation concise but clear.
    """

    refined, used = refiner.refine(complex_prompt)
    print_test_result("Complex Multi-Intent Prompt", complex_prompt, refined, used)


    # ============================================================
    # 3️⃣ Vague Prompt
    # ============================================================
    vague_prompt = "Explain it properly."

    refined, used = refiner.refine(vague_prompt)
    print_test_result("Vague Prompt", vague_prompt, refined, used)


    # ============================================================
    # 4️⃣ Ambiguous Prompt
    # ============================================================
    ambiguous_prompt = "Explain Python performance."

    refined, used = refiner.refine(ambiguous_prompt)
    print_test_result("Ambiguous Prompt", ambiguous_prompt, refined, used)


    # ============================================================
    # 5️⃣ Incomplete Prompt
    # ============================================================
    incomplete_prompt = "Explain the difference between"

    refined, used = refiner.refine(incomplete_prompt)
    print_test_result("Incomplete Prompt", incomplete_prompt, refined, used)


    # ============================================================
    # 6️⃣ Convergence Test
    # ============================================================
    convergence_prompt = """
    Provide a detailed explanation of logistic regression.
    Include mathematical derivation.
    Add example.
    Structure properly.
    """

    refined_1, used_1 = refiner.refine(convergence_prompt)
    refined_2, used_2 = refiner.refine(refined_1)

    print_separator()
    print("TEST CASE: Convergence Behavior")
    print_separator()

    print("🔹 First Refinement Primitives:", used_1)
    print("🔹 Second Refinement Primitives:", used_2)

    print(f"First Length : {len(refined_1.split())}")
    print(f"Second Length: {len(refined_2.split())}")
    print(f"Delta        : {len(refined_2.split()) - len(refined_1.split())}")

    print_separator()


if __name__ == "__main__":
    run_tests()
