"""A5 part 1: does relaxing no_above move Ecerinis's topic toward shared vocabulary?

v2 tokens (src/v2_corpus.token_lists('play')), no_below = 2, play-level LDA with the
notebook settings (passes=20, alpha='symmetric', chunksize = all documents).

Settings:
  0.5        no_above = 0.5 (baseline; same models as A2 v2)
  0.8        no_above = 0.8
  1.0        no_above = 1.0 (no upper filter)
  1.0+tfidf  no_above = 1.0 with TF-IDF weighting of the counts: count x log2(11 / plays
             containing the word), no length normalization. Added because at 1.0 a few
             very frequent words (manus, scelus, magnus, deus, regnum) dominate every topic
             and 10 of 11 plays share one topic. keep_n was not used: it keeps the most
             frequent words, which are the problem. A word in all 11 plays gets weight 0.

Seed check: seeds 0-49, k = 7-9 scored (k = 10 trained for the adjacent-model overlap of
k = 9); selection rule as in A2 (mean trade-off, ties within 1 SE -> smallest k), applied
within k = 7-9. Coherence (c_v) uses the token lists and the setting's dictionary, as in A2.

Per setting and k: Ecerinis's dominant topic in each seed: alone or shared (and with
whom); its top 20 words by relevance (lambda = 0.6, p(w) from the setting's model input);
how many of those words occur in more than 5 of the 11 plays (the words no_above = 0.5
removes) and their mean number of plays; theme-lexicon words (data/theme_lexicon_v1.json)
among them.

Seed 42 at k = 8 and 9 (the conference seed; v2's rule-selected k is 9): Ecerinis's topic,
its top words, the plays sharing it, and the A3 attribution (phi and the contrastive pull
against the next-best topic).

Outputs: results/a5_no_above/no_above_summary.md, tradeoff_by_seed.csv, ecerinis_topic_by_seed.csv
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

import pipeline as P
import v2_corpus

OUT = P.RESULTS / "a5_no_above"
SETTINGS = [("0.5", 0.5, False), ("0.8", 0.8, False), ("1.0", 1.0, False), ("1.0+tfidf", 1.0, True)]
KS = [7, 8, 9]
SEEDS = list(range(50))
_D = {}


def build(no_above, tfidf):
    trip = v2_corpus.token_lists("play")
    titles = [t for _, t, _ in trip]
    lists = [l for _, _, l in trip]
    dictionary, corpus = P.build_corpus(lists, no_above=no_above)
    if tfidf:
        n = len(corpus)
        dictionary.filter_tokens(bad_ids=[i for i, df in dictionary.dfs.items() if df == n])  # weight 0: drop
        dictionary.compactify()
        corpus = [dictionary.doc2bow(t) for t in lists]
        df = Counter(w for doc in corpus for w, _ in doc)
        corpus = [[(w, c * float(np.log2(n / df[w]))) for w, c in doc] for doc in corpus]
    return titles, lists, dictionary, corpus


def init():
    for name, na, tf in SETTINGS:
        _D[name] = build(na, tf)


def run(job):
    name, seed = job
    titles, lists, dictionary, corpus = _D[name]
    models = {k: P.train_lda(corpus, dictionary, k, seed) for k in KS + [10]}
    tops = {k: P.top_words(models[k], k) for k in KS + [10]}
    e = titles.index("Ecerinis")
    trade, topic_rows = [], []
    for k in KS:
        coh = P.coherence_cv(models[k], lists, dictionary)
        ovl = P.adjacent_model_overlap(tops[k], tops[k + 1])
        trade.append({"setting": name, "seed": seed, "k": k, "coherence": coh, "overlap": ovl, "tradeoff": coh - ovl})
        mat = P.doc_topic_matrix(models[k], corpus)
        dom = mat.argmax(axis=1)
        t = int(dom[e])
        rel = P.relevance_keywords(models[k], corpus, topn=20, lam=0.6)[t]
        topic_rows.append({"setting": name, "seed": seed, "k": k, "topic": t, "weight": float(mat[e, t]),
                           "partners": ";".join(titles[i] for i in range(len(titles)) if i != e and dom[i] == t),
                           "n_plays_alone": int(sum(1 for i in range(len(titles))
                                                    if (dom == dom[i]).sum() == 1)),
                           "top20": ";".join(rel)})
    return trade, topic_rows


def attribution_block(name, k, seed, lex_words, plays_per_word):
    titles, lists, dictionary, corpus = _D[name] if name in _D else build(*[(na, tf) for n, na, tf in SETTINGS if n == name][0])
    m = P.train_lda(corpus, dictionary, k, seed)
    mat = P.doc_topic_matrix(m, corpus)
    e = titles.index("Ecerinis")
    t = int(mat[e].argmax())
    bow = corpus[e]
    m.random_state = np.random.RandomState(0)
    _, _, phis = m.get_document_topics(bow, minimum_probability=0.0, minimum_phi_value=0.0, per_word_topics=True)
    phi = {dictionary[w]: dict(p).get(t, 0.0) for w, p in phis}
    topics = m.get_topics()
    ll = [sum(c * np.log(topics[tt, w]) for w, c in bow) for tt in range(k)]
    t2 = int(np.argsort(ll)[-2]) if int(np.argmax(ll)) == t else int(np.argmax(ll))
    pull = {dictionary[w]: c * (np.log(topics[t, w]) - np.log(topics[t2, w])) for w, c in bow}
    rel = P.relevance_keywords(m, corpus, topn=20, lam=0.6)[t]
    partners = [titles[i] for i in range(len(titles)) if i != e and mat[i].argmax() == t]
    t2_plays = [titles[i] for i in range(len(titles)) if mat[i].argmax() == t2]
    weights = ", ".join(f"T{j + 1} {mat[e, j]:.2f}" for j in np.argsort(-mat[e])[:3] if mat[e, j] >= 0.01)

    def mark(w):
        return f"**{w}**" if w in lex_words else w

    return [f"#### setting {name}, k = {k}, seed {seed}", "",
            f"- Ecerinis's topic weights: {weights}. Dominant: Topic {t + 1}, shared with: {', '.join(partners) or 'no other play'}.",
            f"- Top 20 by relevance (λ = 0.6; bold = theme-lexicon word; number = plays containing the word): "
            + ", ".join(f"{mark(w)} ({plays_per_word[w]})" for w in rel) + ".",
            f"- Words carrying Ecerinis into Topic {t + 1} (phi, expected tokens): "
            + ", ".join(f"{mark(w)} {v:.1f}" for w, v in sorted(phi.items(), key=lambda x: -x[1])[:15]) + ".",
            f"- Contrastive pull vs the next-best topic, Topic {t2 + 1} (dominant in: {', '.join(t2_plays) or 'no play'}): "
            + ", ".join(f"{mark(w)} {v:.1f}" for w, v in sorted(pull.items(), key=lambda x: -x[1])[:15]) + ".", ""]


def selection(sc):
    g = sc.groupby("k").tradeoff
    st = pd.DataFrame({"mean": g.mean(), "sd": g.std(ddof=1), "se": g.std(ddof=1) / np.sqrt(g.count())})
    best = int(st["mean"].idxmax())
    tied = [k for k in st.index if st.loc[k, "mean"] >= st.loc[best, "mean"] - st.loc[best, "se"]]
    piv = sc.pivot(index="seed", columns="k", values="tradeoff")
    wins = Counter(int(piv.columns[np.argmax(r.values)]) for _, r in piv.iterrows())
    return st, best, tied, min(tied), wins


def main():
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = [(n, s) for n, _, _ in SETTINGS for s in SEEDS]
    trade, topics = [], []
    with ProcessPoolExecutor(max_workers=workers, initializer=init) as ex:
        for tr, tp in ex.map(run, jobs):
            trade += tr
            topics += tp
    sc, tp = pd.DataFrame(trade), pd.DataFrame(topics)
    sc.to_csv(OUT / "tradeoff_by_seed.csv", index=False)
    tp.to_csv(OUT / "ecerinis_topic_by_seed.csv", index=False, encoding="utf-8-sig")

    trip = v2_corpus.token_lists("play")
    plays_per_word = Counter(w for _, _, l in trip for w in set(l))
    lex = {k: v for k, v in json.loads((P.DATA / "theme_lexicon_v1.json").read_text(encoding="utf-8")).items()
           if not k.startswith("_")}
    lex_words = {w for ws in lex.values() for w in ws}
    a2 = pd.read_csv(P.RESULTS / "a2_seeds" / "tradeoff_by_seed.csv")
    a2 = a2[(a2.pipeline == "v2") & (a2.k.isin(KS))].set_index(["seed", "k"]).tradeoff
    base = sc[sc.setting == "0.5"].set_index(["seed", "k"]).tradeoff
    diff = float((base - a2.loc[base.index]).abs().max())

    md = ["# A5 part 1: no_above and Ecerinis's topic (v2 tokens)", "",
          "Settings: no_above = 0.5 (baseline), 0.8, 1.0, and 1.0 with TF-IDF weighting (count × log2(11 / plays "
          "containing the word), no length normalization). **TF-IDF was added because at 1.0 a few very frequent words "
          "(manus, scelus, magnus, deus, regnum) dominate every topic.** keep_n was not used: it keeps the most frequent "
          "words. Under TF-IDF a word in all 11 plays gets weight 0, so it acts like no_above just below 1.0 plus "
          "down-weighting of the other common words.", "",
          f"Seeds 0–49; k = 7–9 scored. The 0.5 baseline reproduces the A2 v2 trade-offs (largest difference {diff:.1e}).", ""]
    vocab = {n: len(_build_cached(n)[2]) for n, _, _ in SETTINGS}
    md += ["| setting | vocabulary | Ecerinis tokens (or weight) in the model input |", "|---|---|---|"]
    for n, _, _ in SETTINGS:
        titles, _, d, c = _build_cached(n)
        md.append(f"| {n} | {len(d):,} | {sum(v for _, v in c[titles.index('Ecerinis')]):,.0f} |")
    md += ["", "## Seed check: k selection within k = 7–9", "",
           "| setting | mean trade-off k=7 / 8 / 9 (SE) | rule-selected k | tied within 1 SE | wins k=7 / 8 / 9 |",
           "|---|---|---|---|---|"]
    for n, _, _ in SETTINGS:
        st, best, tied, chosen, wins = selection(sc[sc.setting == n])
        md.append(f"| {n} | " + " / ".join(f"{st.loc[k, 'mean']:.3f} ({st.loc[k, 'se']:.3f})" for k in KS)
                  + f" | {chosen} | {', '.join(map(str, tied)) if len(tied) > 1 else 'no tie'} | "
                  + " / ".join(str(wins.get(k, 0)) for k in KS) + " |")
    md += ["", "## Ecerinis's dominant topic across the 50 seeds", "",
           "Shared vocabulary = the topic's top-20 relevance words that occur in more than 5 of the 11 plays (the words "
           "no_above = 0.5 removes). Plays per word = mean number of plays containing each top-20 word.", "",
           "| setting | k | Ecerinis alone | most frequent partners (share of seeds) | mean weight | top-20 words in >5 plays (mean) | "
           "plays per word (mean) | theme-lexicon words in the top 20 (share of seeds) | plays alone in their topic (mean of 11) |",
           "|---|---|---|---|---|---|---|---|---|"]
    stable = []
    for n, _, _ in SETTINGS:
        for k in KS:
            g = tp[(tp.setting == n) & (tp.k == k)]
            words = [s.split(";") for s in g.top20]
            alone = (g.partners.fillna("") == "").mean()
            part = Counter(p for s in g.partners.fillna("") for p in (s.split(";") if s else []))
            shared = np.mean([sum(plays_per_word[w] > 5 for w in ws) for ws in words])
            ppw = np.mean([np.mean([plays_per_word[w] for w in ws]) for ws in words])
            lexc = Counter(w for ws in words for w in ws if w in lex_words)
            md.append(f"| {n} | {k} | {alone:.0%} | " + ", ".join(f"{p} {c / len(g):.0%}" for p, c in part.most_common(3))
                      + f" | {g.weight.mean():.2f} | {shared:.1f} | {ppw:.1f} | "
                      + (", ".join(f"{w} {c / len(g):.0%}" for w, c in lexc.most_common()) or "none")
                      + f" | {g.n_plays_alone.mean():.1f} |")
            cnt = Counter(w for ws in words for w in ws)
            stable.append(f"- **{n}, k = {k}**: " + ", ".join(
                f"{w} {c / len(g):.0%}" for w, c in sorted(cnt.items(), key=lambda x: (-x[1], x[0])) if c / len(g) >= 0.5))
    md += ["", "Words in Ecerinis's topic's top 20 in at least 50% of seeds:", ""] + stable + [""]
    md += ["## Seed 42: Ecerinis's topic and the A3 attribution under each setting", ""]
    for k in (9, 8):
        for n, _, _ in SETTINGS:
            md += attribution_block(n, k, 42, lex_words, plays_per_word)
    (OUT / "no_above_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


_CACHE = {}


def _build_cached(name):
    if name not in _CACHE:
        na, tf = [(a, b) for n, a, b in SETTINGS if n == name][0]
        _CACHE[name] = build(na, tf)
        _D[name] = _CACHE[name]
    return _CACHE[name]


if __name__ == "__main__":
    main()
