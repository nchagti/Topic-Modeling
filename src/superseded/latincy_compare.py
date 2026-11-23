"""Does LatinCy 3.9.8 fix the lemma and NER errors found in the saved (old-build) lemmas?

Runs la_core_web_lg 3.9.8 on data/original/corpus/latin_tragedies_corpus.json, aligns its tokens
to the saved play-level DocBin (earlier build) by normalized surface text, and
reports:
  1. known lemma errors, scored against expected lemmas;
  2. entity tagging of ordinary words (scelus, urbs ...) and of Ecerinis' names;
  3. overall lemma agreement on the tokens the pipeline keeps.
Writes results/a1_normalization/latincy398_test.md and latincy398_play.spacy
(the 3.9.8 parse, kept for the later context checks). The analysis itself still
uses the saved lemmas; nothing here changes them.
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # src/ on the path
import json
from collections import Counter, defaultdict
from difflib import SequenceMatcher

import pandas as pd
import spacy
from spacy.tokens import DocBin

import normalize as N
import pipeline as P
import spacy_docs as S

OUT = P.RESULTS / "a1_normalization"
ENT = {"PERSON", "LOC", "NORP"}

# (label, surface forms, play or None, old POS or None, acceptable lemmas, basis)
CASES = [
    ("vindicem/vindices = vindex", {"vindicem", "vindices"}, None, "NOUN", {"uindex"}, "context checked"),
    ("ponti = pontus", {"ponti"}, None, None, {"pontus"}, "context checked (this run)"),
    ("manes = Manes", {"manes"}, None, None, {"manes"}, "context checked (sample, this run)"),
    ("pavit = pasco", {"pavit"}, None, None, {"pasco"}, "context checked"),
    ("tenere = teneo", {"tenere"}, None, "VERB", {"teneo"}, "context checked"),
    ("liqueris = linquo", {"liqueris"}, None, None, {"linquo"}, "context checked"),
    ("vitas = vito (Troades)", {"vitas"}, "Troades", None, {"uito"}, "context checked"),
    ("vitas = vita (Ecerinis)", {"vitas"}, "Ecerinis", None, {"uita"}, "context checked"),
    ("solo/soli = solum (old NOUN)", {"solo", "soli"}, None, "NOUN", {"solum"}, "context checked"),
    ("sate = sero (Ecerinis)", {"sate"}, "Ecerinis", None, {"sero"}, "context checked"),
    ("dire = dirus (Ecerinis)", {"dire"}, "Ecerinis", None, {"dirus"}, "context checked"),
    ("dest/desset = desum", {"dest", "desset"}, None, None, {"desum"}, "form unambiguous"),
    ("eversa/eversis/eversi = everto", {"eversa", "eversis", "eversi"}, None, None, {"euerto", "euersus"}, "form unambiguous"),
    ("invisum/inviso = invisus/invideo/inviso", {"invisum", "inviso"}, None, None, {"inuisus", "inuideo", "inuiso"}, "Morpheus candidates"),
    ("verbera = verber", {"verbera"}, None, None, {"uerber"}, "form unambiguous"),
    ("iuvenum/iuveni = iuvenis", {"iuvenum", "iuveni"}, None, None, {"iuuenis"}, "form unambiguous"),
    ("lare = lar", {"lare"}, None, None, {"lar"}, "form unambiguous"),
    ("puri = purus", {"puri"}, None, None, {"purus"}, "form unambiguous"),
    ("rati = reor", {"rati"}, None, None, {"reor"}, "form unambiguous"),
    ("vendicemus/vendicabo = vindico (Ecerinis)", {"vendicemus", "vendicabo"}, None, None, {"uindico"}, "Morpheus"),
    ("brevior = brevis", {"brevior"}, None, None, {"breuis"}, "form unambiguous"),
    ("leviore/leviora = levis", {"leviore", "leviora"}, None, None, {"leuis"}, "form unambiguous"),
    ("profare/speculare/gradere = deponents", {"profare", "speculare", "gradere"}, None, None, {"profor", "speculor", "gradior"}, "form unambiguous"),
    ("vasti = vastus", {"vasti"}, None, None, {"uastus"}, "form unambiguous"),
    ("invadam = invado", {"invadam"}, None, None, {"inuado"}, "form unambiguous"),
]
ORDINARY = ["scelus", "magnus", "peto", "mater", "animus", "mors", "caelum", "poena", "dolor",
            "ira", "furor", "urbs", "caedes", "pars", "ferrum", "flamma", "metus"]


def norm_text(s: str) -> str:
    return N.base_normalize(s)


def lem(t) -> str:
    return N.base_normalize(t.lemma_)


def align(old_doc, new_doc):
    a = [norm_text(t.text) for t in old_doc]
    b = [norm_text(t.text) for t in new_doc]
    sm = SequenceMatcher(None, a, b, autojunk=False)
    pairs = []
    for blk in sm.get_matching_blocks():
        for i in range(blk.size):
            pairs.append((old_doc[blk.a + i], new_doc[blk.b + i]))
    return pairs


def kwic(doc, i, w=6):
    return doc[max(0, i - w): i + w + 1].text


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    nlp = spacy.load("la_core_web_lg")
    version = nlp.meta["version"]
    corpus = json.loads((P.ORIGINAL / "corpus" / "latin_tragedies_corpus.json").read_text(encoding="utf-8"))
    titles = [c["title"] for c in corpus]
    new_docs = list(nlp.pipe([c["text"] for c in corpus], batch_size=1))
    db = DocBin(store_user_data=False)
    for d in new_docs:
        db.add(d)
    db.to_disk(OUT / "latincy398_play.spacy")
    old_docs = S.load_docbin("play")
    sw = S.load_stopwords()

    pairs_by_play = {t: align(o, n) for t, o, n in zip(titles, old_docs, new_docs)}
    md = [f"# LatinCy {version} vs the saved lemmas (earlier build)", "",
          "Tokens aligned by normalized surface text (lowercase, v->u, j->i). "
          f"Aligned tokens: {sum(len(p) for p in pairs_by_play.values()):,} of "
          f"{sum(len(d) for d in old_docs):,} old tokens.", ""]

    # ---- 1. known lemma errors ----
    rows, examples = [], defaultdict(list)
    for label, forms, play, opos, gold, basis in CASES:
        n = old_ok = new_ok = 0
        new_lemmas, old_lemmas = Counter(), Counter()
        for t, pairs in pairs_by_play.items():
            if play and t != play:
                continue
            for o, nw in pairs:
                if o.text.lower() in forms and (opos is None or o.pos_ == opos):
                    n += 1
                    old_ok += lem(o) in gold
                    new_ok += lem(nw) in gold
                    old_lemmas[lem(o) or "(empty)"] += 1
                    new_lemmas[lem(nw) or "(empty)"] += 1
                    if label.startswith(("ponti", "manes")) and len(examples[label]) < 12:
                        examples[label].append(f"{t}: ...{kwic(o.doc, o.i)}... [old {lem(o)}, new {lem(nw)}]")
        rows.append({"case": label, "tokens": n, "old correct": old_ok, "3.9.8 correct": new_ok,
                     "old lemmas": ", ".join(f"{k} {v}" for k, v in old_lemmas.most_common()),
                     "3.9.8 lemmas": ", ".join(f"{k} {v}" for k, v in new_lemmas.most_common()),
                     "basis": basis})
    cdf = pd.DataFrame(rows)
    md += ["## 1. Known lemma errors", "",
           f"Totals: old build correct on {cdf['old correct'].sum()} of {cdf.tokens.sum()} tokens; "
           f"3.9.8 correct on {cdf['3.9.8 correct'].sum()}.", "", cdf.to_markdown(index=False), ""]
    for label, ex in examples.items():
        md += [f"Contexts for '{label}' (to check the expected lemma):", ""] + [f"- {e}" for e in ex] + [""]

    # empty lemmas in the old build
    emp = Counter()
    for t, pairs in pairs_by_play.items():
        for o, nw in pairs:
            if o.is_alpha and o.lemma_ == "" and o.pos_ in S.KEEP_POS:
                emp["fixed (lemma differs from surface)" if lem(nw) and lem(nw) != norm_text(o.text) else
                    "surface form copied" if lem(nw) else "still empty"] += 1
    md += [f"- Old empty lemmas (content POS) under 3.9.8: {dict(emp)}", ""]

    # ---- 2. NER ----
    def ent_counts(pairs_iter, lemma_set):
        old, new, tot = Counter(), Counter(), Counter()
        for o, nw in pairs_iter:
            lo = o.lemma_.lower()
            if lo in lemma_set:
                tot[lo] += 1
                old[lo] += o.ent_type_ in ENT
                new[lo] += nw.ent_type_ in ENT
        return old, new, tot

    all_pairs = [p for ps in pairs_by_play.values() for p in ps]
    old, new, tot = ent_counts(all_pairs, set(ORDINARY))
    md += ["## 2. Entity tagging", "", "### Ordinary words tagged as entities (tokens tagged / occurrences)", "",
           "| lemma | occurrences | old build | 3.9.8 |", "|---|---|---|---|"]
    md += [f"| {w} | {tot[w]} | {old[w]} | {new[w]} |" for w in ORDINARY]
    share = pd.read_csv(P.DATA / "superseded" / "named_entities_share.csv")
    low = set(share.loc[~share["keep_as_named_entity_if_share>=0.5"], "lemma"])
    high = set(share.loc[share["keep_as_named_entity_if_share>=0.5"], "lemma"])
    o_low, n_low, t_low = ent_counts(all_pairs, low)
    o_hi, n_hi, t_hi = ent_counts(all_pairs, high)
    any_tag = lambda c: sum(1 for v in c.values() if v > 0)
    md += ["", f"- The 285 listed lemmas tagged < 50% of the time: lemmas tagged at least once "
           f"old {any_tag(o_low)}, 3.9.8 {any_tag(n_low)}; entity tokens old {sum(o_low.values())}, "
           f"3.9.8 {sum(n_low.values())} (of {sum(t_low.values())}).",
           f"- The 987 listed lemmas tagged >= 50% (mostly real names): entity tokens old "
           f"{sum(o_hi.values())}, 3.9.8 {sum(n_hi.values())} (of {sum(t_hi.values())}).",
           "- Under the NER notebook's rule (one tag anywhere puts a lemma on the list), a 3.9.8-built list "
           f"would still include {any_tag(n_low)} of the 285 ordinary-word lemmas.", ""]

    ece = titles.index("Ecerinis")
    diffs = Counter()
    for o, nw in pairs_by_play["Ecerinis"]:
        if o.is_alpha and ((o.ent_type_ in ENT) or (nw.ent_type_ in ENT) or o.pos_ == "PROPN" or nw.pos_ == "PROPN"):
            diffs[(o.text, o.ent_type_ or "-", nw.ent_type_ or "-", o.pos_, nw.pos_, lem(nw))] += 1
    md += ["### Ecerinis: tokens tagged as entities or PROPN by either build", "",
           "| surface | old entity | 3.9.8 entity | old POS | 3.9.8 POS | 3.9.8 lemma | n |", "|---|---|---|---|---|---|---|"]
    md += [f"| {s} | {oe} | {ne} | {op} | {np_} | {nl} | {c} |"
           for (s, oe, ne, op, np_, nl), c in sorted(diffs.items(), key=lambda x: (-x[1], x[0][0]))]
    ent_tot = {"old": sum(len(d.ents) for d in old_docs), "3.9.8": sum(len(d.ents) for d in new_docs)}
    md += ["", f"- Entity spans in the whole corpus: {ent_tot}", ""]

    # ---- 3. overall lemma agreement on kept tokens ----
    agree = n_kept = 0
    dis = Counter()
    for t, pairs in pairs_by_play.items():
        for o, nw in pairs:
            ol = S.CUSTOM_LOOKUPS.get(o.text, o.lemma_).lower()
            if o.is_alpha and ol not in sw and o.pos_ in S.KEEP_POS:
                n_kept += 1
                if N.base_normalize(ol) == lem(nw).lower():
                    agree += 1
                else:
                    dis[(N.base_normalize(ol), lem(nw).lower())] += 1
    md += ["## 3. Overall lemma agreement on the tokens the pipeline keeps", "",
           f"- Same lemma: {agree:,} of {n_kept:,} ({agree / n_kept:.1%}). "
           f"Distinct disagreement pairs: {len(dis):,}.", "",
           "Most frequent disagreements (old -> 3.9.8):", "",
           "| old | 3.9.8 | n |", "|---|---|---|"]
    md += [f"| {a or '(empty)'} | {b or '(empty)'} | {c} |" for (a, b), c in dis.most_common(60)]
    pd.DataFrame([{"old": a, "latincy398": b, "n": c} for (a, b), c in dis.most_common()]).to_csv(
        OUT / "latincy398_disagreements.csv", index=False, encoding="utf-8-sig")

    (OUT / "latincy398_test.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[:60]))


if __name__ == "__main__":
    main()
