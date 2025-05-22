# Compararea performanțelor Treap vs Splay Tree

Acest proiect compară două structuri de date echilibrate – **Treap** și **Splay Tree** – pe un set de operații dinamice, măsurând timpii de execuție în diverse scenarii de lucru.

---

## Definiții

### Treap  
Un **Treap** este un arbore binar de căutare care, pe lângă cheia fiecărui nod, stochează și o _prioritate_ aleasă aleator. Invariantul BST se menține pe chei, iar heap-ul (max-heap sau min-heap) se menține pe priorități. La inserare și ștergere se folosesc rotații pentru a restaura proprietatea de heap, asigurând complexitate amortizată O(log n).

### Splay Tree  
Un **Splay Tree** este un arbore binar de căutare auto-aranjat. Orice acces (inserare, căutare, ștergere) “splay-aza” (aduce în rădăcină) nodul accesat folosind rotații zig, zig-zig sau zig-zag. Această auto-aranjare amortizează costul operațiilor la O(log n) per operație, pe secvențe lungi de accesuri.

---

## Operațiile testate

Cele şase operații ABCE (din Infoarena “abce”) implementate și măsurate sunt:

1. **Insert X** – Inserează cheia X în mulțime (fără duplicate).  
2. **Delete X** – Șterge cheia X dacă există.  
3. **Search X** – Returnează 1 dacă X există, altfel 0.  
4. **Predecessor(X)** – Afișează cel mai mare Y ≤ X.  
5. **Successor(X)** – Afișează cel mai mic Y ≥ X.  
6. **Range(X,Y)** – Afișează, în ordine crescătoare, toate cheile Z cu X ≤ Z ≤ Y.

---

## Cazurile de test

Generăm **7** fișiere de test, fiecare cu **Q = 1 000 000** operații și valori X,Y ∈ [−10⁹, 10⁹]:

| Nume fișier   |  Detalii                                                                                     |
|---------------|--------------------------------------------------------------------------------------------|  
| `heavy_op1.in`| 70 % tip 1 (insert), câte ≈ 6 % din celelalte 5 operații                                     |
| `heavy_op2.in` | 70 % tip 2 (delete), restul împărțit egal                                                  |
| `heavy_op3.in` | 70 % tip 3 (search), restul egal                                                            |
| `heavy_op4.in` | 70 % tip 4 (predecessor), restul egal                                                       |
| `heavy_op5.in` | 70 % tip 5 (successor), restul egal                                                         |
| `heavy_op6.in` | 70 % tip 6 (range query), restul egal                                                |
| `equal_mix.in` | Împărțire egală a celor 6 tipuri de operații                                                |

## Rezultate

Pentru fiecare dintre cele 7 categorii am generat 20 de instanțe diferite de teste și am rulat fiecare implementare de **20 de ori** pe fiecare fișier, obținând în total 140 de măsurători pentru Treap și 140 pentru Splay. În tabelul de mai jos sunt prezentate **valorile medii** ale timpilor de execuție (în milisecunde):

| Test           | Treap   | Splay   |
|----------------|--------:|--------:|
| heavy_op1      | 159 280 | 171 862 |
| heavy_op2      |   9 495 |  11 771 |
| heavy_op3      |   8 926 |   9 173 |
| heavy_op4      |   9 388 |   8 775 |
| heavy_op5      |   8 809 |   9 599 |
| heavy_op6      | 102 191 | 108 803 |
| equal_mix      |  72 825 |  82 373 |

## Interpretarea Datelor


#Operații de inserare 
- **Rezultat**: Treap 159 280 ms vs Splay 171 862 ms → **Treap ~7 % mai rapid**  
- **Explicație**:  
  - Inserarea într-un Treap se face printr-o simplă rotație pe baza priorității, în timp ce Splay Tree face un întreg șir de rotații „zig” pentru a aduce nodul inserat în rădăcină.  
  - Într-un scenariu cu predominanță de inserții, overhead-ul splay-urilor repetate se resimte mai puternic, iar Treap-ul se impune.


**Operații de ștergere, căutare, predecesor și succesor**  

- **Timpi medii**:  
  | Test       | Treap (ms) | Splay (ms) | Observație                       |
  |------------|-----------:|-----------:|---------------------------------|
  | delete     |      9 495 |     11 771 | Treap ~19 % mai rapid           |
  | search     |      8 926 |      9 173 | Performanțe comparabile         |
  | predecessor|      9 388 |      8 775 | **Splay ~6.5 % mai rapid**      |
  | successor  |      8 809 |      9 599 | Treap ~8.3 % mai rapid          |

- **Interpretări**:  
  - **Ștergere**: Treap folosește rotații bazate pe prioritate pentru a coborî nodul la o frunză, apoi îl elimină; Splay adaugă și un splay înainte de ștergere, ceea ce introduce cost suplimentar.  
  - **Căutare**: Splay plasează nodul găsit în rădăcină, dar acest splay adaugă un overhead mic; Treap rămâne la descădere simplă.  
  - **Predecesor**: Splay profită de aducerea la rădăcină a nodului „aproape căutat”, accelerând accesurile succesive în aceeași regiune, de aceea iese puțin în față.  
  - **Succesor**: Similar, însă implementarea Treap se dovedește ușor mai eficientă pentru succesor.

---

**Operații de interval** 
- **Rezultat**: Treap 102 191 ms vs Splay 108 803 ms → **Treap ~6 % mai rapid**  
- **Explicație**:  
  - O interogare de tip range costă O(k + log n), unde k = numărul de noduri din interval. Cu Q mare, k ajunge să domine costul.  
  - Ambele structuri fac o parcurgere inorder recursivă, dar Treap-ul, având o distribuție uniformă de priorități, păstrează un arbore mai echilibrat în medie, reducând ușor costul per vizită.

---

#Distribuție egală (`equal_mix.in`)

- **Rezultat**: Treap 72 825 ms vs Splay 82 373 ms → **Treap ~12 % mai rapid**  
- **Interpretare**:  
  - Într-un scenariu realist, cu mix echilibrat de operații, Treap-ul își arată robustețea și overhead-ul mai mic la rotații, în timp ce Splay plătește prețul restructurărilor agresive frecvente.

---

## Concluzii

- **Treap** domină în 5 din 7 scenarii, dovedind rotațiile bazate pe priorități mai rapide când insertările și range-query-urile sunt majoritare.  
- **Splay Tree** excelează la operațiile ce implică adaptarea ierarhiei de acces pe aceeași regiune (predecessor), grație mecanismului de splaying.  
- Alegerea optimă depinde de profilul aplicației:  
  - Pentru **workload-uri de inserții masive** sau **interogări de interval**, Treap-ul este recomandat.  
  - Pentru **scenario sequentiale sau acces repetat în regiuni înguste**, Splay Tree poate oferi avantaje de localitate amortizată.

