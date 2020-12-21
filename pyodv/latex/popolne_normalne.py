from ..function import Funkcija
from ..util import minterm_v_niz, nanesi_bite
from pylatex import Document, Section, Subsection, Math, FootnoteText
from pylatex.utils import NoEscape

from typing import List,Tuple,Union,Optional

def pdno(self:Funkcija,vrni_ceno=False)->NoEscape:
    """Vrne Popolno disjunktivno normalno obliko funkcije v LaTeX notaciji

    Parameters
    ----------
    fn : Funkcija
        funkcija, katere PDNO želimo dobiti

    vrni_ceno boolean, optional
        Vrne ceno v obliki (<st_komponent>, <st_povezav>)
    
    Returns
    -------
    NoEscape
        LaTeX notacijo pdno
    (int,int), optional
        Ceno, le v primeru, da je vrni_ceno True
    """
    pdno_tex, cena = nanesi_bite(self.n,
        termi_maske=self.mintermi,
        pn=('0','1'),
        using=('\lor',''),
        vrni_ceno=True)
    pdno_tex = NoEscape(self.tex(fn_index="PDNO")+"="+pdno_tex)
    if vrni_ceno:
        return pdno_tex, cena
    return pdno_tex

def pkno(self:Funkcija,vrni_ceno=False)->Union[NoEscape, Tuple[NoEscape,Tuple[int,int]]]:
    """Vrne Popolno konjunktivno normalno obliko funkcije v LaTeX notaciji

    Parameters
    ----------
    fn : Funkcija
        funkcija, katere PKNO želimo dobiti

    vrni_ceno boolean, optional
        Vrne ceno v obliki (<st_komponent>, <st_povezav>)
    
    Returns
    -------
    NoEscape
        LaTeX notacijo PKNO
    (int,int), optional
        Ceno, le v primeru, da je vrni_ceno True
    """
    n = self.n
    pkno_tex, cena =  nanesi_bite(n,
        termi_maske=self.makstermi,
        pn=('0','1'),
        using=('','\lor'),
        vrni_ceno=True,
        wrap_inner=True)
    pkno_tex = NoEscape(self.tex(fn_index="pkno")+"="+pkno_tex)
    if vrni_ceno:
        return pkno_tex, cena
    return pkno_tex

if __name__ == "__main__":
    f = Funkcija("10011010")
    print(f)
    print(*pdno(f,True))
    print(*pkno(f,True))