# Act-level pairings against a chance baseline (k = 24, 101 seeds: 0-99 and 42)

Share = fraction of seeds in which the two acts have the same dominant topic. Baseline = the same share for every pair of the 56 acts (1,540 pairs). Percentile rank = % of all pairs with an equal or lower share.

## original

Baseline over 1540 act pairs: median 0.129, 95th percentile 0.386, max 0.614; 1 pairs never share a topic.

| pairing | source | share of seeds | baseline median | baseline 95th pct | percentile rank |
|---|---|---|---|---|---|
| Ece 1 – Aga 1 | seed-42 pairing | 0.119 (12/101) | 0.129 | 0.386 | 48.2 |
| Ece 1 – Pho 1 | seed-42 pairing | 0.149 (15/101) | 0.129 | 0.386 | 59.4 |
| Ece 2 – Thy 1 | seed-42 pairing | 0.059 (6/101) | 0.129 | 0.386 | 16.1 |
| Ece 5 – Thy 1 | seed-42 pairing | 0.079 (8/101) | 0.129 | 0.386 | 27.9 |
| Ece 2 – Ece 5 | seed-42 pairing | 0.059 (6/101) | 0.129 | 0.386 | 16.1 |
| Ece 4 – Oed 4 | seed-42 pairing | 0.059 (6/101) | 0.129 | 0.386 | 16.1 |
| Ece 4 – Tro 4 | seed-42 pairing | 0.040 (4/101) | 0.129 | 0.386 | 7.2 |
| Ece 1 – HF 2 | 21-seed run: most frequent | 0.178 (18/101) | 0.129 | 0.386 | 67.9 |
| Ece 3 – HF 2 | 21-seed run: most frequent | 0.208 (21/101) | 0.129 | 0.386 | 73.2 |

This pipeline's own seed-42 pairings involving Ecerinis: Aga 1–Ece 1, Aga 2–Ece 3, Aga 3–Ece 3, Ece 1–Pho 1, Ece 2–Ece 5, Ece 2–Thy 1, Ece 3–HF 1, Ece 3–HF 2, Ece 3–HF 3, Ece 3–HO 2, Ece 3–Med 3, Ece 3–Med 5, Ece 3–Oct 1, Ece 3–Oct 6, Ece 3–Oed 2, Ece 3–Pha 2, Ece 3–Pho 2, Ece 3–Pho 4, Ece 3–Thy 2, Ece 3–Thy 3, Ece 3–Tro 3, Ece 4–Oed 4, Ece 4–Tro 4, Ece 5–Thy 1

### Shared content lemmas (original)

Lemmas present in both acts in the model input (after named-entity removal and the dictionary filter no_below=2, no_above=0.5); counts as act A / act B. 'Removed by the filter' = shared before the dictionary filter but not in the model vocabulary.

