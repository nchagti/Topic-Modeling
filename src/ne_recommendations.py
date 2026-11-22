"""Context-based recommendations for the uncertain named-entity lemmas.

Basis: Claude read every occurrence's context (results/a1_v2/named_entity_contexts.txt,
up to 6 passages per lemma, capitalized occurrences first) for the 149 lemmas where
the evidence rule in a1_v2_scan.py is uncertain. Principles:
  P1 people, gods with their own mythology, places, rivers, peoples and adjectives derived from them -> name
  P2 personified abstractions (the name is the ordinary word for the concept)          -> word
  P3 winds, sun and moon (weather/sky vocabulary)                                      -> word
  P4 generic classes of creatures -> word; individual beings -> name
  P5 homographs with unrelated senses -> split: per token, a name if 3.9.8 tags that
     token PROPN or PERSON/LOC/NORP, otherwise a word
  P6 participial adjectives that LiLa lists only as names -> word
Writes data/v2/named_entities_recommendations.csv (column `approve` left empty).
"""
import pandas as pd

import pipeline as P

R = {  # lemma: (recommendation, principle, reason)
    # group A
    "uenus": ("name", "P1", "the goddess; some Phaedra uses are metonymic (love), but it is a deity name"),
    "phryges": ("name", "P1", "the Phrygians (Trojans)"),
    "zephyrus": ("word", "P3", "west wind"),
    "graius": ("name", "P1", "'Greek', ethnic adjective"),
    "eurus": ("word", "P3", "east wind"),
    "luna": ("word", "P3", "the moon (personified in magic passages)"),
    "parthus": ("name", "P1", "Parthians"),
    "caesar": ("name", "P1", "title/name of the emperor (Octavia); Ecerinis 'Caesarum domus'"),
    "arcadius": ("name", "P1", "Arcadian"),
    "centaurus": ("word", "P4", "centaurs as a class of creatures"),
    "cycnus": ("split", "P5", "Cycnus (son of Neptune/Mars) vs cygnus, swan"),
    "sparta": ("name", "P1", "Sparta"),
    "neptunus": ("name", "P1", "the god"),
    "phocis": ("name", "P1", "Phocis"),
    "eleus": ("name", "P1", "Elean"),
    "astraea": ("name", "P1", "Astraea (the Virgin)"),
    "impietas": ("word", "P2", "personified Impiety (HF) and impiety (Oct)"),
    "phineus": ("name", "P1", "Phineus"),
    "latinus": ("name", "P1", "Latin (matres Latinae)"),
    "althaea": ("name", "P1", "Althaea"),
    "plautus": ("name", "P1", "Rubellius Plautus"),
    "uulcanus": ("name", "P1", "Vulcan (Ecerinis: vocative 'Vulcane')"),
    "caritas": ("word", "P2", "Ecerinis: 'Caritas Spes et Fides', 'Caritas pia' (theological virtue)"),
    "fortuna": ("word", "P2", "Fortune personified; a theme word"),
    "sol": ("word", "P3", "the sun (also Medea's ancestor)"),
    "auster": ("word", "P3", "south wind"),
    "siculus": ("name", "P1", "Sicilian"),
    "tigris": ("split", "P5", "river Tigris vs tiger"),
    "cupido": ("word", "P2", "Cupid as personified desire, and cupido 'desire'"),
    "gigas": ("word", "P4", "giants as a class"),
    "maenas": ("word", "P4", "maenads as a class"),
    "senectus": ("word", "P2", "old age, sometimes personified"),
    "eous": ("name", "P1", "'eastern' (from Eos), geographic adjective"),
    "libra": ("split", "P5", "constellation Libra (Thy) vs scales"),
    "alpheus": ("name", "P1", "river Alpheus"),
    "crux": ("word", "P2", "Ecerinis: crosses as punishment, and the Cross; a punishment theme word"),
    "aegaeus": ("name", "P1", "Aegean"),
    "euripus": ("name", "P1", "the Euripus strait"),
    "indus": ("name", "P1", "Indian / the Indus"),
    # group B (participles; everything else in group B defaults to name)
    "tacitus": ("word", "P6", "adjective 'silent'"),
    "patiens": ("word", "P6", "adjective 'enduring'"),
    "doctus": ("word", "P6", "adjective 'skilled'"),
    "citus": ("word", "P6", "adjective 'swift' (Ecerinis: 'atrox Ecerinus citus aduolat')"),
    "decens": ("word", "P6", "adjective 'seemly'"),
    "meritus": ("word", "P6", "Ecerinis 'meriti' (deserved)"),
    "tonans": ("name", "P1", "the Thunderer (Jupiter)"),
    # group C (default name)
    "nubila": ("word", "P1", "clouds ('saeui nubila fati'), not a name"),
    "harpyia": ("word", "P4", "harpies as a class"),
    "thyas": ("word", "P4", "thyiads (bacchants) as a class"),
    # group D
    "ecerinus": ("name", "P1", "Ezzelino"),
    "ecerinum": ("name", "P1", "Ezzelino (3.9.8 lemma for Ecerini/Ecerinum; should merge into ecerinus)"),
    "patauus": ("name", "P1", "Paduans"),
    "iaceret": ("word", "-", "verb form of iaceo with a garbled lemma; fix the lemma to iaceo"),
    # group E (default word)
    "pontus": ("split", "P5", "region Pontus vs pontus 'sea' (60 tokens, mostly the sea)"),
    "taurus": ("split", "P5", "Taurus mountains / Tauri / constellation vs bull"),
    "hydra": ("name", "P4", "the Lernaean Hydra, an individual monster"),
    "anguis": ("split", "P5", "constellation Anguis (Thy) vs snake"),
    "forum": ("split", "P5", "Ecerinis 'Iulii Forum' (Cividale) vs forum"),
    "notus": ("word", "P3", "south wind; the lemma also merges notus 'known'"),
    "comes": ("word", "P2", "companion; Ecerinis 'Comes' is a title (the Count)"),
    "herceus": ("name", "P1", "Jupiter Herceus"),
    "pierius": ("name", "P1", "Pierian"),
    "abydus": ("name", "P1", "Abydos"),
    "parius": ("name", "P1", "Parian (marble)"),
    "actaea": ("name", "P1", "Attic"),
    "io": ("word", "-", "garbled token 'Ius' (Pha); not the name Io"),
}
DEFAULT = {"A": ("name", "P1", ""), "B": ("name", "P1", "a name 3.9.8 tagged ADJ/VERB"),
           "C": ("name", "P1", "a name written in lowercase at a line start"),
           "D": ("name", "P1", ""), "E": ("word", "P2", "personified abstraction / common word")}


