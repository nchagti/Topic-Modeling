# Theme lexicon v2: revised audit (decisions of context/lexicon_audit_decisions.md)

Author-chosen word families (`data/theme_lexicon.json`), counted as v2 tokens before the dictionary filter. Lexicon-only token rules (`_token_rules` in the lexicon file) apply; the LDA input is unchanged. Seneca = the ten plays combined. Rate = family tokens per 1,000 v2 tokens (Ecerinis 2,195; Seneca 41,931). The step 1 audit (`lexicon_audit.md`) is kept as it was.

Verse numbers in this file and from now on are the TEI editions' `<l n>` verse numbers (`src/verses.py`). Earlier reports gave the position of the line in the v2 text, which counts each piece of a verse split between speakers (`<l part="I|M|F">`) as a line; Ecerinis has 25 such extra pieces, so line positions ran ahead of verse numbers (line 325 = v. 312, 454 = v. 431, 466 = v. 443; the vadum lines 505, 529 = vv. 482, 504; the vendico lines 90, 308 = vv. 83, 298). Seneca verse numbers are the DraCor TEI copies' per-verse `<milestone unit="line" n>` values (`data/sources/seneca_tei/`).

## Token rules applied

- deus 'dites' → (not counted): Seneca 1
- deus 'diti' → (not counted): Seneca 1
- foedus 'foeda' → (not counted): Ecerinis 1
- foedus 'foeda' → (not counted): Seneca 6
- foedus 'foedo' → (not counted): Seneca 3
- furor 'furabor' → (not counted): Seneca 2
- prodo 'prodidit' → (not counted): Seneca 1
- prodo 'proditur' → (not counted): Seneca 1
- prodo 'produnt' → (not counted): Seneca 1
- superus 'summa' → (not counted): Ecerinis 1
- superus 'summa' → (not counted): Seneca 7
- superus 'summam' → (not counted): Seneca 1
- superus 'summas' → (not counted): Seneca 4
- superus 'summe' → (not counted): Seneca 5
- superus 'summi' → (not counted): Ecerinis 1
- superus 'summi' → (not counted): Seneca 1
- superus 'summis' → (not counted): Seneca 8
- superus 'summo' → (not counted): Ecerinis 1
- superus 'summo' → (not counted): Seneca 5
- superus 'summum' → (not counted): Seneca 4
- superus 'summus' → (not counted): Seneca 5
- superus 'suprema' → (not counted): Seneca 3
- superus 'supremas' → (not counted): Seneca 1
- superus 'supremo' → (not counted): Seneca 1
- superus 'supremos' → (not counted): Seneca 1
- superus 'supremum' → (not counted): Seneca 1
- superus 'supremus' → (not counted): Seneca 1
- uas 'uadum' → uadum: Ecerinis 2
- uas 'uadum' → uadum: Seneca 3
- uendo 'uendens' → (not counted): Seneca 1
- uendo 'uendidistis' → (not counted): Seneca 1

## Family totals (all families; changed ones marked)

| family | Ecerinis | Ecerinis per 1,000 | Seneca | Seneca per 1,000 | thin (<5 Ecerinis) | change |
|---|---|---|---|---|---|---|
| invasion_conquest | 22 | 10.02 | 301 | 7.18 |  |  |
| deceit_betrayal | 19 | 8.66 | 171 | 4.08 |  | replaces deceit and betrayal_broken_faith; adds astus, transfuga; prodo and uendo only where marked y; foedus nouns only |
| punishment_vengeance | 8 | 3.64 | 206 | 4.91 |  |  |
| fate_fortune | 9 | 4.10 | 276 | 6.58 |  |  |
| natural_cosmic_order | 38 | 17.31 | 501 | 11.95 |  |  |
| providence_divine | 23 | 10.48 | 351 | 8.37 |  | adds superus (super- forms only), diuus, diua; excludes diti, dites from deus |
| piety_virtue | 23 | 10.48 | 314 | 7.49 |  |  |
| sea_water | 12 | 5.47 | 661 | 15.76 |  | uadum counts the vadum tokens v2 lemmatizes as uas |
| grief_lament | 8 | 3.64 | 346 | 8.25 |  | adds fletus |
| memory_report | 3 | 1.37 | 78 | 1.86 | **thin** |  |
| community_commune | 33 | 15.03 | 370 | 8.82 |  |  |
| law_judgment | 32 | 14.58 | 151 | 3.60 |  |  |
| rule_kingship | 22 | 10.02 | 716 | 17.08 |  |  |
| tyranny_servitude | 17 | 7.74 | 109 | 2.60 |  |  |
| lineage_kin | 70 | 31.89 | 1121 | 26.73 |  | adds natus, nata |
| rage_fury | 33 | 15.03 | 469 | 11.19 |  | adds furia; excludes furabor from furor |
| discord_strife | 6 | 2.73 | 25 | 0.60 |  | adds rebellis |

