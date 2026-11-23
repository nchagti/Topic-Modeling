"""Theme lexicon v2, revised audit (context/lexicon_audit_decisions.md).

Recounts the families the decisions changed, with the lexicon-only token rules
(src/theme_lexicon.py), and lists the tokens the author will sense-check:
every prodo token (plus Ecerinis 'prodit', which v2 lemmatizes as prodeo),
every uendo token, every uendico token (kept separate), and the Ecerinis fingo
tokens. Verses are the TEI editions' verse numbers (src/verses.py).

Counts are v2 tokens before the dictionary filter, by final lemma key, as in the
step 1 audit (results/a5_lexicon_v2/lexicon_audit.md, which used the
pre-decision lexicon and is kept as the record of step 1). The rate shown
beside each count is family tokens per 1,000 v2 tokens (the denominator used
by the rate scripts); families with fewer than 5 Ecerinis tokens are flagged
as thin.

Outputs (results/a5_lexicon_v2/): lexicon_audit_revised.md, audit_counts_revised.csv,
prodo_tokens.csv, uendo_tokens.csv (with uendico rows), fingo_ecerinis.csv
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict

import pandas as pd

import normalize as N
import pipeline as P
import theme_lexicon as TL
import v2_corpus as V
import verses as VS

OUT = P.RESULTS / "a5_lexicon_v2"
SEN = "Seneca"
THIN = 5
CHANGED = {
    "deceit_betrayal": "replaces deceit and betrayal_broken_faith; adds astus, transfuga; prodo and uendo only where marked y; foedus nouns only",
    "providence_divine": "adds superus (super- forms only), diuus, diua; excludes diti, dites from deus",
    "lineage_kin": "adds natus, nata",
    "grief_lament": "adds fletus",
    "rage_fury": "adds furia; excludes furabor from furor",
    "discord_strife": "adds rebellis",
    "sea_water": "uadum counts the vadum tokens v2 lemmatizes as uas",
}


def context_rows(docs, loc, select):
    vt = VS.verse_texts()
    rows = []
    for d in docs:
        play = d["title"]
        for t in d["tokens"]:
            why = select(t, play)
            if not why:
                continue
            l = loc[play][t["i"]]
            v = l["verse"]
            rows.append({"play": play, "act": l["act"], "verse": v, "approx_verse": l["approx"],
                         "speaker": l["speaker"], "form": t["text"], "v2_lemma": N.base_normalize(t["lemma"]),
                         "note": why if why is not True else "",
                         "prev_verse": vt[play][VS.neighbours(play, v)[0]] if VS.neighbours(play, v)[0] != v else "",
                         "verse_text": vt[play][v],
                         "next_verse": vt[play][VS.neighbours(play, v)[-1]] if VS.neighbours(play, v)[-1] != v else ""})
    return pd.DataFrame(rows)


def md_table(df, cols):
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in df.itertuples():
        out.append("| " + " | ".join(str(getattr(r, c)).replace("|", "/") for c in cols) + " |")
    return out


def main():
    lex = TL.families()
    docs = json.loads((P.DATA / "v2" / "plays_tokens.json").read_text(encoding="utf-8"))
    loc = VS.token_locations()
    denom = Counter()
    for _, title, toks in V.token_lists("play"):
        denom["Ecerinis" if title == "Ecerinis" else SEN] += len(toks)

    count, forms, ruled, foedus_pos, superus_forms = defaultdict(Counter), defaultdict(Counter), Counter(), Counter(), Counter()
    for d in docs:
        grp = "Ecerinis" if d["title"] == "Ecerinis" else SEN
        for t in d["tokens"]:
            k0 = V.token_key(t, d["title"])
            k = TL.lexicon_key(t, d["title"])
            if k0 != k:
                ruled[(k0, N.base_normalize(t["text"]), k, grp)] += 1
            if k0 == "superus":
                sf = N.base_normalize(t["text"])
                superus_forms[("summ-/supr-" if sf.startswith(("summ", "supr")) else "super-", grp)] += 1
            if k0 == "foedus":
                foedus_pos[(t["pos"], grp)] += 1
            if k:
                count[k][grp] += 1
                forms[k][N.base_normalize(t["text"])] += 1

    rows = []
    for f, ws in lex.items():
        for w in ws:
            rows.append({"family": f, "lemma": w, "ecerinis": count[w]["Ecerinis"], "seneca": count[w][SEN],
                         "forms": "; ".join(f"{s} {n}" for s, n in forms[w].most_common(8))})
    ct = pd.DataFrame(rows)
    ct.to_csv(OUT / "audit_counts_revised.csv", index=False, encoding="utf-8-sig")
    fam = ct.groupby("family", sort=False)[["ecerinis", "seneca"]].sum()

    md = ["# Theme lexicon v2: revised audit (decisions of context/lexicon_audit_decisions.md)", "",
          "Author-chosen word families (`data/theme_lexicon.json`), counted as v2 tokens before the dictionary "
          "filter. Lexicon-only token rules (`_token_rules` in the lexicon file) apply; the LDA input is "
          "unchanged. Seneca = the ten plays combined. Rate = family tokens per 1,000 v2 tokens "
          f"(Ecerinis {denom['Ecerinis']:,}; Seneca {denom[SEN]:,}). The step 1 audit "
          "(`lexicon_audit.md`) is kept as it was.", "",
          "Verse numbers in this file and from now on are the TEI editions' `<l n>` verse numbers "
          "(`src/verses.py`). Earlier reports gave the position of the line in the v2 text, which counts each "
          "piece of a verse split between speakers (`<l part=\"I|M|F\">`) as a line; Ecerinis has 25 such "
          "extra pieces, so line positions ran ahead of verse numbers (line 325 = v. 312, 454 = v. 431, "
          "466 = v. 443; the vadum lines 505, 529 = vv. 482, 504; the vendico lines 90, 308 = vv. 83, 298). "
          "Seneca verse numbers are the DraCor TEI copies' per-verse `<milestone unit=\"line\" n>` values "
          "(`data/sources/seneca_tei/`).", "",
          "## Token rules applied", ""]
    for (k0, s, k, g), n in sorted(ruled.items(), key=str):
        md.append(f"- {k0} '{s}' → {k or '(not counted)'}: {g} {n}")
    md += ["", "## Family totals (all families; changed ones marked)", "",
           "| family | Ecerinis | Ecerinis per 1,000 | Seneca | Seneca per 1,000 | thin (<5 Ecerinis) | change |",
           "|---|---|---|---|---|---|---|"]
    for f, r in fam.iterrows():
        thin = "**thin**" if r.ecerinis < THIN else ""
        md.append(f"| {f} | {r.ecerinis} | {1000 * r.ecerinis / denom['Ecerinis']:.2f} | {r.seneca} | "
                  f"{1000 * r.seneca / denom[SEN]:.2f} | {thin} | {CHANGED.get(f, '')} |")
    md += ["", "## Changed families, per lemma", ""]
    for f in CHANGED:
        sub = ct[ct.family == f]
        md += [f"### {f}", "", f"{CHANGED[f]}. Total: Ecerinis {sub.ecerinis.sum()} / Seneca {sub.seneca.sum()}.", "",
               "| lemma | Ecerinis | Seneca | surface forms (top 8) |", "|---|---|---|---|"]
        md += [f"| {r.lemma} | {r.ecerinis} | {r.seneca} | {r.forms or '—'} |" for r in sub.itertuples()]
        if f == "deceit_betrayal":
            md += ["", "**Homograph, resolved by counting nouns only (`_pos_only`):** the key *foedus* merges *foedus* 'treaty' (noun) with *foedus* "
                   "'foul' (adjective; Morpheus foedus1). By v2 part of speech, before the rule: " + "; ".join(
                       f"{pos} {g} {n}" for (pos, g), n in sorted(foedus_pos.items())) +
                   ". The Ecerinis token is *Foeda* (Ece 2, v. 237, 'Foeda Gomorrae Sodomaeque labes'), the adjective."]
        if f == "providence_divine":
            md += ["", "**superus: only super- forms count (`_exclude_prefixes`).** v2 (LatinCy 3.9.8) files the superlative *summus* / *supremus* under "
                   "*superus*. By surface form, before the rule: " + "; ".join(f"{k} {g} {n}" for (k, g), n in sorted(superus_forms.items())) +
                   ". All Ecerinis tokens are *summus* 'highest': *summi Olympi* (Ece 2, v. 230), *e summo datam* "
                   "(Ece 4, v. 466), *arce summa* (Ece 5, v. 567)."]
        md.append("")
    md += ["### punishment_vengeance (counts unchanged)", "",
           f"*uindico* has two senses, 'avenge / punish' and 'claim', and the lexicon cannot separate them. "
           f"Ecerinis' medieval spelling *vendico* ('claim', vv. 83, 298) is keyed *uendico* "
           f"({count['uendico']['Ecerinis']} / {count['uendico'][SEN]}) and is not counted under *uindico* "
           f"({count['uindico']['Ecerinis']} / {count['uindico'][SEN]}); the *uindico* tokens that remain are not "
           "sense-checked.", ""]

    prodo = context_rows(docs, loc, lambda t, p: True if N.base_normalize(t["lemma"]) == "prodo" else
                         ("v2 lemma prodeo; Morpheus: prodeo or prodo" if p == "Ecerinis" and t["text"] == "prodit"
                          else False))
    prodo.insert(0, "id", range(1, len(prodo) + 1))
    prodo["betray"] = ""
    if not (OUT / "prodo_tokens.csv").exists():      # never overwrite the author's marks
        prodo.to_csv(OUT / "prodo_tokens.csv", index=False, encoding="utf-8-sig")
    prodo = pd.read_csv(OUT / "prodo_tokens.csv", encoding="utf-8-sig", dtype=str).fillna("")
    uendo = context_rows(docs, loc, lambda t, p: N.base_normalize(t["lemma"]) in ("uendo", "uendico") and
                         ("uendico ('claim'): kept separate, listed for reference"
                          if N.base_normalize(t["lemma"]) == "uendico" else True))
    uendo.insert(0, "id", range(1, len(uendo) + 1))
    uendo["decision"] = ""
    if not (OUT / "uendo_tokens.csv").exists():
        uendo.to_csv(OUT / "uendo_tokens.csv", index=False, encoding="utf-8-sig")
    uendo = pd.read_csv(OUT / "uendo_tokens.csv", encoding="utf-8-sig", dtype=str).fillna("")
    fingo = context_rows([d for d in docs if d["title"] == "Ecerinis"], loc,
                         lambda t, p: N.base_normalize(t["lemma"]) == "fingo")
    fingo.to_csv(OUT / "fingo_ecerinis.csv", index=False, encoding="utf-8-sig")

    cols = ["id", "play", "act", "verse", "speaker", "form", "v2_lemma", "verse_text", "note"]
    md += ["## prodo: every token, for sense-checking", "",
           "Marked by the author (`data/lexicon_marks/prodo_tokens_marked.csv`, column `betray`); tokens marked y "
           "count under deceit_betrayal.", ""] + md_table(prodo, cols + ["betray"])
    md += ["", "## uendo ('sell'): every token; uendico listed separately", "",
           "Marked by the author (`data/lexicon_marks/uendo_tokens_marked.csv`, column `decision`); uendo tokens "
           "marked y count under deceit_betrayal.", ""] + md_table(uendo, cols + ["decision"])
    md += ["", "## fingo in Ecerinis (reference only; not added)", ""] + md_table(
        fingo.assign(id=range(1, len(fingo) + 1)), cols)
    (OUT / "lexicon_audit_revised.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
