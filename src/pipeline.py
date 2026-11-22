"""Shared play- and act-level LDA pipeline.

A faithful port of gensimvenv/corpus_pkl/LDA_Coherence_Values.ipynb and
gensimvenv/acts_pkl/Acts_LDA_Coherence_Values.ipynb. Settings, the c_v
coherence call, the adjacent-model overlap and the trade-off score match the
notebooks; only names are updated ("stability" -> "adjacent-model overlap").
"""
from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np
from gensim import corpora, matutils
from gensim.models import CoherenceModel, LdaModel

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
DATA = ROOT / "data"

PLAY_PKL = ROOT / "Corpus" / "processed_corpus.pkl"
ACT_PKL = ROOT / "Acts" / "processed_acts.pkl"
NE_PKL = ROOT / "unique_named_entities.pkl"
STOPWORDS_JSON = ROOT / "stopwords_latin.json"

NO_BELOW = 2
NO_ABOVE = 0.5
PASSES = 20
NUM_KEYWORDS = 10
LAMBDA = 0.6


def load_docs(level: str = "play") -> list[dict]:
    path = PLAY_PKL if level == "play" else ACT_PKL
    with open(path, "rb") as f:
        return pickle.load(f)


def load_named_entities() -> set[str]:
    with open(NE_PKL, "rb") as f:
        return set(pickle.load(f))


def remove_named_entities(docs: list[dict], named_entities: set[str]) -> list[list[str]]:
    return [[t for t in d["tokens"] if t.lower() not in named_entities] for d in docs]


def build_corpus(token_lists, no_below=NO_BELOW, no_above=NO_ABOVE, keep_n=100000):
    dictionary = corpora.Dictionary(token_lists)
    dictionary.filter_extremes(no_below=no_below, no_above=no_above, keep_n=keep_n)
    corpus = [dictionary.doc2bow(t) for t in token_lists]
    return dictionary, corpus


def train_lda(corpus, dictionary, k, seed, alpha="symmetric", passes=PASSES):
    return LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=k,
        chunksize=len(corpus),
        passes=passes,
        alpha=alpha,
        random_state=seed,
    )


def top_words(model, k, n=NUM_KEYWORDS):
    """Top-n words per topic by probability, as the notebooks' show_topics call."""
    shown = model.show_topics(num_topics=k, num_words=n, formatted=False)
    return [[w for w, _ in topic[1]] for topic in shown]


def jaccard(a, b) -> float:
    a, b = set(a), set(b)
    return len(a & b) / len(a | b)


def adjacent_model_overlap(topics_k, topics_k1) -> float:
    """Mean pairwise Jaccard (top-10 words) between every topic of the k model
    and every topic of the k+1 model (the notebooks' 'mean stability')."""
    return float(np.array([[jaccard(t1, t2) for t2 in topics_k1] for t1 in topics_k]).mean())


def coherence_cv(model, token_lists, dictionary, processes=1) -> float:
    return CoherenceModel(
        model=model, texts=token_lists, dictionary=dictionary,
        coherence="c_v", processes=processes,
    ).get_coherence()


def selection_grid(token_lists, dictionary, corpus, seed, ks=range(1, 11),
                   alpha="symmetric", processes=1):
    """Train k in ks; coherence and overlap for all but the last k (as notebook)."""
    ks = list(ks)
    models = {k: train_lda(corpus, dictionary, k, seed, alpha=alpha) for k in ks}
    topics = {k: top_words(models[k], k) for k in ks}
    scored = ks[:-1]
    coh = [coherence_cv(models[k], token_lists, dictionary, processes) for k in scored]
    ovl = [adjacent_model_overlap(topics[k], topics[k + 1]) for k in scored]
    tradeoff = [c - o for c, o in zip(coh, ovl)]
    return models, topics, scored, coh, ovl, tradeoff


def doc_topic_matrix(model, corpus) -> np.ndarray:
    k = model.num_topics
    out = np.zeros((len(corpus), k))
    for i, bow in enumerate(corpus):
        for t, w in model.get_document_topics(bow, minimum_probability=0.0):
            out[i, t] = w
    return out


def relevance_keywords(model, corpus, topn=NUM_KEYWORDS, lam=LAMBDA, return_scores=False):
    """Port of relevance_keywords() in corpus_gensim_relevance_sort.ipynb."""
    phi = model.get_topics()
    K, V = phi.shape
    csc = matutils.corpus2csc(corpus, num_terms=V)
    tf = np.asarray(csc.sum(axis=1)).ravel().astype(float)
    tf[tf == 0.0] = 1e-12
    p_w = tf / tf.sum()
    rel = np.log(np.clip(phi, 1e-12, None)) - (1.0 - lam) * np.log(p_w)[None, :]
    out = {}
    for k in range(K):
        order = np.argsort(-rel[k])[:topn]
        toks = [model.id2word[int(i)] for i in order]
        out[k] = list(zip(toks, rel[k, order].tolist())) if return_scores else toks
    return out