- **Ece 1 – Aga 1**: 34 shared in the model vocabulary: inferus 3/1, nefandus 3/1, incertus 1/2, insero 2/1, leuo 2/1, nubes 2/1, polus 1/2, pudor 1/2, quies 2/1, arx 1/1, collis 1/1, excelsus 1/1, fulmen 1/1, hora 1/1, imus 1/1, iuba 1/1, iugulum 1/1, ius 1/1, labo 1/1, maior 1/1, onus 1/1, paternus 1/1, profundum 1/1, rota 1/1, sedeo 1/1, somnus 1/1, specus 1/1, torqueo 1/1, uaco 1/1, uentus 1/1, uerto 1/1, uicis 1/1, uro 1/1, uterum 1/1. Removed by the filter: 25 more (most frequent: pater 7/3, domus 2/3, regnum 4/1, rex 2/3, cado 3/1, dignus 3/1, locus 1/3, manus 1/3).
- **Ece 1 – Pho 1**: 51 shared in the model vocabulary: nefandus 3/3, nex 1/5, paternus 1/5, facinus 1/4, scio 2/3, imperium 2/2, nobilis 2/2, occupo 2/2, opus 2/2, pudeo 2/2, uis 1/3, cor 2/1, desero 1/2, infans 1/2, insero 2/1, ius 1/2, leuo 2/1, quies 2/1, scindo 1/2, sedeo 1/2, spiritus 2/1, surgo 1/2, uerto 1/2, assum 1/1, capax 1/1, crudelis 1/1, excipio 1/1, explico 1/1, fulmen 1/1, homo 1/1, ignotus 1/1, impetus 1/1, ingenium 1/1, inimicus 1/1, iuuo 1/1, minae 1/1, mixtus 1/1, pareo 1/1, pario 1/1, partus 1/1, possideo 1/1, praeda 1/1, pudor 1/1, recipio 1/1, sanguineus 1/1, sentio 1/1, tendo 1/1, uaco 1/1, uoluo 1/1, uomo 1/1, utor 1/1. Removed by the filter: 45 more (most frequent: pater 7/16, regnum 4/12, manus 1/13, parens 1/10, deus 1/9, domus 2/6, nego 3/5, ago 1/6).
- **Ece 2 – Thy 1**: 25 shared in the model vocabulary: nobilis 3/2, odium 3/1, uicis 2/2, dexter 1/2, dominus 2/1, inuenio 1/2, nefandus 2/1, rabies 2/1, subeo 2/1, ara 1/1, arbiter 1/1, effundo 1/1, eicio 1/1, exardesco 1/1, facinus 1/1, infernus 1/1, innocens 1/1, labo 1/1, pello 1/1, pes 1/1, remotus 1/1, sacro 1/1, superbus 1/1, supplicium 1/1, tutus 1/1. Removed by the filter: 31 more (most frequent: deus 3/3, nefas 2/4, populus 5/1, terra 3/3, bellum 4/1, genus 4/1, malum 1/4, os 1/4).
- **Ece 5 – Thy 1**: 31 shared in the model vocabulary: nepos 1/3, arceo 1/2, dexter 1/2, gladius 2/1, patruus 1/2, subdo 2/1, tango 1/2, tutus 2/1, actus 1/1, agmen 1/1, alludo 1/1, antrum 1/1, cubile 1/1, dens 1/1, fallo 1/1, for 1/1, guttur 1/1, infernus 1/1, innocens 1/1, insto 1/1, ius 1/1, liquor 1/1, modus 1/1, moneo 1/1, mons 1/1, nubes 1/1, patulus 1/1, pes 1/1, placidus 1/1, struo 1/1, supplicium 1/1. Removed by the filter: 34 more (most frequent: domus 1/9, sto 4/5, os 4/4, manus 4/2, caput 4/1, cruor 2/3, miser 1/4, ignis 2/2).
- **Ece 2 – Ece 5**: 26 shared in the model vocabulary: finis 4/1, tenebra 3/1, ardeo 1/2, arx 1/2, proles 1/2, tutus 1/2, aequum 1/1, aeuum 1/1, ambitus 1/1, cassus 1/1, dexter 1/1, dono 1/1, falsus 1/1, frequens 1/1, gemitus 1/1, illecebra 1/1, infans 1/1, infernus 1/1, innocens 1/1, memoro 1/1, meritum 1/1, patro 1/1, pes 1/1, procedo 1/1, supernus 1/1, supplicium 1/1. Removed by the filter: 23 more (most frequent: populus 5/2, manus 2/4, os 1/4, pater 3/2,  2/2, ignis 2/2, ago 2/1, cruor 1/2).
- **Ece 4 – Oed 4**: 19 shared in the model vocabulary: iter 3/1, iuuenis 2/2, pes 1/2, reuertor 2/1, reuoco 2/1, uis 2/1, appeto 1/1, audax 1/1, expedio 1/1, expeto 1/1, fido 1/1, fruor 1/1, horreo 1/1, pietas 1/1, quies 1/1, salus 1/1, scio 1/1, subdo 1/1, tutus 1/1. Removed by the filter: 25 more (most frequent: manus 2/7, fides 2/6, deus 3/2, fatum 1/4, locus 2/3, nomen 1/4, dignus 2/2, moueo 1/3).
- **Ece 4 – Tro 4**: 15 shared in the model vocabulary: uotum 3/2, bonus 2/1, iuuenis 2/1, occupo 2/1, quies 1/2, uirgo 1/2, crudelis 1/1, fraus 1/1, horreo 1/1, misceo 1/1, nex 1/1, opto 1/1, scio 1/1, sinister 1/1, tergum 1/1. Removed by the filter: 27 more (most frequent: deus 3/4, manus 2/5, fatum 1/5, ago 2/3, malum 1/4, uultus 1/4, dignus 2/2, paro 2/2).

## v2

Baseline over 1540 act pairs: median 0.158, 95th percentile 0.436, max 0.614; 0 pairs never share a topic.

