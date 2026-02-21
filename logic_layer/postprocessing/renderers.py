from logic_layer.postprocessing.prompt_schema import CanonicalPrompt


class PromptRenderer:
    """
    Render canonical prompt according to selected model type.
    """

    @staticmethod
    def render(prompt: CanonicalPrompt, model_type: str = "gpt") -> str:

        model_type = model_type.lower()

        if model_type in {"gpt", "gpt4", "openai"}:
            return PromptRenderer._render_gpt(prompt)

        elif model_type in {"llama", "llama-instruct"}:
            return PromptRenderer._render_llama(prompt)

        elif model_type in {"t5", "flan"}:
            return PromptRenderer._render_flan(prompt)

        elif model_type in {"json"}:
            return PromptRenderer._render_json(prompt)

        else:
            # fallback
            return PromptRenderer._render_gpt(prompt)

    # -------------------------------------------------
    # GPT / General Template (Default)
    # -------------------------------------------------
    @staticmethod
    def _render_gpt(prompt: CanonicalPrompt) -> str:

        output = []

        output.append(f"You are {prompt.role}.\n")

        output.append("Your task:")
        for i, task in enumerate(prompt.tasks, 1):
            output.append(f"{i}. {task}")

        if prompt.constraints:
            output.append("\nConstraints:")
            for c in prompt.constraints:
                output.append(f"- {c}")

        if prompt.expectations:
            output.append("\nExpectations:")
            for e in prompt.expectations:
                output.append(f"- {e}")

        return "\n".join(output)

    # -------------------------------------------------
    # Llama Instruct Template
    # -------------------------------------------------
    @staticmethod
    def _render_llama(prompt: CanonicalPrompt) -> str:

        body = []

        body.append("You are " + prompt.role + ".")
        body.append("Complete the following tasks:")

        for task in prompt.tasks:
            body.append(f"- {task}")

        if prompt.constraints:
            body.append("\nConstraints:")
            for c in prompt.constraints:
                body.append(f"- {c}")

        return f"[INST]\n{chr(10).join(body)}\n[/INST]"

    # -------------------------------------------------
    # FLAN / T5 Template (Minimal)
    # -------------------------------------------------
    @staticmethod
    def _render_flan(prompt: CanonicalPrompt) -> str:

        parts = []

        for task in prompt.tasks:
            parts.append(task)

        for c in prompt.constraints:
            parts.append(c)

        return " ".join(parts)

    # -------------------------------------------------
    # JSON Structured Template
    # -------------------------------------------------
    @staticmethod
    def _render_json(prompt: CanonicalPrompt) -> str:

        import json

        return json.dumps(prompt.to_dict(), indent=2)
