"""Build the v2 source texts and record their provenance.

Ecerinis: extracted from the NeoLatDraCor TEI pinned at commit
3d4653db801eb2586c92cb918f6774bd0b079850 (data/sources/mussatus-ecerinis.xml,
CC0), all 654 verse lines including the 5 inside <stage> ("Sic fatus ..."),
with the corrections in data/sources/ecerinis_patches.json. Act boundaries come
from the TEI's <div type="act">.
Seneca: the text the analysis already uses (data/original/corpus/latin_tragedies_corpus.json)
is kept unchanged; act lines come from data/original/acts/latin_tragedies_acts.json (acts_v2.py
aligns them and assigns Phaedra's prelude to act 1). This script records how the
Seneca text compares with DraCor's current TEI and with the local TEI copies.

Outputs: data/v2/corpus_v2.json, data/v2/act_lines_v2.json,
results/a1_v2/sources_report.md
"""
from __future__ import annotations

import hashlib
import json
import re
import urllib.request
from difflib import SequenceMatcher
from pathlib import Path

from lxml import etree

import pipeline as P

V2 = P.DATA / "v2"
SRC = P.DATA / "sources"
OUT = P.RESULTS / "a1_v2"
NS = {"tei": "http://www.tei-c.org/ns/1.0"}
ECERINIS_TEI = SRC / "mussatus-ecerinis.xml"
ECERINIS_COMMIT = "3d4653db801eb2586c92cb918f6774bd0b079850"
ECERINIS_SHA256 = "60a9beb6d85c48d5a85321da30c917520b76bc23e6d456e79216f7aa741b7727"
LOCAL_TEI_DIR = Path(r"c:\Users\nchag\Dropbox\Nits\Syracuse\Ecerinis_DH\TEI\Seneca-Mussato-xmls")
DRACOR = "https://dracor.org/api/v1/corpora/rom/plays/{slug}/tei"


def norm(s: str) -> str:
    return " ".join(s.split())


def key(s: str) -> str:
    return re.sub(r"[^a-z]", "", s.lower().replace("v", "u").replace("j", "i"))


def tei_root(data: bytes):
    return etree.fromstring(data, etree.XMLParser(recover=True, remove_comments=True))


def verse_lines(root, within=None):
    base = within if within is not None else root.find(".//tei:body", NS)
    return [norm("".join(l.itertext())) for l in base.xpath(".//tei:l", namespaces=NS)]


def ecerinis():
    data = ECERINIS_TEI.read_bytes()
    assert hashlib.sha256(data).hexdigest() == ECERINIS_SHA256, "pinned Ecerinis TEI changed"
    root = tei_root(data)
    patches = json.loads((SRC / "ecerinis_patches.json").read_text(encoding="utf-8"))["patches"]
    acts = root.xpath(".//tei:body//tei:div[@type='act']", namespaces=NS)
    act_lines = [(i, l) for i, div in enumerate(acts, 1) for l in verse_lines(root, div)]
    all_lines = verse_lines(root)
    assert [l for _, l in act_lines] == all_lines, "verse lines outside act divisions"
    applied = []
    for p in patches:
        hits = [j for j, (_, l) in enumerate(act_lines) if p["find"] in l]
        assert len(hits) == 1, (p["find"], len(hits))
        a, l = act_lines[hits[0]]
        act_lines[hits[0]] = (a, l.replace(p["find"], p["replace"]))
        applied.append(f"line {hits[0] + 1}: '{p['find']}' -> '{p['replace']}' ({p['reason']})")
    stage = len(root.xpath(".//tei:body//tei:stage//tei:l", namespaces=NS))
    return act_lines, applied, stage


def compare(a_lines, b_lines):
    sm = SequenceMatcher(None, [key(l) for l in a_lines], [key(l) for l in b_lines], autojunk=False)
    return sum(b.size for b in sm.get_matching_blocks())


