# Robustness checks: summary

Two pipelines are compared throughout:
- **original**: the conference pipeline, unchanged (saved lemmas and named-entity list; tag `v0.1-conference-2026`);
- **v2**: the A1 re-lemmatization (LatinCy 3.9.8, with the approved fixes).

The model settings are the notebooks' own: gensim LDA, `passes=20`, `no_below=2`, `no_above=0.5`. Keyword lists are the top 20 by relevance (λ = 0.6). Theme labels are the author's; nothing here interprets them. Each section points to its detailed report.

## 1. What changed after normalization (A1)

Details: `a1_v2/REVIEW_v2.md`, `a1_v2/validation.md`, `a1_v2/token_lists_v2.md`.

- **The original named-entity list removed a large share of Ecerinis.** The list adds a lemma after a single proper-noun tag, and Ecerinis's source capitalizes the first word of every verse line.
  - In the original pipeline, Ecerinis's 2,330 content tokens fall to **1,660 after named-entity removal**: 29% of the play.
  - In v2 they fall to **2,198**; only 124 tokens are removed as names.
  - 284 of the 285 wrongly listed lemmas came from capitalized tokens.
- **v2 changes:**
  - Ecerinis text from the pinned NeoLatDraCor TEI, with 3 logged corrections.
  - Line-initial lowercasing, applied by the same rule to every play.
  - LatinCy 3.9.8, pinned by commit and sha256.
  - 650 context-checked names (7 lemmas decided token by token).
  - A 29-entry spelling map.
  - 136 lemma fixes, each checked against LiLa and Morpheus.
- **Lemma coverage in LiLa** rises from 88.7% of kept lemma types to 92.3% (97.6% → 98.5% of tokens).
- **Two lemma errors sit behind seed 42's Topic 7 keywords:**
  - 6 of the *uindico* tokens in Hercules Oetaeus are *vindicem* (from *vindex*);
  - every Seneca *pons* is *ponti* (*pontus*, the sea), while Ecerinis's *pons* tokens are real bridges. The link between Ecerinis and Seneca through *pons* is therefore an artefact.
- **Model input.** The Ecerinis tokens left after the dictionary filter go from 377 (original) to 416 (v2). The dictionary goes from 1,580 to 1,600 types.

## 2. Which k the rule selects (A2)

The rule is unchanged: c_v coherence minus adjacent-model overlap; 50 seeds (0–49); mean trade-off; ties within 1 SE go to the smallest k. Details: `a2_seeds/a2_summary.md`.

| | original | v2 |
|---|---|---|
| Rule-selected k | **8**, tied with 9 (within 1 SE) | **9**, no tie |
| Wins out of 50 seeds | k=9: 13, k=8: 9, k=5: 7, k=7: 7, k=4: 5, k=6: 5, k=3: 3, k=2: 1 | k=3: 9, k=4: 9, k=7: 8, k=8: 7, k=9: 7, k=5: 4, k=6: 4, k=2: 2 |
| Representative seed (co-assignment closest to consensus) | 25 (k = 8) | 29 (k = 8), 35 (k = 9) |

The win counts are spread out in both pipelines. No k wins in more than 26% of seeds.

## 3. Does Ecerinis's dominant theme (Topic 7 at k = 8) hold across seeds and nearby k?

Details: `a2_seeds/a2_summary.md` and `a3_own_topics/own_topics_summary.md`.

- **Topic 7 rarely recurs.** Its defining grouping (Ecerinis, Medea and Hercules Oetaeus sharing a dominant topic) appears in:
  - **1/50 seeds** in the original pipeline at k = 8 (seed 42 itself);
  - **3/50** in v2 at k = 8 and **2/50** at k = 9.
- **When the triad does recur in v2, its vocabulary is different.** The Jaccard overlap with seed 42's Topic 7 words is 0.10–0.16 (top 20 by relevance).
- **No Seneca play is a regular partner.** No play shares Ecerinis's dominant topic in more than 20% of seeds:
  - original, k = 8: Thyestes 20%, Medea 14%, Hercules Oetaeus 10%;
  - v2, k = 8: Medea 18%;
  - v2, k = 9: Hercules Oetaeus 16%.
