# Keyness: Ecerinis vs the ten Seneca plays combined

v2 tokens (A1-normalized content lemmas), before the dictionary filter. Ecerinis 2,195 tokens; Seneca 41,931 tokens. Tested: the 225 lemmas with frequency ≥ 3 in Ecerinis. G² = log-likelihood (Rayson & Garside); p from χ² (1 df), Bonferroni-corrected for the number of lemmas tested. Log ratio = log2 of the ratio of relative frequencies (Hardie); +1 = twice as frequent in Ecerinis. * = a zero count replaced by 0.5.

**The counts are small (most tested lemmas occur 3–6 times in Ecerinis), so the effect sizes (log ratio) matter more than the p-values.** Bonferroni is conservative: few lemmas pass it.

- Lemmas passing Bonferroni p < 0.05: 15 (15 over-used, 0 under-used): annuo, tyrannis, crux, lis, patro, progredior, nocuus, inspecto, actus, atrox, forum, ordo, homo, finis, tollo.
- Over-used lemmas (log ratio > 0): 189; under-used: 36.
- Of the top 40 over-used, 16 are in Ecerinis's topic's top 20 (v2 seed 29, k = 8), 16 at seed 35, k = 9; 22 are removed by the dictionary filter.
- Topic columns: in the top 20 by relevance (λ = 0.6) of Ecerinis's dominant topic in the v2 representative models (seed 29, k = 8; seed 35, k = 9), and the share of the 50 seeds (v2, k = 8) in which the lemma is in that topic's top 20. 'In model vocab' = kept by no_below=2 / no_above=0.5.

## Lemma notes

- **ausus → audeo (keyness only).** Ecerinis's *ausibus* is the noun *ausus, -ūs* and its lemma is correct, but LatinCy 3.9.8 lemmatizes all of Seneca's *aus-* participle forms as *audeo*, so the two would be counted apart. For keyness only, *ausus* is counted as *audeo* in both corpora (the LDA input is unchanged).
  - Before the mapping: *ausus* Ecerinis 3 / Seneca 0; *audeo* Ecerinis 1 / Seneca 51.
  - Seneca's *aus-* forms in v2 (23 tokens), all lemmatized *audeo*: ausa 8, ausus 8, ausae 2, ausos 2, ausas 1, ausi 1, ausurus 1. *ausum* and *ausis* do not occur. No Seneca token is lemmatized *ausus*.
  - Ecerinis's forms: *ausus* ← ausibus 3; *audeo* ← audes 1.
  - After the mapping: *audeo* Ecerinis 4 / Seneca 51.
  - *audeo* keyness: log ratio +0.58, G² 0.5, Bonferroni p 1.
- **nocuus: lexical keyword.** The lemma was checked against its contexts and kept as it is. Counts of related lemmas (v2, before the dictionary filter):

  | lemma | Ecerinis | Seneca combined |
  |---|---|---|
  | nocuus | 3 | 0 |
  | noxius | 1 | 8 |
  | nocens | 0 | 32 |
  | noceo | 0 | 28 |

## Top 40 over-used in Ecerinis (ranked by log ratio)

