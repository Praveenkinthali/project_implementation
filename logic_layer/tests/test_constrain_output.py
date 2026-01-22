from logic_layer.intent.intent_analyzer import IntentAnalyzer
from logic_layer.primitives.constrain_output import ConstrainOutput

analyzer = IntentAnalyzer()
constrain = ConstrainOutput()

prompts = [
    # No constraints
    "Explain binary search algorithm.",
    
    # Already constrained
    "Explain binary search algorithm in 100 words using bullet points.",
]

for prompt in prompts:
    intent = analyzer.analyze(prompt)
    new_prompt, meta = constrain.apply(prompt, intent)

    print("\n" + "=" * 90)
    print("ORIGINAL PROMPT:")
    print(prompt)

    print("\nUPDATED PROMPT:")
    print(new_prompt)

    print("\nMETADATA:")
    print(meta)
