"""Theme lexicon v2: play- and act-level rates (steps 2-4 of context/theme_lexicon_v2_brief.md).

**Author-chosen lexicon counts, not model output.** Families: data/theme_lexicon.json
(as revised by context/lexicon_audit_decisions.md), with the lexicon-only token rules
of src/theme_lexicon.py (vadum, furabor, diti/dites, prodo and uendo only where the
author marked them, foedus nouns only, superus super- forms only).

Tokens: the v2 content tokens (src/v2_corpus.token_lists: LatinCy 3.9.8, stopwords,
named entities, lemma fixes and spelling map applied), before the dictionary filter.
A token that a lexicon rule excludes stays in the denominator and counts for no family.
Rate = family tokens per 1,000 tokens.

Intervals: bootstrap 95% percentile intervals, resampling consecutive 200-token chunks
within each play (50-token chunks within each act) with replacement, 2,000 replicates,
seed 0; a final chunk shorter than half a chunk is merged into the one before it
(the same procedure as src/a5_theme_rates.py).

Act percentile: mid-rank percentile of the act's rate among all 56 acts, the act
included: 100 x (acts with a lower rate + half the acts with an equal rate) / 56.
Many acts have a rate of 0 for the thin families, and ties share the mid-rank.

Families with fewer than 5 Ecerinis tokens are flagged as thin; raw counts are shown
beside every rate.

Outputs (results/a5_lexicon_v2/rates/): lexicon_rates_summary.md, rates_plays.csv,
rates_acts.csv, act_percentiles.csv, word_counts.csv;
figures/fig_lexicon_v2_plays.png, figures/fig_lexicon_v2_act_percentiles.png
"""
from __future__ import annotations

import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

import pipeline as P
import theme_lexicon as TL
import v2_corpus as V
from a2_acts import ABBR
from a2_analyze import AXIS, GRID, INK, INK2, MUTED, SURFACE, style
from a5_theme_rates import ACT_CHUNK, CHUNK, FOCUS, OTHER, rates

OUT = P.RESULTS / "a5_lexicon_v2" / "rates"
FIG = OUT / "figures"
THIN = 5
EXCLUDED = "<excluded by lexicon rule>"
FOCUS_ACTS = ["Ece 1", "Ece 2", "Ece 3", "Ece 4", "Ece 5", "Aga 1", "Pho 1", "Thy 1", "Thy 2", "Thy 3", "Oed 4",
              "Tro 4", "Aga 3", "Med 3", "Med 5", "Aga 2", "HF 3", "Pha 2"]
DIVERGING = LinearSegmentedColormap.from_list(
    "pct_div", ["#1f5fae", "#6da7ec", "#cde2fb", "#efeeea", "#f9d3bd", "#f09a68", "#c4501f"])


def units(level):
    """[(play, label, [lexicon keys])], one key per v2 token (EXCLUDED where a rule drops it)."""
    path = P.DATA / "v2" / ("plays_tokens.json" if level == "play" else "acts_tokens.json")
    docs = json.loads(path.read_text(encoding="utf-8"))
    out = []
    for d in docs:
        play = d["title"]
        keys = []
        for t in d["tokens"]:
            if V.token_key(t, play) is None:
                continue
            k = TL.lexicon_key(t, play)
            keys.append(k if k else EXCLUDED)
        label = play if level == "play" else f"{ABBR[play]} {d['act']}"
        out.append((play, label, keys))
    return out


def check_denominators(play_units):
    ref = {t: len(l) for _, t, l in V.token_lists("play")}
    assert all(ref[p] == len(k) for p, _, k in play_units), "token totals differ from v2_corpus.token_lists"


def mid_percentile(values, x):
    v = np.asarray(values)
    return 100 * ((v < x).sum() + 0.5 * (v == x).sum()) / len(v)


