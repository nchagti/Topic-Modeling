"""Turn the v2 (LatinCy 3.9.8) tokens into the token lists the topic models use.

For every token the preprocessing kept (content POS, not a stopword):
  1. lemma key = lowercase, v->u, j->i;
  2. approved lemma fixes (data/v2/lemma_fixes_v2.csv): surface/play-specific
     rows first, then lemma-wide rows; '<drop>' removes the token, and a fix that
     produces a stopword removes it too;
  3. named entities (src/ne_final.py: data/v2/named_entities_final.json) are removed;
  4. the approved spelling map (data/v2/variant_map_v2.json) is applied.
Used by every v2 model run, so all of them see the same tokens.
"""
from __future__ import annotations

import json
from functools import lru_cache

import pandas as pd

import normalize as N
import pipeline as P
from ne_final import is_name
from preprocess_v2 import stopwords_v2

V2 = P.DATA / "v2"


@lru_cache(maxsize=1)
def lemma_fixes():
    df = pd.read_csv(V2 / "lemma_fixes_v2.csv", encoding="utf-8-sig", dtype=str).fillna("")
    df = df[df.status.str.startswith("approved")]
    specific, wide = {}, {}
    for r in df.itertuples():
        frm, to = N.base_normalize(r.from_lemma), r.to_lemma.strip()
        to = to if to == "<drop>" else N.base_normalize(to)
        if r.surface or r.play:
            specific[(frm, N.base_normalize(r.surface), r.play)] = to
        else:
            wide[frm] = to
    return specific, wide


@lru_cache(maxsize=1)
def variant_map():
    m = json.loads((V2 / "variant_map_v2.json").read_text(encoding="utf-8-sig"))
    return {N.base_normalize(k): N.base_normalize(v) for k, v in m["map"].items()}


@lru_cache(maxsize=1)
def named_entities():
    return json.loads((V2 / "named_entities_final.json").read_text(encoding="utf-8-sig"))


@lru_cache(maxsize=1)
def stopwords():
    return frozenset(stopwords_v2())


def fixed_key(token: dict, play: str):
    """Lemma key after the approved lemma fixes (None if the token is dropped)."""
    if not token["kept"]:
        return None
    k = N.base_normalize(token["lemma"])
    specific, wide = lemma_fixes()
    surf = N.base_normalize(token["text"])
    k = specific.get((k, surf, play), specific.get((k, surf, ""), wide.get(k, k)))
    if k == "<drop>" or k in stopwords():
        return None
    return k


def token_key(token: dict, play: str):
    """The token's final lemma key, or None if the token is dropped."""
    k = fixed_key(token, play)
    if k is None:
        return None
    if is_name(k, token, play, named_entities()):
        return None
    return variant_map().get(k, k)


def token_lists(level: str = "play"):
    """[(doc_id, title, [lemma keys])] for 'play' (11 docs) or 'act' (56 docs)."""
    if level == "play":
        docs = json.loads((V2 / "plays_tokens.json").read_text(encoding="utf-8"))
        ids = [d["title"] for d in docs]
    else:
        docs = json.loads((V2 / "acts_tokens.json").read_text(encoding="utf-8"))
        ids = [d["id"] for d in docs]
    out = []
    for doc_id, d in zip(ids, docs):
        keys = [token_key(t, d["title"]) for t in d["tokens"]]
        out.append((doc_id, d["title"], [k for k in keys if k]))
    return out


def main():
    plays = token_lists("play")
    acts = token_lists("act")
    titles = [t for _, t, _ in plays]
    lists = [l for _, _, l in plays]
    dictionary, corpus = P.build_corpus(lists)
    i = titles.index("Ecerinis")
    act_totals = {}
    for _, t, l in acts:
        act_totals[t] = act_totals.get(t, 0) + len(l)
    assert all(act_totals[t] == len(l) for t, l in zip(titles, lists)), "play and act token counts differ"
    md = ["# v2 token lists (lemma fixes, named entities, spelling map applied)", "",
          "| play | tokens | after dictionary filter |", "|---|---|---|"]
    md += [f"| {t} | {len(l):,} | {sum(c for _, c in corpus[j]):,} |" for j, (t, l) in enumerate(zip(titles, lists))]
    md += ["", f"- Dictionary (no_below=2, no_above=0.5): {len(dictionary):,} types.",
           f"- Ecerinis: {len(lists[i]):,} tokens, {sum(c for _, c in corpus[i]):,} after the dictionary filter.",
           "- Act-level token lists add up to the play-level lists for every play."]
    (P.RESULTS / "a1_v2" / "token_lists_v2.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
