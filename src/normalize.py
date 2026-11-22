"""A1 spelling normalization applied to LatinCy lemmas.

Order: lowercase -> v->u, j->i -> approved variant map (data/variant_map.json).
The same function is applied to the stopword list and named-entity list, so
filtering compares like with like.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import pipeline as P

VARIANT_MAP = P.DATA / "variant_map.json"


def base_normalize(s: str) -> str:
    return s.lower().replace("v", "u").replace("j", "i")


def load_variant_map(path: Path = VARIANT_MAP) -> dict[str, str]:
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {base_normalize(k): base_normalize(v) for k, v in raw.get("map", raw).items()}


def normalize(s: str, vmap: dict[str, str] | None = None) -> str:
    b = base_normalize(s)
    return vmap.get(b, b) if vmap else b


@lru_cache(maxsize=1)
def lemma_lookup() -> dict[str, str]:
    """LatinCy's form -> lemma table (la-latincy-lookups 1.0.0), u-spelling."""
    import la_latincy_lookups as L
    path = Path(L.__file__).parent / "data" / "la_lemma_lookup.json"
    return json.loads(path.read_text(encoding="utf-8"))


def lookup_lemma(form: str) -> str | None:
    t = lemma_lookup()
    for f in (form, base_normalize(form), form.lower(), base_normalize(form).capitalize()):
        if f in t:
            return t[f]
    return None


@lru_cache(maxsize=1)
def headwords() -> frozenset[str]:
    return frozenset(base_normalize(v) for v in lemma_lookup().values())
