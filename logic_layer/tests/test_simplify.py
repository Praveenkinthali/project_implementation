from logic_layer.intent.intent_analyzer import IntentAnalyzer
from logic_layer.primitives.simplify import Simplify

analyzer = IntentAnalyzer()
simplify = Simplify()

prompts = [
    "Can you please explain binary search in a simple way so that I can understand?",
    "Explain binary search algorithm.",
    "I am preparing for exams and I am confused about operating systems, can you explain processes and threads?",
    "I am preparing for my exams and I am confused about data structures. Can you please explain binary search in a simple way so that I can understand it clearly?"
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
