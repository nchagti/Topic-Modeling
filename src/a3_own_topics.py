"""Each play's own topic across the 50 seeds, and Ecerinis's next-best topic.

Configurations (pipeline, k, representative seed): original 8 25; v2 8 29; v2 9 35.

Part 1 (from the saved A2 outputs, no retraining). For every play and seed, the
play's topic is its dominant topic (argmax of its topic weights). Per play:
  - alone: share of seeds in which no other play has that topic as dominant
  - stable words: words in that topic's top 20 by relevance (lambda = 0.6) in
    >= 50% and >= 80% of the 50 seeds (all seeds, shared or not)
  - mean Jaccard (top 20 by relevance) between the play's topic in each seed
    and in the representative seed (49 comparisons)
Ecerinis is the focus; the ten Seneca plays are the baseline.

Part 2 (retrains the 150 models; deterministic for a given seed, checked
against the saved doc-topic weights). Ecerinis's next-best topic t2, as in
src/a3_attribution.py: the topic other than its dominant topic t under which its
bag of words has the highest log-likelihood (sum of count x log p(w|topic)).
Margin = log-likelihood under t minus under t2 = the sum of the contrastive
pulls over all words. Reported: share of seeds in which t2 is the dominant
topic of each play (a topic can be dominant in several plays) or of no play,
and the median margin.

Outputs: results/a3_own_topics/own_topics_summary.md, own_topics_by_play.csv,
own_topic_word_frequency.csv, ecerinis_next_best_by_seed.csv
"""
from __future__ import annotations

import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

import pipeline as P
from a2_seeds import load_pipeline

A2 = P.RESULTS / "a2_seeds"
OUT = P.RESULTS / "a3_own_topics"
CONFIGS = [("original", 8, 25), ("v2", 8, 29), ("v2", 9, 35)]
SEEDS = list(range(50))
_DATA = {}


def init():
    for n in ("original", "v2"):
        _DATA[n] = load_pipeline(n)


def next_best(job):
    pipe, k, seed = job
    titles, lists, dictionary, corpus = _DATA[pipe]
    m = P.train_lda(corpus, dictionary, k, seed)
    mat = P.doc_topic_matrix(m, corpus)
    e = titles.index("Ecerinis")
    bow = corpus[e]
    topics = m.get_topics()
    t = int(mat[e].argmax())
    ll = np.array([sum(c * np.log(topics[tt, w]) for w, c in bow) for tt in range(k)])
    t2 = int(np.argsort(ll)[-2]) if int(np.argmax(ll)) == t else int(np.argmax(ll))
    dom = mat.argmax(axis=1)
    return {"pipeline": pipe, "k": k, "seed": seed, "ecerinis_topic": t, "next_best_topic": t2,
            "t_is_max_likelihood": bool(int(np.argmax(ll)) == t),
            "margin": float(ll[t] - ll[t2]), "margin_per_token": float((ll[t] - ll[t2]) / sum(c for _, c in bow)),
            "next_best_dominant_in": ";".join(titles[i] for i in range(len(titles)) if dom[i] == t2),
            "ecerinis_topic_shared_with": ";".join(titles[i] for i in range(len(titles)) if i != e and dom[i] == t),
            "_mat": mat}


def pct(x):
    return f"{100 * x:.0f}%"


