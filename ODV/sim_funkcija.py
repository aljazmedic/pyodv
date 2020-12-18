from funkcija import Funkcija
from typing import List, Optional
from pylatex import Document, Section, Subsection, Math
from pylatex.utils import NoEscape, escape_latex
from itertools import zip_longest
from util import minterm_v_niz

class SimFunkcija(Funkcija):
	def __init__(self, n:int, sim_stevila:List[int], neg:Optional[List[int]]=None, **kwargs):
		"""
		Paramteri:
		----------
		n : int
			Stevilo vhodnih spremenljivk

		sim_stevila : list[int]
			Simterijska števila funkcije
		
		neg : list[int]
			0-osnovni seznam negacij npr. [0] => ~x1 x2

		**kwargs : dict
			Argumenti za razred Funkcija
		"""
		if neg is None:neg="1"*n
		if isinstance(neg, str):
			neg_s = neg
		else:
			neg_s = ["1"]*n
			for ni in neg:
				neg_s[ni] = "0"
			neg_s = ''.join(neg_s)
		pravilnostni_vektor_sestevkov = [False]*(n+1)
		for sim_st in sim_stevila:
			if sim_st > n:
				raise Exception(f"Neveljavno simetrijsko število: {sim_st}")
			pravilnostni_vektor_sestevkov[sim_st] = True
		self.sim_stevila = sim_stevila
		
		mtrmi=[]
		
		for i in range(2**n):
			bits = minterm_v_niz(i,n=n)
			st_bitov = 0
			for b, neg_bit in zip_longest(bits, neg_s):

				if (neg_bit is None or neg_bit=="1") and b=="1":
					st_bitov+=1
				elif (neg_bit=="0") and b == "0":
					st_bitov+=1

			if pravilnostni_vektor_sestevkov[st_bitov]:
				mtrmi.append(i)
		kwargs.update({"mintermi":mtrmi})
		#print(kwargs)
		super(SimFunkcija, self).__init__(**kwargs)
	
	def __str__(self):
		inputs = ','.join(self.imena_spr)
		sim_simb = '{'+','.join(map(str,self.sim_stevila))+'}'
		return f"f{sim_simb}({inputs}): {self.pravilni_biti}"
		
	def tex(self)-> Math: 
		sim_simb = escape_latex('{'+','.join(map(str,self.sim_stevila))+'}')
		return super().tex(sim_simb)


if __name__=="__main__":
	f1 = Funkcija("1001",n=2)
	f2= SimFunkcija(2,[0,2])
	f2= SimFunkcija(4,[1,3],neg=[1,2],spremenljivke=["x_1", "x_2","x_3","g"])
	f3= SimFunkcija(4,[1,3])
	print(~f1,f2,f3,sep="\n")