"""A4: the conference topic heatmaps redrawn with empty topics labelled.

Uses the saved models unchanged (no retraining):
  play level  gensimvenv/corpus_pkl/filtered_ideal_model.pkl (k = 8) + filtered_corpus.pkl
  act level   gensimvenv/acts_pkl/acts_filtered_LDA_models.pkl[24] + acts_filtered_corpus.pkl
Topic labels are the author's, copied from the notebooks
(LDA_Coherence_Values.ipynb cell 53, Acts_LDA_Coherence_Values.ipynb cell 34);
each is prefixed with its topic number, which also separates the two topics that
share the label "Restraint & Ethical Reflection" (Topics 3 and 8).

Empty topic = no document (play or act) has a weight of at least 0.05 in it.
Empty topics are marked "(empty)" in grey, and their columns are hatched.
The original figures in figures/ are not touched.

Outputs: results/a4_heatmaps/a4_heatmaps.md, fig_a4_play_topics_k8.png, fig_a4_act_topics_k24.png
"""
from __future__ import annotations

import pickle

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

import pipeline as P
from a2_acts import ABBR
from a2_analyze import BLUES, INK, INK2, SURFACE

OUT = P.RESULTS / "a4_heatmaps"
G = P.ROOT / "gensimvenv"
EMPTY_MAX = 0.05
MUTED = "#8a897f"
PLAY_LABELS = ["Grotesque Pleasure & Familial Betrayal", "Concealed Sin & Homecoming", "Restraint & Ethical Reflection",
               "Perversion & Ritual Distortion", "Fortune & Poetic Mediation", "Tyranny & Political Ambition",
               "Invasion, Punishment, Deceit & Fate", "Restraint & Ethical Reflection"]
ACT_LABELS = ["Authority, Emotional Unrest, and Social Fragility", "Rightful Origin, Cosmic Order, and Betrayal",
              "Passion, Materiality, and Violated Interiors", "Fate, Grief, and the Sea",
              "Cycles of Kinship, Growth and Violence", "Constrained Desire and Rehearsed Transgression",
              "Power, Control and Social Consent", "Virtue and Suffering under Divine Judgement",
              "Immediate Action, Struggle, and Perception", "Ritualized Grief and the Materiality of Catastrophe",
              "Order, Moral Duty, and Emerging Conflict", "Material Power, Anticipation, and Kinship",
              "Spectacle, Youth, and Ritualized Violence", "Commemoration, Response, and Rationality",
              "Authority, Violence, and Human Suffering", "Symbols of Power, Martial Action, and Human Fragility",
              "Ceremony, Kinship and the Subversion of Ritual", "Governance, Social Instability, and Displacement",
              "Civic Judgement, Incited Rage, and Public Punishment",
              "Material Death and Ritual Invocation in Contained Spaces",
              "Restraint, Perception, and Physical Seasonality", "Grief, Judgement, and Fragile Vitality",
              "Performance, Spectacle, and Ritual Action", "Divination, Law, and Contamination"]


def load(path):
    with open(path, "rb") as f:
        return pickle.load(f)


