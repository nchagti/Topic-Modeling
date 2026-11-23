# Each play's own topic across 50 seeds; Ecerinis's next-best topic

A play's topic in a seed = its dominant topic (argmax of its topic weights). 'Alone' = no other play has that topic as dominant. Stable words = words in that topic's top 20 by relevance (λ = 0.6) in at least 50% / 80% of the 50 seeds, counted over all 50 seeds whether or not the topic is shared (when it is shared, its top words describe the shared topic, not the play alone). Jaccard = overlap of the top-20 relevance lists between the play's topic in a seed and in the representative seed, averaged over the other 49 seeds.

Ecerinis is the focus; the ten Seneca plays are the baseline.

## original, k = 8 (representative seed 25)

| play | alone | words ≥50% | words ≥80% | mean Jaccard to rep. seed (SD) |
|---|---|---|---|---|
| **Ecerinis** | 32% (16/50) | 7 | 2 | 0.36 (0.33) |
| Agamemnon | 20% (10/50) | 5 | 1 | 0.13 (0.10) |
| Hercules Furens | 28% (14/50) | 6 | 0 | 0.10 (0.10) |
| Hercules Oetaeus | 42% (21/50) | 14 | 9 | 0.46 (0.15) |
| Medea | 26% (13/50) | 5 | 0 | 0.27 (0.34) |
| Octavia | 38% (19/50) | 12 | 3 | 0.50 (0.36) |
| Oedipus | 32% (16/50) | 3 | 0 | 0.27 (0.27) |
| Phaedra | 12% (6/50) | 1 | 0 | 0.10 (0.12) |
| Phoenissae | 34% (17/50) | 5 | 0 | 0.33 (0.39) |
| Thyestes | 28% (14/50) | 6 | 2 | 0.15 (0.11) |
| Troades | 16% (8/50) | 6 | 2 | 0.13 (0.08) |

Baseline (ten Seneca plays): alone median 28% (range 12%–42%); words ≥50% median 6 (range 1–14); words ≥80% median 0 (range 0–9); mean Jaccard median 0.21 (range 0.10–0.50).
Ecerinis's rank among the 11 plays (1 = highest; ties share the higher rank): alone 4, words ≥50% 3, words ≥80% 3, mean Jaccard 3.

Stable words per play (share of the 50 seeds in which the word is in the play's topic's top 20):

- **Ecerinis**, ≥80%: lis 96%; actus 90%
  - 50–79%: forum 78%; rabies 62%; plebs 58%; triplex 54%; anxius 52%
- **Agamemnon**, ≥80%: classis 90%
  - 50–79%: comitor 64%; nata 62%; lacero 56%; laurus 52%
- **Hercules Furens**, ≥80%: —
  - 50–79%: aspectus 60%; ferax 60%; harundo 58%; mano 56%; occasus 56%; uolucer 56%
- **Hercules Oetaeus**, ≥80%: axis 100%; colus 100%; uoltus 100%; uindico 96%; maereo 92%; uolucer 92%; triumphus 88%; deficio 86%; palla 86%
  - 50–79%: abrumpo 78%; inuado 64%; uirus 64%; intendo 58%; caelestis 54%
- **Medea**, ≥80%: —
  - 50–79%: paeniteo 66%; peruro 66%; profugio 62%; carina 52%; nubo 50%
- **Octavia**, ≥80%: princeps 100%; subicio 98%; constituo 86%
  - 50–79%: suboles 76%; lacero 74%; saevus 66%; uolucer 66%; incestus 64%; porto 62%; resoluo 60%; immitis 56%; extruo 52%
- **Oedipus**, ≥80%: —
  - 50–79%: curuus 76%; cognatus 70%; laurus 58%
- **Phaedra**, ≥80%: —
  - 50–79%: saltus 70%
- **Phoenissae**, ≥80%: —
  - 50–79%: eruo 70%; abnuo 54%; affectus 52%; dirigo 52%; externus 50%
- **Thyestes**, ≥80%: mensa 100%; cibus 86%
  - 50–79%: uinum 66%; obsto 60%; amputo 58%; uoluptas 50%
- **Troades**, ≥80%: bustum 94%; classis 94%
  - 50–79%: accido 74%; sumo 70%; cultus 54%; amoueo 50%

## v2, k = 8 (representative seed 29)

