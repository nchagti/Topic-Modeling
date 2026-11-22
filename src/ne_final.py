"""Final v2 named-entity decisions, and the functions the v2 corpus uses to apply
them and the approved lemma fixes.

Decision order for a kept token:
  1. a token-level override (data/v2/named_entity_token_overrides.csv) wins;
  2. else the approved context-reading recommendation for its lemma
     (data/v2/named_entities_recommendations.csv): name / word / split;
  3. else the evidence rule's decision (data/v2/named_entities_v2.csv).
"split" lemmas are names only where 3.9.8 tags that token PROPN or PERSON/LOC/NORP.
Writes data/v2/named_entities_final.json and results/a1_v2/named_entities_final.md.
"""
from __future__ import annotations

import json
from collections import Counter

import pandas as pd

import normalize as N
import pipeline as P

V2 = P.DATA / "v2"
OUT = P.RESULTS / "a1_v2"
ENT = {"PERSON", "LOC", "NORP"}


def load_lemma_fixes() -> dict[str, str]:
    df = pd.read_csv(V2 / "lemma_fixes_v2.csv", encoding="utf-8-sig")
    df = df[df.status.str.startswith("approved") & df.surface.isna() & df.play.isna()]
    return dict(zip(df.from_lemma, df.to_lemma))


def lemma_key(lemma: str, fixes: dict[str, str]) -> str:
    k = N.base_normalize(lemma)
    return fixes.get(k, k)


def build() -> dict:
    rule = pd.read_csv(V2 / "named_entities_v2.csv")
    rec = pd.read_csv(V2 / "named_entities_recommendations.csv")
    rec = rec[rec.approve.astype(str).str.lower().isin(["y", "yes", "true", "accept", "accepted"])]
    final = {r.lemma: r.decision.replace(" (flag)", "") for r in rule.itertuples()}
    final.update({r.lemma: r.recommendation for r in rec.itertuples()})
    add_path = V2 / "named_entities_additions.csv"  # names found in the lemma triage
    if add_path.exists():
        add = pd.read_csv(add_path, encoding="utf-8-sig")
        final.update({r.lemma: "name" for r in add.itertuples() if str(r.status).startswith("approved")})
    ov = pd.read_csv(V2 / "named_entity_token_overrides.csv")
    return {"names": sorted(l for l, d in final.items() if d == "name"),
            "split": sorted(l for l, d in final.items() if d == "split"),
            "token_overrides": [{"play": r.play, "i": int(r.i), "decision": r.decision} for r in ov.itertuples()]}


def is_name(key: str, token: dict, play: str, ne: dict, _cache={}) -> bool:
    if id(ne) not in _cache:
        _cache[id(ne)] = ({(o["play"], o["i"]): o["decision"] for o in ne["token_overrides"]},
                          set(ne["names"]), set(ne["split"]))
    ov, names, split = _cache[id(ne)]
    if (play, token["i"]) in ov:
        return ov[(play, token["i"])] == "name"
    if key in names:
        return True
    if key in split:
        return token["pos"] == "PROPN" or token["ent"] in ENT
    return False


def main():
    rec_path = V2 / "named_entities_recommendations.csv"
    rec = pd.read_csv(rec_path)
    if rec.approve.isna().all():  # user accepted all recommendations on 2026-11-21
        rec["approve"] = "y"
        rec.to_csv(rec_path, index=False, encoding="utf-8-sig")
    ne = build()
    (V2 / "named_entities_final.json").write_text(json.dumps(ne, ensure_ascii=False, indent=1), encoding="utf-8")

    import v2_corpus  # imported here: v2_corpus itself imports is_name from this module
    v2 = json.loads((V2 / "plays_tokens.json").read_text(encoding="utf-8"))
    removed, removed_ece, split_removed = Counter(), Counter(), Counter()
    lists, titles = [], []
    for r in v2:
        keep = []
        for t in r["tokens"]:
            k = v2_corpus.fixed_key(t, r["title"])  # all approved lemma fixes applied
            if k is None:
                continue
            if is_name(k, t, r["title"], ne):
                removed[k] += 1
                removed_ece[k] += r["title"] == "Ecerinis"
                if k in ne["split"]:
                    split_removed[k] += 1
            else:
                keep.append(k)
        lists.append(keep)
        titles.append(r["title"])
    i = titles.index("Ecerinis")
    dictionary, corpus = P.build_corpus(lists)
    md = ["# Final v2 named-entity decisions", "",
          f"- Names: {len(ne['names'])} lemmas; per-token (split): {len(ne['split'])} lemmas "
          f"({', '.join(ne['split'])}); token overrides: {len(ne['token_overrides'])}.",
          f"- Tokens removed as names: {sum(removed.values()):,} (Ecerinis {sum(removed_ece.values())}); "
          f"of these from split lemmas: {sum(split_removed.values())} ({dict(split_removed)}).",
          f"- Ecerinis after named-entity removal: {len(lists[i]):,} tokens; after the dictionary filter "
          f"(no_below=2, no_above=0.5): {sum(c for _, c in corpus[i]):,}. Dictionary size {len(dictionary):,}. "
          "(Lemma fixes applied; spelling map not applied here. Final token lists: token_lists_v2.md.)",
          "", "Most removed lemmas: " + ", ".join(f"{k} {v}" for k, v in removed.most_common(25))]
    (OUT / "named_entities_final.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
