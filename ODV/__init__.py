from funkcija import Funkcija
from util import minterm_v_niz
from tabela import tabela
from sim_funkcija import SimFunkcija
from quin import quin
from popolne_normalne import PDNO, PKNO
# begin-doc-include
from pylatex import Document, Section, Subsection, Command, Math, Tabular
from pylatex.basic import NewLine, LineBreak
from pylatex.utils import italic, NoEscape


if __name__ == '__main__':
	f2 = Funkcija(mintermi=[0,1,2,3,6,7,8,10,11,13,14,15],n=4)
	#f2 = Funkcija(mintermi=[2,3,4,5,9,10,11,12,13],n=4)
	print(f2)
	qf2_tex, q2_vseb, q2_cena, (mdno_tex, mkno_tex) = quin(f2)
	print(q2_vseb)

	d = Document('basic')
	with d.create(Section('Section no. 1')):
		d.append("Funkcija f")
		d.append(NewLine())
		d.append(NewLine())

		d.append(PDNO(f2))
		d.append(NewLine())
		d.append(NewLine())

		d.append(PKNO(f2))
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

