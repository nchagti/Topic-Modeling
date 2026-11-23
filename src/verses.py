"""Edition verse numbers, speeches and acts for every v2 token.

Verse numbers are the TEI editions' <l n="..."> values. The TEI numbers only every
fifth verse, and a verse shared between speakers is split into <l part="I|M|F">
pieces that carry one number. Each <l> is therefore numbered by counting verses
(a part="M" or part="F" piece continues the previous verse) and re-anchoring on
every explicit n. In the Ecerinis TEI this reproduces every n value except two
part indexes (n="1", n="2" on the part="M" pieces of v. 416), which are ignored.

The Seneca TEIs (DraCor) also mark every verse with <milestone unit="line" n>, which
carries the edition's number (transposed verses and 'b' verses included); those are
used where present, so Seneca verse labels are strings such as "286b".

Earlier reports cited the position of the line in data/v2/corpus_v2.json (one
line per <l> element, the five <stage> lines included). Those positions run ahead
of the verse numbers by the number of split-verse pieces before the line (25 in
Ecerinis; e.g. line 325 = v. 312).

Sources: Ecerinis = the pinned NeoLatDraCor TEI (data/sources/mussatus-ecerinis.xml,
the text v2 uses, so lines match one to one); Seneca = the DraCor TEI copies in
data/sources/seneca_tei/ (copied from TEI/Seneca-Mussato-xmls), aligned to the
corpus lines on normalized spelling (results/a1_v2/sources_report.md: all but 3
of 12,031 lines match). An unmatched corpus line takes the verse and speech of
the preceding matched line and is flagged approx=True.

Speech = the enclosing <sp>; the Ecerinis <stage> verses ("Sic fatus ...") form
their own unit. Act = the act of the token in data/v2/acts_tokens.json.
"""
from __future__ import annotations

import bisect
import json
import re
from difflib import SequenceMatcher
from functools import lru_cache

import spacy
from spacy.tokens import DocBin

import pipeline as P
import sources as S

V2 = P.DATA / "v2"
SENECA_TEI = P.DATA / "sources" / "seneca_tei"
TEI_FILE = {
    "Ecerinis": P.DATA / "sources" / "mussatus-ecerinis.xml",
    "Phoenissae": SENECA_TEI / "rom000015-seneca-phoenissae.tei.xml",
    "Troades": SENECA_TEI / "rom000016-seneca-troades.tei.xml",
    "Phaedra": SENECA_TEI / "rom000031-seneca-phaedra.tei.xml",
    "Agamemnon": SENECA_TEI / "rom000029-seneca-agamemnon.tei.xml",
    "Hercules Furens": SENECA_TEI / "seneca-hercules-furens.xml",
    "Medea": SENECA_TEI / "rom000005-seneca-medea.tei.xml",
    "Octavia": SENECA_TEI / "rom000030-seneca-octavia.tei.xml",
    "Oedipus": SENECA_TEI / "rom000002-seneca-oedipus.tei.xml",
    "Thyestes": SENECA_TEI / "seneca-thyestes.xml",
    "Hercules Oetaeus": SENECA_TEI / "rom000001-seneca-hercules-oetaeus.tei.xml",
}
ABBR = {"Ecerinis": "Ece", "Phoenissae": "Pho", "Troades": "Tro", "Phaedra": "Pha", "Agamemnon": "Aga",
        "Hercules Furens": "HF", "Medea": "Med", "Octavia": "Oct", "Oedipus": "Oed", "Thyestes": "Thy",
        "Hercules Oetaeus": "HO"}


def line_key(s: str) -> str:
    return re.sub(r"[^a-z]", "", s.lower().replace("v", "u").replace("j", "i"))


MILESTONE = "{http://www.tei-c.org/ns/1.0}milestone"


def tei_verses(path):
    """[(verse label, text, speech_id, speaker, part)] for every <l> in the body, plus diagnostics.

    Label: the <milestone unit="line" n> directly before the <l> (the Seneca TEIs mark every
    verse this way, transpositions and 'b' verses included; ed="exclude" only hides the number
    from display); otherwise a part="M"/"F" piece continues the previous verse; otherwise the
    <l n> value; otherwise the previous number + 1."""
    root = S.tei_root(path.read_bytes())
    sps = root.xpath(".//tei:body//tei:sp", namespaces=S.NS)
    sp_index = {id(sp): j for j, sp in enumerate(sps)}
    out, v, label, ignored, reanchored = [], 0, "0", [], []
    for el in root.xpath(".//tei:body//tei:l", namespaces=S.NS):
        part = el.get("part")
        prev = el.getprevious()
        ms = prev.get("n") if prev is not None and prev.tag == MILESTONE and prev.get("unit") == "line" else None
        n = el.get("n")
        if ms:
            label = ms
        elif part in ("M", "F") and v > 0:
            if n and n.isdigit() and abs(int(n) - v) > 3:
                ignored.append((v, n))          # part index, not a verse number
        elif n and n[:1].isdigit():
            if int(re.match(r"\d+", n).group()) != v + 1:
                reanchored.append((v + 1, n))
            label = n
        else:
            label = str(v + 1)
        v = int(re.match(r"\d+", label).group())
        sp = el.xpath("ancestor::tei:sp[1]", namespaces=S.NS)
        if sp:
            sid = f"sp{sp_index[id(sp[0])]}"
            who = sp[0].findtext("tei:speaker", namespaces=S.NS) or sp[0].get("who", "")
        else:
            st = el.xpath("ancestor::tei:stage[1]", namespaces=S.NS)
            sid = f"stage{id(st[0]) if st else 'x'}"
            who = "(stage)"
        out.append((label, S.norm("".join(el.itertext())), sid, " ".join(who.split()), part))
    return out, ignored, reanchored


