"""
TemplateSynthesizer + extract_topic (v5)
=========================================
Root cause fixes for all failing prompts:

PROBLEM 1: "Compare REST and GraphQL" → "Compare building a mobile API"
  Cause: _dep_parse_topic iterated children in order and found prep "for"
  (a CONTENT_PREP) before finishing with dobj "REST"+"GraphQL". It took
  "building a mobile API" as the best candidate (longest), discarding the
  actual subjects.
  Fix: PRIORITY ORDER — dobj/attr always wins over prep objects.
       Only fall to prep objects if no dobj/attr/ccomp found.

PROBLEM 2: "Write a Python function to implement..." → "Write implement..."
  Cause: _strip_leading_task_verb stripped "Write", leaving
  "a Python function to implement binary search on a sorted list"
  then _clean_topic_text stripped the article "a", leaving
  "Python function to implement..." — correct so far.
  But then _pattern_fallback_topic also ran and stripped "implement"
  as a TASK_VERB, leaving just "binary search on a sorted list".
  Fix: Once dep parse succeeds with a good result, do NOT run pattern
       fallback. Pattern fallback only runs when dep parse returns None.

PROBLEM 3: "How do I deploy FastAPI..." → "a FastAPI application"
  Cause: QUESTION_STRIP regex matched "How do I" and stripped it,
  leaving "deploy a FastAPI application to AWS using Docker".
  Then _strip_leading_task_verb found "deploy" as a TASK_VERB and
  stripped it, leaving "a FastAPI application to AWS using Docker".
  Then _clean_topic_text stripped the article "a", leaving
  "FastAPI application to AWS using Docker" — actually correct!
  But the gerund conversion tried to make "a" into a gerund.
  Fix: Strip article AFTER checking for task verb, and only convert
       to gerund when a verb is actually found at position 0.

PROBLEM 4: "I'm building an e-commerce startup..." → "Summarize an e-commerce startup"
  Cause: Distiller extracted "an e-commerce startup" as the content span
  from "I'm building", then intent analyzer saw short prompt → summarization.
  Fix: Distiller must preserve the FULL object subtree including conjuncts
  and "we expect heavy traffic spikes" context. The content span from
  "I'm building an e-commerce startup AND we expect..." should include
  the entire coordination.
"""

from typing import Dict, List, Optional
import re
import spacy

_nlp = spacy.load("en_core_web_sm")

TEMPLATES: Dict[str, List[str]] = {
    "explanation":    ["Explain {topic}{audience_clause}.",    "{clarify_clause}", "{scope_clause}",    "{example_clause}", "{length_clause}"],
    "definition":     ["Define {topic}{audience_clause}.",     "{clarify_clause}", "{example_clause}",  "{length_clause}"],
    "analysis":       ["Analyze {topic}{audience_clause}.",    "{clarify_clause}", "{decompose_clause}", "{reflect_clause}", "{length_clause}"],
    "comparison":     ["Compare {topic}{audience_clause}.",    "{clarify_clause}", "{format_clause}",   "{reflect_clause}", "{length_clause}"],
    "summarization":  ["Summarize {topic}{audience_clause}.",  "{clarify_clause}", "{length_clause}"],
    "code_generation":["Write {topic}.",                       "{clarify_clause}", "{format_clause}",   "{reflect_clause}"],
    "procedure":      ["Provide step-by-step instructions for {topic}{audience_clause}.", "{clarify_clause}", "{format_clause}", "{length_clause}"],
}
DEFAULT_TEMPLATE = ["{topic}.", "{clarify_clause}", "{scope_clause}", "{length_clause}"]

TASK_VERB_SET = {
    "explain", "describe", "define", "compare", "analyze", "analyse",
    "summarize", "summarise", "write", "implement", "create", "build",
    "design", "provide", "list", "discuss", "evaluate", "assess",
    "give", "show", "walk", "break", "find", "identify", "outline",
    "generate", "tell", "help", "shed", "deploy", "structure",
}

