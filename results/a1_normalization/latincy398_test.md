# LatinCy 3.9.8 vs the saved lemmas (earlier build)

Tokens aligned by normalized surface text (lowercase, v->u, j->i). Aligned tokens: 82,544 of 82,765 old tokens.

## 1. Known lemma errors

Totals: old build correct on 32 of 189 tokens; 3.9.8 correct on 149.

| case                                      |   tokens |   old correct |   3.9.8 correct | old lemmas                                          | 3.9.8 lemmas                                  | basis                              |
|:------------------------------------------|---------:|--------------:|----------------:|:----------------------------------------------------|:----------------------------------------------|:-----------------------------------|
| vindicem/vindices = vindex                |       10 |             0 |               7 | uindico 10                                          | uindex 7, uindico 3                           | context checked                    |
| ponti = pontus                            |        9 |             2 |               9 | pons 7, pontus 2                                    | pontus 9                                      | context checked (this run)         |
| manes = Manes                             |       47 |             4 |              28 | maneo 43, manes 4                                   | manes 28, maneo 12, mane 5, manis 1, macnes 1 | context checked (sample, this run) |
| pavit = pasco                             |        5 |             0 |               5 | po 5                                                | pasco 5                                       | context checked                    |
| tenere = teneo                            |        5 |             0 |               5 | tenere 5                                            | teneo 5                                       | context checked                    |
| liqueris = linquo                         |        2 |             0 |               2 | liquo 2                                             | linquo 2                                      | context checked                    |
| vitas = vito (Troades)                    |        1 |             0 |               1 | uitas 1                                             | uito 1                                        | context checked                    |
| vitas = vita (Ecerinis)                   |        1 |             0 |               0 | uitas 1                                             | uito 1                                        | context checked                    |
| solo/soli = solum (old NOUN)              |       20 |            15 |              14 | solum 15, solus 5                                   | solum 14, solus 5, sol 1                      | context checked                    |
| sate = sero (Ecerinis)                    |        1 |             0 |               1 | so 1                                                | sero 1                                        | context checked                    |
| dire = dirus (Ecerinis)                   |        1 |             0 |               1 | deo 1                                               | dirus 1                                       | context checked                    |
| dest/desset = desum                       |        5 |             0 |               5 | dsum 5                                              | desum 5                                       | form unambiguous                   |
| eversa/eversis/eversi = everto            |       11 |             2 |              11 | euergeo 4, euerdo 3, (empty) 2, euerto 1, euersus 1 | euerto 11                                     | form unambiguous                   |
| invisum/inviso = invisus/invideo/inviso   |        8 |             1 |               8 | inuido 7, inuisus 1                                 | inuisus 8                                     | Morpheus candidates                |
| verbera = verber                          |       12 |             0 |              12 | uerberum 6, uerbera 4, uerbus 2                     | uerber 12                                     | form unambiguous                   |
| iuvenum/iuveni = iuvenis                  |        9 |             0 |               9 | iuue 4, iuuenes 3, iuuen 1, iuuenus 1               | iuuenis 9                                     | form unambiguous                   |
| lare = lar                                |        5 |             1 |               0 | lo 4, lar 1                                         | larus 5                                       | form unambiguous                   |
| puri = purus                              |        2 |             0 |               2 | pus 2                                               | purus 2                                       | form unambiguous                   |
| rati = reor                               |        5 |             1 |               1 | ror 2, ratis 1, ro 1, reor 1                        | ratis 3, rano 1, reor 1                       | form unambiguous                   |
| vendicemus/vendicabo = vindico (Ecerinis) |        2 |             0 |               0 | (empty) 2                                           | uendico 2                                     | Morpheus                           |
| brevior = brevis                          |        4 |             0 |               4 | breuus 4                                            | breuis 4                                      | form unambiguous                   |
| leviore/leviora = levis                   |        5 |             0 |               5 | leuior 5                                            | leuis 5                                       | form unambiguous                   |
| profare/speculare/gradere = deponents     |        7 |             0 |               7 | profo 3, speculo 2, grado 2                         | profor 3, speculor 2, gradior 2               | form unambiguous                   |
| vasti = vastus                            |       10 |             4 |              10 | (empty) 4, uastus 4, uastum 1, uo 1                 | uastus 10                                     | form unambiguous                   |
| invadam = invado                          |        2 |             2 |               2 | inuado 2                                            | inuado 2                                      | form unambiguous                   |

Contexts for 'ponti = pontus' (to check the expected lemma):

- Phaedra: ...vacat immunis, qua curvati litora ponti Sunion urget si quem tangit gloria... [old pons, new pontus]
- Phaedra: ...murmure saevo. amat insani belua ponti Lucaeque boves: vindicat omnes... [old pons, new pontus]
- Phaedra: ...fuit.] qualis relictis frigidi Ponti plagis egit catervas Atticum pulsans solum... [old pontus, new pontus]
- Phaedra: ...nam toto obvius incurrit ore corniger ponti horridus. tum vero pavida sonipedes... [old pons, new pontus]
- Phaedra: ...malis, nunc adeste, saeva ponti monstra, nunc vastum mare,... [old pons, new pontus]
- Hercules Furens: ...alti tellusque ferax et vaga ponti mobilis unda, tuque ante... [old pons, new pontus]
- Medea: ...rediturus auri, exitu diro temerata ponti iura piavit. exigit poenas mare... [old pons, new pontus]
- Oedipus: ..., velut ignotum videre nefas. Ponti regna tenet nitidi matertera Bacchi Nereidum... [old pontus, new pontus]
- Oedipus: ...habet in fluctus magni puer advena ponti, cognatus Bacchi, numen non... [old pons, new pontus]

Contexts for 'manes = Manes' (to check the expected lemma):

