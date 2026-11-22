"""A3 word-level attribution for Ecerinis.

Models (pipeline, seed, k):
  original 42 8   the model the conference analysis used
  original 25 8   representative seed (rule 3) at the rule-selected k (8)
  v2       42 8
  v2       35 9   representative seed at v2's rule-selected k (9)
  v2       29 8   representative seed at k = 8 (added for a like-for-like comparison)

For each: gensim get_document_topics(bow, per_word_topics=True) on Ecerinis.
phi_values give, per word, the expected number of its Ecerinis tokens assigned to
each topic (probability x count). The words that carry Ecerinis into its dominant
topic are ranked by that value; 'share' is the word's part of Ecerinis's total
phi mass in the topic. Inference starts from random values, so the model's random
state is fixed before each call (checked: two calls give identical output).
Shown next to the topic's top 20 words by relevance (lambda = 0.6).

Outputs: results/a3_attribution/a3_summary.md, attribution_*.csv, figures/fig_a3_*.png
"""
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import pipeline as P
from a2_analyze import AXIS, GRID, INK, INK2, MUTED, SURFACE, style
from a2_seeds import load_pipeline

OUT = P.RESULTS / "a3_attribution"
FIG = OUT / "figures"
MODELS = [("original", 42, 8, "conference model"), ("original", 25, 8, "representative seed, rule-selected k"),
          ("v2", 42, 8, "seed 42"), ("v2", 35, 9, "representative seed, rule-selected k"),
          ("v2", 29, 8, "representative seed at k = 8")]
SHARED, OTHER = "#2a78d6", "#c3c2b7"