## Changed families, per lemma

### deceit_betrayal

replaces deceit and betrayal_broken_faith; adds astus, transfuga; prodo and uendo only where marked y; foedus nouns only. Total: Ecerinis 19 / Seneca 171.

| lemma | Ecerinis | Seneca | surface forms (top 8) |
|---|---|---|---|
| fraus | 3 | 34 | fraude 16; fraudis 6; fraudes 5; fraudi 3; fraus 3; fraudem 3; fraudibus 1 |
| dolus | 4 | 40 | dolos 15; doli 10; dolus 7; dolis 6; dolo 6 |
| fallo | 1 | 20 | fallor 4; falli 3; fallit 3; fallere 2; fallant 2; fefellissem 1; fallatur 1; fefellit 1 |
| falsus | 5 | 26 | falsa 8; falsum 5; falso 4; falsis 4; falsi 3; falsus 3; falsos 2; falsas 1 |
| fallax | 1 | 16 | fallax 11; fallaci 2; fallacis 2; fallacem 1; fallaces 1 |
| insidiae | 1 | 5 | insidias 3; insidiis 3 |
| astus | 2 | 4 | astu 4; astus 2 |
| transfuga | 1 | 0 | transfugas 1 |
| proditor | 0 | 0 | — |
| proditio | 0 | 0 | — |
| perfidus | 0 | 9 | perfida 3; perfidi 2; perfido 2; perfide 1; perfidus 1 |
| perfidia | 0 | 0 | — |
| periurus | 0 | 0 | — |
| periurium | 0 | 0 | — |
| foedus | 0 | 11 | foedus 5; foedera 4; foederis 1; foederi 1 |
| prodo | 0 | 6 | prodat 1; prodas 1; prodet 1; prodidit 1; prodimus 1; proditus 1 |
| uendo | 1 | 0 | uendidere 1 |

**Homograph, resolved by counting nouns only (`_pos_only`):** the key *foedus* merges *foedus* 'treaty' (noun) with *foedus* 'foul' (adjective; Morpheus foedus1). By v2 part of speech, before the rule: ADJ Ecerinis 1; ADJ Seneca 9; NOUN Seneca 11. The Ecerinis token is *Foeda* (Ece 2, v. 237, 'Foeda Gomorrae Sodomaeque labes'), the adjective.

### providence_divine

adds superus (super- forms only), diuus, diua; excludes diti, dites from deus. Total: Ecerinis 23 / Seneca 351.

| lemma | Ecerinis | Seneca | surface forms (top 8) |
|---|---|---|---|
| deus | 18 | 199 | deos 64; deus 61; deum 21; deorum 20; dei 17; deo 12; deis 12; di 8 |
| numen | 2 | 47 | numen 28; numina 8; numinum 5; numinis 4; numine 4 |
| superi | 0 | 64 | superos 35; superi 16; superis 12; superum 1 |
| diuinus | 1 | 0 | diuinam 1 |
| prouidentia | 0 | 0 | — |
| caelestis | 0 | 8 | caelestes 2; caelestis 2; caelestium 1; caelesti 1; caelestibus 1; caelestem 1 |
| superus | 0 | 11 | superis 5; superos 3; supera 1; superum 1; superi 1 |
| diuus | 1 | 19 | diuum 7; diui 4; diuos 2; diuus 2; diuae 1; diua 1; diuis 1; diuo 1 |
| diua | 1 | 3 | diua 4 |