def main():
    sel = pd.read_csv(P.RESULTS / "a1_v2" / "named_entity_selection.csv")
    rows = []
    for r in sel.itertuples():
        rec, pr, why = R.get(r.lemma, DEFAULT[r.g])
        rows.append({"lemma": r.lemma, "group": r.g, "rule_decision": r.decision, "recommendation": rec,
                     "principle": pr, "reason": why, "n": r.n, "ecerinis": r.ecerinis,
                     "lila_pos": r.lila_pos, "entity_or_propn_share": r.entity_or_propn_share,
                     "changes_rule_decision": rec != r.decision.replace(" (flag)", ""), "approve": ""})
    df = pd.DataFrame(rows).sort_values(["changes_rule_decision", "n"], ascending=[False, False])
    df.to_csv(P.DATA / "v2" / "named_entities_recommendations.csv", index=False, encoding="utf-8-sig")
    print(df.groupby(["recommendation"]).agg(lemmas=("lemma", "size"), tokens=("n", "sum")).to_string())
    ch = df[df.changes_rule_decision]
    print(f"\nchanges vs the rule: {len(ch)} lemmas, {ch.n.sum()} tokens")
    print(ch[["lemma", "rule_decision", "recommendation", "principle", "n", "ecerinis"]].to_string(index=False))


if __name__ == "__main__":
    main()
