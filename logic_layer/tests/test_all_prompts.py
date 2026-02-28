"""
Extended Generalization Test Suite
====================================
Tests prompts OUTSIDE the original 12 — unusual phrasings, edge cases,
and real-world variants that expose fragile pattern-matching.
"""

import re
from logic_layer.refiner.single_pass_refiner import SinglePassRefiner

SEP  = "=" * 80
SEP2 = "-" * 80

TEST_PROMPTS = [
    # ── Original 12 ──────────────────────────────────────────────────
    {"label": "01. Simple / Short",             "prompt": "Explain recursion."},
    {"label": "02. Vague single word",           "prompt": "machine learning"},
    {"label": "03. Long narrative",              "prompt": "I'm building an e-commerce startup and we expect heavy traffic spikes during big sale events. I'm confused about how to structure backend services, databases, and deployments because I don't want downtime and I need something scalable and fault tolerant."},
    {"label": "04. Technical analysis",          "prompt": "Design a scalable microservices architecture for a real-time chat application."},
    {"label": "05. Comparison",                  "prompt": "Compare REST and GraphQL for building a mobile API."},
    {"label": "06. Code generation",             "prompt": "Write a Python function to implement binary search on a sorted list."},
    {"label": "07. Procedure",                   "prompt": "How do I deploy a FastAPI application to AWS using Docker?"},
    {"label": "08. Multi-intent",                "prompt": "Explain how transformers work in NLP. Then compare BERT and GPT architectures. Also write Python code to load a pretrained BERT model using HuggingFace."},
    {"label": "09. Definition",                  "prompt": "What is eventual consistency in distributed systems?"},
    {"label": "10. Verbose / filler-heavy",      "prompt": "Could you please kindly explain to me basically what gradient descent actually is in machine learning? I would really like to understand it so that I can use it in my projects."},
    {"label": "11. Ambiguous pronoun",           "prompt": "Explain how it works."},
    {"label": "12. Summarization",               "prompt": "Summarize the key differences between SQL and NoSQL databases for a software engineering interview."},

    # ── Unusual phrasings (should NOT break) ─────────────────────────
    {"label": "13. Walk me through",             "prompt": "Walk me through how neural networks learn."},
    {"label": "14. Give me an overview",         "prompt": "Give me an overview of Kubernetes architecture."},
    {"label": "15. Break down",                  "prompt": "Break down the concept of attention mechanisms in transformers."},
    {"label": "16. Help me understand",          "prompt": "Help me understand how garbage collection works in Java."},
    {"label": "17. Can you shed light on",       "prompt": "Can you shed light on the CAP theorem?"},
    {"label": "18. I want to know",              "prompt": "I want to know how OAuth 2.0 authentication works."},
    {"label": "19. Tell me about",               "prompt": "Tell me about the differences between TCP and UDP."},
    {"label": "20. I need to understand",        "prompt": "I need to understand how to design a RESTful API."},

    # ── Edge cases ───────────────────────────────────────────────────
    {"label": "21. All caps",                    "prompt": "EXPLAIN HOW DOCKER CONTAINERS WORK."},
    {"label": "22. No verb (noun phrase only)",  "prompt": "binary search trees"},
    {"label": "23. Very long technical",         "prompt": "I am trying to figure out the best way to implement a distributed caching layer using Redis for a high-traffic web application that needs to handle 100k requests per second with sub-10ms latency."},
    {"label": "24. Passive question",            "prompt": "How is data stored in a PostgreSQL database?"},
    {"label": "25. Informal / conversational",   "prompt": "yo what even is a blockchain lol"},
    {"label": "26. Academic style",              "prompt": "Provide a comprehensive analysis of the trade-offs between consistency and availability in distributed database systems."},
    {"label": "27. Nested question",             "prompt": "Can you explain what happens when I type a URL into a browser and press enter?"},
    {"label": "28. Implicit code request",       "prompt": "Show me how to implement a rate limiter in Python."},
    {"label": "29. Comparison no 'compare'",     "prompt": "What are the differences between monolithic and microservices architecture?"},
    {"label": "30. Procedure no 'how to'",       "prompt": "Steps to set up a CI/CD pipeline using GitHub Actions."},
]


def run_all(show_trace: bool = False):

    refiner = SinglePassRefiner(use_distiller=True)
    passed = failed = 0

    print(f"\n{SEP}")
    print("  SIPP — GENERALIZATION TEST SUITE (30 prompts)")
    print(SEP)

    for test in TEST_PROMPTS:
        label  = test["label"]
        prompt = test["prompt"]

        print(f"\n{SEP2}")
        print(f"  {label}")
        print(SEP2)
        print(f"  IN  : {prompt.strip()[:120]}")

        try:
            final_prompt, trace = refiner.refine(prompt)

            print(f"  DIST: {trace['stage_1_distilled'][:100]}")
            print(f"  TOPIC: {trace['stage_2_topic'][:80]}")
            print(f"  TYPE : {trace['stage_3_task_type']}  |  APPLIED: {trace['applied_primitives']}")
            print(f"  OUT : {final_prompt}")

            if show_trace:
                print(f"  SCORES: { {k:round(v,2) for k,v in trace['utility_scores'].items()} }")

            issues = []
            if not final_prompt or len(final_prompt.strip()) < 10:
                issues.append("output too short")
            if "Optimized" in final_prompt:
                issues.append("LLM artifact leaked")
            if "[clarify:" in final_prompt:
                issues.append("raw clarify tag leaked")
            if "Task 1:" in final_prompt:
                issues.append("raw Task label leaked")
            if re.search(r"\bI'?m\b|\bI am\b|\bI need\b|\bI want\b", final_prompt):
                issues.append("first-person not stripped")
            if "How do I" in final_prompt or "how do i" in final_prompt.lower():
                issues.append("question form leaked into output")
            if "What is" in final_prompt and "?" in final_prompt:
                issues.append("question form leaked into output")
            topic = trace['stage_2_topic']
            if len(topic.split()) > 25:
                issues.append(f"topic too long ({len(topic.split())} words) — probably not cleaned")

            if issues:
                print(f"  ⚠  ISSUES: {', '.join(issues)}")
                failed += 1
            else:
                print(f"  ✓  PASS")
                passed += 1

        except Exception as e:
            import traceback
            print(f"  ✗  ERROR: {e}")
            traceback.print_exc()
            failed += 1

    print(f"\n{SEP}")
    print(f"  RESULTS: {passed} passed  |  {failed} failed  |  {len(TEST_PROMPTS)} total")
    print(SEP + "\n")


if __name__ == "__main__":
    run_all(show_trace=False)