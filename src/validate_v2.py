"""Validate v2 (LatinCy 3.9.8) lemmas against LiLa and Morpheus, and score the
old build vs 3.9.8 where they disagree.

Per kept token:
  - LiLa: is the lemma a LiLa lemma?
  - Morpheus (only for questionable tokens: lemma not in LiLa, or the two builds
    disagree): is the lemma one of the analyses Morpheus gives for the form?
Writes results/a1_v2/validation.md, validation_review.csv (token groups that need
a decision) and disagreement_scores.csv.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from difflib import SequenceMatcher

import pandas as pd

import lexicon as L
import normalize as N
import pipeline as P
import spacy_docs as S

OUT = P.RESULTS / "a1_v2"


def key(lemma: str) -> str:
    return N.base_normalize(lemma)


def morph_ok(lemma, cands):
    if not cands:
        return None
    exact = {L.headword_key(h) for h, _ in cands}
    loose = {L.loose_key(L.headword_key(h)) for h, _ in cands}
    k = key(lemma)
    return "exact" if k in exact else "spelling variant" if L.loose_key(k) in loose else "no"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    v2 = json.loads((P.DATA / "v2" / "plays_tokens.json").read_text(encoding="utf-8"))
    titles = [r["title"] for r in v2]
    sw = S.load_stopwords()
    old_docs = S.load_docbin("play")

    # ---- align old kept tokens to v2 tokens ----
    pairs = []  # (play, old_surface, old_lemma, v2 token dict or None)
    old_kept_all = []
    for r, od in zip(v2, old_docs):
        a = [N.base_normalize(t.text) for t in od]
        b = [N.base_normalize(t["text"]) for t in r["tokens"]]
        sm = SequenceMatcher(None, a, b, autojunk=False)
        m = {}
        for blk in sm.get_matching_blocks():
            for i in range(blk.size):
                m[blk.a + i] = r["tokens"][blk.b + i]
        for t in od:
            ol = S.CUSTOM_LOOKUPS.get(t.text, t.lemma_).lower()
            if t.is_alpha and ol not in sw and t.pos_ in S.KEEP_POS:
                old_kept_all.append((r["title"], t.text, ol))
                pairs.append((r["title"], t.text, ol, m.get(t.i)))

    v2_kept = [(r["title"], t) for r in v2 for t in r["tokens"] if t["kept"]]

    # ---- LiLa ----
    lemmas = {key(t["lemma"]) for _, t in v2_kept} | {key(l) for _, _, l in old_kept_all}
    lila = L.lila_pos(sorted(lemmas))

    def lila_cov(items):
        types = {key(l) for l in items}
        return (sum(1 for l in types if lila.get(l)), len(types),
                sum(1 for l in items if lila.get(key(l))), len(items))

    cov_v2 = lila_cov([t["lemma"] for _, t in v2_kept])
    cov_old = lila_cov([l for _, _, l in old_kept_all])

    # ---- Morpheus for questionable tokens ----
    disagree = [(p, s, ol, t) for p, s, ol, t in pairs if t is not None and key(ol) != key(t["lemma"])]
    need = {t["text"].lower() for _, t in v2_kept if not lila.get(key(t["lemma"]))}
    need |= {s.lower() for _, s, _, _ in disagree}
    need |= {s.lower() for _, s, ol in old_kept_all if not lila.get(key(ol))}
    morph = L.morpheus(sorted(need))

    # ---- score disagreements ----
    score = Counter()
    drows = defaultdict(Counter)
    for p, s, ol, t in disagree:
        c = morph.get(s.lower())
        o, n = morph_ok(ol, c), morph_ok(t["lemma"], c)
        if c is None:
            cls = "Morpheus query failed"
        elif not c:
            cls = "Morpheus has no analysis"
        else:
            ov, nv = o != "no", n != "no"
            cls = ("both valid" if ov and nv else "only 3.9.8 valid" if nv else
                   "only old build valid" if ov else "neither valid")
        score[cls] += 1
        drows[(key(ol), key(t["lemma"]), cls)][p] += 1
    ddf = pd.DataFrame([{"old": a, "latincy398": b, "class": c, "n": sum(v.values()),
                         "plays": ", ".join(f"{k} {x}" for k, x in v.items())}
                        for (a, b, c), v in drows.items()]).sort_values("n", ascending=False)
    ddf.to_csv(OUT / "disagreement_scores.csv", index=False, encoding="utf-8-sig")

    # ---- per-token status for v2 ----
    status = Counter()
    review = defaultdict(lambda: {"n": 0, "plays": Counter()})
    ece_status = Counter()
    for p, t in v2_kept:
        k = key(t["lemma"])
        in_lila = bool(lila.get(k))
        c = morph.get(t["text"].lower()) if t["text"].lower() in need else None
        mo = morph_ok(t["lemma"], c) if c else None
        if in_lila and mo in (None, "exact", "spelling variant"):
            st = "ok"
        elif not in_lila and mo in ("exact", "spelling variant"):
            st = "ok (not in LiLa; Morpheus confirms)"
        elif mo == "no":
            st = "review: Morpheus rejects lemma for this form"
        elif not in_lila and t["pos"] == "PROPN":
            st = "unverified proper noun (in neither resource)"
        else:
            st = "review: lemma in neither resource"
        status[st] += 1
        if p == "Ecerinis":
            ece_status[st] += 1
        if st.startswith("review"):
            g = review[(t["text"].lower(), k, t["pos"], st)]
            g["n"] += 1
            g["plays"][p] += 1
            g["cands"] = "; ".join(f"{h} ({pos})" for h, pos in (c or []))
            g["lila"] = ", ".join(lila.get(k, []))
    rdf = pd.DataFrame([{"surface": s, "lemma_398": k, "pos_398": pos, "status": st, "n": g["n"],
                         "ecerinis": g["plays"]["Ecerinis"], "morpheus_candidates": g.get("cands", ""),
                         "lila_pos_of_lemma": g.get("lila", ""),
                         "plays": ", ".join(f"{a} {b}" for a, b in g["plays"].items()), "decision": ""}
                        for (s, k, pos, st), g in review.items()]).sort_values("n", ascending=False)
    rdf.to_csv(OUT / "validation_review.csv", index=False, encoding="utf-8-sig")

    tot_dis = sum(score.values())
    md = ["# v2 lemma validation (LatinCy 3.9.8 vs LiLa and Morpheus)", "",
          "## LiLa coverage of kept lemmas", "",
          "| pipeline | lemma types in LiLa | tokens whose lemma is in LiLa |", "|---|---|---|",
          f"| old build (saved) | {cov_old[0]:,} / {cov_old[1]:,} ({cov_old[0] / cov_old[1]:.1%}) | "
          f"{cov_old[2]:,} / {cov_old[3]:,} ({cov_old[2] / cov_old[3]:.1%}) |",
          f"| v2 (3.9.8, line starts lowercased) | {cov_v2[0]:,} / {cov_v2[1]:,} ({cov_v2[0] / cov_v2[1]:.1%}) | "
          f"{cov_v2[2]:,} / {cov_v2[3]:,} ({cov_v2[2] / cov_v2[3]:.1%}) |", "",
          "## Where the two builds disagree (kept tokens, scored by Morpheus)", "",
          f"{tot_dis:,} aligned kept tokens have different lemmas. Morpheus lists the possible lemmas for each "
          "surface form; a lemma counts as valid if it is among them (spelling variants such as "
          "coniunx/coniux count as valid).", "",
          "| class | tokens | share |", "|---|---|---|"]
    md += [f"| {k} | {v:,} | {v / tot_dis:.1%} |" for k, v in score.most_common()]
    md += ["", "Largest groups per class: `disagreement_scores.csv`.", "",
           "## Status of every v2 kept token", "",
           "| status | tokens | Ecerinis |", "|---|---|---|"]
    md += [f"| {k} | {v:,} | {ece_status[k]:,} |" for k, v in status.most_common()]
    md += ["", f"Token groups needing a decision: {len(rdf):,} (`validation_review.csv`), "
           f"covering {rdf.n.sum():,} tokens; {int((rdf.ecerinis > 0).sum())} groups occur in Ecerinis.", ""]
    for cls in ["only old build valid", "only 3.9.8 valid", "neither valid"]:
        sub = ddf[ddf["class"] == cls].head(15)
        md += [f"### Top '{cls}' groups", "", sub[["old", "latincy398", "n"]].to_markdown(index=False), ""]
    (OUT / "validation.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