@lru_cache(maxsize=1)
def play_lines():
    """{play: [dict(verse, speech, speaker, approx) per corpus line]} and diagnostics."""
    corpus = json.loads((V2 / "corpus_v2.json").read_text(encoding="utf-8"))
    res, diag = {}, {}
    for c in corpus:
        lines = c["text"].split("\n")
        tv, ignored, reanchored = tei_verses(TEI_FILE[c["title"]])
        sm = SequenceMatcher(None, [line_key(l) for l in lines], [line_key(t[1]) for t in tv], autojunk=False)
        info = [None] * len(lines)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            # equal blocks, and same-length replaced blocks (e.g. the patched Ecerinis lines), map one to one
            if op == "equal" or (op == "replace" and i2 - i1 == j2 - j1):
                for i in range(i2 - i1):
                    v, _, sid, who, part = tv[j1 + i]
                    info[i1 + i] = {"verse": v, "speech": sid, "speaker": who, "approx": False}
        unmatched = 0
        prev = {"verse": "0", "speech": "start", "speaker": "", "approx": True}
        for i, x in enumerate(info):
            if x is None:
                unmatched += 1
                info[i] = {**prev, "approx": True}
            else:
                prev = x
        res[c["title"]] = info
        diag[c["title"]] = {"lines": len(lines), "tei_l": len(tv), "unmatched": unmatched,
                            "ignored_n": ignored, "reanchored": reanchored, "last_verse": tv[-1][0]}
    return res, diag


@lru_cache(maxsize=1)
def verse_texts():
    """{play: {verse label: full verse text (split pieces joined with ' | ')}}, in TEI order."""
    out = {}
    for play, path in TEI_FILE.items():
        tv, _, _ = tei_verses(path)
        d = {}
        for v, text, *_ in tv:
            d[v] = f"{d[v]} | {text}" if v in d else text
        out[play] = d
    return out


def neighbours(play, verse, n=1):
    """Verse labels from n before to n after `verse`, in TEI order."""
    labels = list(verse_texts()[play])
    i = labels.index(verse)
    return labels[max(0, i - n):i + n + 1]


@lru_cache(maxsize=1)
def token_locations():
    """{play: {token i: dict(line, verse, speech, speaker, approx, act)}} for every token in plays_tokens.json."""
    corpus = json.loads((V2 / "corpus_v2.json").read_text(encoding="utf-8"))
    plays_tok = json.loads((V2 / "plays_tokens.json").read_text(encoding="utf-8"))
    acts = json.loads((V2 / "acts_tokens.json").read_text(encoding="utf-8"))
    docs = list(DocBin().from_disk(V2 / "plays_latincy398.spacy").get_docs(spacy.blank("la").vocab))
    lines_info, _ = play_lines()
    act_of = {}
    for a in acts:
        for t in a["tokens"]:
            act_of[(a["title"], t["i"])] = a["act"]
    out = {}
    for c, ptok, doc in zip(corpus, plays_tok, docs):
        # same token-placement procedure as acts_v2.py (LatinCy rewrites newlines and v/j)
        src = c["text"].lower().replace("v", "u").replace("j", "i")
        starts, pos = [], 0
        for l in c["text"].split("\n"):
            starts.append(pos)
            pos += len(l) + 1
        keep = {t["i"] for t in ptok["tokens"]}
        ptr, loc = 0, {}
        for t in doc:
            if t.i not in keep:
                continue
            needle = t.text.lower().replace("v", "u").replace("j", "i")
            hit = src.find(needle, ptr, ptr + 200) if needle else -1
            if hit < 0:
                hit = ptr
            else:
                ptr = hit + len(needle)
            ln = bisect.bisect_right(starts, hit) - 1
            loc[t.i] = {"line": ln + 1, **lines_info[c["title"]][ln], "act": act_of.get((c["title"], t.i))}
        out[c["title"]] = loc
    return out


def cite(play, loc):
    return f"{ABBR[play]} {loc['act']}, v. {loc['verse']}" + (" (approx.)" if loc["approx"] else "")


if __name__ == "__main__":
    _, diag = play_lines()
    for p, d in diag.items():
        print(p, {k: (v if not isinstance(v, list) else (len(v), v[:6])) for k, v in d.items()})