- **Ecerinis has a topic to itself in 32–44% of seeds, not "usually".** This corrects my earlier wording.

| | Ecerinis alone in its topic | Seneca plays: median (range) | Ecerinis's rank of 11 |
|---|---|---|---|
| original, k = 8 | 32% (16/50) | 28% (12–42%) | 4 |
| v2, k = 8 | 40% (20/50) | 26% (20–46%) | 2 |
| v2, k = 9 | 44% (22/50) | 27% (14–46%) | 2 |

- **Ecerinis's topic vocabulary is among the most stable of any play.** Across all 50 seeds, whether or not the topic is shared:

  | | Words in its topic's top 20 in ≥80% of seeds | Mean Jaccard to the representative seed | Rank of 11 |
  |---|---|---|---|
  | original | 2 (*lis* 96%, *actus* 90%) | 0.36 | 3rd |
  | v2, k = 8 | 3 (*lis* 92%, *atrox* 90%, *actus* 86%) | 0.42 | 2nd |
  | v2, k = 9 | 3 | 0.45 | 2nd |

  The play with the most stable vocabulary is Octavia (0.46–0.50), or Hercules Oetaeus in the original pipeline (9 words ≥80%).
- **Ecerinis's next-best topic is almost always one no play is dominant in.** This is the topic other than its dominant one under which its words are most likely, the same contrastive measure as in A3.

  | | Next-best topic is dominant in no play | If picked at random |
  |---|---|---|
  | original | 48/50 seeds | 27% |
  | v2, k = 8 | 48/50 seeds | 27% |
  | v2, k = 9 | 49/50 seeds | 35% |

  - The next-best topic is Octavia's in only 1–2 seeds per configuration.
  - The median margin over it is 351–441 nats (0.9–1.1 per token).
  - Ecerinis's dominant topic is also its maximum-likelihood topic in every seed.

## 4. Attribution findings (A3)

Details: `a3_attribution/a3_summary.md`.

- **The brief's attribution method only reproduces Ecerinis's word counts.** In every model Ecerinis's topic weight is 0.998. Gensim's per-word phi values are then just Ecerinis's word counts, so they can't show which words pull it into a topic. I added a contrastive measure, labelled as supplementary: count × (log p(w | topic) − log p(w | next-best topic)).
- **Conference model (original, seed 42, Topic 7):**
  - The words carrying Ecerinis into the topic are *lis, forum, actus, inuado, rabies, pons, potior, largus, plebs*. None of them is among Topic 7's top 20 by relevance except *inuado* and *pons*.
  - Only 8 of Topic 7's top 20 occur in Ecerinis at all, each 1–3 times.
  - Topic 7's top words come from the Seneca plays: *uoltus, uindico, uolucer, axis, colus, glacialis, ursa, harundo*.
- **In the four other models** (original seed 25; v2 seeds 42, 35 and 29), Ecerinis has a topic of its own, and all 20 of that topic's top words occur in Ecerinis.
- **Correction to my earlier report.** I said the next-best topic was Octavia's in three of these models. That is true of exactly the three representative seeds, but across 50 seeds it is a 1–2-seed exception (section 3).

## 5. Act level (k = 24): which topics each Ecerinis act falls into, and how stable this is

Details: `a2_seeds/acts_summary.md` (21 seeds) and `a2_seeds/acts_pairs_summary.md` (101 seeds).

**Seed 42 (conference model):**

| Act | Topic and the author's label | Shared with |
|---|---|---|
| Ece 1 | T11, "Order, Moral Duty, and Emerging Conflict" | Aga 1, Pho 1 |
| Ece 2, Ece 5 | T19, "Civic Judgement, Incited Rage, and Public Punishment" | Thy 1 |
| Ece 3 | T12, "Material Power, Anticipation, and Kinship" | 17 Seneca acts |
| Ece 4 | T4, "Fate, Grief, and the Sea" | Oed 4, Tro 4 |

