"""A5 part 2: theme word-family rates per play and per act, with bootstrap intervals.

The word families are a lexicon chosen by the author (data/theme_lexicon_v1.json),
not model output. Rate = family tokens per 1,000 tokens.

Tokens:
  v2        A1-normalized content tokens (src/v2_corpus.token_lists: LatinCy
            3.9.8, stopwords, named entities, lemma fixes and spelling map applied)
  original  the processed tokens of the conference pipeline (data/original/corpus and acts pickles,
            'tokens' field, before named-entity removal), the basis of the rates
            quoted in the brief
Both are counted before the dictionary filter, which would remove most of
these words.

Interval: bootstrap 95% percentile interval, resampling consecutive 200-token
chunks within each play (50-token chunks within each act, since acts are short)
with replacement (2,000 replicates, seed 0; a final chunk shorter than half a
chunk is merged into the one before it).
Seneca reference = mean of the ten Seneca plays' rates (this reproduces the
brief's figures).

Outputs: results/a5_theme_rates/theme_rates_summary.md, theme_rates_plays.csv,
theme_rates_acts.csv, theme_word_rates.csv, figures/fig_a5_theme_rates_{v2,original}.png
"""
from __future__ import annotations

import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import pipeline as P
from a2_acts import ABBR
from a2_analyze import AXIS, GRID, INK, INK2, SURFACE, style

OUT = P.RESULTS / "a5_theme_rates"
FIG = OUT / "figures"
CHUNK, ACT_CHUNK, B = 200, 50, 2000
FOCUS, OTHER = "#eb6834", "#2a78d6"


def lexicon():
    lex = json.loads((P.DATA / "theme_lexicon_v1.json").read_text(encoding="utf-8"))
    return {k: v for k, v in lex.items() if not k.startswith("_")}


def load(pipe, level):
    if pipe == "v2":
        import v2_corpus
        trip = v2_corpus.token_lists(level)
        if level == "play":
            return [(t, t, l) for _, t, l in trip]
        return [(t, f"{ABBR[t]} {i.rsplit('act', 1)[1]}", l) for i, t, l in trip]
    docs = P.load_docs(level)
    if level == "play":
        return [(d["title"], d["title"], d["tokens"]) for d in docs]
    return [(d["title"], f"{ABBR[d['title']]} {d['act']}", d["tokens"]) for d in docs]


def chunks(n, size):
    edges = list(range(0, n, size)) + [n]
    if len(edges) > 2 and edges[-1] - edges[-2] < size // 2:
        edges.pop(-2)
    return list(zip(edges[:-1], edges[1:]))


def rates(units, lex, rng, size=CHUNK):
    rows = []
    for play, label, toks in units:
        cs = chunks(len(toks), size)
        sizes = np.array([b - a for a, b in cs])
        for theme, words in lex.items():
            ws = set(words)
            hits = np.array([sum(t in ws for t in toks[a:b]) for a, b in cs])
            idx = rng.integers(0, len(cs), size=(B, len(cs)))
            boot = 1000 * hits[idx].sum(1) / sizes[idx].sum(1)
            rows.append({"play": play, "unit": label, "theme": theme, "tokens": len(toks), "chunks": len(cs),
                         "count": int(hits.sum()), "rate": 1000 * hits.sum() / len(toks),
                         "ci_low": float(np.percentile(boot, 2.5)), "ci_high": float(np.percentile(boot, 97.5))})
    return pd.DataFrame(rows)


