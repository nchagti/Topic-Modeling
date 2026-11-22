# v2 scans (LatinCy 3.9.8 lemmas)

## Ecerinis token funnel (dictionary filter unchanged: no_below=2, no_above=0.5)

| pipeline | content tokens | after named-entity removal | after dictionary filter | dictionary size |
|---|---|---|---|---|
| original (saved lemmas, original list) | 2,330 | 1,660 | 377 | 1,580 |
| v2 lemmas, original list (normalized) | 2,324 | 1,696 | 370 | 1,521 |
| v2 lemmas, rebuilt list | 2,324 | 2,203 | 420 | 1,653 |

No spelling map applied yet.

## Named-entity list (`data/v2/named_entities_v2.csv`)

| decision    |   lemmas |   tokens |   ecerinis |
|:------------|---------:|---------:|-----------:|
| name        |      604 |     2365 |        121 |
| word        |      449 |     6724 |        387 |
| word (flag) |      605 |    11303 |        558 |

- Lemmas on the original list that the rebuilt list keeps as words: 541.
- Theme words: scelus → word, poena → word (flag), urbs → word (flag), ira → word (flag), furor → word (flag), dolus → word (flag), crimen → word, fortuna → word (flag), amor → word (flag)

## Spelling-variant candidates (`variant_candidates_v2.csv`)

- 46 candidate groups.

## Validation review, prioritized (`validation_review_prioritized.csv`)

- 738 groups (1,310 tokens). Priority (can change the LDA vocabulary or occur in Ecerinis, and not a name): 340 groups, 615 tokens.
