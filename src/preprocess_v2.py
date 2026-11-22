"""Reprocess the play texts with LatinCy 3.9.8 (robustness pipeline "v2").

The original pipeline (saved DocBins, earlier LatinCy build) stays untouched as
the conference baseline (tag v0.1-conference-2026).

Steps
1. Line-start lowercasing, same rule for every play: the first word of each
   verse line is lowercased unless that exact form is capitalized mid-line and
   mid-sentence (not after . ! ? : ;) somewhere in the corpus (a likely name). Ecerinis' TEI capitalizes every
   line (100% vs 7-21% in Seneca), which made LatinCy tag ordinary words as
   PROPN/PERSON. Every change is logged.
2. la_core_web_lg 3.9.8 (sha256 5b5ca107...fe72), plus the notebooks' custom
   lookups (inquit -> inquam, ablatus -> aufero).
Outputs (data/v2/): plays_latincy398.spacy, plays_tokens.json (every token with
surface, lemma, POS, entity type, kept flag); results/a1_v2/line_lowercasing.csv.
"""
from __future__ import annotations

import json
import re
from collections import Counter

import pandas as pd
import spacy
from spacy.tokens import DocBin

import normalize as N
import pipeline as P
import spacy_docs as S

V2 = P.DATA / "v2"
OUT = P.RESULTS / "a1_v2"
WORD = re.compile(r"[A-Za-z]+")
EXPECTED_VERSION = "3.9.8"


def stopwords_v2() -> set[str]:
    """Notebook stopword list, plus u/i-normalized spellings (3.9.8 lemmas are
    u-normalized). tenuis is excluded: it only matches after normalization and
    is a content adjective."""
    sw = S.load_stopwords()
    return (sw | {N.base_normalize(w) for w in sw}) - {"tenuis"}


def lowercase_line_starts(corpus):
    midcap = Counter()  # capitalized mid-line AND mid-sentence: evidence of a name
    for c in corpus:
        for line in c["text"].split("\n"):
            for m in list(WORD.finditer(line))[1:]:
                w = m.group(0)
                before = line[:m.start()].rstrip()
                if w[0].isupper() and not before.endswith((".", "!", "?", ":", ";")):
                    midcap[w] += 1
    log, out = [], []
    for c in corpus:
        new_lines = []
        for n, line in enumerate(c["text"].split("\n"), 1):
            m = WORD.search(line)
            if m and m.group(0)[0].isupper() and not m.group(0).isupper() and midcap[m.group(0)] == 0:
                w = m.group(0)
                line = line[:m.start()] + w.lower() + line[m.end():]
                log.append({"play": c["title"], "line": n, "word": w})
            new_lines.append(line)
        out.append({**c, "text": "\n".join(new_lines)})
    return out, pd.DataFrame(log)


def main():
    V2.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    nlp = spacy.load("la_core_web_lg")
    assert nlp.meta["version"] == EXPECTED_VERSION, nlp.meta["version"]
    corpus = json.loads((V2 / "corpus_v2.json").read_text(encoding="utf-8"))  # built by sources.py
    corpus_lc, log = lowercase_line_starts(corpus)
    log.to_csv(OUT / "line_lowercasing.csv", index=False, encoding="utf-8-sig")

    sw = stopwords_v2()
    docs = list(nlp.pipe([c["text"] for c in corpus_lc], batch_size=1))
    db = DocBin(store_user_data=False)
    records = []
    for c, d in zip(corpus_lc, docs):
        db.add(d)
        toks = []
        for t in d:
            if t.is_space:
                continue
            lemma = S.CUSTOM_LOOKUPS.get(t.text.lower(), t.lemma_)
            low = N.base_normalize(lemma)
            kept = t.is_alpha and low not in sw and t.pos_ in S.KEEP_POS
            toks.append({"i": t.i, "text": t.text, "lemma": lemma, "pos": t.pos_,
                         "ent": t.ent_type_, "kept": kept})
        records.append({"title": c["title"], "author": c["author"], "tokens": toks})
    db.to_disk(V2 / "plays_latincy398.spacy")
    (V2 / "plays_tokens.json").write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")

    rows = []
    for c, r in zip(corpus, records):
        k = [t for t in r["tokens"] if t["kept"]]
        rows.append({"play": c["title"], "lines_lowercased": int((log.play == c["title"]).sum()) if len(log) else 0,
                     "kept_tokens": len(k), "kept_PROPN": sum(t["pos"] == "PROPN" for t in k),
                     "entity_tokens": sum(t["ent"] in {"PERSON", "LOC", "NORP"} for t in r["tokens"]),
                     "empty_lemmas": sum(t["lemma"] == "" for t in k)})
    summary = pd.DataFrame(rows)
    (OUT / "preprocess_summary.md").write_text(
        f"# v2 preprocessing (LatinCy {nlp.meta['version']})\n\n" + summary.to_markdown(index=False) + "\n",
        encoding="utf-8")
    print(summary.to_markdown(index=False))


if __name__ == "__main__":
    main()
