from logic_layer.intent.intent_analyzer import IntentAnalyzer
from logic_layer.primitives.scope_align import ScopeAlign
from logic_layer.primitives.self_reflect import SelfReflect

analyzer = IntentAnalyzer()
scope = ScopeAlign()
reflect = SelfReflect()

prompts = [

    # 1️⃣ Overly broad short prompt
    "Explain artificial intelligence.",

    # 2️⃣ Broad but slightly longer
    "Discuss software engineering principles.",

    # 3️⃣ Complex multi-intent system design
    """
    Design a distributed microservices system for a global e-commerce platform.
    Compare REST and GraphQL.
    Analyze scalability trade-offs and justify your architectural decisions.
    """,

    # 4️⃣ Deep technical explanation
    """
    Explain transformer architectures including attention mechanisms,
    positional encoding, and training stability challenges.
    """,

    # 5️⃣ Simple factual definition
    "Define stack."
]

for prompt in prompts:
    print("\n" + "=" * 120)
    print("ORIGINAL:\n", prompt.strip())

    intent = analyzer.analyze(prompt)

    # Test ScopeAlign
    scoped_prompt, scope_meta = scope.apply(prompt, intent)
    print("\nSCOPE ALIGN META:", scope_meta)

    # Test SelfReflect
    reflected_prompt, reflect_meta = reflect.apply(prompt, intent)
    print("SELF REFLECT META:", reflect_meta)

    print("\nFINAL PROMPT AFTER BOTH (for visualization):")
    temp_prompt, _ = scope.apply(prompt, intent)
    final_prompt, _ = reflect.apply(temp_prompt, intent)
    print(final_prompt)
