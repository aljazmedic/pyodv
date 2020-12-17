from funkcija import Funkcija
from util import minterm_v_niz
from tabela import tabela
from from_latex import from_latex
from sim_funkcija import SimFunkcija
from quin import quin
from popolne_normalne import PDNO, PKNO
# begin-doc-include
from pylatex import Document, Section, Subsection, Command, Math, Tabular
from pylatex.basic import NewLine, LineBreak
from pylatex.utils import italic, NoEscape


if __name__ == '__main__':
	#f2 = Funkcija(mintermi=[0,1,2,3,6,7,8,10,11,13,14,15],n=4)
	#f2 = Funkcija("11001010")
	# f2 = Funkcija(mintermi=[2,3,4,5,9,10,11,12,13],n=4)
	#f2 = from_latex("1 \\lor x_2 \\implies ( x_3 \\lor x_4)",name="g")
	f2 = from_latex("\\overline{\\overline{x_1} \\overline{x_2}\\lor x_3 } ")
	#f2 = Funkcija(mintermi=[0,1,2,3,6,7,8,10,11,13,14,15], n=4, name="f")
	print("F2", f2)
	
	