def fig_plays(df, lex, thin, path):
    themes = list(lex)
    ncol = 6
    nrow = int(np.ceil(len(themes) / ncol))
    plays = ["Ecerinis"] + sorted(p for p in df.play.unique() if p != "Ecerinis")
    y = {p: i for i, p in enumerate(reversed(plays))}
    fig, axes = plt.subplots(nrow, ncol, figsize=(16, 3.1 * nrow + 0.9), sharey=True, facecolor=SURFACE,
                             constrained_layout=True)
    axes = axes.ravel()
    for ax, theme in zip(axes, themes):
        style(ax)
        ax.grid(axis="y", visible=False)
        ax.grid(axis="x", color=GRID, linewidth=0.6)
        d = df[df.theme == theme].set_index("play")
        sen = d.drop("Ecerinis").rate.mean()
        ax.axvline(sen, color=AXIS, linewidth=1.2, linestyle=(0, (3, 2)), zorder=1)
        for p in plays:
            c = FOCUS if p == "Ecerinis" else OTHER
            ax.plot([d.loc[p, "ci_low"], d.loc[p, "ci_high"]], [y[p]] * 2, color=c, linewidth=2,
                    solid_capstyle="round", alpha=1 if p == "Ecerinis" else 0.55, zorder=2)
            ax.plot(d.loc[p, "rate"], y[p], "o", markersize=7.5 if p == "Ecerinis" else 5.5, color=c,
                    markeredgecolor=SURFACE, markeredgewidth=1.3, zorder=3)
        n = int(d.loc["Ecerinis", "count"])
        ax.set_title(theme + (" (thin)" if theme in thin else "") + "\n", fontsize=10, color=INK, loc="left")
        ax.text(0.0, 1.015, f"Ecerinis n = {n}", transform=ax.transAxes, fontsize=8, color=INK2,
                ha="left", va="bottom")
        ax.set_xlim(left=0)
        ax.tick_params(axis="x", labelsize=8)
        ax.set_yticks(list(y.values()), list(y.keys()), fontsize=8)
        for lbl in ax.get_yticklabels():
            if lbl.get_text() == "Ecerinis":
                lbl.set_color(FOCUS)
                lbl.set_fontweight("bold")
    for ax in axes[len(themes):]:
        ax.set_visible(False)
    for ax in axes[(nrow - 1) * ncol:len(themes)]:
        ax.set_xlabel("per 1,000 tokens", fontsize=8.5, color=INK2)
    fig.suptitle("Author-chosen lexicon counts (data/theme_lexicon.json), not model output. v2 tokens before the "
                 "dictionary filter.\nDot: rate per 1,000 tokens; bar: bootstrap 95% interval (200-token chunks); "
                 "dashed line: mean of the ten Seneca plays. 'thin' = fewer than 5 Ecerinis tokens.",
                 fontsize=9, color=INK2, x=0.01, ha="left")
    fig.savefig(path, dpi=300)
    plt.close(fig)


