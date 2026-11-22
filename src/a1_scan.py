"""A1 review scans (nothing is applied here).

1. Effect preview of the fixed rules (lowercase, v->u, j->i).
2. Spelling-variant candidates for data/variant_map.json, for approval.
3. Suspected LatinCy lemmatization errors, with suggested fixes, for approval.

Input: the play-level DocBin (verified identical to processed_corpus.pkl), so
every lemma can be traced to its surface forms. Reference list: LatinCy's own
form->lemma table (la-latincy-lookups 1.0.0).

Writes to results/a1_normalization/:
  base_rules_preview.md, variant_candidates.csv, lemma_audit.csv, scan_summary.md
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict

import pandas as pd

import normalize as N
import pipeline as P
import spacy_docs as S

OUT = P.RESULTS / "a1_normalization"
ECERINIS = "Ecerinis"
ABBR = {"Phoenissae": "Pho", "Troades": "Tro", "Phaedra": "Pha", "Agamemnon": "Aga",
        "Hercules Furens": "HF", "Medea": "Med", "Octavia": "Oct", "Oedipus": "Oed",
        "Thyestes": "Thy", "Hercules Oetaeus": "HO", "Ecerinis": "Ece"}

PREFIXES = [("adf", "aff"), ("adc", "acc"), ("adp", "app"), ("adg", "agg"), ("adl", "all"),
            ("adr", "arr"), ("ads", "ass"), ("adt", "att"), ("inm", "imm"), ("inl", "ill"),
            ("inr", "irr"), ("inp", "imp"), ("inb", "imb"), ("conl", "coll"), ("conr", "corr"),
            ("conm", "comm"), ("conp", "comp"), ("conb", "comb"), ("obf", "off"), ("obp", "opp"),
            ("obc", "occ"), ("subf", "suff"), ("subp", "supp"), ("subc", "succ"),
            ("subm", "summ"), ("subg", "sugg"), ("exs", "ex")]


def assimilate(w):
    for a, b in PREFIXES:
        if w.startswith(a):
            return b + w[len(a):]
    return w


RULES = {
    "uo/uu": lambda w: w.replace("uo", "uu"),
    "ae/e": lambda w: w.replace("ae", "e"),
    "oe/e": lambda w: w.replace("oe", "e"),
    "ae/oe": lambda w: w.replace("oe", "ae"),
    "chi/hi": lambda w: w.replace("chi", "hi"),
    "initial h": lambda w: w[1:] if w.startswith("h") else w,
    "ci/ti": lambda w: re.sub(r"ci(?=[aeiou])", "ti", w),
    "mpn/mn, mpt/mt": lambda w: w.replace("mpn", "mn").replace("mpt", "mt"),
    "y/i": lambda w: w.replace("y", "i"),
    "ph/f": lambda w: w.replace("ph", "f"),
    "th/t": lambda w: w.replace("th", "t"),
    "double consonant": lambda w: re.sub(r"([bcdfglmnprst])\1", r"\1", w),
    "prefix assimilation": assimilate,
}
RISKY = {"ae/e", "oe/e", "ae/oe", "initial h", "double consonant", "th/t", "ph/f", "ci/ti"}


def plays_str(counter_by_play, form):
    return ", ".join(f"{ABBR[t]} {c[form]}" for t, c in counter_by_play.items() if c[form])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sw = S.load_stopwords()
    ne = P.load_named_entities()
    plays = P.load_docs("play")
    titles = [p["title"] for p in plays]
    docs = S.load_docbin("play")
    kept = {t: S.kept_tokens(d, sw) for t, d in zip(titles, docs)}

    orig_tl = P.remove_named_entities(plays, ne)
    orig_dict, _ = P.build_corpus(orig_tl)
    orig_dict_words = set(orig_dict.token2id)
    sw_b = {N.base_normalize(w) for w in sw}
    ne_b = {N.base_normalize(w) for w in ne}

    # ---------- 1. fixed rules preview ----------
    rows, merges = [], defaultdict(set)
    for t in titles:
        lem = [l for _, l, _ in kept[t]]
        changed = [l for l in lem if N.base_normalize(l) != l]
        new_sw = [l for l in lem if l not in sw and N.base_normalize(l) in sw_b]
        new_ne = [l for l in lem if l not in ne and N.base_normalize(l) in ne_b]
        rows.append({"play": t, "tokens": len(lem), "tokens_changed": len(changed),
                     "pct_tokens_changed": round(100 * len(changed) / len(lem), 1),
                     "types": len(set(lem)), "types_changed": len(set(changed)),
                     "types_after": len({N.base_normalize(l) for l in lem}),
                     "newly_stopwords": len(new_sw), "newly_named_entities": len(new_ne)})
        for l in set(lem):
            merges[N.base_normalize(l)].add(l)
    pre = pd.DataFrame(rows)
    merged = {k: v for k, v in merges.items() if len(v) > 1}
    all_lem = Counter(l for t in titles for _, l, _ in kept[t])
    new_sw_all = Counter(l for l in all_lem.elements() if l not in sw and N.base_normalize(l) in sw_b)
    new_ne_all = Counter(l for l in all_lem.elements() if l not in ne and N.base_normalize(l) in ne_b)
    md = ["# A1 preview: fixed rules only (lowercase, v->u, j->i)", "",
          "Counts are over the tokens the preprocessing keeps (content POS, stopwords removed), "
          "before named-entity removal. The variant map is not applied yet.", "",
          pre.to_markdown(index=False), "",
          f"- Types that merge under v->u / j->i: {len(merged)} groups", ""]
    md += [f"  - {k}: " + ", ".join(f"{w} ({all_lem[w]})" for w in sorted(v)) for k, v in sorted(merged.items())]
    md += ["", "- Tokens that become stopwords only after normalization (the original stopword "
           "list was spelled differently): " + ", ".join(f"{w} ({c})" for w, c in new_sw_all.most_common()),
           "", "- Tokens that become named entities only after normalization: "
           + ", ".join(f"{w} ({c})" for w, c in new_ne_all.most_common())]
    (OUT / "base_rules_preview.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # ---------- 2. variant candidates ----------
    by_play = {t: Counter(N.base_normalize(l) for _, l, _ in kept[t]) for t in titles}
    vocab = Counter()
    for c in by_play.values():
        vocab.update(c)
    seneca = Counter()
    for t in titles:
        if t != ECERINIS:
            seneca.update(by_play[t])
    in_dict_b = {N.base_normalize(w) for w in orig_dict_words}
    hw = N.headwords()

    groups = defaultdict(set)  # frozenset(members) -> rules
    for name, fn in RULES.items():
        keyed = defaultdict(set)
        for w in vocab:
            keyed[fn(w)].add(w)
        for members in keyed.values():
            if len(members) > 1:
                groups[frozenset(members)].add(name)

    vrows = []
    for gid, (members, rules) in enumerate(sorted(groups.items(), key=lambda g: -sum(vocab[w] for w in g[0])), 1):
        lks = {w: N.lookup_lemma(w) for w in members}
        lk_targets = {N.base_normalize(v) for v in lks.values() if v} & set(members)
        if len(lk_targets) == 1:
            canon = next(iter(lk_targets))
        elif len(members & hw) == 1:
            canon = next(iter(members & hw))
        else:
            canon = max(members, key=lambda w: (seneca[w], vocab[w]))
        others = members - {canon}
        confirmed = all(lks[w] and N.base_normalize(lks[w]) == canon for w in others)
        both_headwords = all(w in hw for w in members)
        if confirmed:
            sugg = "apply (LatinCy lookup lists it as a form of the canonical lemma)"
        elif both_headwords and rules & RISKY:
            sugg = "likely reject (both are separate headwords)"
        else:
            sugg = "check"
        for w in sorted(members, key=lambda w: w != canon):
            vrows.append({"group": gid, "rules": "; ".join(sorted(rules)), "form": w,
                          "canonical": canon, "is_canonical": w == canon,
                          "n_total": vocab[w], "n_seneca": seneca[w], "n_ecerinis": by_play[ECERINIS][w],
                          "plays": plays_str(by_play, w), "in_dictionary": w in in_dict_b,
                          "lookup_lemma": lks[w] or "", "is_headword": w in hw,
                          "suggestion": sugg, "approve": ""})
    vdf = pd.DataFrame(vrows)
    vdf.to_csv(OUT / "variant_candidates.csv", index=False, encoding="utf-8-sig")

    # ---------- 3. lemma audit ----------
    surf, pos, per_play = defaultdict(Counter), defaultdict(Counter), defaultdict(Counter)
    for t in titles:
        for s, l, p in kept[t]:
            surf[l][s] += 1
            pos[l][p] += 1
            per_play[l][t] += 1
    arows = []
    for l, sc in surf.items():
        lb = N.base_normalize(l)
        n = sum(sc.values())
        surf_lk = {s: N.lookup_lemma(s) for s in sc}
        lk_votes = Counter()
        for s, c in sc.items():
            if surf_lk[s]:
                lk_votes[N.base_normalize(surf_lk[s])] += c
        top_lk, top_n = (lk_votes.most_common(1)[0] if lk_votes else (None, 0))
        disagree = {s: N.base_normalize(v) for s, v in surf_lk.items() if v and N.base_normalize(v) != lb}
        main_pos = pos[l].most_common(1)[0][0]
        flags = []
        m = re.match(r"^(.*?)(que|ue|ne)$", lb)
        if m and lb not in hw and m.group(1) and N.lookup_lemma(m.group(1)):
            flags.append("enclitic not split")
        if lb not in hw:
            if len(lb) <= 3:
                flags.append("truncated lemma")
            if lb.endswith(("ior", "ius")) and main_pos == "ADJ":
                flags.append("comparative as lemma")
            if lb.endswith("ndus"):
                flags.append("gerundive as lemma")
            if main_pos == "NOUN" and lb.endswith(("ae", "arum", "orum", "ibus")):
                flags.append("inflected noun as lemma")
            if main_pos == "ADJ" and lb.endswith(("um", "ae", "a", "i", "o")):
                flags.append("inflected adjective as lemma")
            if main_pos == "VERB" and not lb.endswith(("o", "or", "i", "t", "m", "sum")):
                flags.append("verb lemma with non-lemma ending")
            if top_lk and top_n / n >= 0.5 and not flags:
                flags.append("not in lookup; lookup assigns surface forms elsewhere")
        elif top_lk and top_lk != lb and top_n / n >= 0.3:
            flags.append("homograph? lookup assigns surface forms elsewhere")
        if pos[l]["PROPN"] / n >= 0.5 and l not in ne:
            flags.append("possible missed named entity")
        if not flags:
            continue
        hard = {"enclitic not split", "truncated lemma", "comparative as lemma", "gerundive as lemma",
                "inflected noun as lemma", "inflected adjective as lemma", "verb lemma with non-lemma ending"}
        priority = ("A" if hard & set(flags) else
                    "B" if any(f.startswith(("homograph", "not in lookup")) for f in flags) else "C")
        arows.append({"priority": priority, "lemma": l, "flags": "; ".join(flags),
                      "proposed_lemma": top_lk if top_lk and top_lk != lb else "",
                      "surface_suggestions": "; ".join(f"{s}->{v} ({sc[s]})" for s, v in
                                                       sorted(disagree.items(), key=lambda x: -sc[x[0]])),
                      "n_total": n,
                      "n_ecerinis": per_play[l][ECERINIS], "in_dictionary": l in orig_dict_words,
                      "pos": ", ".join(f"{p} {c}" for p, c in pos[l].most_common()),
                      "surface_forms": ", ".join(f"{s} {c}" for s, c in sc.most_common(8)),
                      "plays": ", ".join(f"{ABBR[t]} {c}" for t, c in per_play[l].items()),
                      "approve": ""})
    adf = pd.DataFrame(arows).sort_values(["priority", "in_dictionary", "n_total"], ascending=[True, False, False])
    adf.to_csv(OUT / "lemma_audit.csv", index=False, encoding="utf-8-sig")

    # ---------- summary ----------
    sm = ["# A1 scan summary (for review; nothing applied)", "",
          "## Fixed rules (v->u, j->i)", "", pre[["play", "tokens", "tokens_changed", "pct_tokens_changed",
                                                   "types_changed", "newly_stopwords"]].to_markdown(index=False),
          "", f"{len(merged)} pairs of types merge (e.g. invado/inuado). Full list: `base_rules_preview.md`.", "",
          "## Variant candidates (`variant_candidates.csv`)", "",
          f"- {vdf.group.nunique()} candidate groups; by suggestion: "
          + ", ".join(f"{k}: {v}" for k, v in vdf.drop_duplicates('group').suggestion.value_counts().items()), "",
          "## Lemma audit (`lemma_audit.csv`)", "",
          "- Priority A: lemma has a non-lemma shape (truncated, enclitic attached, comparative, gerundive, "
          "inflected ending). B: LatinCy's own lookup table assigns the surface forms to another lemma "
          "(homographs; the lookup is single-valued, so many B rows are lookup errors). "
          "C: only flagged as a possible missed named entity (mostly PROPN).",
          "- The lookup table (la-latincy-lookups 1.0.0) is incomplete: many correct lemmas are absent "
          "from it, so absence alone is not flagged.", "",
          adf.groupby("priority").agg(lemmas=("lemma", "size"), tokens=("n_total", "sum"),
                                      in_dictionary=("in_dictionary", "sum"),
                                      ecerinis_tokens=("n_ecerinis", "sum")).to_markdown()]
    (OUT / "scan_summary.md").write_text("\n".join(sm) + "\n", encoding="utf-8")
    print("\n".join(sm))


if __name__ == "__main__":
    main()
