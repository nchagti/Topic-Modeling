"""Read the saved LatinCy DocBins and re-derive the processed tokens from them.

The DocBins (data/original/corpus/latin_tragedies_corpus.spacy: play level, earlier
la_core_web_lg build; data/original/acts/latin_tragedies_acts.spacy: act level, 3.8.0) keep
each token's text, lemma and POS, so no model is needed to read them.
"""
from __future__ import annotations

import json

import spacy
from spacy.tokens import DocBin

import pipeline as P

PLAY_DOCBIN = P.ORIGINAL / "corpus" / "latin_tragedies_corpus.spacy"
ACT_DOCBIN = P.ORIGINAL / "acts" / "latin_tragedies_acts.spacy"
KEEP_POS = {"PROPN", "NOUN", "VERB", "ADJ"}
CUSTOM_LOOKUPS = {"inquit": "inquam", "ablatus": "aufero"}


def load_stopwords() -> set[str]:
    """Same flattening as the preprocessing notebooks."""
    sw = json.loads(P.STOPWORDS_JSON.read_text(encoding="utf-8"))
    out = set()
    for items in sw.values():
        if isinstance(items, list):
            out.update(w.lower() for w in items)
        elif isinstance(items, dict):
            for lemma, forms in items.items():
                out.add(lemma.lower())
                out.update(w.lower() for w in forms)
    return out


def load_docbin(level: str = "play"):
    nlp = spacy.blank("la")
    path = PLAY_DOCBIN if level == "play" else ACT_DOCBIN
    return list(DocBin().from_disk(path).get_docs(nlp.vocab))


def kept_tokens(doc, stopwords):
    """(surface, lemma, pos) for tokens the preprocessing notebook keeps."""
    out = []
    for t in doc:
        lemma = CUSTOM_LOOKUPS.get(t.text, t.lemma_)
        if t.is_alpha and lemma.lower() not in stopwords and t.pos_ in KEEP_POS:
            out.append((t.text, lemma.lower(), t.pos_))
    return out
