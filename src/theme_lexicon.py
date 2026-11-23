"""Theme lexicon v2: loading and the lexicon-only token rules.

data/theme_lexicon.json holds the author-chosen word families (keys not starting
with '_') and rules that apply to the lexicon counts only (the LDA input,
src/v2_corpus.token_key, is unchanged):

  _token_rules        a token whose final v2 key is `key` and whose surface form
                      (lowercase, v->u, j->i) is `surface` is counted under `to`
                      (null = not counted); e.g. vadum, which v2 lemmatizes as uas
  _marked_only        the key counts only for tokens the author marked y in the
                      given CSV (matched on play, verse and surface form); e.g. prodo
  _pos_only           the key counts only for tokens with this v2 part of speech
                      (foedus: NOUN, excluding the adjective 'foul')
  _exclude_prefixes   surface forms starting with these prefixes are not counted
                      under the key (superus: summus / supremus)
"""
from __future__ import annotations

import json
from functools import lru_cache

import pandas as pd

import normalize as N
import pipeline as P
import v2_corpus as V

LEXICON = P.DATA / "theme_lexicon.json"


@lru_cache(maxsize=1)
def raw():
    return json.loads(LEXICON.read_text(encoding="utf-8"))


def families():
    return {k: v for k, v in raw().items() if not k.startswith("_")}


@lru_cache(maxsize=1)
def token_rules():
    return {(r["key"], r["surface"]): r["to"] for r in raw().get("_token_rules", [])}


@lru_cache(maxsize=1)
def marked():
    """{key: {(play, verse, surface)}} of the tokens marked y."""
    out = {}
    for key, spec in raw().get("_marked_only", {}).items():
        df = pd.read_csv(P.ROOT / spec["file"], encoding="utf-8-sig", dtype=str).fillna("")
        y = df[df[spec["column"]].str.strip().str.lower() == "y"]
        out[key] = {(r.play, r.verse, N.base_normalize(r.form)) for r in y.itertuples()}
    return out


def lexicon_key(token: dict, play: str):
    """The key a token is counted under in the lexicon (None = not counted)."""
    k = V.token_key(token, play)
    if k is None:
        return None
    surf = N.base_normalize(token["text"])
    k = token_rules().get((k, surf), k)
    if k is None:
        return None
    pos = raw().get("_pos_only", {}).get(k)
    if pos and token["pos"] != pos["pos"]:
        return None
    ex = raw().get("_exclude_prefixes", {}).get(k)
    if ex and surf.startswith(tuple(ex["prefixes"])):
        return None
    if k in marked():
        import verses as VS
        verse = VS.token_locations()[play][token["i"]]["verse"]
        if (play, verse, surf) not in marked()[k]:
            return None
    return k