# Deps that carry the core topic — PRIORITY ORDER matters
# dobj/attr are checked FIRST, prep objects only as fallback
PRIMARY_CONTENT_DEPS  = {"dobj", "attr", "ccomp", "xcomp", "oprd"}
SECONDARY_CONTENT_DEPS = {"pcomp", "relcl", "advcl"}
CONTENT_PREPS = {"about", "on", "for", "regarding", "of", "into", "over", "through"}

QUESTION_STRIP = re.compile(
    r"^(what\s+(is|are|does|do|was|were)\s+"
    r"|how\s+(do\s+i|do\s+we|do\s+you|can\s+i|can\s+we|is|are|was|were|to)\s+"
    r"|why\s+(is|are|does|do)\s+"
    r"|when\s+(should|do|does|is)\s+"
    r"|which\s+(is|are)\s+)",
    re.IGNORECASE,
)

TRAILING_NOISE = re.compile(
    r"\s*(,\s*)?(because|since|so\s+that?|so)\s+i\s+(can|could|want|need|don't|do\s+not)\s+[^,\.]*",
    re.IGNORECASE,
)


def _subtree_text(token) -> str:
    return token.doc[
        min(t.i for t in token.subtree):
        max(t.i for t in token.subtree) + 1
    ].text.strip()


def _clean(text: str) -> str:
    """Final cleanup — strip trailing noise and normalize."""
    text = TRAILING_NOISE.sub("", text).strip()
    text = re.sub(r"\s+", " ", text).strip().rstrip("?.")
    return text


def _strip_task_verb(text: str) -> str:
    """Strip a leading task verb and article only."""
    words = text.split()
    if words and words[0].lower().rstrip(".,?!") in TASK_VERB_SET:
        text = " ".join(words[1:]).strip()
        text = re.sub(r"^(a|an|the)\s+", "", text, flags=re.IGNORECASE)
    return text


def _dep_parse_topic(prompt: str) -> Optional[str]:
    """
    Dependency parse topic extraction with correct priority:
    1. dobj/attr/ccomp/xcomp (direct objects — most reliable)
    2. advcl/relcl (clausal modifiers)
    3. prep objects via CONTENT_PREPS (only if no direct object found)

    For coordinated objects ("REST and GraphQL"), the full coordination
    subtree is returned, not just the first conjunct.
    """
    doc = _nlp(prompt)

    root = next(
        (t for t in doc if t.dep_ == "ROOT" and t.pos_ in {"VERB", "AUX"}),
        None,
    )
    if root is None:
        return None

    primary   = []   # dobj, attr, ccomp, xcomp
    secondary = []   # advcl, relcl
    prep_objs = []   # prep -> pobj (lowest priority)

    for child in root.children:
        if child.dep_ in PRIMARY_CONTENT_DEPS and child.pos_ not in {"PRON"}:
            span = _subtree_text(child)
            if span:
                primary.append(span)

        elif child.dep_ in SECONDARY_CONTENT_DEPS:
            span = _subtree_text(child)
            if span:
                secondary.append(span)

        elif child.dep_ == "prep" and child.text.lower() in CONTENT_PREPS:
            for gc in child.children:
                if gc.dep_ in {"pobj", "pcomp"}:
                    span = _subtree_text(gc)
                    if span:
                        prep_objs.append(span)

    # Use PRIMARY first — this preserves "REST and GraphQL" in "Compare REST and GraphQL for..."
    candidates = primary or secondary or prep_objs
    if not candidates:
        return None

    best = max(candidates, key=lambda x: len(x.split()))
    best = _strip_task_verb(best)
    best = _clean(best)
    return best if best else None


def _question_fallback_topic(prompt: str) -> Optional[str]:
    """
    Handle question forms: "What is X", "How do I X", "How is X stored"
    Strips question prefix, converts leading verb to gerund for procedure topics.
    """
    m = QUESTION_STRIP.match(prompt)
    if not m:
        return None

    remainder = prompt[m.end():].strip().rstrip("?.")

    # Check if remainder starts with a verb → convert to gerund
    doc = _nlp(remainder)
    first_tok = next((t for t in doc if not t.is_punct and not t.is_space), None)

    if first_tok and first_tok.pos_ == "VERB":
        lemma = first_tok.lemma_.lower()
        # Gerund rules
        if lemma.endswith("e") and not lemma.endswith("ee"):
            gerund = lemma[:-1] + "ing"
        elif (len(lemma) >= 3
              and lemma[-1] not in "aeiou"
              and lemma[-2] in "aeiou"
              and lemma[-3] not in "aeiou"):
            gerund = lemma + lemma[-1] + "ing"
        else:
            gerund = lemma + "ing"
        remainder = gerund + remainder[len(first_tok.text):]

    remainder = re.sub(r"^(a|an|the)\s+", "", remainder, flags=re.IGNORECASE)
    remainder = _clean(remainder)
    return remainder if remainder else None