def main():
    V2.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    corpus = json.loads((P.ORIGINAL / "corpus" / "latin_tragedies_corpus.json").read_text(encoding="utf-8"))
    acts_old = json.loads((P.ORIGINAL / "acts" / "latin_tragedies_acts.json").read_text(encoding="utf-8"))

    ece_acts, applied, stage = ecerinis()
    old_ece = next(c for c in corpus if c["title"] == "Ecerinis")
    old_lines = [l for l in old_ece["text"].split("\n") if l.strip()]
    corpus_v2, act_lines_v2 = [], {}
    for c in corpus:
        if c["title"] == "Ecerinis":
            corpus_v2.append({"title": c["title"], "author": c["author"],
                              "text": "\n".join(l for _, l in ece_acts),
                              "source": f"NeoLatDraCor tei/mussatus-ecerinis.xml @ {ECERINIS_COMMIT}, patched"})
            act_lines_v2[c["title"]] = ece_acts
        else:
            corpus_v2.append({**c, "source": "data/original/corpus/latin_tragedies_corpus.json (unchanged)"})
            act_lines_v2[c["title"]] = [(a["act"], l) for a in acts_old if a["title"] == c["title"]
                                        for l in a["text"].split("\n") if l.strip()]
    (V2 / "corpus_v2.json").write_text(json.dumps(corpus_v2, ensure_ascii=False, indent=1), encoding="utf-8")
    (V2 / "act_lines_v2.json").write_text(json.dumps(act_lines_v2, ensure_ascii=False), encoding="utf-8")

    md = ["# v2 source texts", "",
          "## Ecerinis", "",
          f"- NeoLatDraCor `tei/mussatus-ecerinis.xml`, commit `{ECERINIS_COMMIT}` (CC0), "
          f"copy at `data/sources/mussatus-ecerinis.xml` (sha256 `{ECERINIS_SHA256[:16]}…`).",
          "- Text: MQDQ edition, after L. Padrin (ed.), *Ecerinide* (Bologna: Zanichelli, 1900), pp. 23–66.",
          f"- {len(ece_acts)} verse lines in {len({a for a, _ in ece_acts})} acts, including {stage} lines "
          "encoded inside `<stage>` (\"Sic fatus ima parte secessit domus …\").",
          "- Corrections applied (`data/sources/ecerinis_patches.json`):"] + [f"  - {x}" for x in applied]
    md += [f"- Compared with the text used so far (`data/original/corpus/latin_tragedies_corpus.json`): "
           f"{compare(old_lines, [l for _, l in ece_acts])} of {len(old_lines)} lines match ignoring case and "
           "punctuation; the old text capitalizes every line and reads 'Quadnam' for Quodnam.", ""]

    md += ["## Seneca (text unchanged; provenance check)", "",
           "| play | lines used | matching DraCor's current TEI | matching the local TEI copy (file) |",
           "|---|---|---|---|"]
    slug_of = {a["title"]: a["play_slug"] for a in acts_old}
    local = {p.name: p for p in LOCAL_TEI_DIR.glob("*.xml")} if LOCAL_TEI_DIR.exists() else {}
    for c in corpus:
        if c["title"] == "Ecerinis":
            continue
        lines = [l for l in c["text"].split("\n") if l.strip()]
        slug = slug_of.get(c["title"], "")
        try:
            req = urllib.request.Request(DRACOR.format(slug=slug), headers={"Accept": "application/xml"})
            d_lines = verse_lines(tei_root(urllib.request.urlopen(req, timeout=60).read()))
            d_match = f"{compare(lines, d_lines)} / {len(d_lines)}"
        except Exception as e:
            d_match = f"fetch failed ({type(e).__name__})"
        short = slug.replace("seneca-", "")
        lf = next((p for n, p in local.items() if short and short in n.lower()), None)
        if lf:
            l_lines = verse_lines(tei_root(lf.read_bytes()))
            l_match = f"{compare(lines, l_lines)} / {len(l_lines)} (`{lf.name}`)"
        else:
            l_match = "no local copy"
        md.append(f"| {c['title']} | {len(lines)} | {d_match} | {l_match} |")
    md += ["", "DraCor's live API is not versioned; the comparison records the state on the date this "
           "report was generated."]
    (OUT / "sources_report.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
