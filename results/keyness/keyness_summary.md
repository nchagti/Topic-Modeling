# Keyness: Ecerinis vs the ten Seneca plays combined

v2 tokens (A1-normalized content lemmas), before the dictionary filter. Ecerinis 2,198 tokens; Seneca 41,931 tokens. Tested: the 226 lemmas with frequency ≥ 3 in Ecerinis. G² = log-likelihood (Rayson & Garside); p from χ² (1 df), Bonferroni-corrected for the number of lemmas tested. Log ratio = log2 of the ratio of relative frequencies (Hardie); +1 = twice as frequent in Ecerinis. * = a zero count replaced by 0.5.

**The counts are small (most tested lemmas occur 3–6 times in Ecerinis), so the effect sizes (log ratio) matter more than the p-values.** Bonferroni is conservative: few lemmas pass it.

- Lemmas passing Bonferroni p < 0.05: 17 (17 over-used, 0 under-used): annuo, tyrannis, crux, lis, marchia, patro, progredior, ausus, nocuus, inspecto, actus, atrox, forum, ordo, homo, finis, tollo.
- Over-used lemmas (log ratio > 0): 190; under-used: 36.
- Of the top 40 over-used, 16 are in Ecerinis's topic's top 20 (v2 seed 29, k = 8), 16 at seed 35, k = 9; 22 are removed by the dictionary filter.
- Topic columns: in the top 20 by relevance (λ = 0.6) of Ecerinis's dominant topic in the v2 representative models (seed 29, k = 8; seed 35, k = 9), and the share of the 50 seeds (v2, k = 8) in which the lemma is in that topic's top 20. 'In model vocab' = kept by no_below=2 / no_above=0.5.

## Top 40 over-used in Ecerinis (ranked by log ratio)