**superus: only super- forms count (`_exclude_prefixes`).** v2 (LatinCy 3.9.8) files the superlative *summus* / *supremus* under *superus*. By surface form, before the rule: summ-/supr- Ecerinis 3; summ-/supr- Seneca 48; super- Seneca 11. All Ecerinis tokens are *summus* 'highest': *summi Olympi* (Ece 2, v. 230), *e summo datam* (Ece 4, v. 466), *arce summa* (Ece 5, v. 567).

### lineage_kin

adds natus, nata. Total: Ecerinis 70 / Seneca 1121.

| lemma | Ecerinis | Seneca | surface forms (top 8) |
|---|---|---|---|
| pater | 18 | 189 | pater 89; patrem 34; patris 32; patri 28; patre 15; patres 6; patrum 3 |
| paternus | 1 | 31 | paternis 7; paterna 5; paterno 5; paternae 4; paternus 4; paternum 3; paterni 3; paternos 1 |
| mater | 8 | 173 | mater 63; matris 44; matrem 22; matri 22; matres 19; matre 9; matrum 1; matribus 1 |
| auus | 0 | 13 | auo 4; aui 3; auum 3; auos 1; auiis 1; auus 1 |
| proles | 6 | 28 | proles 18; prolis 7; prolem 6; prole 3 |
| suboles | 1 | 5 | suboles 3; sobolis 2; subolem 1 |
| stirps | 1 | 21 | stirpem 9; stirpe 6; stirpis 5; stirps 1; stirpi 1 |
| genus | 13 | 80 | genus 69; generis 15; genere 6; generi 2; genera 1 |
| sanguis | 6 | 80 | sanguine 33; sanguis 22; sanguinem 21; sanguinis 10 |
| nepos | 1 | 18 | nepotes 6; nepos 6; nepotem 4; nepotibus 2; nepotis 1 |
| progenies | 1 | 5 | progenies 6 |
| heres | 0 | 3 | heres 3 |
| frater | 7 | 124 | frater 40; fratris 23; fratrem 22; fratri 13; fratrum 12; fratres 10; fratre 7; fratribus 4 |
| germanus | 0 | 9 | germani 3; germane 3; germanos 2; germanum 1 |
| parens | 3 | 140 | parens 73; parentis 25; parentem 19; parenti 11; parentes 8; parentum 3; parente 3; parentibus 1 |
| natus | 4 | 176 | nate 27; natum 24; nato 23; nati 16; natos 15; natus 13; natis 13; gnatus 8 |
| nata | 0 | 26 | nata 12; natam 7; gnata 4; natas 2; gnatae 1 |

### grief_lament

adds fletus. Total: Ecerinis 8 / Seneca 346.

| lemma | Ecerinis | Seneca | surface forms (top 8) |
|---|---|---|---|
| lacrima | 2 | 61 | lacrimas 30; lacrimis 19; lacrimae 13; lacrimam 1 |
| lacrimo | 0 | 5 | lacrimat 2; lacrimare 2; lacrimandum 1 |
| fleo | 0 | 43 | flere 9; flete 5; flemus 4; fleuit 4; flendi 3; fleat 3; flentem 3; fleo 2 |
| luctus | 0 | 43 | luctus 28; luctu 9; luctum 5; luctibus 1 |
| lugeo | 1 | 17 | lugere 7; luget 3; lugete 2; lugeat 2; lugebis 1; lugendus 1; lugendae 1; lugendo 1 |
| maeror | 0 | 10 | maeror 5; maerore 3; maeroris 2 |
| maereo | 0 | 15 | maeret 6; maerenti 2; maerens 2; maeres 2; maerere 2; maerentem 1 |
| gemitus | 3 | 18 | gemitus 13; gemitu 6; gemitum 2 |
| gemo | 0 | 40 | gemit 11; gemuit 5; gemunt 4; gemis 3; gemam 3; gemere 2; gemendus 2; gemeret 1 |
| planctus | 0 | 21 | planctus 16; planctu 4; planctibus 1 |
| plango | 0 | 7 | plangite 4; plangente 1; plangant 1; planxerunt 1 |
| queror | 1 | 26 | questus 5; queritur 5; queror 4; querimur 3; querar 2; questibus 2; questum 1; querere 1 |
| querela | 1 | 5 | querelas 3; querelis 2; querelae 1 |
| lamentor | 0 | 0 | — |
| fletus | 0 | 35 | fletus 17; fletu 12; fletum 4; fletibus 2 |

