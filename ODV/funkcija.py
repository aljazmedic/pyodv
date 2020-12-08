import numpy as np
from typing import List
from util import minterm_v_niz
from pylatex import Document, Section, Subsection, Math
from pylatex.utils import NoEscape
import re


class Funkcija:
	# pravilne bite
	# minterme
	def __init__(self, pravilni_biti:str=None, mintermi:List[int]=None,n=0,spremenljivke=None,name="f"):
		mtn = mintermi is not None
		pbn = pravilni_biti is not None
		if not mtn^pbn:
			raise Exception("Nepravilna uporaba konstruktorja!")
		elif pbn:
			self.pravilni_biti = pravilni_biti
			self.st_spremenljivk = max(np.log2(len(pravilni_biti)).astype(np.int32),n)
			if self.st_spremenljivk%1 != 0:
				raise Exception(f"Nepravilno stevilo bitov: {len(pravilni_biti)}")

			self.mintermi=[]
			self.makstermi=[]
			for i, e in enumerate(pravilni_biti):
				if e == "1":
					self.mintermi.append(i)
				elif e == "0":
					self.makstermi.append(2**self.st_spremenljivk - i-1)
				else:
					raise Exception(f"Nepravilno zap. bitov: {mintermi}")
				
		elif mtn:
			self.mintermi = mintermi
			max_term = max(mintermi)+1
			self.st_spremenljivk = max(np.ceil(np.log2(max_term)).astype(np.int32), n)
			self.pravilni_biti = ["0"]*(2**self.st_spremenljivk)
			for n in self.mintermi:
				self.pravilni_biti[n] = "1"
			self.pravilni_biti = "".join(self.pravilni_biti)
			self.makstermi=[]
			for i, e in enumerate(self.pravilni_biti):
				if e == "0":
					self.makstermi.append(2**self.st_spremenljivk-i-1)
		
		##Imena, spremenljivke
		self.name=name
		x = lambda n: NoEscape(f"x_{n}")
		if not spremenljivke:
			self.imena_spr = [x(i+1) for i in range(n)]
		else:
			self.imena_spr = spremenljivke[:self.st_spremenljivk]
		


	def __str__(self):
		inputs = ','.join([f"x_{n}" for n in range(1, self.st_spremenljivk+1,1)])
		return f"{self.name}({inputs}): {self.pravilni_biti}"

	def __eq__(self, value):
		if type(value) != Funkcija:
			return False
		return self.pravilni_biti == value.pravilni_biti# all([x==y for x, y in zip(self.mintermi, value.mintermi)])
	
	def tex(self, fn_index=None)-> NoEscape: 
		inputs = ','.join(self.imena_spr)
		#print(inputs)
		if fn_index is not None:
			fn_index="_{"+fn_index+"}"
		else:
			fn_index= ""
		return NoEscape(self.name+fn_index+NoEscape(f"({inputs})"))



if __name__ == '__main__':
	f1 = Funkcija("0111")
	""" print(f1)
	f1.table()
	print(f1)
	print(f1.mintermi)
	print(f1.makstermi)
	print(f1.tex())
	"""