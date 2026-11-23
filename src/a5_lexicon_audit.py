"""Audit of the theme lexicon v2 (data/theme_lexicon.json) against the v2 tokens.

Step 1 of context/theme_lexicon_v2_brief.md. No rates are computed here.

For every lemma in the lexicon:
  - count of tokens whose final v2 key is the lemma (src/v2_corpus.token_key: lemma
    fixes, named entities, spelling map applied), Ecerinis vs the ten Seneca plays;
  - tokens whose raw LatinCy 3.9.8 lemma is the lemma but whose final key is not, with
    the reason (removed as a name, stopword, approved lemma fix, spelling map,
    not kept by preprocessing);
  - tokens folded into the lemma from another raw lemma (lemma fixes, spelling map);
  - surface forms that Perseids Morpheus assigns to the lemma but v2 keys to something
    else ("forms elsewhere"; candidates = corpus forms sharing the lemma's first
    letters, checked with Morpheus; homographs are expected among them);
  - surface forms keyed to the lemma that Morpheus does not assign to it;
  - the lemma's surface forms in the corpus (participles under verbs etc.).
Also: lemmas with zero occurrences, lemmas listed in two families, and explicit checks
of the cases named in the brief (iussus/iubeo, natus/nascor, Furiae/Erinys, Parca).

Morpheus responses are cached in data/lexicon_cache/morpheus.json (src/lexicon.py).

Outputs: results/a5_lexicon_v2/lexicon_audit.md, audit_counts.csv, audit_forms_elsewhere.csv,
audit_forms_not_in_morpheus.csv
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict

import pandas as pd

import lexicon as LX
import normalize as N
import pipeline as P
import v2_corpus as V
from ne_final import is_name

OUT = P.RESULTS / "a5_lexicon_v2"
SEN = "Seneca"


def load_lexicon():
    lex = json.loads((P.DATA / "theme_lexicon.json").read_text(encoding="utf-8"))
    return {k: v for k, v in lex.items() if not k.startswith("_")}


def reason(t, play):
    """Why a token's raw lemma did not survive as its final key."""
    if not t["kept"]:
        return "not kept by preprocessing"
    raw = N.base_normalize(t["lemma"])
    k = V.fixed_key(t, play)
    if k is None:
        return "stopword or dropped"
    if is_name(k, t, play, V.named_entities()):
        return "removed as a name"
    final = V.variant_map().get(k, k)
    if k != raw:
        return f"lemma fix -> {final}"
    return f"spelling map -> {final}"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    lex = load_lexicon()
    fam_of = defaultdict(list)
    for f, ws in lex.items():
        for w in ws:
            fam_of[w].append(f)
    L = set(fam_of)
    docs = json.loads((P.DATA / "v2" / "plays_tokens.json").read_text(encoding="utf-8"))

    count = defaultdict(Counter)            # lemma -> {Ecerinis, Seneca}
    forms = defaultdict(Counter)            # lemma -> normalized surface -> n
    lost = defaultdict(Counter)             # raw lemma in L -> (reason, grp) -> n
    lost_forms = defaultdict(Counter)       # raw lemma in L -> surface forms lost
    folded = defaultdict(Counter)           # key in L, raw lemma differs -> (raw, grp) -> n
    form_key = defaultdict(Counter)         # query form -> (final key, grp) -> n
    query_of = {}                           # normalized surface -> query form (lowercase, original v)
    for d in docs:
        grp = "Ecerinis" if d["title"] == "Ecerinis" else SEN
        for t in d["tokens"]:
            k = V.token_key(t, d["title"])
            raw = N.base_normalize(t["lemma"])
            q = t["text"].lower()
            s = N.base_normalize(t["text"])
            query_of.setdefault(s, q)
            form_key[s][(k, grp)] += 1
            if k in L:
                count[k][grp] += 1
                forms[k][s] += 1
                if raw != k:
                    folded[k][(raw, grp)] += 1
            if raw in L and k != raw:
                lost[raw][(reason(t, d["title"]), grp)] += 1
                lost_forms[raw][t["text"]] += 1

    # candidate forms for "forms elsewhere": corpus forms sharing the lemma's opening letters
    def prefix(l):
        return l[:max(4, min(len(l) - 2, 6))] if len(l) > 4 else l[:3]

    cands = defaultdict(set)
    for l in L:
        p = prefix(l)
        for s, kc in form_key.items():
            if s.startswith(p) and l not in {k for k, _ in kc}:
                cands[l].add(s)
    keyed = {s for l in L for s in forms[l]}
    need = sorted({query_of[s] for s in set().union(*cands.values()) | keyed})
    morph = LX.morpheus(need)

    def heads(s):
        r = morph.get(query_of[s])
        return None if r is None else {LX.loose_key(LX.headword_key(h)) for h, _ in r}

    elsewhere, not_in_morph = [], []
    for l in sorted(L):
        lk = LX.loose_key(l)
        for s in sorted(cands[l]):
            h = heads(s)
            if h and lk in h:
                for (k, grp), n in form_key[s].items():
                    elsewhere.append({"lemma": l, "family": "; ".join(fam_of[l]), "form": s, "v2_key": k or "(removed)",
                                      "group": grp, "tokens": n, "morpheus": "; ".join(sorted(h))})
        for s, n in forms[l].items():
            h = heads(s)
            if h is not None and h and lk not in h:
                ece = form_key[s].get((l, "Ecerinis"), 0)
                not_in_morph.append({"lemma": l, "family": "; ".join(fam_of[l]), "form": s, "tokens": n,
                                     "ecerinis": ece, "morpheus": "; ".join(sorted(h))})
    ew = pd.DataFrame(elsewhere)
    nm = pd.DataFrame(not_in_morph)
    ew.to_csv(OUT / "audit_forms_elsewhere.csv", index=False, encoding="utf-8-sig")
    nm.to_csv(OUT / "audit_forms_not_in_morpheus.csv", index=False, encoding="utf-8-sig")

    rows = []
    for f, ws in lex.items():
        for w in ws:
            rows.append({"family": f, "lemma": w, "ecerinis": count[w]["Ecerinis"], "seneca": count[w][SEN],
                         "also_in": "; ".join(x for x in fam_of[w] if x != f),
                         "forms": "; ".join(f"{s} {n}" for s, n in forms[w].most_common(8)),
                         "lost_from_raw_lemma": "; ".join(f"{r} ({g}) {n}" for (r, g), n in lost[w].items()),
                         "folded_in": "; ".join(f"{r} ({g}) {n}" for (r, g), n in folded[w].items())})
    ct = pd.DataFrame(rows)
    ct.to_csv(OUT / "audit_counts.csv", index=False, encoding="utf-8-sig")

    # token-level counts by final key, for the named checks
    key_counts = defaultdict(Counter)
    for s, c in form_key.items():
        for (k, g), n in c.items():
            key_counts[k][g] += n

    def kv(k):
        return f"{k} {key_counts[k]['Ecerinis']} / {key_counts[k][SEN]}"

    def raw_check(raws):
        out = Counter()
        ex = defaultdict(Counter)
        for d in docs:
            grp = "Ecerinis" if d["title"] == "Ecerinis" else SEN
            for t in d["tokens"]:
                if N.base_normalize(t["lemma"]) in raws:
                    k = V.token_key(t, d["title"])
                    why = "kept as " + k if k else reason(t, d["title"])
                    out[(N.base_normalize(t["lemma"]), why, grp)] += 1
                    ex[(N.base_normalize(t["lemma"]), why)][t["text"]] += 1
        return out, ex

    md = ["# Theme lexicon v2: audit (step 1; no rates computed)", "",
          "Author-chosen word families (`data/theme_lexicon.json`; the earlier four-family lexicon is now "
          "`data/theme_lexicon_v1.json`). Counts are v2 tokens before the dictionary filter, by final lemma key "
          "(after lemma fixes, named-entity removal and the spelling map). Ecerinis / Seneca = the ten Seneca plays "
          "combined.", ""]
    zero = ct[(ct.ecerinis == 0) & (ct.seneca == 0)]
    dup = {w: fs for w, fs in fam_of.items() if len(fs) > 1}
    md += ["## Summary", "",
           f"- {len(ct)} lemmas in {len(lex)} families.",
           f"- Zero occurrences in the corpus ({len(zero)}): " + (", ".join(f"{r.lemma} ({r.family})" for r in zero.itertuples()) or "none") + ".",
           f"- Absent from Ecerinis but present in Seneca: {int(((ct.ecerinis == 0) & (ct.seneca > 0)).sum())} lemmas; "
           f"present in Ecerinis but absent from Seneca: {int(((ct.ecerinis > 0) & (ct.seneca == 0)).sum())}.",
           "- Listed in two families: " + ("; ".join(f"{w} ({', '.join(fs)})" for w, fs in dup.items()) or "none") + ".", ""]

    md += ["## Counts per family", ""]
    for f, ws in lex.items():
        sub = ct[ct.family == f]
        md += [f"### {f}", "", f"Family total: Ecerinis {sub.ecerinis.sum()} / Seneca {sub.seneca.sum()}.", "",
               "| lemma | Ecerinis | Seneca | surface forms (top 8) | notes |", "|---|---|---|---|---|"]
        for r in sub.itertuples():
            notes = []
            if r.lost_from_raw_lemma:
                notes.append("raw lemma lost: " + r.lost_from_raw_lemma)
            if r.folded_in:
                notes.append("folded in: " + r.folded_in)
            if r.also_in:
                notes.append("also in " + r.also_in)
            if r.ecerinis == 0 and r.seneca == 0:
                notes.append("**zero in corpus**")
            md.append(f"| {r.lemma} | {r.ecerinis} | {r.seneca} | {r.forms or '—'} | {'; '.join(notes)} |")
        md.append("")

    md += ["## Lemmatized differently", "",
           "### Forms Morpheus assigns to a listed lemma that v2 keys elsewhere", "",
           "Candidates are corpus forms that share the lemma's first letters; Morpheus confirms that the form can "
           "belong to the listed lemma. Many are homographs that v2 assigns correctly to the other lemma (e.g. *fata* "
           "from *for*); the reading is the author's call. Rows with 2 or more tokens (all rows in "
           "`audit_forms_elsewhere.csv`).", "",
           "| listed lemma | form | v2 key | Ecerinis | Seneca | Morpheus lemmas |", "|---|---|---|---|---|---|"]
    if len(ew):
        g = ew.pivot_table(index=["lemma", "form", "v2_key", "morpheus"], columns="group", values="tokens",
                           aggfunc="sum", fill_value=0).reset_index()
        for c in ("Ecerinis", SEN):
            if c not in g:
                g[c] = 0
        g["total"] = g.Ecerinis + g[SEN]
        for r in g[g.total >= 2].sort_values(["lemma", "total"], ascending=[True, False]).itertuples():
            md.append(f"| {r.lemma} | {r.form} | {r.v2_key} | {r.Ecerinis} | {getattr(r, SEN)} | {r.morpheus} |")
    md += ["", "### Forms keyed to a listed lemma that Morpheus does not assign to it", "",
           "Possible wrong lemma or a LatinCy convention; all rows (`audit_forms_not_in_morpheus.csv`).", "",
           "| listed lemma | form | tokens | of which Ecerinis | Morpheus lemmas |", "|---|---|---|---|---|"]
    for r in nm.sort_values(["lemma", "tokens"], ascending=[True, False]).itertuples() if len(nm) else []:
        md.append(f"| {r.lemma} | {r.form} | {r.tokens} | {r.ecerinis} | {r.morpheus} |")

    md += ["", "### Cases named in the brief and related conventions", ""]
    iub = Counter()
    for s, c in form_key.items():
        if s.startswith("iuss"):
            for (k, g), n in c.items():
                iub[(k, g)] += n
    md.append("- **iussus / iubeo.** Forms in *iuss-*: " + "; ".join(
        f"{k or '(removed)'} ({g}) {n}" for (k, g), n in sorted(iub.items(), key=lambda x: (str(x[0][0]), x[0][1]))) +
        f". Keys: {kv('iubeo')}; {kv('iussum')}; {kv('iussus')} (Ecerinis / Seneca).")
    nat = Counter()
    for s, c in form_key.items():
        if s.startswith("nat") and not s.startswith(("natur", "nato", "natan", "natat")):
            for (k, g), n in c.items():
                nat[(k, g)] += n
    md.append(f"- **natus / nascor.** Keys: {kv('natus')}; {kv('nata')}; {kv('nascor')}. Forms in *nat-* "
              "(excluding natura, nato, nat(at)o): " + "; ".join(
                  f"{k or '(removed)'} ({g}) {n}" for (k, g), n in sorted(nat.items(), key=lambda x: (-x[1], str(x[0][0])))[:10]) +
              ". *natus* is not in any family.")
    for raws, label in [({"furia", "furiae"}, "Furiae / furia"), ({"erinys", "erinyes", "erinnys"}, "Erinys"),
                        ({"parca", "parcae"}, "Parca"), ({"fortuna"}, "Fortuna"), ({"pontus"}, "Pontus"),
                        ({"nemesis"}, "Nemesis"), ({"fama"}, "Fama"), ({"ira"}, "Ira")]:
        out, ex = raw_check(raws)
        if not out:
            md.append(f"- **{label}.** No token with this raw lemma.")
            continue
        parts = [f"{why} ({g}) {n}" for (_, why, g), n in sorted(out.items(), key=lambda x: (x[0][1], x[0][2]))]
        exs = "; ".join(f"{why}: " + ", ".join(f"{w} {n}" for w, n in c.most_common(5)) for (_, why), c in ex.items())
        md.append(f"- **{label}.** " + "; ".join(parts) + f". Forms: {exs}.")
    md += [f"- **superi.** Keys: {kv('superi')}; {kv('superus')}; {kv('supernus')}. 3.9.8 keeps some substantive plurals "
           "(superi, inferi, manes) as their own lemmas.",
           f"- **aequus.** Keys: {kv('aequus')}; {kv('aequum')}; {kv('aequo')}; {kv('iniquus')}.",
           f"- **falsus.** Keys: {kv('falsus')}; {kv('falsum')}; {kv('fallo')}.",
           f"- **arma / armo.** Keys: {kv('arma')}; {kv('armo')}; {kv('armatus')}; {kv('armum')}.",
           f"- **insidiae.** Keys: {kv('insidiae')}; {kv('insidia')}; {kv('insidior')}.",
           f"- **uindex / uindico / uindicta.** Keys: {kv('uindex')}; {kv('uindico')}; {kv('uindicta')}; {kv('uendico')}.",
           f"- **planctus / plango.** Keys: {kv('planctus')}; {kv('plango')} (approved lemma fixes moved noun forms to planctus).",
           f"- **tyrannus / tyrannis.** Keys: {kv('tyrannus')}; {kv('tyrannis')}.",
           f"- **furor / furo / furia.** Keys: {kv('furor')}; {kv('furo')}; {kv('furia')}; {kv('furiae')}.",
           f"- **diuinus / diuus.** Keys: {kv('diuinus')}; {kv('diuus')}; {kv('diua')}.",
           f"- **caelum / caelestis / caelicola.** Keys: {kv('caelum')}; {kv('caelestis')}; {kv('caelicola')}.", ""]
    (OUT / "lexicon_audit.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
