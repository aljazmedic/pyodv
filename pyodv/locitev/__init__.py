from ..util import minterm_v_niz
from ..function import Funkcija
from pylatex.utils import NoEscape
from pprint import PrettyPrinter
from collections import defaultdict

from typing import List

pp = PrettyPrinter(indent=4)
def _loci_po(self:Funkcija, zap:int):
    ret = defaultdict(str)
    lx = ["X"]*self.n
    lx[zap] = "%s"
    L_X = "".join(lx)
    def izp(n):
        return L_X%n

    for i, vred in enumerate(self.pravilni_biti):
        zap_bitov = list(minterm_v_niz(i,self.n))
        izp_bit = zap_bitov.pop(zap)
        ret[izp(izp_bit)]+=vred
        #ret.append((''.join([ta_vr]+l),vred))
    pp.pprint(dict(ret))
    return dict(ret)

def locitev(self:Funkcija):
    for i in range(self.n):
        _loci_po(self,i)

if __name__ == "__main__":
    f = Funkcija(mintermi=[0,1,2,3,6,7,8,10,11,13,14,15],n=4)
    print(f)
    locitev(f)
    
    f2 = Funkcija('11001001',name="f_{3=0}")
    print(f2)
    locitev(f2)

    f3= Funkcija('0001',name="f_{3=0,2=1}")
    print(f3)
    locitev(f3)
    