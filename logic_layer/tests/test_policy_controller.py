from logic_layer.controller.policy_controller import PolicyController


def run_test(prompt: str):
    controller = PolicyController()

    print("\n" + "=" * 120)
    print("ORIGINAL PROMPT:\n", prompt.strip())

    refined_prompt, meta = controller.process(prompt)

    print("\n--- SCORES ---")
    for k, v in meta["scores"].items():
        print(f"{k:15s}: {round(v, 3)}")

    print("\nSELECTED PRIMITIVES:", meta["selected_primitives"])
    print("APPLIED PRIMITIVES :", meta["applied_primitives"])

    print("\nREFINED PROMPT:\n")
    print(refined_prompt)


if __name__ == "__main__":

    test_prompts = [

        # 1️⃣ Short explanation
        "Explain artificial intelligence.",

        # 2️⃣ Multi-intent system design
        """
        Design a distributed microservices system.
        Compare REST and GraphQL.
        Analyze scalability trade-offs.
        """,

        # 3️⃣ Deep technical explanation
        "Explain transformer architectures including attention mechanisms and positional encoding.",

        # 4️⃣ Comparison
        "Compare CNNs and Transformers for image classification.",

        # 5️⃣ Procedure
        "Provide step-by-step instructions to deploy a Node.js app using Docker.",

        # 6️⃣ Ambiguous prompt
        "Explain this.",

        # 7️⃣ Verbose user-style prompt
        "Can you please explain in a simple way how binary search works because I am preparing for exams and I am confused?"
    ]

    for prompt in test_prompts:
        run_test(prompt)
