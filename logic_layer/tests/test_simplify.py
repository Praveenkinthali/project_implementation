from logic_layer.intent.intent_analyzer import IntentAnalyzer
from logic_layer.primitives.simplify import Simplify

analyzer = IntentAnalyzer()
simplify = Simplify()

prompts = [
    "Can you please explain binary search in a simple way so that I can understand?",
    "Explain binary search algorithm.",
    "I am preparing for exams and I am confused about operating systems, can you explain processes and threads?",
    "I am preparing for my exams and I am confused about data structures. Can you please explain binary search in a simple way so that I can understand it clearly?",
    "The proposed system is implemented using a modular three-tier architecture that separates intent understanding, prompt transformation, and orchestration logic. The logic layer begins with an intent analyzer module (logic_layer/intent/intent_analyzer.py), which encodes a raw user prompt into structured intent signals such as task type, ambiguity types (e.g., missing domain or comparison criteria), complexity, constraints, and risk level using lightweight linguistic and semantic analysis. Based on these intent signals, a controller module selects and orders a set of orthogonal prompt transformation primitives implemented under logic_layer/primitives/. Each primitive (e.g., Clarify, Decompose, Simplify) operates directly on the original prompt and produces localized, intent-preserving annotations along with structured metadata describing its effect. These primitive outputs are composable and do not alter the user’s intent. Finally, a dedicated prompt reframing component synthesizes the accumulated annotations into a clean, well-aligned prompt that is sent to the language model. This design ensures explainability, modularity, and deterministic behavior, enabling precise control over prompt refinement while maintaining alignment with the original user request."
]

for prompt in prompts:
    intent = analyzer.analyze(prompt)
    new_prompt, meta = simplify.apply(prompt, intent)

    print("\n" + "=" * 90)
    print("ORIGINAL PROMPT:")
    print(prompt)

    print("\nUPDATED PROMPT:")
    print(new_prompt)

    print("\nMETADATA:")
    print(meta)