def figure(df, pipe, lex, path):
    themes = list(lex)
    plays = ["Ecerinis"] + sorted(p for p in df.play.unique() if p != "Ecerinis")
    y = {p: i for i, p in enumerate(reversed(plays))}
    fig, axes = plt.subplots(1, len(themes), figsize=(12, 4.6), sharey=True, facecolor=SURFACE, constrained_layout=True)
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
        ax.text(0.0, 1.0, " / ".join(lex[theme]), transform=ax.transAxes, fontsize=7.5, color=INK2, va="bottom",
                ha="left")
        ax.set_title(f"{theme}\n", fontsize=10.5, color=INK, loc="left")
        ax.set_xlabel("per 1,000 tokens", fontsize=8.5, color=INK2)
        ax.set_xlim(left=0)
    axes[0].set_yticks(list(y.values()), list(y.keys()))
    for lbl in axes[0].get_yticklabels():
        if lbl.get_text() == "Ecerinis":
            lbl.set_color(FOCUS)
            lbl.set_fontweight("bold")
    note = ("Lexicon counts from author-chosen word lists (data/theme_lexicon_v1.json), not model output. "
            "Dots: rate; bars: bootstrap 95% interval (200-token chunks); dashed: mean of the ten Seneca plays. "
            f"Tokens: {'v2 (A1-normalized)' if pipe == 'v2' else 'original pipeline (processed tokens)'}.")
    fig.suptitle(note, fontsize=8.5, color=INK2, x=0.01, ha="left", wrap=True)
    fig.savefig(path, dpi=300)
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    lex = lexicon()
    rng = np.random.default_rng(0)
    plays_all, acts_all, words_all = [], [], []
    md = ["# A5 part 2: theme word-family rates", "",
          "**These are lexicon counts from word lists chosen by the author (`data/theme_lexicon_v1.json`), not model output.** "
          "Rate = family tokens per 1,000 tokens, counted before the dictionary filter. Interval = bootstrap 95% "
          f"percentile interval from resampling consecutive {CHUNK}-token chunks within each play ({ACT_CHUNK}-token chunks within each act) ({B} replicates). "
          "Seneca mean = mean of the ten Seneca plays' rates (this definition reproduces the brief's figures). "
          "Raw counts in Ecerinis are small, so the intervals are wide; treat as descriptive.", "",
          "Families: " + "; ".join(f"**{t}**: {', '.join(w)}" for t, w in lex.items()) + ".", ""]
    for pipe in ("v2", "original"):
        pl = rates(load(pipe, "play"), lex, rng).assign(pipeline=pipe)
        ac = rates(load(pipe, "act"), lex, rng, ACT_CHUNK).assign(pipeline=pipe)
        plays_all.append(pl)
        acts_all.append(ac)
        for play, _, toks in load(pipe, "play"):
            for theme, words in lex.items():
                for w in words:
                    n = sum(t == w for t in toks)
                    words_all.append({"pipeline": pipe, "play": play, "theme": theme, "word": w, "count": n,
                                      "rate": 1000 * n / len(toks)})
        figure(pl, pipe, lex, FIG / f"fig_a5_theme_rates_{pipe}.png")
        tok = "v2 tokens (A1-normalized)" if pipe == "v2" else "original processed tokens (conference pipeline)"
        md += [f"## {tok}", "", "| theme | Ecerinis rate [95% CI] (count / tokens) | Seneca mean | Seneca plays: range | "
               "Ecerinis rank of 11 | Seneca plays whose interval does not overlap Ecerinis's |", "|---|---|---|---|---|---|"]
        for theme in lex:
            d = pl[pl.theme == theme].set_index("play")
            e, s = d.loc["Ecerinis"], d.drop("Ecerinis")
            below = [p for p in s.index if s.loc[p, "ci_high"] < e.ci_low or s.loc[p, "ci_low"] > e.ci_high]
            md.append(f"| {theme} | {e.rate:.1f} [{e.ci_low:.1f}–{e.ci_high:.1f}] ({e['count']} / {e.tokens}) | "
                      f"{s.rate.mean():.1f} | {s.rate.min():.1f}–{s.rate.max():.1f} | {int((d.rate > e.rate).sum()) + 1} | "
                      f"{len(below)}: {', '.join(below) or '—'} |")
        md += ["", "Per play (rate [95% CI]):", "", "| play | " + " | ".join(lex) + " |", "|---|" + "---|" * len(lex)]
        for play in ["Ecerinis"] + sorted(p for p in pl.play.unique() if p != "Ecerinis"):
            cells = []
            for theme in lex:
                x = pl[(pl.play == play) & (pl.theme == theme)].iloc[0]
                cells.append(f"{x.rate:.1f} [{x.ci_low:.1f}–{x.ci_high:.1f}]")
            md.append(f"| {play} | " + " | ".join(cells) + " |")
        md += ["", "Ecerinis acts (rate [95% CI], count; act length in tokens). Seneca acts: median rate and range "
               "over all Seneca acts:", "", "| act | tokens | " + " | ".join(lex) + " |", "|---|---|" + "---|" * len(lex)]
        ea = ac[ac.play == "Ecerinis"]
        for unit in ea.unit.unique():
            cells = []
            for theme in lex:
                x = ea[(ea.unit == unit) & (ea.theme == theme)].iloc[0]
                cells.append(f"{x.rate:.1f} [{x.ci_low:.1f}–{x.ci_high:.1f}], n={x['count']}")
            md.append(f"| {unit} | {ea[ea.unit == unit].tokens.iloc[0]} ({ea[ea.unit == unit].chunks.iloc[0]} chunks) | "
                      + " | ".join(cells) + " |")
        sa = ac[ac.play != "Ecerinis"]
        md.append("| Seneca acts | — | " + " | ".join(
            f"median {sa[sa.theme == t].rate.median():.1f} (range {sa[sa.theme == t].rate.min():.1f}–{sa[sa.theme == t].rate.max():.1f})"
            for t in lex) + " |")
        md += ["", f"Figure: `figures/fig_a5_theme_rates_{pipe}.png`.", ""]
    pd.concat(plays_all).to_csv(OUT / "theme_rates_plays.csv", index=False, encoding="utf-8-sig")
    pd.concat(acts_all).to_csv(OUT / "theme_rates_acts.csv", index=False, encoding="utf-8-sig")
    wr = pd.DataFrame(words_all)
    wr.to_csv(OUT / "theme_word_rates.csv", index=False, encoding="utf-8-sig")
    md += ["## Per-word rates (Ecerinis vs Seneca mean)", "", "| pipeline | theme | word | Ecerinis rate (count) | Seneca mean |",
           "|---|---|---|---|---|"]
    for (pipe, theme, w), g in wr.groupby(["pipeline", "theme", "word"], sort=False):
        e = g[g.play == "Ecerinis"].iloc[0]
        md.append(f"| {pipe} | {theme} | {w} | {e.rate:.2f} ({e['count']}) | {g[g.play != 'Ecerinis'].rate.mean():.2f} |")
    md += ["", "Note: the original act files lack Phaedra's prelude and take Ecerinis from a different TEI version "
           "(see A1); the v2 acts are cut from the v2 play texts."]
    (OUT / "theme_rates_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
