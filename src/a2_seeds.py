"""A2 seed check, play level: the notebook's selection grid over many seeds.

For each pipeline and seed: LDA for k = 1..10 (passes=20, alpha='symmetric',
chunksize=len(corpus)), c_v coherence and adjacent-model overlap for k = 1..9,
trade-off = coherence - overlap. Exactly the calculation in
notebooks/play_lda/LDA_Coherence_Values.ipynb (see src/pipeline.py).

Pipelines:
  original  saved LatinCy lemmas, original named-entity list, no normalization
            (the conference pipeline)
  v2        LatinCy 3.9.8 lemmas with the approved A1 fixes (src/v2_corpus.py)
Seeds 0-49 (includes 42).

Outputs (results/a2_seeds/):
  tradeoff_by_seed.csv   pipeline, seed, k, coherence, overlap, tradeoff
  doc_topics.csv.gz      pipeline, seed, k, play, topic, weight   (every run)
  top_words.csv.gz       pipeline, seed, k, topic, rank, word, prob (top 20, every run)
  top_words_relevance.csv.gz  top 20 by relevance (lambda = 0.6), every run
                         (second pass: `python src/a2_seeds.py 4 relevance`)
  reproduction.md        seed 42 (original) against the saved notebook values
"""
from __future__ import annotations

import pickle
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

import pipeline as P

OUT = P.RESULTS / "a2_seeds"
SEEDS = list(range(50))
KS = list(range(1, 11))
_DATA = {}


def load_pipeline(name):
    if name == "original":
        docs = P.load_docs("play")
        titles = [d["title"] for d in docs]
        lists = P.remove_named_entities(docs, P.load_named_entities())
    else:
        import v2_corpus
        triples = v2_corpus.token_lists("play")
        titles = [t for _, t, _ in triples]
        lists = [l for _, _, l in triples]
    dictionary, corpus = P.build_corpus(lists)
    return titles, lists, dictionary, corpus


def init_worker():
    for name in ("original", "v2"):
        _DATA[name] = load_pipeline(name)


def run(job):
    name, seed = job
    titles, lists, dictionary, corpus = _DATA[name]
    models, topics, scored, coh, ovl, tr = P.selection_grid(lists, dictionary, corpus, seed=seed)
    dt, tw = [], []
    for k in KS:
        m = models[k]
        mat = P.doc_topic_matrix(m, corpus)
        for i, play in enumerate(titles):
            for t in range(k):
                dt.append((name, seed, k, play, t, float(mat[i, t])))
        for t in range(k):
            for r, (w, p) in enumerate(m.show_topic(t, topn=20)):
                tw.append((name, seed, k, t, r, w, float(p)))
    scores = [(name, seed, k, c, o, x) for k, c, o, x in zip(scored, coh, ovl, tr)]
    return scores, dt, tw


def run_relevance(job):
    """Retrain (deterministic for a given seed) and return the top 20 words per
    topic by relevance, lambda = 0.6 (no coherence needed)."""
    name, seed = job
    titles, lists, dictionary, corpus = _DATA[name]
    rows = []
    for k in KS:
        m = P.train_lda(corpus, dictionary, k, seed)
        rel = P.relevance_keywords(m, corpus, topn=20, lam=0.6, return_scores=True)
        for t, words in rel.items():
            for r, (w, score) in enumerate(words):
                rows.append((name, seed, k, t, r, w, score))
    return rows


def main_relevance(workers):
    jobs = [(name, s) for name in ("original", "v2") for s in SEEDS]
    rows = []
    with ProcessPoolExecutor(max_workers=workers, initializer=init_worker) as ex:
        for r in ex.map(run_relevance, jobs):
            rows += r
    pd.DataFrame(rows, columns=["pipeline", "seed", "k", "topic", "rank", "word", "relevance"]).to_csv(
        OUT / "top_words_relevance.csv.gz", index=False)
    print(f"relevance top-20 saved for {len(jobs)} runs")


def main():
    if len(sys.argv) > 2 and sys.argv[2] == "relevance":
        main_relevance(int(sys.argv[1]))
        return
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = [(name, s) for name in ("original", "v2") for s in SEEDS]
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    t0 = time.time()
    scores, dts, tws = [], [], []
    with ProcessPoolExecutor(max_workers=workers, initializer=init_worker) as ex:
        for n, (s, d, w) in enumerate(ex.map(run, jobs), 1):
            scores += s
            dts += d
            tws += w
            if n % 10 == 0:
                print(f"{n}/{len(jobs)} runs, {time.time() - t0:.0f} s", flush=True)
    sc = pd.DataFrame(scores, columns=["pipeline", "seed", "k", "coherence", "overlap", "tradeoff"])
    sc.to_csv(OUT / "tradeoff_by_seed.csv", index=False)
    pd.DataFrame(dts, columns=["pipeline", "seed", "k", "play", "topic", "weight"]).to_csv(
        OUT / "doc_topics.csv.gz", index=False)
    pd.DataFrame(tws, columns=["pipeline", "seed", "k", "topic", "rank", "word", "prob"]).to_csv(
        OUT / "top_words.csv.gz", index=False)

    with open(P.MODELS / "play" / "filtered_coh_sta_diffs.pkl", "rb") as f:
        saved = pickle.load(f)
    s42 = sc[(sc.pipeline == "original") & (sc.seed == 42)].sort_values("k").tradeoff.to_numpy()
    diff = np.abs(np.array(saved) - s42)
    md = ["# Seed 42, original pipeline: grid run vs saved notebook values", "",
          "| k | saved trade-off | this run | abs. difference |", "|---|---|---|---|"]
    md += [f"| {k} | {a:.4f} | {b:.4f} | {d:.1e} |" for k, a, b, d in zip(range(1, 10), saved, s42, diff)]
    md += ["", f"Max difference for k = 2-9: {diff[1:].max():.1e} (k = 1 differs as in "
           "results/a0_reproduction; it is never selected).", f"Wall time: {time.time() - t0:.0f} s."]
    (OUT / "reproduction.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