- Phoenissae: ...umbras Ditis aeternas? quid hic manes meos detineo? quid terram gravo... [old maneo, new maneo]
- Troades: ...conditum regno tegit, tuosque manes quo stetit stante Ilium, et... [old maneo, new manes]
- Troades: ...felix Priamus dicite cunctae: liber manes vadit ad imos, nec feret... [old maneo, new maneo]
- Troades: ..., iubet. Nullumne Achillis praemium manes ferent? 1 Ferent, et... [old maneo, new maneo]
- Troades: ...deos, deosque veros coniugis manes mei: non aliud, Hector... [old maneo, new manes]
- Troades: ...tamen perfer querelae verba: 'si manes habent curas priores nec perit flammis... [old maneo, new manes]
- Troades: ...vestem: tumulus hanc tetigit meus manesque cari. si quid hic... [old maneo, new mane]
- Troades: ...superos caede funesta deos, maculate manes— quid precer vobis? precor... [old maneo, new maneo]
- Phaedra: ...profugi noctis aeternae plagam vastoque manes carcere umbrantem polum, et vix... [old maneo, new maneo]
- Phaedra: ...ultra lucidum Hippolytum diem adeatque manes iuvenis iratos patri, fer abominandam... [old maneo, new mane]
- Phaedra: ...in verum scelus. sidera et manes et undas scelere complevi meo:... [old maneo, new manes]
- Phaedra: ...remitte munus; ereptos mihi restitue manes, impius frustra invoco mortem relictam... [old maneo, new maneo]

- Old empty lemmas (content POS) under 3.9.8: {'fixed (lemma differs from surface)': 44, 'surface form copied': 20}

## 2. Entity tagging

### Ordinary words tagged as entities (tokens tagged / occurrences)

| lemma | occurrences | old build | 3.9.8 |
|---|---|---|---|
| scelus | 241 | 4 | 5 |
| magnus | 216 | 2 | 5 |
| peto | 205 | 2 | 1 |
| mater | 181 | 3 | 3 |
| animus | 177 | 5 | 4 |
| mors | 162 | 10 | 12 |
| caelum | 153 | 3 | 2 |
| poena | 108 | 1 | 2 |
| dolor | 108 | 1 | 4 |
| ira | 99 | 1 | 2 |
| furor | 84 | 1 | 0 |
| urbs | 66 | 1 | 0 |
| caedes | 68 | 2 | 3 |
| pars | 107 | 3 | 1 |
| ferrum | 107 | 1 | 5 |
| flamma | 106 | 1 | 0 |
| metus | 101 | 2 | 2 |

- The 285 listed lemmas tagged < 50% of the time: lemmas tagged at least once old 285, 3.9.8 217; entity tokens old 437, 3.9.8 420 (of 13200).
- The 987 listed lemmas tagged >= 50% (mostly real names): entity tokens old 3002, 3.9.8 2665 (of 3184).
- Under the NER notebook's rule (one tag anywhere puts a lemma on the list), a 3.9.8-built list would still include 217 of the 285 ordinary-word lemmas.

### Ecerinis: tokens tagged as entities or PROPN by either build

