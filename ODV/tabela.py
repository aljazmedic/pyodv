import numpy as np
from typing import List
from util import minterm_v_niz
from funkcija import Funkcija
from pylatex import Document, Section, Subsection, Math, Tabular
from pylatex.utils import NoEscape

def tabela(self:Funkcija) -> NoEscape:
    x = lambda n: NoEscape(f"x_{n}")

    pravilnostna_tabela = Tabular('|'.join('c'*(self.st_spremenljivk+1)))
    pravilnostna_tabela.add_row(list(map(x, range(1,1+self.st_spremenljivk)))+[self.tex()])
    pravilnostna_tabela.add_hline()
    for minterm, vrednost in zip(range(2**self.st_spremenljivk),self.pravilni_biti):
        niz_vhodnih_bitov = minterm_v_niz(minterm, self.st_spremenljivk)
        pravilnostna_tabela.add_row(list(niz_vhodnih_bitov)+[vrednost])
    return pravilnostna_tabela

if __name__ == "__main__":
    f = Funkcija("1010")
    print(tabela(f))