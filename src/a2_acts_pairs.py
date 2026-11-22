"""Act-level pairing check against a chance baseline (k = 24, alpha='auto', passes=20).

Seeds 0-99 plus 42 (101), both pipelines (original, v2; see src/a2_acts.py).
For the named Ecerinis pairings: the share of seeds in which the two acts share a
dominant topic, set against the distribution of that share over all act pairs
(median, 95th percentile, and the pairing's percentile rank = % of all pairs
with an equal or lower share). For the seed-42 pairings: the content lemmas the
two acts share in the model input (after named-entity removal and the
dictionary filter), with counts; lemmas shared before the dictionary filter but
removed by it are counted and listed in the CSV.

Outputs: results/a2_seeds/acts_pairs_summary.md, acts_pairs_dominant.csv.gz,
acts_pairs_shared_lemmas.csv
"""
from __future__ import annotations

import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from itertools import combinations

import numpy as np
import pandas as pd

import pipeline as P
from a2_acts import load

OUT = P.RESULTS / "a2_seeds"
K = 24
SEEDS = list(range(100)) + [42]
SEED42_PAIRS = [("Ece 1", "Aga 1"), ("Ece 1", "Pho 1"), ("Ece 2", "Thy 1"), ("Ece 5", "Thy 1"),
                ("Ece 2", "Ece 5"), ("Ece 4", "Oed 4"), ("Ece 4", "Tro 4")]
EXTRA_PAIRS = [("Ece 1", "HF 2"), ("Ece 3", "HF 2")]
_DATA = {}


def init():
    for n in ("original", "v2"):
        _DATA[n] = load(n)


def run(job):
    name, seed = job
    labels, lists, dictionary, corpus = _DATA[name]
    m = P.train_lda(corpus, dictionary, K, seed, alpha="auto")
    return name, seed, P.doc_topic_matrix(m, corpus).argmax(axis=1).tolist()


def main():
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    jobs = [(n, s) for n in ("original", "v2") for s in SEEDS]
    with ProcessPoolExecutor(max_workers=workers, initializer=init) as ex:
        res = list(ex.map(run, jobs))
    rows = []
    md = [f"# Act-level pairings against a chance baseline (k = {K}, {len(SEEDS)} seeds: 0-99 and 42)", "",
          "Share = fraction of seeds in which the two acts have the same dominant topic. Baseline = the same "
          "share for every pair of the 56 acts (1,540 pairs). Percentile rank = % of all pairs with an equal or lower share.", ""]
    lemma_rows = []
    for name in ("original", "v2"):
        labels, lists, dictionary, corpus = load(name)
        L = {l: i for i, l in enumerate(labels)}
        dom = {s: d for n, s, d in res if n == name}
        for s, d in dom.items():
            rows += [(name, s, labels[i], t) for i, t in enumerate(d)]
        D = np.array([dom[s] for s in SEEDS])  # seeds x acts
        share = {(a, b): float(np.mean(D[:, a] == D[:, b])) for a, b in combinations(range(len(labels)), 2)}
        base = np.array(list(share.values()))
        med, p95 = np.median(base), np.percentile(base, 95)
        md += [f"## {name}", "",
               f"Baseline over {len(base)} act pairs: median {med:.3f}, 95th percentile {p95:.3f}, "
               f"max {base.max():.3f}; {int((base == 0).sum())} pairs never share a topic.", "",
               "| pairing | source | share of seeds | baseline median | baseline 95th pct | percentile rank |",
               "|---|---|---|---|---|---|"]
        for (a, b), src in [(p, "seed-42 pairing") for p in SEED42_PAIRS] + [(p, "21-seed run: most frequent") for p in EXTRA_PAIRS]:
            i, j = sorted((L[a], L[b]))
            v = share[(i, j)]
            pr = 100 * np.mean(base <= v)
            md.append(f"| {a} – {b} | {src} | {v:.3f} ({int(round(v * len(SEEDS)))}/{len(SEEDS)}) | {med:.3f} | {p95:.3f} | {pr:.1f} |")
        d42 = dom[42]
        own = sorted({tuple(sorted((labels[i], labels[j]))) for i in range(len(labels)) for j in range(len(labels))
                      if i != j and labels[i].startswith("Ece") and d42[i] == d42[j]})
        md += ["", f"This pipeline's own seed-42 pairings involving Ecerinis: "
               + ", ".join(f"{a}–{b}" for a, b in own), ""]

        # shared lemmas for the seed-42 pairings (and the two extra pairings, CSV only)
        vocab = set(dictionary.token2id)
        md += [f"### Shared content lemmas ({name})", "",
               "Lemmas present in both acts in the model input (after named-entity removal and the dictionary "
               "filter no_below=2, no_above=0.5); counts as act A / act B. 'Removed by the filter' = shared before the "
               "dictionary filter but not in the model vocabulary.", ""]
        for (a, b) in SEED42_PAIRS + EXTRA_PAIRS:
            ca, cb = Counter(lists[L[a]]), Counter(lists[L[b]])
            shared = sorted(set(ca) & set(cb), key=lambda w: (-(ca[w] + cb[w]), w))
            in_v = [w for w in shared if w in vocab]
            out_v = [w for w in shared if w not in vocab]
            for w in shared:
                lemma_rows.append({"pipeline": name, "pair": f"{a} – {b}", "lemma": w, "count_a": ca[w], "count_b": cb[w],
                                   "in_model_vocabulary": w in vocab})
            if (a, b) in SEED42_PAIRS:
                md.append(f"- **{a} – {b}**: {len(in_v)} shared in the model vocabulary"
                          + (": " + ", ".join(f"{w} {ca[w]}/{cb[w]}" for w in in_v) if in_v else "")
                          + f". Removed by the filter: {len(out_v)} more"
                          + (f" (most frequent: {', '.join(f'{w} {ca[w]}/{cb[w]}' for w in out_v[:8])})" if out_v else "") + ".")
        md.append("")
    pd.DataFrame(rows, columns=["pipeline", "seed", "act", "dominant_topic"]).to_csv(
        OUT / "acts_pairs_dominant.csv.gz", index=False)
    pd.DataFrame(lemma_rows).to_csv(OUT / "acts_pairs_shared_lemmas.csv", index=False, encoding="utf-8-sig")
    (OUT / "acts_pairs_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