def attribution(model, bow, t):
    model.random_state = np.random.RandomState(0)
    doc, word_topics, phis = model.get_document_topics(bow, minimum_probability=0.0,
                                                       minimum_phi_value=0.0, per_word_topics=True)
    return dict(doc), {w: dict(p).get(t, 0.0) for w, p in phis}


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    md = ["# A3 word-level attribution for Ecerinis", "",
          "For each model: the Ecerinis words that carry it into its dominant topic (expected Ecerinis tokens assigned "
          "to the topic, from gensim's per-word phi values) next to the topic's top 20 words by relevance (λ = 0.6).", "",
          "**Caveat.** In every model Ecerinis sits almost entirely in one topic (weight 0.998), so each word's phi equals "
          "its count: the phi ranking is Ecerinis's word frequency list, not a measure of which words pull it into the "
          "topic. A supplementary contrastive measure is therefore added: each word's pull toward the dominant topic "
          "relative to the topic that would explain Ecerinis second best.", ""]
    cache = {}
    for pipe, seed, k, tag in MODELS:
        if pipe not in cache:
            cache[pipe] = load_pipeline(pipe)
        titles, lists, dictionary, corpus = cache[pipe]
        e = titles.index("Ecerinis")
        bow = corpus[e]
        model = P.train_lda(corpus, dictionary, k, seed)
        mat = P.doc_topic_matrix(model, corpus)
        t = int(mat[e].argmax())
        doc1, phi1 = attribution(model, bow, t)
        doc2, phi2 = attribution(model, bow, t)
        assert phi1 == phi2, "attribution not deterministic"
        counts = dict(bow)
        dfreq = {}
        for d in corpus:
            for w, _ in d:
                dfreq[w] = dfreq.get(w, 0) + 1
        total = sum(phi1.values())
        rel = P.relevance_keywords(model, corpus, topn=20, lam=0.6, return_scores=True)[t]
        rel_words = [w for w, _ in rel]
        phi_t = model.get_topics()[t]
        rows = [{"lemma": dictionary[w], "count_in_ecerinis": counts[w], "expected_tokens_in_topic": round(v, 3),
                 "share_of_ecerinis_topic_mass": round(v / total, 4), "plays_containing": dfreq[w],
                 "in_topic_top20_relevance": dictionary[w] in rel_words}
                for w, v in sorted(phi1.items(), key=lambda x: -x[1]) if v > 0]
        att = pd.DataFrame(rows)
        # supplementary, contrastive: which words favour the dominant topic over the next-best one
        topics = model.get_topics()
        ll = [sum(c * np.log(topics[tt, w]) for w, c in bow) for tt in range(k)]
        t2 = int(np.argsort(ll)[-2]) if int(np.argmax(ll)) == t else int(np.argmax(ll))
        pull = {dictionary[w]: c * (np.log(topics[t, w]) - np.log(topics[t2, w])) for w, c in bow}
        att["pull_vs_next_best_topic"] = att.lemma.map(lambda w: round(float(pull[w]), 3))
        att.to_csv(OUT / f"attribution_{pipe}_seed{seed}_k{k}.csv", index=False, encoding="utf-8-sig")
        t2_plays = [titles[i] for i in range(len(titles)) if mat[i].argmax() == t2]
        pull_df = pd.DataFrame([{"lemma": w, "count_in_ecerinis": counts[dictionary.token2id[w]],
                                 "pull": round(float(v), 3),
                                 "in_topic_top20_relevance": w in rel_words}
                                for w, v in sorted(pull.items(), key=lambda x: -x[1])[:20]])
        partners = [titles[i] for i in range(len(titles)) if i != e and mat[i].argmax() == t]
        top20_cum = att.share_of_ecerinis_topic_mass.head(20).sum()
        kw = [{"rank": r + 1, "lemma": w, "relevance": round(s, 3), "p(w|topic)": round(float(phi_t[dictionary.token2id[w]]), 5),
               "count_in_ecerinis": counts.get(dictionary.token2id[w], 0)} for r, (w, s) in enumerate(rel)]
        kwdf = pd.DataFrame(kw)
        kwdf.to_csv(OUT / f"topic_keywords_{pipe}_seed{seed}_k{k}.csv", index=False, encoding="utf-8-sig")
        n_kw_in_ece = int((kwdf.count_in_ecerinis > 0).sum())
        md += [f"## {pipe}, seed {seed}, k = {k} ({tag})", "",
               f"- Ecerinis's dominant topic: Topic {t + 1}, weight {mat[e, t]:.3f}; shared as dominant topic with: "
               f"{', '.join(partners) or 'no other play'}.",
               f"- Ecerinis has {len(bow)} word types ({sum(counts.values())} tokens) in the model vocabulary; "
               f"{len(att)} carry weight into Topic {t + 1}. The top 20 account for {top20_cum:.0%} of Ecerinis's mass in the topic.",
               f"- Of the topic's top 20 words by relevance, {n_kw_in_ece} occur in Ecerinis.", "",
               "**Words that place Ecerinis in the topic (top 20):**", "",
               att.head(20).to_markdown(index=False), "",
               "**Words that define the topic (top 20 by relevance, λ = 0.6):**", "",
               kwdf.to_markdown(index=False), "",
               f"**Supplementary (contrastive): words that most favour Topic {t + 1} over the next-best topic for Ecerinis, "
               f"Topic {t2 + 1}** (dominant in: {', '.join(t2_plays) or 'no play'}). "
               "Pull = count × (log p(w|topic) − log p(w|next-best topic)).", "",
               pull_df.to_markdown(index=False), ""]

        # figure: two bar charts side by side
        a15 = att.head(15).iloc[::-1]
        k15 = kwdf.head(15).iloc[::-1]
        both = set(att.lemma.head(15)) & set(kwdf.lemma.head(15))
        fig, axes = plt.subplots(1, 2, figsize=(10, 4.8), facecolor=SURFACE)
        for ax in axes:
            style(ax)
            ax.grid(axis="y", visible=False)
            ax.grid(axis="x", color=GRID, linewidth=0.6)
        axes[0].barh(a15.lemma, a15.expected_tokens_in_topic, height=0.7,
                     color=[SHARED if w in set(kwdf.lemma) else OTHER for w in a15.lemma])
        axes[0].set_xlabel("Expected Ecerinis tokens assigned to the topic", fontsize=9, color=INK2)
        axes[0].set_title(f"Words that place Ecerinis in Topic {t + 1}", fontsize=10, color=INK, loc="left")
        axes[1].barh(k15.lemma, k15["p(w|topic)"] * 1000, height=0.7,
                     color=[SHARED if c > 0 else OTHER for c in k15.count_in_ecerinis])
        axes[1].set_xlabel("p(word | topic) × 1000  (ordered by relevance, λ = 0.6)", fontsize=9, color=INK2)
        axes[1].set_title(f"Words that define Topic {t + 1}", fontsize=10, color=INK, loc="left")
        for ax in axes:
            ax.tick_params(axis="y", labelsize=9, colors=INK)
        fig.suptitle(f"{pipe}, seed {seed}, k = {k} ({tag}).  Blue: left, also a top-20 topic word; right, occurs in Ecerinis.",
                     fontsize=9.5, color=INK2, x=0.01, ha="left")
        fig.tight_layout(rect=(0, 0, 1, 0.95))
        fig.savefig(FIG / f"fig_a3_{pipe}_seed{seed}_k{k}.png", dpi=300)
        plt.close(fig)
    md += ["## Figures", ""] + [f"- `figures/fig_a3_{p}_seed{s}_k{k}.png`: {p}, seed {s}, k = {k} ({tag}): Ecerinis's "
                                 f"attribution words (left) vs the topic's top relevance words (right)." for p, s, k, tag in MODELS]
    (OUT / "a3_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
