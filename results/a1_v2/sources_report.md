# v2 source texts

## Ecerinis

- NeoLatDraCor `tei/mussatus-ecerinis.xml`, commit `3d4653db801eb2586c92cb918f6774bd0b079850` (CC0), copy at `data/sources/mussatus-ecerinis.xml` (sha256 `60a9beb6d85c48d5…`).
- Text: MQDQ edition, after L. Padrin (ed.), *Ecerinide* (Bologna: Zanichelli, 1900), pp. 23–66.
- 654 verse lines in 5 acts, including 5 lines encoded inside `<stage>` ("Sic fatus ima parte secessit domus …").
- Corrections applied (`data/sources/ecerinis_patches.json`):
  - line 369: 'dtabiles perennis' -> 'stabiles perennis' (typo (Padrin 1900: Stabiles))
  - line 371: 'dub lege certa' -> 'sub lege certa' (typo (Padrin 1900: Sub))
  - line 26: 'Resperge faciem, Nuntius sincopim' -> 'Resperge faciem, sincopim' (speaker name inside a spoken line)
- Compared with the text used so far (`Corpus/latin_tragedies_corpus.json`): 653 of 654 lines match ignoring case and punctuation; the old text capitalizes every line and reads 'Quadnam' for Quodnam.

## Seneca (text unchanged; provenance check)

| play | lines used | matching DraCor's current TEI | matching the local TEI copy (file) |
|---|---|---|---|
| Phoenissae | 672 | 672 / 672 | 672 / 672 (`rom000015-seneca-phoenissae.tei.xml`) |
| Troades | 1214 | 1214 / 1214 | 1212 / 1214 (`rom000016-seneca-troades.tei.xml`) |
| Phaedra | 1308 | 1308 / 1308 | 1308 / 1308 (`rom000031-seneca-phaedra.tei.xml`) |
| Agamemnon | 1060 | 1060 / 1060 | 1060 / 1060 (`rom000029-seneca-agamemnon.tei.xml`) |
| Hercules Furens | 1393 | 1392 / 1393 | 1392 / 1393 (`seneca-hercules-furens.xml`) |
| Medea | 1068 | 1067 / 1068 | 1068 / 1068 (`rom000005-seneca-medea.tei.xml`) |
| Octavia | 1020 | 1020 / 1020 | 1020 / 1020 (`rom000030-seneca-octavia.tei.xml`) |
| Oedipus | 1092 | 1092 / 1092 | 1092 / 1092 (`rom000002-seneca-oedipus.tei.xml`) |
| Thyestes | 1166 | 1166 / 1166 | 1166 / 1166 (`seneca-thyestes.xml`) |
| Hercules Oetaeus | 2038 | 2038 / 2038 | 2038 / 2038 (`rom000001-seneca-hercules-oetaeus.tei.xml`) |

DraCor's live API is not versioned; the comparison records the state on the date this report was generated.