| rank | lemma | Ecerinis | Seneca | per 1,000 Ece / Sen | log ratio | G² | p (Bonferroni) | topic s29 k8 | topic s35 k9 | % of 50 seeds (k8) | in model vocab |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | annuo | 5 | 0 | 2.28 / 0.00 | +7.58* | 30.0 | 9.7e-06 |  |  | 0% | no |
| 2 | tyrannis | 5 | 0 | 2.28 / 0.00 | +7.58* | 30.0 | 9.7e-06 |  |  | 0% | no |
| 3 | crux | 4 | 0 | 1.82 / 0.00 | +7.26* | 24.0 | 2.2e-04 |  |  | 0% | no |
| 4 | lis | 6 | 1 | 2.73 / 0.02 | +6.84 | 30.4 | 8.0e-06 | ✓ | ✓ | 92% | yes |
| 5 | patro | 3 | 0 | 1.37 / 0.00 | +6.84* | 18.0 | 0.005 |  |  | 0% | no |
| 6 | progredior | 3 | 0 | 1.37 / 0.00 | +6.84* | 18.0 | 0.005 |  |  | 0% | no |
| 7 | nocuus (lexical keyword) | 3 | 0 | 1.37 / 0.00 | +6.84* | 18.0 | 0.005 |  |  | 0% | no |
| 8 | inspecto | 3 | 0 | 1.37 / 0.00 | +6.84* | 18.0 | 0.005 |  |  | 0% | no |
| 9 | triplex | 3 | 1 | 1.37 / 0.02 | +5.84 | 13.6 | 0.051 | ✓ | ✓ | 52% | yes |
| 10 | pons | 3 | 1 | 1.37 / 0.02 | +5.84 | 13.6 | 0.051 | ✓ | ✓ | 52% | yes |
| 11 | actus | 5 | 3 | 2.28 / 0.07 | +4.99 | 19.7 | 0.002 | ✓ | ✓ | 86% | yes |
| 12 | atrox | 6 | 4 | 2.73 / 0.10 | +4.84 | 23.0 | 3.7e-04 | ✓ | ✓ | 90% | yes |
| 13 | deuoueo | 3 | 2 | 1.37 / 0.05 | +4.84 | 11.5 | 0.158 | ✓ | ✓ | 56% | yes |
| 14 | desino | 3 | 2 | 1.37 / 0.05 | +4.84 | 11.5 | 0.158 | ✓ | ✓ | 54% | yes |
| 15 | forum | 4 | 3 | 1.82 / 0.07 | +4.67 | 14.8 | 0.028 | ✓ | ✓ | 62% | yes |
| 16 | plebs | 4 | 4 | 1.82 / 0.10 | +4.26 | 13.3 | 0.059 | ✓ | ✓ | 60% | yes |
| 17 | rabies | 4 | 4 | 1.82 / 0.10 | +4.26 | 13.3 | 0.059 | ✓ | ✓ | 70% | yes |
| 18 | patulus | 3 | 3 | 1.37 / 0.07 | +4.26 | 10.0 | 0.353 | ✓ | ✓ | 48% | yes |
| 19 | potior | 3 | 3 | 1.37 / 0.07 | +4.26 | 10.0 | 0.353 | ✓ | ✓ | 44% | yes |
| 20 | supernus | 3 | 3 | 1.37 / 0.07 | +4.26 | 10.0 | 0.353 | ✓ | ✓ | 50% | yes |
| 21 | adulter | 4 | 5 | 1.82 / 0.12 | +3.93 | 12.2 | 0.110 | ✓ | ✓ | 68% | yes |
| 22 | ordo | 7 | 9 | 3.19 / 0.21 | +3.89 | 21.0 | 0.001 |  |  | 0% | no |
| 23 | anxius | 3 | 4 | 1.37 / 0.10 | +3.84 | 8.9 | 0.658 | ✓ | ✓ | 52% | yes |
| 24 | series | 3 | 4 | 1.37 / 0.10 | +3.84 | 8.9 | 0.658 | ✓ | ✓ | 46% | yes |
| 25 | homo | 8 | 15 | 3.64 / 0.36 | +3.35 | 19.8 | 0.002 |  |  | 0% | no |
| 26 | iudex | 3 | 6 | 1.37 / 0.14 | +3.26 | 7.2 | 1 |  |  | 12% | yes |
| 27 | largus | 3 | 6 | 1.37 / 0.14 | +3.26 | 7.2 | 1 |  |  | 20% | yes |
| 28 | conuerto | 3 | 7 | 1.37 / 0.17 | +3.03 | 6.5 | 1 |  |  | 0% | no |
| 29 | finis | 9 | 23 | 4.10 / 0.55 | +2.90 | 18.3 | 0.004 |  |  | 0% | no |
| 30 | iustus | 5 | 13 | 2.28 / 0.31 | +2.88 | 10.1 | 0.340 |  |  | 0% | no |
| 31 | duro | 3 | 8 | 1.37 / 0.19 | +2.84 | 5.9 | 1 |  |  | 0% | no |
| 32 | subigo | 3 | 8 | 1.37 / 0.19 | +2.84 | 5.9 | 1 |  |  | 0% | no |
| 33 | subdo | 4 | 11 | 1.82 / 0.26 | +2.80 | 7.7 | 1 |  |  | 0% | no |
| 34 | tollo | 8 | 23 | 3.64 / 0.55 | +2.73 | 15.0 | 0.025 |  |  | 0% | no |
| 35 | exitium | 4 | 12 | 1.82 / 0.29 | +2.67 | 7.2 | 1 |  |  | 0% | no |
| 36 | aperio | 3 | 9 | 1.37 / 0.21 | +2.67 | 5.4 | 1 |  |  | 0% | no |
| 37 | consto | 3 | 9 | 1.37 / 0.21 | +2.67 | 5.4 | 1 |  |  | 0% | no |
| 38 | fumus | 3 | 9 | 1.37 / 0.21 | +2.67 | 5.4 | 1 |  |  | 0% | no |
| 39 | stabilis | 3 | 9 | 1.37 / 0.21 | +2.67 | 5.4 | 1 |  |  | 0% | no |
| 40 | expeto | 5 | 15 | 2.28 / 0.36 | +2.67 | 9.0 | 0.592 |  |  | 0% | no |

## Top 20 under-used in Ecerinis (lemmas with frequency ≥ 3 in Ecerinis; ranked by log ratio)