| pairing | source | share of seeds | baseline median | baseline 95th pct | percentile rank |
|---|---|---|---|---|---|
| Ece 1 – Aga 1 | seed-42 pairing | 0.079 (8/101) | 0.158 | 0.436 | 23.4 |
| Ece 1 – Pho 1 | seed-42 pairing | 0.149 (15/101) | 0.158 | 0.436 | 49.9 |
| Ece 2 – Thy 1 | seed-42 pairing | 0.010 (1/101) | 0.158 | 0.436 | 0.3 |
| Ece 5 – Thy 1 | seed-42 pairing | 0.129 (13/101) | 0.158 | 0.436 | 44.0 |
| Ece 2 – Ece 5 | seed-42 pairing | 0.030 (3/101) | 0.158 | 0.436 | 3.5 |
| Ece 4 – Oed 4 | seed-42 pairing | 0.089 (9/101) | 0.158 | 0.436 | 28.5 |
| Ece 4 – Tro 4 | seed-42 pairing | 0.050 (5/101) | 0.158 | 0.436 | 9.5 |
| Ece 1 – HF 2 | 21-seed run: most frequent | 0.188 (19/101) | 0.158 | 0.436 | 59.9 |
| Ece 3 – HF 2 | 21-seed run: most frequent | 0.297 (30/101) | 0.158 | 0.436 | 79.9 |

This pipeline's own seed-42 pairings involving Ecerinis: Aga 2–Ece 3, Aga 5–Ece 3, Ece 1–Ece 4, Ece 3–HF 2, Ece 3–HF 4, Ece 3–HF 5, Ece 3–HO 2, Ece 3–HO 3, Ece 3–HO 4, Ece 3–Med 2, Ece 3–Med 3, Ece 3–Med 4, Ece 3–Med 5, Ece 3–Oct 1, Ece 3–Oct 2, Ece 3–Oct 3, Ece 3–Oed 1, Ece 3–Oed 2, Ece 3–Oed 3, Ece 3–Pha 1, Ece 3–Pha 2, Ece 3–Pha 3, Ece 3–Pha 5, Ece 3–Pho 1, Ece 3–Pho 3, Ece 3–Thy 2, Ece 3–Thy 3, Ece 3–Tro 2, Ece 3–Tro 3, Ece 5–Oed 5, Ece 5–Pho 2, Ece 5–Thy 4

### Shared content lemmas (v2)

Lemmas present in both acts in the model input (after named-entity removal and the dictionary filter no_below=2, no_above=0.5); counts as act A / act B. 'Removed by the filter' = shared before the dictionary filter but not in the model vocabulary.

