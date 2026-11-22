"""Context-based triage of the v2 lemma review (proposals; nothing applied until approved).

Basis: Claude read the passages of the 333 priority review groups
(results/a1_v2/lemma_contexts.txt: up to 3 per group, surface/lemma/POS as LatinCy
3.9.8 assigned them), plus all 12 Seneca 'manes -> maneo' tokens, the 28 'anime -> anima'
tokens and the cecid- forms. Surface lists for every lemma-wide merge were checked
(e.g. all fragro tokens are flagr- forms).

Writes:
  data/v2/lemma_fixes_v2.csv          rows appended with status 'proposed (lemma triage)'
  data/v2/named_entities_additions.csv names found in the triage (status proposed)
  results/a1_v2/lemma_triage.csv      every priority group with its decision and reason
"""
import pandas as pd

import normalize as N
import pipeline as P

V2 = P.DATA / "v2"
OUT = P.RESULTS / "a1_v2"

# (from_lemma, to_lemma, surface ('' = every surface), play ('' = all), reason)
FIXES = [
    # lemma-wide merges (all surfaces checked)
    ("tuor", "tutus", "", "", "adjective 'safe' (tutus, tutis, tutissimum)"),
    ("fragro", "flagro", "", "", "all tokens are flagr- 'blaze' (fragro is 'smell')"),
    ("fulgo", "fulgeo", "", "", "fulges, fulsi: fulgeo"),
    ("negligo", "neglego", "", "", "same verb; neglego is the other 3.9.8 lemma"),
    ("afflico", "affligo", "", "", "non-word lemma for afflictos"),
    ("tinguo", "tingo", "", "", "same verb; tingo is the other 3.9.8 lemma"),
    ("nuo", "nutus", "", "", "nutus, nutibus: noun 'nod, command'"),
    ("pecu", "pecus", "", "", "pecori, pecudis: pecus"),
    ("furio", "furia", "", "", "furiis 'with frenzies'"),
    ("furius", "furia", "", "", "Medea 'pectus en Furiis patet'"),
    ("carbasa", "carbasus", "", "", "plural carbasa of carbasus 'sail'"),
    ("ruino", "ruina", "", "", "ruinis: noun ruina"),
    ("summisit", "summitto", "", "", "non-word lemma"),
    ("summisi", "summitto", "", "", "non-word lemma"),
    ("iamna", "<drop>", "", "", "iamne = iam + -ne (adverb)"),
    ("iror", "iratus", "", "", "non-word lemma for iratus"),
    ("iro", "iratus", "", "", "non-word lemma for iratae"),
    ("coniugi", "coniux", "", "", "dative of coniux (3.9.8's headword)"),
    ("largio", "largior", "", "", "largire is the deponent largior"),
    ("threicium", "threicius", "", "", "Thracian (a name; see additions)"),
    ("uerono", "uerona", "", "", "Ecerinis: Verona, lowercased at a line start"),
    ("proco", "procus", "", "", "proci 'suitors'"),
    ("sollicio", "sollicitus", "", "", "non-word lemma"),
    ("solliceo", "sollicitus", "", "", "non-word lemma"),
    ("solliceor", "sollicitus", "", "", "non-word lemma"),
    ("frequensne", "frequens", "", "", "frequens + -ne"),
    ("inquieo", "inquietus", "", "", "non-word lemma"),
    ("genital", "genitalis", "", "", "Ecerinis 'infantum genital recidi' (truncated in the source)"),
    ("mammo", "mamma", "", "", "Ecerinis 'sectis mammis'"),
    ("ziramons", "<drop>", "", "", "Ecerinis 'Ziramons? domine': a name/label, not vocabulary"),
    ("uidetne", "uideo", "", "", "uidet + -ne (Ecerinis)"),
    ("implicio", "implico", "", "", "non-word lemma"),
    ("paenitendi", "paeniteo", "", "", "gerund of paeniteo"),
    ("iacentum", "iaceo", "", "", "Ecerinis 'gemitus iacentum'"),
    ("erebo", "erebus", "", "", "Erebus (a name)"),
    ("spumo", "spuma", "", "", "Ecerinis 'ex ore spumam mittit'"),
    ("trago", "traho", "", "", "Ecerinis 'uirgines tractae'"),
    ("peruetustae", "peruetustus", "", "", "Ecerinis 'peruetustae memoriae'"),
    ("ausibus", "ausus", "", "", "Ecerinis 'ausibus nostris' (noun ausus)"),
    ("certauo", "certus", "", "", "Ecerinis 'certaue funera' = certa + -ue"),
    ("panquo", "pactum", "", "", "'pacta fratrum' (agreements)"),
    ("posteo", "postis", "", "", "'in postem' (doorpost)"),
    ("excelse", "excelsus", "", "", "Ecerinis vocative 'excelse mundi rector'"),
    ("instabilio", "instabilis", "", "", "'instabile regnum'"),
    ("diremit", "dirimo", "", "", "Ecerinis 'litem diremit'"),
    ("purisuus", "purus", "", "", "purisue = puris + -ue"),
    ("resonio", "resono", "", "", "Ecerinis 'resonuit caelum'"),
    ("executo", "exsecutor", "", "", "Ecerinis 'ipse executor'"),
    ("pompo", "pompa", "", "", "'nec pompae ueniet'"),
    ("euxilium", "auxilium", "", "", "Ecerinis 'mortale euxilium damus': typo for auxilium"),
    ("uen", "<drop>", "", "", "Phaedra 'trito uine ala collo': garbled text"),
    ("abomino", "abominor", "", "", "deponent"),
    ("dure", "durus", "", "", "vocative 'o dure Theseu'"),
    ("uereris", "uereor", "", "", "'uereris fratris dolos'"),
    ("scelestis", "scelestus", "", "", "'diris, scelestis'"),
    ("miserus", "miser", "", "", "non-word lemma"),
    ("carino", "carina", "", "", "'mille carinis'"),
    ("stulta", "stultus", "", "", "'Stulta est fides'"),
    ("infer", "inferi", "", "", "'inferorum carcer' (3.9.8's plural noun inferi)"),
    ("oblite", "obliuiscor", "", "", "'oblite nostri'"),
    ("uenerandos", "uenerandus", "", "", "like the other uenerandus tokens"),
    ("desertae", "desertus", "", "", "'senectae desertae'"),
    ("lugubre", "lugubris", "", "", "'lugubribus amicta'"),
    ("abdio", "abdo", "", "", "'iura abdita'"),
    ("belligera", "belliger", "", "", "'belligera Pallas'"),
    ("sacrus", "sacer", "", "", "non-word lemma"),
    ("pella", "pello", "", "", "'regno pelle' (expel)"),
    ("semusta", "semustus", "", "", "'semustas faces'"),
    ("cyclada", "cyclades", "", "", "the Cyclades (a name; see additions)"),
    ("lombardum", "lombardus", "", "", "Ecerinis 'lombarda gens' (a name; see additions)"),
    ("aegisthe", "aegisthus", "", "", "vocative of Aegisthus (a name)"),
    ("instabilio", "instabilis", "", "", ""),
    # surface-specific fixes
    ("maneo", "manes", "manes", "", "all 12 Seneca tokens are the Manes ('manes meos', 'restitue manes')"),
    ("mane", "manes", "manes", "", "the Manes"),
    ("manis", "manes", "manes", "", "the Manes"),
    ("macnes", "manes", "manes", "", "the Manes ('manes semel umbrasque uidi')"),
    ("anima", "animus", "anime", "", "vocative of animus ('O my soul'), 28 tokens"),
    ("nascor", "nata", "nata", "", "vocative/noun 'daughter' ('quid me, nata, ...')"),
    ("nascor", "nata", "natam", "", "'daughter' ('tuam natam parens Helenae immolasti')"),
    ("nascor", "nata", "natas", "", "'daughters' (Medea: Pelias' daughters)"),
    ("plango", "planctus", "planctus", "", "noun 'lament' (beating of breasts)"),
    ("plango", "planctus", "planctibus", "", "noun 'lament'"),
    ("oblino", "obliuiscor", "oblita", "", "'oblita nati', 'oblita nostri' (forgetting)"),
    ("specto", "spectator", "spectator", "", "noun 'onlooker' (Ecerinis 1)"),
    ("uere", "uer", "uere", "", "'uere primo' (spring)"),
    ("libo", "libens", "libens", "", "'furabor libens' (willingly)"),
    ("capio", "coepi", "coepit", "", "'qua coepit'"),
    ("caedo", "caedes", "caedibus", "", "Ecerinis 'caedibus tantis', 'polluere caedibus' (slaughter)"),
    ("caedo", "cado", "ceciderant", "", "Octavia 'quo uota ceciderant mea' (fell)"),
    ("tyrannus", "tyrannis", "tyrannidi", "", "Ecerinis 'mors est mixta tyrannidi' (tyranny)"),
    ("tyrannus", "tyrannis", "tyrannidis", "", "Ecerinis 'saeuae tyrannidis' (tyranny)"),
    ("tyrannus", "tyrannis", "tyrannis", "Ecerinis", "Ecerinis 'saeua tyrannis', 'subiit tyrannis' (tyranny); HO 'tyrannis regibus' stays tyrannus"),
    ("magnum", "magnus", "magna", "", "substantive 'great things' (3.9.8 convention: adjective lemma)"),
    ("imo", "inferus", "imo", "", "'ab imo': same as the other imus tokens (accepted convention)"),
    ("cio", "citus", "citas", "", "'citas undas' (swift)"),
    ("cio", "citus", "citis", "", "'cursibus citis'"),
    ("cio", "citus", "citos", "", "'citos currus'"),
    ("cio", "cieo", "cite", "", "imperative of cieo"),
    ("odor", "olor", "oloris", "", "'pennas oloris' (swan)"),
    ("stips", "stipes", "stipites", "", "Ecerinis 'pingues stipites' (logs)"),
    ("modero", "moderator", "moderator", "", "Ecerinis 'moderator aequi'"),
    ("paco", "paciscor", "pactus", "", "'coniugem pactus sibi'"),
    ("paco", "pacator", "pacator", "", "'orbis pacator'"),
    ("residus", "resido", "residi", "", "'in quis residi'"),
    ("renis", "ren", "renes", "", "Ecerinis 'supplices renes'"),
    ("merx", "merces", "merces", "", "'funesta merces' (reward)"),
    ("supersto", "superstes", "superstite", "", "Ecerinis 'te superstite'"),
    ("lampo", "lampas", "lampade", "", "'dira lampade Erinys'"),
    ("praesum", "praesens", "praesentibus", "", "Ecerinis 'praesentibus malis'"),
    ("aes", "aer", "aeris", "Ecerinis", "'faciem aeris sulphureus inuasit uapor' (air)"),
    ("ministro", "ministra", "ministrae", "", "Ecerinis 'ministrae facinorum'"),
    ("rapto", "raptor", "raptorem", "", "'raptorem sui'"),
    ("strepo", "strepitus", "strepitus", "", "noun 'noise'"),
    ("aspicio", "aspectus", "adspectus", "", "noun 'sight'"),
    ("senex", "senium", "senii", "", "'deformis senii'"),
    ("ico", "ictus", "ictibus", "", "noun 'blows' (Ecerinis 1)"),
    ("ico", "ictus", "ictum", "Troades", "'conuersa ad ictum' (noun)"),
    ("tero", "teres", "teretes", "", "'teretes laqueos' (smooth)"),
    ("aequo", "aequor", "aequoris", "", "'aequoris undis' (sea)"),
    ("aequo", "aequor", "aequorum", "", "'Proteus aequorum'"),
    ("undo", "unda", "undarum", "", "'undarum globus'"),
    ("pensus", "pensum", "pensi", "", "'pensi nihil ducunt'"),
    ("oppono", "oppositus", "oppositu", "", "noun 'interposition'"),
    ("domito", "domitrix", "domitrix", "", "'maris domitrix Iolcos'"),
    ("machinor", "machinator", "machinator", "", "'O machinator fraudis'"),
    ("serpo", "serpens", "serpentum", "", "'serpentum genus'"),
    ("co", "cassis", "casse", "", "'casse uinctus' (net)"),
    ("color", "colus", "colos", "", "'parcarum colos' (distaffs)"),
    ("superior", "supremus", "supremum", "", "'supremum munus/ignem' (last); like the supremus tokens"),
]
ADDITIONS = [
    ("cadmeius", "Cadmean (Cadmea progenies, Cadmeis Bacchis)"),
    ("threicius", "Thracian"),
    ("cyclades", "the Cyclades"),
    ("lombardus", "Lombard (Ecerinis 'lombarda gens')"),
]
CONVENTION = {"inferus", "exter", "exterior", "propior", "interior", "superi", "superum", "superior"}
MAPPED = {"assum", "adsuesco", "submitto", "irrogo", "exurgo"}