| surface | old entity | 3.9.8 entity | old POS | 3.9.8 POS | 3.9.8 lemma | n |
|---|---|---|---|---|---|---|
| Padua | LOC | LOC | PROPN | PROPN | padua | 5 |
| Verona | LOC | LOC | PROPN | PROPN | uerona | 4 |
| Albricus | PERSON | PERSON | PROPN | PROPN | albricus | 3 |
| Albrici | PERSON | PERSON | PROPN | PROPN | albricus | 2 |
| Amissa | PERSON | PERSON | VERB | VERB | amitto | 2 |
| Animos | NORP | PERSON | NOUN | ADJ | animus | 2 |
| Commilitones | NORP | PERSON | NOUN | PROPN | commilito | 2 |
| Ecerinus | PERSON | - | PROPN | PROPN | ecerinus | 2 |
| Ecerinus | PERSON | PERSON | PROPN | PROPN | ecerinus | 2 |
| Fortuna | - | PERSON | NOUN | PROPN | fortuna | 2 |
| Hem | - | PERSON | INTJ | DET | hem | 2 |
| Ille | - | PERSON | DET | DET | ille | 2 |
| Marchio | PERSON | PERSON | PROPN | PROPN | marchium | 2 |
| Natura | - | - | PROPN | PROPN | natura | 2 |
| Parens | - | - | PROPN | PROPN | parens | 2 |
| Quos | NORP | - | PRON | PRON | qui | 2 |
| Abductus | PERSON | PERSON | VERB | PROPN | abductus | 1 |
| Abel | PERSON | PERSON | PROPN | PROPN | abel | 1 |
| Abinde | PERSON | PERSON | ADV | ADV | abinde | 1 |
| Abscede | PERSON | PERSON | VERB | PROPN | abscede | 1 |
| Abscedite | PERSON | - | VERB | PROPN | absceditus | 1 |
| Absorbet | PERSON | PERSON | PROPN | PROPN | absorbet | 1 |
| Abstracta | PERSON | PERSON | VERB | PROPN | abstracta | 1 |
| Abundet | PERSON | - | VERB | VERB | abundeo | 1 |
| Accede | - | PERSON | VERB | VERB | accede | 1 |
| Acer | PERSON | - | ADJ | PROPN | acer | 1 |
| Adest | - | - | VERB | PROPN | adest | 1 |
| Adiere | PERSON | PERSON | VERB | PROPN | adiere | 1 |
| Adua | - | LOC | PROPN | PROPN | abdua | 1 |
| Aduae | - | PERSON | ADJ | PROPN | abdua | 1 |
| Aduam | - | LOC | ADJ | PROPN | abdua | 1 |
| Adulter | PERSON | PERSON | PROPN | PROPN | adulter | 1 |
| Adversa | - | PERSON | ADJ | ADJ | aduersa | 1 |
| Adversus | PERSON | - | ADP | ADP | aduersus | 1 |
| Aegyptius | - | NORP | PROPN | ADJ | aegyptius | 1 |
| Aetas | NORP | LOC | NOUN | NOUN | aetas | 1 |
| Aethnaeus | PERSON | PERSON | PROPN | ADJ | aethnaeus | 1 |
| Agens | - | PERSON | VERB | VERB | agens | 1 |
| Agnovere | PERSON | PERSON | VERB | PROPN | agnouere | 1 |
| Ah | - | - | INTJ | PROPN | ahus | 1 |
| Albrice | LOC | PERSON | PROPN | PROPN | albricus | 1 |
| Albrice | PERSON | PERSON | PROPN | PROPN | albricus | 1 |
| Alecto | PERSON | PERSON | ADJ | PROPN | alectus | 1 |
| Alius | - | PERSON | DET | DET | alius | 1 |
| Altos | NORP | NORP | ADJ | DET | altos | 1 |
| Altum | NORP | - | PROPN | ADJ | altus | 1 |
| Anguis | PERSON | PERSON | PROPN | PROPN | anguis | 1 |
| Anhelitus | PERSON | PERSON | PROPN | PROPN | anhelitus | 1 |
| Annuat | - | PERSON | VERB | PROPN | annuat | 1 |
| Annue | PERSON | PERSON | VERB | PROPN | annue | 1 |
| Annue | PERSON | PERSON | VERB | PROPN | annuus | 1 |
| Ansedisius | LOC | - | PROPN | PROPN | ansedisius | 1 |
| Antiqua | LOC | LOC | ADJ | ADJ | antiqua | 1 |
| Arcthici | LOC | PERSON | PROPN | PROPN | arcthicus | 1 |
| Arcthoo | PERSON | PERSON | PROPN | PROPN | arcthous | 1 |
| Ardens | PERSON | PERSON | PROPN | VERB | ardeo | 1 |
| Arx | - | PERSON | NOUN | NOUN | arx | 1 |
| Asperans | - | PERSON | VERB | PROPN | asperans | 1 |
| Assuetam | - | LOC | ADJ | PROPN | assuetam | 1 |
| Atram | PERSON | PERSON | NOUN | ADJ | atrus | 1 |
| Atrox | NORP | PERSON | ADJ | ADJ | atrox | 1 |
| Attendis | NORP | PERSON | VERB | VERB | atto | 1 |
| Audi | - | PERSON | VERB | PROPN | audi | 1 |
| Audire | NORP | LOC | VERB | PROPN | audio | 1 |
| Audite | - | - | VERB | PROPN | audite | 1 |
| Axan | PERSON | PERSON | PROPN | PROPN | axan | 1 |
| Azo | - | PERSON | PROPN | PROPN | azo | 1 |
| Azo | LOC | PERSON | PROPN | PROPN | azo | 1 |
| Baxan | PERSON | PERSON | PROPN | PROPN | baxan | 1 |
| Belli | - | - | PROPN | PROPN | bellus | 1 |
| Bistonis | PERSON | PERSON | NOUN | PROPN | biston | 1 |
| Bonifacius | PERSON | PERSON | PROPN | PROPN | bonifacius | 1 |
| Bosi | PERSON | PERSON | PROPN | PROPN | bosus | 1 |
| Braida | LOC | LOC | ADJ | PROPN | brais | 1 |
| Brixia | LOC | LOC | PROPN | PROPN | brixia | 1 |
| Bullit | - | PERSON | VERB | VERB | bullio | 1 |
| Caecis | NORP | PERSON | ADJ | PROPN | caecus | 1 |
| Caedis | - | PERSON | PROPN | PROPN | caedes | 1 |
| Caedit | - | PERSON | VERB | VERB | caedo | 1 |
| Caelo | PERSON | LOC | PROPN | PROPN | caelum | 1 |
| Caelo | LOC | LOC | PROPN | NOUN | caelum | 1 |
| Caelum | LOC | - | NOUN | NOUN | caelum | 1 |
| Caesarum | NORP | NORP | PROPN | PROPN | caesar | 1 |
| Campestre | LOC | LOC | ADJ | ADJ | campestrus | 1 |
| Capiamus | LOC | - | VERB | VERB | capio | 1 |
| Capta | LOC | - | VERB | VERB | capio | 1 |
| Captivos | NORP | NORP | NOUN | PROPN | captiuus | 1 |
| Carceres | NORP | - | NOUN | PROPN | carceres | 1 |
| Caritas | - | - | NOUN | PROPN | caritas | 1 |
| Carpit | - | PERSON | VERB | VERB | carpit | 1 |
| Caxan | PERSON | PERSON | ADJ | PROPN | caxan | 1 |
| Caxani | PERSON | PERSON | PROPN | ADJ | caxani | 1 |
| Censet | - | PERSON | VERB | VERB | censet | 1 |
| Cernis | NORP | - | VERB | NOUN | cernis | 1 |
| Certas | NORP | - | ADJ | PROPN | certas | 1 |
| Cervice | LOC | PERSON | NOUN | PROPN | ceruix | 1 |
| Chaos | NORP | - | PROPN | NOUN | chaos | 1 |
| Christe | PERSON | PERSON | VERB | PROPN | christus | 1 |
| Christum | PERSON | PERSON | PROPN | PROPN | christus | 1 |
| Circum | LOC | PERSON | ADP | PROPN | circus | 1 |
| Circumlatrantes | NORP | NORP | VERB | PROPN | circumlatrantes | 1 |
| Cives | NORP | - | NOUN | NOUN | ciuis | 1 |
| Clamor | PERSON | LOC | NOUN | NOUN | clamor | 1 |
| Coepti | LOC | - | NOUN | NOUN | coepi | 1 |
| Colla | LOC | PERSON | NOUN | NOUN | collum | 1 |
| Collata | LOC | - | VERB | VERB | confero | 1 |
| Comes | PERSON | PERSON | PROPN | PROPN | comes | 1 |
| Comes | PERSON | PERSON | NOUN | PROPN | comes | 1 |
| Consors | PERSON | PERSON | ADJ | PROPN | consors | 1 |
| Consorte | PERSON | PERSON | PROPN | ADJ | consorte | 1 |
| Contexe | PERSON | PERSON | VERB | PROPN | contexus | 1 |
| Convertam | - | PERSON | VERB | PROPN | conuerta | 1 |
| Converte | - | PERSON | VERB | PROPN | conuertus | 1 |
| Corpora | PERSON | - | NOUN | NOUN | corpus | 1 |
| Credendus | PERSON | PERSON | VERB | PROPN | credendus | 1 |
| Cremonae | PERSON | PERSON | PROPN | PROPN | cremona | 1 |
| Cremonensium | NORP | NORP | PROPN | PROPN | cremonenses | 1 |
| Crepuisset | PERSON | PERSON | VERB | PROPN | crepuisset | 1 |
| Crimen | NORP | PERSON | NOUN | NOUN | crimen | 1 |
| Cruce | LOC | PERSON | NOUN | PROPN | crux | 1 |
| Crucis | PERSON | LOC | PROPN | PROPN | crux | 1 |
| Cruentus | PERSON | PERSON | PROPN | PROPN | cruentus | 1 |
| Cunctantis | - | LOC | PROPN | PROPN | cunctans | 1 |
| Curas | PERSON | PERSON | PROPN | NOUN | cura | 1 |
| Currit | - | LOC | VERB | VERB | curro | 1 |
| Deferre | PERSON | - | VERB | VERB | deferre | 1 |
| Delicta | NORP | - | VERB | VERB | delicta | 1 |
| Delicta | - | - | NOUN | PROPN | delicta | 1 |
| Deus | - | - | PROPN | PROPN | deus | 1 |
| Deus | - | - | PROPN | NOUN | deus | 1 |
| Devota | PERSON | - | ADJ | ADJ | deuotus | 1 |
| Diis | NORP | - | NOUN | NOUN | dium | 1 |
| Diluvia | LOC | - | NOUN | ADJ | diluuium | 1 |
| Diros | NORP | NORP | ADJ | DET | dirus | 1 |
| Dirum | - | - | NOUN | PROPN | dirus | 1 |
| Districtualium | - | PERSON | NOUN | PROPN | districtualium | 1 |
| Ditis | NORP | PERSON | PROPN | NOUN | dis | 1 |
| Dolis | NORP | - | PROPN | PROPN | dolis | 1 |
| Dolosa | - | LOC | ADJ | ADJ | dolosus | 1 |
| Dominum | - | - | NOUN | PROPN | dominus | 1 |
| Dormire | PERSON | PERSON | VERB | PROPN | dormire | 1 |
| Ducto | PERSON | PERSON | VERB | VERB | ducto | 1 |
| Durat | - | PERSON | VERB | VERB | duro | 1 |
| Ecerine | - | - | ADV | PROPN | ecerinus | 1 |
| Ecerine | PERSON | - | PROPN | PROPN | ecerinus | 1 |
| Ecerine | LOC | - | VERB | PROPN | ecerinus | 1 |
| Ecerini | PERSON | LOC | PROPN | PROPN | ecerinum | 1 |
| Ecerinum | - | PERSON | ADJ | ADJ | ecerinum | 1 |
| Ecerinus | PERSON | - | ADJ | ADJ | ecerinus | 1 |
| Ecerinus | PERSON | - | PROPN | ADJ | ecerinus | 1 |
| Ecerinus | PERSON | PERSON | PROPN | ADJ | ecerinus | 1 |
| Ecerinus | PERSON | PERSON | ADJ | ADJ | ecerinus | 1 |
| Ecerinus | PERSON | - | ADJ | PROPN | ecerinus | 1 |
| Ecerinus | - | - | PROPN | PROPN | ecerinus | 1 |
| Edissero | PERSON | PERSON | VERB | PROPN | edissero | 1 |
| Effare | - | PERSON | VERB | PROPN | effarus | 1 |
| Encheladus | PERSON | PERSON | PROPN | PROPN | encheladus | 1 |
| Erige | - | PERSON | VERB | PROPN | erigus | 1 |
| Erimus | PERSON | PERSON | VERB | PROPN | erimus | 1 |
| Errore | - | PERSON | NOUN | PROPN | error | 1 |
| Errore | - | - | NOUN | PROPN | errore | 1 |
| Estensis | PERSON | PERSON | PROPN | PROPN | estensis | 1 |
| Evelle | - | PERSON | VERB | NOUN | euello | 1 |
| Eventus | PERSON | PERSON | NOUN | PROPN | euentus | 1 |
| Eversa | - | PERSON | VERB | VERB | euerto | 1 |
| Exangue | PERSON | - | PROPN | PROPN | exangue | 1 |
| Exarsit | - | PERSON | VERB | VERB | exardeo | 1 |
| Excelse | - | - | ADJ | PROPN | excelse | 1 |
| Excelsus | - | PERSON | PROPN | PROPN | excelsus | 1 |
| Exclusit | - | PERSON | VERB | VERB | exclusit | 1 |
| Exertus | - | PERSON | VERB | PROPN | exertus | 1 |
| Facile | PERSON | PERSON | ADV | PROPN | facilus | 1 |
| Falsum | - | PERSON | ADJ | ADJ | falsus | 1 |
| Fatale | - | PERSON | ADJ | PROPN | fatalus | 1 |
| Favilla | PERSON | - | NOUN | NOUN | fauilla | 1 |
| Favore | PERSON | PERSON | NOUN | NOUN | fauor | 1 |
| Favore | PERSON | PERSON | PROPN | PROPN | fauorus | 1 |
| Felicis | PERSON | PERSON | PROPN | PROPN | felix | 1 |
| Feltro | PERSON | PERSON | ADJ | ADJ | feltrus | 1 |
| Feminas | NORP | - | NOUN | ADJ | femina | 1 |
| Ferrariae | PERSON | - | PROPN | PROPN | ferraria | 1 |
| Ferrariensium | - | NORP | PROPN | PROPN | ferrarienses | 1 |
| Ferro | - | - | NOUN | PROPN | ferrum | 1 |
| Ferro | - | LOC | NOUN | PROPN | ferro | 1 |
| Ferrum | NORP | - | NOUN | NOUN | ferrum | 1 |
| Fides | - | - | NOUN | PROPN | fides | 1 |
| Fides | - | - | PROPN | PROPN | fides | 1 |
| Fidite | - | - | VERB | PROPN | fidite | 1 |
| Finem | - | PERSON | NOUN | NOUN | fin | 1 |
| Flagrat | - | LOC | VERB | PROPN | flagrat | 1 |
| Flammam | PERSON | - | PROPN | PROPN | flamma | 1 |
| Flatu | PERSON | PERSON | NOUN | NOUN | flatus | 1 |
| Foeda | LOC | - | ADJ | ADJ | foedus | 1 |
| Fortuna | PERSON | PERSON | PROPN | PROPN | fortuna | 1 |
| Forum | - | - | NOUN | PROPN | forum | 1 |
| Frater | - | PERSON | NOUN | PROPN | frater | 1 |
| Fratris | PERSON | - | NOUN | NOUN | frater | 1 |
| Frigore | PERSON | PERSON | NOUN | ADJ | frigorus | 1 |
| Fulgur | PERSON | PERSON | PROPN | PROPN | fulgur | 1 |
| Fuso | PERSON | PERSON | VERB | NOUN | fuso | 1 |
| Gallia | LOC | LOC | PROPN | PROPN | gallia | 1 |
| Gallicis | NORP | - | ADJ | ADJ | gallicus | 1 |
| Gardae | PERSON | - | PROPN | PROPN | gardas | 1 |
| Genetricis | PERSON | - | PROPN | PROPN | genetrix | 1 |
| Gens | - | PERSON | NOUN | PROPN | gens | 1 |
| Genui | PERSON | PERSON | PROPN | PROPN | genuus | 1 |
| Gladium | - | - | NOUN | PROPN | gladius | 1 |
| Gladium | - | - | PROPN | PROPN | gladius | 1 |
| Gnati | PERSON | PERSON | PROPN | PROPN | gnatus | 1 |
| Gomorrae | LOC | LOC | PROPN | PROPN | gomorra | 1 |
| Herinis | PERSON | PERSON | ADJ | ADJ | herini | 1 |
| Heu | - | PERSON | INTJ | PART | heu | 1 |
| Hos | NORP | - | DET | DET | hic | 1 |
| Huc | - | LOC | ADV | ADV | huc | 1 |
| Illaesa | LOC | PERSON | ADJ | PROPN | illaesa | 1 |
| Imago | PERSON | - | PROPN | PROPN | imago | 1 |
| Imbre | PERSON | - | PROPN | PROPN | imbre | 1 |
| Incerta | - | PERSON | ADJ | ADJ | incerta | 1 |
| Inclite | - | - | VERB | PROPN | inclitus | 1 |
| Infausta | PERSON | PERSON | ADJ | ADJ | infausta | 1 |
| Inferus | - | - | ADJ | PROPN | inferus | 1 |
| Infesta | LOC | PERSON | PROPN | PROPN | infesta | 1 |
| Infestam | - | - | PROPN | PROPN | infesta | 1 |
| Iniecit | - | PERSON | VERB | VERB | inicio | 1 |
| Inspectans | - | PERSON | VERB | PROPN | inspectans | 1 |
| Intro | - | PERSON | ADV | ADJ | inter | 1 |
| Invade | - | PERSON | VERB | PROPN | inuadus | 1 |
| Invocat | - | PERSON | VERB | VERB | inuocat | 1 |
| Iovi | PERSON | PERSON | PROPN | PROPN | iuppiter | 1 |
| Iovis | PERSON | PERSON | PROPN | PROPN | iuppiter | 1 |
| Italia | LOC | LOC | PROPN | PROPN | italia | 1 |
| Iudex | - | - | PROPN | NOUN | iudex | 1 |
| Iulii | - | - | PROPN | PROPN | iulius | 1 |
| Iustitia | - | - | PROPN | PROPN | iustitia | 1 |
| Iustus | PERSON | PERSON | ADJ | PROPN | iustus | 1 |
| Iuvenes | NORP | - | ADJ | ADJ | iuuenis | 1 |
| Lacrimae | PERSON | PERSON | NOUN | NOUN | lacrimae | 1 |
| Latere | PERSON | PERSON | VERB | VERB | lateo | 1 |
| Leges | NORP | - | NOUN | NOUN | lex | 1 |
| Lombarda | PERSON | LOC | ADJ | ADJ | lombardus | 1 |
| Lombardia | LOC | LOC | PROPN | PROPN | lombardia | 1 |
| Lucifer | PERSON | PERSON | PROPN | PROPN | lucifer | 1 |
| Luciferum | PERSON | PERSON | PROPN | PROPN | lucifer | 1 |
| Luget | PERSON | PERSON | VERB | PROPN | luget | 1 |
| Lumine | PERSON | PERSON | NOUN | NOUN | lumen | 1 |
| Lustravit | - | PERSON | VERB | VERB | lustrauit | 1 |
| Macedonis | LOC | PERSON | PROPN | ADJ | macedones | 1 |
| Magnanime | PERSON | PERSON | ADJ | PROPN | magnanimus | 1 |
| Mantuae | - | LOC | ADJ | PROPN | mantua | 1 |
| Manum | - | PERSON | NOUN | ADJ | manus | 1 |
| Marchia | PERSON | - | PROPN | PROPN | marchia | 1 |
| Marchia | LOC | LOC | PROPN | PROPN | marchia | 1 |
| Marchiae | LOC | - | PROPN | PROPN | marchia | 1 |
| Marchiae | LOC | LOC | PROPN | PROPN | marchius | 1 |
| Marchiae | PERSON | LOC | PROPN | PROPN | marchiae | 1 |
| Marchiae | PERSON | PERSON | PROPN | PROPN | marchiae | 1 |
| Marte | PERSON | PERSON | PROPN | PROPN | mars | 1 |
| Marti | PERSON | PERSON | PROPN | PROPN | mars | 1 |
| Martinus | PERSON | PERSON | PROPN | PROPN | martinus | 1 |
| Martius | PERSON | - | PROPN | ADJ | martius | 1 |
| Matris | PERSON | PERSON | NOUN | PROPN | mater | 1 |
| Mediolanum | LOC | LOC | PROPN | PROPN | mediolanum | 1 |
| Megaera | LOC | PERSON | PROPN | PROPN | megaera | 1 |
| Meos | NORP | NORP | DET | ADJ | meus | 1 |
| Meritum | - | PERSON | ADJ | PROPN | meritus | 1 |
| Meus | - | PERSON | DET | ADJ | meus | 1 |
| Mira | - | PERSON | ADJ | ADJ | mirus | 1 |
| Mitis | - | - | ADJ | PROPN | mitis | 1 |
| Monachus | PERSON | PERSON | PROPN | PROPN | monachus | 1 |
| Monaldi | PERSON | PERSON | PROPN | PROPN | monaldus | 1 |
| Monticuli | LOC | LOC | PROPN | PROPN | monticulus | 1 |
| Monticulis | - | LOC | PROPN | PROPN | monticulis | 1 |
| Mors | NORP | PERSON | NOUN | NOUN | mors | 1 |
| Mortale | PERSON | PERSON | ADJ | ADJ | mortalis | 1 |
| Morte | PERSON | PERSON | NOUN | NOUN | mors | 1 |
| Mortes | NORP | - | NOUN | PROPN | mors | 1 |
| Mortis | PERSON | PERSON | NOUN | NOUN | mors | 1 |
| Mortis | PERSON | LOC | PROPN | PROPN | mors | 1 |
| Motus | PERSON | PERSON | NOUN | PROPN | motus | 1 |
| Movit | - | - | VERB | PROPN | mouit | 1 |
| Nabuchodonosor | PERSON | PERSON | PROPN | PROPN | nabuchodonosor | 1 |
| Natalis | PERSON | PERSON | PROPN | PROPN | natalis | 1 |
| Natus | PERSON | PERSON | PROPN | PROPN | nascor | 1 |
| Nefanda | - | PERSON | ADJ | PROPN | nefanda | 1 |
| Nero | PERSON | PERSON | PROPN | PROPN | nero | 1 |
| Neronis | PERSON | PERSON | PROPN | PROPN | nero | 1 |
| Nescitis | - | PERSON | VERB | PROPN | nescitis | 1 |
| Nostro | - | - | DET | PROPN | noster | 1 |
| Nova | - | - | ADJ | PROPN | nouus | 1 |
| Nubem | - | - | PROPN | PROPN | nubes | 1 |
| Nullo | - | - | DET | PROPN | nullus | 1 |
| Occidit | - | PERSON | VERB | VERB | occido | 1 |
| Odi | PERSON | - | VERB | PROPN | odius | 1 |
| Odore | - | PERSON | NOUN | PROPN | odore | 1 |
| Olympi | PERSON | PERSON | PROPN | PROPN | olympus | 1 |
| Olympo | PERSON | PERSON | PROPN | PROPN | olympus | 1 |
| Omni | - | - | DET | PROPN | omnis | 1 |
| Orcho | PERSON | PERSON | PROPN | PROPN | orchus | 1 |
| Ordo | - | PERSON | NOUN | NOUN | ordo | 1 |
| Pace | LOC | - | NOUN | PROPN | pax | 1 |
| Paduae | LOC | LOC | ADJ | PROPN | padua | 1 |
| Paduae | PERSON | LOC | PROPN | PROPN | padua | 1 |
| Paduam | LOC | - | PROPN | PROPN | paduam | 1 |
| Paduam | LOC | - | ADJ | PROPN | padua | 1 |
| Paduanos | NORP | NORP | PROPN | PROPN | paduani | 1 |
| Paludis | - | LOC | VERB | PROPN | palus | 1 |
| Pande | - | - | VERB | PROPN | pandus | 1 |
| Papae | - | - | PROPN | PROPN | papa | 1 |
| Parce | - | PERSON | VERB | PROPN | parcus | 1 |
| Pars | - | PERSON | PROPN | NOUN | pars | 1 |
| Partes | NORP | - | NOUN | NOUN | pars | 1 |
| Partes | NORP | - | NOUN | NOUN | partes | 1 |
| Patavorum | NORP | NORP | PROPN | PROPN | patauorum | 1 |
| Patavos | NORP | - | ADJ | PROPN | patauus | 1 |
| Patavum | - | - | PROPN | ADJ | patauus | 1 |
| Patrem | - | - | NOUN | PROPN | pater | 1 |
| Pax | - | PERSON | PROPN | PROPN | pax | 1 |
| Peccare | PERSON | - | VERB | VERB | pecco | 1 |
| Pellavicini | PERSON | PERSON | PROPN | PROPN | pellauicinus | 1 |
| Pellavicino | PERSON | - | ADJ | PROPN | pellauicinus | 1 |
| Perditio | PERSON | PERSON | PROPN | PROPN | perditio | 1 |
| Persephone | PERSON | PERSON | PROPN | PROPN | persephone | 1 |
| Pertulit | PERSON | PERSON | VERB | VERB | perfero | 1 |
| Pervigil | PERSON | PERSON | NOUN | PROPN | peruigil | 1 |
| Petens | PERSON | - | VERB | PROPN | petens | 1 |
| Petiere | PERSON | PERSON | PROPN | PROPN | petiere | 1 |
| Pharao | PERSON | PERSON | PROPN | PROPN | pharao | 1 |
| Philippi | PERSON | PERSON | PROPN | PROPN | philippus | 1 |
| Pietas | - | - | PROPN | PROPN | pietas | 1 |
| Pinguis | PERSON | - | PROPN | PROPN | pinguis | 1 |
| Plebe | - | PERSON | NOUN | PROPN | plebus | 1 |
| Plebs | - | - | PROPN | PROPN | plebs | 1 |
| Pleno | PERSON | PERSON | ADJ | PROPN | plenus | 1 |
| Plurimas | - | - | DET | PROPN | plurimas | 1 |
| Plutone | PERSON | PERSON | PROPN | PROPN | pluto | 1 |
| Poenas | NORP | - | NOUN | PROPN | poena | 1 |
| Polluere | PERSON | - | VERB | PROPN | polluere | 1 |
| Pons | - | - | NOUN | PROPN | pons | 1 |
| Praelata | - | - | PROPN | VERB | praelata | 1 |
| Praemium | PERSON | - | PROPN | PROPN | praemium | 1 |
| Praepotens | - | - | NOUN | PROPN | praepotens | 1 |
| Praesidia | - | PERSON | NOUN | PROPN | praesidium | 1 |
| Procede | - | PERSON | VERB | VERB | procedo | 1 |
| Procede | - | PERSON | VERB | PROPN | procedus | 1 |
| Procustis | NORP | PERSON | PROPN | PROPN | procustis | 1 |
| Progredere | - | - | VERB | PROPN | progredere | 1 |
| Progressa | - | PERSON | VERB | PROPN | progressa | 1 |
| Proh | PERSON | - | VERB | ADJ | proh | 1 |
| Prohibere | - | - | VERB | PROPN | prohiberus | 1 |
| Prohibere | PERSON | - | VERB | VERB | prohibere | 1 |
| Promissa | - | - | VERB | PROPN | promissa | 1 |
| Propere | - | PERSON | ADV | PROPN | propere | 1 |
| Publico | - | PERSON | NOUN | ADJ | publico | 1 |
| Quadnam | - | - | ADV | PROPN | quadnam | 1 |
| Qualis | - | - | DET | PROPN | qualis | 1 |
| Qualis | - | PERSON | DET | ADJ | qualis | 1 |
| Quemquam | - | - | PRON | PROPN | quemquamus | 1 |
| Quidni | - | - | ADV | PROPN | quidni | 1 |
| Recolis | - | PERSON | VERB | ADJ | recolo | 1 |
| Recolo | LOC | PERSON | VERB | PROPN | recolo | 1 |
| Redemptor | - | PERSON | PROPN | PROPN | redemptor | 1 |
| Regula | LOC | - | PROPN | NOUN | regula | 1 |
| Regula | - | - | NOUN | PROPN | regula | 1 |
| Remus | - | - | PROPN | PROPN | remus | 1 |
| Retro | PERSON | PERSON | ADV | PROPN | retro | 1 |
| Retro | PERSON | PERSON | ADV | PROPN | retrus | 1 |
| Rex | - | PERSON | NOUN | NOUN | rex | 1 |
| Romanum | NORP | NORP | ADJ | ADJ | romanus | 1 |
| Romulus | PERSON | PERSON | PROPN | PROPN | romulus | 1 |
| Rumor | PERSON | PERSON | PROPN | NOUN | rumor | 1 |
| Saepe | NORP | - | ADV | PROPN | saepus | 1 |
| Saeva | LOC | LOC | PROPN | PROPN | saeua | 1 |
| Saevae | PERSON | LOC | ADJ | ADJ | saeuus | 1 |
| Saevire | NORP | PERSON | VERB | PROPN | saeuire | 1 |
| Salinguerra | - | PERSON | PROPN | PROPN | salinguerra | 1 |
| Salubre | PERSON | PERSON | ADJ | PROPN | salubra | 1 |
| Sathan | PERSON | PERSON | PROPN | PROPN | sathan | 1 |
| Saul | PERSON | PERSON | PROPN | PROPN | saul | 1 |
| Saulus | PERSON | PERSON | PROPN | PROPN | saulus | 1 |
| Scriptura | PERSON | - | PROPN | NOUN | scriptura | 1 |
| Secede | - | PERSON | VERB | PROPN | secedus | 1 |
| Sedes | NORP | LOC | NOUN | NOUN | sedes | 1 |
| Semper | - | - | ADV | PROPN | semper | 1 |
| Senem | PERSON | PERSON | PROPN | PROPN | sen | 1 |
| Sermone | PERSON | PERSON | NOUN | PROPN | sermo | 1 |
| Serperet | - | PERSON | VERB | PROPN | serperet | 1 |
| Servare | - | PERSON | VERB | VERB | seruo | 1 |
| Setis | NORP | PERSON | PROPN | ADJ | setis | 1 |
| Signis | NORP | - | NOUN | NOUN | signis | 1 |
| Sodomae | LOC | - | PROPN | PROPN | sodoma | 1 |
| Soli | PERSON | PERSON | PROPN | PROPN | sol | 1 |
| Solvite | PERSON | PERSON | VERB | PROPN | soluitus | 1 |
| Spectator | PERSON | PERSON | NOUN | PROPN | spectator | 1 |
| Speres | - | - | VERB | PROPN | speres | 1 |
| Spes | - | - | PROPN | PROPN | spes | 1 |
| Stabiles | NORP | - | ADJ | ADJ | stabiles | 1 |
| Stigem | PERSON | PERSON | PROPN | PROPN | stix | 1 |
| Stillet | PERSON | PERSON | VERB | PROPN | stillet | 1 |
| Stratus | PERSON | PERSON | VERB | PROPN | stratus | 1 |
| Strictus | PERSON | - | VERB | PROPN | strictus | 1 |
| Stupenda | - | PERSON | PROPN | VERB | stupenda | 1 |
| Subigam | LOC | - | VERB | PROPN | subiga | 1 |
| Subiit | - | PERSON | VERB | VERB | subeo | 1 |
| Suncini | PERSON | - | PROPN | PROPN | suncinus | 1 |
| Supina | LOC | LOC | PROPN | ADJ | supina | 1 |
| Supplicia | - | PERSON | NOUN | NOUN | supplicium | 1 |
| Tartareas | NORP | LOC | ADJ | ADJ | tartareus | 1 |
| Tarvisia | PERSON | LOC | ADJ | ADJ | taruisia | 1 |
| Tarvisium | LOC | LOC | PROPN | PROPN | taruisius | 1 |
| Tarvisium | PERSON | LOC | PROPN | PROPN | taruisium | 1 |
| Tellure | PERSON | PERSON | PROPN | PROPN | tellus | 1 |
| Tellure | PERSON | PERSON | NOUN | PROPN | tellus | 1 |
| Telluris | PERSON | - | PROPN | PROPN | tellus | 1 |
| Tellus | PERSON | PERSON | PROPN | PROPN | tellus | 1 |
| Terribile | NORP | - | ADJ | ADJ | terribile | 1 |
| Terror | NORP | PERSON | NOUN | NOUN | terror | 1 |
| Testor | - | PERSON | VERB | ADJ | testor | 1 |
| Thesiphone | PERSON | PERSON | PROPN | PROPN | thesipho | 1 |
| Tormenta | PERSON | PERSON | PROPN | PROPN | tormenta | 1 |
| Totus | PERSON | PERSON | DET | DET | totus | 1 |
| Tradere | PERSON | PERSON | VERB | PROPN | tradereus | 1 |
| Traducat | - | PERSON | VERB | VERB | traducat | 1 |
| Tragula | PERSON | PERSON | NOUN | PROPN | tragula | 1 |
| Traxere | NORP | PERSON | VERB | VERB | traxere | 1 |
| Triennis | LOC | PERSON | PROPN | PROPN | triennes | 1 |
| Turbine | NORP | LOC | NOUN | PROPN | turbinus | 1 |
| Turpi | PERSON | - | PROPN | ADJ | turpis | 1 |
| Turris | PERSON | PERSON | PROPN | PROPN | turris | 1 |
| Typheus | PERSON | PERSON | PROPN | PROPN | typheus | 1 |
| Una | - | - | ADV | PROPN | una | 1 |
| Una | - | PERSON | ADV | NUM | una | 1 |
| Undante | - | PERSON | PROPN | PROPN | undans | 1 |
| Unius | - | PERSON | NUM | DET | unus | 1 |
| Urbs | LOC | - | PROPN | PROPN | urbs | 1 |
| Utraque | - | PERSON | DET | DET | utraque | 1 |
| Vallatam | PERSON | PERSON | PROPN | PROPN | uallata | 1 |
| Venere | PERSON | PERSON | ADJ | PROPN | uenus | 1 |
| Venere | PERSON | LOC | VERB | PROPN | uenus | 1 |
| Venetis | NORP | NORP | VERB | ADJ | ueneti | 1 |
| Venetus | PERSON | PERSON | PROPN | PROPN | uenetus | 1 |
| Venit | - | PERSON | VERB | VERB | uenio | 1 |
| Venit | - | PERSON | VERB | VERB | uenit | 1 |
| Ventorum | - | PERSON | PROPN | ADJ | uentorum | 1 |
| Venturae | PERSON | PERSON | PROPN | PROPN | uenturas | 1 |
| Venus | PERSON | PERSON | PROPN | PROPN | uenus | 1 |
| Veronam | LOC | PERSON | PROPN | PROPN | uerona | 1 |
| Veronam | LOC | PERSON | NOUN | PROPN | uerona | 1 |
| Vesane | NORP | PERSON | PROPN | PROPN | uesane | 1 |
| Vetus | PERSON | PERSON | PROPN | PROPN | uetus | 1 |
| Vi | - | - | NOUN | PROPN | ui | 1 |
| Viam | LOC | PERSON | PROPN | PROPN | uia | 1 |
| Vicentia | - | - | ADJ | PROPN | uicetia | 1 |
| Vicentia | - | - | VERB | PROPN | uicetia | 1 |
| Victimis | NORP | PERSON | ADJ | ADJ | uictimis | 1 |
| Videt | - | PERSON | VERB | VERB | uideo | 1 |
| Videtne | - | PERSON | VERB | PROPN | uidetne | 1 |
| Vincenda | PERSON | PERSON | VERB | PROPN | uincenda | 1 |
| Vincenda | - | PERSON | VERB | PROPN | uincenda | 1 |
| Vindex | PERSON | PERSON | PROPN | PROPN | uindex | 1 |
| Virgine | PERSON | PERSON | NOUN | NOUN | uirgo | 1 |
| Viscera | PERSON | PERSON | NOUN | PROPN | uiscera | 1 |
| Voces | NORP | - | NOUN | NOUN | uoces | 1 |
| Vos | - | NORP | PRON | PRON | uos | 1 |
| Vota | - | PERSON | NOUN | PROPN | uota | 1 |
| Vulcane | PERSON | PERSON | PROPN | PROPN | uulcanus | 1 |
| Vulgus | NORP | PERSON | PROPN | PROPN | uulgus | 1 |
| Vulgus | - | PERSON | PROPN | PROPN | uulgus | 1 |
| Zenonis | PERSON | PERSON | PROPN | PROPN | zeno | 1 |
| Ziramons | PERSON | PERSON | NOUN | PROPN | ziramons | 1 |

