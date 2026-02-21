from logic_layer.refiner.single_pass_refiner import SinglePassRefiner
from logic_layer.postprocessing.prompt_schema import CanonicalPrompt
from logic_layer.postprocessing.renderers import PromptRenderer
import re


def extract_to_canonical(refined_prompt: str) -> CanonicalPrompt:
    """
    Robust parser to convert refined text into CanonicalPrompt object.
    """

    lines = [line.strip() for line in refined_prompt.split("\n") if line.strip()]

    tasks = []
    constraints = []
    expectations = []

    task_pattern = re.compile(r"^task\s*\d+:", re.IGNORECASE)

    for line in lines:

        # Explicit Task lines only
        if task_pattern.match(line):
            task_text = line.split(":", 1)[1].strip()
            tasks.append(task_text)

        # Strict constraint rules
        elif line.lower().startswith(("limit", "keep")):
            constraints.append(line)

        elif line.lower().startswith("structure the response"):
            constraints.append(line)

        # Expectations
        elif "address each" in line.lower():
            expectations.append(line)

    # If no explicit Task N lines found
    if not tasks:
        main_content = []

        for line in lines:
            lower = line.lower()

            if not (
                lower.startswith(("limit", "keep"))
                or lower.startswith("structure the response")
                or "address each" in lower
            ):
                main_content.append(line)

        if main_content:
            tasks.append(" ".join(main_content))

    return CanonicalPrompt(
        role="a knowledgeable domain expert",
        tasks=tasks,
        constraints=constraints,
        expectations=expectations,
    )


def run_test(model_type="gpt"):

    refiner = SinglePassRefiner()

    test_prompt = """
    I’m building an e-commerce startup and we expect heavy traffic spikes
    during big sale events. I’m confused about how to structure backend
    services, databases, and deployments because I don’t want downtime
    and I need something scalable and fault tolerant.
    """

    refined_prompt, _ = refiner.refine(test_prompt)

    canonical = extract_to_canonical(refined_prompt)

    rendered_prompt = PromptRenderer.render(canonical, model_type=model_type)

    print("\n" + "=" * 100)
    print("ORIGINAL PROMPT")
    print("=" * 100)
    print(test_prompt.strip())

    print("\n" + "=" * 100)
    print("FINAL MODIFIED PROMPT")
    print("=" * 100)
    print(refined_prompt.strip())

    print("\n" + "=" * 100)
    print(f"PROMPT RENDERED FOR MODEL: {model_type.upper()}")
    print("=" * 100)
    print(rendered_prompt)

    print("\n" + "=" * 100 + "\n")


if __name__ == "__main__":
    run_test(model_type="json")



