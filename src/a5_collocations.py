"""'Broken faith' collocations: fides / fidus near a verb of breaking, removing or neglecting.

An author-chosen collocation measure (context/lexicon_audit_decisions.md), kept
separate from the theme rates.

Input: the full v2 lemma sequence of each play (data/v2/plays_tokens.json), before
stopword and part-of-speech filtering: every token with a letter in it (punctuation
dropped; LatinCy's split-off enclitics such as -que count as tokens). Lemma = the
LatinCy 3.9.8 lemma, lowercase, v->u, j->i, with the approved lemma fixes (e.g.
negligo -> neglego) and spelling map applied; named entities are not removed.

Node lemmas: fides, fidus. Collocates: rumpo, frango, uiolo, absum, neglego, nego,
fallo, credo, iuro, sperno, laedo. Window: 5 tokens either side of the node, within
the same speech (TEI <sp>; src/verses.py). A hit = one node token with at least one
collocate in its window; all collocates in the window are listed.

Each hit is classified by hand (column `class`: broken / pledge / other). Classes
are read from data/lexicon_marks/collocation_hits_marked.csv if it exists, else
kept from an earlier results/a5_collocations/collocation_hits.csv, matched on
play, verse, node form and collocate forms, so a rerun never discards a class.
Reported as counts with the passages (automatic hits beside the hand classes),
not rates.

Outputs (results/a5_collocations/): collocations_summary.md, collocation_hits.csv,
collocations_plays.csv, collocations_acts.csv
"""
from __future__ import annotations

import json
import re
from collections import Counter

import pandas as pd

import normalize as N
import pipeline as P
import v2_corpus as V
import verses as VS

OUT = P.RESULTS / "a5_collocations"
NODES = {"fides", "fidus"}
COLLOCATES = ["rumpo", "frango", "uiolo", "absum", "neglego", "nego", "fallo", "credo", "iuro", "sperno", "laedo"]
CLASSES = ["broken", "pledge", "other"]
MATCH = ["play", "verse", "node_form", "collocate_forms"]
MARKED = P.DATA / "lexicon_marks" / "collocation_hits_marked.csv"
WINDOW = 5
EXPECTED = {"202": "negligens facti fidem", "320": "Absit fides", "472": "rupta fide",
            "480": "fides ... iuratas (vv. 480-481)"}
WORD = re.compile(r"[A-Za-z]")


def full_key(t, play):
    """Lemma for the full sequence: normalized, lemma fixes (no drops) and spelling map applied."""
    k = N.base_normalize(t["lemma"])
    specific, wide = V.lemma_fixes()
    surf = N.base_normalize(t["text"])
    f = specific.get((k, surf, play), specific.get((k, surf, ""), wide.get(k, k)))
    k = k if f == "<drop>" else f
    return V.variant_map().get(k, k)


def earlier_classes():
    for path in (MARKED, OUT / "collocation_hits.csv"):
        if path.exists():
            df = pd.read_csv(path, encoding="utf-8-sig", dtype=str).fillna("")
            if "class" in df and (df["class"].str.strip() != "").any():
                return {tuple(r[c] for c in MATCH): r["class"].strip().lower() for _, r in df.iterrows()}, path
    return {}, None