def _imperative_fallback_topic(prompt: str) -> Optional[str]:
    """Strip leading task verb from imperative prompts."""
    words = prompt.split()
    if not words:
        return None
    first = words[0].lower().rstrip(".,?!")
    if first in TASK_VERB_SET:
        remainder = " ".join(words[1:]).strip()
        remainder = re.sub(r"^(a|an|the)\s+", "", remainder, flags=re.IGNORECASE)
        remainder = _clean(remainder)
        return remainder if remainder else None
    return None


def _noun_chunk_fallback(prompt: str) -> str:
    doc = _nlp(prompt)
    chunks = list(doc.noun_chunks)
    if chunks:
        return max(chunks, key=lambda c: len(c.text.split())).text.strip()
    return _clean(prompt)


def extract_topic(prompt: str) -> str:
    """
    Hybrid topic extraction — dependency parse with layered fallbacks.

    Priority:
    1. Dep parse on most content-dense sentence (primary — generalizes to any phrasing)
    2. Question form stripping (for "What is X", "How do I X")
    3. Imperative verb stripping (for "Explain X", "Summarize X")
    4. Noun chunk fallback (last resort)
    """
    prompt = re.sub(r"\s+", " ", prompt).strip()
    if not prompt:
        return prompt

    # For multi-sentence: pick most content-dense sentence
    doc = _nlp(prompt)
    sents = [s.text.strip() for s in doc.sents if s.text.strip()]
    if len(sents) > 1:
        def score(s):
            d = _nlp(s)
            n = sum(1 for t in d if t.pos_ in {"NOUN", "PROPN", "VERB"} and not t.is_stop)
            return n / max(len(list(d)), 1)
        working = max(sents, key=score)
    else:
        working = prompt

    # 1. Dependency parse (primary — works for any phrasing)
    topic = _dep_parse_topic(working)
    if topic and len(topic.strip()) >= 2:
        return topic

    # 2. Question form fallback
    topic = _question_fallback_topic(working)
    if topic and len(topic.strip()) >= 2:
        return topic

    # 3. Imperative verb fallback
    topic = _imperative_fallback_topic(working)
    if topic and len(topic.strip()) >= 2:
        return topic

    # 4. Noun chunk fallback
    return _noun_chunk_fallback(working)


class TemplateSynthesizer:

    def synthesize(self, topic: str, task_type: str, slots: Dict[str, str]) -> str:
        template = TEMPLATES.get(task_type, DEFAULT_TEMPLATE)
        audience = slots.get("audience_clause", "")
        ctx = {
            "topic": topic.strip(),
            "audience_clause": f" {audience.strip()}" if audience else "",
        }
        ctx.update(slots)
        sentences = [r for f in template if (r := self._render(f, ctx))]
        return self._join(sentences)

    def _render(self, fragment: str, ctx: Dict[str, str]) -> str:
        for slot in re.findall(r"\{(\w+)\}", fragment):
            value = ctx.get(slot, "")
            if not value and slot not in {"topic", "audience_clause"}:
                return ""
            fragment = fragment.replace("{" + slot + "}", value)
        fragment = re.sub(r"\{[^}]+\}", "", fragment).strip()
        return "" if fragment in {".", ",", ""} else fragment

    def _join(self, sentences: List[str]) -> str:
        result = []
        for s in sentences:
            s = s.strip()
            if not s:
                continue
            s = re.sub(r"([?!])\.$", r"\1", s)
            if s[-1] not in ".!?":
                s += "."
            result.append(s)
        return " ".join(result)