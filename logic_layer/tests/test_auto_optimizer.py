from logic_layer.controller.rl_controller import RLController
from logic_layer.controller.auto_optimizer import AutoOptimizer

controller = RLController()
optimizer = AutoOptimizer(controller)

prompts = [

    # Very vague prompt
    "Explain AI.",

    # Multi-intent complex prompt
    """
    Design a scalable microservices system.
    Compare REST and GraphQL.
    Justify architectural trade-offs.
    """,

    # Clean structured prompt
    "Compare CNNs and Transformers in terms of accuracy and computation cost."
]

for prompt in prompts:
    print("\n" + "=" * 120)
    print("ORIGINAL PROMPT:\n", prompt.strip())

    final_prompt, used = optimizer.refine(prompt)

    print("\nPRIMITIVES USED:", used)
    print("\nREFINED PROMPT:\n", final_prompt)
    
