# Robustness checks: summary

Two pipelines are compared throughout:
- **original**: the conference pipeline, unchanged (saved lemmas and named-entity list; tag `v0.1-conference-2026`);
- **v2**: the A1 re-lemmatization (LatinCy 3.9.8, with the approved fixes).

The model settings are the notebooks' own: gensim LDA, `passes=20`, `no_below=2`, `no_above=0.5`. Keyword lists are the top 20 by relevance (λ = 0.6). Theme labels are the author's; nothing here interprets them. Each section points to its detailed report.

## 1. What changed after normalization (A1)

Details: `a1_v2/REVIEW_v2.md`, `a1_v2/validation.md`, `a1_v2/token_lists_v2.md`.

- **The original named-entity list removed a large share of Ecerinis.** The list adds a lemma after a single proper-noun tag, and Ecerinis's source capitalizes the first word of every verse line.
  - In the original pipeline, Ecerinis's 2,330 content tokens fall to **1,660 after named-entity removal**: 29% of the play.
  - In v2 they fall to **2,195**; only 127 tokens are removed as names. This count includes *marchia*, the March of Treviso, added as a name on 2026-11-22 (section 6).
  - 284 of the 285 wrongly listed lemmas came from capitalized tokens.
- **v2 changes:**
  - Ecerinis text from the pinned NeoLatDraCor TEI, with 3 logged corrections.
  - Line-initial lowercasing, applied by the same rule to every play.
  - LatinCy 3.9.8, pinned by commit and sha256.
  - 651 context-checked names (7 lemmas decided token by token).
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
- **The act-level topic vocabularies barely recur across seeds.** The mean Jaccard of each Ecerinis act's topic to its version in the representative seed is 0.02–0.18 (original) and 0.02–0.11 (v2).
- **Chance test (101 seeds, 0–99 and 42).** For each pairing: the share of seeds in which the two acts share a dominant topic, against the same share for all 1,540 act pairs.

| Pairing | original: share (percentile rank) | v2: share (percentile rank) |
|---|---|---|
| Ece 1 – Aga 1 | 0.119 (48th) | 0.099 (32nd) |
| Ece 1 – Pho 1 | 0.149 (59th) | 0.149 (50th) |
| Ece 2 – Thy 1 | 0.059 (16th) | 0.079 (25th) |
| Ece 5 – Thy 1 | 0.079 (28th) | 0.099 (32nd) |
| Ece 2 – Ece 5 | 0.059 (16th) | 0.099 (32nd) |
| Ece 4 – Oed 4 | 0.059 (16th) | 0.050 (14th) |
| Ece 4 – Tro 4 | 0.040 (7th) | 0.069 (21st) |
| Ece 1 – HF 2 (most frequent in the 21-seed run) | 0.178 (68th) | 0.178 (59th) |
| Ece 3 – HF 2 (most frequent in the 21-seed run) | 0.208 (73rd) | 0.267 (79th) |
| **All act pairs** | median 0.129, 95th percentile 0.386 | median 0.158, 95th percentile 0.406 |

- **No seed-42 pairing reaches the 95th percentile of the all-pairs baseline,** and most sit below its median.
- **The pairs share little vocabulary.** The words that pass the dictionary filter and occur in both acts number 15–51 per pair (original) and 17–72 (v2), most only once or twice in each act. Frequent shared words (*pater, regnum, deus, scelus, manus*) are removed by `no_above=0.5`.

## 6. Keyness: Ecerinis vs the ten Seneca plays combined

v2 lemmas, counted before the dictionary filter; the 225 lemmas with ≥3 occurrences in Ecerinis. Details: `keyness/keyness_summary.md`.

**The counts are small, so read the effect sizes (log ratio), not the p-values.**

- **The keyness results now exclude *marchia*.** It is the March of Treviso (Ecerinis vv. 148, 174 and 180: "in Marchia … Estensis Azo marchio"), so it is treated as a named entity (`data/v2/named_entities_additions.csv`).
  - It was in the first keyness run (5th by log ratio, 3 occurrences against 0 in Seneca).
  - LiLa lists *marchia* only as a common noun, which is why the evidence rule had kept it as a word.
  - **Play-level LDA results are unaffected.** *marchia* occurs in one play only, so `no_below=2` already kept it out of the model; I checked that the play-level model input is identical before and after.
  - **The v2 act-level analyses were rerun after the change** (`a2_seeds/acts_summary.md`, `acts_pairs_summary.md`; section 5 shows the rerun). *marchia* occurs in two Ecerinis acts, so it had been in the act-level vocabulary. The original-pipeline act results are unchanged.