**How stable these assignments are:**
- **The act-level topic vocabularies barely recur across seeds.** The mean Jaccard of each Ecerinis act's topic to its version in the representative seed is 0.02–0.18 (original) and 0.03–0.22 (v2).
- **Chance test (101 seeds, 0–99 and 42).** For each pairing: the share of seeds in which the two acts share a dominant topic, against the same share for all 1,540 act pairs.

| Pairing | original: share (percentile rank) | v2: share (percentile rank) |
|---|---|---|
| Ece 1 – Aga 1 | 0.119 (48th) | 0.079 (23rd) |
| Ece 1 – Pho 1 | 0.149 (59th) | 0.149 (50th) |
| Ece 2 – Thy 1 | 0.059 (16th) | 0.010 (0.3rd) |
| Ece 5 – Thy 1 | 0.079 (28th) | 0.129 (44th) |
| Ece 2 – Ece 5 | 0.059 (16th) | 0.030 (3.5th) |
| Ece 4 – Oed 4 | 0.059 (16th) | 0.089 (28th) |
| Ece 4 – Tro 4 | 0.040 (7th) | 0.050 (9.5th) |
| Ece 1 – HF 2 (most frequent in the 21-seed run) | 0.178 (68th) | 0.188 (60th) |
| Ece 3 – HF 2 (most frequent in the 21-seed run) | 0.208 (73rd) | 0.297 (80th) |
| **All act pairs** | median 0.129, 95th percentile 0.386 | median 0.158, 95th percentile 0.436 |

- **No seed-42 pairing reaches the 95th percentile of the all-pairs baseline,** and most sit below its median.
- **The pairs share little vocabulary.** The words that pass the dictionary filter and occur in both acts number 15–51 per pair (original) and 17–72 (v2), most only once or twice in each act. Frequent shared words (*pater, regnum, deus, scelus, manus*) are removed by `no_above=0.5`.

## 6. Keyness: Ecerinis vs the ten Seneca plays combined

v2 lemmas, counted before the dictionary filter; the 226 lemmas with ≥3 occurrences in Ecerinis. Details: `keyness/keyness_summary.md`.

**The counts are small, so read the effect sizes (log ratio), not the p-values.**

- **17 lemmas pass Bonferroni p < 0.05, all over-used:** *annuo, tyrannis, crux, lis, marchia, patro, progredior, ausus, nocuus, inspecto, actus, atrox, forum, ordo, homo, finis, tollo*.
- **No lemma with ≥3 Ecerinis occurrences is significantly under-used.** The largest under-use is *dies* (log ratio −1.65).
- **Common Seneca words Ecerinis barely uses** (fewer than 3 times; supplementary, uncorrected): *grauis* 0 vs 148, *malum* 1/164, *coniux* 1/137, *fatum* 2/153, *rex* 2/138.
- **Overlap with Ecerinis's topic.** Of the top 40 over-used lemmas, 16 are in Ecerinis's topic's top 20 (v2 seeds 29 and 35). 22 never reach the model:
  - lemmas found in Ecerinis only (*annuo, tyrannis, crux, marchia* …) are removed by `no_below=2`;
  - common lemmas (*ordo, homo, finis, tollo*) are removed by `no_above=0.5`.
- **To check:** *marchia* (possibly the place name, the March), *ausus* and *nocuus* are unusual lemmas.

## 7. A5 part 2: theme word-family rates

The word lists are the author's (`data/theme_lexicon.json`); these are lexicon counts, not model output. Rates are per 1,000 tokens, with bootstrap 95% intervals from resampled 200-token chunks (50-token chunks for acts). Details: `a5_theme_rates/theme_rates_summary.md`.

