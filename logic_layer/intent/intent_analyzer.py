"""
Intent Analyzer & Encoder (FINAL FIXED VERSION)
==============================================
Encodes a raw user prompt into a structured intent representation.

Key properties:
- Domain-agnostic
- Deterministic
- No training / datasets
- Robust to real user prompts
- Correctly distinguishes vague vs concrete prompts
"""

from typing import Dict
import spacy
from sentence_transformers import SentenceTransformer, util


# -------------------------------------------------
# Global models (loaded once)
# -------------------------------------------------
nlp = spacy.load("en_core_web_sm")
embedder = SentenceTransformer("all-MiniLM-L6-v2")


class IntentAnalyzer:
    """
    Robust intent analyzer using linguistic + semantic signals.
    """

    def __init__(self):
        # Canonical task intent prototypes
        self.task_prototypes = {
            "explanation": "provide a detailed conceptual explanation of a topic",
            "definition": "give a precise definition of a concept",
            "analysis": "analyze a system or theory and discuss reasoning and implications",
            "comparison": "compare multiple concepts and highlight similarities and differences",
            "summarization": "summarize provided content concisely",
            "code_generation": "write executable source code for a program or algorithm",
            "procedure": "provide ordered step by step instructions to complete a task",
        }


        # Precompute prototype embeddings
        self.prototype_embeddings = {
            task: embedder.encode(desc, convert_to_tensor=True)
            for task, desc in self.task_prototypes.items()
        }

    # -------------------------------------------------
    # Helper: detect concrete technical topic
    # -------------------------------------------------
    def _has_concrete_topic(self, doc) -> bool:
        """
        Returns True if the prompt contains a concrete technical topic
        (e.g., 'binary search algorithm', 'sorting algorithms').
        """
        for chunk in doc.noun_chunks:
            # Multi-word noun phrases usually indicate a topic
            if len(chunk.text.split()) >= 2:
                return True
        return False

    # -------------------------------------------------
    # Hybrid task detection (Rule + Semantic)
    # -------------------------------------------------
    def _detect_task_type(self, prompt: str, prompt_embedding):

        lower_prompt = prompt.lower().strip()

        # -----------------------------
        # 1️⃣ Strong Rule-Based Overrides
        # -----------------------------

        # Code generation signals
        if any(keyword in lower_prompt for keyword in [
            "write code",
            "python program",
            "implement in python",
            "write a function",
            "provide code",
            "algorithm implementation"
        ]):
            return "code_generation", {"rule_based": 1.0}

        # Comparison
        if lower_prompt.startswith("compare"):
            return "comparison", {"rule_based": 1.0}

        # Procedure
        if "step by step" in lower_prompt or lower_prompt.startswith("provide step"):
            return "procedure", {"rule_based": 1.0}

        # Definition
        if lower_prompt.startswith("define"):
            return "definition", {"rule_based": 1.0}

        # Explanation
        if lower_prompt.startswith(("explain", "describe", "how")):
            return "explanation", {"rule_based": 1.0}

        # Design / Build → Analysis (NEW FIX)
        if lower_prompt.startswith(("design", "build")):
            return "analysis", {"rule_based": 1.0}

        # -----------------------------
        # 2️⃣ Semantic Fallback
        # -----------------------------
        scores = {
            task: util.cos_sim(prompt_embedding, proto_emb).item()
            for task, proto_emb in self.prototype_embeddings.items()
        }

        best_task = max(scores, key=scores.get)
        return best_task, scores

    # -------------------------------------------------
    # Main analysis function
    # -------------------------------------------------
    def analyze(self, prompt: str) -> Dict:
        doc = nlp(prompt)
        prompt_embedding = embedder.encode(prompt, convert_to_tensor=True)

        # ---------- Task Type ----------
        task_type, semantic_scores = self._detect_task_type(prompt, prompt_embedding)

        # ---------- Ambiguity Detection ----------
        vague_pronouns = any(
            tok.pos_ in {"PRON", "DET"} and tok.text.lower() in {"this", "that", "it"}
            for tok in doc
        )

        has_named_entity = len(doc.ents) > 0
        has_concrete_topic = self._has_concrete_topic(doc)

        has_specific_object = any(
            tok.dep_ in {"dobj", "pobj", "attr"} for tok in doc
        )

        ambiguity = {
            "vague_pronouns": vague_pronouns,
            "missing_domain": not (has_named_entity or has_concrete_topic),
            "underspecified_object": not has_specific_object
        }

        # ---------- Complexity ----------
        verb_count = sum(1 for tok in doc if tok.pos_ == "VERB")
        clause_count = sum(1 for tok in doc if tok.dep_ in {"conj", "advcl", "ccomp"})

        multi_intent = (verb_count + clause_count) >= 3

        complexity = {
            "verb_count": verb_count,
            "clause_count": clause_count,
            "multi_intent": multi_intent
        }

        # ---------- Constraints ----------
        constraints = {
            "has_example": any(tok.lemma_ == "example" for tok in doc),
            "has_format": any(tok.lemma_ in {"step", "format", "bullet", "structure"} for tok in doc),
            "has_limit": any(tok.lemma_ in {"limit", "maximum", "minimum", "words", "tokens"} for tok in doc)
        }

        # ---------- Style (Derived) ----------
        token_count = len(doc)
        verbosity_score = round(token_count / max(1, verb_count), 2)

        style = {
            "verbosity_score": verbosity_score,
            "is_verbose": verbosity_score > 6.0
        }

        # ---------- Reasoning ----------
        reasoning = {
            "requires_reasoning": task_type in {"analysis", "comparison", "explanation"} or multi_intent
        }

        # ---------- Risk Assessment ----------
        if ambiguity["missing_domain"] and multi_intent:
            risk_level = "high"
        elif ambiguity["missing_domain"]:
            risk_level = "medium"
        else:
            risk_level = "low"

        risk = {
            "output_risk_level": risk_level
        }

        # ---------- Linguistic Features ----------
        linguistic = {
            "tokens": [tok.text for tok in doc],
            "pos_tags": [(tok.text, tok.pos_) for tok in doc],
            "entities": [(ent.text, ent.label_) for ent in doc.ents]
        }

        # ---------- Final Intent Representation ----------
        return {
            "task_type": task_type,
            "ambiguity": ambiguity,
            "complexity": complexity,
            "constraints": constraints,
            "style": style,
            "reasoning": reasoning,
            "risk": risk,
            "semantic_scores": semantic_scores,
            "linguistic": linguistic
        }
