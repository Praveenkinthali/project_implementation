from logic_layer.intent.intent_analyzer import IntentAnalyzer
from logic_layer.controller.policy_controller import PolicyController


def run_debug_test(prompt: str):

    print("\n" + "=" * 140)
    print("ORIGINAL PROMPT:\n")
    print(prompt.strip())

    # =====================================================
    # 1️⃣ Intent Analysis
    # =====================================================
    analyzer = IntentAnalyzer()
    intent = analyzer.analyze(prompt)

    print("\n" + "-" * 60)
    print("INTENT ANALYSIS")
    print("-" * 60)

    print("Task Type     :", intent.get("task_type"))
    print("Ambiguity     :", intent.get("ambiguity"))
    print("Complexity    :", intent.get("complexity"))
    print("Constraints   :", intent.get("constraints"))
    print("Risk Level    :", intent.get("risk", {}).get("output_risk_level"))

    # =====================================================
    # 2️⃣ Controller Scoring
    # =====================================================
    controller = PolicyController()

    # ✅ FIX: pass prompt
    scores = controller.score_primitives(intent, prompt)

    print("\n" + "-" * 60)
    print("PRIMITIVE SCORES")
    print("-" * 60)

    for name, score in scores.items():
        print(f"{name:<15}: {round(score, 3)}")

    # ✅ FIX: pass prompt
    selected = controller.select_primitives(intent, prompt)

    print("\nSELECTED PRIMITIVES:")
    print(selected)

    # =====================================================
    # 3️⃣ Step-by-Step Primitive Application
    # =====================================================
    print("\n" + "-" * 60)
    print("STEP-BY-STEP PRIMITIVE APPLICATION")
    print("-" * 60)

    current_prompt = prompt

    execution_order = [
        "clarify",
        "simplify",
        "scope_align",
        "decompose",
        "add_example",
        "constrain",
        "format_enforce",
        "self_reflect",
    ]

    for name in execution_order:

        if name in selected:

            primitive = controller.primitives[name]

            print(f"\n>>> Applying Primitive: {name.upper()}")

            updated_prompt, meta = primitive.apply(current_prompt, intent)

            print("Metadata:", meta)

            if meta.get("applied", False):
                print("\nUpdated Prompt After", name, ":\n")
                print(updated_prompt)
                current_prompt = updated_prompt
            else:
                print("Primitive decided NOT to apply.")

    print("\n" + "-" * 60)
    print("FINAL PROMPT BEFORE REFINER")
    print("-" * 60)
    print(current_prompt)

    print("=" * 140)


# ==============================================================
# COMPLEX REAL-WORLD TEST CASES
# ==============================================================

if __name__ == "__main__":

    test_prompts = [

        """
        Design a scalable AI-powered e-commerce platform using microservices architecture.
        Compare REST and GraphQL APIs in terms of performance, flexibility, and maintainability.
        Discuss caching strategies, authentication mechanisms, CI/CD integration, monitoring,
        and analyze scalability trade-offs with justification.
        """,

        """
        Analyze the impact of transformer architectures on natural language processing.
        Compare them with RNNs and CNNs in terms of computational complexity,
        data efficiency, and scalability. Provide theoretical insights and real-world examples.
        """,

        """
        Provide step-by-step instructions to deploy a production-ready Node.js application
        using Docker and Kubernetes, including load balancing, monitoring,
        environment configuration, and secure secret management.
        """,

        """
        Can you please explain in detail how this works and why it is better,
        because I am confused and preparing for interviews?
        """,

        """
        Explain reinforcement learning in depth, including Markov Decision Processes,
        policy gradients, value iteration, Q-learning, and actor-critic methods.
        Compare model-based and model-free approaches, discuss convergence properties,
        and analyze computational trade-offs.
        """
    ]

    for prompt in test_prompts:
        run_debug_test(prompt)
