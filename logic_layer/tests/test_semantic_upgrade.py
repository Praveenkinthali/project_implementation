"""
Test Script for Upgraded SIPP Framework
----------------------------------------
Tests:
- Narrative compression
- Short ambiguous clarification
- Multi-intent handling
- Already strong prompt preservation
"""

from logic_layer.refiner.single_pass_refiner import SinglePassRefiner
from logic_layer.postprocessing.canonical_extractor import CanonicalExtractor

# -------------------------------------------------
# Test Prompts
# -------------------------------------------------

TEST_PROMPTS = {
    "narrative_long": """
    I'm building an e-commerce startup and we expect heavy traffic spikes
    during seasonal sales. I'm confused about how to structure the backend
    system and database scaling because downtime would be disastrous.
    Can you help me understand what architecture choices I should make?
    """,

    "short_ambiguous": "Explain databases",

    "multi_intent": "Explain REST APIs and compare them with GraphQL in terms of performance and scalability",

    "already_good": "Design a scalable microservices architecture for an e-commerce platform. Include database strategy and deployment considerations."
}

# -------------------------------------------------
# Test Runner
# -------------------------------------------------

def run_test(prompt_name, prompt_text):
    print("=" * 80)
    print(f"TEST CASE: {prompt_name}")
    print("=" * 80)

    print("\n🔹 ORIGINAL PROMPT:")
    print(prompt_text.strip())

    refiner = SinglePassRefiner()

    optimized_prompt, used_primitives = refiner.refine(prompt_text)

    print("\n🔹 OPTIMIZED PROMPT:")
    print(optimized_prompt)

    print("\n🔹 PRIMITIVES USED:")
    print(used_primitives)

    extractor = CanonicalExtractor()
    canonical = extractor.extract(optimized_prompt)

    print("\n🔹 CANONICAL STRUCTURE:")
    print("Role:", canonical.role)
    print("Tasks:", canonical.tasks)
    print("Constraints:", canonical.constraints)
    print("Expectations:", canonical.expectations)

    print("\n\n")


# -------------------------------------------------
# Execute All Tests
# -------------------------------------------------

if __name__ == "__main__":
    for name, prompt in TEST_PROMPTS.items():
        run_test(name, prompt)