| play | alone | words ≥50% | words ≥80% | mean Jaccard to rep. seed (SD) |
|---|---|---|---|---|
| **Ecerinis** | 40% (20/50) | 13 | 3 | 0.42 (0.31) |
| Agamemnon | 26% (13/50) | 4 | 1 | 0.16 (0.13) |
| Hercules Furens | 22% (11/50) | 4 | 1 | 0.18 (0.20) |
| Hercules Oetaeus | 24% (12/50) | 10 | 6 | 0.31 (0.14) |
| Medea | 20% (10/50) | 3 | 1 | 0.23 (0.29) |
| Octavia | 46% (23/50) | 15 | 3 | 0.50 (0.35) |
| Oedipus | 30% (15/50) | 6 | 1 | 0.06 (0.13) |
| Phaedra | 26% (13/50) | 2 | 0 | 0.32 (0.40) |
| Phoenissae | 36% (18/50) | 4 | 0 | 0.37 (0.41) |
| Thyestes | 26% (13/50) | 5 | 1 | 0.31 (0.31) |
| Troades | 28% (14/50) | 10 | 4 | 0.24 (0.11) |

Baseline (ten Seneca plays): alone median 26% (range 20%–46%); words ≥50% median 4 (range 2–15); words ≥80% median 1 (range 0–6); mean Jaccard median 0.27 (range 0.06–0.50).
Ecerinis's rank among the 11 plays (1 = highest; ties share the higher rank): alone 2, words ≥50% 2, words ≥80% 3, mean Jaccard 2.

Stable words per play (share of the 50 seeds in which the word is in the play's topic's top 20):

- **Ecerinis**, ≥80%: lis 92%; atrox 90%; actus 86%
  - 50–79%: rabies 70%; adulter 68%; forum 62%; plebs 60%; deuoueo 56%; desino 54%; anxius 52%; pons 52%; triplex 52%; supernus 50%
- **Agamemnon**, ≥80%: classis 92%
  - 50–79%: remeo 74%; danai 60%; laurus 58%
- **Hercules Furens**, ≥80%: inferi 98%
  - 50–79%: aspectus 56%; occasus 52%; harundo 50%
- **Hercules Oetaeus**, ≥80%: axis 96%; foris 92%; irascor 92%; colus 90%; maereo 90%; serpens 88%
  - 50–79%: abrumpo 72%; paelex 70%; palla 66%; uirus 54%
- **Medea**, ≥80%: serpens 80%
  - 50–79%: colchus 62%; paeniteo 52%
- **Octavia**, ≥80%: princeps 100%; constituo 84%; lacero 82%
  - 50–79%: interimo 74%; polluo 72%; iussum 70%; immitis 66%; incestus 66%; porto 66%; claro 64%; consensus 62%; obsequor 56%; extruo 54%; resoluo 54%; nutus 50%
- **Oedipus**, ≥80%: uates 80%
  - 50–79%: curuus 76%; cognatus 72%; cauus 62%; bos 50%; morbus 50%
- **Phaedra**, ≥80%: —
  - 50–79%: sanus 66%; saltus 62%
- **Phoenissae**, ≥80%: —
  - 50–79%: thebanus 72%; eruo 60%; affectus 56%; externus 52%
- **Thyestes**, ≥80%: mensa 94%
  - 50–79%: cibus 74%; uinum 64%; amputo 62%; uoluptas 56%
- **Troades**, ≥80%: captiuus 98%; danai 98%; classis 96%; bustum 94%
  - 50–79%: accido 78%; sumo 72%; hectoreus 66%; pelasgus 54%; eruo 50%; misereor 50%

## v2, k = 9 (representative seed 35)

| play | alone | words ≥50% | words ≥80% | mean Jaccard to rep. seed (SD) |
|---|---|---|---|---|
| **Ecerinis** | 44% (22/50) | 12 | 3 | 0.45 (0.32) |
| Agamemnon | 26% (13/50) | 4 | 1 | 0.28 (0.30) |
| Hercules Furens | 14% (7/50) | 2 | 1 | 0.13 (0.18) |
| Hercules Oetaeus | 22% (11/50) | 9 | 6 | 0.40 (0.27) |
| Medea | 28% (14/50) | 5 | 1 | 0.32 (0.35) |
| Octavia | 46% (23/50) | 15 | 3 | 0.46 (0.33) |
| Oedipus | 26% (13/50) | 6 | 0 | 0.18 (0.18) |
| Phaedra | 24% (12/50) | 3 | 0 | 0.26 (0.33) |
| Phoenissae | 34% (17/50) | 2 | 0 | 0.32 (0.37) |
| Thyestes | 40% (20/50) | 9 | 1 | 0.17 (0.14) |
| Troades | 32% (16/50) | 9 | 4 | 0.24 (0.13) |

Baseline (ten Seneca plays): alone median 27% (range 14%–46%); words ≥50% median 6 (range 2–15); words ≥80% median 1 (range 0–6); mean Jaccard median 0.27 (range 0.13–0.46).
Ecerinis's rank among the 11 plays (1 = highest; ties share the higher rank): alone 2, words ≥50% 2, words ≥80% 3, mean Jaccard 2.

Stable words per play (share of the 50 seeds in which the word is in the play's topic's top 20):

- **Ecerinis**, ≥80%: lis 96%; atrox 94%; actus 82%
  - 50–79%: rabies 74%; forum 72%; adulter 66%; plebs 66%; supernus 58%; triplex 58%; desino 52%; pons 52%; deuoueo 50%
- **Agamemnon**, ≥80%: classis 92%
  - 50–79%: remeo 64%; laurus 58%; danai 56%
- **Hercules Furens**, ≥80%: inferi 96%
  - 50–79%: aspectus 60%
- **Hercules Oetaeus**, ≥80%: axis 98%; foris 90%; irascor 90%; colus 88%; serpens 86%; maereo 84%
  - 50–79%: abrumpo 74%; paelex 68%; palla 66%
- **Medea**, ≥80%: serpens 84%
  - 50–79%: colchus 74%; paeniteo 58%; peruro 58%; nubo 56%
- **Octavia**, ≥80%: princeps 100%; constituo 82%; lacero 82%
  - 50–79%: interimo 74%; iussum 72%; polluo 66%; immitis 64%; incestus 62%; porto 62%; uxor 58%; obsequor 54%; consensus 52%; nutus 52%; claro 50%; extruo 50%
- **Oedipus**, ≥80%: —
  - 50–79%: uates 74%; curuus 70%; cognatus 66%; cauus 52%; morbus 52%; purus 52%
- **Phaedra**, ≥80%: —
  - 50–79%: saltus 64%; sanus 64%; ambiguus 50%
- **Phoenissae**, ≥80%: —
  - 50–79%: thebanus 76%; eruo 56%
- **Thyestes**, ≥80%: mensa 100%
  - 50–79%: cibus 76%; uinum 74%; compono 70%; amputo 68%; obsto 64%; uoluptas 64%; incubo 54%; rictus 50%
- **Troades**, ≥80%: bustum 98%; captiuus 96%; danai 96%; classis 92%
  - 50–79%: accido 76%; sumo 72%; hectoreus 70%; pelasgus 58%; amoueo 50%

## Ecerinis's next-best topic (contrastive measure, 50 seeds)

Next-best topic = the topic other than Ecerinis's dominant topic under which Ecerinis's bag of words has the highest log-likelihood (as in A3). Margin = log-likelihood under the dominant topic minus under the next-best topic (= the sum of the per-word pulls); per token = divided by Ecerinis's tokens in the model vocabulary. Shares by play can sum to more than 100% because a topic can be dominant in several plays.

Retrained models match the saved doc-topic weights (largest absolute difference 1.1e-16).

### original, k = 8

| next-best topic is dominant in | seeds | share |
|---|---|---|
| Octavia | 1 | 2% |
| Phoenissae | 1 | 2% |
| no play | 48 | 96% |

For comparison: of the k − 1 topics other than Ecerinis's, on average 27% are the dominant topic of no play (mean 1.9 empty topics per seed), so a topic picked at random from them would be a no-play topic 27% of the time.
Median margin 351.3 nats (IQR 239.7–563.0); per token 0.93 (IQR 0.64–1.49). Ecerinis's dominant topic is also its maximum-likelihood topic in 50/50 seeds.

### v2, k = 8

| next-best topic is dominant in | seeds | share |
|---|---|---|
| Octavia | 2 | 4% |
| Thyestes | 1 | 2% |
| no play | 48 | 96% |

For comparison: of the k − 1 topics other than Ecerinis's, on average 27% are the dominant topic of no play (mean 1.9 empty topics per seed), so a topic picked at random from them would be a no-play topic 27% of the time.
Median margin 381.8 nats (IQR 280.4–600.5); per token 0.92 (IQR 0.67–1.44). Ecerinis's dominant topic is also its maximum-likelihood topic in 50/50 seeds.

### v2, k = 9

| next-best topic is dominant in | seeds | share |
|---|---|---|
| Octavia | 1 | 2% |
| no play | 49 | 98% |

For comparison: of the k − 1 topics other than Ecerinis's, on average 35% are the dominant topic of no play (mean 2.8 empty topics per seed), so a topic picked at random from them would be a no-play topic 35% of the time.
Median margin 441.2 nats (IQR 282.7–611.8); per token 1.06 (IQR 0.68–1.47). Ecerinis's dominant topic is also its maximum-likelihood topic in 50/50 seeds.

