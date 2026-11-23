"""A2 analysis of the play-level seed grid (reads results/a2_seeds/*.csv*).

Selection rule (fixed in advance, from the brief):
  1. ideal k = highest mean trade-off across seeds; also how often each k wins
     (per seed, the notebook's argmax with the first, i.e. smallest, k on exact ties);
  2. ties: any k whose mean is within one standard error (of the best k's mean)
     of the best is reported as tied, and the smallest tied k is the default;
  3. representative seed at the chosen k: the seed whose binary co-assignment
     matrix (plays sharing a dominant topic) is closest to the consensus matrix
     (mean over seeds) in Frobenius distance; ties -> lowest seed number.
Dominant topic = argmax of the play's topic distribution.

Outputs: results/a2_seeds/a2_summary.md, representative_topics_*.csv, figures/*.png
"""
from __future__ import annotations

import pickle

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle

import pipeline as P
from a2_seeds import load_pipeline

OUT = P.RESULTS / "a2_seeds"
FIG = OUT / "figures"
PIPES = ["original", "v2"]
LABEL = {"original": "Original pipeline (conference)", "v2": "v2 (LatinCy 3.9.8 + A1 fixes)"}
# reference palette (dataviz skill, light mode)
SERIES = {"original": "#2a78d6", "v2": "#eb6834"}
INK, INK2, MUTED, GRID, AXIS, SURFACE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"
BLUES = LinearSegmentedColormap.from_list("seq_blue", ["#fcfcfb", "#cde2fb", "#9ec5f4", "#6da7ec",
                                                       "#3987e5", "#256abf", "#184f95", "#0d366b"])
TRIAD = ["Ecerinis", "Medea", "Hercules Oetaeus"]


def style(ax):
    ax.set_facecolor(SURFACE)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(AXIS)
    ax.tick_params(colors=INK2, labelsize=9)
    ax.grid(axis="y", color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)


def selection(sc):
    g = sc[sc.k <= 9].groupby("k")
    st = pd.DataFrame({m + "_" + f: getattr(g[m], f)() for m in ("coherence", "overlap", "tradeoff")
                       for f in ("mean", "std")})
    n = sc.seed.nunique()
    st["tradeoff_se"] = st.tradeoff_std / np.sqrt(n)
    best = int(st.tradeoff_mean.idxmax())
    tied = sorted(k for k in st.index if st.loc[k, "tradeoff_mean"] >= st.loc[best, "tradeoff_mean"] - st.loc[best, "tradeoff_se"])
    wins = (sc[sc.k <= 9].sort_values(["seed", "k"]).groupby("seed")
            .apply(lambda d: int(d.k.iloc[int(np.argmax(d.tradeoff.to_numpy()))])).value_counts())
    st["wins"] = [int(wins.get(k, 0)) for k in st.index]
    return st, best, tied, min(tied)


def dominant(dt):
    """(seed, k) -> {play: dominant topic}"""
    idx = dt.loc[dt.groupby(["seed", "k", "play"]).weight.idxmax()]
    return {key: dict(zip(g.play, g.topic)) for key, g in idx.groupby(["seed", "k"])}


def coassign(dom, k, plays, seeds):
    mats = []
    for s in seeds:
        d = dom[(s, k)]
        mats.append(np.array([[d[a] == d[b] for b in plays] for a in plays], float))
    return np.mean(mats, axis=0), mats