def count_table(hdf, by, order):
    rows = []
    for key in order:
        sub = hdf[hdf[by] == key]
        row = {by: key, "automatic hits": len(sub)}
        for c in CLASSES:
            row[c] = int((sub["class"] == c).sum())
        row["unclassified"] = int((sub["class"] == "").sum())
        row["passages"] = "; ".join(f"v. {r['verse']}" + (f" ({r['class']})" if r["class"] else "")
                                    for _, r in sub.iterrows())
        rows.append(row)
    return pd.DataFrame(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    docs = json.loads((P.DATA / "v2" / "plays_tokens.json").read_text(encoding="utf-8"))
    loc = VS.token_locations()
    vt = VS.verse_texts()
    hits, node_play = [], Counter()
    for d in docs:
        play = d["title"]
        seq = [(t, full_key(t, play), loc[play][t["i"]]) for t in d["tokens"] if WORD.search(t["text"])]
        for j, (t, k, l) in enumerate(seq):
            if k not in NODES:
                continue
            node_play[play] += 1
            rng = range(max(0, j - WINDOW), min(len(seq), j + WINDOW + 1))
            found = [(i, seq[i]) for i in rng
                     if i != j and seq[i][2]["speech"] == l["speech"] and seq[i][1] in COLLOCATES]
            if not found:
                continue
            labels = [x[2]["verse"] for _, x in found] + [l["verse"]]
            order = list(vt[play])
            lo, hi = min(order.index(v) for v in labels), max(order.index(v) for v in labels)
            span = order[max(0, lo - 1):hi + 2]
            hits.append({
                "play": play, "act": l["act"], "verse": l["verse"], "speaker": l["speaker"],
                "node": k, "node_form": t["text"],
                "collocates": "; ".join(sorted({x[1] for _, x in found})),
                "collocate_forms": "; ".join(f"{x[0]['text']} ({x[1]}, {i - j:+d}, v. {x[2]['verse']})"
                                             for i, x in found),
                "class": "",
                "window": " ".join(seq[i][0]["text"] for i in rng if seq[i][2]["speech"] == l["speech"]),
                "verses": f"{span[0]}-{span[-1]}",
                "verse_text": " / ".join(f"[{v}] {vt[play][v]}" for v in span)})
    hdf = pd.DataFrame(hits)
    old, src = earlier_classes()
    if old:
        hdf["class"] = [old.get(tuple(str(r[c]) for c in MATCH), "") for _, r in hdf.iterrows()]
    bad = sorted(set(hdf["class"]) - set(CLASSES) - {""})
    assert not bad, f"unknown classes {bad}"
    hdf.insert(0, "id", range(1, len(hdf) + 1))
    hdf.to_csv(OUT / "collocation_hits.csv", index=False, encoding="utf-8-sig")

    plays = [d["title"] for d in docs]
    hdf["act_label"] = [f"{VS.ABBR[p]} {a}" for p, a in zip(hdf.play, hdf.act)]
    ptab = count_table(hdf, "play", plays)
    ptab.insert(1, "fides/fidus tokens", [node_play[p] for p in plays])
    sen = ptab[ptab.play != "Ecerinis"]
    tot = {"play": "Seneca (10 plays combined)", "fides/fidus tokens": sen["fides/fidus tokens"].sum(),
           "automatic hits": sen["automatic hits"].sum(), **{c: sen[c].sum() for c in CLASSES},
           "unclassified": sen["unclassified"].sum(), "passages": ""}
    ptab = pd.concat([ptab, pd.DataFrame([tot])])
    ptab.to_csv(OUT / "collocations_plays.csv", index=False, encoding="utf-8-sig")
    atab = count_table(hdf, "act_label", list(dict.fromkeys(hdf.act_label))).rename(columns={"act_label": "act"})
    atab.to_csv(OUT / "collocations_acts.csv", index=False, encoding="utf-8-sig")

    ece = hdf[hdf.play == "Ecerinis"]
    marking = (f" (from `{src.relative_to(P.ROOT).as_posix()}`)." if src else
               "; not yet filled in: mark column `class` (Excel column J) in `collocation_hits.csv`.")
    md = ["# 'Broken faith' collocations (author-chosen collocation measure)", "",
          "**An author-chosen collocation measure, separate from the theme rates; not model output.** "
          f"Node *fides* / *fidus*; collocates {', '.join('*' + c + '*' for c in COLLOCATES)}; window ±{WINDOW} "
          "tokens within the same speech, on the full v2 lemma sequence (before stopword and part-of-speech "
          "filtering; punctuation dropped; lemma fixes and spelling map applied). A hit is a node token with at "
          "least one collocate in its window. Verse numbers are the TEI editions' (`src/verses.py`).", "",
          "Automatic hits are window matches; the hand classes (broken / pledge / other) are the author's reading "
          "of each hit" + marking + " Counts with the passages, not rates.", "",
          "## Per play", "", ptab.to_markdown(index=False), "",
          "## Per act (acts with at least one hit)", "", atab.to_markdown(index=False), "",
          "## Check: Ecerinis passages", ""]
    for v, desc in EXPECTED.items():
        ok = ece[(ece.verse == v) | ece.collocate_forms.str.contains(f"v. {v})", regex=False)]
        md.append(f"- v. {v} ({desc}): " + (
            "found (" + "; ".join(f"{r.node_form} v. {r.verse} + {r.collocate_forms}" for r in ok.itertuples()) + ")"
            if len(ok) else "**not found**"))
    md += ["", "## Every hit", "",
           "| id | act, verse | speaker | node | collocates (form, lemma, offset, verse) | class | verses |",
           "|---|---|---|---|---|---|---|"]
    for _, r in hdf.iterrows():
        md.append(f"| {r['id']} | {r['act_label']}, v. {r['verse']} | {r['speaker']} | {r['node_form']} | "
                  f"{r['collocate_forms']} | {r['class']} | {r['verse_text'].replace('|', '/')} |")
    (OUT / "collocations_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
