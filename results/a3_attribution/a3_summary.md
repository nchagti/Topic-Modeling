# A3 word-level attribution for Ecerinis

For each model: the Ecerinis words that carry it into its dominant topic (expected Ecerinis tokens assigned to the topic, from gensim's per-word phi values) next to the topic's top 20 words by relevance (λ = 0.6).

**Caveat.** In every model Ecerinis sits almost entirely in one topic (weight 0.998), so each word's phi equals its count: the phi ranking is Ecerinis's word frequency list, not a measure of which words pull it into the topic. A supplementary contrastive measure is therefore added: each word's pull toward the dominant topic relative to the topic that would explain Ecerinis second best.

## original, seed 42, k = 8 (conference model)

- Ecerinis's dominant topic: Topic 7, weight 0.998; shared as dominant topic with: Phaedra, Hercules Furens, Medea, Hercules Oetaeus.
- Ecerinis has 283 word types (377 tokens) in the model vocabulary; 283 carry weight into Topic 7. The top 20 account for 18% of Ecerinis's mass in the topic.
- Of the topic's top 20 words by relevance, 8 occur in Ecerinis.

**Words that place Ecerinis in the topic (top 20):**

| lemma     |   count_in_ecerinis |   expected_tokens_in_topic |   share_of_ecerinis_topic_mass |   plays_containing | in_topic_top20_relevance   |   pull_vs_next_best_topic |
|:----------|--------------------:|---------------------------:|-------------------------------:|-------------------:|:---------------------------|--------------------------:|
| lis       |                   6 |                          6 |                         0.0159 |                  2 | False                      |                     7.601 |
| forum     |                   5 |                          5 |                         0.0133 |                  3 | False                      |                     7.082 |
| actus     |                   5 |                          5 |                         0.0133 |                  3 | False                      |                     6.331 |
| rabies    |                   4 |                          4 |                         0.0106 |                  4 | False                      |                     5.065 |
| plebs     |                   4 |                          4 |                         0.0106 |                  3 | False                      |                     3.478 |
| inuado    |                   3 |                          3 |                         0.008  |                  5 | True                       |                     5.53  |
| pons      |                   3 |                          3 |                         0.008  |                  5 | True                       |                     4.849 |
| potior    |                   3 |                          3 |                         0.008  |                  4 | False                      |                     3.652 |
| largus    |                   3 |                          3 |                         0.008  |                  4 | False                      |                     3.563 |
| fido      |                   3 |                          3 |                         0.008  |                  5 | False                      |                     3.265 |
| patulus   |                   3 |                          3 |                         0.008  |                  4 | False                      |                     3.168 |
| iudex     |                   3 |                          3 |                         0.008  |                  5 | False                      |                     2.972 |
| supernus  |                   3 |                          3 |                         0.008  |                  3 | False                      |                     2.793 |
| spons     |                   3 |                          3 |                         0.008  |                  4 | False                      |                     2.616 |
| series    |                   3 |                          3 |                         0.008  |                  5 | False                      |                     2.615 |
| anxius    |                   3 |                          3 |                         0.008  |                  4 | False                      |                     2.21  |
| triplex   |                   3 |                          3 |                         0.008  |                  2 | False                      |                     2.032 |
| desino    |                   3 |                          3 |                         0.008  |                  3 | False                      |                     1.784 |
| perpetuus |                   2 |                          2 |                         0.0053 |                  5 | True                       |                     3.211 |
| rigidus   |                   2 |                          2 |                         0.0053 |                  4 | True                       |                     3.097 |

**Words that define the topic (top 20 by relevance, λ = 0.6):**

|   rank | lemma     |   relevance |   p(w|topic) |   count_in_ecerinis |
|-------:|:----------|------------:|-------------:|--------------------:|
|      1 | uoltus    |      -2.61  |      0.0074  |                   0 |
|      2 | uindico   |      -2.777 |      0.00602 |                   0 |
|      3 | uolucer   |      -2.926 |      0.00549 |                   0 |
|      4 | axis      |      -2.966 |      0.0044  |                   0 |
|      5 | inuado    |      -2.996 |      0.00402 |                   3 |
|      6 | colus     |      -3.113 |      0.00332 |                   0 |
|      7 | intendo   |      -3.118 |      0.00331 |                   1 |
|      8 | glacialis |      -3.132 |      0.00298 |                   0 |
|      9 | ursa      |      -3.132 |      0.00298 |                   0 |
|     10 | rigidus   |      -3.132 |      0.00298 |                   2 |
|     11 | harundo   |      -3.133 |      0.00298 |                   0 |
|     12 | falsum    |      -3.16  |      0.0029  |                   2 |
|     13 | perpetuus |      -3.163 |      0.00316 |                   2 |
|     14 | flagrans  |      -3.183 |      0.00297 |                   2 |
|     15 | tingo     |      -3.189 |      0.00295 |                   0 |
|     16 | pons      |      -3.191 |      0.0032  |                   3 |
|     17 | sanus     |      -3.199 |      0.00293 |                   0 |
|     18 | occasus   |      -3.205 |      0.00291 |                   0 |
|     19 | uirus     |      -3.209 |      0.00262 |                   0 |
|     20 | innocuus  |      -3.211 |      0.00261 |                   1 |

**Supplementary (contrastive): words that most favour Topic 7 over the next-best topic for Ecerinis, Topic 3** (dominant in: no play). Pull = count × (log p(w|topic) − log p(w|next-best topic)).

| lemma     |   count_in_ecerinis |   pull | in_topic_top20_relevance   |
|:----------|--------------------:|-------:|:---------------------------|
| lis       |                   6 |  7.601 | False                      |
| forum     |                   5 |  7.082 | False                      |
| actus     |                   5 |  6.331 | False                      |
| inuado    |                   3 |  5.53  | True                       |
| rabies    |                   4 |  5.065 | False                      |
| pons      |                   3 |  4.849 | True                       |
| potior    |                   3 |  3.652 | False                      |
| largus    |                   3 |  3.563 | False                      |
| plebs     |                   4 |  3.478 | False                      |
| fido      |                   3 |  3.265 | False                      |
| perpetuus |                   2 |  3.211 | True                       |
| patulus   |                   3 |  3.168 | False                      |
| rigidus   |                   2 |  3.097 | True                       |
| flagrans  |                   2 |  3.087 | True                       |
| falsum    |                   2 |  3.042 | True                       |
| iudex     |                   3 |  2.972 | False                      |
| supernus  |                   3 |  2.793 | False                      |
| spons     |                   3 |  2.616 | False                      |
| series    |                   3 |  2.615 | False                      |
| urgeo     |                   2 |  2.533 | False                      |

## original, seed 25, k = 8 (representative seed, rule-selected k)

- Ecerinis's dominant topic: Topic 6, weight 0.998; shared as dominant topic with: no other play.
- Ecerinis has 283 word types (377 tokens) in the model vocabulary; 283 carry weight into Topic 6. The top 20 account for 18% of Ecerinis's mass in the topic.
- Of the topic's top 20 words by relevance, 20 occur in Ecerinis.

**Words that place Ecerinis in the topic (top 20):**

| lemma    |   count_in_ecerinis |   expected_tokens_in_topic |   share_of_ecerinis_topic_mass |   plays_containing | in_topic_top20_relevance   |   pull_vs_next_best_topic |
|:---------|--------------------:|---------------------------:|-------------------------------:|-------------------:|:---------------------------|--------------------------:|
| lis      |                   6 |                          6 |                         0.0159 |                  2 | True                       |                    23.784 |
| actus    |                   5 |                          5 |                         0.0133 |                  3 | True                       |                    18.931 |
| forum    |                   5 |                          5 |                         0.0133 |                  3 | True                       |                     7.963 |
| rabies   |                   4 |                          4 |                         0.0106 |                  4 | True                       |                     5.503 |
| plebs    |                   4 |                          4 |                         0.0106 |                  3 | True                       |                     1.416 |
| triplex  |                   3 |                          3 |                         0.008  |                  2 | True                       |                     9.88  |
| supernus |                   3 |                          3 |                         0.008  |                  3 | True                       |                     9.877 |
| anxius   |                   3 |                          3 |                         0.008  |                  4 | True                       |                     9.876 |
| patulus  |                   3 |                          3 |                         0.008  |                  4 | True                       |                     9.878 |
| desino   |                   3 |                          3 |                         0.008  |                  3 | True                       |                     9.879 |
| series   |                   3 |                          3 |                         0.008  |                  5 | True                       |                     3.294 |
| spons    |                   3 |                          3 |                         0.008  |                  4 | True                       |                     9.878 |
| potior   |                   3 |                          3 |                         0.008  |                  4 | True                       |                     9.88  |
| fido     |                   3 |                          3 |                         0.008  |                  5 | False                      |                     9.877 |
| largus   |                   3 |                          3 |                         0.008  |                  4 | False                      |                     9.874 |
| iudex    |                   3 |                          3 |                         0.008  |                  5 | False                      |                     9.877 |
| pons     |                   3 |                          3 |                         0.008  |                  5 | False                      |                     9.87  |
| inuado   |                   3 |                          3 |                         0.008  |                  5 | False                      |                     9.871 |
| sinister |                   2 |                          2 |                         0.0053 |                  2 | False                      |                     5.817 |
| ciuitas  |                   2 |                          2 |                         0.0053 |                  2 | True                       |                     5.819 |

**Words that define the topic (top 20 by relevance, λ = 0.6):**

|   rank | lemma      |   relevance |   p(w|topic) |   count_in_ecerinis |
|-------:|:-----------|------------:|-------------:|--------------------:|
|      1 | lis        |      -1.806 |      0.01065 |                   6 |
|      2 | actus      |      -1.984 |      0.00891 |                   5 |
|      3 | forum      |      -2.038 |      0.00891 |                   5 |
|      4 | rabies     |      -2.255 |      0.00717 |                   4 |
|      5 | plebs      |      -2.255 |      0.00717 |                   4 |
|      6 | triplex    |      -2.255 |      0.00543 |                   3 |
|      7 | desino     |      -2.344 |      0.00543 |                   3 |
|      8 | patulus    |      -2.417 |      0.00543 |                   3 |
|      9 | supernus   |      -2.417 |      0.00543 |                   3 |
|     10 | potior     |      -2.479 |      0.00543 |                   3 |
|     11 | anxius     |      -2.479 |      0.00543 |                   3 |
|     12 | spons      |      -2.479 |      0.00543 |                   3 |
|     13 | series     |      -2.479 |      0.00543 |                   3 |
|     14 | ciuitas    |      -2.525 |      0.0037  |                   2 |
|     15 | excludo    |      -2.525 |      0.0037  |                   2 |
|     16 | relatus    |      -2.526 |      0.00369 |                   2 |
|     17 | secedo     |      -2.526 |      0.00369 |                   2 |
|     18 | frendo     |      -2.526 |      0.00369 |                   2 |
|     19 | praepotens |      -2.526 |      0.00369 |                   2 |
|     20 | deuius     |      -2.526 |      0.00369 |                   2 |

**Supplementary (contrastive): words that most favour Topic 6 over the next-best topic for Ecerinis, Topic 8** (dominant in: Octavia). Pull = count × (log p(w|topic) − log p(w|next-best topic)).

| lemma     |   count_in_ecerinis |   pull | in_topic_top20_relevance   |
|:----------|--------------------:|-------:|:---------------------------|
| lis       |                   6 | 23.784 | True                       |
| actus     |                   5 | 18.931 | True                       |
| potior    |                   3 |  9.88  | True                       |
| triplex   |                   3 |  9.88  | True                       |
| desino    |                   3 |  9.879 | True                       |
| patulus   |                   3 |  9.878 | True                       |
| spons     |                   3 |  9.878 | True                       |
| iudex     |                   3 |  9.877 | False                      |
| supernus  |                   3 |  9.877 | True                       |
| fido      |                   3 |  9.877 | False                      |
| anxius    |                   3 |  9.876 | True                       |
| largus    |                   3 |  9.874 | False                      |
| inuado    |                   3 |  9.871 | False                      |
| pons      |                   3 |  9.87  | False                      |
| forum     |                   5 |  7.963 | True                       |
| ciuitas   |                   2 |  5.819 | True                       |
| mensis    |                   2 |  5.818 | False                      |
| excludo   |                   2 |  5.817 | True                       |
| continuus |                   2 |  5.817 | False                      |
| frendo    |                   2 |  5.817 | True                       |

## v2, seed 42, k = 8 (seed 42)

- Ecerinis's dominant topic: Topic 2, weight 0.998; shared as dominant topic with: no other play.
- Ecerinis has 311 word types (416 tokens) in the model vocabulary; 311 carry weight into Topic 2. The top 20 account for 17% of Ecerinis's mass in the topic.
- Of the topic's top 20 words by relevance, 20 occur in Ecerinis.

**Words that place Ecerinis in the topic (top 20):**

| lemma     |   count_in_ecerinis |   expected_tokens_in_topic |   share_of_ecerinis_topic_mass |   plays_containing | in_topic_top20_relevance   |   pull_vs_next_best_topic |
|:----------|--------------------:|---------------------------:|-------------------------------:|-------------------:|:---------------------------|--------------------------:|
| lis       |                   6 |                          6 |                         0.0144 |                  2 | True                       |                    16.552 |
| atrox     |                   6 |                          6 |                         0.0144 |                  4 | True                       |                    16.541 |
| actus     |                   5 |                          5 |                         0.012  |                  4 | True                       |                    13.778 |
| adulter   |                   4 |                          4 |                         0.0096 |                  4 | True                       |                     9.485 |
| forum     |                   4 |                          4 |                         0.0096 |                  3 | True                       |                     9.469 |
| plebs     |                   4 |                          4 |                         0.0096 |                  3 | True                       |                     9.466 |
| rabies    |                   4 |                          4 |                         0.0096 |                  4 | True                       |                     9.462 |
| triplex   |                   3 |                          3 |                         0.0072 |                  2 | True                       |                     6.339 |
| pons      |                   3 |                          3 |                         0.0072 |                  2 | True                       |                     6.267 |
| supernus  |                   3 |                          3 |                         0.0072 |                  3 | True                       |                     6.265 |
| series    |                   3 |                          3 |                         0.0072 |                  5 | True                       |                     6.263 |
| patulus   |                   3 |                          3 |                         0.0072 |                  4 | True                       |                     6.261 |
| desino    |                   3 |                          3 |                         0.0072 |                  3 | True                       |                     6.267 |
| largus    |                   3 |                          3 |                         0.0072 |                  4 | False                      |                     6.26  |
| potior    |                   3 |                          3 |                         0.0072 |                  4 | True                       |                     6.262 |
| deuoueo   |                   3 |                          3 |                         0.0072 |                  2 | True                       |                     6.257 |
| iudex     |                   3 |                          3 |                         0.0072 |                  5 | False                      |                     6.269 |
| anxius    |                   3 |                          3 |                         0.0072 |                  4 | True                       |                     6.249 |
| secedo    |                   2 |                          2 |                         0.0048 |                  3 | False                      |                     3.449 |
| superstes |                   2 |                          2 |                         0.0048 |                  3 | False                      |                     3.446 |

**Words that define the topic (top 20 by relevance, λ = 0.6):**

|   rank | lemma      |   relevance |   p(w|topic) |   count_in_ecerinis |
|-------:|:-----------|------------:|-------------:|--------------------:|
|      1 | lis        |      -1.858 |      0.0099  |                   6 |
|      2 | actus      |      -1.914 |      0.00987 |                   5 |
|      3 | atrox      |      -2     |      0.0099  |                   6 |
|      4 | forum      |      -2.253 |      0.00667 |                   4 |
|      5 | triplex    |      -2.284 |      0.00517 |                   3 |
|      6 | rabies     |      -2.306 |      0.00667 |                   4 |
|      7 | plebs      |      -2.306 |      0.00667 |                   4 |
|      8 | pons       |      -2.307 |      0.00505 |                   3 |
|      9 | adulter    |      -2.348 |      0.00671 |                   4 |
|     10 | desino     |      -2.396 |      0.00505 |                   3 |
|     11 | deuoueo    |      -2.396 |      0.00505 |                   3 |
|     12 | patulus    |      -2.469 |      0.00505 |                   3 |
|     13 | potior     |      -2.469 |      0.00505 |                   3 |
|     14 | supernus   |      -2.469 |      0.00505 |                   3 |
|     15 | series     |      -2.531 |      0.00505 |                   3 |
|     16 | anxius     |      -2.531 |      0.00505 |                   3 |
|     17 | praepotens |      -2.577 |      0.00344 |                   2 |
|     18 | allido     |      -2.577 |      0.00344 |                   2 |
|     19 | sinister   |      -2.577 |      0.00344 |                   2 |
|     20 | recolo     |      -2.577 |      0.00344 |                   2 |

**Supplementary (contrastive): words that most favour Topic 2 over the next-best topic for Ecerinis, Topic 8** (dominant in: no play). Pull = count × (log p(w|topic) − log p(w|next-best topic)).

| lemma     |   count_in_ecerinis |   pull | in_topic_top20_relevance   |
|:----------|--------------------:|-------:|:---------------------------|
| lis       |                   6 | 16.552 | True                       |
| atrox     |                   6 | 16.541 | True                       |
| actus     |                   5 | 13.778 | True                       |
| adulter   |                   4 |  9.485 | True                       |
| forum     |                   4 |  9.469 | True                       |
| plebs     |                   4 |  9.466 | True                       |
| rabies    |                   4 |  9.462 | True                       |
| triplex   |                   3 |  6.339 | True                       |
| iudex     |                   3 |  6.269 | False                      |
| pons      |                   3 |  6.267 | True                       |
| desino    |                   3 |  6.267 | True                       |
| supernus  |                   3 |  6.265 | True                       |
| series    |                   3 |  6.263 | True                       |
| potior    |                   3 |  6.262 | True                       |
| patulus   |                   3 |  6.261 | True                       |
| largus    |                   3 |  6.26  | False                      |
| deuoueo   |                   3 |  6.257 | True                       |
| anxius    |                   3 |  6.249 | True                       |
| secedo    |                   2 |  3.449 | False                      |
| superstes |                   2 |  3.446 | False                      |

## v2, seed 35, k = 9 (representative seed, rule-selected k)

- Ecerinis's dominant topic: Topic 3, weight 0.998; shared as dominant topic with: no other play.
- Ecerinis has 311 word types (416 tokens) in the model vocabulary; 311 carry weight into Topic 3. The top 20 account for 17% of Ecerinis's mass in the topic.
- Of the topic's top 20 words by relevance, 20 occur in Ecerinis.

**Words that place Ecerinis in the topic (top 20):**

| lemma     |   count_in_ecerinis |   expected_tokens_in_topic |   share_of_ecerinis_topic_mass |   plays_containing | in_topic_top20_relevance   |   pull_vs_next_best_topic |
|:----------|--------------------:|---------------------------:|-------------------------------:|-------------------:|:---------------------------|--------------------------:|
| lis       |                   6 |                          6 |                         0.0144 |                  2 | True                       |                    24.232 |
| atrox     |                   6 |                          6 |                         0.0144 |                  4 | True                       |                    24.224 |
| actus     |                   5 |                          5 |                         0.012  |                  4 | True                       |                    19.296 |
| forum     |                   4 |                          4 |                         0.0096 |                  3 | True                       |                     5.372 |
| rabies    |                   4 |                          4 |                         0.0096 |                  4 | True                       |                     5.37  |
| adulter   |                   4 |                          4 |                         0.0096 |                  4 | True                       |                    14.565 |
| plebs     |                   4 |                          4 |                         0.0096 |                  3 | True                       |                     1.254 |
| series    |                   3 |                          3 |                         0.0072 |                  5 | True                       |                     3.193 |
| potior    |                   3 |                          3 |                         0.0072 |                  4 | True                       |                    10.092 |
| pons      |                   3 |                          3 |                         0.0072 |                  2 | True                       |                    10.094 |
| triplex   |                   3 |                          3 |                         0.0072 |                  2 | True                       |                    10.094 |
| desino    |                   3 |                          3 |                         0.0072 |                  3 | True                       |                    10.092 |
| anxius    |                   3 |                          3 |                         0.0072 |                  4 | True                       |                    10.091 |
| patulus   |                   3 |                          3 |                         0.0072 |                  4 | True                       |                    10.093 |
| supernus  |                   3 |                          3 |                         0.0072 |                  3 | True                       |                    10.094 |
| deuoueo   |                   3 |                          3 |                         0.0072 |                  2 | True                       |                    10.095 |
| largus    |                   3 |                          3 |                         0.0072 |                  4 | False                      |                    10.089 |
| iudex     |                   3 |                          3 |                         0.0072 |                  5 | False                      |                    10.086 |
| continuus |                   2 |                          2 |                         0.0048 |                  2 | False                      |                     5.955 |
| frendo    |                   2 |                          2 |                         0.0048 |                  2 | False                      |                     5.955 |

**Words that define the topic (top 20 by relevance, λ = 0.6):**

|   rank | lemma      |   relevance |   p(w|topic) |   count_in_ecerinis |
|-------:|:-----------|------------:|-------------:|--------------------:|
|      1 | lis        |      -1.82  |      0.01029 |                   6 |
|      2 | atrox      |      -1.962 |      0.01029 |                   6 |
|      3 | actus      |      -2.052 |      0.0086  |                   5 |
|      4 | forum      |      -2.216 |      0.00692 |                   4 |
|      5 | plebs      |      -2.27  |      0.00692 |                   4 |
|      6 | rabies     |      -2.27  |      0.00692 |                   4 |
|      7 | triplex    |      -2.271 |      0.00524 |                   3 |
|      8 | pons       |      -2.271 |      0.00524 |                   3 |
|      9 | adulter    |      -2.317 |      0.00692 |                   4 |
|     10 | deuoueo    |      -2.36  |      0.00524 |                   3 |
|     11 | desino     |      -2.36  |      0.00524 |                   3 |
|     12 | potior     |      -2.433 |      0.00524 |                   3 |
|     13 | patulus    |      -2.433 |      0.00524 |                   3 |
|     14 | supernus   |      -2.433 |      0.00524 |                   3 |
|     15 | anxius     |      -2.495 |      0.00524 |                   3 |
|     16 | series     |      -2.495 |      0.00524 |                   3 |
|     17 | praepotens |      -2.544 |      0.00355 |                   2 |
|     18 | fulgur     |      -2.544 |      0.00355 |                   2 |
|     19 | recolo     |      -2.544 |      0.00355 |                   2 |
|     20 | ciuitas    |      -2.544 |      0.00355 |                   2 |

**Supplementary (contrastive): words that most favour Topic 3 over the next-best topic for Ecerinis, Topic 7** (dominant in: Octavia). Pull = count × (log p(w|topic) − log p(w|next-best topic)).

| lemma     |   count_in_ecerinis |   pull | in_topic_top20_relevance   |
|:----------|--------------------:|-------:|:---------------------------|
| lis       |                   6 | 24.232 | True                       |
| atrox     |                   6 | 24.224 | True                       |
| actus     |                   5 | 19.296 | True                       |
| adulter   |                   4 | 14.565 | True                       |
| deuoueo   |                   3 | 10.095 | True                       |
| supernus  |                   3 | 10.094 | True                       |
| triplex   |                   3 | 10.094 | True                       |
| pons      |                   3 | 10.094 | True                       |
| patulus   |                   3 | 10.093 | True                       |
| potior    |                   3 | 10.092 | True                       |
| desino    |                   3 | 10.092 | True                       |
| anxius    |                   3 | 10.091 | True                       |
| largus    |                   3 | 10.089 | False                      |
| iudex     |                   3 | 10.086 | False                      |
| fulgur    |                   2 |  5.955 | True                       |
| ultio     |                   2 |  5.955 | False                      |
| frendo    |                   2 |  5.955 | False                      |
| continuus |                   2 |  5.955 | False                      |
| allido    |                   2 |  5.955 | False                      |
| excludo   |                   2 |  5.954 | False                      |

## v2, seed 29, k = 8 (representative seed at k = 8)

- Ecerinis's dominant topic: Topic 6, weight 0.998; shared as dominant topic with: no other play.
- Ecerinis has 311 word types (416 tokens) in the model vocabulary; 311 carry weight into Topic 6. The top 20 account for 17% of Ecerinis's mass in the topic.
- Of the topic's top 20 words by relevance, 20 occur in Ecerinis.

**Words that place Ecerinis in the topic (top 20):**

| lemma     |   count_in_ecerinis |   expected_tokens_in_topic |   share_of_ecerinis_topic_mass |   plays_containing | in_topic_top20_relevance   |   pull_vs_next_best_topic |
|:----------|--------------------:|---------------------------:|-------------------------------:|-------------------:|:---------------------------|--------------------------:|
| lis       |                   6 |                          6 |                         0.0144 |                  2 | True                       |                    23.532 |
| atrox     |                   6 |                          6 |                         0.0144 |                  4 | True                       |                    23.519 |
| actus     |                   5 |                          5 |                         0.012  |                  4 | True                       |                    18.714 |
| forum     |                   4 |                          4 |                         0.0096 |                  3 | True                       |                     5.331 |
| adulter   |                   4 |                          4 |                         0.0096 |                  4 | True                       |                    14.096 |
| rabies    |                   4 |                          4 |                         0.0096 |                  4 | True                       |                     5.331 |
| plebs     |                   4 |                          4 |                         0.0096 |                  3 | True                       |                     1.245 |
| patulus   |                   3 |                          3 |                         0.0072 |                  4 | True                       |                     9.748 |
| triplex   |                   3 |                          3 |                         0.0072 |                  2 | True                       |                     9.75  |
| pons      |                   3 |                          3 |                         0.0072 |                  2 | True                       |                     9.75  |
| desino    |                   3 |                          3 |                         0.0072 |                  3 | True                       |                     9.75  |
| deuoueo   |                   3 |                          3 |                         0.0072 |                  2 | True                       |                     9.749 |
| potior    |                   3 |                          3 |                         0.0072 |                  4 | True                       |                     9.749 |
| supernus  |                   3 |                          3 |                         0.0072 |                  3 | True                       |                     9.745 |
| anxius    |                   3 |                          3 |                         0.0072 |                  4 | True                       |                     9.745 |
| series    |                   3 |                          3 |                         0.0072 |                  5 | True                       |                     3.166 |
| iudex     |                   3 |                          3 |                         0.0072 |                  5 | False                      |                     9.747 |
| largus    |                   3 |                          3 |                         0.0072 |                  4 | False                      |                     9.737 |
| continuus |                   2 |                          2 |                         0.0048 |                  2 | False                      |                     5.73  |
| sinister  |                   2 |                          2 |                         0.0048 |                  2 | True                       |                     5.731 |

**Words that define the topic (top 20 by relevance, λ = 0.6):**

|   rank | lemma    |   relevance |   p(w|topic) |   count_in_ecerinis |
|-------:|:---------|------------:|-------------:|--------------------:|
|      1 | lis      |      -1.854 |      0.00994 |                   6 |
|      2 | atrox    |      -1.997 |      0.00994 |                   6 |
|      3 | actus    |      -2.086 |      0.00832 |                   5 |
|      4 | forum    |      -2.25  |      0.00669 |                   4 |
|      5 | plebs    |      -2.303 |      0.00669 |                   4 |
|      6 | rabies   |      -2.303 |      0.00669 |                   4 |
|      7 | pons     |      -2.303 |      0.00507 |                   3 |
|      8 | triplex  |      -2.303 |      0.00507 |                   3 |
|      9 | adulter  |      -2.35  |      0.00669 |                   4 |
|     10 | desino   |      -2.393 |      0.00507 |                   3 |
|     11 | deuoueo  |      -2.393 |      0.00507 |                   3 |
|     12 | potior   |      -2.466 |      0.00507 |                   3 |
|     13 | patulus  |      -2.466 |      0.00507 |                   3 |
|     14 | supernus |      -2.466 |      0.00507 |                   3 |
|     15 | anxius   |      -2.527 |      0.00507 |                   3 |
|     16 | series   |      -2.527 |      0.00507 |                   3 |
|     17 | allido   |      -2.574 |      0.00345 |                   2 |
|     18 | frendo   |      -2.574 |      0.00345 |                   2 |
|     19 | sinister |      -2.574 |      0.00345 |                   2 |
|     20 | ciuitas  |      -2.574 |      0.00345 |                   2 |

**Supplementary (contrastive): words that most favour Topic 6 over the next-best topic for Ecerinis, Topic 4** (dominant in: Octavia). Pull = count × (log p(w|topic) − log p(w|next-best topic)).

| lemma     |   count_in_ecerinis |   pull | in_topic_top20_relevance   |
|:----------|--------------------:|-------:|:---------------------------|
| lis       |                   6 | 23.532 | True                       |
| atrox     |                   6 | 23.519 | True                       |
| actus     |                   5 | 18.714 | True                       |
| adulter   |                   4 | 14.096 | True                       |
| triplex   |                   3 |  9.75  | True                       |
| desino    |                   3 |  9.75  | True                       |
| pons      |                   3 |  9.75  | True                       |
| deuoueo   |                   3 |  9.749 | True                       |
| potior    |                   3 |  9.749 | True                       |
| patulus   |                   3 |  9.748 | True                       |
| iudex     |                   3 |  9.747 | False                      |
| anxius    |                   3 |  9.745 | True                       |
| supernus  |                   3 |  9.745 | True                       |
| largus    |                   3 |  9.737 | False                      |
| sinister  |                   2 |  5.731 | True                       |
| continuus |                   2 |  5.73  | False                      |
| frendo    |                   2 |  5.73  | True                       |
| ciuitas   |                   2 |  5.73  | True                       |
| murmuro   |                   2 |  5.73  | False                      |
| allido    |                   2 |  5.73  | True                       |

## Figures

- `figures/fig_a3_original_seed42_k8.png`: original, seed 42, k = 8 (conference model): Ecerinis's attribution words (left) vs the topic's top relevance words (right).
- `figures/fig_a3_original_seed25_k8.png`: original, seed 25, k = 8 (representative seed, rule-selected k): Ecerinis's attribution words (left) vs the topic's top relevance words (right).
- `figures/fig_a3_v2_seed42_k8.png`: v2, seed 42, k = 8 (seed 42): Ecerinis's attribution words (left) vs the topic's top relevance words (right).
- `figures/fig_a3_v2_seed35_k9.png`: v2, seed 35, k = 9 (representative seed, rule-selected k): Ecerinis's attribution words (left) vs the topic's top relevance words (right).
- `figures/fig_a3_v2_seed29_k8.png`: v2, seed 29, k = 8 (representative seed at k = 8): Ecerinis's attribution words (left) vs the topic's top relevance words (right).