def fig_heatmap(pct, cnt, lex, thin, path):
    themes = list(lex)
    M = np.array([[pct[(t, a)] for a in FOCUS_ACTS] for t in themes])
    fig, ax = plt.subplots(figsize=(13.5, 8.6), facecolor=SURFACE, constrained_layout=True)
    ax.set_facecolor(SURFACE)
    im = ax.imshow(M, cmap=DIVERGING, vmin=0, vmax=100, aspect="auto")
    for i, t in enumerate(themes):
        for j, a in enumerate(FOCUS_ACTS):
            v = M[i, j]
            ax.text(j, i - 0.12, f"{v:.0f}", ha="center", va="center", fontsize=8,
                    color=SURFACE if v < 12 or v > 88 else INK)
            ax.text(j, i + 0.27, f"n={cnt[(t, a)]}", ha="center", va="center", fontsize=5.8,
                    color=SURFACE if v < 12 or v > 88 else INK2)
    ax.set_xticks(range(len(FOCUS_ACTS)), FOCUS_ACTS, rotation=0, fontsize=8.5)
    ax.set_yticks(range(len(themes)), [t + (" (thin)" if t in thin else "") for t in themes], fontsize=9)
    for lbl in ax.get_xticklabels():
        if lbl.get_text().startswith("Ece"):
            lbl.set_color(FOCUS)
            lbl.set_fontweight("bold")
    ax.axvline(4.5, color=INK, linewidth=1.4)
    ax.set_xticks(np.arange(-0.5, len(FOCUS_ACTS)), minor=True)
    ax.set_yticks(np.arange(-0.5, len(themes)), minor=True)
    ax.grid(which="minor", color=SURFACE, linewidth=2)
    ax.tick_params(which="both", length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    cb = fig.colorbar(im, ax=ax, shrink=0.6, pad=0.01)
    cb.set_label("percentile among all 56 acts (mid-rank)", fontsize=8.5, color=INK2)
    cb.outline.set_visible(False)
    cb.ax.tick_params(labelsize=8, colors=INK2)
    ax.set_title("Author-chosen lexicon counts (data/theme_lexicon.json), not model output. Cell: percentile of the "
                 "act's family rate among all 56 acts (50 = median); n = family tokens in the act.\n"
                 "Acts are short (50-token-chunk intervals in rates_acts.csv are wide); 'thin' = fewer than 5 "
                 "Ecerinis tokens in the whole play.", fontsize=8.5, color=INK2, loc="left")
    fig.savefig(path, dpi=300)
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    lex = TL.families()
    rng = np.random.default_rng(0)
    pu, au = units("play"), units("act")
    check_denominators(pu)
    assert len(au) == 56, len(au)
    pl = rates(pu, lex, rng)
    ac = rates(au, lex, rng, ACT_CHUNK)
    pl.to_csv(OUT / "rates_plays.csv", index=False, encoding="utf-8-sig")

    ece_counts = pl[pl.play == "Ecerinis"].set_index("theme")["count"]
    thin = {t for t in lex if ece_counts[t] < THIN}

    pct, cnt, prow = {}, {}, []
    for t in lex:
        sub = ac[ac.theme == t]
        for r in sub.itertuples():
            p = mid_percentile(sub.rate, r.rate)
            pct[(t, r.unit)] = p
            cnt[(t, r.unit)] = r.count
            prow.append({"theme": t, "act": r.unit, "play": r.play, "tokens": r.tokens, "count": r.count,
                         "rate": r.rate, "ci_low": r.ci_low, "ci_high": r.ci_high, "percentile": p,
                         "focus_act": r.unit in FOCUS_ACTS, "thin_family": t in thin})
    ac["percentile"] = [pct[(t, u)] for t, u in zip(ac.theme, ac.unit)]
    ac.to_csv(OUT / "rates_acts.csv", index=False, encoding="utf-8-sig")
    pdf = pd.DataFrame(prow)
    pdf[pdf.focus_act].to_csv(OUT / "act_percentiles.csv", index=False, encoding="utf-8-sig")
    missing = set(FOCUS_ACTS) - set(ac.unit)
    assert not missing, missing

    words = []
    for play, _, keys in pu:
        for t, ws in lex.items():
            for w in ws:
                n = sum(k == w for k in keys)
                words.append({"play": play, "theme": t, "word": w, "count": n, "rate": 1000 * n / len(keys)})
    wd = pd.DataFrame(words)
    wd.to_csv(OUT / "word_counts.csv", index=False, encoding="utf-8-sig")

    fig_plays(pl, lex, thin, FIG / "fig_lexicon_v2_plays.png")
    fig_heatmap(pct, cnt, lex, thin, FIG / "fig_lexicon_v2_act_percentiles.png")

    flag = lambda t: " †" if t in thin else ""
    md = ["# Theme lexicon v2: rates (steps 2-4)", "",
          "**Author-chosen lexicon counts (`data/theme_lexicon.json`), not model output.** v2 tokens before the "
          "dictionary filter; lexicon-only token rules applied (`src/theme_lexicon.py`). Rate = family tokens per "
          f"1,000 tokens. Interval = bootstrap 95% percentile interval ({CHUNK}-token chunks within plays, "
          f"{ACT_CHUNK}-token chunks within acts, 2,000 replicates, seed 0). Seneca mean = mean of the ten Seneca "
          "plays' rates. † = thin family (fewer than 5 Ecerinis tokens): read its rates with the raw counts.", "",
          "Families: " + "; ".join(f"**{t}**: {', '.join(w)}" for t, w in lex.items()) + ".", "",
          "## Play level", "",
          "| theme | Ecerinis rate [95% CI] (count / tokens) | Seneca mean | Seneca plays: range | "
          "Ecerinis rank of 11 | Seneca plays whose interval does not overlap Ecerinis's |", "|---|---|---|---|---|---|"]
    for t in lex:
        d = pl[pl.theme == t].set_index("play")
        e, s = d.loc["Ecerinis"], d.drop("Ecerinis")
        apart = [f"{p} ({'above' if s.loc[p, 'ci_low'] > e.ci_high else 'below'})" for p in s.index
                 if s.loc[p, "ci_high"] < e.ci_low or s.loc[p, "ci_low"] > e.ci_high]
        md.append(f"| {t}{flag(t)} | {e.rate:.1f} [{e.ci_low:.1f}–{e.ci_high:.1f}] ({e['count']} / {e.tokens}) | "
                  f"{s.rate.mean():.1f} | {s.rate.min():.1f}–{s.rate.max():.1f} | {int((d.rate > e.rate).sum()) + 1} | "
                  f"{len(apart)}: {', '.join(apart) or '—'} |")
    md += ["", "Rank: 1 = highest rate; ties share the better rank. 'above' / 'below' = the Seneca play's interval "
           "lies wholly above / below Ecerinis's.", "",
           "Per play (rate [95% CI], count):", "", "| play | " + " | ".join(f"{t}{flag(t)}" for t in lex) + " |",
           "|---|" + "---|" * len(lex)]
    for play in ["Ecerinis"] + sorted(p for p in pl.play.unique() if p != "Ecerinis"):
        cells = []
        for t in lex:
            x = pl[(pl.play == play) & (pl.theme == t)].iloc[0]
            cells.append(f"{x.rate:.1f} [{x.ci_low:.1f}–{x.ci_high:.1f}], n={x['count']}")
        md.append(f"| {play} | " + " | ".join(cells) + " |")

    md += ["", "## Act level", "",
           "Percentile = mid-rank percentile of the act's rate among all 56 acts (the act included; 50 = median). "
           "Many Seneca and Ecerinis acts have 0 tokens in the smaller families, so a percentile near 30-45 can "
           "simply mean 'zero, tied with many acts'. All 56 acts are in `rates_acts.csv`.", "",
           "### Percentiles (n = family tokens in the act)", "",
           "| theme | " + " | ".join(FOCUS_ACTS) + " |", "|---|" + "---|" * len(FOCUS_ACTS)]
    for t in lex:
        md.append(f"| {t}{flag(t)} | " + " | ".join(f"{pct[(t, a)]:.0f} (n={cnt[(t, a)]})" for a in FOCUS_ACTS) + " |")
    tok = ac.drop_duplicates("unit").set_index("unit").tokens
    md += ["", "Act lengths (v2 tokens): " + "; ".join(f"{a} {tok[a]}" for a in FOCUS_ACTS) + ".", "",
           "### Rates with 95% intervals (50-token chunks; wide)", "",
           "| act | " + " | ".join(f"{t}{flag(t)}" for t in lex) + " |", "|---|" + "---|" * len(lex)]
    for a in FOCUS_ACTS:
        cells = []
        for t in lex:
            x = ac[(ac.unit == a) & (ac.theme == t)].iloc[0]
            cells.append(f"{x.rate:.1f} [{x.ci_low:.1f}–{x.ci_high:.1f}]")
        md.append(f"| {a} | " + " | ".join(cells) + " |")
    md += ["", "## Figures", "", "- `figures/fig_lexicon_v2_plays.png`: play-level small multiples, one panel per family.",
           "- `figures/fig_lexicon_v2_act_percentiles.png`: families × the 18 acts above, coloured by percentile.", "",
           "Per-word counts per play: `word_counts.csv`."]
    (OUT / "lexicon_rates_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
