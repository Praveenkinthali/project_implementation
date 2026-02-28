import time
from pprint import pprint

# Core Modules
from logic_layer.intent.intent_analyzer import IntentAnalyzer
from logic_layer.controller.policy_controller import PolicyController
from logic_layer.refiner.single_pass_refiner import SinglePassRefiner
from logic_layer.evaluation.evaluator import Evaluator


# ============================================================
# MOCK LLM (Safe for System Testing)
# ============================================================

class MockLLM:
    def generate(self, prompt: str):
        return f"""
[MOCK RESPONSE]

This is a simulated response for testing.

Prompt received:
{prompt}

- Point 1: Example explanation
- Point 2: Structured output
"""


# ============================================================
# Utility Printing
# ============================================================

def print_section(title):
    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)


def display_summary(result):
    print("\n📊 COMPONENT SCORES:")
    pprint(result["aggregation"]["component_scores"])

    print("\n🏁 FINAL COMPOSITE SCORE:")
    print(result["final_score"])

    print("\n🔁 SHOULD ITERATE?")
    print(result["should_iterate"])


# ============================================================
# FULL PIPELINE EXECUTION
# ============================================================

def run_full_pipeline():

    print_section("🚀 SRPP FULL PIPELINE TEST")

    # ---------------------------------------------------
    # 1️⃣ User Prompt
    # ---------------------------------------------------

    user_prompt = "Explain neural networks."

    print("\n🧾 ORIGINAL PROMPT:")
    print(user_prompt)

    # ---------------------------------------------------
    # 2️⃣ Intent Analysis
    # ---------------------------------------------------

    analyzer = IntentAnalyzer()
    intent = analyzer.analyze(user_prompt)

    print("\n🧠 INTENT ANALYSIS OUTPUT:")
    pprint(intent)

    # ---------------------------------------------------
    # 3️⃣ Controller (Optional if refiner handles internally)
    # ---------------------------------------------------

    controller = PolicyController()
    selected_primitives = controller.select_primitives(intent, user_prompt)

    print("\n🎯 SELECTED PRIMITIVES:")
    pprint(selected_primitives)

    # ---------------------------------------------------
    # 4️⃣ Refinement
    # ---------------------------------------------------

    refiner = SinglePassRefiner()

    refine_output = refiner.refine(user_prompt)

    # Handle both return types safely
    if isinstance(refine_output, tuple):
        optimized_prompt, refine_metadata = refine_output
    else:
        optimized_prompt = refine_output
        refine_metadata = {}

    print("\n✨ OPTIMIZED PROMPT:")
    print(optimized_prompt)

    # ---------------------------------------------------
    # 5️⃣ Mock LLM
    # ---------------------------------------------------

    llm = MockLLM()

    print("\n⏳ Generating optimized response...")
    start_time = time.time()
    optimized_response = llm.generate(optimized_prompt)
    latency = time.time() - start_time

    print("\n🤖 OPTIMIZED RESPONSE:")
    print(optimized_response)

    print(f"\n⏱ LATENCY: {latency:.4f} seconds")

    # ---------------------------------------------------
    # 6️⃣ Baseline Response (Original Prompt)
    # ---------------------------------------------------

    original_response = llm.generate(user_prompt)

    # ---------------------------------------------------
    # 7️⃣ Evaluation
    # ---------------------------------------------------

    evaluator = Evaluator(
        llm=None,                 # No LLM judge for test
        enable_semantic=True,
        enable_judge=False,
        quality_threshold=0.65
    )

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

    print_section("📊 EVALUATION RESULTS")

    display_summary(evaluation_result)

    print_section("✅ FULL PIPELINE TEST COMPLETE")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    run_full_pipeline()