| rank | lemma | Ecerinis | Seneca | per 1,000 Ece / Sen | log ratio | G² | p (Bonferroni) | topic s29 k8 | topic s35 k9 | % of 50 seeds (k8) | in model vocab |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | annuo | 5 | 0 | 2.27 / 0.00 | +7.58* | 30.0 | 9.8e-06 |  |  | 0% | no |
| 2 | tyrannis | 5 | 0 | 2.27 / 0.00 | +7.58* | 30.0 | 9.8e-06 |  |  | 0% | no |
| 3 | crux | 4 | 0 | 1.82 / 0.00 | +7.25* | 24.0 | 2.2e-04 |  |  | 0% | no |
| 4 | lis | 6 | 1 | 2.73 / 0.02 | +6.84 | 30.4 | 8.1e-06 | ✓ | ✓ | 92% | yes |
| 5 | marchia | 3 | 0 | 1.36 / 0.00 | +6.84* | 18.0 | 0.005 |  |  | 0% | no |
| 6 | patro | 3 | 0 | 1.36 / 0.00 | +6.84* | 18.0 | 0.005 |  |  | 0% | no |
| 7 | progredior | 3 | 0 | 1.36 / 0.00 | +6.84* | 18.0 | 0.005 |  |  | 0% | no |
| 8 | ausus | 3 | 0 | 1.36 / 0.00 | +6.84* | 18.0 | 0.005 |  |  | 0% | no |
| 9 | nocuus | 3 | 0 | 1.36 / 0.00 | +6.84* | 18.0 | 0.005 |  |  | 0% | no |
| 10 | inspecto | 3 | 0 | 1.36 / 0.00 | +6.84* | 18.0 | 0.005 |  |  | 0% | no |
| 11 | triplex | 3 | 1 | 1.36 / 0.02 | +5.84 | 13.6 | 0.051 | ✓ | ✓ | 52% | yes |
| 12 | pons | 3 | 1 | 1.36 / 0.02 | +5.84 | 13.6 | 0.051 | ✓ | ✓ | 52% | yes |
| 13 | actus | 5 | 3 | 2.27 / 0.07 | +4.99 | 19.7 | 0.002 | ✓ | ✓ | 86% | yes |
| 14 | atrox | 6 | 4 | 2.73 / 0.10 | +4.84 | 22.9 | 3.8e-04 | ✓ | ✓ | 90% | yes |
| 15 | deuoueo | 3 | 2 | 1.36 / 0.05 | +4.84 | 11.5 | 0.160 | ✓ | ✓ | 56% | yes |
| 16 | desino | 3 | 2 | 1.36 / 0.05 | +4.84 | 11.5 | 0.160 | ✓ | ✓ | 54% | yes |
| 17 | forum | 4 | 3 | 1.82 / 0.07 | +4.67 | 14.7 | 0.028 | ✓ | ✓ | 62% | yes |
| 18 | plebs | 4 | 4 | 1.82 / 0.10 | +4.25 | 13.3 | 0.060 | ✓ | ✓ | 60% | yes |
| 19 | rabies | 4 | 4 | 1.82 / 0.10 | +4.25 | 13.3 | 0.060 | ✓ | ✓ | 70% | yes |
| 20 | patulus | 3 | 3 | 1.36 / 0.07 | +4.25 | 10.0 | 0.356 | ✓ | ✓ | 48% | yes |
| 21 | potior | 3 | 3 | 1.36 / 0.07 | +4.25 | 10.0 | 0.356 | ✓ | ✓ | 44% | yes |
| 22 | supernus | 3 | 3 | 1.36 / 0.07 | +4.25 | 10.0 | 0.356 | ✓ | ✓ | 50% | yes |
| 23 | adulter | 4 | 5 | 1.82 / 0.12 | +3.93 | 12.1 | 0.111 | ✓ | ✓ | 68% | yes |
| 24 | ordo | 7 | 9 | 3.18 / 0.21 | +3.89 | 21.0 | 0.001 |  |  | 0% | no |
| 25 | anxius | 3 | 4 | 1.36 / 0.10 | +3.84 | 8.8 | 0.664 | ✓ | ✓ | 52% | yes |
| 26 | series | 3 | 4 | 1.36 / 0.10 | +3.84 | 8.8 | 0.664 | ✓ | ✓ | 46% | yes |
| 27 | homo | 8 | 15 | 3.64 / 0.36 | +3.35 | 19.8 | 0.002 |  |  | 0% | no |
| 28 | iudex | 3 | 6 | 1.36 / 0.14 | +3.25 | 7.2 | 1 |  |  | 12% | yes |
| 29 | largus | 3 | 6 | 1.36 / 0.14 | +3.25 | 7.2 | 1 |  |  | 20% | yes |
| 30 | conuerto | 3 | 7 | 1.36 / 0.17 | +3.03 | 6.5 | 1 |  |  | 0% | no |
| 31 | finis | 9 | 23 | 4.09 / 0.55 | +2.90 | 18.3 | 0.004 |  |  | 0% | no |
| 32 | iustus | 5 | 13 | 2.27 / 0.31 | +2.88 | 10.1 | 0.344 |  |  | 0% | no |
| 33 | duro | 3 | 8 | 1.36 / 0.19 | +2.84 | 5.9 | 1 |  |  | 0% | no |
| 34 | subigo | 3 | 8 | 1.36 / 0.19 | +2.84 | 5.9 | 1 |  |  | 0% | no |
| 35 | subdo | 4 | 11 | 1.82 / 0.26 | +2.79 | 7.7 | 1 |  |  | 0% | no |
| 36 | tollo | 8 | 23 | 3.64 / 0.55 | +2.73 | 14.9 | 0.025 |  |  | 0% | no |
| 37 | expeto | 5 | 15 | 2.27 / 0.36 | +2.67 | 9.0 | 0.599 |  |  | 0% | no |
| 38 | exitium | 4 | 12 | 1.82 / 0.29 | +2.67 | 7.2 | 1 |  |  | 0% | no |
| 39 | aperio | 3 | 9 | 1.36 / 0.21 | +2.67 | 5.4 | 1 |  |  | 0% | no |
| 40 | consto | 3 | 9 | 1.36 / 0.21 | +2.67 | 5.4 | 1 |  |  | 0% | no |

## Top 20 under-used in Ecerinis (lemmas with frequency ≥ 3 in Ecerinis; ranked by log ratio)

