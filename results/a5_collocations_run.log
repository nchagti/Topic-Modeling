# 'Broken faith' collocations (author-chosen collocation measure)

**An author-chosen collocation measure, separate from the theme rates; not model output.** Node *fides* / *fidus*; collocates *rumpo*, *frango*, *uiolo*, *absum*, *neglego*, *nego*, *fallo*, *credo*, *iuro*, *sperno*, *laedo*; window ±5 tokens within the same speech, on the full v2 lemma sequence (before stopword and part-of-speech filtering; punctuation dropped; lemma fixes and spelling map applied). A hit is a node token with at least one collocate in its window. Verse numbers are the TEI editions' (`src/verses.py`).

Automatic hits are window matches; the hand classes (broken / pledge / other) are the author's reading of each hit (from `data/lexicon_marks/collocation_hits_marked.csv`). Counts with the passages, not rates.

## Per play

| play                       |   fides/fidus tokens |   automatic hits |   broken |   pledge |   other |   unclassified | passages                                                                          |
|:---------------------------|---------------------:|-----------------:|---------:|---------:|--------:|---------------:|:----------------------------------------------------------------------------------|
| Phoenissae                 |                    8 |                4 |        4 |        0 |       0 |              0 | v. 280 (broken); v. 293 (broken); v. 588 (broken); v. 649 (broken)                |
| Troades                    |                   12 |                1 |        0 |        1 |       0 |              0 | v. 611 (pledge)                                                                   |
| Phaedra                    |                    7 |                1 |        0 |        0 |       1 |              0 | v. 161 (other)                                                                    |
| Agamemnon                  |                   17 |                0 |        0 |        0 |       0 |              0 |                                                                                   |
| Hercules Furens            |                   10 |                0 |        0 |        0 |       0 |              0 |                                                                                   |
| Medea                      |                   10 |                1 |        0 |        1 |       0 |              0 | v. 1003 (pledge)                                                                  |
| Octavia                    |                   16 |                2 |        0 |        1 |       1 |              0 | v. 275 (other); v. 352 (pledge)                                                   |
| Oedipus                    |                   10 |                0 |        0 |        0 |       0 |              0 |                                                                                   |
| Thyestes                   |                   18 |                2 |        0 |        2 |       0 |              0 | v. 294 (pledge); v. 1099 (pledge)                                                 |
| Hercules Oetaeus           |                    9 |                0 |        0 |        0 |       0 |              0 |                                                                                   |
| Ecerinis                   |                    7 |                5 |        2 |        1 |       2 |              0 | v. 202 (other); v. 320 (broken); v. 360 (other); v. 472 (broken); v. 480 (pledge) |
| Seneca (10 plays combined) |                  117 |               11 |        4 |        5 |       2 |              0 |                                                                                   |

## Per act (acts with at least one hit)

| act   |   automatic hits |   broken |   pledge |   other |   unclassified | passages                         |
|:------|-----------------:|---------:|---------:|--------:|---------------:|:---------------------------------|
| Pho 1 |                2 |        2 |        0 |       0 |              0 | v. 280 (broken); v. 293 (broken) |
| Pho 4 |                2 |        2 |        0 |       0 |              0 | v. 588 (broken); v. 649 (broken) |
| Tro 3 |                1 |        0 |        1 |       0 |              0 | v. 611 (pledge)                  |
| Pha 1 |                1 |        0 |        0 |       1 |              0 | v. 161 (other)                   |
| Med 5 |                1 |        0 |        1 |       0 |              0 | v. 1003 (pledge)                 |
| Oct 1 |                2 |        0 |        1 |       1 |              0 | v. 275 (other); v. 352 (pledge)  |
| Thy 2 |                1 |        0 |        1 |       0 |              0 | v. 294 (pledge)                  |
| Thy 5 |                1 |        0 |        1 |       0 |              0 | v. 1099 (pledge)                 |
| Ece 2 |                1 |        0 |        0 |       1 |              0 | v. 202 (other)                   |
| Ece 3 |                2 |        1 |        0 |       1 |              0 | v. 320 (broken); v. 360 (other)  |
| Ece 4 |                2 |        1 |        1 |       0 |              0 | v. 472 (broken); v. 480 (pledge) |

## Check: Ecerinis passages

- v. 202 (negligens facti fidem): found (fidem v. 202 + negligens (neglego, -2, v. 202))
- v. 320 (Absit fides): found (fides v. 320 + Absit (absum, -1, v. 320))
- v. 472 (rupta fide): found (fide v. 472 + rupta (rumpo, -1, v. 472))
- v. 480 (fides ... iuratas (vv. 480-481)): found (fides v. 480 + iuratas (iuro, +5, v. 481))

## Every hit

