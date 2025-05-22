# Compararea performanțelor Treap vs Splay Tree

Acest proiect compară două structuri de date echilibrate – **Treap** și **Splay Tree** – pe un set de operații dinamice de tip ABCE, măsurând timpii de execuție în diverse scenarii de lucru.

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

Fiecare fișier se generează astfel:
1. Calculăm cota absolută de linii pentru fiecare tip de operație (sumă = 750 000).  
2. Construim o listă cu codurile de operație în funcție de cote, o amestecăm, și apoi scriem pe fiecare linie:
