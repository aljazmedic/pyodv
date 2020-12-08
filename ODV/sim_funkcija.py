from funkcija import Funkcija
from typing import List, Optional
from pylatex import Document, Section, Subsection, Math
from pylatex.utils import NoEscape, escape_latex

class SimFunkcija(Funkcija):
	def __init__(self, n:int, sim_stevila:List[int], neg:Optional[List[int]]=None):
		
		pravilnostni_vektor_sestevkov = [False]*(n+1)
		for sim_st in sim_stevila:
			if sim_st > n:
				raise Exception(f"Neveljavno simetrijsko število: {sim_st}")
			pravilnostni_vektor_sestevkov[sim_st] = True
		self.sim_stevila = sim_stevila
		pravilni_biti=list("0"*(2**n))
		for i in range(len(pravilni_biti)):
			bits = list(bin(i)[2:])
			n_bits = []
			for b, n in zip(bits, neg):
				if n=="0":
					if b == "1": n_bits.append("0")
					elif b == "0": n_bits.append("1")
				else:
					n_bits.append(b)

			s_bits = sum(map(int, n_bits))

			if pravilnostni_vektor_sestevkov[s_bits]:
				pravilni_biti[i]="1"
		pravilni_biti = "".join(pravilni_biti)
		super(SimFunkcija, self).__init__(pravilni_biti)
	
	def __str__(self):
		inputs = ','.join(["x_{%d}"%n for n in range(1, self.st_spremenljivk+1,1)])
		sim_simb = '{'+','.join(map(str,self.sim_stevila))+'}'
		return f"f{sim_simb}({inputs}): {self.pravilni_biti}"
		
	def tex(self)-> Math: 
		sim_simb = escape_latex('{'+','.join(map(str,self.sim_stevila))+'}')
		return super().tex(sim_simb)


if __name__=="__main__":
	f1 = Funkcija("1001",n=2)
	f2= SimFunkcija(2,[0,2])
	print(f1,"\n",f2)
	f1.table()
	f2.table()
	print(f1.pravilni_biti)
	print(f2.pravilni_biti)
	print(f1==f2)
	print(f2==2)