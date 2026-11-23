"""Keyness: Ecerinis vs the ten Seneca plays combined (v2 tokens, before the dictionary filter).

Tokens: src/v2_corpus.token_lists('play') (A1-normalized content lemmas; stopwords
and named entities removed; no no_below / no_above filter).

Tested: every lemma with frequency >= 3 in Ecerinis.
  G2 (log-likelihood, Rayson & Garside 2000): 2 * sum O ln(O/E) over the two corpora,
     E = corpus size x combined frequency / total size. p from chi-square, 1 df;
     Bonferroni: p x number of lemmas tested (capped at 1).
  Log ratio (Hardie 2014): log2 of (relative frequency in Ecerinis / relative
     frequency in Seneca); a zero count is replaced by 0.5 (flagged).
Over-used: log ratio > 0, the top 40 by log ratio (ties broken by G2).
Under-used: log ratio < 0, the top 20 by log ratio (most negative first).
Supplementary (outside the >= 3 rule): lemmas Ecerinis uses fewer than 3 times
although the Seneca rate predicts at least 5, ranked by log ratio.

LDA topic columns: whether the lemma is in Ecerinis's topic's top 20 by relevance
(lambda = 0.6) in the v2 representative models (seed 29, k = 8; seed 35, k = 9;
src/a3_attribution.py), and the share of the 50 seeds (v2, k = 8) in which it is
in the top 20 of Ecerinis's dominant topic (src/a3_own_topics.py). 'In model
vocabulary' = kept by the dictionary filter (no_below=2, no_above=0.5).

Keyness-only lemma mapping (KEYNESS_MAP, both corpora; the LDA input is not changed):
  ausus -> audeo. Ecerinis's ausibus is the noun ausus, -us (lemma correct), but in
  Seneca LatinCy 3.9.8 lemmatizes every aus- participle form as audeo, so the noun and
  the verb would otherwise be counted apart. Decided by the author, 2026-11-22.
  (Seneca: 23 aus- tokens, all audeo; no Seneca token is lemmatized ausus.)
Lexical keywords (LEXICAL): lemmas checked by the author and kept as they are; the
summary reports the counts of related lemmas (RELATED).

Outputs: results/keyness/keyness_summary.md, keyness_all.csv, figures/fig_keyness_log_ratio.png
"""
from __future__ import annotations

from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import chi2

import pipeline as P
import v2_corpus
from a2_analyze import GRID, INK, INK2, SURFACE, style

OUT = P.RESULTS / "keyness"
FIG = OUT / "figures"
MIN_ECE = 3
OVER_C, UNDER_C = "#eb6834", "#2a78d6"
KEYNESS_MAP = {"ausus": "audeo"}
LEXICAL = {"nocuus"}
RELATED = {"nocuus": ["nocuus", "noxius", "nocens", "noceo"]}


def g2(a, b, n1, n2):
    e1, e2 = n1 * (a + b) / (n1 + n2), n2 * (a + b) / (n1 + n2)
    return 2 * ((a * np.log(a / e1) if a else 0) + (b * np.log(b / e2) if b else 0))


def log_ratio(a, b, n1, n2):
    return float(np.log2((max(a, 0.5) / n1) / (max(b, 0.5) / n2)))


def aus_forms():
    """v2 surface forms behind the lemmas ausus / audeo, by corpus (Ecerinis / Seneca)."""
    import json
    toks = json.loads((P.DATA / "v2" / "plays_tokens.json").read_text(encoding="utf-8"))
    out = {"Ecerinis": Counter(), "Seneca": Counter()}
    for d in toks:
        grp = "Ecerinis" if d["title"] == "Ecerinis" else "Seneca"
        for t in d["tokens"]:
            k = v2_corpus.token_key(t, d["title"])
            if k in ("ausus", "audeo"):
                out[grp][(t["text"].lower().replace("v", "u").replace("j", "i"), k)] += 1
    return out