| Theme (v2) | Ecerinis [95% CI] | Seneca mean (range) | Rank of 11 | Seneca plays whose interval doesn't overlap Ecerinis's |
|---|---|---|---|---|
| Invasion | 9.6 [4.6–15.0] | 3.7 (1.7–6.2) | 1 | Phaedra, Oedipus |
| Deceit | 5.5 [3.2–8.2] | 2.4 (0.6–3.6) | 1 | Hercules Furens, Oedipus |
| Punishment | 5.5 [3.2–8.2] | 3.3 (1.8–5.0) | 1 | none |
| Fate | 3.6 [1.8–5.5] | 5.4 (1.9–8.9) | 7 | Oedipus, Hercules Oetaeus (both higher) |

- **The original tokens give the same ordering.** The per-word rates reproduce the brief's table.
- **Fate includes *fatum*,** because the brief lists it in that row. *fatum* is much rarer in Ecerinis (0.9 vs 3.5 per 1,000), and that lowers the family rate.
- **The act intervals are wide,** and acts with zero hits have a degenerate [0–0] interval.
- **The `no_above` comparison (A5 part 1) was not run.**

## 8. A4: heatmaps

- **The two conference topic heatmaps are redrawn from the saved models** with empty topics labelled; the originals in `figures/` are unchanged. "Empty" means no document has a weight of 0.05 or more.
  - Play level: T3, T5 and T8 are empty.
  - Act level: T6, T14, T16, T18, T23 and T24 are empty.
- **The duplicate label "Restraint & Ethical Reflection" is on T3 and T8,** both empty. They are told apart by their topic numbers; relabelling is left to the author.
- **The co-assignment heatmaps (A2)** show plays or acts against each other, not topics, so they have no empty topics.

## Flags

- **The original named-entity list removed 29% of Ecerinis's tokens** (section 1). Any original-pipeline result for Ecerinis rests on 71% of its text.
- **Topic 7's triad is a single-seed result** (1/50). In seed 42, Phaedra's two largest topic weights are almost equal (0.334 vs 0.328).
- **The representative seeds are atypical for Ecerinis's next-best topic** (sections 3–4).
- **The act-level seed-42 pairings are at or below chance** (section 5).
- **The dictionary filter removes both Ecerinis-only words (`no_below`) and shared theme words (`no_above`).** The model sees neither the strongest keyness words nor most of the theme lexicon.
- **The original pipeline contains an empty lemma (the empty string).** It is one lemma type carried by 64 tokens across all 11 plays (11 in Ecerinis, including the medieval spelling *vendico*; see `a1_normalization/REVIEW.md`).
  - Because it occurs in every play, `no_above=0.5` removes it, so it never reaches the model.
  - It does count in that pipeline's token totals, for example the denominators of the original-token theme rates.
  - It was left unchanged.

## Figures

| File | What it shows |
|---|---|
| `a2_seeds/figures/fig_a2_tradeoff_curves.png` | Coherence, adjacent-model overlap and trade-off by k, mean ± 1 SD over 50 seeds, both pipelines |
| `a2_seeds/figures/fig_a2_wins.png` | Number of seeds in which each k has the highest trade-off |
| `a2_seeds/figures/fig_a2_coassignment_{original,v2}.png` | Share of seeds in which each pair of plays shares a dominant topic, at the rule-selected k and k = 8 |
| `a2_seeds/figures/fig_a2_coassignment_neighbours_{original,v2}.png` | The same at neighbouring k (supplementary) |
| `a2_seeds/figures/fig_a2_acts_{original,v2}.png` | Ecerinis acts × Seneca acts: share of 21 seeds sharing a dominant topic (k = 24) |
| `a3_attribution/figures/fig_a3_{pipeline}_seed{s}_k{k}.png` | Five models: words placing Ecerinis in its topic vs the topic's top words |
| `a4_heatmaps/fig_a4_play_topics_k8.png` | Conference play-level topic weights, empty topics labelled |
| `a4_heatmaps/fig_a4_act_topics_k24.png` | Conference act-level topic weights, empty topics labelled |
| `keyness/figures/fig_keyness_log_ratio.png` | Log ratio of the top 40 over-used and top 20 under-used lemmas in Ecerinis |
| `a5_theme_rates/figures/fig_a5_theme_rates_{v2,original}.png` | Theme-family rates per play with bootstrap 95% intervals, Ecerinis highlighted |
