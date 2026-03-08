import os

from logic_layer.refinement.iterative_optimizer import IterativeOptimizer
from logic_layer.target_llm.llm_factory import get_llm


api_key = os.getenv("GROQ_API_KEY")

llm = get_llm(
    provider="groq",
    config={
        "api_key": api_key,
        "model_name": "llama-3.1-8b-instant"
    }
)

optimizer = IterativeOptimizer(llm)

prompt = "Explain neural networks"

result = optimizer.optimize(prompt)

print("\n==============================")
print("FINAL RESULT")
print("==============================")

print("\nBest Prompt:\n", result["best_prompt"])
print("\nBest Score:", result["best_score"])

print("\nIteration History:")
for step in result["history"]:
    print(step)

from logic_layer.evaluation.adaptive_learning import AdaptiveLearningEngine

engine = AdaptiveLearningEngine()

print("\nPrimitive Ranking:")
print(engine.get_ranked_primitives())