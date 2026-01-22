"""
Intent Analyzer (FINAL FIXED VERSION)
------------------------------------
Detects task intent, ambiguity, complexity, constraints, and risk
from a raw user prompt.

Key fixes:
- Detects concrete technical topics (not only named entities)
- Detects missing comparison criteria for comparison tasks
"""

from typing import Dict
import spacy
from sentence_transformers import SentenceTransformer, util

# Load models once
nlp = spacy.load("en_core_web_sm")
embedder = SentenceTransformer("all-MiniLM-L6-v2")


class IntentAnalyzer:
    def __init__(self):
        self.task_prototypes = {
            "explanation": "explain a concept clearly",
            "definition": "define a concept",
            "analysis": "analyze a topic and discuss implications",
            "comparison": "compare two concepts and decide which is better",
            "summarization": "summarize the given text",
            "code_generation": "write a program or function",
            "procedure": "give step by step instructions",
        }

        self.prototype_embeddings = {
            task: embedder.encode(desc, convert_to_tensor=True)
            for task, desc in self.task_prototypes.items()
        }

    # ---------- helper ----------
    def _has_concrete_topic(self, doc) -> bool:
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) >= 2:
                return True
        return False

    # ---------- semantic task ----------
    def _detect_task_type(self, embedding):
        scores = {
            task: util.cos_sim(embedding, proto).item()
            for task, proto in self.prototype_embeddings.items()
        }
        return max(scores, key=scores.get), scores

    # ---------- main ----------
    def analyze(self, prompt: str) -> Dict:
        doc = nlp(prompt)
        embedding = embedder.encode(prompt, convert_to_tensor=True)

        # Task
        task_type, semantic_scores = self._detect_task_type(embedding)

        # Ambiguity: pronouns
        vague_pronouns = any(
            tok.text.lower() in {"this", "that", "it"} and tok.pos_ in {"PRON", "DET"}
            for tok in doc
        )

        # Ambiguity: domain
        has_named_entity = len(doc.ents) > 0
        has_concrete_topic = self._has_concrete_topic(doc)

        # Ambiguity: object
        has_specific_object = any(
            tok.dep_ in {"dobj", "pobj", "attr"} for tok in doc
        )

        # 🔴 NEW: missing comparison criteria
        missing_comparison_criteria = (
            task_type == "comparison"
            and not any(
                tok.lemma_ in {
                    "time", "space", "complexity", "performance",
                    "efficiency", "speed", "memory", "cost",
                    "use", "case", "application"
                }
                for tok in doc
            )
        )

        ambiguity = {
            "vague_pronouns": vague_pronouns,
            "missing_domain": not (has_named_entity or has_concrete_topic),
            "underspecified_object": not has_specific_object,
            "missing_comparison_criteria": missing_comparison_criteria
        }

        # Complexity
        verb_count = sum(1 for tok in doc if tok.pos_ == "VERB")
        clause_count = sum(1 for tok in doc if tok.dep_ in {"conj", "advcl", "ccomp"})
        multi_intent = (verb_count + clause_count) >= 3

        complexity = {
            "verb_count": verb_count,
            "clause_count": clause_count,
            "multi_intent": multi_intent
        }

        # Constraints
        constraints = {
            "has_example": any(tok.lemma_ == "example" for tok in doc),
            "has_format": any(tok.lemma_ in {"step", "format", "bullet"} for tok in doc),
            "has_limit": any(tok.lemma_ in {"limit", "words", "tokens"} for tok in doc),
        }

        # Style
        verbosity_score = round(len(doc) / max(1, verb_count), 2)
        style = {
            "verbosity_score": verbosity_score,
            "is_verbose": verbosity_score > 6.0
        }

        # Reasoning
        reasoning = {
            "requires_reasoning": task_type in {"analysis", "comparison"} or multi_intent
        }

        # Risk
        if missing_comparison_criteria or ambiguity["missing_domain"]:
            risk_level = "medium"
        else:
            risk_level = "low"

        risk = {"output_risk_level": risk_level}

        return {
            "task_type": task_type,
            "ambiguity": ambiguity,
            "complexity": complexity,
            "constraints": constraints,
            "style": style,
            "reasoning": reasoning,
            "risk": risk,
            "semantic_scores": semantic_scores,
        }