| rank | lemma | Ecerinis | Seneca | per 1,000 Ece / Sen | log ratio | G² | p (Bonferroni) | topic s29 k8 | topic s35 k9 | % of 50 seeds (k8) | in model vocab |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | dies | 3 | 179 | 1.37 / 4.27 | -1.64 | 5.7 | 1 |  |  | 0% | no |
| 2 | regnum | 4 | 211 | 1.82 / 5.03 | -1.47 | 5.7 | 1 |  |  | 0% | no |
| 3 | parens | 3 | 140 | 1.37 / 3.34 | -1.29 | 3.2 | 1 |  |  | 0% | no |
| 4 | uultus | 3 | 136 | 1.37 / 3.24 | -1.25 | 2.9 | 1 |  |  | 0% | no |
| 5 | natus | 4 | 176 | 1.82 / 4.20 | -1.20 | 3.6 | 1 |  |  | 0% | no |
| 6 | animus | 4 | 173 | 1.82 / 4.13 | -1.18 | 3.4 | 1 |  |  | 0% | no |
| 7 | pectus | 3 | 128 | 1.37 / 3.05 | -1.16 | 2.5 | 1 |  |  | 0% | no |
| 8 | mare | 3 | 128 | 1.37 / 3.05 | -1.16 | 2.5 | 1 |  |  | 0% | no |
| 9 | ferrum | 3 | 109 | 1.37 / 2.60 | -0.93 | 1.5 | 1 |  |  | 0% | no |
| 10 | iubeo | 3 | 104 | 1.37 / 2.48 | -0.86 | 1.3 | 1 |  |  | 0% | no |
| 11 | metus | 3 | 98 | 1.37 / 2.34 | -0.77 | 1.0 | 1 |  |  | 0% | no |
| 12 | domus | 5 | 155 | 2.28 / 3.70 | -0.70 | 1.3 | 1 |  |  | 0% | no |
| 13 | terra | 5 | 155 | 2.28 / 3.70 | -0.70 | 1.3 | 1 |  |  | 0% | no |
| 14 | magnus | 8 | 238 | 3.64 / 5.68 | -0.64 | 1.7 | 1 |  |  | 0% | no |
| 15 | iaceo | 4 | 119 | 1.82 / 2.84 | -0.64 | 0.9 | 1 |  |  | 0% | no |
| 16 | manus | 12 | 356 | 5.47 / 8.49 | -0.64 | 2.6 | 1 |  |  | 0% | no |
| 17 | premo | 4 | 106 | 1.82 / 2.53 | -0.47 | 0.5 | 1 |  |  | 0% | no |
| 18 | primus | 3 | 78 | 1.37 / 1.86 | -0.44 | 0.3 | 1 |  |  | 0% | no |
| 19 | thalamus | 3 | 78 | 1.37 / 1.86 | -0.44 | 0.3 | 1 |  |  | 0% | no |
| 20 | scelus | 9 | 233 | 4.10 / 5.56 | -0.44 | 0.9 | 1 |  |  | 0% | no |

## Supplementary: lemmas Ecerinis uses fewer than 3 times although the Seneca rate predicts at least 5

Outside the ≥ 3 rule, so not Bonferroni-corrected (uncorrected p shown). Ranked by log ratio.

| rank | lemma | Ecerinis | Seneca | per 1,000 Ece / Sen | log ratio | G² | p (Bonferroni) | topic s29 k8 | topic s35 k9 | % of 50 seeds (k8) | in model vocab |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | grauis | 0 | 148 | 0.00 / 3.53 | -3.95* | 15.1 | 1.0e-04 (uncorr.) |  |  | 0% | no |
| 2 | malum | 1 | 164 | 0.46 / 3.91 | -3.10 | 10.5 | 0.001 (uncorr.) |  |  | 0% | no |
| 3 | coniux | 1 | 137 | 0.46 / 3.27 | -2.84 | 8.1 | 0.004 (uncorr.) |  |  | 0% | no |
| 4 | fugio | 1 | 110 | 0.46 / 2.62 | -2.53 | 5.8 | 0.016 (uncorr.) |  |  | 0% | no |
| 5 | nox | 1 | 107 | 0.46 / 2.55 | -2.49 | 5.6 | 0.018 (uncorr.) |  |  | 0% | no |
| 6 | fatum | 2 | 153 | 0.91 / 3.65 | -2.00 | 6.2 | 0.012 (uncorr.) |  |  | 0% | no |
| 7 | timeo | 2 | 148 | 0.91 / 3.53 | -1.95 | 5.9 | 0.015 (uncorr.) |  |  | 0% | no |
| 8 | rex | 2 | 138 | 0.91 / 3.29 | -1.85 | 5.1 | 0.024 (uncorr.) |  |  | 0% | no |
| 9 | miser | 2 | 125 | 0.91 / 2.98 | -1.71 | 4.2 | 0.041 (uncorr.) |  |  | 0% | no |
| 10 | rapio | 2 | 108 | 0.91 / 2.58 | -1.50 | 3.0 | 0.082 (uncorr.) |  |  | 0% | no |
| 11 | poena | 2 | 106 | 0.91 / 2.53 | -1.47 | 2.9 | 0.088 (uncorr.) |  |  | 0% | no |
| 12 | dolor | 2 | 106 | 0.91 / 2.53 | -1.47 | 2.9 | 0.088 (uncorr.) |  |  | 0% | no |

Figure: `figures/fig_keyness_log_ratio.png`.

Full table: `keyness_all.csv`.
