from ..function import Funkcija, SimFunkcija, from_latex
from ..util import minterm_v_niz
from ..latex import tabela, pdno, pkno
from ..quin import quin

from pylatex import Document, Section, Subsection, Command, Math, Tabular
from pylatex.basic import NewLine, LineBreak
from pylatex.utils import italic, NoEscape


if __name__ == '__main__':
	#f2 = Funkcija(mintermi=[0,1,2,3,6,7,8,10,11,13,14,15],n=4)
	#f2 = Funkcija("11001010")
	# f2 = Funkcija(mintermi=[2,3,4,5,9,10,11,12,13],n=4)
	#f2 = from_latex("1 \\lor x_2 \\implies ( x_3 \\lor x_4)",name="g")
	#f2 = from_latex("\\overline{\\overline{x_1} \\overline{x_2}\\lor x_3 } ")
	#f2 = Funkcija(mintermi=[0,1,2,3,6,7,8,10,11,13,14,15], n=4, name="f")
	f2 = Funkcija(mintermi=[3, 6, 9, 10, 11, 12, 14, 15],spremenljivke=['x_1', 'x_2', 'x_3', 'q'])
	print("F2", f2)
	qf2_tex, q2_vseb, q2_cena, (mdno_tex, mkno_tex) = quin(f2)
	print("q2 vseb", q2_vseb)
	
	d = Document('basic')
	with d.create(Section('Section no. 1')):
		d.append("Funkcija f")
		d.append(NewLine())
		d.append(NewLine())

		d.append(pdno(f2))
		d.append(NewLine())
		d.append(NewLine())

		d.append(pkno(f2))
		d.append(NewLine())
		d.append(NewLine())

		d.append(tabela(f2))
		d.append(NewLine())
		
		d.append(mdno_tex)
		d.append(NewLine())
		
		d.append(mkno_tex)
		d.append(NewLine())

		d.append(qf2_tex)
		d.append(NewLine())

	d.generate_pdf(clean_tex=False)
	#d.generate_tex()

