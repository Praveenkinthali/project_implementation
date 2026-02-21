from logic_layer.refiner.single_pass_refiner import SinglePassRefiner


def print_result(original: str, refined: str):
    print("\n" + "=" * 100)
    print("ORIGINAL PROMPT")
    print("=" * 100)
    print(original.strip())

    print("\n" + "-" * 100)
    print("REFINED PROMPT")
    print("-" * 100)
    print(refined.strip())
    print("=" * 100 + "\n")


def run_tests():

    refiner = SinglePassRefiner()

    real_world_prompts = [

        # 1️⃣ Software Engineering Architecture
        """
        Design a scalable microservices architecture for an e-commerce platform.
        Discuss database selection, API gateway usage, service communication,
        deployment strategy, and monitoring considerations.
        Provide reasoning for design decisions.
        """,

        # 2️⃣ Machine Learning System Design
        """
        Build an end-to-end machine learning pipeline for predicting customer churn.
        Include data preprocessing, feature engineering, model selection,
        evaluation metrics, deployment strategy, and monitoring.
        """,

        # 3️⃣ Security Analysis
        """
        Analyze the security risks in deploying a public REST API.
        Compare authentication mechanisms such as OAuth, JWT, and API keys.
        Recommend best practices and justify your reasoning.
        """,

        # 4️⃣ DevOps / Cloud
        """
        Provide step by step instructions to deploy a Dockerized FastAPI application
        to AWS using CI/CD pipeline integration.
        Include security and scalability considerations.
        """,

        # 5️⃣ Data Engineering
        """
        Compare batch processing and stream processing architectures.
        Include real-world use cases, trade-offs, performance implications,
        and implementation examples.
        """,

        # 6️⃣ Research-Level Prompt
        """
        Evaluate the advantages and limitations of transformer-based architectures
        compared to recurrent neural networks for sequence modeling tasks.
        Include computational complexity, scalability, and practical deployment challenges.
        """

    ]

    for prompt in real_world_prompts:
        refined_prompt, _ = refiner.refine(prompt)
        print_result(prompt, refined_prompt)


if __name__ == "__main__":
    run_tests()
