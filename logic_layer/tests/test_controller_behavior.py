from logic_layer.controller.rl_controller import RLController

controller = RLController()

prompts = [
    "Define stack.",
    "Explain recursion in detail.",
    "Compare quicksort and mergesort.",
    "Explain binary search and compare it with linear search.",
]

for prompt in prompts:
    final_prompt, used = controller.optimize(prompt)

    print("\n" + "=" * 100)
    print("ORIGINAL:", prompt)
    print("USED PRIMITIVES:", used)
    print("FINAL PROMPT:\n", final_prompt)