def lemma_notes(df, ece, sen, ece_raw, sen_raw, fmt_p):
    forms = aus_forms()

    def fl(grp, key):
        c = {f: n for (f, k), n in forms[grp].items() if k == key}
        return ", ".join(f"{f} {n}" for f, n in sorted(c.items(), key=lambda x: (-x[1], x[0]))) or "none"

    sen_aus = sorted(((f, n) for (f, k), n in forms["Seneca"].items() if k == "audeo" and f.startswith("aus")),
                     key=lambda x: (-x[1], x[0]))
    md = ["## Lemma notes", "",
          "- **ausus → audeo (keyness only).** Ecerinis's *ausibus* is the noun *ausus, -ūs* and its lemma is correct, but "
          "LatinCy 3.9.8 lemmatizes all of Seneca's *aus-* participle forms as *audeo*, so the two would be counted apart. "
          "For keyness only, *ausus* is counted as *audeo* in both corpora (the LDA input is unchanged).",
          f"  - Before the mapping: *ausus* Ecerinis {ece_raw['ausus']} / Seneca {sen_raw['ausus']}; *audeo* Ecerinis "
          f"{ece_raw['audeo']} / Seneca {sen_raw['audeo']}.",
          f"  - Seneca's *aus-* forms in v2 ({sum(n for _, n in sen_aus)} tokens), all lemmatized *audeo*: "
          + ", ".join(f"{f} {n}" for f, n in sen_aus) + ". *ausum* and *ausis* do not occur. "
          f"No Seneca token is lemmatized *ausus*.",
          f"  - Ecerinis's forms: *ausus* ← {fl('Ecerinis', 'ausus')}; *audeo* ← {fl('Ecerinis', 'audeo')}.",
          f"  - After the mapping: *audeo* Ecerinis {ece['audeo']} / Seneca {sen['audeo']}."]
    if (df.lemma == "audeo").any():
        x = df[df.lemma == "audeo"].iloc[0]
        md.append(f"  - *audeo* keyness: log ratio {x.log_ratio:+.2f}, G² {x.G2:.1f}, Bonferroni p {fmt_p(x.p_bonferroni)}.")
    for lem in sorted(LEXICAL):
        md += [f"- **{lem}: lexical keyword.** The lemma was checked against its contexts and kept as it is. "
               "Counts of related lemmas (v2, before the dictionary filter):", "",
               "  | lemma | Ecerinis | Seneca combined |", "  |---|---|---|"]
        md += [f"  | {w} | {ece_raw[w]} | {sen_raw[w]} |" for w in RELATED[lem]]
    return md + [""]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    trip = v2_corpus.token_lists("play")
    ece_raw = Counter(next(l for _, t, l in trip if t == "Ecerinis"))
    sen_raw = Counter(w for _, t, l in trip if t != "Ecerinis" for w in l)
    ece = Counter(KEYNESS_MAP.get(w, w) for _, t, l in trip if t == "Ecerinis" for w in l)
    sen = Counter(KEYNESS_MAP.get(w, w) for _, t, l in trip if t != "Ecerinis" for w in l)
    n1, n2 = sum(ece.values()), sum(sen.values())
    vocab = set(P.build_corpus([l for _, _, l in trip])[0].token2id)
    rel29 = set(pd.read_csv(P.RESULTS / "a3_attribution" / "topic_keywords_v2_seed29_k8.csv", encoding="utf-8-sig").lemma)
    rel35 = set(pd.read_csv(P.RESULTS / "a3_attribution" / "topic_keywords_v2_seed35_k9.csv", encoding="utf-8-sig").lemma)
    wf = pd.read_csv(P.RESULTS / "a3_own_topics" / "own_topic_word_frequency.csv", encoding="utf-8-sig")
    share50 = wf[(wf.pipeline == "v2") & (wf.k == 8) & (wf.play == "Ecerinis")].set_index("word").share.to_dict()

    def row(w):
        a, b = ece[w], sen[w]
        return {"lemma": w, "count_ecerinis": a, "count_seneca": b, "per_1000_ecerinis": 1000 * a / n1,
                "per_1000_seneca": 1000 * b / n2, "expected_ecerinis": n1 * (a + b) / (n1 + n2),
                "G2": g2(a, b, n1, n2), "log_ratio": log_ratio(a, b, n1, n2), "zero_smoothed": (a == 0 or b == 0),
                "in_model_vocabulary": w in vocab, "in_topic_v2_seed29_k8": w in rel29,
                "in_topic_v2_seed35_k9": w in rel35, "share_of_50_seeds_v2_k8": share50.get(w, 0.0)}

    tested = [w for w, c in ece.items() if c >= MIN_ECE]
    df = pd.DataFrame([row(w) for w in tested])
    m = len(df)
    df["p"] = chi2.sf(df.G2, 1)
    df["p_bonferroni"] = np.minimum(1.0, df.p * m)
    df["direction"] = np.where(df.log_ratio > 0, "over", "under")
    df = df.sort_values(["log_ratio", "G2"], ascending=[False, False])
    df.to_csv(OUT / "keyness_all.csv", index=False, encoding="utf-8-sig")
    over = df[df.log_ratio > 0].head(40)
    under = df[df.log_ratio < 0].sort_values(["log_ratio", "G2"], ascending=[True, False]).head(20)
    supp = pd.DataFrame([row(w) for w in sen if ece[w] < MIN_ECE and n1 * (ece[w] + sen[w]) / (n1 + n2) >= 5])
    supp["p"] = chi2.sf(supp.G2, 1)
    supp = supp.sort_values(["log_ratio", "G2"], ascending=[True, False]).head(20)
    supp.to_csv(OUT / "keyness_supplementary_underused.csv", index=False, encoding="utf-8-sig")

    def fmt_p(p):
        return "1" if p >= 0.9995 else (f"{p:.3f}" if p >= 0.001 else f"{p:.1e}")

    def table(d, bonf=True):
        lines = ["| rank | lemma | Ecerinis | Seneca | per 1,000 Ece / Sen | log ratio | G² | p (Bonferroni) | "
                 "topic s29 k8 | topic s35 k9 | % of 50 seeds (k8) | in model vocab |", "|" + "---|" * 12]
        for r, (_, x) in enumerate(d.iterrows(), 1):
            lr = f"{x.log_ratio:+.2f}" + ("*" if x.zero_smoothed else "")
            pv = fmt_p(x.p_bonferroni) if bonf else f"{fmt_p(x.p)} (uncorr.)"
            name = f"{x.lemma} (lexical keyword)" if x.lemma in LEXICAL else x.lemma
            lines.append(f"| {r} | {name} | {x.count_ecerinis} | {x.count_seneca} | {x.per_1000_ecerinis:.2f} / "
                         f"{x.per_1000_seneca:.2f} | {lr} | {x.G2:.1f} | {pv} | {'✓' if x.in_topic_v2_seed29_k8 else ''} | "
                         f"{'✓' if x.in_topic_v2_seed35_k9 else ''} | {100 * x.share_of_50_seeds_v2_k8:.0f}% | "
                         f"{'yes' if x.in_model_vocabulary else 'no'} |")
        return lines

    sig = df[df.p_bonferroni < 0.05]
    md = ["# Keyness: Ecerinis vs the ten Seneca plays combined", "",
          f"v2 tokens (A1-normalized content lemmas), before the dictionary filter. Ecerinis {n1:,} tokens; Seneca "
          f"{n2:,} tokens. Tested: the {m} lemmas with frequency ≥ {MIN_ECE} in Ecerinis. G² = log-likelihood "
          "(Rayson & Garside); p from χ² (1 df), Bonferroni-corrected for the number of lemmas tested. Log ratio = "
          "log2 of the ratio of relative frequencies (Hardie); +1 = twice as frequent in Ecerinis. "
          "* = a zero count replaced by 0.5.", "",
          "**The counts are small (most tested lemmas occur 3–6 times in Ecerinis), so the effect sizes (log ratio) "
          "matter more than the p-values.** Bonferroni is conservative: few lemmas pass it.", "",
          f"- Lemmas passing Bonferroni p < 0.05: {len(sig)} ({len(sig[sig.log_ratio > 0])} over-used, "
          f"{len(sig[sig.log_ratio < 0])} under-used): {', '.join(sig.lemma)}.",
          f"- Over-used lemmas (log ratio > 0): {int((df.log_ratio > 0).sum())}; under-used: {int((df.log_ratio < 0).sum())}.",
          f"- Of the top 40 over-used, {int(over.in_topic_v2_seed29_k8.sum())} are in Ecerinis's topic's top 20 "
          f"(v2 seed 29, k = 8), {int(over.in_topic_v2_seed35_k9.sum())} at seed 35, k = 9; "
          f"{int((~over.in_model_vocabulary).sum())} are removed by the dictionary filter.",
          "- Topic columns: in the top 20 by relevance (λ = 0.6) of Ecerinis's dominant topic in the v2 representative "
          "models (seed 29, k = 8; seed 35, k = 9), and the share of the 50 seeds (v2, k = 8) in which the lemma is in "
          "that topic's top 20. 'In model vocab' = kept by no_below=2 / no_above=0.5.", ""] + lemma_notes(
              df, ece, sen, ece_raw, sen_raw, fmt_p) + [
          "## Top 40 over-used in Ecerinis (ranked by log ratio)", ""] + table(over) + [
          "", "## Top 20 under-used in Ecerinis (lemmas with frequency ≥ 3 in Ecerinis; ranked by log ratio)", ""] + table(under) + [
          "", "## Supplementary: lemmas Ecerinis uses fewer than 3 times although the Seneca rate predicts at least 5",
          "", "Outside the ≥ 3 rule, so not Bonferroni-corrected (uncorrected p shown). Ranked by log ratio.", ""] + table(supp, bonf=False) + [
          "", "Figure: `figures/fig_keyness_log_ratio.png`.", "", "Full table: `keyness_all.csv`."]
    (OUT / "keyness_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # figure
    fig, axes = plt.subplots(1, 2, figsize=(11, 10), facecolor=SURFACE, constrained_layout=True,
                             gridspec_kw={"width_ratios": [2, 1.15]})
    for ax, d, c, title in [(axes[0], over, OVER_C, "Top 40 over-used in Ecerinis"),
                            (axes[1], under, UNDER_C, "Top 20 under-used in Ecerinis")]:
        style(ax)
        ax.grid(axis="y", visible=False)
        ax.grid(axis="x", color=GRID, linewidth=0.6)
        d = d.iloc[::-1]
        labels = [f"{'● ' if t else ''}{w}{' ‡' if w in LEXICAL else ''}  {a}/{b}" for w, a, b, t in
                  zip(d.lemma, d.count_ecerinis, d.count_seneca, d.in_topic_v2_seed29_k8 | d.in_topic_v2_seed35_k9)]
        bars = ax.barh(range(len(d)), d.log_ratio, height=0.7, color=c, edgecolor=SURFACE, linewidth=0.8)
        for bar, z in zip(bars, d.zero_smoothed):
            if z:
                bar.set_hatch("////")
                bar.set_alpha(0.75)
        ax.set_ylim(len(d) - 40.5, len(d) - 0.5)
        for i, (lr, ps) in enumerate(zip(d.log_ratio, d.p_bonferroni)):
            if ps < 0.05:
                ax.text(lr + (0.08 if lr > 0 else -0.08), i, "†", va="center", ha="left" if lr > 0 else "right",
                        fontsize=9, color=INK)
        ax.set_yticks(range(len(d)), labels, fontsize=8)
        ax.set_title(title, fontsize=10.5, color=INK, loc="left")
        ax.set_xlabel("Log ratio (log2 of relative-frequency ratio)", fontsize=8.5, color=INK2)
        ax.axvline(0, color=INK2, linewidth=0.8)
    fig.suptitle(f"Keyness, Ecerinis vs ten Seneca plays combined (v2 lemmas, before the dictionary filter; lemmas with "
                 f"≥ {MIN_ECE} Ecerinis occurrences).\nLabels: lemma  Ecerinis count / Seneca count.  ● in Ecerinis's "
                 "LDA topic (top 20 by relevance, v2 seed 29 k = 8 or seed 35 k = 9).  † Bonferroni p < 0.05.\n"
                 "Hatched: Seneca count 0, log ratio computed with 0.5 in its place.  ‡ lexical keyword (lemma checked).  "
                 "ausus counted as audeo.\nCounts are small: read the bar lengths, not the p-values.", fontsize=8.5, color=INK2, x=0.01, ha="left")
    fig.savefig(FIG / "fig_keyness_log_ratio.png", dpi=300)
    plt.close(fig)
    print("\n".join(md))


if __name__ == "__main__":
    main()