- Entity spans in the whole corpus: {'old': 3455, '3.9.8': 3449}

## 3. Overall lemma agreement on the tokens the pipeline keeps

- Same lemma: 41,695 of 46,544 (89.6%). Distinct disagreement pairs: 2,146.

Most frequent disagreements (old -> 3.9.8):

| old | 3.9.8 | n |
|---|---|---|
| coniunx | coniux | 136 |
| alo | altus | 68 |
| nascor | natus | 62 |
| superus | superi | 49 |
| malum | malus | 44 |
| dexter | dextera | 29 |
| minor | paruus | 29 |
| adsum | assum | 29 |
| animus | anima | 28 |
| exul | exsul | 27 |
| uictus | uinco | 25 |
| tenebra | tenebrae | 25 |
| maneo | manes | 24 |
| extremus | exter | 24 |
| iussus | iubeo | 23 |
| danaus | danai | 23 |
| inferus | inferi | 23 |
| fera | ferus | 22 |
| iunctus | iungo | 22 |
| umerus | humerus | 21 |
| gnatus | natus | 21 |
| uoltus | uultus | 21 |
| malus | malum | 20 |
| maior | magnus | 18 |
| misero | miserandus | 18 |
| mixtus | misceo | 17 |
| saeuio | saeuus | 17 |
| ferus | fero | 17 |
| melior | bonus | 17 |
| planctus | plango | 17 |
| imus | inferus | 17 |
| natis | natus | 16 |
| stirpes | stirps | 16 |
| tono | tonans | 16 |
| exilium | exsilium | 15 |
| laeto | laetus | 15 |
| tempto | tento | 15 |
| bracchium | brachium | 15 |
| natus | nascor | 14 |
| paelex | pellex | 14 |
| rex | rego | 13 |
| tego | tectum | 13 |
| inuideo | inuisus | 13 |
| sacer | sacrum | 13 |
| tutus | tuor | 13 |
| caesum | caedo | 13 |
| nosco | notus | 12 |
| paro | par | 12 |
| genitus | gigno | 12 |
| patria | patrius | 12 |
| noceo | nocens | 12 |
| pinna | penna | 12 |
| ardens | ardeo | 12 |
| summus | superus | 12 |
| uinclum | uinculum | 12 |
| iratus | irascor | 12 |
| erinys | erinnys | 12 |
| grauus | grauis | 11 |
| grauior | grauis | 11 |
| raptum | rapio | 11 |