def main():
    fx = pd.read_csv(V2 / "lemma_fixes_v2.csv", encoding="utf-8-sig", dtype=str).fillna("")
    fx = fx[~fx.status.str.contains("lemma triage")]  # idempotent
    seen, new = set(), []
    for frm, to, surf, play, why in FIXES:
        k = (frm, surf, play)
        if k in seen or not why:
            continue
        seen.add(k)
        new.append({"from_lemma": frm, "to_lemma": to, "surface": surf, "play": play, "reason": why,
                    "status": "proposed (lemma triage)"})
    out = pd.concat([fx, pd.DataFrame(new)], ignore_index=True)
    out.to_csv(V2 / "lemma_fixes_v2.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame([{"lemma": l, "reason": r, "status": "proposed (lemma triage)"} for l, r in ADDITIONS]).to_csv(
        V2 / "named_entities_additions.csv", index=False, encoding="utf-8-sig")

    groups = pd.read_csv(OUT / "lemma_groups.csv")
    by_specific = {(f, s): (t, w) for f, t, s, p, w in FIXES if s}
    by_wide = {f: (t, w) for f, t, s, p, w in FIXES if not s}
    rows = []
    for g in groups.itertuples():
        lem, surf = g.lemma_398, g.surface
        if (lem, surf) in by_specific:
            to, why = by_specific[(lem, surf)]
            dec = "drop" if to == "<drop>" else "fix"
        elif lem in by_wide:
            to, why = by_wide[lem]
            dec = "drop" if to == "<drop>" else "fix"
        elif lem in CONVENTION:
            to, dec, why = "", "keep", "3.9.8 convention (accepted): comparative/superlative or plural noun lemma"
        elif lem in MAPPED:
            to, dec, why = "", "keep", "handled by the approved spelling map"
        elif lem in {"cadmeius"}:
            to, dec, why = "", "name", "Cadmean: add to the name list"
        else:
            to, dec, why = "", "keep", "3.9.8 lemma is right in context (Morpheus lacks it or lists only the source verb)"
        rows.append({"gid": g.gid, "surface": surf, "lemma_398": lem, "pos_398": g.pos_398, "n": g.n,
                     "ecerinis": g.ecerinis, "decision": dec, "to_lemma": to, "reason": why})
    tri = pd.DataFrame(rows)
    tri.to_csv(OUT / "lemma_triage.csv", index=False, encoding="utf-8-sig")
    s = tri.groupby("decision").agg(groups=("gid", "size"), tokens=("n", "sum"), ecerinis=("ecerinis", "sum"))
    print(s.to_string())
    print(f"\nfix rows proposed: {len(new)}; name additions: {len(ADDITIONS)}")


if __name__ == "__main__":
    main()
