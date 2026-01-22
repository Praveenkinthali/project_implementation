from logic_layer.intent.intent_analyzer import IntentAnalyzer
from logic_layer.primitives.clarify import Clarify

analyzer = IntentAnalyzer()
clarify = Clarify()

test_prompts = [
    "Explain this.",
    "Compare sorting algorithms and tell which is better.",
    "Explain binary search algorithm for beginners with an example."
]

for prompt in test_prompts:
    intent = analyzer.analyze(prompt)
    new_prompt, meta = clarify.apply(prompt, intent)

    print("\n" + "=" * 90)
    print("ORIGINAL PROMPT:")
    print(prompt)

    print("\nUPDATED PROMPT:")
    print(new_prompt)

    print("\nMETADATA:")
    print(meta)
