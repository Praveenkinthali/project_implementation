from logic_layer.intent.intent_analyzer import IntentAnalyzer
from logic_layer.primitives.format_enforce import FormatEnforce

analyzer = IntentAnalyzer()
primitive = FormatEnforce()

prompts = [

    # 1️⃣ Full-stack project design
    """
    Design a scalable microservices architecture for an e-commerce platform.
    Compare REST and GraphQL APIs in terms of performance and flexibility.
    Provide deployment considerations.
    """,

    # 2️⃣ ML project + implementation
    """
    Build a machine learning pipeline for spam email detection.
    Include preprocessing steps, model selection, evaluation metrics,
    and provide Python implementation.
    """,

    # 3️⃣ OS system-level explanation
    """
    Explain how operating systems implement virtual memory,
    paging, and segmentation. Provide mathematical reasoning
    and performance trade-offs.
    """,

    # 4️⃣ Research-style transformer architecture task
    """
    Compare CNNs, RNNs, and Transformers for sequence modeling.
    Provide theoretical justification and real-world applications.
    """,

    # 5️⃣ Software engineering procedure
    """
    Provide step-by-step instructions to deploy a Node.js application
    using Docker and Kubernetes in a production environment.
    """
]

for prompt in prompts:
    intent = analyzer.analyze(prompt)
    updated, meta = primitive.apply(prompt, intent)

    print("\n" + "=" * 120)
    print("ORIGINAL:\n", prompt.strip())
    print("\nTASK TYPE:", intent["task_type"])
    print("\nUPDATED:\n", updated)
    print("\nMETA:\n", meta)
