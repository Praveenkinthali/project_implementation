from logic_layer.intent.intent_analyzer import IntentAnalyzer
from logic_layer.primitives.decompose import Decompose

analyzer = IntentAnalyzer()
decompose = Decompose()

prompts = [
    "Explain sorting algorithms and compare them and tell which is better.",
    "Explain binary search algorithm.", 
    "Summarize the following text and provide an analysis of its implications.",
    "Define machine learning and give step by step instructions to implement a simple model.",
    "Explain advantages and disadvantages of binary search."
]

for prompt in prompts:
    intent = analyzer.analyze(prompt)
    new_prompt, meta = decompose.apply(prompt, intent)

    print("\n" + "=" * 90)
    print("ORIGINAL PROMPT:")
    print(prompt)

    print("\nUPDATED PROMPT:")
    print(new_prompt)

    print("\nMETADATA:")
    print(meta)
