import numpy as np
from ..util import minterm_v_niz
from ..function import Funkcija
from pylatex import Document, Section, Subsection, Math, Tabular
from pylatex.utils import NoEscape

from typing import List

def tabela(self:Funkcija) -> NoEscape:
    """
    Vrni tabelo v LaTeX jeziku
    
    fn:Funkcija
        Funkcija
    """
    pravilnostna_tabela = Tabular('|'.join('c'*(self.n+1)))
    pravilnostna_tabela.add_row(list(self.imena_spr)+[self.tex()])
    pravilnostna_tabela.add_hline()
    if self.n == 0:
        pravilnostna_tabela.add_row(self.pravilni_biti)
        return pravilnostna_tabela
    for minterm, vrednost in zip(range(2**self.n),self.pravilni_biti):
        niz_vhodnih_bitov = minterm_v_niz(minterm, self.n)
        pravilnostna_tabela.add_row(list(niz_vhodnih_bitov) +[vrednost])
    return pravilnostna_tabela

if __name__ == "__main__":
    f = Funkcija("1010")
    print(tabela(f))