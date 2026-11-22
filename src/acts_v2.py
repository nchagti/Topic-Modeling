"""Act-level documents for v2, cut from the play-level v2 parse.

Inputs from sources.py: data/v2/corpus_v2.json (play texts) and
data/v2/act_lines_v2.json (Ecerinis: the pinned TEI's act divisions; Seneca:
the old act files' lines).

The original act files (Acts/latin_tragedies_acts.json) were extracted
separately from the play texts and differ from them: Phaedra's 90-line
<div type="prelude"> ("Ite, umbrosas cingite silvas ...") is missing because
get_acts.py keeps only <div type="act">, and Ecerinis' acts come from a different
TEI version (missing passage, speaker labels, a line number, typos).

Here act boundaries are recovered by aligning the act files' verse lines to the
play text's lines; play lines with no match inherit the act of the preceding
matched line (lines before the first match go to act 1). The v2 play parse is
then split at those line boundaries, so both levels have identical text and
lemmas.
Outputs: data/v2/acts_tokens.json, results/a1_v2/acts_v2_report.md
"""
from __future__ import annotations

import bisect
import json
import re
from difflib import SequenceMatcher

import pandas as pd
import spacy
from spacy.tokens import DocBin

import pipeline as P

V2 = P.DATA / "v2"
OUT = P.RESULTS / "a1_v2"


def line_key(s: str) -> str:
    return re.sub(r"[^a-z]", "", s.lower().replace("v", "u").replace("j", "i"))


def main():
    corpus = json.loads((V2 / "corpus_v2.json").read_text(encoding="utf-8"))  # built by sources.py
    act_lines_v2 = json.loads((V2 / "act_lines_v2.json").read_text(encoding="utf-8"))
    acts = json.loads((P.ROOT / "Acts" / "latin_tragedies_acts.json").read_text(encoding="utf-8"))
    plays_tok = json.loads((V2 / "plays_tokens.json").read_text(encoding="utf-8"))
    docs = list(DocBin().from_disk(V2 / "plays_latincy398.spacy").get_docs(spacy.blank("la").vocab))

    out, rows = [], []
    for c, ptok, doc in zip(corpus, plays_tok, docs):
        play_acts = [a for a in acts if a["title"] == c["title"]]
        act_lines = [tuple(x) for x in act_lines_v2[c["title"]]]  # Ecerinis: TEI act divisions
        play_lines = c["text"].split("\n")
        sm = SequenceMatcher(None, [line_key(l) for l in play_lines],
                             [line_key(l) for _, l in act_lines], autojunk=False)
        line_act = [None] * len(play_lines)
        for blk in sm.get_matching_blocks():
            for i in range(blk.size):
                line_act[blk.a + i] = act_lines[blk.b + i][0]
        matched = sum(a is not None for a in line_act)
        first = next((a for a in line_act if a is not None), 1)
        cur, inherited = first, 0
        for i, a in enumerate(line_act):
            if a is None:
                if play_lines[i].strip():
                    inherited += 1
                line_act[i] = cur
            else:
                cur = a
        # LatinCy 3.9.8 rewrites the text (newlines -> spaces, -que split off,
        # v -> u), so each token is located in the source text in order, on
        # normalized spelling (lowercase, v->u, j->i; length-preserving).
        src = c["text"].lower().replace("v", "u").replace("j", "i")
        starts, pos = [], 0
        for l in c["text"].split("\n"):
            starts.append(pos)
            pos += len(l) + 1
        by_act = {}
        tok_by_i = {t["i"]: t for t in ptok["tokens"]}
        ptr, unplaced = 0, 0
        for t in doc:
            if t.i not in tok_by_i:
                continue
            needle = t.text.lower().replace("v", "u").replace("j", "i")
            hit = src.find(needle, ptr, ptr + 200) if needle else -1
            if hit < 0:
                unplaced += 1
                hit = ptr
            else:
                ptr = hit + len(needle)
            ln = bisect.bisect_right(starts, hit) - 1
            by_act.setdefault(line_act[ln], []).append(tok_by_i[t.i])
        if unplaced:
            print(f"{c['title']}: {unplaced} tokens not found in source; assigned to the current position")
        slug = play_acts[0]["play_slug"] if play_acts else c["title"].lower().replace(" ", "-")
        for a in sorted(by_act):
            out.append({"id": f"{slug}_act{a}", "play_slug": slug, "title": c["title"],
                        "author": c["author"], "act": a, "tokens": by_act[a]})
            old = next((x for x in acts if x["title"] == c["title"] and x["act"] == a), None)
            rows.append({"play": c["title"], "act": a,
                         "v2_kept_tokens": sum(t["kept"] for t in by_act[a]),
                         "old_act_text_lines": len([l for l in old["text"].split("\n") if l.strip()]) if old else 0,
                         "v2_lines": sum(1 for i, x in enumerate(line_act) if x == a and play_lines[i].strip())})
        rows.append({"play": c["title"], "act": "lines matched / inherited",
                     "v2_kept_tokens": None, "old_act_text_lines": matched, "v2_lines": inherited})
    (V2 / "acts_tokens.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    df = pd.DataFrame(rows)
    (OUT / "acts_v2_report.md").write_text(
        "# v2 act documents (cut from the play-level parse)\n\n"
        f"{len(out)} act documents.\n\n" + df.to_markdown(index=False) + "\n", encoding="utf-8")
    print(f"{len(out)} acts")
    print(df[df.act == "lines matched / inherited"].to_markdown(index=False))
    print(df[df.play.isin(["Phaedra", "Ecerinis"])].to_markdown(index=False))


if __name__ == "__main__":
    main()
