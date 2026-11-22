# v2 lemma validation (LatinCy 3.9.8 vs LiLa and Morpheus)

## LiLa coverage of kept lemmas

| pipeline | lemma types in LiLa | tokens whose lemma is in LiLa |
|---|---|---|
| old build (saved) | 4,702 / 5,303 (88.7%) | 45,443 / 46,558 (97.6%) |
| v2 (3.9.8, line starts lowercased) | 4,673 / 5,061 (92.3%) | 45,940 / 46,626 (98.5%) |

## Where the two builds disagree (kept tokens, scored by Morpheus)

4,585 aligned kept tokens have different lemmas. Morpheus lists the possible lemmas for each surface form; a lemma counts as valid if it is among them (spelling variants such as coniunx/coniux count as valid).

| class | tokens | share |
|---|---|---|
| both valid | 2,085 | 45.5% |
| only 3.9.8 valid | 987 | 21.5% |
| only old build valid | 695 | 15.2% |
| Morpheus has no analysis | 571 | 12.5% |
| neither valid | 247 | 5.4% |

Largest groups per class: `disagreement_scores.csv`.

## Status of every v2 kept token

| status | tokens | Ecerinis |
|---|---|---|
| ok | 45,105 | 2,185 |
| review: Morpheus rejects lemma for this form | 1,164 | 72 |
| review: lemma in neither resource | 146 | 22 |
| ok (not in LiLa; Morpheus confirms) | 129 | 8 |
| unverified proper noun (in neither resource) | 82 | 37 |

Token groups needing a decision: 738 (`validation_review.csv`), covering 1,310 tokens; 81 groups occur in Ecerinis.

### Top 'only old build valid' groups

| old      | latincy398   |   n |
|:---------|:-------------|----:|
| superus  | superi       |  52 |
| adsum    | assum        |  37 |
| animus   | anima        |  28 |
| extremus | exter        |  24 |
| maneo    | manes        |  24 |
| imus     | inferus      |  18 |
| paelex   | pellex       |  17 |
| tono     | tonans       |  16 |
| noceo    | nocens       |  12 |
| fauces   | faux         |  10 |
| creo     | creon        |   9 |
| maena    | maenas       |   8 |
| pigeo    | piget        |   8 |
| furo     | furens       |   7 |
| taceo    | tacitus      |   7 |

### Top 'only 3.9.8 valid' groups

| old      | latincy398   |   n |
|:---------|:-------------|----:|
| uoltus   | uultus       |  21 |
| melior   | bonus        |  18 |
| maior    | magnus       |  18 |
| mixtus   | misceo       |  17 |
| stirpes  | stirps       |  16 |
| tempto   | tento        |  15 |
| pinna    | penna        |  12 |
| ardens   | ardeo        |  12 |
| iussus   | iubeo        |  12 |
| iratus   | irascor      |  11 |
| grauus   | grauis       |  11 |
| grauior  | grauis       |  11 |
| minor    | paruus       |  10 |
| solutus  | soluo        |   8 |
| timendus | timeo        |   8 |

### Top 'neither valid' groups

| old      | latincy398   |   n |
|:---------|:-------------|----:|
| gnatus   | natus        |  23 |
| tutus    | tuor         |  13 |
| martha   | mars         |   7 |
| cadmea   | cadmeius     |   6 |
| egono    | egone        |   5 |
| dsum     | desum        |   5 |
| flagrans | fragro       |   5 |
| solemnis | sollemnis    |   4 |
| uenero   | uenerandus   |   3 |
| exero    | exsero       |   3 |
| aes      | aer          |   3 |
| oetes    | oeta         |   3 |
| assuetus | adsuesco     |   3 |
| silentum | silens       |   2 |
| secus    | secum        |   2 |

