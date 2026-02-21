import re
import spacy
import torch
from dataclasses import dataclass
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer, util

nlp = spacy.load("en_core_web_sm")


@dataclass
class PromptState:
    token_count: int
    sentence_count: int
    narrative_ratio: float
    imperative_score: float
    ambiguity_score: float
    information_density: float
    multi_intent_score: float
    constraint_presence: bool
    domain_specificity_score: float


class SemanticAbstraction:
    """
    Adaptive Semantic Abstraction Engine
    ------------------------------------
    - Semantic profiling
    - Mode-based optimization
    - Deterministic + LLM hybrid
    """

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
        self.sim_model = SentenceTransformer("all-MiniLM-L6-v2")

    # -------------------------------------------------
    # Prompt State Computation
    # -------------------------------------------------
    def _compute_prompt_state(self, prompt: str) -> PromptState:
        doc = nlp(prompt)
        tokens = [t for t in doc if not t.is_space]

        token_count = len(tokens)
        sentence_count = len(list(doc.sents))

        # Narrative ratio
        first_person = {"i", "we", "my", "our", "me", "us"}
        narrative_tokens = sum(1 for t in tokens if t.text.lower() in first_person)
        narrative_ratio = narrative_tokens / token_count if token_count else 0

        # Imperative score
        imperative_sentences = 0
        for sent in doc.sents:
            first = next((t for t in sent if not t.is_punct), None)
            if first and first.pos_ == "VERB" and first.tag_ == "VB":
                imperative_sentences += 1

        imperative_score = (
            imperative_sentences / sentence_count if sentence_count else 0
        )

        # Ambiguity score
        vague_terms = {
            "improve", "better", "help", "explain",
            "optimize", "system", "thing", "stuff"
        }
        vague_count = sum(1 for t in tokens if t.lemma_.lower() in vague_terms)
        ambiguity_score = vague_count / token_count if token_count else 0

        # Information density
        content_tokens = sum(
            1 for t in tokens if t.pos_ in {"NOUN", "VERB", "PROPN"}
        )
        information_density = content_tokens / token_count if token_count else 0

        # Multi-intent
        root_verbs = sum(1 for t in doc if t.dep_ == "ROOT" and t.pos_ == "VERB")
        conjunctions = sum(1 for t in tokens if t.dep_ == "cc")
        multi_intent_score = (root_verbs + conjunctions) / 5

        # Constraint presence
        constraint_markers = {"limit", "within", "under", "must", "should"}
        constraint_presence = any(
            t.lemma_.lower() in constraint_markers for t in tokens
        )

        # Domain specificity
        noun_chunks = list(doc.noun_chunks)
        long_chunks = sum(1 for chunk in noun_chunks if len(chunk) >= 2)
        domain_specificity_score = (
            long_chunks / len(noun_chunks) if noun_chunks else 0
        )

        return PromptState(
            token_count,
            sentence_count,
            narrative_ratio,
            imperative_score,
            ambiguity_score,
            information_density,
            multi_intent_score,
            constraint_presence,
            domain_specificity_score,
        )

    # -------------------------------------------------
    # LLM Rewrite
    # -------------------------------------------------
    def _rewrite(self, instruction: str) -> str:
        inputs = self.tokenizer(
            instruction,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=150,
            do_sample=False
        )

        result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return result.strip()

    # -------------------------------------------------
    # Semantic Guard
    # -------------------------------------------------
    def _semantic_guard(self, original: str, rewritten: str) -> bool:
        emb1 = self.sim_model.encode(original, convert_to_tensor=True)
        emb2 = self.sim_model.encode(rewritten, convert_to_tensor=True)
        similarity = util.cos_sim(emb1, emb2).item()
        return similarity >= 0.75  # stronger guard

    # -------------------------------------------------
    # Compression Mode
    # -------------------------------------------------
    def _compression_mode(self, prompt: str) -> str:
        doc = nlp(prompt)

        # Extract noun phrases
        noun_phrases = [chunk.text for chunk in doc.noun_chunks]

        # Extract root verbs
        root_verbs = [t for t in doc if t.dep_ == "ROOT" and t.pos_ == "VERB"]

        # Detect confusion/help framing
        confusion_patterns = ["confused", "help", "understand", "trying"]

        contains_confusion = any(word in prompt.lower() for word in confusion_patterns)

        # Remove first-person tokens
        cleaned_tokens = [
            t.text for t in doc
            if t.text.lower() not in {"i", "we", "my", "our", "me", "us"}
        ]
        cleaned_text = " ".join(cleaned_tokens)

        # If confusion detected → construct imperative objective
        if contains_confusion and noun_phrases:
            # Choose longest noun phrase as likely technical target
            target = max(noun_phrases, key=lambda x: len(x.split()))

            return f"Design and explain the architecture for {target}."

        # If multiple root verbs → multi-intent, preserve but clean
        if len(root_verbs) > 1:
            sentences = [sent.text.strip() for sent in doc.sents]
            return "\n".join(sentences)

        # Fallback: cleaned declarative → imperative
        if noun_phrases:
            target = noun_phrases[-1]
            return f"Explain and design {target}."

        return cleaned_text


    # -------------------------------------------------
    # Clarification Mode
    # -------------------------------------------------
    def _clarification_mode(self, prompt: str) -> str:
        doc = nlp(prompt)
        noun_phrases = [chunk.text for chunk in doc.noun_chunks]

        if noun_phrases:
            topic = noun_phrases[-1]
            return (
                f"Provide a comprehensive explanation of {topic}. "
                "Cover core concepts, architecture, practical considerations, "
                "and real-world examples. Structure the response clearly."
            )

        return prompt


    # -------------------------------------------------
    # Public API
    # -------------------------------------------------
    def abstract(self, prompt: str) -> str:

        prompt = re.sub(r"\s+", " ", prompt).strip()
        state = self._compute_prompt_state(prompt)

        # -------------------------------------------------
        # 1️⃣ Narrative Compression Mode
        # Trigger only if BOTH narrative + non-imperative
        # -------------------------------------------------
        if state.narrative_ratio > 0.15 and state.imperative_score < 0.3:
            compressed = self._compression_mode(prompt)

            # Only accept if meaningful change
            if compressed and compressed.strip() != prompt.strip():
                return compressed

        # -------------------------------------------------
        # 2️⃣ Clarification Mode (Short + Vague)
        # -------------------------------------------------
        if (
            state.token_count <= 8
            and state.ambiguity_score > 0.03
            and state.domain_specificity_score < 0.5
        ):
            clarified = self._clarification_mode(prompt)

            if clarified and clarified.strip() != prompt.strip():
                return clarified

        # -------------------------------------------------
        # 3️⃣ Multi-Intent Normalization
        # -------------------------------------------------
        if state.multi_intent_score > 0.6 and state.imperative_score < 0.5:
            doc = nlp(prompt)
            sentences = [sent.text.strip() for sent in doc.sents]
            if len(sentences) > 1:
                return "\n".join(sentences)

        # -------------------------------------------------
        # 4️⃣ Otherwise Leave As-Is
        # -------------------------------------------------
        return prompt