def main():
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    OUT.mkdir(parents=True, exist_ok=True)
    dt = pd.read_csv(A2 / "doc_topics.csv.gz")
    rel = pd.read_csv(A2 / "top_words_relevance.csv.gz")
    md = ["# Each play's own topic across 50 seeds; Ecerinis's next-best topic", "",
          "A play's topic in a seed = its dominant topic (argmax of its topic weights). 'Alone' = no other play has "
          "that topic as dominant. Stable words = words in that topic's top 20 by relevance (λ = 0.6) in at least 50% / "
          "80% of the 50 seeds, counted over all 50 seeds whether or not the topic is shared (when it is shared, its top "
          "words describe the shared topic, not the play alone). Jaccard = overlap of the top-20 relevance lists between "
          "the play's topic in a seed and in the representative seed, averaged over the other 49 seeds.", "",
          "Ecerinis is the focus; the ten Seneca plays are the baseline.", ""]
    play_rows, word_rows = [], []
    for pipe, k, rep in CONFIGS:
        d = dt[(dt.pipeline == pipe) & (dt.k == k)]
        dom = d.loc[d.groupby(["seed", "play"]).weight.idxmax(), ["seed", "play", "topic"]]
        r = rel[(rel.pipeline == pipe) & (rel.k == k)]
        words = {(s, t): set(g.word) for (s, t), g in r.groupby(["seed", "topic"])}
        plays = sorted(dom.play.unique(), key=lambda p: (p != "Ecerinis", p))
        rows = []
        for play in plays:
            dp = dom[dom.play == play].set_index("seed").topic
            alone = [int((dom[(dom.seed == s)].topic == dp[s]).sum()) == 1 for s in SEEDS]
            cnt = Counter(w for s in SEEDS for w in words[(s, dp[s])])
            ref = words[(rep, dp[rep])]
            jac = [len(ref & words[(s, dp[s])]) / len(ref | words[(s, dp[s])]) for s in SEEDS if s != rep]
            w50 = [(w, c / len(SEEDS)) for w, c in sorted(cnt.items(), key=lambda x: (-x[1], x[0])) if c / len(SEEDS) >= 0.5]
            w80 = [(w, f) for w, f in w50 if f >= 0.8]
            for w, c in cnt.items():
                word_rows.append({"pipeline": pipe, "k": k, "play": play, "word": w, "seeds": c, "share": c / len(SEEDS)})
            rows.append({"pipeline": pipe, "k": k, "play": play, "share_alone": np.mean(alone),
                         "n_words_ge50": len(w50), "n_words_ge80": len(w80),
                         "mean_jaccard_to_rep": float(np.mean(jac)), "sd_jaccard_to_rep": float(np.std(jac, ddof=1)),
                         "alone_in_rep_seed": alone[SEEDS.index(rep)],
                         "words_ge50": "; ".join(f"{w} {pct(f)}" for w, f in w50),
                         "words_ge80": "; ".join(f"{w} {pct(f)}" for w, f in w80)})
        df = pd.DataFrame(rows)
        play_rows.append(df)
        base = df[df.play != "Ecerinis"]
        ece = df[df.play == "Ecerinis"].iloc[0]

        def rank(col):
            return int((df[col] > ece[col]).sum()) + 1

        md += [f"## {pipe}, k = {k} (representative seed {rep})", "",
               "| play | alone | words ≥50% | words ≥80% | mean Jaccard to rep. seed (SD) |", "|---|---|---|---|---|"]
        for _, x in df.iterrows():
            name = f"**{x.play}**" if x.play == "Ecerinis" else x.play
            md.append(f"| {name} | {pct(x.share_alone)} ({int(round(x.share_alone * 50))}/50) | {x.n_words_ge50} | "
                      f"{x.n_words_ge80} | {x.mean_jaccard_to_rep:.2f} ({x.sd_jaccard_to_rep:.2f}) |")
        md += ["", f"Baseline (ten Seneca plays): alone median {pct(base.share_alone.median())} "
               f"(range {pct(base.share_alone.min())}–{pct(base.share_alone.max())}); words ≥50% median "
               f"{base.n_words_ge50.median():.0f} (range {base.n_words_ge50.min()}–{base.n_words_ge50.max()}); words ≥80% median "
               f"{base.n_words_ge80.median():.0f} (range {base.n_words_ge80.min()}–{base.n_words_ge80.max()}); mean Jaccard median "
               f"{base.mean_jaccard_to_rep.median():.2f} (range {base.mean_jaccard_to_rep.min():.2f}–{base.mean_jaccard_to_rep.max():.2f}).",
               f"Ecerinis's rank among the 11 plays (1 = highest; ties share the higher rank): alone {rank('share_alone')}, words ≥50% {rank('n_words_ge50')}, "
               f"words ≥80% {rank('n_words_ge80')}, mean Jaccard {rank('mean_jaccard_to_rep')}.", "",
               "Stable words per play (share of the 50 seeds in which the word is in the play's topic's top 20):", ""]
        for _, x in df.iterrows():
            md.append(f"- **{x.play}**, ≥80%: {x.words_ge80 or '—'}")
            rest = "; ".join(s for s in x.words_ge50.split("; ") if s and s not in x.words_ge80.split("; "))
            md.append(f"  - 50–79%: {rest or '—'}")
        md.append("")
    pd.concat(play_rows).to_csv(OUT / "own_topics_by_play.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(word_rows).sort_values(["pipeline", "k", "play", "seeds", "word"], ascending=[True, True, True, False, True]) \
        .to_csv(OUT / "own_topic_word_frequency.csv", index=False, encoding="utf-8-sig")

    # Part 2: next-best topic for Ecerinis
    jobs = [(pipe, k, s) for pipe, k, _ in CONFIGS for s in SEEDS]
    with ProcessPoolExecutor(max_workers=workers, initializer=init) as ex:
        res = list(ex.map(next_best, jobs))
    titles = {n: load_pipeline(n)[0] for n in ("original", "v2")}
    worst = 0.0
    for x in res:
        d = dt[(dt.pipeline == x["pipeline"]) & (dt.k == x["k"]) & (dt.seed == x["seed"])]
        for i, play in enumerate(titles[x["pipeline"]]):
            saved = d[d.play == play].sort_values("topic").weight.to_numpy()
            worst = max(worst, float(np.abs(saved - x["_mat"][i]).max()))
    nb = pd.DataFrame([{kk: v for kk, v in x.items() if kk != "_mat"} for x in res])
    nb.to_csv(OUT / "ecerinis_next_best_by_seed.csv", index=False, encoding="utf-8-sig")
    md += ["## Ecerinis's next-best topic (contrastive measure, 50 seeds)", "",
           "Next-best topic = the topic other than Ecerinis's dominant topic under which Ecerinis's bag of words has the "
           "highest log-likelihood (as in A3). Margin = log-likelihood under the dominant topic minus under the next-best "
           "topic (= the sum of the per-word pulls); per token = divided by Ecerinis's tokens in the model vocabulary. "
           "Shares by play can sum to more than 100% because a topic can be dominant in several plays.", "",
           f"Retrained models match the saved doc-topic weights (largest absolute difference {worst:.1e}).", ""]
    for pipe, k, rep in CONFIGS:
        g = nb[(nb.pipeline == pipe) & (nb.k == k)]
        c = Counter(p for v in g.next_best_dominant_in for p in (v.split(";") if v else []))
        none = int((g.next_best_dominant_in.fillna("") == "").sum())
        d = dt[(dt.pipeline == pipe) & (dt.k == k)]
        n_dom = d.loc[d.groupby(["seed", "play"]).weight.idxmax()].groupby("seed").topic.nunique()
        empty_share = ((k - n_dom) / (k - 1)).mean()
        md += [f"### {pipe}, k = {k}", "",
               "| next-best topic is dominant in | seeds | share |", "|---|---|---|"]
        for p, n in sorted(c.items(), key=lambda x: (-x[1], x[0])):
            md.append(f"| {p} | {n} | {pct(n / len(g))} |")
        md.append(f"| no play | {none} | {pct(none / len(g))} |")
        md += ["", f"For comparison: of the k − 1 topics other than Ecerinis's, on average {pct(empty_share)} are the "
               f"dominant topic of no play (mean {(k - n_dom).mean():.1f} empty topics per seed), so a topic picked at "
               f"random from them would be a no-play topic {pct(empty_share)} of the time.",
               f"Median margin {g.margin.median():.1f} nats (IQR {g.margin.quantile(.25):.1f}–{g.margin.quantile(.75):.1f}); "
               f"per token {g.margin_per_token.median():.2f} (IQR {g.margin_per_token.quantile(.25):.2f}–"
               f"{g.margin_per_token.quantile(.75):.2f}). Ecerinis's dominant topic is also its maximum-likelihood topic in "
               f"{int(g.t_is_max_likelihood.sum())}/{len(g)} seeds.", ""]
    (OUT / "own_topics_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
