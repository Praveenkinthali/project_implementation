import os
from pprint import pprint

# Core modules
from logic_layer.intent.intent_analyzer import IntentAnalyzer
from logic_layer.controller.policy_controller import PolicyController
from logic_layer.refiner.single_pass_refiner import SinglePassRefiner
from logic_layer.target_llm.llm_factory import get_llm
from logic_layer.evaluation.evaluator import Evaluator


def run_real_evaluation():

    groq_key = os.getenv("GROQ_API_KEY")

    if not groq_key:
        raise ValueError("GROQ_API_KEY not set.")

    llm = get_llm(
        provider="groq",
        config={
            "api_key": groq_key,
            "model_name": "llama-3.1-8b-instant"
        }
    )

    evaluator = Evaluator(
        llm=None,
        enable_semantic=True,
        enable_judge=False,
        quality_threshold=0.65
    )

    # ===============================================
    # USER PROMPT
    # ===============================================

    user_prompt = "Explain the effects of deforestation."

    print("\n" + "=" * 100)
    print("ORIGINAL PROMPT:\n")
    print(user_prompt)

    # ===============================================
    # INTENT + CONTROLLER + REFINEMENT
    # ===============================================

    analyzer = IntentAnalyzer()
    intent = analyzer.analyze(user_prompt)

    controller = PolicyController()
    selected_primitives = controller.select_primitives(intent, user_prompt)

    refiner = SinglePassRefiner()
    refine_output = refiner.refine(user_prompt)

    if isinstance(refine_output, tuple):
        optimized_prompt, refine_metadata = refine_output
    else:
        optimized_prompt = refine_output
        refine_metadata = {}

    print("\n" + "=" * 100)
    print("OPTIMIZED PROMPT:\n")
    print(optimized_prompt)

    # ===============================================
    # ORIGINAL RESPONSE
    # ===============================================

    print("\nGenerating ORIGINAL response...\n")
    original_result = llm.generate(user_prompt)

    original_response = original_result["output"]
    original_latency = original_result["latency"]
    original_tokens = original_result["tokens_used"]

    print("\n--- GENERATED OUTPUT (Original Prompt) ---\n")
    print(original_response)
    print("\nLatency:", original_latency)
    print("Tokens:", original_tokens)

    # ===============================================
    # OPTIMIZED RESPONSE
    # ===============================================

    print("\nGenerating OPTIMIZED response...\n")
    optimized_result = llm.generate(optimized_prompt)

    optimized_response = optimized_result["output"]
    optimized_latency = optimized_result["latency"]
    optimized_tokens = optimized_result["tokens_used"]

    print("\n--- GENERATED OUTPUT (Optimized Prompt) ---\n")
    print(optimized_response)
    print("\nLatency:", optimized_latency)
    print("Tokens:", optimized_tokens)

    # ===============================================
    # EVALUATION
    # ===============================================

    evaluation_result = evaluator.evaluate(
        original_prompt=user_prompt,
        optimized_prompt=optimized_prompt,
        original_response=original_response,
        optimized_response=optimized_response,
        metadata={
            "primitives_used": selected_primitives,
            **refine_metadata
        }
    )

    print("\n" + "=" * 100)
    print("EVALUATION RESULTS")
    print("=" * 100)

    pprint(evaluation_result["aggregation"]["component_scores"])

    print("\nFINAL SCORE:", evaluation_result["final_score"])
    print("SHOULD ITERATE:", evaluation_result["should_iterate"])

    print("\n" + "=" * 100)
    print("IMPROVEMENT SUMMARY")
    print("=" * 100)

    print("Original Tokens:", original_tokens)
    print("Optimized Tokens:", optimized_tokens)

    print("Original Latency:", original_latency)
    print("Optimized Latency:", optimized_latency)


if __name__ == "__main__":
    run_real_evaluation()