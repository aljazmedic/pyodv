# pyodv
Paket za interakcijo s pravilnistnimi funkcijami, napisan v pythonu. Omogoča zapis ali pa zajetje funkcije iz LaTeX-a, prikaz pravilnistne tabele in minimizacije s Quinovo metodo.

### Namestitev
- (Opcijsko) Ustvarimo virtualno okolje za projekt in ga aktiviramo
  ```bash
  python -m venv venv
  source venv/Scripts/activate
  ```

### Pretvornik iz LaTeX v pdf:
#### Windows
Potrebno je namestiti texlive ali pa MikTex 
#### Linux
```bash
sudo apt-get install texlive-pictures texlive-science texlive-latex-extra latexmk
```

- Potrebno je namestiti knjižnice, ki se nahajajo v datoteki `requirements.txt`. To naredimo z ukazom

  ```bash
  python -m pip install --update pip
  python -m pip install -r requirements.txt
  ```
### Uporaba

### `Funkcija(pravilni_biti, mintermi, makstermi, n=0, spremenljivke=None, name='f')`
 |      Paramteri:
 |      ----------
 |      pravilni_biti : **str**  Pravilni biti funkcije, ekskluziven z `makstermi` in `mintermi`
 |      mintermi : **list[int]** Mintermi funkcije, ekskluziven z `makstermi` in `pravilnimi_biti`
 |      makstermi : **list[int]** Makstermi funkcije, ekskluziven z `mintermi` in `pravilnimi_biti`
 |      n : **int** (Opcijsko) Stevilo vhodnih spremenljivk, dobljeno iz prvih argumentov
 |      spremenljivke : **iter[str]** (Opcijsko *[x_1, x_2, ...]*)  Imena spremenljivk funkcije
 |      name : **str** (Opcijsko *[f]*) Ime funkcije
 | 

|      Metode:
 |      -----------
 | `sort(order=None)` Vrne kopijo funkcije z drugačnim vrstnim redom spremenljivk
 | `table(order=None)` Izpiše pravilnostno tabelo v terminal
 | 



### `SimFunkcija(n, sim_stevila, neg=[], **kwargs)`

|      Paramteri:
 |      ----------
 |      n : **int** Stevilo vhodnih spremenljivk
 |      sim_stevila : **list[int]** Simterijska Stevila funkcije
 |      neg : **list[int]** (Opcijsko []) 0-based npr. [0] => ~x1 x2
 |      \*\*kwargs : **dict**  argumenti za razred Funkcija
 | 

```python
f = Funkcija("10010101")
# funkcija treh spremenljivk

f = Funkcija(mintermi=[1,2])
# funckija dveh spremenljivk, vrednosti "0110"

f = from_latex("\overline{x_1} \land \overline{x_2})")
#funkcija dveh spremenljivk, vrednosti "1110"
```

### Uporaba v interpreterju

Pričnemo z ukazom `python -i ODV`, s čimer označimo interaktivni način, kjer bomo lahko uporabljali vse razrede in funkcije modula. (Tudi `IPython -i ODV`)
