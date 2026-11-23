# A5 part 2: theme word-family rates

**These are lexicon counts from word lists chosen by the author (`data/theme_lexicon.json`), not model output.** Rate = family tokens per 1,000 tokens, counted before the dictionary filter. Interval = bootstrap 95% percentile interval from resampling consecutive 200-token chunks within each play (50-token chunks within each act) (2000 replicates). Seneca mean = mean of the ten Seneca plays' rates (this definition reproduces the brief's figures). Raw counts in Ecerinis are small, so the intervals are wide; treat as descriptive.

Families: **Invasion**: hostis, urbs, occupo, inuado; **Deceit**: falsus, dolus, fraus; **Punishment**: supplicium, ultio, ignis; **Fate**: sors, sidus, fatum.

## v2 tokens (A1-normalized)

| theme | Ecerinis rate [95% CI] (count / tokens) | Seneca mean | Seneca plays: range | Ecerinis rank of 11 | Seneca plays whose interval does not overlap Ecerinis's |
|---|---|---|---|---|---|
| Invasion | 9.6 [4.6–15.0] (21 / 2195) | 3.7 | 1.7–6.2 | 1 | 2: Phaedra, Oedipus |
| Deceit | 5.5 [3.2–8.2] (12 / 2195) | 2.4 | 0.6–3.6 | 1 | 2: Hercules Furens, Oedipus |
| Punishment | 5.5 [3.2–8.2] (12 / 2195) | 3.3 | 1.8–5.0 | 1 | 0: — |
| Fate | 3.6 [1.8–5.5] (8 / 2195) | 5.4 | 1.9–8.9 | 7 | 2: Oedipus, Hercules Oetaeus |

Per play (rate [95% CI]):

| play | Invasion | Deceit | Punishment | Fate |
|---|---|---|---|---|
| Ecerinis | 9.6 [4.6–15.0] | 5.5 [3.2–8.2] | 5.5 [3.2–8.2] | 3.6 [1.8–5.5] |
| Agamemnon | 3.3 [1.1–5.9] | 3.0 [1.4–5.0] | 3.0 [1.1–5.3] | 4.4 [2.7–6.4] |
| Hercules Furens | 3.2 [1.6–5.0] | 0.6 [0.0–1.4] | 2.0 [0.8–3.4] | 3.4 [2.2–4.8] |
| Hercules Oetaeus | 5.3 [3.7–7.3] | 2.7 [1.3–4.3] | 3.6 [1.9–5.7] | 8.4 [6.0–11.1] |
| Medea | 3.3 [1.4–5.9] | 3.6 [1.7–5.8] | 5.0 [2.5–7.8] | 1.9 [0.6–3.6] |
| Octavia | 6.2 [4.4–7.9] | 1.5 [0.0–3.5] | 1.8 [0.3–3.5] | 7.3 [4.4–10.6] |
| Oedipus | 1.7 [0.5–3.5] | 1.5 [0.5–2.8] | 3.7 [2.2–5.5] | 8.9 [6.0–12.1] |
| Phaedra | 2.0 [1.0–3.3] | 2.7 [1.4–4.1] | 4.1 [1.9–6.4] | 4.7 [2.5–6.9] |
| Phoenissae | 4.0 [1.8–6.2] | 2.0 [0.4–3.7] | 3.6 [1.2–6.7] | 3.2 [1.2–5.8] |
| Thyestes | 3.0 [1.3–5.1] | 3.0 [0.8–5.6] | 4.3 [2.0–7.2] | 3.3 [1.5–5.2] |
| Troades | 4.8 [2.7–7.4] | 3.4 [1.7–5.2] | 2.2 [1.0–3.6] | 8.2 [4.9–12.1] |

Ecerinis acts (rate [95% CI], count; act length in tokens). Seneca acts: median rate and range over all Seneca acts:

| act | tokens | Invasion | Deceit | Punishment | Fate |
|---|---|---|---|---|---|
| Ece 1 | 551 (11 chunks) | 7.3 [0.0–14.5], n=4 | 9.1 [0.0–18.2], n=5 | 3.6 [0.0–9.1], n=2 | 1.8 [0.0–5.5], n=1 |
| Ece 2 | 409 (8 chunks) | 4.9 [0.0–10.0], n=2 | 7.3 [0.0–19.6], n=3 | 7.3 [0.0–19.1], n=3 | 0.0 [0.0–0.0], n=0 |
| Ece 3 | 614 (12 chunks) | 11.4 [3.3–20.0], n=7 | 3.3 [0.0–8.1], n=2 | 4.9 [0.0–10.0], n=3 | 6.5 [1.6–11.7], n=4 |
| Ece 4 | 271 (5 chunks) | 22.1 [6.4–44.0], n=6 | 3.7 [0.0–12.0], n=1 | 0.0 [0.0–0.0], n=0 | 3.7 [0.0–12.0], n=1 |
| Ece 5 | 350 (7 chunks) | 5.7 [0.0–17.1], n=2 | 2.9 [0.0–8.6], n=1 | 11.4 [2.9–22.9], n=4 | 5.7 [0.0–11.4], n=2 |
| Seneca acts | — | median 3.8 (range 0.0–13.6) | median 1.7 (range 0.0–10.6) | median 2.5 (range 0.0–11.5) | median 4.0 (range 0.0–21.1) |

Figure: `figures/fig_a5_theme_rates_v2.png`.

## original processed tokens (conference pipeline)

| theme | Ecerinis rate [95% CI] (count / tokens) | Seneca mean | Seneca plays: range | Ecerinis rank of 11 | Seneca plays whose interval does not overlap Ecerinis's |
|---|---|---|---|---|---|
| Invasion | 8.6 [4.3–13.3] (20 / 2330) | 3.4 | 1.7–6.0 | 1 | 2: Phaedra, Oedipus |
| Deceit | 4.3 [1.8–6.9] (10 / 2330) | 2.0 | 0.2–3.2 | 1 | 1: Hercules Furens |
| Punishment | 5.2 [2.6–8.0] (12 / 2330) | 3.2 | 1.7–5.3 | 2 | 0: — |
| Fate | 3.4 [1.7–5.4] (8 / 2330) | 4.9 | 1.8–7.8 | 8 | 0: — |

Per play (rate [95% CI]):

| play | Invasion | Deceit | Punishment | Fate |
|---|---|---|---|---|
| Ecerinis | 8.6 [4.3–13.3] | 4.3 [1.8–6.9] | 5.2 [2.6–8.0] | 3.4 [1.7–5.4] |
| Agamemnon | 3.1 [1.0–5.2] | 2.8 [1.2–4.8] | 2.8 [0.8–5.5] | 3.6 [2.0–5.5] |
| Hercules Furens | 2.8 [1.2–4.6] | 0.2 [0.0–0.6] | 1.9 [0.7–3.2] | 3.2 [2.0–4.7] |
| Hercules Oetaeus | 4.8 [3.4–6.3] | 2.2 [1.1–3.4] | 3.3 [1.6–5.2] | 7.8 [5.4–10.5] |
| Medea | 2.9 [1.1–5.5] | 3.2 [1.6–5.3] | 5.3 [3.4–7.4] | 1.8 [0.8–3.2] |
| Octavia | 6.0 [4.3–7.8] | 1.4 [0.0–3.4] | 1.7 [0.6–2.8] | 6.8 [3.7–10.7] |
| Oedipus | 1.7 [0.5–2.9] | 1.7 [0.5–3.1] | 3.6 [1.7–5.5] | 7.6 [5.0–10.5] |
| Phaedra | 2.0 [0.8–3.4] | 1.6 [0.6–2.8] | 3.9 [1.8–6.4] | 4.5 [2.8–6.6] |
| Phoenissae | 3.9 [1.9–6.2] | 2.0 [0.8–3.3] | 3.5 [1.2–6.5] | 3.5 [1.6–5.9] |
| Thyestes | 2.9 [1.4–4.8] | 2.9 [0.8–5.5] | 4.2 [2.2–6.4] | 2.9 [1.4–4.7] |
| Troades | 4.2 [2.0–6.7] | 2.4 [0.9–4.2] | 2.0 [0.7–3.4] | 7.3 [3.9–10.9] |

