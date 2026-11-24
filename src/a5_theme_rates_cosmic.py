"""Four-panel theme-rate figure: Invasion, Deceit, Punishment (v1 lists) and Cosmic order (v2).

Same style as results/a5_theme_rates/figures/fig_a5_theme_rates_v2.png, with Fate replaced
by Cosmic order = the natural_cosmic_order family of the theme lexicon v2
(data/theme_lexicon.json, lexicon-only token rules applied).

Author-chosen lexicon counts, not model output. All four panels use v2 tokens before the
dictionary filter (the same token totals per play in both runs; checked below) and the
same bootstrap (200-token chunks, 2,000 replicates, seed 0). Nothing is recomputed: the
numbers are read from
  results/a5_theme_rates/theme_rates_plays.csv      (Invasion, Deceit, Punishment; v2 rows)
  results/a5_lexicon_v2/rates/rates_plays.csv       (natural_cosmic_order)
so they match the tables already reported. The Cosmic order subtitle lists its three most
frequent lemmas in Ecerinis (results/a5_lexicon_v2/rates/word_counts.csv).

Output: results/a5_theme_rates/figures/fig_theme_rates_cosmic.png
"""
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

import pipeline as P
from a2_analyze import AXIS, GRID, INK, INK2, SURFACE, style
from a5_theme_rates import FOCUS, OTHER, lexicon as lexicon_v1

V1_THEMES = ["Invasion", "Deceit", "Punishment"]
COSMIC, COSMIC_KEY = "Cosmic order", "natural_cosmic_order"
OUT = P.RESULTS / "a5_theme_rates" / "figures" / "fig_theme_rates_cosmic.png"


def main():
    v1 = pd.read_csv(P.RESULTS / "a5_theme_rates" / "theme_rates_plays.csv", encoding="utf-8-sig")
    v1 = v1[(v1.pipeline == "v2") & v1.theme.isin(V1_THEMES)]
    v2 = pd.read_csv(P.RESULTS / "a5_lexicon_v2" / "rates" / "rates_plays.csv", encoding="utf-8-sig")
    v2 = v2[v2.theme == COSMIC_KEY].assign(theme=COSMIC)
    tok1 = v1.drop_duplicates("play").set_index("play").tokens
    tok2 = v2.set_index("play").tokens
    assert (tok1 == tok2.reindex(tok1.index)).all(), "token totals differ between the two runs"
    df = pd.concat([v1, v2])

    wc = pd.read_csv(P.RESULTS / "a5_lexicon_v2" / "rates" / "word_counts.csv", encoding="utf-8-sig")
    top = (wc[(wc.play == "Ecerinis") & (wc.theme == COSMIC_KEY)]
           .sort_values(["count", "word"], ascending=[False, True]).head(3))
    lex1 = lexicon_v1()
    subtitles = {t: " / ".join(lex1[t]) for t in V1_THEMES}
    subtitles[COSMIC] = " / ".join(top.word)

    themes = V1_THEMES + [COSMIC]
    plays = ["Ecerinis"] + sorted(p for p in df.play.unique() if p != "Ecerinis")
    y = {p: i for i, p in enumerate(reversed(plays))}
    fig, axes = plt.subplots(1, len(themes), figsize=(12, 4.6), sharey=True, facecolor=SURFACE,
                             constrained_layout=True)
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
            ax.plot(d.loc[p, "rate"], y[p], "o", markersize=8 if p == "Ecerinis" else 6.5, color=c,
                    markeredgecolor=SURFACE, markeredgewidth=1.5, zorder=3)
        ax.text(0.0, 1.0, subtitles[theme], transform=ax.transAxes, fontsize=7.5, color=INK2, va="bottom",
                ha="left")
        ax.set_title(f"{theme}\n", fontsize=10.5, color=INK, loc="left")
        ax.set_xlabel("per 1,000 tokens", fontsize=8.5, color=INK2)
        ax.set_xlim(left=0)
    axes[0].set_yticks(list(y.values()), list(y.keys()))
    for lbl in axes[0].get_yticklabels():
        if lbl.get_text() == "Ecerinis":
            lbl.set_color(FOCUS)
            lbl.set_fontweight("bold")
    note = ("Lexicon counts from author-chosen word lists, not model output. Invasion, Deceit, Punishment: "
            "data/theme_lexicon_v1.json; Cosmic order: natural_cosmic_order in data/theme_lexicon.json (v2).\n"
            "Dots: rate; bars: bootstrap 95% interval (200-token chunks); dashed: mean of the ten Seneca plays. "
            "Tokens: v2 (A1-normalized).")
    fig.suptitle(note, fontsize=8.5, color=INK2, x=0.01, ha="left")
    fig.savefig(OUT, dpi=300)
    plt.close(fig)

    d = v2.set_index("play")
    e, s = d.loc["Ecerinis"], d.drop("Ecerinis")
    apart = [f"{p} ({'higher' if s.loc[p, 'ci_low'] > e.ci_high else 'lower'})" for p in s.index
             if s.loc[p, "ci_high"] < e.ci_low or s.loc[p, "ci_low"] > e.ci_high]
    print("| Theme (v2) | Ecerinis [95% CI] | Seneca mean (range) | Rank of 11 | "
          "Seneca plays whose interval doesn't overlap Ecerinis's |")
    print(f"| {COSMIC} | {e.rate:.1f} [{e.ci_low:.1f}–{e.ci_high:.1f}] | {s.rate.mean():.1f} "
          f"({s.rate.min():.1f}–{s.rate.max():.1f}) | {int((d.rate > e.rate).sum()) + 1} | {', '.join(apart) or 'none'} |")
    print(f"Ecerinis count {e['count']} / {e.tokens}; top lemmas: "
          + ", ".join(f"{r.word} {r['count']}" for _, r in top.iterrows()))


if __name__ == "__main__":
    main()
