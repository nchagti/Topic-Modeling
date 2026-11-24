# Topic Modeling Padua

This repo contains the code for static and dynamic topic modeling of the literary output of Duecento and Trecento Padua. The current work is LDA topic modeling of Albertino Mussato's *Ecerinis* against the ten tragedies of the Senecan corpus, at play level and act level, with robustness checks.

- **Conference results:** tag `v0.1-conference-2026` marks the state of the repo used for the conference paper. The notebooks and the pickles and figures they saved are the conference pipeline. They are kept unchanged.
- **Robustness checks:** branch `robustness`. The scripts are in `src/`, their outputs in `results/`, and editable inputs in `data/`.
- **Start here:** `results/SUMMARY.md` gives the findings.

## Setup

Windows, Python 3.12. Create a fresh virtual environment and install the pinned versions:

```
python -m venv .venv
```

```
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

`requirements.txt` pins every package. It includes the LatinCy model `la_core_web_lg` 3.9.8, pinned by Hugging Face commit and sha256.

The original LatinCy build behind the conference lemmas can no longer be downloaded. Its output survives as the saved DocBins and pickles in `data/original/`, and the original pipeline reads those. Only the v2 pipeline runs LatinCy.

## Repository layout

| Folder | Contents |
|---|---|
| `notebooks/` | Conference notebooks. Top level: NER, POS, lemma notebooks. `play_lda/`: play-level LDA. `act_lda/`: act-level LDA. `test_topic_modeling.ipynb` is exploratory (early tests, not part of the conference pipeline). |
| `Corpus/`, `Acts/` | Conference notebooks for cosine similarity and act extraction (`Acts/get_acts.py`), and the keyword CSVs (`Corpus/corpus_csv/`, `Acts/acts_csvs/`). |
| `models/play/`, `models/act/` | The conference LDA pickles and dictionaries (formerly `gensimvenv/corpus_pkl/` and `gensimvenv/acts_pkl/`). |
| `models/play/raw/` | The conference-era play-level model run that kept named entities (corpus, dictionary, LDA models and topics; formerly `gensimvenv/raw_corpus/`). |
| `data/original/` | Conference inputs: the stopword lists, `unique_named_entities.pkl`, `entities_info.pkl`, `topic_data.json`. `corpus/` and `acts/` hold the source JSON, DocBins and processed pickles. `ner/` holds `ner_corpus.pkl` and `ner_dictionary.gensim` (formerly in `gensimvenv/`). |
| `data/v2/`, `data/sources/`, `data/lexicon_cache/` | v2 pipeline inputs: corrected sources, approved decisions, cached lexicon responses. |
| `data/theme_lexicon.json` | Theme lexicon v2: 17 author-chosen word families and the lexicon-only token rules (A5). The earlier four-family lexicon is `data/theme_lexicon_v1.json`. |
| `data/lexicon_marks/` | The author's hand marks: *prodo* and *uendo* senses, and the classes of the collocation hits. |
| `data/superseded/`, `src/superseded/` | The first-pass A1 proposals and scripts, kept for the record. |
| `src/` | Robustness scripts (below). |
| `results/` | Robustness outputs; `results/SUMMARY.md` gives the findings. |
| `figures/` | Conference figures (unchanged). |

The notebooks' file paths were rewritten for this layout by static analysis; none was re-executed. Several notebooks write pickles and figures, so running them overwrites the conference outputs.

## Two pipelines

| | original (conference) | v2 (robustness) |
|---|---|---|
| Lemmas | saved output of the earlier LatinCy build (`data/original/corpus/processed_corpus.pkl`, `data/original/acts/processed_acts.pkl`) | LatinCy 3.9.8 with context-checked fixes (`data/v2/`) |
| Named entities | `data/original/unique_named_entities.pkl` | `data/v2/named_entities_final.json` |
| Ecerinis text | `data/original/corpus/latin_tragedies_corpus.json` | NeoLatDraCor TEI, pinned commit, 3 corrections (`data/sources/`) |
| Entry point in `src/` | `pipeline.load_docs`, `pipeline.remove_named_entities` | `v2_corpus.token_lists` |

**Known issue, left unchanged:** the original pipeline contains an empty lemma (the empty string).
- It is one lemma type carried by 64 tokens across all 11 plays (11 in Ecerinis, including the medieval spelling *vendico*).
- Because it occurs in every play, `no_above=0.5` removes it before modelling.
- It does count in that pipeline's token totals.

## Pipeline order

### Conference pipeline (notebooks; order follows what each one reads and writes)

Each notebook's paths are relative to its own folder, which is the working directory Jupyter uses.

| Step | Notebook or script | Reads | Writes |
|---|---|---|---|
| 1 | `Acts/get_acts.py` (run from `Acts/`) | DraCor API | `data/original/acts/latin_tragedies_acts.json` |
| 2 | `notebooks/NER_Mussato_Seneca.ipynb` | `data/original/corpus/latin_tragedies_corpus.json` | `data/original/unique_named_entities.pkl` |
| 3 | `Corpus/Cosine_Sim_Mussato_Seneca.ipynb` | `data/original/corpus/latin_tragedies_corpus.json` | `data/original/corpus/processed_tragedies_corpus.json`, `processed_corpus.pkl`, cosine heatmaps |
| 4 | `Acts/process_acts.ipynb`, then `Acts/cosine_sim_acts.ipynb` | `data/original/acts/latin_tragedies_acts.json` | `data/original/acts/processed_acts.pkl`, act cosine heatmap |
| 5 | `notebooks/play_lda/LDA_Coherence_Values.ipynb` | steps 2–3 | `models/play/filtered_*.pkl` (incl. `filtered_ideal_model.pkl`), `figures/corpus_figures/` |
| 6 | `notebooks/play_lda/corpus_gensim_relevance_sort.ipynb`, `pyLDAvis_corpus.ipynb` | step 5 | `Corpus/corpus_csv/`, pyLDAvis |
| 7 | `notebooks/act_lda/Acts_LDA_Coherence_Values.ipynb` | steps 2 and 4 | `models/act/acts_filtered_*.pkl`, `figures/act_figures/` |
| 8 | `notebooks/act_lda/acts_gensim_relevance_sort.ipynb`, `ideal_keywords.ipynb`, `extract_pyldavis_for_webpage.ipynb` | step 7 | `Acts/acts_csvs/`, pyLDAvis |

Other notebooks: `notebooks/POS_Ecerinis_NLP.ipynb`, `lemmas.ipynb`, `topic_lemma_search.ipynb` and `remove_integers_ecerinis.ipynb` (exploratory). The last reads `Ecerinis_spoken_text.txt`, which is not in the repo. `notebooks/play_lda/LDA_w-o_NE_TFIDF.ipynb` is an earlier TF-IDF experiment.

### Robustness pipeline (`src/`, run from the repo root with the `.venv` Python)

Each script writes a markdown report next to its outputs. A trailing number is the number of worker processes.

**A0: reproduction check**
- `src/check_reproduce.py`: retrains seed 42 and compares it with the saved model → `results/a0_reproduction/`.

**A1: v2 normalization**
- `src/sources.py`: Ecerinis from the pinned TEI; Seneca provenance check against DraCor (network) → `data/v2/corpus_v2.json`.
- `src/preprocess_v2.py`: line-start lowercasing and LatinCy 3.9.8 → `data/v2/plays_tokens.json`.
- `src/acts_v2.py`: acts cut from the play parse → `data/v2/acts_tokens.json`.
- `src/validate_v2.py`: checks lemmas against LiLa and Morpheus. Responses are cached in `data/lexicon_cache/`, so a rerun needs no network.
- `src/a1_v2_scan.py`: named-entity rule and spelling-variant candidates.
- `src/ne_recommendations.py`: the approved context decisions on names.
- `src/ne_final.py`: applies them → `data/v2/named_entities_final.json`.
- `src/lemma_triage.py`: the approved lemma triage.
- `src/v2_corpus.py`: final v2 token lists and report.

**A2: seed check**
- `src/a2_seeds.py 4`: 50 seeds × k = 1–10, both pipelines → `results/a2_seeds/`.
- `src/a2_seeds.py 4 relevance`: adds the top 20 by relevance for every run.
- `src/a2_analyze.py`: k selection, Topic 7 check, representative seeds, figures.
- `src/a2_acts.py 4`: act level, k = 24, 21 seeds.
- `src/a2_acts_pairs.py 4`: act pairings against a chance baseline, 101 seeds.

**A3: attribution and each play's own topic**
- `src/a3_attribution.py`: word-level attribution for Ecerinis, 5 models → `results/a3_attribution/`.
- `src/a3_own_topics.py 4`: each play's own topic across 50 seeds; Ecerinis's next-best topic → `results/a3_own_topics/`.

**A4: heatmaps**
- `src/a4_heatmaps.py`: conference heatmaps with empty topics labelled → `results/a4_heatmaps/`.

**Keyness and A5**
- `src/keyness.py`: Ecerinis vs Seneca keyness (G², log ratio) → `results/keyness/`.
- `src/a5_theme_rates.py`: theme word-family rates for the v1 four-family lexicon (`data/theme_lexicon_v1.json`) → `results/a5_theme_rates/`.
- `src/theme_lexicon.py`: loads lexicon v2 and applies its lexicon-only token rules (the LDA input is unchanged).
- `src/a5_lexicon_audit.py`, `src/a5_lexicon_revision.py`: audit of lexicon v2 (counts, zero lemmas, lemmatization checks; sense-check lists) → `results/a5_lexicon_v2/`.
- `src/a5_lexicon_v2_rates.py`: lexicon v2 rates per play and per act, act percentiles, figures → `results/a5_lexicon_v2/rates/`.
- `src/a5_collocations.py`: 'broken faith' collocations (*fides*/*fidus* near verbs of breaking), with hand classes → `results/a5_collocations/`.
- `src/verses.py`: edition verse numbers, speeches and acts for every v2 token (TEI `<l n>` for Ecerinis, `<milestone unit="line">` for Seneca). All passages are cited by these verse numbers.
- `src/a5_no_above.py 4`: `no_above` 0.5 / 0.8 / 1.0 / 1.0 with TF-IDF; 50-seed check at k = 7–9; Ecerinis's topic and attribution under each → `results/a5_no_above/`.

**Shared and superseded modules**
- Shared: `src/pipeline.py` (the notebook settings ported to functions, and the path constants), `src/normalize.py`, `src/spacy_docs.py`, `src/lexicon.py`.
- Superseded first pass, kept for the record:
  - scripts in `src/superseded/` (`a1_build_check.py`, `a1_scan.py`, `a1_proposals.py`, `latincy_compare.py`). `src/a1_v2_scan.py` still imports its rule tables from `superseded/a1_scan.py`.
  - data in `data/superseded/`;
  - reports in `results/a1_normalization/`.
- Reports written before the reorganization (`results/a0_*`, `results/a1_*`) cite the old paths (`Corpus/`, `Acts/`, `gensimvenv/corpus_pkl/`).

## Figure index

### Conference figures (`figures/`, unchanged)

| File | What it shows |
|---|---|
| `figures/corpus_figures/filtered_8topics_heatmap.png` | Topic weights per play, k = 8 (empty topics unlabelled; see A4 for the labelled version) |
| `figures/corpus_figures/filtered_topics_coherence_stability.png` | Coherence and adjacent-model overlap by k, play level |
| `figures/corpus_figures/new_cosine_similarity_heatmap.png` | Cosine similarity between plays, processed tokens |
| `figures/corpus_figures/old_unprocessed_cosine_heatmap.png` | Cosine similarity between plays, unprocessed text |
| `figures/act_figures/acts_filtered_topics_heatmap.png` | Topic weights per act, k = 24 |
| `figures/act_figures/acts_filtered_topics_coherence_stability.png` | Coherence and adjacent-model overlap by k, act level |
| `figures/act_figures/acts_median_elbow.png` | Act-level k selection (elbow) |
| `figures/act_figures/acts_cosine_similarity_heatmap.png` | Cosine similarity between acts |
| `figures/raw-v-filt_corpus/coherence_stability_comparison*.png` | Raw vs filtered corpus, coherence and overlap |

### Robustness figures (`results/`)

| File | What it shows |
|---|---|
| `results/a2_seeds/figures/fig_a2_tradeoff_curves.png` | Coherence, overlap and trade-off by k, mean ± 1 SD over 50 seeds, both pipelines |
| `results/a2_seeds/figures/fig_a2_wins.png` | Seeds in which each k has the highest trade-off |
| `results/a2_seeds/figures/fig_a2_coassignment_{original,v2}.png` | Share of seeds in which each pair of plays shares a dominant topic |
| `results/a2_seeds/figures/fig_a2_coassignment_neighbours_{original,v2}.png` | The same at neighbouring k (supplementary) |
| `results/a2_seeds/figures/fig_a2_acts_{original,v2}.png` | Ecerinis acts × Seneca acts, share of seeds sharing a dominant topic |
| `results/a3_attribution/figures/fig_a3_*.png` | Words placing Ecerinis in its topic vs the topic's top words (5 models) |
| `results/a4_heatmaps/fig_a4_play_topics_k8.png` | Conference play-level topic weights, empty topics labelled |
| `results/a4_heatmaps/fig_a4_act_topics_k24.png` | Conference act-level topic weights, empty topics labelled |
| `results/keyness/figures/fig_keyness_log_ratio.png` | Keyness log ratio, top 40 over-used and top 20 under-used lemmas in Ecerinis |
| `results/a5_theme_rates/figures/fig_a5_theme_rates_{v2,original}.png` | v1 four-family theme rates per play with bootstrap 95% intervals |
| `results/a5_lexicon_v2/rates/figures/fig_lexicon_v2_plays.png` | Lexicon v2: rates per play, one panel per family (author-chosen lexicon counts) |
| `results/a5_lexicon_v2/rates/figures/fig_lexicon_v2_act_percentiles.png` | Lexicon v2: families × 18 acts, coloured by percentile among all 56 acts |

## Data and licences

- **Code:** MIT (`LICENSE`).
- **Seneca:** the RomDraCor (Roman Drama Corpus) TEI files, licensed CC BY-SA 3.0 US according to the DraCor API (`https://dracor.org/api/v1/corpora/rom`). Derived token files in this repo carry the same licence, as do the copies of the Seneca TEI files in `data/sources/seneca_tei/` (used only for verse numbers and speech boundaries).
- **Ecerinis (v2):** NeoLatDraCor `tei/mussatus-ecerinis.xml`, commit `3d4653db`, CC0. The text is the MQDQ edition after L. Padrin (ed.), *Ecerinide* (Bologna, 1900). Provenance and corrections are in `results/a1_v2/sources_report.md`.
- **Lexical resources:** lemma checks use LiLa (`lila-erc.eu`) and Perseids Morpheus (`morph.perseids.org`). Their responses are cached in `data/lexicon_cache/`.
- **Not in git:** `context/` (unpublished chapter material).
