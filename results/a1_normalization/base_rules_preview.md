# A1 preview: fixed rules only (lowercase, v->u, j->i)

Counts are over the tokens the preprocessing keeps (content POS, stopwords removed), before named-entity removal. The variant map is not applied yet.

| play             |   tokens |   tokens_changed |   pct_tokens_changed |   types |   types_changed |   types_after |   newly_stopwords |   newly_named_entities |
|:-----------------|---------:|-----------------:|---------------------:|--------:|----------------:|--------------:|------------------:|-----------------------:|
| Phoenissae       |     2548 |               19 |                  0.7 |    1130 |              17 |          1124 |                 0 |                      7 |
| Troades          |     4502 |               50 |                  1.1 |    1657 |              38 |          1642 |                 1 |                     19 |
| Phaedra          |     5065 |               53 |                  1   |    1995 |              42 |          1980 |                 2 |                     12 |
| Agamemnon        |     3918 |               32 |                  0.8 |    1689 |              27 |          1685 |                 0 |                     14 |
| Hercules Furens  |     5314 |               53 |                  1   |    1891 |              44 |          1877 |                 2 |                     10 |
| Medea            |     3784 |               28 |                  0.7 |    1611 |              25 |          1603 |                 2 |                     10 |
| Octavia          |     3526 |               36 |                  1   |    1194 |              24 |          1186 |                 2 |                     12 |
| Oedipus          |     4197 |               41 |                  1   |    1763 |              30 |          1750 |                 4 |                     11 |
| Thyestes         |     4094 |               33 |                  0.8 |    1687 |              31 |          1678 |                 0 |                      5 |
| Hercules Oetaeus |     7280 |               43 |                  0.6 |    1951 |              23 |          1938 |                 3 |                     20 |
| Ecerinis         |     2330 |               27 |                  1.2 |    1256 |              22 |          1251 |                 0 |                      2 |

- Types that merge under v->u / j->i: 78 groups

  - achiuus: achiuus (1), achivus (1)
  - adiuuo: adiuuo (7), adiuvo (1)
  - aduena: aduena (2), advena (1)
  - aestiuus: aestiuus (2), aestivus (1)
  - argiuus: argiuus (5), argivus (1)
  - auarus: auarus (2), avarus (2)
  - aueho: aueho (4), aveho (1)
  - auernus: auernus (1), avernus (1)
  - auerto: auerto (7), averto (2)
  - auidus: auidus (21), avidus (15)
  - auis: auis (12), avis (3)
  - auius: auius (1), avius (2)
  - caueo: caueo (1), caveo (1)
  - cauus: cauus (3), cavus (3)
  - ciuilis: ciuilis (2), civilis (3)
  - conuerto: conuerto (9), converto (1)
  - curuo: curuo (3), curvo (1)
  - curuus: curuus (8), curvus (1)
  - deuinco: deuinco (4), devinco (1)
  - diuus: diuus (23), divus (1)
  - euello: euello (2), evello (1)
  - euerto: euerto (6), everto (4)
  - feruidus: feruidus (11), fervidus (2)
  - grauo: grauo (12), gravo (1)
  - inuado: inuado (12), invado (2)
  - inuenio: inuenio (18), invenio (6)
  - inuictus: inuictus (9), invictus (1)
  - inuiso: inuiso (5), inviso (1)
  - inuius: inuius (6), invius (1)
  - iuuenilis: iuuenilis (1), iuvenilis (2)
  - iuuenis: iuuenis (27), iuvenis (3)
  - iuuentus: iuuentus (5), iuventus (1)
  - iuuo: iuuo (33), iuvo (4)
  - laeuus: laeuus (5), laevus (11)
  - niueus: niueus (6), niveus (6)
  - niuosus: niuosus (1), nivosus (3)
  - nouerca: nouerca (33), noverca (8)
  - nouus: nouus (82), novus (6)
  - obuius: obuius (12), obvius (4)
  - paruulus: paruulus (3), parvulus (4)
  - paruus: paruus (31), parvus (2)
  - pauidus: pauidus (18), pavidus (6)
  - peruius: peruius (7), pervius (2)
  - prouoco: prouoco (1), provoco (1)
  - releuo: releuo (4), relevo (2)
  - renouo: renouo (2), renovo (2)
  - reuello: reuello (6), revello (1)
  - riuus: riuus (3), rivus (1)
  - saeue: saeue (1), saeve (3)
  - saeuus: saeuus (114), saevus (10)
  - saluo: saluo (2), salvo (1)
  - seruo: seruo (31), servo (2)
  - soluo: soluo (50), solvo (3)
  - toruus: toruus (16), torvus (2)
  - uagus: uagus (34), vagus (8)
  - uanus: uanus (17), vanus (3)
  - uarius: uarius (10), varius (6)
  - uastus: uastus (40), vastus (9)
  - uena: uena (10), vena (2)
  - uenio: uenio (99), venio (1)
  - uenus: uenus (15), venus (11)
  - uerso: uerso (13), verso (1)
  - uersum: uersum (1), versum (1)
  - uerto: uerto (29), verto (3)
  - uerus: uerus (31), verus (1)
  - uinco: uinco (129), vinco (8)
  - uireo: uireo (8), vireo (1)
  - uirgo: uirgo (48), virgo (2)
  - uiuo: uiuo (40), uivo (1)
  - uiuus: uiuus (2), uivus (1), viuus (7)
  - ulixes: ulixes (1), vlixes (9)
  - ulixus: ulixus (1), vlixus (1)
  - uoco: uoco (70), voco (1)
  - uoluo: uoluo (13), uolvo (2)
  - uotum: uotum (50), votum (12)
  - urbs: urbs (66), vrbs (1)
  - uulgaris: uulgaris (1), vulgaris (1)
  - uulnus: uulnus (47), vulnus (2)

- Tokens that become stopwords only after normalization (the original stopword list was spelled differently): tenuis (16)

- Tokens that become named entities only after normalization: uirgo (48), iuuenis (27), avidus (15), saevus (10), vinco (8), vagus (8), solvo (3), verso (1), venio (1), iuuenilis (1)