| rank | lemma | Ecerinis | Seneca | per 1,000 Ece / Sen | log ratio | G² | p (Bonferroni) | topic s29 k8 | topic s35 k9 | % of 50 seeds (k8) | in model vocab |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | dies | 3 | 179 | 1.36 / 4.27 | -1.65 | 5.7 | 1 |  |  | 0% | no |
| 2 | regnum | 4 | 211 | 1.82 / 5.03 | -1.47 | 5.8 | 1 |  |  | 0% | no |
| 3 | parens | 3 | 140 | 1.36 / 3.34 | -1.29 | 3.2 | 1 |  |  | 0% | no |
| 4 | uultus | 3 | 136 | 1.36 / 3.24 | -1.25 | 2.9 | 1 |  |  | 0% | no |
| 5 | natus | 4 | 176 | 1.82 / 4.20 | -1.21 | 3.6 | 1 |  |  | 0% | no |
| 6 | animus | 4 | 173 | 1.82 / 4.13 | -1.18 | 3.4 | 1 |  |  | 0% | no |
| 7 | pectus | 3 | 128 | 1.36 / 3.05 | -1.16 | 2.5 | 1 |  |  | 0% | no |
| 8 | mare | 3 | 128 | 1.36 / 3.05 | -1.16 | 2.5 | 1 |  |  | 0% | no |
| 9 | ferrum | 3 | 109 | 1.36 / 2.60 | -0.93 | 1.5 | 1 |  |  | 0% | no |
| 10 | iubeo | 3 | 104 | 1.36 / 2.48 | -0.86 | 1.3 | 1 |  |  | 0% | no |
| 11 | metus | 3 | 98 | 1.36 / 2.34 | -0.78 | 1.0 | 1 |  |  | 0% | no |
| 12 | domus | 5 | 155 | 2.27 / 3.70 | -0.70 | 1.3 | 1 |  |  | 0% | no |
| 13 | terra | 5 | 155 | 2.27 / 3.70 | -0.70 | 1.3 | 1 |  |  | 0% | no |
| 14 | magnus | 8 | 238 | 3.64 / 5.68 | -0.64 | 1.8 | 1 |  |  | 0% | no |
| 15 | iaceo | 4 | 119 | 1.82 / 2.84 | -0.64 | 0.9 | 1 |  |  | 0% | no |
| 16 | manus | 12 | 356 | 5.46 / 8.49 | -0.64 | 2.6 | 1 |  |  | 0% | no |
| 17 | premo | 4 | 106 | 1.82 / 2.53 | -0.47 | 0.5 | 1 |  |  | 0% | no |
| 18 | primus | 3 | 78 | 1.36 / 1.86 | -0.45 | 0.3 | 1 |  |  | 0% | no |
| 19 | thalamus | 3 | 78 | 1.36 / 1.86 | -0.45 | 0.3 | 1 |  |  | 0% | no |
| 20 | scelus | 9 | 233 | 4.09 / 5.56 | -0.44 | 0.9 | 1 |  |  | 0% | no |

## Supplementary: lemmas Ecerinis uses fewer than 3 times although the Seneca rate predicts at least 5

Outside the ≥ 3 rule, so not Bonferroni-corrected (uncorrected p shown). Ranked by log ratio.

| rank | lemma | Ecerinis | Seneca | per 1,000 Ece / Sen | log ratio | G² | p (Bonferroni) | topic s29 k8 | topic s35 k9 | % of 50 seeds (k8) | in model vocab |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | grauis | 0 | 148 | 0.00 / 3.53 | -3.96* | 15.1 | 1.0e-04 (uncorr.) |  |  | 0% | no |
| 2 | malum | 1 | 164 | 0.45 / 3.91 | -3.10 | 10.6 | 0.001 (uncorr.) |  |  | 0% | no |
| 3 | coniux | 1 | 137 | 0.45 / 3.27 | -2.84 | 8.2 | 0.004 (uncorr.) |  |  | 0% | no |
| 4 | fugio | 1 | 110 | 0.45 / 2.62 | -2.53 | 5.8 | 0.016 (uncorr.) |  |  | 0% | no |
| 5 | nox | 1 | 107 | 0.45 / 2.55 | -2.49 | 5.6 | 0.018 (uncorr.) |  |  | 0% | no |
| 6 | fatum | 2 | 153 | 0.91 / 3.65 | -2.00 | 6.3 | 0.012 (uncorr.) |  |  | 0% | no |
| 7 | timeo | 2 | 148 | 0.91 / 3.53 | -1.96 | 5.9 | 0.015 (uncorr.) |  |  | 0% | no |
| 8 | rex | 2 | 138 | 0.91 / 3.29 | -1.85 | 5.1 | 0.023 (uncorr.) |  |  | 0% | no |
| 9 | miser | 2 | 125 | 0.91 / 2.98 | -1.71 | 4.2 | 0.040 (uncorr.) |  |  | 0% | no |
| 10 | rapio | 2 | 108 | 0.91 / 2.58 | -1.50 | 3.0 | 0.081 (uncorr.) |  |  | 0% | no |
| 11 | poena | 2 | 106 | 0.91 / 2.53 | -1.47 | 2.9 | 0.088 (uncorr.) |  |  | 0% | no |
| 12 | dolor | 2 | 106 | 0.91 / 2.53 | -1.47 | 2.9 | 0.088 (uncorr.) |  |  | 0% | no |

Figure: `figures/fig_keyness_log_ratio.png`.

Full table: `keyness_all.csv`.