Ecerinis acts (rate [95% CI], count; act length in tokens). Seneca acts: median rate and range over all Seneca acts:

| act | tokens | Invasion | Deceit | Punishment | Fate |
|---|---|---|---|---|---|
| Ece 1 | 546 (11 chunks) | 7.3 [0.0–16.4], n=4 | 5.5 [0.0–11.0], n=3 | 3.7 [0.0–9.1], n=2 | 1.8 [0.0–5.5], n=1 |
| Ece 2 | 436 (9 chunks) | 4.6 [0.0–11.1], n=2 | 6.9 [2.2–13.3], n=3 | 6.9 [0.0–17.2], n=3 | 0.0 [0.0–0.0], n=0 |
| Ece 3 | 662 (13 chunks) | 10.6 [3.0–19.6], n=7 | 3.0 [0.0–7.7], n=2 | 4.5 [0.0–9.2], n=3 | 6.0 [1.5–10.8], n=4 |
| Ece 4 | 295 (6 chunks) | 16.9 [6.8–27.1], n=5 | 3.4 [0.0–10.2], n=1 | 0.0 [0.0–0.0], n=0 | 3.4 [0.0–10.2], n=1 |
| Ece 5 | 365 (7 chunks) | 5.5 [0.0–17.1], n=2 | 2.7 [0.0–8.6], n=1 | 11.0 [2.5–22.9], n=4 | 5.5 [0.0–11.4], n=2 |
| Seneca acts | — | median 3.6 (range 0.0–12.7) | median 1.3 (range 0.0–10.2) | median 2.5 (range 0.0–10.7) | median 3.5 (range 0.0–17.3) |

Figure: `figures/fig_a5_theme_rates_original.png`.

## Per-word rates (Ecerinis vs Seneca mean)

| pipeline | theme | word | Ecerinis rate (count) | Seneca mean |
|---|---|---|---|---|
| v2 | Invasion | hostis | 2.73 (6) | 1.41 |
| v2 | Invasion | urbs | 3.19 (7) | 1.42 |
| v2 | Invasion | occupo | 2.28 (5) | 0.67 |
| v2 | Invasion | inuado | 1.37 (3) | 0.20 |
| v2 | Deceit | falsus | 2.28 (5) | 0.58 |
| v2 | Deceit | dolus | 1.82 (4) | 0.98 |
| v2 | Deceit | fraus | 1.37 (3) | 0.84 |
| v2 | Punishment | supplicium | 0.91 (2) | 0.46 |
| v2 | Punishment | ultio | 0.91 (2) | 0.06 |
| v2 | Punishment | ignis | 3.64 (8) | 2.81 |
| v2 | Fate | sors | 1.37 (3) | 0.89 |
| v2 | Fate | sidus | 1.37 (3) | 1.00 |
| v2 | Fate | fatum | 0.91 (2) | 3.50 |
| original | Invasion | hostis | 2.58 (6) | 1.34 |
| original | Invasion | urbs | 3.00 (7) | 1.31 |
| original | Invasion | occupo | 1.72 (4) | 0.64 |
| original | Invasion | inuado | 1.29 (3) | 0.14 |
| original | Deceit | falsus | 1.72 (4) | 0.38 |
| original | Deceit | dolus | 1.72 (4) | 0.93 |
| original | Deceit | fraus | 0.86 (2) | 0.72 |
| original | Punishment | supplicium | 0.86 (2) | 0.44 |
| original | Punishment | ultio | 0.86 (2) | 0.05 |
| original | Punishment | ignis | 3.43 (8) | 2.73 |
| original | Fate | sors | 1.29 (3) | 0.84 |
| original | Fate | sidus | 1.29 (3) | 0.93 |
| original | Fate | fatum | 0.86 (2) | 3.16 |

Note: the original act files lack Phaedra's prelude and take Ecerinis from a different TEI version (see A1); the v2 acts are cut from the v2 play texts.
