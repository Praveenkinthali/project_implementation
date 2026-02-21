import re
import spacy
from logic_layer.postprocessing.prompt_schema import CanonicalPrompt

nlp = spacy.load("en_core_web_sm")


class CanonicalExtractor:

    @staticmethod
    def extract(refined_prompt: str) -> CanonicalPrompt:

        lines = [line.strip() for line in refined_prompt.split("\n") if line.strip()]

        tasks = []
        constraints = []
        expectations = []

        task_pattern = re.compile(r"^task\s*\d+:", re.IGNORECASE)

        # -------------------------------------------------
        # 1️⃣ Explicit Task Lines (Highest Priority)
        # -------------------------------------------------
        for line in lines:
            if task_pattern.match(line):
                task_text = line.split(":", 1)[1].strip()
                tasks.append(task_text)

        # -------------------------------------------------
        # 2️⃣ Constraint Detection
        # -------------------------------------------------
        for line in lines:
            lower = line.lower()

            if any(
                phrase in lower
                for phrase in [
                    "limit the response",
                    "within",
                    "under",
                    "no more than",
                    "must",
                    "should",
                ]
            ):
                constraints.append(line)

        # -------------------------------------------------
        # 3️⃣ Expectation Detection
        # -------------------------------------------------
        for line in lines:
            lower = line.lower()

            if any(
                phrase in lower
                for phrase in [
                    "structure the response",
                    "use bullet",
                    "address each",
                    "include",
                ]
            ):
                expectations.append(line)

        # -------------------------------------------------
        # 4️⃣ Fallback: If No Explicit Tasks Found
        # -------------------------------------------------
        if not tasks:
            doc = nlp(refined_prompt)
            for sent in doc.sents:
                first = next((t for t in sent if not t.is_punct), None)
                if first and first.pos_ == "VERB":
                    tasks.append(sent.text.strip())

        # Final Safety Fallback
        if not tasks:
            tasks.append(refined_prompt.strip())

        return CanonicalPrompt(
            role="a knowledgeable domain expert",
            tasks=tasks,
            constraints=constraints,
            expectations=expectations,
        )