### rage_fury

adds furia; excludes furabor from furor. Total: Ecerinis 33 / Seneca 469.

| lemma | Ecerinis | Seneca | surface forms (top 8) |
|---|---|---|---|
| ira | 5 | 93 | ira 53; iras 22; irae 12; iram 7; irarum 4 |
| irascor | 0 | 13 | irata 7; irato 2; irasci 2; iratus 1; iratis 1 |
| furor | 7 | 75 | furor 57; furore 9; furoris 7; furorem 6; furori 2; furores 1 |
| furo | 3 | 58 | furit 21; furens 20; furentes 5; furentem 4; furentis 3; furis 2; furente 2; fureret 2 |
| furiosus | 0 | 4 | furiosa 2; furiose 1; furiosus 1 |
| rabies | 4 | 4 | rabies 6; rabiem 2 |
| rabidus | 0 | 14 | rabidus 4; rabidos 3; rabida 2; rabido 2; rabidum 1; rabidam 1; rabidae 1 |
| saeuio | 1 | 14 | saeuit 9; saeuire 5; saeuite 1 |
| saeuus | 8 | 141 | saeua 52; saeui 18; saeuus 16; saeuo 11; saeuum 10; saeuis 10; saeuos 8; saeuae 8 |
| insania | 0 | 0 | — |
| exardesco | 1 | 1 | exarsit 2 |
| odium | 4 | 46 | odia 27; odium 11; odio 11; odiis 1 |
| furia | 0 | 6 | furiarum 4; furiis 2 |

### discord_strife

adds rebellis. Total: Ecerinis 6 / Seneca 25.

| lemma | Ecerinis | Seneca | surface forms (top 8) |
|---|---|---|---|
| discordia | 0 | 0 | — |
| discors | 0 | 5 | discors 4; discordem 1 |
| dissidium | 0 | 0 | — |
| seditio | 1 | 0 | seditio 1 |
| factio | 0 | 0 | — |
| rixa | 0 | 0 | — |
| certamen | 1 | 1 | certaminis 1; certamina 1 |
| contentio | 0 | 0 | — |
| pugna | 0 | 3 | pugnam 2; pugnas 1 |
| pugno | 1 | 5 | pugnat 3; pugnanti 2; pugnandi 1 |
| inimicus | 1 | 11 | inimica 6; inimicum 4; inimici 1; inimicos 1 |
| rebellis | 2 | 0 | rebelle 1; rebelles 1 |

### sea_water

uadum counts the vadum tokens v2 lemmatizes as uas. Total: Ecerinis 12 / Seneca 661.

| lemma | Ecerinis | Seneca | surface forms (top 8) |
|---|---|---|---|
| mare | 3 | 128 | mare 66; maria 27; maris 21; mari 17 |
| pelagus | 0 | 29 | pelagus 12; pelago 9; pelagi 8 |
| pontus | 0 | 56 | pontum 17; pontus 16; ponto 15; ponti 8 |
| aequor | 0 | 19 | aequor 8; aequora 5; aequoris 3; aequore 2; aequorum 1 |
| fretum | 0 | 56 | freta 21; fretum 18; freto 10; fretis 5; freti 2 |
| unda | 1 | 82 | unda 31; undas 28; undis 17; undae 6; undarum 1 |
| fluctus | 0 | 48 | fluctus 23; fluctu 11; fluctibus 10; fluctum 4 |
| ratis | 2 | 66 | rates 23; ratem 14; ratis 11; ratibus 10; rate 7; rati 3 |
| nauis | 0 | 8 | nauibus 3; naues 2; nauem 2; nauis 1 |
| classis | 0 | 25 | classis 14; classibus 3; classes 3; classi 2; classe 2; classem 1 |
| prora | 0 | 4 | prora 3; prorae 1 |
| puppis | 0 | 24 | puppis 13; puppes 5; puppem 3; puppe 2; puppibus 1 |
| uelum | 0 | 20 | uela 14; uelis 5; uelo 1 |
| portus | 0 | 14 | portus 8; portu 3; portibus 2; portum 1 |
| naufragium | 0 | 3 | naufragia 2; naufragium 1 |
| procella | 1 | 11 | procellae 5; procella 4; procellis 2; procellas 1 |
| flumen | 2 | 13 | fluminis 5; flumina 3; flumine 3; fluminibus 2; flumini 1; flumen 1 |
| fluuius | 1 | 1 | fluuio 1; fluuius 1 |
| amnis | 0 | 22 | amnis 8; amnes 8; amnem 4; amne 2 |
| uadum | 2 | 32 | uada 12; uado 9; uadis 8; uadum 5 |

