"""A2 act-level check: k = 24 fixed (alpha='auto', passes=20, as in
gensimvenv/acts_pkl/Acts_LDA_Coherence_Values.ipynb), seeds 0-19 plus 42.

Pipelines: original (Acts/processed_acts.pkl, original named-entity list) and
v2 (acts cut from the v2 play parse, src/v2_corpus.py).

Reports how often each Ecerinis act shares a dominant topic with each Seneca act,
the representative seed (rule 3: co-assignment closest to the consensus), and for
each Ecerinis act its dominant topic's top 20 words by relevance (lambda = 0.6).
Outputs: results/a2_seeds/acts_*.csv, acts_summary.md, figures/fig_a2_acts_*.png
"""
from __future__ import annotations

import sys
from concurrent.futures import ProcessPoolExecutor

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import pipeline as P
from a2_analyze import BLUES, INK, INK2, SURFACE

OUT = P.RESULTS / "a2_seeds"
FIG = OUT / "figures"
K = 24
SEEDS = list(range(20)) + [42]
ABBR = {"Phoenissae": "Pho", "Troades": "Tro", "Phaedra": "Pha", "Agamemnon": "Aga", "Hercules Furens": "HF",
        "Medea": "Med", "Octavia": "Oct", "Oedipus": "Oed", "Thyestes": "Thy", "Hercules Oetaeus": "HO",
        "Ecerinis": "Ece"}
_DATA = {}


def load(name):
    if name == "original":
        docs = P.load_docs("act")
        labels = [f"{ABBR[d['title']]} {d['act']}" for d in docs]
        lists = P.remove_named_entities(docs, P.load_named_entities())
    else:
        import v2_corpus
        triples = v2_corpus.token_lists("act")
        labels = [f"{ABBR[t]} {i.rsplit('act', 1)[1]}" for i, t, _ in triples]
        lists = [l for _, _, l in triples]
    dictionary, corpus = P.build_corpus(lists)
    return labels, lists, dictionary, corpus


def init():
    for n in ("original", "v2"):
        _DATA[n] = load(n)


def run(job):
    name, seed = job
    labels, lists, dictionary, corpus = _DATA[name]
    m = P.train_lda(corpus, dictionary, K, seed, alpha="auto")
    mat = P.doc_topic_matrix(m, corpus)
    rel = P.relevance_keywords(m, corpus, topn=20, lam=0.6)
    return name, seed, mat.argmax(axis=1).tolist(), mat.max(axis=1).tolist(), {t: rel[t] for t in range(K)}


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    jobs = [(n, s) for n in ("original", "v2") for s in SEEDS]
    with ProcessPoolExecutor(max_workers=workers, initializer=init) as ex:
        res = list(ex.map(run, jobs))
    md = [f"# A2 act level: k = {K} fixed, {len(SEEDS)} seeds (0-19 and 42)", ""]
    for name in ("original", "v2"):
        labels = load(name)[0]
        runs = {s: (dom, w, rel) for n, s, dom, w, rel in res if n == name}
        ece = [i for i, l in enumerate(labels) if l.startswith("Ece")]
        sen = [i for i, l in enumerate(labels) if not l.startswith("Ece")]
        B = {s: np.array([[runs[s][0][a] == runs[s][0][b] for b in range(len(labels))] for a in range(len(labels))], float)
             for s in SEEDS}
        C = np.mean(list(B.values()), axis=0)
        rep = min(SEEDS, key=lambda s: (np.linalg.norm(B[s] - C), s))
        share = pd.DataFrame(C[np.ix_(ece, sen)], index=[labels[i] for i in ece], columns=[labels[j] for j in sen])
        share.to_csv(OUT / f"acts_coassignment_{name}.csv", encoding="utf-8-sig")
        ee = pd.DataFrame(C[np.ix_(ece, ece)], index=[labels[i] for i in ece], columns=[labels[i] for i in ece])

        md += [f"## {name}", "", f"Representative seed (rule 3): {rep}.", "",
               "### Seneca acts sharing each Ecerinis act's dominant topic (share of seeds; ≥ 0.25 shown)", ""]
        for i in ece:
            row = share.loc[labels[i]].sort_values(ascending=False)
            top = ", ".join(f"{c} {v:.0%}" for c, v in row.items() if v >= 0.25) or "none in ≥ 25% of seeds"
            md.append(f"- **{labels[i]}**: {top}")
        md += ["", "### Ecerinis acts sharing a topic with each other (share of seeds)", "",
               ee.round(2).to_markdown(), ""]
        for s, tag in [(42, "seed 42 (conference)"), (rep, f"representative seed {rep}")]:
            dom, w, rel = runs[s]
            md += [f"### Ecerinis acts' dominant topics, {tag}", "",
                   "| act | topic | weight | shares it with | top 20 by relevance (λ = 0.6) |", "|---|---|---|---|---|"]
            for i in ece:
                t = dom[i]
                partners = [labels[j] for j in range(len(labels)) if j != i and dom[j] == t]
                md.append(f"| {labels[i]} | {t + 1} | {w[i]:.2f} | {', '.join(partners) or '-'} | {', '.join(rel[t])} |")
            md.append("")
        # stability of each Ecerinis act's topic vocabulary: mean Jaccard (top 20 relevance) with the representative seed
        md += ["### Stability of each Ecerinis act's topic vocabulary", "",
               "Mean Jaccard similarity (top 20 by relevance) between the act's dominant topic in each seed and in the representative seed.", ""]
        for i in ece:
            ref = set(runs[rep][2][runs[rep][0][i]])
            js = [P.jaccard(set(runs[s][2][runs[s][0][i]]), ref) for s in SEEDS if s != rep]
            md.append(f"- {labels[i]}: {np.mean(js):.2f} (min {min(js):.2f}, max {max(js):.2f})")
        md.append("")

        fig, ax = plt.subplots(figsize=(14, 2.6), facecolor=SURFACE)
        im = ax.imshow(share.to_numpy(), cmap=BLUES, vmin=0, vmax=1, aspect="auto")
        ax.set_xticks(range(len(sen)), share.columns, rotation=90, fontsize=7, color=INK2)
        ax.set_yticks(range(len(ece)), share.index, fontsize=8, color=INK2)
        for s_ in ax.spines.values():
            s_.set_visible(False)
        ax.tick_params(length=0)
        cb = fig.colorbar(im, ax=ax, shrink=0.9, pad=0.01)
        cb.set_label("Share of seeds", fontsize=8, color=INK2)
        cb.ax.tick_params(labelsize=7, colors=INK2)
        cb.outline.set_visible(False)
        ax.set_title(f"Act level, k = {K}: share of {len(SEEDS)} seeds in which an Ecerinis act and a Seneca act share a dominant topic ({name})",
                     fontsize=10, color=INK, loc="left")
        fig.savefig(FIG / f"fig_a2_acts_{name}.png", dpi=300, bbox_inches="tight")
        plt.close(fig)
    md += ["## Figures", "", "- `figures/fig_a2_acts_{original,v2}.png`: Ecerinis acts × Seneca acts, share of seeds sharing a dominant topic."]
    (OUT / "acts_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
