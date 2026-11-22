"""Generate the two optional A1 proposal lists (for approval; nothing applied).

data/lemma_policy_proposed.csv
    Gerundive lemmas (timendus) -> verb, and regular comparative/superlative
    lemmas (leuior) -> positive. LatinCy is inconsistent here: most comparatives
    are already lemmatized to the positive, a few are not. Suppletive and
    lexicalized forms (maior, melior, summus, supremus ...) are left out.
data/named_entities_proposed.csv
    Lemmas tagged PROPN in most of their occurrences, or hand-identified as
    names, that are not in unique_named_entities.pkl.
"""
from collections import Counter, defaultdict

import pandas as pd

import normalize as N
import pipeline as P
import spacy_docs as S

SUPPLETIVE = {"melior", "peior", "maior", "minor", "plurimus", "minimus", "optimus", "pessimus",
              "prior", "superior", "inferior", "ulterior", "interior", "exterior", "posterior",
              "citerior", "supremus", "summus", "infimus", "intimus", "extremus", "postremus",
              "ultimus", "proximus", "maximus", "senior", "iunior"}
HAND_NE = {"martha": "Mars (Marte)", "furius": "Furiae", "uenerus": "Venus", "patauus": "Padua",
           "monticulus": "Monticoli family", "vicentia": "Vicenza", "tarvisius": "Treviso",
           "adua": "Adda (river)", "lombarda": "Lombardy", "mantuus": "Mantua", "gallia": "Gaul",
           "zenon": "Zeno", "remi": "Remus", "tartarus": "Tartarus", "arctos": "the Bear",
           "scythes": "Scythian", "hesperia": "Hesperia", "triuia": "Trivia", "pentheus": "Pentheus",
           "ida": "Ida", "persa": "Persian", "poeni": "Carthaginians", "azo": "Azzo",
           "salinguerra": "Salinguerra", "ferrarienses": "Ferrarese", "aegyptius": "Egyptian"}
NOT_NE = {"iustitia", "impietas", "natura", "fortuna", "redemptor", "papa", "stupenda", "cunctor", "bellus"}


def main():
    sw = S.load_stopwords()
    ne = P.load_named_entities()
    plays = P.load_docs("play")
    titles = [p["title"] for p in plays]
    docs = S.load_docbin("play")
    surf, pos, per_play = defaultdict(Counter), defaultdict(Counter), defaultdict(Counter)
    for t, d in zip(titles, docs):
        for s, l, p in S.kept_tokens(d, sw):
            surf[l][s] += 1
            pos[l][p] += 1
            per_play[l][t] += 1
    hw = N.headwords()

    def lookup_target(l):
        votes = Counter()
        for s, c in surf[l].items():
            lk = N.lookup_lemma(s)
            if lk:
                votes[N.base_normalize(lk)] += c
        return votes.most_common(1)[0][0] if votes else ""

    rows = []
    for l in surf:
        lb = N.base_normalize(l)
        kind = None
        if lb.endswith("ndus") and lb not in hw:
            kind = "gerundive -> verb"
        elif lb.endswith(("ior", "issimus")) and lb not in SUPPLETIVE and pos[l].most_common(1)[0][0] == "ADJ":
            kind = "comparative/superlative -> positive"
        if not kind:
            continue
        target = lookup_target(l)
        if not target or target == lb:
            continue
        rows.append({"from_lemma": l, "to_lemma": target, "category": kind,
                     "n_total": sum(surf[l].values()), "n_ecerinis": per_play[l]["Ecerinis"],
                     "target_already_in_corpus": target in {N.base_normalize(x) for x in surf},
                     "surface_forms": ", ".join(f"{s} {c}" for s, c in surf[l].most_common(6)),
                     "approve": ""})
    pd.DataFrame(rows).sort_values(["category", "n_total"], ascending=[True, False]).to_csv(
        P.DATA / "lemma_policy_proposed.csv", index=False, encoding="utf-8-sig")

    ne_rows = []
    for l in surf:
        if l in ne or l in NOT_NE:
            continue
        n = sum(surf[l].values())
        propn = pos[l]["PROPN"] / n >= 0.5
        if propn or l in HAND_NE:
            ne_rows.append({"lemma": l, "note": HAND_NE.get(l, ""), "n_total": n,
                            "n_ecerinis": per_play[l]["Ecerinis"],
                            "basis": "identified by hand" if l in HAND_NE else "PROPN in most occurrences",
                            "surface_forms": ", ".join(f"{s} {c}" for s, c in surf[l].most_common(5)),
                            "plays": ", ".join(f"{t} {c}" for t, c in per_play[l].items()),
                            "approve": ""})
    pd.DataFrame(ne_rows).sort_values(["basis", "n_total"], ascending=[True, False]).to_csv(
        P.DATA / "named_entities_proposed.csv", index=False, encoding="utf-8-sig")
    print(f"policy rows: {len(rows)}; named-entity candidates: {len(ne_rows)}")


def named_entity_share():
    """How often each lemma on unique_named_entities.pkl was actually tagged
    PERSON/LOC/NORP (the NER notebook adds a lemma after a single tag, then the
    pipeline removes every occurrence). Writes data/named_entities_share.csv."""
    sw = S.load_stopwords()
    ne = P.load_named_entities()
    plays = P.load_docs("play")
    docs = S.load_docbin("play")
    tagged, total, kept, ece = Counter(), Counter(), Counter(), Counter()
    for p, d in zip(plays, docs):
        kept_set = {i for i, t in enumerate(d)
                    if t.is_alpha and S.CUSTOM_LOOKUPS.get(t.text, t.lemma_).lower() not in sw
                    and t.pos_ in S.KEEP_POS}
        for i, t in enumerate(d):
            l = t.lemma_.lower()
            if l in ne and t.is_alpha:
                total[l] += 1
                tagged[l] += t.ent_type_ in {"PERSON", "LOC", "NORP"}
                if i in kept_set:
                    kept[l] += 1
                    ece[l] += p["title"] == "Ecerinis"
    rows = [{"lemma": l, "times_tagged_entity": tagged[l], "occurrences": total[l],
             "share_tagged": round(tagged[l] / total[l], 3),
             "content_tokens_removed": kept[l], "ecerinis_tokens_removed": ece[l],
             "keep_as_named_entity_if_share>=0.5": tagged[l] / total[l] >= 0.5}
            for l in total]
    df = pd.DataFrame(rows).sort_values("content_tokens_removed", ascending=False)
    df.to_csv(P.DATA / "named_entities_share.csv", index=False, encoding="utf-8-sig")
    off = df[~df["keep_as_named_entity_if_share>=0.5"]]
    print(f"listed lemmas found: {len(df)}; tagged <50% of the time: {len(off)} lemmas, "
          f"{off.content_tokens_removed.sum()} content tokens removed "
          f"({off.ecerinis_tokens_removed.sum()} in Ecerinis)")


if __name__ == "__main__":
    main()
    named_entity_share()
