"""Do the play-level (earlier build) and act-level (3.8.0) LatinCy runs agree?

1. Re-derives processed tokens from each DocBin and checks they equal the
   saved processed_corpus.pkl / processed_acts.pkl.
2. Concatenates each play's acts and aligns them token by token against the
   play-level doc, then counts lemma and POS disagreements between builds.
Writes results/a1_normalization/build_comparison.md and build_disagreements.csv.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # src/ on the path
from collections import Counter, defaultdict
from difflib import SequenceMatcher

import pandas as pd

import pipeline as P
import spacy_docs as S

OUT = P.RESULTS / "a1_normalization"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sw = S.load_stopwords()
    plays, acts = P.load_docs("play"), P.load_docs("act")
    play_docs, act_docs = S.load_docbin("play"), S.load_docbin("act")
    lines = ["# LatinCy build comparison: play level (earlier build) vs act level (3.8.0)", ""]

    play_ok = [[l for _, l, _ in S.kept_tokens(d, sw)] == p["tokens"] for d, p in zip(play_docs, plays)]
    act_ok = [[l for _, l, _ in S.kept_tokens(d, sw)] == a["tokens"] for d, a in zip(act_docs, acts)]
    lines.append(f"- Play DocBin reproduces processed_corpus.pkl: {sum(play_ok)}/{len(play_ok)} plays")
    lines.append(f"- Act DocBin reproduces processed_acts.pkl: {sum(act_ok)}/{len(act_ok)} acts")
    lines.append("")

    acts_by_title = defaultdict(list)
    for d, a in zip(act_docs, acts):
        acts_by_title[a["title"]].append(d)

    rows, summary = [], []
    for pdoc, p in zip(play_docs, plays):
        a_toks = [t for d in acts_by_title[p["title"]] for t in d]
        p_toks = list(pdoc)
        sm = SequenceMatcher(None, [t.text for t in p_toks], [t.text for t in a_toks], autojunk=False)
        aligned = lemma_diff = pos_diff = 0
        for blk in sm.get_matching_blocks():
            for i in range(blk.size):
                tp, ta = p_toks[blk.a + i], a_toks[blk.b + i]
                aligned += 1
                if tp.lemma_ != ta.lemma_ or tp.pos_ != ta.pos_:
                    lemma_diff += tp.lemma_ != ta.lemma_
                    pos_diff += tp.pos_ != ta.pos_
                    rows.append({"play": p["title"], "surface": tp.text,
                                 "lemma_play_build": tp.lemma_, "pos_play_build": tp.pos_,
                                 "lemma_act_build": ta.lemma_, "pos_act_build": ta.pos_})
        kept_p = Counter(p["tokens"])
        kept_a = Counter(t for a in acts if a["title"] == p["title"] for t in a["tokens"])
        summary.append({"play": p["title"], "play_tokens": len(p_toks), "act_tokens": len(a_toks),
                        "aligned": aligned, "lemma_diffs": lemma_diff, "pos_diffs": pos_diff,
                        "kept_tokens_play": sum(kept_p.values()), "kept_tokens_acts": sum(kept_a.values()),
                        "kept_count_L1_diff": sum(((kept_p - kept_a) + (kept_a - kept_p)).values())})

    sdf = pd.DataFrame(summary)
    lines.append(sdf.to_markdown(index=False))
    lines += ["", f"- Total lemma disagreements on aligned tokens: {sdf.lemma_diffs.sum()} "
              f"of {sdf.aligned.sum()} ({sdf.lemma_diffs.sum() / sdf.aligned.sum():.2%})",
              f"- Total POS disagreements: {sdf.pos_diffs.sum()}"]
    ddf = pd.DataFrame(rows)
    ddf.to_csv(OUT / "build_disagreements.csv", index=False, encoding="utf-8")
    if len(ddf):
        top = ddf.groupby(["surface", "lemma_play_build", "lemma_act_build"]).size().sort_values(ascending=False).head(25)
        lines += ["", "## Most frequent disagreements", "", top.reset_index(name="n").to_markdown(index=False)]
    (OUT / "build_comparison.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
