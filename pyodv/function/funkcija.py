import numpy as np
from ..util import minterm_v_niz, provide_no_escape
from pylatex.utils import NoEscape
from varname import varname
from typing import List, Optional, Union


class Funkcija:
	"""
	Attributes
	----------
	pravilni_biti : str
		Niz pravilnih bitov po pravilnostni tabeli
	
	mintermi : list of int
		Mintermi funkcije
	
	makstermi : list of int
		Makstermi funkcije
	
	n : int
		Stevilo vhodnih spremenljivk funkcije
	
	imena_spr : list of NoEscape
		Imena vhodnih spremenljivk
	
	name : NoEscape
		Ime funkcije

	Examples
	--------
	>>> f1 = Funkcija("0111")
	>>> print(f1.table())
	x_1 x_2 | f
	  0   0 | 0
	  0   1 | 1
	  1   0 | 1
	  1   1 | 1

	>>> f2 = Funkcija(mintermi=[3])
	>>> print(f2.table())
	x_1 x_2 | f
	  0   0 | 0
	  0   1 | 0
	  1   0 | 0
	  1   1 | 1

	>>> f3 = f & ~f2
	>>> print(f3.table())
	x_1 x_2 | f
	  0   0 | 0
	  0   1 | 1
	  1   0 | 1
	  1   1 | 0
	"""

	def __init__(self, pravilni_biti:str=None, mintermi:List[int]=None, makstermi:List[int]=None, n=0,spremenljivke=None,name=None):
		"""
		Parameters
		----------
		pravilni_biti : str
			Pravilni biti funkcije, ekskluziven z makstermi in mintermi

		mintermi : list of int
			Mintermi funkcije, ekskluziven z makstermi in pravilnimi_biti
		
		makstermi : list of int
			Makstermi funkcije, ekskluziven z mintermi in pravilnimi_biti
		
		n : int, optional
			Stevilo vhodnih spremenljivk, dobljeno iz prvih argumentov

		spremenljivke : iterable object, optional
			Imena spremenljivk funkcije. Privzeto:  [x_1, x_2, ...]
		
		name : str, optional
			Ime funkcije. Privzeto "f"
		
		"""
		mtn = mintermi is not None
		pbn = pravilni_biti is not None
		mkstn = makstermi is not None
		if mtn + pbn + mkstn != 1:
			raise Exception("Nepravilna uporaba konstruktorja!")
		
		if spremenljivke is None:
			spremenljivke = []
		if pbn:
			self.n = max(
				np.ceil(np.log2(len(pravilni_biti))).astype(np.int32),
				n,
				len(spremenljivke))

			self.pravilni_biti = ("{:0>%s}"%(2**self.n)).format(pravilni_biti)
			if self.n%1 != 0:
				raise Exception(f"Nepravilno stevilo bitov: {len(pravilni_biti)}")

			self.mintermi=[]
			self.makstermi=[]
			for i, e in enumerate(pravilni_biti):
				if e == "1":
					self.mintermi.append(i)
				elif e == "0":
					self.makstermi.append(2**self.n - i-1)
				else:
					raise Exception(f"Nepravilno zap. bitov: {mintermi}")
		elif mkstn:
			self.makstermi = makstermi
			max_term = max(makstermi)+1
			self.n = max(
				np.ceil(np.log2(max_term)).astype(np.int32),
				n,
				len(spremenljivke))
			self.pravilni_biti = ["1"]*(2**self.n)
			for mtm in self.makstermi:
				self.pravilni_biti[2**self.n-mtm-1] = "0"
			self.pravilni_biti = "".join(self.pravilni_biti)
			self.mintermi=[]
			for i, e in enumerate(self.pravilni_biti):
				if e == "1":
					self.mintermi.append(i)
		elif mtn:
			self.mintermi = mintermi
			max_term = max(mintermi)+1
			self.n = max(
				np.ceil(np.log2(max_term)).astype(np.int32),
				n,
				len(spremenljivke))
			self.pravilni_biti = ["0"]*(2**self.n)
			for mtm in self.mintermi:
				self.pravilni_biti[mtm] = "1"
			self.pravilni_biti = "".join(self.pravilni_biti)
			self.makstermi=[]
			for i, e in enumerate(self.pravilni_biti):
				if e == "0":
					self.makstermi.append(2**self.n-i-1)
				##Imena, spremenljivke
		if name is None:
			name = varname(raise_exc=False) or 'f'
		self.name=name
		x = lambda n: NoEscape(f"x_{n}")
		if not spremenljivke:
			self.imena_spr = [x(i+1) for i in range(self.n)]
		else:
			self.imena_spr = provide_no_escape(*spremenljivke[:self.n])

	def __str__(self):
		inputs = ','.join(self.imena_spr)
		return f"{self.name}({inputs}): {self.pravilni_biti}"

	def __eq__(self, value):
		if type(value) != Funkcija:
			return False
		return self.pravilni_biti == value.pravilni_biti# all([x==y for x, y in zip(self.mintermi, value.mintermi)])
	
	def __or__(self,other):
		name = varname(raise_exc=False) or self.name or "f"
		if other == 0:
			return Funkcija(mintermi=self.mintermi.copy(), n=self.n, spremenljivke=self.imena_spr,name=name)
		elif other == 1:
			return Funkcija(pravilni_biti="1",n=0,name=name)
		elif type(other) != Funkcija:
			raise Exception("Not a Function: "+ str(other))
		spr, (spr_f1, spr_f2) = get_overlapping_inputs(self,other)
		#print("Union spr", spr)
		p_biti = ""
		new_fn_n = len(spr)
		for trm in range(2**(new_fn_n)):
			mtm = minterm_v_niz(trm,n=new_fn_n)
			b_f1 = int(spr_f1(self.pravilni_biti,mtm))
			b_f2 = int(spr_f2(other.pravilni_biti,mtm))
			p_biti+= "1" if (b_f1==1 or b_f2==1) else "0"
		#print(p_biti)
		return Funkcija(p_biti,spremenljivke=spr,name=name)

	def __add__(self,other):
		return self.__or__(other)

	def __and__(self, other):
		name = varname(raise_exc=False) or self.name or "f"
		if other == 0:
			return Funkcija(pravilni_biti="0",n=0)
		elif other == 1:
			return Funkcija(mintermi=self.mintermi.copy(), n=self.n, spremenljivke=self.imena_spr,name=name)
		elif type(other) != Funkcija:
			raise Exception("Not a Function: "+ str(other))
		spr, (spr_f1, spr_f2) = get_overlapping_inputs(self,other)
		#print("Union spr", spr)
		p_biti = ""
		new_fn_n = len(spr)
		for trm in range(2**(new_fn_n)):
			mtm = minterm_v_niz(trm,n=new_fn_n)
			b_f1 = int(spr_f1(self.pravilni_biti, mtm))
			b_f2 = int(spr_f2(other.pravilni_biti, mtm))
			p_biti+= "1" if (b_f1==1 and b_f2==1) else "0"
		#print(p_biti)
		return Funkcija(p_biti,spremenljivke=spr,name=name)

	def __mul__(self, other):
		return self.__and__(other)

	def __invert__(self):
		name = varname(raise_exc=False) or self.name or "f"
		prav = ''.join(["0" if x == "1" else "1" for x in self.pravilni_biti])
		return Funkcija(prav,n=self.n,spremenljivke=self.imena_spr,name=name)
	
	def __neg__(self):
		return self.__invert__()	

	def tex(self, fn_index=None)-> NoEscape: 
		"""
		Vrne notacijo funkcije v odvisnosti od spremenljivk

		Parameters
		----------
		sub_index: str, optional
			Opcijski podpis funkciji

		"""
		inputs = ','.join(self.imena_spr)
		#print(inputs)
		if fn_index is not None:
			fn_index="_{"+fn_index+"}"
		else:
			fn_index= ""
		return NoEscape(self.name+fn_index+NoEscape(f"({inputs})"))
	
	def sort(self,order=None):
		"""
		Vrne kopijo funkcije z danim oz. urejenim vrstnim redom

		Parameters
		----------
		order: list of str, optional
			Zaporedje vhodnih spremenljivk, ki prepiše sortiranje po abecedi

		"""
		o, (fn,) = get_overlapping_inputs(self,inputs=order)
		pb = ''.join(
			[fn(self.pravilni_biti, minterm_v_niz(i,n=self.n)) for i in range(2**self.n) ]
			)
		return Funkcija(pb,spremenljivke=o,n=self.n)

	def table(self,order:Optional[List[str]]=None) -> str:
		"""
		Vrne niz, ki predstavlja pravilnostno tabelo funkcije

		Parameters
		----------
		order: list of str, optional
			Zaporedje vhodnih spremenljivk, ki prepiše sortiranje po abecedi

		"""
		if order is not None:
			return self.sort(order).table()
		r = []
		w = max([len(n) for n in self.imena_spr])
		headers = ' '.join([("{: <%s}"%w).format(b) for b in self.imena_spr])
		print(headers,self.name,sep=" | ")
		for mtrm, vr in enumerate(self.pravilni_biti):
			niz = minterm_v_niz(mtrm,n=self.n)
			print(*[" ".join([("{: >%s}"%w).format(b) for b in niz]),vr], sep=" | ")

	@classmethod
	def table_all(cls, *functions, sort=None):
		spr, fns = get_overlapping_inputs(*functions, inputs=sort)
		n_all_inp = len(spr)
		names = [f.name for f in functions]
		r = []
		w = max([len(n) for n in spr])
		headers = ' '.join([("{: <%s}"%w).format(b) for b in spr])
		print(headers,*names, sep=" | ")
		for mtrm in range(2**n_all_inp):
			niz = minterm_v_niz(mtrm,n=n_all_inp)
			print(
					*[" ".join([("{: >%s}"%w).format(b) for b in niz]),
					*[str(fn_f(f.pravilni_biti, niz)) for fn_f, f in zip(fns, functions)]
					], sep=" | "
					)
		r = "\n".join(r)
		return r

def fn_for(poi):
	_poi = poi.copy()
	def fn(biti, skupni_term_in):
		#print(_poi)
		v_tej_f = int(''.join([skupni_term_in[i] for i in _poi]),2)
		return biti[v_tej_f]
	return fn

def get_overlapping_inputs(*functions:List[Funkcija], inputs=None):
	if inputs is None:
		inputs = set()
		for f in functions:
			[inputs.add(ime) for ime in f.imena_spr]
		o = list(sorted(inputs))
	else:
		if not isinstance(inputs, (list,tuple,set)):
			raise Exception("Invalid inputs:" + str(inputs))
		inputs = provide_no_escape(*inputs)
		print(inputs)
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
	pass