def heatmap(ax, M, plays, title, show_y=True):
    im = ax.imshow(M, cmap=BLUES, vmin=0, vmax=1)
    ax.set_xticks(range(len(plays)), plays, rotation=60, ha="right", fontsize=8, color=INK2)
    ax.set_yticks(range(len(plays)), plays if show_y else [""] * len(plays), fontsize=8, color=INK2)
    ax.set_title(title, fontsize=10, color=INK, loc="left")
    for s in ax.spines.values():
        s.set_visible(False)
    e = plays.index("Ecerinis")
    ax.add_patch(Rectangle((-0.5, e - 0.5), len(plays), 1, fill=False, edgecolor=INK, linewidth=1.6))
    for j in range(len(plays)):
        if j != e:
            v = M[e, j]
            ax.text(j, e, f"{v:.2f}".lstrip("0") if v < 1 else "1", ha="center", va="center", fontsize=6.5,
                    color="#ffffff" if v > 0.55 else INK)
    ax.tick_params(length=0)
    return im


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    sc_all = pd.read_csv(OUT / "tradeoff_by_seed.csv")
    dt_all = pd.read_csv(OUT / "doc_topics.csv.gz")
    tw_all = pd.read_csv(OUT / "top_words.csv.gz")
    rv_all = pd.read_csv(OUT / "top_words_relevance.csv.gz")
    with open(P.MODELS / "play" / "filtered_LDA_topics.pkl", "rb") as f:
        ref_topic7 = set(pickle.load(f)[8][6])  # seed 42, k=8, Topic 7 (top 10 by probability)
    # same model retrained (identical to the saved one): Topic 7 = index 6, top 20 by relevance
    ref_topic7_rel = set(rv_all[(rv_all.pipeline == "original") & (rv_all.seed == 42) & (rv_all.k == 8)
                                & (rv_all.topic == 6)].word)

    def rel20(rv, s, k, t):
        return set(rv[(rv.seed == s) & (rv.k == k) & (rv.topic == t)].word)

    md = ["# A2 seed check (play level)", "",
          f"Seeds: {sc_all.seed.nunique()} per pipeline (0-49). k = 1-10 trained; coherence, adjacent-model "
          "overlap and the trade-off scored for k = 1-9, as in the notebook.",
          "Pipelines: **original** = the conference pipeline (saved lemmas, original named-entity list); "
          "**v2** = LatinCy 3.9.8 lemmas with the approved A1 fixes.", ""]
    results = {}
    for pipe in PIPES:
        sc, dt, tw, rv = (x[x.pipeline == pipe] for x in (sc_all, dt_all, tw_all, rv_all))
        seeds = sorted(sc.seed.unique())
        plays = list(dt[(dt.seed == seeds[0]) & (dt.k == 1)].play)
        st, best, tied, chosen = selection(sc)
        dom = dominant(dt)
        results[pipe] = dict(st=st, best=best, tied=tied, chosen=chosen, dom=dom, plays=plays, seeds=seeds, tw=tw)

        md += [f"## {LABEL[pipe]}", "", "| k | coherence (mean ± SD) | overlap (mean ± SD) | trade-off (mean ± SD) | SE | wins |",
               "|---|---|---|---|---|---|"]
        for k, r in st.iterrows():
            mark = " **(best)**" if k == best else (" (tied)" if k in tied else "")
            md.append(f"| {k}{mark} | {r.coherence_mean:.3f} ± {r.coherence_std:.3f} | {r.overlap_mean:.3f} ± "
                      f"{r.overlap_std:.3f} | {r.tradeoff_mean:.3f} ± {r.tradeoff_std:.3f} | {r.tradeoff_se:.4f} | {r.wins} |")
        md += ["", f"- **Rule-selected k = {chosen}.** Highest mean trade-off: k = {best}. "
               f"Within one SE of the best: {tied}" + (" (no tie)." if len(tied) == 1 else
               f" → reported as tied; the smallest, k = {chosen}, is the default."),
               f"- Wins out of {len(seeds)} seeds: " + ", ".join(f"k = {k}: {int(w)}" for k, w in st.wins.items() if w) + ".", ""]

        # Topic 7 check
        ref42 = ref42_rel = None
        if pipe == "v2":
            t = dom[(42, 8)]["Ecerinis"]
            ref42 = set(tw[(tw.seed == 42) & (tw.k == 8) & (tw.topic == t) & (tw["rank"] < 10)].word)
            ref42_rel = rel20(rv, 42, 8, t)
        md += ["### Ecerinis's dominant topic: the 'Topic 7' check", "",
               "Jaccard similarity of the shared topic's word list with seed 42's Topic 7 (original pipeline), "
               "computed two ways: top 10 by probability (as in the selection calculation) and top 20 by "
               "relevance (λ = 0.6, as in the keyword tables). Mean [min-max] over the seeds where the three plays share a topic.", "",
               "| k | seeds where Ecerinis, Medea and Hercules Oetaeus share a dominant topic | top 10 by probability | top 20 by relevance"
               + (" | v2's own seed 42, top 10 / top 20 relevance" if pipe == "v2" else "") + " |",
               "|---|---|---|---|" + ("---|" if pipe == "v2" else "")]
        for k in sorted({8, chosen}):
            js, jr, js2, jr2, n_shared = [], [], [], [], 0
            for s in seeds:
                d = dom[(s, k)]
                if d["Ecerinis"] == d["Medea"] == d["Hercules Oetaeus"]:
                    n_shared += 1
                    t = d["Ecerinis"]
                    words = set(tw[(tw.seed == s) & (tw.k == k) & (tw.topic == t) & (tw["rank"] < 10)].word)
                    rwords = rel20(rv, s, k, t)
                    js.append(P.jaccard(words, ref_topic7))
                    jr.append(P.jaccard(rwords, ref_topic7_rel))
                    if ref42 is not None:
                        js2.append(P.jaccard(words, ref42))
                        jr2.append(P.jaccard(rwords, ref42_rel))
            f = lambda v: f"{np.mean(v):.2f} [{min(v):.2f}-{max(v):.2f}]" if v else "-"
            md.append(f"| {k} | {n_shared}/{len(seeds)} ({n_shared / len(seeds):.0%}) | {f(js)} | {f(jr)}"
                      + (f" | {f(js2)} / {f(jr2)}" if pipe == "v2" else "") + " |")
        if pipe == "original":
            md += ["", "Seed-42 Topic 7, top 20 by relevance (λ = 0.6): "
                   + ", ".join(rv_all[(rv_all.pipeline == "original") & (rv_all.seed == 42) & (rv_all.k == 8)
                                      & (rv_all.topic == 6)].sort_values("rank").word)]
        else:
            t = dom[(42, 8)]["Ecerinis"]
            md += ["", f"v2 seed 42, k = 8, Ecerinis's topic (Topic {t + 1}), top 20 by relevance (λ = 0.6): "
                   + ", ".join(rv[(rv.seed == 42) & (rv.k == 8) & (rv.topic == t)].sort_values("rank").word)]
        M8, _ = coassign(dom, 8, plays, seeds)
        Mc, mats = coassign(dom, chosen, plays, seeds)
        e = plays.index("Ecerinis")
        for k, M in sorted({8: M8, chosen: Mc}.items()):
            row = sorted(((plays[j], M[e, j]) for j in range(len(plays)) if j != e), key=lambda x: -x[1])
            md.append(f"\n- k = {k}, share of seeds in which each play shares Ecerinis's dominant topic: "
                      + ", ".join(f"{p} {v:.0%}" for p, v in row))
        md.append("")

        # representative seed (rule 3) at chosen k (and k=8 if different)
        titles, lists, dictionary, corpus = load_pipeline(pipe)
        for k in sorted({chosen, 8}):
            Mk, matsk = coassign(dom, k, plays, seeds)
            dist = [np.linalg.norm(B - Mk) for B in matsk]
            rep = seeds[int(np.argmin(dist))]
            model = P.train_lda(corpus, dictionary, k, rep)
            rel = P.relevance_keywords(model, corpus, topn=20, lam=0.6)
            mat = P.doc_topic_matrix(model, corpus)
            rows = []
            for t in range(k):
                members = [(titles[i], mat[i, t]) for i in range(len(titles)) if mat[i].argmax() == t]
                rows.append({"topic": t + 1, "top20_relevance_lambda06": ", ".join(rel[t]),
                             "plays_dominant": ", ".join(f"{p} ({w:.2f})" for p, w in members) or "(no play: empty topic)",
                             "total_weight": round(float(mat[:, t].sum()), 3)})
            rdf = pd.DataFrame(rows)
            rdf.to_csv(OUT / f"representative_topics_{pipe}_k{k}.csv", index=False, encoding="utf-8-sig")
            md += [f"### Representative seed at k = {k}: seed {rep} (Frobenius distance to consensus {min(dist):.2f}; "
                   f"median over seeds {np.median(dist):.2f})", "", rdf.to_markdown(index=False), ""]
            results[pipe][f"rep{k}"] = rep

    # ---------------- figures ----------------
    ks = list(range(1, 10))
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), facecolor=SURFACE)
    for ax, (m, name) in zip(axes, [("coherence", "Coherence (c_v)"), ("overlap", "Adjacent-model overlap (Jaccard)"),
                                    ("tradeoff", "Trade-off (coherence − overlap)")]):
        style(ax)
        for pipe in PIPES:
            st = results[pipe]["st"]
            mu, sd = st[f"{m}_mean"].to_numpy(), st[f"{m}_std"].to_numpy()
            ax.fill_between(ks, mu - sd, mu + sd, color=SERIES[pipe], alpha=0.15, linewidth=0)
            ax.plot(ks, mu, color=SERIES[pipe], linewidth=2, marker="o", markersize=5, label=LABEL[pipe])
            if m == "tradeoff":
                c = results[pipe]["chosen"]
                ax.axvline(c, color=SERIES[pipe], linewidth=1, linestyle="--")
        ax.set_title(name, fontsize=10, color=INK, loc="left")
        ax.set_xticks(ks)
        ax.set_xlabel("Number of topics (k)", fontsize=9, color=INK2)
    axes[0].legend(frameon=False, fontsize=8, labelcolor=INK2, loc="lower left")
    fig.suptitle(f"Selection metrics across {len(results['original']['seeds'])} seeds (mean ± 1 SD; dashed line = rule-selected k)",
                 fontsize=11, color=INK, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(FIG / "fig_a2_tradeoff_curves.png", dpi=300)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.5, 3.4), facecolor=SURFACE)
    style(ax)
    w = 0.38
    for i, pipe in enumerate(PIPES):
        v = results[pipe]["st"].wins.to_numpy()
        ax.bar(np.array(ks) + (i - 0.5) * w, v, width=w - 0.04, color=SERIES[pipe], label=LABEL[pipe])
    ax.set_xticks(ks)
    ax.set_xlabel("Number of topics (k)", fontsize=9, color=INK2)
    ax.set_ylabel("Seeds in which k has the highest trade-off", fontsize=9, color=INK2)
    ax.legend(frameon=False, fontsize=8, labelcolor=INK2)
    ax.set_title("How often each k wins", fontsize=10, color=INK, loc="left")
    fig.tight_layout()
    fig.savefig(FIG / "fig_a2_wins.png", dpi=300)
    plt.close(fig)

    for pipe in PIPES:
        r = results[pipe]
        ks_show = sorted({r["chosen"], 8})
        fig, axes = plt.subplots(1, len(ks_show), figsize=(4.4 * len(ks_show) + 1.6, 5.0), facecolor=SURFACE,
                                 squeeze=False, constrained_layout=True)
        for n, (ax, k) in enumerate(zip(axes[0], ks_show)):
            M, _ = coassign(r["dom"], k, r["plays"], r["seeds"])
            tag = "rule-selected" if k == r["chosen"] else "conference k"
            im = heatmap(ax, M, r["plays"], f"k = {k} ({tag})", show_y=(n == 0))
        cb = fig.colorbar(im, ax=axes[0].tolist(), shrink=0.7)
        cb.set_label("Share of seeds sharing a dominant topic", fontsize=8, color=INK2)
        cb.ax.tick_params(labelsize=7, colors=INK2)
        cb.outline.set_visible(False)
        fig.suptitle(f"Co-assignment across seeds: {LABEL[pipe]} (Ecerinis row outlined)", fontsize=11,
                     color=INK, x=0.01, ha="left")
        fig.savefig(FIG / f"fig_a2_coassignment_{pipe}.png", dpi=300, bbox_inches="tight")
        plt.close(fig)

        nb = [k for k in (r["chosen"] - 1, r["chosen"], r["chosen"] + 1) if 2 <= k <= 10]
        fig, axes = plt.subplots(1, len(nb), figsize=(4.0 * len(nb) + 1.6, 4.6), facecolor=SURFACE,
                                 squeeze=False, constrained_layout=True)
        for n, (ax, k) in enumerate(zip(axes[0], nb)):
            M, _ = coassign(r["dom"], k, r["plays"], r["seeds"])
            im = heatmap(ax, M, r["plays"], f"k = {k}", show_y=(n == 0))
        cb = fig.colorbar(im, ax=axes[0].tolist(), shrink=0.6)
        cb.set_label("Share of seeds", fontsize=8, color=INK2)
        cb.ax.tick_params(labelsize=7, colors=INK2)
        cb.outline.set_visible(False)
        fig.suptitle(f"Co-assignment at neighbouring k (supplementary): {LABEL[pipe]}", fontsize=11, color=INK,
                     x=0.01, ha="left")
        fig.savefig(FIG / f"fig_a2_coassignment_neighbours_{pipe}.png", dpi=300, bbox_inches="tight")
        plt.close(fig)

    md += ["## Figures", "",
           "- `figures/fig_a2_tradeoff_curves.png`: coherence, adjacent-model overlap and trade-off, mean ± 1 SD across seeds, both pipelines; dashed = rule-selected k.",
           "- `figures/fig_a2_wins.png`: number of seeds in which each k has the highest trade-off.",
           "- `figures/fig_a2_coassignment_{original,v2}.png`: share of seeds in which each pair of plays shares a dominant topic, at the rule-selected k and at k = 8 (Ecerinis row outlined and labelled).",
           "- `figures/fig_a2_coassignment_neighbours_{original,v2}.png`: the same at the neighbouring k values (supplementary)."]
    (OUT / "a2_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
