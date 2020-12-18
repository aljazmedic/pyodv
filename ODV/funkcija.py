import numpy as np
from typing import List
from util import minterm_v_niz
from pylatex import Document, Section, Subsection, Math
from pylatex.utils import NoEscape
import re

class Funkcija:
	# pravilne bite
	# minterme
	def __init__(self, pravilni_biti:str=None, mintermi:List[int]=None, makstermi:List[int]=None, n=0,spremenljivke=None,name="f"):
		"""
		Paramteri:
		----------
		pravilni_biti : str
			Pravilni biti funkcije, ekskluziven z makstermi in mintermi

		mintermi : list[int]
			Mintermi funkcije, ekskluziven z makstermi in pravilnimi_biti
		
		makstermi : list[int]
			Makstermi funkcije, ekskluziven z mintermi in pravilnimi_biti
		
		n : int (Opcijsko)
			število vhodnih spremenljivk, dobljeno iz prvih argumentov

		spremenljivke : iter[str] (Opcijsko)
			imena spremenljivk funkcije
		
		name : str (Opcijsko)
			ime funkcije
		"""
		mtn = mintermi is not None
		pbn = pravilni_biti is not None
		mkstn = makstermi is not None
		if mtn + pbn + mkstn != 1:
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
		elif mkstn:
			self.makstermi = makstermi
			max_term = max(makstermi)+1
			self.st_spremenljivk = max(np.ceil(np.log2(max_term)).astype(np.int32), n)
			self.pravilni_biti = ["1"]*(2**self.st_spremenljivk)
			for mtm in self.makstermi:
				self.pravilni_biti[2**self.st_spremenljivk-mtm-1] = "0"
			self.pravilni_biti = "".join(self.pravilni_biti)
			self.mintermi=[]
			for i, e in enumerate(self.pravilni_biti):
				if e == "1":
					self.mintermi.append(i)
		elif mtn:
			self.mintermi = mintermi
			max_term = max(mintermi)+1
			self.st_spremenljivk = max(np.ceil(np.log2(max_term)).astype(np.int32), n)
			self.pravilni_biti = ["0"]*(2**self.st_spremenljivk)
			for mtm in self.mintermi:
				self.pravilni_biti[mtm] = "1"
			self.pravilni_biti = "".join(self.pravilni_biti)
			self.makstermi=[]
			for i, e in enumerate(self.pravilni_biti):
				if e == "0":
					self.makstermi.append(2**self.st_spremenljivk-i-1)
		self.n = self.st_spremenljivk
		##Imena, spremenljivke
		self.name=name
		x = lambda n: NoEscape(f"x_{n}")
		if not spremenljivke:
			self.imena_spr = [x(i+1) for i in range(self.n)]
		else:
			self.imena_spr =[]
			for s in spremenljivke[:self.n]:
				 self.imena_spr.append(s if isinstance(s, NoEscape) else NoEscape(s))


	def __str__(self):
		inputs = ','.join(self.imena_spr)
		return f"{self.name}({inputs}): {self.pravilni_biti}"

	def __eq__(self, value):
		if type(value) != Funkcija:
			return False
		return self.pravilni_biti == value.pravilni_biti# all([x==y for x, y in zip(self.mintermi, value.mintermi)])
	
	def __or__(self,other):
		if other == 0:
			return Funkcija(mintermi=self.mintermi.copy(), n=self.n, spremenljivke=self.imena_spr,name=self.name)
		elif other == 1:
			return Funkcija(pravilni_biti="1",n=0)
		elif type(other) != Funkcija:
			raise Exception("Not a Function: "+ str(other))
		spr, (spr_f1, spr_f2) = get_overlapping_inputs(self,other)
		p_biti = ""
		new_fn_n = len(spr)
		for trm in range(2**(new_fn_n)):
			mtm = minterm_v_niz(trm,n=new_fn_n)
			b_f1 = int(spr_f1(self.pravilni_biti,mtm))
			b_f2 = int(spr_f2(other.pravilni_biti,mtm))
			p_biti+= "1" if (b_f1 | b_f2) else "0"
		return Funkcija(p_biti,spremenljivke=spr,n=new_fn_n)

	def __add__(self,other):
		return self.__or__(other)

	def __and__(self, other):
		if other == 0:
			return Funkcija(pravilni_biti="0",n=0)
		elif other == 1:
			return Funkcija(mintermi=self.mintermi.copy(), n=self.n, spremenljivke=self.imena_spr,name=self.name)
		elif type(other) != Funkcija:
			raise Exception("Not a Function: "+ str(other))
		spr, (spr_f1, spr_f2) = get_overlapping_inputs(self,other)
		p_biti = ""
		new_fn_n = len(spr)
		for trm in range(2**(new_fn_n)):
			mtm = minterm_v_niz(trm,n=new_fn_n)
			b_f1 = int(spr_f1(self.pravilni_biti,mtm))
			b_f2 = int(spr_f2(other.pravilni_biti,mtm))
			p_biti+= "1" if (b_f1 & b_f2) else "0"
		return Funkcija(p_biti,spremenljivke=spr,n=new_fn_n)

	def __mul__(self, other):
		return self.__and__(other)

	def __invert__(self):
		prav = ''.join(["0" if x == "1" else "1" for x in self.pravilni_biti])
		return Funkcija(prav,n=self.n,spremenljivke=self.imena_spr,name=self.name)
	
	def __neg__(self):
		return self.__invert__()	

	def tex(self, fn_index=None)-> NoEscape: 
		inputs = ','.join(self.imena_spr)
		#print(inputs)
		if fn_index is not None:
			fn_index="_{"+fn_index+"}"
		else:
			fn_index= ""
		return NoEscape(self.name+fn_index+NoEscape(f"({inputs})"))
	
	def sort(self,order=None):
		o, (fn,) = get_overlapping_inputs(self,inputs=order)
		pb = ''.join(
			[fn(self.pravilni_biti, minterm_v_niz(i,n=self.n)) for i in range(2**self.n) ]
			)
		return Funkcija(pb,spremenljivke=o,n=self.n)

	def table(self,order=None):
		if order is not None:
			return self.sort(order).table()
		
		widths = [len(n) for n in self.imena_spr]
		headers = ' '.join(self.imena_spr)
		print(headers,self.name,sep=" | ")
		for mtrm, vr in enumerate(self.pravilni_biti):
			niz = minterm_v_niz(mtrm,n=self.n)
			print(" ".join([("{: >%s}"%w).format(b) for w, b in zip(widths, niz)]),vr,sep=" | ")
			
def fn_for(poi):
	_poi = poi.copy()
	def fn(biti, skupni_term_in):
		v_tej_f = int(''.join([skupni_term_in[i] for i in _poi]),2)
		return biti[v_tej_f]
	return fn

def get_overlapping_inputs(*functions:List[Funkcija], inputs=None):
	if inputs ==None:
		inputs = set()
		for f in functions:
			[inputs.add(ime) for ime in f.imena_spr]
		o = list(sorted(inputs))
	else:
		for f in functions:
			if any([ime not in inputs for ime in f.imena_spr]):
				raise Exception("Missing some of the names "+str(f.imena_spr))
		o = inputs
	consec_fn = []
	for f in functions:
		poi = [o.index(ime) for ime in f.imena_spr]
		consec_fn.append(fn_for(poi))
	return tuple(o), consec_fn


if __name__ == '__main__':
	f1 = Funkcija("0111")
	f2 = Funkcija("0010",spremenljivke=[NoEscape("x_2"),NoEscape("x_3"), ])
	print(f1)
	print(f2)
	print(f1&f2)
	f1.table()
	print(-f2.sort())

