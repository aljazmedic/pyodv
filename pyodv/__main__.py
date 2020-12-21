#from . import Funkcija, SimFunkcija, from_latex, quin, tabela,  pdno, pkno

from pyodv.function import Funkcija,SimFunkcija
from pyodv.latex import pdno, pkno, tabela
#from pyodv.function.funkcija import Funkcija
if __name__ == '__main__':
	# f2 = Funkcija(mintermi=[0,1,2,3,6,7,8,10,11,13,14,15],n=4)
	# f2 = Funkcija("11001010")
	# f2 = Funkcija(mintermi=[2,3,4,5,9,10,11,12,13],n=4)
	# f2 = from_latex("1 \\lor x_2 \\implies ( x_3 \\lor x_4)",name="g")
	# f2 = from_latex("\\overline{\\overline{x_1} \\overline{x_2}\\lor x_3 } ")
	# f2 = Funkcija(mintermi=[0,1,2,3,6,7,8,10,11,13,14,15], n=4, name="f")
	# print("F2", f2)

	f = SimFunkcija(4, [1,3], neg=[1, 2])                                 
	a = Funkcija(makstermi=[4,1], n=4) 
	b = Funkcija(mintermi=[0,5,7], n=4) 
	o= (~((f&a)|b))
	#print(o.table())
	pass
	
	
