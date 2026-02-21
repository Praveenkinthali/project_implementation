from logic_layer.refiner.single_pass_refiner import SinglePassRefiner


def print_result(original: str, refined: str):
    print("\n" + "=" * 100)
    print("ORIGINAL INPUT")
    print("=" * 100)
    print(original.strip())

    print("\n" + "-" * 100)
    print("FINAL OPTIMIZED PROMPT")
    print("-" * 100)
    print(refined.strip())
    print("=" * 100 + "\n")


def run_tests():

    refiner = SinglePassRefiner()

    real_world_story_prompts = [

        # 1️⃣ Startup Story Scenario
        """
        I’m building an e-commerce startup and we expect heavy traffic spikes
        during big sale events. I’m confused about how to structure backend
        services, databases, and deployments because I don’t want downtime
        and I need something scalable and fault tolerant.
        """,

        # 2️⃣ ML Research Scenario
        """
        I’m working on a machine learning research project and I’m trying to
        understand whether transformers are really better than recurrent neural
        networks for sequence modeling. I care about scalability, computational
        cost, and deployment challenges.
        """,

        # 3️⃣ Security Concern Story
        """
        I have built a REST API and now I’m worried about security because
        it will be exposed publicly. I want to understand authentication options,
        possible vulnerabilities, and best practices to prevent attacks.
        """,

        # 4️⃣ DevOps Confusion
        """
        I deployed my application using Docker locally but now I need to move it
        to AWS with proper CI/CD integration and I’m not sure how to structure
        the deployment pipeline or handle scalability and security.
        """,

        # 5️⃣ Data Engineering Narrative
        """
        We currently process data in batches but real-time analytics is becoming
        important for our product. I’m trying to decide whether to switch to
        stream processing and I want to understand trade-offs, performance,
        and practical implementation differences.
        """
    ]

    for prompt in real_world_story_prompts:
        refined_prompt, _ = refiner.refine(prompt)
        print_result(prompt, refined_prompt)


if __name__ == "__main__":
    run_tests()
