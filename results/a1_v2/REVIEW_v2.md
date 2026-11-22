# v2 pipeline (LatinCy 3.9.8): what needs approval before the reruns

The original pipeline (saved lemmas, earlier LatinCy build) is untouched and remains the conference baseline (tag `v0.1-conference-2026`). Nothing below has been run through LDA yet.

## What v2 does

0. **Sources** (`src/sources.py`): Ecerinis from the NeoLatDraCor TEI pinned at commit `3d4653db`, with 3 corrections in `data/sources/ecerinis_patches.json`; Seneca unchanged.
1. **Line-start lowercasing, same rule for every play** (`src/preprocess_v2.py`, log in `line_lowercasing.csv`). The first word of a verse line is lowercased unless that form is capitalized mid-line and mid-sentence somewhere in the corpus. Ecerinis: 231 of 654 lines (the published TEI capitalizes sentence starts only); Seneca: 39–202 lines per play.
2. **LatinCy 3.9.8** (pinned by commit and sha256 in `requirements.txt`), plus the notebooks' inquit → inquam and ablatus → aufero.
3. **Acts cut from the play parse** (`src/acts_v2.py`, `acts_v2_report.md`): act boundaries come from aligning the old act files to the play text, so both levels have the same text and lemmas. Phaedra Act 1 now includes the 90-line prelude; Ecerinis' acts use the play-level text (complete, no typos).
4. **Validation** against LiLa and Morpheus (`src/validate_v2.py`, `validation.md`; responses cached in `data/lexicon_cache/`).

## Results so far

| | original | v2 |
|---|---|---|
| Kept lemma types found in LiLa | 88.7% | 92.3% |
| Kept tokens whose lemma is in LiLa | 97.6% | 98.5% |
| Ecerinis: content tokens → after named-entity removal → after dictionary filter | 2,330 → 1,660 → 377 | 2,324 → 2,203 → 420 |
| Kept proper-noun tokens in Ecerinis | 321 | 127 |

Where the builds disagree (4,584 kept tokens), Morpheus accepts only 3.9.8's lemma on 987 and only the old build's on 695; both are valid on 2,084. Part of the "only old build valid" group is Morpheus missing words that 3.9.8 gets right (Manes, Creon, Maenas, Dis).

**Known 3.9.8 errors:** anime → anima (28; vocative of animus), manes → maneo (26 still wrong), Ecerinis vitas → uito (vita), lare → larus, rati → ratis, Ecerinis vendico copied as uendico.

## Decisions needed

1. **Resolved (2026-11-21):** all context-reading recommendations accepted; Oedipus 'Ponti regna' (the sea) is kept as a word through a token override. The final decisions are in `data/v2/named_entities_final.json`, applied by `src/ne_final.py` (`named_entities_final.md`): 646 names, 7 per-token lemmas, 2,469 tokens removed (121 in Ecerinis). Original notes:
   **Named-entity list** (`data/v2/named_entities_v2.csv`, 604 names). Rule:
   - LiLa lists the lemma only as a proper noun → name, unless 3.9.8 mostly tags it ADJ or VERB (tacitus, patiens, doctus collide with LiLa name entries);
   - LiLa lists it as a proper noun and a common word → name if 3.9.8 tags it as a name in at least half its occurrences;
   - not in LiLa → same 50% test.

   Theme words stay words: scelus, poena, urbs, ira, furor, dolus, crimen.
   **Context reading of the 149 uncertain lemmas** (`data/v2/named_entities_recommendations.csv`; passages in `named_entity_contexts.txt`): 100 names, 42 words, 7 decided per token (homographs). This changes the rule's decision for 70 lemmas (313 tokens). Principles P1–P6 are in `src/ne_recommendations.py`. **Borderline personifications, your call:** Fortuna (tagged as a name 49% of the time; currently a word), Caritas and Impietas (50%; currently names), Cupido (40%) and Auster (44%) (currently words).
2. **Resolved (2026-11-21):** the context-checked spelling map was accepted, `data/v2/variant_map_v2.json`: 29 mappings, canonical = the spelling the texts use most often. The 6 lemma fixes found behind false pairs were accepted (`lemma_fixes_v2.csv`). Everything is applied by `src/v2_corpus.py` (`token_lists_v2.md`): Ecerinis has 2,203 tokens, 421 after the dictionary filter.
3. **Resolved (2026-11-21): accepted as they are.** **3.9.8 lemma conventions.** 3.9.8 merges comparatives and superlatives into the positive (maior → magnus, melior → bonus, minor → paruus, extremus → exter, imus → inferus), lemmatizes many participles to the verb (mixtus → misceo, iussus → iubeo, ardens → ardeo), and keeps some substantive plurals (superi, inferi, manes). Recommendation: accept them as they are. They're consistent across the corpus, and undoing them would mean hand-editing hundreds of lemmas.
4. **Resolved (2026-11-21): triage accepted and applied** (136 approved fix rows in total, 650 names). Final v2 token lists: Ecerinis has 2,198 tokens, 416 after the dictionary filter; the dictionary has 1,600 types (`token_lists_v2.md`). Triage notes: Claude read the passages for the 333 priority groups, the 12 Seneca manes → maneo tokens, the 28 anime → anima tokens and the cecid- forms (`lemma_triage.csv`, `lemma_contexts.txt`). Result: 129 groups fixed (189 tokens; 36 in Ecerinis), 199 kept, 3 dropped, 2 names. That is 128 fix rows marked 'proposed (lemma triage)' in `data/v2/lemma_fixes_v2.csv`, and 4 name additions in `data/v2/named_entities_additions.csv`. Original note: **Remaining lemma review** (`validation_review_prioritized.csv`). 159 groups (434 tokens; 67 groups in Ecerinis) can change the LDA vocabulary or occur in Ecerinis. Many are Morpheus gaps, not errors. Recommendation: I triage these 159, each with its evidence (Morpheus candidates, LiLa entry, one passage of context), with my judgments labelled as such for you to check. The known 3.9.8 errors above get fixed as part of this.
5. ~~Ecerinis text~~ **Resolved:** Ecerinis now comes from the NeoLatDraCor TEI pinned at commit `3d4653db` (CC0), all 654 lines, with 3 logged corrections; act boundaries come from the TEI (`src/sources.py`, `sources_report.md`). The Seneca text is unchanged, and its match with DraCor and the local TEI copies is recorded.

## Superseded

`data/variant_map_proposed.json`, `data/lemma_fixes_proposed.csv`, `data/lemma_policy_proposed.csv` and `data/named_entities_proposed.csv` were built on the old lemmas. They're kept for the record, but v2 doesn't use them.
