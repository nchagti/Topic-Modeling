"""Check that the new environment reproduces the saved seed-42 play-level results.

Reads (never writes) the pickles in gensimvenv/corpus_pkl/.
Writes results/a0_reproduction/reproduction_check.md.
"""
import pickle

import numpy as np

import pipeline as P

OLD = P.ROOT / "gensimvenv" / "corpus_pkl"
OUT = P.RESULTS / "a0_reproduction"


def load(name):
    with open(OLD / name, "rb") as f:
        return pickle.load(f)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    docs = P.load_docs("play")
    titles = [d["title"] for d in docs]
    tl = P.remove_named_entities(docs, P.load_named_entities())
    dictionary, corpus = P.build_corpus(tl)

    old_tl = load("filtered_token_lists.pkl")
    old_coh = load("filtered_coherences.pkl")
    old_ovl = load("filtered_mean_stabilities.pkl")
    old_tr = load("filtered_coh_sta_diffs.pkl")
    old_topics = load("filtered_LDA_topics.pkl")
    old_models = load("filtered_LDA_models.pkl")

    models, topics, scored, coh, ovl, tr = P.selection_grid(tl, dictionary, corpus, seed=42)
    coh_default = P.coherence_cv(models[8], tl, dictionary, processes=-1)

    lines = ["# Seed-42 reproduction check (play level)", ""]
    lines.append(f"- Token lists identical to saved `filtered_token_lists.pkl`: {tl == old_tl}")
    old_vocab = set(old_models[8].id2word.token2id)
    lines.append(f"- Dictionary identical to saved model's dictionary: {set(dictionary.token2id) == old_vocab} "
                 f"(new {len(dictionary)}, saved {len(old_vocab)})")
    lines.append(f"- Ecerinis tokens: {len(tl[titles.index('Ecerinis')])} after NE removal, "
                 f"{sum(c for _, c in corpus[titles.index('Ecerinis')])} after dictionary filter")
    lines.append(f"- c_v at k=8 with processes=1: {coh[scored.index(8)]:.10f}; default processes: {coh_default:.10f}")
    lines += ["", "| k | coherence (saved / new) | overlap (saved / new) | trade-off (saved / new) | top-10 lists identical |",
              "|---|---|---|---|---|"]
    for i, k in enumerate(scored):
        lines.append(f"| {k} | {old_coh[i]:.4f} / {coh[i]:.4f} | {old_ovl[i]:.4f} / {ovl[i]:.4f} | "
                     f"{old_tr[i]:.4f} / {tr[i]:.4f} | {old_topics[k] == topics[k]} |")
    max_abs = max(abs(a - b) for a, b in zip(old_tr, tr))
    lines += ["", f"- Max |trade-off difference|: {max_abs:.2e}"]
    lines.append(f"- Selected k (new): {scored[int(np.argmax(tr))]}")

    old_dt = P.doc_topic_matrix(old_models[8], corpus)
    new_dt = P.doc_topic_matrix(models[8], corpus)
    lines.append(f"- k=8 doc-topic max |difference| vs saved model: {np.abs(old_dt - new_dt).max():.2e}")
    lines += ["", "## k=8, new run: dominant topic per play (1-based)", ""]
    for t, row in zip(titles, new_dt):
        lines.append(f"- {t}: Topic {row.argmax() + 1} ({row.max():.3f})")
    rel = P.relevance_keywords(models[8], corpus)
    lines += ["", "## k=8 relevance keywords (lambda=0.6), new run", ""]
    for k, w in rel.items():
        lines.append(f"- Topic {k + 1}: {', '.join(w)}")

    (OUT / "reproduction_check.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
