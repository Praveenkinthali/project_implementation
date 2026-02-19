from logic_layer.controller.rl_controller import RLController

controller = RLController()

prompts = [

    # Broad short explanation
    "Explain artificial intelligence.",

    # Multi-intent complex task
    """
    Design a distributed microservices system.
    Compare REST and GraphQL.
    Analyze scalability trade-offs.
    """,

    # Deep explanation
    "Explain transformer architectures including attention mechanisms and positional encoding.",

    # Comparison task
    "Compare CNNs and Transformers for image classification.",

    # Procedure
    "Provide step-by-step instructions to deploy a Node.js app using Docker."
]

for prompt in prompts:
    print("\n" + "=" * 120)
    print("ORIGINAL PROMPT:\n", prompt.strip())

    final_prompt, used = controller.optimize(prompt)

    print("\nPRIMITIVES USED:", used)
    print("\nFINAL PROMPT:\n", final_prompt)