### punishment_vengeance (counts unchanged)

*uindico* has two senses, 'avenge / punish' and 'claim', and the lexicon cannot separate them. Ecerinis' medieval spelling *vendico* ('claim', vv. 83, 298) is keyed *uendico* (2 / 0) and is not counted under *uindico* (0 / 12); the *uindico* tokens that remain are not sense-checked.

## prodo: every token, for sense-checking

Marked by the author (`data/lexicon_marks/prodo_tokens_marked.csv`, column `betray`); tokens marked y count under deceit_betrayal.

| id | play | act | verse | speaker | form | v2_lemma | verse_text | note | betray |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Troades | 3 | 492 | Sen. | prodat | prodo | Ne prodat aliquis, amove testes doli. , |  | y |
| 2 | Troades | 3 | 587 | Andr. | prodas | prodo | [VLIX. Stulta est fides celare quod prodas statim.] |  | y |
| 3 | Phaedra | 2 | 363 | #nutrix | proditur | prodo | quamvis tegatur, proditur vultu furor; |  | n |
| 4 | Phaedra | 3 | 883 | Thes. | prodet | prodo | altrixque prodet quicquid haec fari abnuit. |  | y |
| 5 | Octavia | 1 | 269 | Oct. | prodidit | prodo | natumque ad umbras, prodidit lapsam domum. |  | y |
| 6 | Octavia | 1 | 290 | Chorus Romanorum | prodimus | prodo | prodimus aegro suadente metu. |  | y |
| 7 | Oedipus | 1 | 144 | Chorus Thebanorum | prodidit | prodo | prodidit armo. |  | n |
| 8 | Thyestes | 1 | 139 | Chorus | proditus | prodo | aut commune nefas, proditus occidit |  | y |
| 9 | Thyestes | 2 | 332 | Atr. | produnt | prodo | consilia produnt: nesciant quantae rei |  | n |
| 10 | Ecerinis | 3 | 281 | Ecerinus | prodit | prodeo | Matris relatu, vera quem prodit fides, | v2 lemma prodeo; Morpheus: prodeo or prodo | n |

## uendo ('sell'): every token; uendico listed separately

Marked by the author (`data/lexicon_marks/uendo_tokens_marked.csv`, column `decision`); uendo tokens marked y count under deceit_betrayal.

| id | play | act | verse | speaker | form | v2_lemma | verse_text | note | decision |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Troades | 3 | 664 | Andr. | uendidistis | uendo | Quae vendidistis? / Pergam et e summo |  | n |
| 2 | Hercules Furens | 1 | 173 | Chorus | uendens | uendo | iurgia vendens |  | n |
| 3 | Ecerinis | 1 | 83 | Ecerinus | uendicemus | uendico | si vendicemus operibus regnum patris, | uendico ('claim'): kept separate, listed for reference | n |
| 4 | Ecerinis | 2 | 227 | Nuntius | uendidere | uendo | qui vendidere, scelera iam expendunt sua. |  | y |
| 5 | Ecerinis | 3 | 298 | Ecerinus | uendicabo | uendico | ubi vendicabo forsitan caelum potens. | uendico ('claim'): kept separate, listed for reference | n |

## fingo in Ecerinis (reference only; not added)

| id | play | act | verse | speaker | form | v2_lemma | verse_text | note |
|---|---|---|---|---|---|---|---|---|
| 1 | Ecerinis | 3 | 318 | Ecerinus | finge | fingo | sub fraudis astu; finge te iratum michi: |  |
