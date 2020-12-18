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
