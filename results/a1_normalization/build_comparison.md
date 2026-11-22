# LatinCy build comparison: play level (earlier build) vs act level (3.8.0)

- Play DocBin reproduces processed_corpus.pkl: 11/11 plays
- Act DocBin reproduces processed_acts.pkl: 56/56 acts

| play             |   play_tokens |   act_tokens |   aligned |   lemma_diffs |   pos_diffs |   kept_tokens_play |   kept_tokens_acts |   kept_count_L1_diff |
|:-----------------|--------------:|-------------:|----------:|--------------:|------------:|-------------------:|-------------------:|---------------------:|
| Phoenissae       |          4994 |         4994 |      4994 |             0 |           1 |               2548 |               2548 |                    0 |
| Troades          |          8216 |         8216 |      8216 |             0 |           1 |               4502 |               4502 |                    0 |
| Phaedra          |          8565 |         8131 |      8131 |             0 |           0 |               5065 |               4787 |                  278 |
| Agamemnon        |          6605 |         6605 |      6605 |             0 |           0 |               3918 |               3918 |                    0 |
| Hercules Furens  |          9076 |         9078 |      9076 |             0 |           1 |               5314 |               5315 |                    1 |
| Medea            |          6914 |         6914 |      6914 |             0 |           0 |               3784 |               3784 |                    0 |
| Octavia          |          6149 |         6149 |      6149 |             0 |           0 |               3526 |               3526 |                    0 |
| Oedipus          |          6975 |         6975 |      6975 |             1 |           0 |               4197 |               4197 |                    2 |
| Thyestes         |          7474 |         7474 |      7474 |             0 |           0 |               4094 |               4094 |                    0 |
| Hercules Oetaeus |         13658 |        13658 |     13658 |             0 |           0 |               7280 |               7280 |                    0 |
| Ecerinis         |          4139 |         4111 |      3711 |             5 |          10 |               2330 |               2304 |                   76 |

- Total lemma disagreements on aligned tokens: 6 of 81903 (0.01%)
- Total POS disagreements: 13

## Most frequent disagreements

| surface     | lemma_play_build   | lemma_act_build   |   n |
|:------------|:-------------------|:------------------|----:|
| Deus        | Deus               | Deus              |   2 |
| A           | ab                 | a                 |   1 |
| ardens      | ardens             | ardeo             |   1 |
| vertit      |                    | verto             |   1 |
| secus       | secus              | secus             |   1 |
| remotos     | remotus            | remotus           |   1 |
| pervetustae | pervetuso          | pervetuso         |   1 |
| malis       | malum              | malus             |   1 |
| lubrici     | lubrix             | lubricus          |   1 |
| Victrice    | uictrix            | uictrix           |   1 |
| Comes       | comes              | comes             |   1 |
| Praedicta   | praedictum         | praedictus        |   1 |
| Pellavicino | pellavicinus       | pellavicinus      |   1 |
| Ferrariae   | ferrarius          | ferrarius         |   1 |
| Felix       | Felix              | Felix             |   1 |
| Depulse     | depulsus           | depulsus          |   1 |
| Contexe     | contexo            | contexo           |   1 |
| —           | —                  | —                 |   1 |