- **Ece 1 – Aga 1**: 41 shared in the model vocabulary: dolus 2/2, nefandus 3/1, uiscus 3/1, cura 1/2, incertus 1/2, insero 2/1, leuo 2/1, nubes 2/1, polus 1/2, pudor 1/2, quies 2/1, superbus 1/2, arx 1/1, auster 1/1, ceruix 1/1, collis 1/1, fulmen 1/1, hora 1/1, iuba 1/1, iugulum 1/1, labo 1/1, misceo 1/1, natalis 1/1, odi 1/1, onus 1/1, paternus 1/1, profundus 1/1, remus 1/1, rota 1/1, sedeo 1/1, somnus 1/1, specus 1/1, torqueo 1/1, turris 1/1, uaco 1/1, uentus 1/1, uerro 1/1, uicis 1/1, uilis 1/1, uro 1/1, uterus 1/1. Removed by the filter: 48 more (most frequent: pater 8/3, magnus 2/5, scelus 3/4, domus 3/3, inferus 5/1, animus 3/2, cado 4/1, mater 4/1).
- **Ece 1 – Pho 1**: 72 shared in the model vocabulary: nefandus 3/3, nex 1/5, paternus 1/5, crimen 3/2, facinus 1/4, uiscus 3/2, dolus 2/2, gigno 2/2, imperium 2/2, nobilis 2/2, occupo 2/2, opus 2/2, pudeo 2/2, uis 1/3, antiquus 1/2, auris 1/2, careo 1/2, comes 1/2, cor 2/1, desero 1/2, infans 1/2, insero 2/1, leuo 2/1, paruus 2/1, quies 2/1, scindo 1/2, sedeo 1/2, spiritus 2/1, surgo 1/2, uerus 2/1, utor 1/2, aetas 1/1, capax 1/1, citus 1/1, ciuis 1/1, clades 1/1, condio 1/1, crudelis 1/1, cura 1/1, effor 1/1, excipio 1/1, explico 1/1, faueo 1/1, fulmen 1/1, homo 1/1, ignotus 1/1, impetus 1/1, infaustus 1/1, ingenium 1/1, inimicus 1/1, iuuo 1/1, lateo 1/1, lex 1/1, lues 1/1, manes 1/1, misceo 1/1, pario 1/1, partus 1/1, possideo 1/1, praeda 1/1, pudor 1/1, recipio 1/1, sanguineus 1/1, sterno 1/1, supplex 1/1, taurus 1/1, tendo 1/1, tono 1/1, uaco 1/1, uoluo 1/1, uomo 1/1, uterus 1/1. Removed by the filter: 85 more (most frequent: pater 8/16, mors 4/16, regnum 4/12, scelus 3/12, manus 1/13, mater 4/9, deus 2/9, parens 1/10).
- **Ece 2 – Thy 1**: 37 shared in the model vocabulary: fames 2/7, nobilis 3/2, carcer 2/2, odium 3/1, uicis 2/2, dominus 2/1, inuenio 1/2, labo 2/1, nefandus 2/1, neglego 2/1, rabies 2/1, subeo 2/1, tollo 2/1, uetus 1/2, anguis 1/1, ara 1/1, arbiter 1/1, caecus 1/1, cerno 1/1, dexter 1/1, effundo 1/1, eicio 1/1, exardesco 1/1, facinus 1/1, flagro 1/1, fuga 1/1, infernus 1/1, innocens 1/1, lateo 1/1, luo 1/1, pello 1/1, pes 1/1, sedes 1/1, sisto 1/1, superbus 1/1, supplicium 1/1, uictima 1/1. Removed by the filter: 53 more (most frequent: scelus 3/7, dirus 4/3, deus 3/3, frater 3/3, magnus 2/4, nefas 2/4, populus 5/1, terra 3/3).
- **Ece 5 – Thy 1**: 40 shared in the model vocabulary: fames 1/7, auidus 1/3, nepos 1/3, patruus 2/2, arceo 1/2, gladius 2/1, pateo 2/1, profugus 1/2, subdo 2/1, tango 1/2, actus 1/1, agmen 1/1, alludo 1/1, antrum 1/1, crimen 1/1, cubile 1/1, dens 1/1, dexter 1/1, duro 1/1, fallo 1/1, guttur 1/1, incendo 1/1, infernus 1/1, infestus 1/1, innocens 1/1, insto 1/1, lex 1/1, liquor 1/1, modus 1/1, moneo 1/1, mons 1/1, nubes 1/1, patulus 1/1, pes 1/1, placidus 1/1, stringo 1/1, struo 1/1, supplicium 1/1, uena 1/1, uiolentus 1/1. Removed by the filter: 50 more (most frequent: domus 1/9, sto 4/5, os 4/4, scelus 1/7, manus 4/2, caput 4/1, cruor 2/3, magnus 1/4).
- **Ece 2 – Ece 5**: 34 shared in the model vocabulary: finis 4/1, tenebrae 3/1, arx 1/2, atrox 1/2, fames 2/1, fundo 1/2, iustus 1/2, lumen 2/1, pando 1/2, proles 1/2, uulgus 1/2, aequum 1/1, aeuum 1/1, ambitus 1/1, cassus 1/1, deuoueo 1/1, dexter 1/1, dono 1/1, falsus 1/1, frequens 1/1, gemitus 1/1, illecebra 1/1, infans 1/1, infernus 1/1, innocens 1/1, marchio 1/1, memoro 1/1, patro 1/1, pes 1/1, procedo 1/1, seco 1/1, serpo 1/1, supernus 1/1, supplicium 1/1. Removed by the filter: 37 more (most frequent: populus 5/2, manus 2/4, caelum 3/2, dirus 4/1, os 1/4, pars 3/2, pater 3/2, altus 2/2).
- **Ece 4 – Oed 4**: 23 shared in the model vocabulary: iter 3/1, iuuenis 2/2, uis 3/1, anceps 1/2, pes 1/2, reuoco 2/1, acer 1/1, allido 1/1, appeto 1/1, audax 1/1, cura 1/1, expedio 1/1, expeto 1/1, fido 1/1, fruor 1/1, horreo 1/1, nobilis 1/1, pietas 1/1, quies 1/1, salus 1/1, subdo 1/1, summus 1/1, uiduus 1/1. Removed by the filter: 42 more (most frequent: senex 3/7, manus 2/7, fides 2/6, fatum 1/6, peto 2/5, uia 1/5, deus 3/2, locus 2/3).
- **Ece 4 – Tro 4**: 17 shared in the model vocabulary: occupo 3/1, signum 3/1, bonus 2/1, iuuenis 2/1, quies 1/2, uirgo 1/2, crudelis 1/1, festus 1/1, fraus 1/1, horreo 1/1, infestus 1/1, misceo 1/1, nex 1/1, opto 1/1, reuiuo 1/1, sinister 1/1, tergum 1/1. Removed by the filter: 46 more (most frequent: capio 1/6, deus 3/4, manus 2/5, fatum 1/5, mater 1/5, mors 1/5, malum 1/4, peto 2/3).

