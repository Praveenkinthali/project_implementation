from logic_layer.intent.intent_analyzer import IntentAnalyzer

analyzer = IntentAnalyzer()

test_cases = {
    # 1️⃣ Perfect Prompt (well-specified)
    "PERFECT PROMPT": """
    Explain binary search algorithm in data structures for beginners.
    Use bullet points and include one example.
    """,

    # 2️⃣ Worst Prompt (extremely vague)
    "WORST PROMPT": """
    Explain this.
    """,

    # 3️⃣ Long Prompt (academic / assignment style)
    "LONG PROMPT": """
    Analyze the impact of artificial intelligence on modern healthcare systems.
    Discuss its applications in diagnosis, treatment planning, patient monitoring,
    and hospital management. Also mention ethical challenges and future scope.
    """,

    # 4️⃣ Real-Time User Prompt (natural human language)
    "REAL-TIME PROMPT": """
    I am preparing for my exams and I am confused about operating systems.
    Can you please explain processes and threads in a simple way so that I can
    understand the difference clearly?
    """,

    # 5️⃣ Ambiguous Prompt (missing criteria & constraints)
    "AMBIGUOUS PROMPT": """
    Compare sorting algorithms and tell which one is better.
    """,

    # 6️⃣ Half Prompt / Incomplete Thought
    "HALF PROMPT": """
    Explain advantages and disadvantages of
    """
}

# -------------------------------------------------
# Run tests
# -------------------------------------------------
for case_name, prompt in test_cases.items():
    intent = analyzer.analyze(prompt)

    print("\n" + "=" * 100)
    print(f"TEST CASE: {case_name}")
    print("-" * 100)
    print("PROMPT:")
    print(prompt.strip())

    print("\nINTENT ANALYSIS RESULT:")
    print("Task Type      :", intent["task_type"])
    print("Ambiguity      :", intent["ambiguity"])
    print("Complexity     :", intent["complexity"])
    print("Constraints    :", intent["constraints"])
    print("Style          :", intent["style"])
    print("Reasoning      :", intent["reasoning"])
    print("Risk Level     :", intent["risk"])
