# Seed-42 reproduction check (play level)

- Token lists identical to saved `filtered_token_lists.pkl`: True
- Dictionary identical to saved model's dictionary: True (new 1580, saved 1580)
- Ecerinis tokens: 1660 after NE removal, 377 after dictionary filter
- c_v at k=8 with processes=1: 0.3624602830; default processes: 0.3624602830

| k | coherence (saved / new) | overlap (saved / new) | trade-off (saved / new) | top-10 lists identical |
|---|---|---|---|---|
| 1 | 0.3983 / 0.4052 | 0.3575 / 0.3575 | 0.0409 / 0.0478 | False |
| 2 | 0.3473 / 0.3473 | 0.1638 / 0.1638 | 0.1834 / 0.1834 | True |
| 3 | 0.3399 / 0.3399 | 0.1366 / 0.1366 | 0.2033 / 0.2033 | True |
| 4 | 0.3318 / 0.3318 | 0.1378 / 0.1378 | 0.1940 / 0.1940 | True |
| 5 | 0.3577 / 0.3577 | 0.0995 / 0.0995 | 0.2583 / 0.2583 | True |
| 6 | 0.3555 / 0.3555 | 0.1321 / 0.1321 | 0.2234 / 0.2234 | True |
| 7 | 0.3714 / 0.3714 | 0.1198 / 0.1198 | 0.2516 / 0.2516 | True |
| 8 | 0.3625 / 0.3625 | 0.1017 / 0.1017 | 0.2608 / 0.2608 | True |
| 9 | 0.3674 / 0.3674 | 0.1103 / 0.1103 | 0.2571 / 0.2571 | True |

- Max |trade-off difference|: 6.87e-03
- Selected k (new): 8
- k=8 doc-topic max |difference| vs saved model: 3.31e-05

## k=8, new run: dominant topic per play (1-based)

- Phoenissae: Topic 1 (0.997)
- Troades: Topic 4 (0.998)
- Phaedra: Topic 7 (0.334)
- Agamemnon: Topic 2 (0.948)
- Hercules Furens: Topic 7 (0.491)
- Medea: Topic 7 (0.998)
- Octavia: Topic 6 (0.998)
- Oedipus: Topic 4 (0.999)
- Thyestes: Topic 1 (0.999)
- Hercules Oetaeus: Topic 7 (0.999)
- Ecerinis: Topic 7 (0.998)

## k=8 relevance keywords (lambda=0.6), new run

- Topic 1: mensa, compono, aspectus, obsto, abscondo, cibus, abnuo, orno, hospitium, intactus
- Topic 2: classis, nuntius, remeo, niueus, pudicus, memini, lacero, furtiuus, grates, nescius
- Topic 3: subiectus, iulius, puellaris, propago, servo, adimo, sollers, ambitio, ostento, tremulus
- Topic 4: bos, opimus, uinclum, cultus, classis, curuus, celo, bustum, torpeo, misereor
- Topic 5: exclamo, afflicto, ornus, gestio, quaesitor, ile, linea, adortus, incruentus, impietas
- Topic 6: princeps, subicio, constituo, suboles, consensus, extruo, uolucer, lacero, porto, incestus
- Topic 7: uoltus, uindico, uolucer, axis, inuado, colus, intendo, glacialis, ursa, rigidus
- Topic 8: conuexus, facultas, instigo, labes, saluo, abscisus, intonsus, inspiro, strepitus, procrustes