| id | act, verse | speaker | node | collocates (form, lemma, offset, verse) | class | verses |
|---|---|---|---|---|---|---|
| 1 | Pho 1, v. 280 | Oedip. | fides | spernitur (sperno, -2, v. 280); negat (nego, +5, v. 281) | broken | [279] paternus animus, iacta iam sunt semina / [280] cladis futurae: spernitur pacti fides; / [281] hic occupato cedere imperio negat, / [282] ius ille et icti foederis testes deos |
| 2 | Pho 1, v. 293 | Antig. | fidem | laeso (laedo, -1, v. 293); negas (nego, +5, v. 294) | broken | [292] inhibere iuvenes, civibus pacem dare, / [293] patriae quietem, foederi laeso fidem. / [294] vitam tibi ipse si negas, multis negas. / [295] Illis parentis ullus aut aequi est amor, |
| 3 | Pho 4, v. 588 | Pol. | fidem | fefellissem (fallo, -1, v. 588) | broken | [587] opemque gentis hospes externae sequar? / [588] quid paterer aliud, si fefellissem fidem? / [589] si peierassem? fraudis alienae dabo |
| 4 | Pho 4, v. 649 | Ioc. | fide | rupta (rumpo, +1, v. 650) | broken | [648] Cadmique proles, sceptra Thebano fuit / [649] impune nulli gerere, nec quisquam fide / [650] rupta tenebit illa: iam numeres licet / [651] fratrem inter istos. |
| 5 | Tro 3, v. 611 | Vlix. | fidem | iurando (iuro, +3, v. 611) | pledge | [610] auspicia metuunt qui nihil maius timent. / [611] fidem alligavit iure iurando suam— / [612] si peierat, timere quid gravius potest? |
| 6 | Pha 1, v. 161 | Nvt. | fides | negata (nego, -4, v. 161) | other | [160] coitus nefandos utque contingat stupro / [161] negata magnis sceleribus semper fides: / [162] quid poena praesens, conscius mentis pavor |
| 7 | Med 5, v. 1003 | Ias. | fides | uiolauit (uiolo, -1, v. 1003) | pledge | [1002] Per numen omne perque communes fugas / [1003] torosque, quos non nostra violavit fides, / [1004] iam parce nato. si quod est crimen, meum est: |
| 8 | Oct 1, v. 275 | Chorus Romanorum | fidem | credita (credo, -5, v. 274) | other | [273] Quae fama modo venit ad aures? / [274] utinam falso credita perdat / [275] frustra totiens iactata fidem, / [276] nec nova coniunx nostri thalamos |
| 9 | Oct 1, v. 352 | Chorus Romanorum | fides | spreta (sperno, -4, v. 352) | pledge | [351] mansit tacitis in pectoribus / [352] spreta tristi iam morte fides: / [353] multi dominae ferre auxilium |
| 10 | Thy 2, v. 294 | Sat. | fidem | credet (credo, +5, v. 295) | pledge | [293] hac spe, quod esse maximum retur malum, / [294] fratrem videbit. / Quis fidem pacis dabit? / [295] cui tanta credet? / Credula est spes improba. / [296] gnatis tamen mandata quae patruo ferant |
| 11 | Thy 5, v. 1099 | Atr. | fidem | credo (credo, -3, v. 1099) | pledge | [1098] nisi sic doleres. liberos nasci mihi / [1099] nunc credo, castis nunc fidem reddi toris. / [1100] Quid liberi meruere? / Quod fuerant tui. |
| 12 | Ece 2, v. 202 | Nuntius | fidem | negligens (neglego, -2, v. 202) | other | [201] vulgus, et ad omne facinus in clades ruens, / [202] voces secutum et negligens facti fidem! / [203] Procede: redeas unde coepisti prius. |
| 13 | Ece 3, v. 320 | Ecerinus | fides | Absit (absum, -1, v. 320) | broken | [319] dolosa species haec ad interitum trahet / [320] hinc inde multos transfugas. Absit fides / [321] pietasque nostris actibus semper procul. |
| 14 | Ece 3, v. 360 | Fr. Lucas | Fides | crede (credo, +2, v. 361) | other | [359] Hos esse tales edocent primo insitae / [360] natura ab ipsa Caritas Spes et Fides. / [361] Has, crede, quisque pectori innatas habet, / [362] traducat error devius quemquam licet. |
| 15 | Ece 4, v. 472 | Nuntius | fide | rupta (rumpo, -1, v. 472) | broken | [471] Iam iam occupata Brixia, Ecerinus ferox, / [472] favore Cremonensium, rupta fide / [473] exclusit illos: Pellavicino quoque |
| 16 | Ece 4, v. 480 | Nuntius | fides | iuratas (iuro, +5, v. 481) | pledge | [479] sensit Cremonae Mantuae Ferrariae / [480] unaque Bosi et Pellavicini fides / [481] in eius omnem sponte iuratas necem. / [482] Collata ad Aduae signa fixerunt vadum, |
