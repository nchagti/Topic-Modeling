"""Cached clients for two independent Latin lexical resources.

LiLa lemma bank (https://lila-erc.eu, SPARQL): does a lemma exist, and with
which parts of speech (noun / verb / adjective / proper_noun ...)?
Perseids Morpheus (https://morph.perseids.org): which lemmas can a surface form
belong to?

Only Latin words are sent. Every response is cached in data/lexicon_cache/
(lila.json, morpheus.json), so later runs and reviewers can rerun the checks
offline and see the evidence.
"""
from __future__ import annotations

import json
import re
import threading
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import pipeline as P

CACHE = P.DATA / "lexicon_cache"
LILA_EP = "https://lila-erc.eu/sparql/lila_knowledge_base/sparql"
MORPH_EP = "https://morph.perseids.org/analysis/word"
_lock = threading.Lock()


def _load(name):
    p = CACHE / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def _save(name, data):
    CACHE.mkdir(parents=True, exist_ok=True)
    (CACHE / name).write_text(json.dumps(data, ensure_ascii=False, indent=0, sort_keys=True), encoding="utf-8")


def _get(url, accept=None, tries=4):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"Accept": accept} if accept else {})
            return urllib.request.urlopen(req, timeout=60).read()
        except Exception:
            if k == tries - 1:
                raise
            time.sleep(2 * (k + 1))


def lila_pos(lemmas, batch=150) -> dict[str, list[str]]:
    """lemma -> sorted list of LiLa POS labels ([] = not in LiLa). Lemmas are
    matched exactly, lowercase, u-spelling (LiLa's convention)."""
    cache = _load("lila.json")
    todo = sorted({l for l in lemmas if l and l not in cache})
    for i in range(0, len(todo), batch):
        chunk = todo[i:i + batch]
        vals = " ".join('"' + l.replace('"', "") + '"@la' for l in chunk)
        q = ("PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#> "
             "PREFIX lila: <http://lila-erc.eu/ontologies/lila/> "
             f"SELECT ?w ?pos WHERE {{ VALUES ?w {{ {vals} }} ?l a lila:Lemma ; "
             "ontolex:writtenRep ?w ; lila:hasPOS ?pos . }")
        url = LILA_EP + "?" + urllib.parse.urlencode({"query": q, "format": "json"})
        res = json.loads(_get(url, "application/sparql-results+json"))["results"]["bindings"]
        found = {l: set() for l in chunk}
        for b in res:
            found[b["w"]["value"]].add(b["pos"]["value"].rsplit("/", 1)[-1])
        for l, s in found.items():
            cache[l] = sorted(s)
        _save("lila.json", cache)
    return {l: cache.get(l, []) for l in lemmas}


def _morph_one(word):
    url = MORPH_EP + "?" + urllib.parse.urlencode({"lang": "lat", "engine": "morpheuslat", "word": word})
    d = json.loads(_get(url))
    body = d["RDF"]["Annotation"].get("Body", [])
    if isinstance(body, dict):
        body = [body]
    out = set()
    for b in body:
        e = b.get("rest", {}).get("entry", {})
        dw = e.get("dict", {})
        hw = dw.get("hdwd", {}).get("$")
        if hw:
            out.add((hw, dw.get("pofs", {}).get("$", "")))
    return sorted(out)


def morpheus(words, workers=4) -> dict[str, list[list[str]]]:
    """surface form -> [[headword, pos], ...] ([] = Morpheus has no analysis)."""
    cache = _load("morpheus.json")
    todo = sorted({w for w in words if w and w not in cache})

    def work(w):
        try:
            r = _morph_one(w)
        except Exception:
            return w, None
        with _lock:
            cache[w] = r
            if len(cache) % 200 == 0:
                _save("morpheus.json", cache)
        return w, r

    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(work, todo))
    _save("morpheus.json", cache)
    return {w: cache.get(w) for w in words}


def headword_key(hw: str) -> str:
    """Morpheus headword -> comparable lemma: lowercase, u/i spelling, homograph digits removed."""
    return re.sub(r"\d+$", "", hw).lower().replace("v", "u").replace("j", "i")


def loose_key(lemma: str) -> str:
    """Spelling-tolerant key for comparing headwords across lexicons
    (coniunx/coniux, exsul/exul, humerus/umerus, bracchium/brachium)."""
    k = lemma.lower().replace("v", "u").replace("j", "i")
    k = k.replace("exs", "ex").replace("nx", "x").replace("h", "").replace("y", "i")
    return re.sub(r"(.)\1", r"\1", k)
