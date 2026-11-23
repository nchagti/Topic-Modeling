"""v2 review scans on the LatinCy 3.9.8 lemmas (nothing applied).

1. Named-entity list rebuilt with an evidence rule:
     - LiLa lists the lemma only as proper_noun                -> name, unless
       3.9.8 mostly tags it ADJ/VERB (participles like tacitus, patiens, doctus
       collide with LiLa name entries)                          -> word (flag)
     - LiLa lists it as proper_noun AND noun/adj/verb: name if 3.9.8 tags it
       PERSON/LOC/NORP or PROPN in >= 50% of its kept occurrences, else word
       (flagged; personifications such as Fortuna land here)
     - not in LiLa: 3.9.8 tags it PERSON/LOC/NORP or PROPN in >= 50% of its
       kept occurrences                                         -> name
     - otherwise                                                -> word
2. Spelling-variant candidates on the v2 lemmas (same rules as the A1 scan).
3. Impact triage of validation_review.csv: which groups can change the LDA
   vocabulary (lemma or a Morpheus candidate occurs in 2-5 plays).
4. Ecerinis token funnel: original pipeline vs v2.
Outputs: data/v2/named_entities_v2.csv, results/a1_v2/variant_candidates_v2.csv,
results/a1_v2/validation_review_prioritized.csv, results/a1_v2/scan_v2.md
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict

import pandas as pd

import lexicon as L
import normalize as N
import pipeline as P
from superseded.a1_scan import RISKY, RULES

V2 = P.DATA / "v2"
OUT = P.RESULTS / "a1_v2"
ENT = {"PERSON", "LOC", "NORP"}


def k(lemma):
    return N.base_normalize(lemma)


def main():
    v2 = json.loads((V2 / "plays_tokens.json").read_text(encoding="utf-8"))
    titles = [r["title"] for r in v2]
    kept = {r["title"]: [t for t in r["tokens"] if t["kept"]] for r in v2}
    lila = L.lila_pos(sorted({k(t["lemma"]) for ts in kept.values() for t in ts}))

    # ---------- 1. named entities ----------
    n, ent, propn, ece, plays = Counter(), Counter(), Counter(), Counter(), defaultdict(set)
    surf, pos398 = defaultdict(Counter), defaultdict(Counter)
    for p, ts in kept.items():
        for t in ts:
            l = k(t["lemma"])
            n[l] += 1
            pos398[l][t["pos"]] += 1
            ent[l] += t["ent"] in ENT
            propn[l] += t["pos"] == "PROPN"
            ece[l] += p == "Ecerinis"
            plays[l].add(p)
            surf[l][t["text"]] += 1
    old_ne = P.load_named_entities()
    old_ne_b = {N.base_normalize(x) for x in old_ne}
    rows = []
    for l in n:
        pos = set(lila.get(l, []))
        share = max(ent[l], propn[l]) / n[l]
        main_pos = pos398[l].most_common(1)[0][0]
        if pos == {"proper_noun"} and main_pos in ("ADJ", "VERB"):
            dec, rule = "word (flag)", f"LiLa: proper noun only, but 3.9.8 tags it {main_pos} (participle/adjective homograph)"
        elif pos == {"proper_noun"}:
            dec, rule = "name", "LiLa: proper noun only"
        elif "proper_noun" in pos and share >= 0.5:
            dec, rule = "name", f"LiLa: proper noun and common word; 3.9.8 tags it as a name in {share:.0%}"
        elif "proper_noun" in pos:
            dec, rule = "word (flag)", f"LiLa: proper noun and common word; tagged as a name in {share:.0%}"
        elif not pos and share >= 0.5:
            dec, rule = "name", f"not in LiLa; 3.9.8 tags it as a name in {share:.0%}"
        elif not pos:
            dec, rule = "word", f"not in LiLa; tagged as a name in {share:.0%}"
        else:
            dec, rule = "word", "LiLa: common word only"
        if dec == "word" and share < 0.5 and l not in old_ne_b:
            continue  # ordinary word, never listed: omit from the review file
        rows.append({"lemma": l, "decision": dec, "rule": rule, "n": n[l], "ecerinis": ece[l],
                     "plays": len(plays[l]), "lila_pos": ", ".join(sorted(pos)),
                     "entity_or_propn_share": round(share, 2), "on_old_list": l in old_ne_b,
                     "surface_forms": ", ".join(f"{s} {c}" for s, c in surf[l].most_common(5)),
                     "approve": ""})
    ne = pd.DataFrame(rows).sort_values(["decision", "n"], ascending=[True, False])
    ne.to_csv(V2 / "named_entities_v2.csv", index=False, encoding="utf-8-sig")
    names = set(ne.loc[ne.decision == "name", "lemma"])

    # ---------- 2. variant candidates ----------
    by_play = {p: Counter(k(t["lemma"]) for t in ts) for p, ts in kept.items()}
    vocab = Counter()
    for c in by_play.values():
        vocab.update(c)
    groups = defaultdict(set)
    for name, fn in RULES.items():
        keyed = defaultdict(set)
        for w in vocab:
            if w not in names:
                keyed[fn(w)].add(w)
        for members in keyed.values():
            if len(members) > 1:
                groups[frozenset(members)].add(name)
    vrows = []
    for gid, (members, rules) in enumerate(sorted(groups.items(), key=lambda g: -sum(vocab[w] for w in g[0])), 1):
        both_lila = all(lila.get(w) for w in members)
        for w in sorted(members, key=lambda w: -vocab[w]):
            vrows.append({"group": gid, "rules": "; ".join(sorted(rules)), "form": w, "n_total": vocab[w],
                          "n_ecerinis": by_play["Ecerinis"][w], "lila_pos": ", ".join(lila.get(w, [])),
                          "note": "both in LiLa: may be distinct words" if both_lila and rules & RISKY else "",
                          "plays": ", ".join(f"{p} {c[w]}" for p, c in by_play.items() if c[w])})
    vdf = pd.DataFrame(vrows)
    vdf.to_csv(OUT / "variant_candidates_v2.csv", index=False, encoding="utf-8-sig")

    # ---------- 3. review triage ----------
    rev = pd.read_csv(OUT / "validation_review.csv")
    dfreq = {l: len(ps) for l, ps in plays.items()}

    def band(row):
        cands = [L.headword_key(c.split(" (")[0]) for c in str(row.morpheus_candidates).split("; ") if c and c != "nan"]
        ls = [row.lemma_398] + cands
        return any(2 <= dfreq.get(x, 0) <= 5 for x in ls)

    rev["affects_lda_vocab"] = rev.apply(band, axis=1)
    rev["priority"] = (rev.affects_lda_vocab | (rev.ecerinis > 0)) & ~rev.lemma_398.isin(names)
    rev = rev.sort_values(["priority", "n"], ascending=[False, False])
    rev.to_csv(OUT / "validation_review_prioritized.csv", index=False, encoding="utf-8-sig")

    # ---------- 4. Ecerinis funnel ----------
    def funnel(token_lists, title_list, ne_set):
        i = title_list.index("Ecerinis")
        tl = [[t for t in d if t not in ne_set] for d in token_lists]
        dictionary, corpus = P.build_corpus(tl)
        return len(token_lists[i]), len(tl[i]), sum(c for _, c in corpus[i]), len(dictionary)

    old_plays = P.load_docs("play")
    f_old = funnel([d["tokens"] for d in old_plays], [d["title"] for d in old_plays], old_ne)
    v2_lists = [[k(t["lemma"]) for t in kept[p]] for p in titles]
    f_v2 = funnel(v2_lists, titles, names)
    f_v2_oldrule = funnel(v2_lists, titles, {N.base_normalize(x) for x in old_ne})

    md = ["# v2 scans (LatinCy 3.9.8 lemmas)", "",
          "## Ecerinis token funnel (dictionary filter unchanged: no_below=2, no_above=0.5)", "",
          "| pipeline | content tokens | after named-entity removal | after dictionary filter | dictionary size |",
          "|---|---|---|---|---|",
          f"| original (saved lemmas, original list) | {f_old[0]:,} | {f_old[1]:,} | {f_old[2]:,} | {f_old[3]:,} |",
          f"| v2 lemmas, original list (normalized) | {f_v2_oldrule[0]:,} | {f_v2_oldrule[1]:,} | {f_v2_oldrule[2]:,} | {f_v2_oldrule[3]:,} |",
          f"| v2 lemmas, rebuilt list | {f_v2[0]:,} | {f_v2[1]:,} | {f_v2[2]:,} | {f_v2[3]:,} |", "",
          "No spelling map applied yet.", "",
          "## Named-entity list (`data/v2/named_entities_v2.csv`)", "",
          ne.groupby("decision").agg(lemmas=("lemma", "size"), tokens=("n", "sum"),
                                     ecerinis=("ecerinis", "sum")).to_markdown(), "",
          f"- Lemmas on the original list that the rebuilt list keeps as words: "
          f"{int(((ne.decision != 'name') & ne.on_old_list).sum())}.",
          "- Theme words: " + ", ".join(
              f"{w} → {ne.set_index('lemma').decision.get(w, 'word')}"
              for w in ["scelus", "poena", "urbs", "ira", "furor", "dolus", "crimen", "fortuna", "amor"]), "",
          "## Spelling-variant candidates (`variant_candidates_v2.csv`)", "",
          f"- {vdf.group.nunique() if len(vdf) else 0} candidate groups.", "",
          "## Validation review, prioritized (`validation_review_prioritized.csv`)", "",
          f"- {len(rev)} groups ({rev.n.sum():,} tokens). Priority (can change the LDA vocabulary or occur in "
          f"Ecerinis, and not a name): {int(rev.priority.sum())} groups, {int(rev[rev.priority].n.sum()):,} tokens."]
    (OUT / "scan_v2.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