def draw(M, rows, labels, title, path, figsize, annot_size, rot):
    k = M.shape[1]
    empty = M.max(axis=0) < EMPTY_MAX
    fig, ax = plt.subplots(figsize=figsize, facecolor=SURFACE, constrained_layout=True)
    im = ax.imshow(M, cmap=BLUES, vmin=0, vmax=1, aspect="auto")
    for j in np.where(empty)[0]:
        ax.add_patch(Rectangle((j - 0.5, -0.5), 1, len(rows), fill=False, hatch="///", edgecolor="#c3c2b7",
                               linewidth=0))
    for i in range(M.shape[0]):
        for j in range(k):
            v = M[i, j]
            ax.text(j, i, f"{v:.2f}" if v >= 0.005 else "0", ha="center", va="center", fontsize=annot_size,
                    color=SURFACE if v > 0.6 else (INK if v >= 0.005 else MUTED))
    xl = [f"T{j + 1}  {lab}" + ("  (empty)" if empty[j] else "") for j, lab in enumerate(labels)]
    ax.set_xticks(range(k), xl, rotation=rot, ha="right", rotation_mode="anchor", fontsize=8.5)
    for j, t in enumerate(ax.get_xticklabels()):
        t.set_color(MUTED if empty[j] else INK)
        if empty[j]:
            t.set_fontstyle("italic")
    ax.set_yticks(range(len(rows)), rows, fontsize=8.5)
    for t in ax.get_yticklabels():
        if t.get_text().startswith("Ece"):
            t.set_fontweight("bold")
    ax.tick_params(length=0, colors=INK)
    for s in ax.spines.values():
        s.set_visible(False)
    cb = fig.colorbar(im, ax=ax, shrink=0.6, pad=0.01)
    cb.set_label("Topic weight", fontsize=9, color=INK2)
    cb.outline.set_visible(False)
    cb.ax.tick_params(labelsize=8, colors=INK2)
    ax.set_title(title, fontsize=11, color=INK, loc="left", pad=16)
    ax.text(0, 1.005, f"(empty) = no {'play' if len(rows) < 20 else 'act'} has a weight of {EMPTY_MAX} or more "
            "in the topic (hatched column). Topic labels: the author's.", transform=ax.transAxes,
            fontsize=8, color=INK2, va="bottom", ha="left")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    return empty


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    md = ["# A4: conference topic heatmaps with empty topics labelled", "",
          f"Saved conference models, unchanged. Empty topic = no document has a weight of {EMPTY_MAX} or more in it. "
          "Each label is prefixed with its topic number, which also separates the two topics that carry the same label.", ""]
    # play level
    model = load(G / "corpus_pkl" / "filtered_ideal_model.pkl")
    corpus = load(G / "corpus_pkl" / "filtered_corpus.pkl")
    titles = [d["title"] for d in P.load_docs("play")]
    M = P.doc_topic_matrix(model, corpus)
    e1 = draw(M, titles, PLAY_LABELS, "Topic weights per play (conference model, k = 8, seed 42)",
              OUT / "fig_a4_play_topics_k8.png", (11, 6.2), 8.5, 30)
    dom = M.argmax(axis=1)
    md += ["## Play level (k = 8)", "",
           f"- Empty topics: {', '.join(f'T{j + 1} ({PLAY_LABELS[j]})' for j in np.where(e1)[0]) or 'none'}.",
           f"- Topics that are no play's dominant topic: {', '.join(f'T{j + 1}' for j in range(8) if j not in dom)}.",
           "- The duplicate label 'Restraint & Ethical Reflection' is on T3 and T8; both are empty. The labels are kept "
           "as written in the notebook; relabelling is left to the author.", "",
           "Figure: `fig_a4_play_topics_k8.png`.", ""]
    # act level
    model = load(G / "acts_pkl" / "acts_filtered_LDA_models.pkl")[24]
    corpus = load(G / "acts_pkl" / "acts_filtered_corpus.pkl")
    acts = P.load_docs("act")
    rows = [f"{ABBR[d['title']]} {d['act']}" for d in acts]
    M = P.doc_topic_matrix(model, corpus)
    e2 = draw(M, rows, ACT_LABELS, "Topic weights per act (conference model, k = 24, seed 42)",
              OUT / "fig_a4_act_topics_k24.png", (15, 15), 6.5, 45)
    dom = M.argmax(axis=1)
    md += ["## Act level (k = 24)", "",
           f"- Empty topics ({int(e2.sum())}): {', '.join(f'T{j + 1} ({ACT_LABELS[j]})' for j in np.where(e2)[0]) or 'none'}.",
           f"- Topics that are no act's dominant topic: {', '.join(f'T{j + 1}' for j in range(24) if j not in dom)}.", "",
           "Figure: `fig_a4_act_topics_k24.png`.", ""]
    (OUT / "a4_heatmaps.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
