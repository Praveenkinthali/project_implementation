from logic_layer.intent.intent_analyzer import IntentAnalyzer
from logic_layer.primitives.constrain_output import ConstrainOutput

analyzer = IntentAnalyzer()
primitive = ConstrainOutput()

prompts = [

    # 1️⃣ Academic explanation (long + complex)
    """Explain how operating systems manage process scheduling,
    memory management, and synchronization in multiprogramming environments.
    Discuss trade-offs and performance implications.""",

    # 2️⃣ Multi-intent research task
    """Compare supervised and unsupervised learning algorithms,
    provide mathematical intuition behind both, and suggest use cases
    where each approach is preferable.""",

    # 3️⃣ Code + explanation hybrid
    """Write a Python program that implements Dijkstra’s algorithm.
    Then explain its time complexity and provide an example graph.""",

    # 4️⃣ Research writing task
    """Write a detailed overview of transformer architectures,
    including attention mechanisms, positional encoding,
    and their applications in NLP and computer vision.""",

    # 5️⃣ Vague but large scope
    """Explain artificial intelligence and its impact on modern society."""
]

for prompt in prompts:
    intent = analyzer.analyze(prompt)
    updated, meta = primitive.apply(prompt, intent)

    print("\n" + "=" * 100)
    print("ORIGINAL:\n", prompt)
    print("\nUPDATED:\n", updated)
    print("\nMETA:\n", meta)
