import os

from logic_layer.controller.policy_controller import PolicyController
from logic_layer.refiner.prompt_refiner import PromptRefiner
from logic_layer.llm.local_phi_llm import LocalPhiLLM




def run_test(prompt: str):

    print("\n" + "=" * 120)
    print("ORIGINAL PROMPT:\n", prompt.strip())

    controller = PolicyController()
    llm = LocalPhiLLM()
    refiner = PromptRefiner(llm_generate_function=llm.generate)



    # Step 1: Controller processing
    structural_prompt, meta = controller.process(prompt)

    print("\nAPPLIED PRIMITIVES:", meta["applied_primitives"])

    # Step 2: Semantic refinement
    final_prompt = refiner.refine(
        original_prompt=prompt,
        intent=meta["intent"],
        applied_primitives=meta["applied_primitives"]
    )

    print("\nFINAL REFINED PROMPT:\n")
    print(final_prompt)


if __name__ == "__main__":

    test_prompts = [

        "Explain artificial intelligence.",

        "Explain this.",

        """
        Design a distributed microservices system.
        Compare REST and GraphQL.
        Analyze scalability trade-offs.
        """,

        "Compare CNNs and Transformers for image classification.",

        "Can you please explain in a simple way how binary search works because I am preparing for exams and I am confused?"
    ]

    for prompt in test_prompts:
        run_test(prompt)
