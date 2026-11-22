# A1 review: what needs approval before the reruns

Nothing below has been applied. All model results so far use the original pipeline.

## Files to review

| File | What it is | How to approve |
|---|---|---|
| `data/variant_map_proposed.json` | 55 spelling mappings (uoltus→uultus, thorus→torus, assimilated prefixes, exs-), 3 optional syncope pairs, 19 rejected pairs with reasons | Delete lines you reject; move optional ones into `map` |
| `data/lemma_fixes_proposed.csv` | 146 LatinCy lemmatization errors (133 high confidence, 13 medium), keyed by surface form (homographs, truncated or non-word lemmas, empty lemmas) | Fill `approve` (y/n), or tell me "all high" / "all" |
| `data/lemma_policy_proposed.csv` | 30 optional merges: gerundive lemmas → verb (timendus→timeo), regular comparatives/superlatives → positive (grauior→grauis) | Same |
| `data/named_entities_proposed.csv` | 45 names missing from the named-entity list (Adda, Vicenza, Padua, Azzo, Salinguerra, Ossa, Procrustes …) | Same |
| `data/named_entities_share.csv` | Evidence for the named-entity issue below | Decision, not row approval |

Evidence: `variant_candidates.csv`, `lemma_audit.csv` (all heuristic flags, including unreviewed long-tail rows), `base_rules_preview.md`, `build_comparison.md`, `../a0_reproduction/reproduction_check.md`.

## Decisions needed

1. **Named-entity list.** `unique_named_entities.pkl` adds a lemma after a single PERSON/LOC/NORP tag anywhere, and the pipeline then removes every occurrence of it. 285 of the 1,272 lemmas were tagged in under half their occurrences, e.g. scelus 4/241, magnus 2/216, poena 1/108, ira 1/99, furor 1/84, urbs 1/66. Together they remove **9,223 content tokens, 489 of them in Ecerinis** (of the 670 Ecerinis loses at this step). Options: (a) keep the list as-is for the baseline and add a cleaned list (share ≥ 0.5) as a robustness condition, like A5; (b) replace it. Recommendation: (a).
2. **v-spelled common words on the named-entity list** (virgo, iuvenis, avidus, saevus, vinco, vagus, solvo, verso, venio, iuvenilis). Today they don't match the u-spelled tokens. Normalizing the list would start removing uirgo (48), iuuenis (27) and others. Recommendation: exempt them. Likewise, keep tenuis (16) out of the normalized stopword list.
3. **Scope of "normalized".** The brief's A1 is spelling only. Recommendation: one "normalized" condition = spelling map + approved lemma fixes (+ policy rows if you approve them), compared against the original pipeline, rather than adding a third condition to every A2 grid.

## LatinCy 3.9.8 test (`latincy398_test.md`, `latincy398_disagreements.csv`)

- On 189 tokens with known errors in the saved lemmas, 3.9.8 is right on 149; the saved lemmas on 32. This set was chosen because the old build failed on it, so it favours 3.9.8. 3.9.8 still gets wrong: manes (19 of 47 tokens; all 47 are the Manes), vindices (3 of 10), Ecerinis vitas (→ uito), lare (→ larus), rati (→ ratis), and vendicemus (copied as uendico).
- Overall, 3.9.8 and the saved lemmas agree on 89.6% of kept tokens (41,695 / 46,544). The disagreements mix corrections (pavit, verbera, dest), different headword spellings (coniunx → coniux 136, adsum → assum, exul → exsul, umerus → humerus), merges of comparatives and superlatives into the positive (maior → magnus, melior → bonus, summus → superus, extremus → exter), and some likely 3.9.8 errors (rex → rego, ferus → fero, tutus → tuor). These haven't been scored yet.
- NER is not better for this purpose. Ordinary words are still tagged occasionally (scelus 5/241, mors 12/162). Under the notebook's one-tag rule, 217 of the 285 ordinary-word lemmas would still be on the list.

## Root cause of the named-entity problem: capitalized verse lines in Ecerinis

- Ecerinis's text capitalizes every verse line: 24.8% of its words are capitalized, against 3–9% in the Seneca texts. Both LatinCy builds tag line-initial verbs and nouns as PERSON or PROPN (Abinde, Absorbet, Adiere, Annue …).
- 284 of the 285 ordinary-word lemmas on the named-entity list got there through tags on capitalized tokens. 109 of them come from Ecerinis tags alone (peto, caelum, frater, poena, ferrum, urbs, dolus, crimen …), and the remove-everywhere rule deletes 3,083 tokens of them across all eleven plays.
- The capitals also damage Ecerinis's lemmas: 178 kept tokens are PROPN with the surface form copied as the lemma (absorbet, adiere). These become Ecerinis-only types that `no_below` then removes.
- Test with 3.9.8 on Ecerinis, lowercasing line starts except words capitalized mid-line elsewhere: entity-tagged words 345 → 109 (almost all real names), PROPN among kept tokens 321 → 125, surface-copied PROPN lemmas 178 → 62.
- The act-level Ecerinis text is already lowercased at line starts, so the two levels were processed from differently formatted text.

## Findings so far

- **Reproduction:** seed 42 reproduces in the new `.venv` (k=2–9 match exactly, k=8 still wins at 0.2608; doc-topic differences ≤ 3e-5). k=1 coherence differs (0.3983 → 0.4052); k=1 is never selected.
- **Topic 7 at k=8 is the dominant topic of five plays, not three:** Phaedra (0.334) and Hercules Furens (0.491) as well as Medea, Hercules Oetaeus and Ecerinis.
- Ecerinis keeps **377** tokens after the dictionary filter (brief estimated ~450): 2,330 processed → 1,660 after named-entity removal → 377.
- **Two Topic 7 keywords rest on lemma errors.** uindico: 6 of its Hercules Oetaeus tokens are *vindicem* (vindex). pons: every Seneca "pons" is *ponti* (pontus, the sea). Ecerinis's own pons tokens are real bridges, so its link to Seneca through pons is an artefact. Ecerinis also has uindico in the medieval spelling *vendico* (2 tokens), which LatinCy left with an empty lemma.
- **LatinCy builds:** the play-level DocBin (earlier build) and the act-level DocBin (3.8.0) give identical lemmas on 81,897 of 81,903 aligned tokens. Re-lemmatizing is unnecessary. Neither build can be downloaded any more (the Hugging Face repo was recreated in March 2026; only 3.9.6 and 3.9.8 are available), so the saved DocBins are the record of the lemmatization.
- **Act-level text differs from play-level text:** the Phaedra acts are missing the opening 434 tokens ("Ite, umbrosas cingite silvas …"). The Ecerinis acts come from a different TEI version: a 32-token passage missing ("Sic fatus ima parte secessit domus … Luciferum ciet"), speaker labels and a line number ("340") included, and typos (*dtabiles*, *dub*). Not fixed; this affects the act-level A2 check.
- **Ecerinis is mostly in classical spelling.** The medieval forms found are thoro, Aethna-, arctho-, Stix, thus, Setis, sulphureus, executor, negligens, vendico. All are in the proposed map or fixes.
- 64 tokens (11 in Ecerinis) have an empty lemma, including OCR noise in the Seneca text (Plirygiurn, victamqne, orbεs, fiexa) and speaker labels (TIR, NVT).