- **For keyness only, *ausus* is now counted as *audeo* (author's decision).**
  - Ecerinis's *ausibus* (3 tokens) is the noun *ausus, -ūs*, and its lemma is correct.
  - But v2 lemmatizes all 23 of Seneca's *aus-* participle tokens as *audeo* (*ausa* 8, *ausus* 8, *ausae* 2, *ausos* 2, *ausas* 1, *ausi* 1, *ausurus* 1). *ausum* and *ausis* do not occur, and no Seneca token is lemmatized *ausus*.
  - Mapped, *audeo* is Ecerinis 4 vs Seneca 51: log ratio +0.58, G² 0.5, Bonferroni p = 1. It is not a keyword.
  - The LDA input is unchanged.
- ***nocuus* is marked as a lexical keyword** (lemma checked, kept). Related lemmas, Ecerinis / Seneca combined: *nocuus* 3 / 0, *noxius* 1 / 8, *nocens* 0 / 32, *noceo* 0 / 28.
- **15 lemmas pass Bonferroni p < 0.05, all over-used:** *annuo, tyrannis, crux, lis, patro, progredior, nocuus, inspecto, actus, atrox, forum, ordo, homo, finis, tollo*.
- **No lemma with ≥3 Ecerinis occurrences is significantly under-used.** The largest under-use is *dies* (log ratio −1.65).
- **Common Seneca words Ecerinis barely uses** (fewer than 3 times; supplementary, uncorrected): *grauis* 0 vs 148, *malum* 1/164, *coniux* 1/137, *fatum* 2/153, *rex* 2/138.
- **Overlap with Ecerinis's topic.** Of the top 40 over-used lemmas, 16 are in Ecerinis's topic's top 20 (v2 seeds 29 and 35). 22 never reach the model:
  - lemmas found in Ecerinis only (*annuo, tyrannis, crux* …) are removed by `no_below=2`;
  - common lemmas (*ordo, homo, finis, tollo*) are removed by `no_above=0.5`.
- **Ecerinis contexts:** *ausibus* at vv. 312, 431 and 443; *nocuos*, *nocuis* and *nocuum* at vv. 313, 597 and 619 (verse numbers of the NeoLatDraCor edition; `src/verses.py`).

## 7. A5 part 2: theme word-family rates (author-chosen lexicon counts, not model output)

**Everything in this section is a count of author-chosen word lists, not model output.** The lexicon is `data/theme_lexicon.json` (v2: 17 families, `context/theme_lexicon_v2_brief.md` as revised by `context/lexicon_audit_decisions.md`). Counts use v2 tokens before the dictionary filter. Rates are per 1,000 tokens, with bootstrap 95% intervals from resampled 200-token chunks (50-token chunks for acts). Details: `a5_lexicon_v2/rates/lexicon_rates_summary.md`; audit: `a5_lexicon_v2/lexicon_audit.md` (step 1) and `lexicon_audit_revised.md`.

**Lexicon-only rules** (`src/theme_lexicon.py`; the LDA input is unchanged):
- *vadum* tokens that v2 lemmatizes as *uas* count as *uadum* (a known v2 lemma error; see Flags).
- Not counted: *furabor* under *furor*; *diti*, *dites* under *deus*; the adjective *foedus* 'foul' (only nouns count); *summus*/*supremus* forms under *superus* (only *super-* forms count).
- *prodo* and *uendo* count only for the tokens the author marked as betrayal (`data/lexicon_marks/`): 6 Seneca *prodo* tokens and Ecerinis *vendidere* (v. 227). *uendico* ('claim', Ecerinis vv. 83, 298) is not counted under *uindico*; *uindico* has both senses and the lexicon cannot separate them.
- *fingo* is not in any family. 19 listed lemmas never occur in the corpus and are kept (they add 0).

### Play level

† = thin family: fewer than 5 Ecerinis tokens; read its rate with the raw count.

| Family | Ecerinis [95% CI] | Ecerinis tokens | Seneca mean (range) | Rank of 11 | Seneca plays whose interval doesn't overlap Ecerinis's |
|---|---|---|---|---|---|
| invasion_conquest | 10.0 [5.5–16.4] | 22 | 7.8 (2.3–18.9) | 3 | Phaedra (lower), Oedipus (lower) |
| deceit_betrayal | 8.7 [5.0–12.8] | 19 | 4.2 (0.8–6.1) | 1 | Hercules Furens (lower), Oedipus (lower) |
| punishment_vengeance | 3.6 [1.4–5.9] | 8 | 5.1 (2.5–8.4) | 8 | none |
| fate_fortune | 4.1 [1.4–7.3] | 9 | 6.6 (3.1–9.9) | 8 | none |
| natural_cosmic_order | 17.3 [10.9–25.0] | 38 | 10.8 (3.6–22.1) | 2 | Phoenissae (lower), Troades (lower) |
| providence_divine | 10.5 [4.6–17.7] | 23 | 8.3 (6.1–13.2) | 2 | none |
| piety_virtue | 10.5 [5.0–16.8] | 23 | 8.0 (4.0–14.7) | 4 | none |
| sea_water | 5.5 [0.9–10.9] | 12 | 15.8 (6.4–32.8) | 11 | Troades (higher), Agamemnon (higher), Medea (higher) |
| grief_lament | 3.6 [0.9–6.8] | 8 | 7.8 (2.8–19.3) | 10 | Troades (higher), Octavia (higher), Hercules Oetaeus (higher) |
| memory_report † | 1.4 [0.0–3.2] | 3 | 1.8 (0.0–3.3) | 7 | none |
| community_commune | 15.0 [9.6–20.1] | 33 | 9.0 (5.6–16.2) | 2 | Phaedra (lower), Medea (lower) |
| law_judgment | 14.6 [6.8–22.4] | 32 | 3.8 (1.3–5.6) | 1 | Troades (lower), Phaedra (lower), Agamemnon (lower), Hercules Furens (lower), Oedipus (lower), Thyestes (lower), Hercules Oetaeus (lower) |
| rule_kingship | 10.0 [4.1–17.7] | 22 | 17.8 (11.7–24.6) | 11 | none |
| tyranny_servitude | 7.7 [4.1–11.8] | 17 | 2.6 (1.0–4.4) | 1 | Phoenissae (lower), Phaedra (lower), Agamemnon (lower), Oedipus (lower), Thyestes (lower), Hercules Oetaeus (lower) |
| lineage_kin | 31.9 [19.1–45.6] | 70 | 28.2 (19.5–54.4) | 2 | Phoenissae (higher) |
| rage_fury | 15.0 [7.3–24.1] | 33 | 11.5 (7.9–20.3) | 3 | none |
| discord_strife | 2.7 [0.9–4.6] | 6 | 0.6 (0.0–1.6) | 1 | Troades (lower), Agamemnon (lower), Medea (lower), Octavia (lower), Oedipus (lower), Hercules Oetaeus (lower) |

- Ecerinis has 2,195 v2 tokens. Rank 1 = highest rate.
- **The Ecerinis counts are small** (3–70 tokens per family), so the intervals are wide; most families overlap most Seneca plays.

### Act level

Percentile = mid-rank percentile of the act's rate among all 56 acts (50 = median). Full table: `a5_lexicon_v2/rates/lexicon_rates_summary.md`; all 56 acts with intervals: `rates_acts.csv`; heatmap: `fig_lexicon_v2_act_percentiles.png`.

- **Acts are short** (Ece 4 has 271 tokens, Ece 5 has 350), so most act counts are 0–10 tokens and the act intervals are wide.
- **Many acts tie at 0 for the smaller families,** and a tie at zero shares one mid-rank percentile (e.g. 21 for memory_report, 32 for discord_strife). A low-30s percentile can simply mean 'no tokens'.
- **Ecerinis acts at or above the 90th percentile:** law_judgment in Ece 1, 2, 3 and 5 (94–99); tyranny_servitude in Ece 2, 3 and 4 (92–99); deceit_betrayal in Ece 1 and 2 (94, 96); discord_strife in Ece 1, 3 and 4 (90–94, 1–2 tokens each); piety_virtue in Ece 3 and 4 (99, 94); natural_cosmic_order and providence_divine in Ece 3 (94, 96); invasion_conquest in Ece 4 (94); community_commune in Ece 2 (92); lineage_kin in Ece 1 (92); rage_fury in Ece 2 (97).
- **Ecerinis acts at or below the 10th percentile (all with 0 tokens):** sea_water in Ece 1, 2 and 5; rule_kingship in Ece 4 and 5; piety_virtue and fate_fortune in Ece 1; punishment_vengeance and grief_lament in Ece 4.

### 'Broken faith' collocations (author-chosen collocation measure)

A separate measure, not part of the theme rates. *fides* / *fidus* within ±5 tokens (same speech) of *rumpo, frango, uiolo, absum, neglego, nego, fallo, credo, iuro, sperno, laedo*, on the full v2 lemma sequence before stopword and part-of-speech filtering. Each automatic hit was classified by hand. Counts with passages, not rates; details: `a5_collocations/collocations_summary.md`.

| | *fides*/*fidus* tokens | Automatic hits | broken | pledge | other |
|---|---|---|---|---|---|
| Ecerinis | 7 | 5 | 2 (vv. 320, 472) | 1 (v. 480) | 2 (vv. 202, 360) |
| Seneca (10 plays) | 117 | 11 | 4 (Pho 280, 293, 588, 649) | 5 (Tro 611, Med 1003, Oct 352, Thy 294, 1099) | 2 (Pha 161, Oct 275) |

- The four Ecerinis passages named in the decisions (vv. 202, 320, 472, 480–481) are all found.
- Betrayal in Ecerinis is also expressed without *fides* (e.g. *transfugas*, v. 320; *vendidere*, v. 227; *creditus nullis*, v. 539), which this measure does not count.

### Earlier four-family lexicon (v1)

The rates reported before this revision used `data/theme_lexicon_v1.json` (`src/a5_theme_rates.py`, `a5_theme_rates/`; v2 tokens shown):

| Theme (v2) | Ecerinis [95% CI] | Seneca mean (range) | Rank of 11 | Seneca plays whose interval doesn't overlap Ecerinis's |
|---|---|---|---|---|
| Invasion | 9.6 [4.6–15.0] | 3.7 (1.7–6.2) | 1 | Phaedra, Oedipus |
| Deceit | 5.5 [3.2–8.2] | 2.4 (0.6–3.6) | 1 | Hercules Furens, Oedipus |
| Punishment | 5.5 [3.2–8.2] | 3.3 (1.8–5.0) | 1 | none |
| Fate | 3.6 [1.8–5.5] | 5.4 (1.9–8.9) | 7 | Oedipus, Hercules Oetaeus (both higher) |

The v1 families are not comparable one to one with v2 (e.g. v1 'Invasion' and v2 invasion_conquest have different word lists).

## 7b. A5 part 1: does relaxing `no_above` move Ecerinis's topic toward the shared vocabulary?

v2 tokens; 50 seeds; k = 7–9; seed 42 for the single-model view. Details: `a5_no_above/no_above_summary.md`.

**Settings:**
- `no_above` = 0.5 (baseline), 0.8 and 1.0.
- **1.0 with TF-IDF weighting:** counts × log2(11 / plays containing the word). This is needed because at 1.0 a few very frequent words (*manus, scelus, magnus, deus, regnum*) dominate every topic. TF-IDF gives a word in all 11 plays weight 0.
- `keep_n` was not used: it keeps the most frequent words, which are the problem.

"Shared words" means the topic's top-20 words that occur in more than 5 of the 11 plays, i.e. the words `no_above=0.5` removes.

| Setting | Rule-selected k (within 7–9) | Ecerinis alone (k = 8 / 9) | Shared words in Ecerinis's top 20 (k = 8) | Brief's theme words in its top 20 | Most frequent partners (k = 8) |
|---|---|---|---|---|---|
| 0.5 | 9 (no tie) | 40% / 44% | 0 | *ultio* in 6–12% of seeds | Medea 18%, Oedipus 16%, Thyestes 16% |
| 0.8 | 7 (no tie) | 32% / 34% | 11.7 | *inuado*, *ultio* ≤ 4% | Octavia 28%, Thyestes 24%, Hercules Furens 18% |
| 1.0 | 7 (tied with 8) | 24% / 26% | 17.8 | *fatum* 14–24%, *ignis* 8–22%, *hostis* 4–8% | Medea 58%, Hercules Furens 52%, Phaedra 50% |
| 1.0 + TF-IDF | 7 (no tie) | 34% / 34% | 1.3 | *ultio* 4–12%, *inuado* 2–8% | Octavia 16%, Thyestes 16%, Troades 14% |

**At 0.8:**
- **Shared words do enter Ecerinis's topic.** The most stable are *homo* (80% of seeds at k = 8), *ordo* (70%), *tyrannus* (68%), *iustus* and *fames* (54%).
- **Its own words remain:** *lis, atrox, actus*.
- **The brief's theme words still almost never appear,** and neither do the plays that shared Topic 7. Medea and Hercules Oetaeus are not among the top partners at k = 8; Hercules Oetaeus reaches 18% at k = 9.

**At 1.0:**
- **The model degenerates.** Most plays share one topic of corpus-wide common words (*deus* 100%, *pater* 88–98%, *manus, scelus, magnus, regnum*).
- **Ecerinis falls into that topic with half or more of the Seneca plays.** *fatum, ignis* and *hostis* appear only as part of it.
- **The trade-off is negative at every k.**

**With TF-IDF at 1.0,** Ecerinis's topic returns to its own vocabulary: *lis* 100%, *atrox, actus, forum, triplex, pons, plebs*. On average only 1.3–1.5 of its top 20 are shared words.

**The rule-selected k changes** from 9 to 7 under every relaxed setting.

**Seed 42:**

| Setting | k = 8 | k = 9 |
|---|---|---|
| 0.5 | alone | with Agamemnon |
| 0.8 | alone; carried by *homo, tyrannus, ordo, lis, atrox* | with Agamemnon, Medea, Thyestes |
| 1.0 | with 9 of the 10 Seneca plays | with 9 of the 10 Seneca plays |
| 1.0 + TF-IDF | with Agamemnon, Oedipus | with Agamemnon |

In every one of these models the contrastive next-best topic for Ecerinis is a topic no play is dominant in.

**Answer to the brief's question.** Relaxing `no_above` to 0.8 brings shared words into Ecerinis's topic (*homo, ordo, tyrannus, iustus, fames*), but not the theme families in `data/theme_lexicon_v1.json` (the lexicon at the time), and not a stable link to Medea or Hercules Oetaeus. At 1.0 the shared vocabulary takes over the whole model rather than Ecerinis's topic in particular.

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
- **The dictionary filter removes both Ecerinis-only words (`no_below`) and shared theme words (`no_above`).** The model sees neither the strongest keyness words nor most of the theme lexicon. Relaxing `no_above` does not bring the theme lexicon into Ecerinis's topic (section 7b).
- **The original pipeline contains an empty lemma (the empty string).** It is one lemma type carried by 64 tokens across all 11 plays (11 in Ecerinis, including the medieval spelling *vendico*; see `a1_normalization/REVIEW.md`).
  - Because it occurs in every play, `no_above=0.5` removes it, so it never reaches the model.
  - It does count in that pipeline's token totals, for example the denominators of the original-token theme rates.
  - It was left unchanged.
- **Known v2 lemma error, not yet fixed: *vadum* 'ford' is lemmatized as *uas* 'vessel'.** This affects all 5 *vadum* tokens: Ece 4, vv. 482 and 504; Oed 2, v. 285; Thy 2, v. 376; HO 2, v. 587 (edition verse numbers, `src/verses.py`).
  - The theme lexicon counts them as *uadum* through a lexicon-only token rule (`_token_rules` in `data/theme_lexicon.json`).
  - The LDA input still has *uas*, so every v2 model result (A2, A3, act level, keyness, `no_above`) includes the error.
  - Fixing it means adding a v2 lemma fix and rerunning those analyses. Deferred.

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
| `a5_theme_rates/figures/fig_a5_theme_rates_{v2,original}.png` | v1 (four-family) theme rates per play with bootstrap 95% intervals, Ecerinis highlighted |
| `a5_lexicon_v2/rates/figures/fig_lexicon_v2_plays.png` | Lexicon v2: rate per play for each of the 17 families, bootstrap 95% intervals, Ecerinis highlighted (author-chosen lexicon counts) |
| `a5_lexicon_v2/rates/figures/fig_lexicon_v2_act_percentiles.png` | Lexicon v2: families × 18 acts (Ece 1–5 and 13 Seneca acts), coloured by percentile among all 56 acts (author-chosen lexicon counts) |
