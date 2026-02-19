from logic_layer.intent.intent_analyzer import IntentAnalyzer
from logic_layer.primitives.add_example import AddExample

analyzer = IntentAnalyzer()
primitive = AddExample()

prompts = [
    "Explain the concept of recursion in detail.",
    
    "Explain how blockchain works in distributed systems.",
    
    "Explain recursion with an example.",
    
    "Define stack.",
    
    "Explain how operating systems handle process scheduling and memory management."
]


for prompt in prompts:
    intent = analyzer.analyze(prompt)
    updated, meta = primitive.apply(prompt, intent)

    print("\n" + "=" * 90)
    print("ORIGINAL:", prompt)
    print("UPDATED:", updated)
    print("META:", meta)
