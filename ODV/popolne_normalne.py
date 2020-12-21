import numpy as np
from funkcija import Funkcija
from typing import List,Tuple
from util import minterm_v_niz, nanesi_bite
from pylatex import Document, Section, Subsection, Math, FootnoteText
from pylatex.utils import NoEscape
from pprint import PrettyPrinter


def PDNO(self:Funkcija,vrni_ceno=False)->NoEscape:
    """
    Vrne Popolno disjunktivno normalno obliko funkcije v LaTeX notaciji

    fn:Funkcija
        Funkcija

    vrni_ceno boolean (Optional)
        Vrne ceno v obliki (<st_komponent>, <st_povezav>)
    """
    pdno_tex, cena = nanesi_bite(self.st_spremenljivk,
        termi_maske=self.mintermi,
        pn=('0','1'),
        using=('\lor',''),
        vrni_ceno=True)
    pdno_tex = NoEscape(self.tex(fn_index="PDNO")+"="+pdno_tex)
    if vrni_ceno:
        return pdno_tex, cena
    return pdno_tex

def PKNO(self:Funkcija,vrni_ceno=False)->NoEscape:
    """
    Vrne Popolno konjunktivno normalno obliko funkcije v LaTeX notaciji

    fn:Funkcija
        Funkcija

    vrni_ceno boolean (Optional)
        Vrne ceno v obliki (<st_komponent>, <st_povezav>)
    """
    n = self.st_spremenljivk
    pkno_tex, cena =  nanesi_bite(n,
        termi_maske=self.makstermi,
        pn=('0','1'),
        using=('','\lor'),
        vrni_ceno=True,
        wrap_inner=True)
    pkno_tex = NoEscape(self.tex(fn_index="PKNO")+"="+pkno_tex)
    if vrni_ceno:
        return pkno_tex, cena
    return pkno_tex

if __name__ == "__main__":
    f = Funkcija("10011010")
    print(f)
    print(*PDNO(f,True))
    print(*PKNO(f,True))