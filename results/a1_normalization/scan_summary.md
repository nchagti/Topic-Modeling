# A1 scan summary (for review; nothing applied)

## Fixed rules (v->u, j->i)

| play             |   tokens |   tokens_changed |   pct_tokens_changed |   types_changed |   newly_stopwords |
|:-----------------|---------:|-----------------:|---------------------:|----------------:|------------------:|
| Phoenissae       |     2548 |               19 |                  0.7 |              17 |                 0 |
| Troades          |     4502 |               50 |                  1.1 |              38 |                 1 |
| Phaedra          |     5065 |               53 |                  1   |              42 |                 2 |
| Agamemnon        |     3918 |               32 |                  0.8 |              27 |                 0 |
| Hercules Furens  |     5314 |               53 |                  1   |              44 |                 2 |
| Medea            |     3784 |               28 |                  0.7 |              25 |                 2 |
| Octavia          |     3526 |               36 |                  1   |              24 |                 2 |
| Oedipus          |     4197 |               41 |                  1   |              30 |                 4 |
| Thyestes         |     4094 |               33 |                  0.8 |              31 |                 0 |
| Hercules Oetaeus |     7280 |               43 |                  0.6 |              23 |                 3 |
| Ecerinis         |     2330 |               27 |                  1.2 |              22 |                 0 |

78 pairs of types merge (e.g. invado/inuado). Full list: `base_rules_preview.md`.

## Variant candidates (`variant_candidates.csv`)

- 69 candidate groups; by suggestion: check: 40, apply (LatinCy lookup lists it as a form of the canonical lemma): 15, likely reject (both are separate headwords): 14

## Lemma audit (`lemma_audit.csv`)

- Priority A: lemma has a non-lemma shape (truncated, enclitic attached, comparative, gerundive, inflected ending). B: LatinCy's own lookup table assigns the surface forms to another lemma (homographs; the lookup is single-valued, so many B rows are lookup errors). C: only flagged as a possible missed named entity (mostly PROPN).
- The lookup table (la-latincy-lookups 1.0.0) is incomplete: many correct lemmas are absent from it, so absence alone is not flagged.

| priority   |   lemmas |   tokens |   in_dictionary |   ecerinis_tokens |
|:-----------|---------:|---------:|----------------:|------------------:|
| A          |      298 |     1010 |              70 |                70 |
| B          |      443 |     1069 |              84 |                69 |
| C          |       41 |       56 |              10 |                12 |
