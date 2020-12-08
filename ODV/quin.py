import numpy as np
from funkcija import Funkcija
from typing import List,Tuple
from util import minterm_v_niz, nanesi_bite
from pylatex import Document, Section, Subsection, Math
from pylatex.utils import NoEscape
from pprint import PrettyPrinter
from itertools import zip_longest

pp = PrettyPrinter(indent=4)

def _poisci_vsebovalnike(n:int, termi:List[int]):
	#struktura returna:
	"""
	'<nivo>:{
		'<vsebovalnik>': (<porabljen>, (<pokriti_mintermi>, ...)),
		...
		},
	...
	"""

	levels = {
		f"{n}":dict([([minterm_v_niz(m,n),[False,(m,)]]) for m in termi])
	}

	#Napreduj iz lvl v lvl
	while str(n) in levels:
		ns = str(n)
		termi = list(levels[ns].keys())
		check_len = len(termi)
		for m1i in range(check_len):
			for m2i in range(m1i+1,check_len):
				term1 = termi[m1i]
				term2 = termi[m2i]
				diff = str_one_bit_diff(term1,term2)
				if diff is not None:
					if f"{n-1}" not in levels:
						levels[f"{n-1}"]={}

					#Pokrije katere minterme
					pokriti_termi = [*levels[ns][term1][1], *levels[ns][term2][1]]
					pokriti_termi.sort()
					levels[f"{n-1}"][diff]=[False,tuple(pokriti_termi)]
					#trenutne 2 porabljena
					levels[ns][term1][0]=True
					levels[ns][term2][0]=True

		#print(ns, levels[ns])
		n-=1
	return levels

def _neporabljeni_sloji(n_spremenljvk, levels):
	#najdi vse vsebovalnike, ki se niso bili porabljeni
	r = {}
	for n in range(n_spremenljvk+1):
		ns = str(n)
		for nghbr,nghtbr_cover in levels.get(ns, {}).items():
			if not nghtbr_cover[0]:
				r[nghbr] = nghtbr_cover[1]
	return r

def _tex_tabela(n_spremenljvk, levels):
	cols = []

	for k, v in levels.items():
		pass
	pass

def _odstrani_nepotrebne(vsebovalniki, termi):
	# Brute force :^)
	# Naredi vse mozne kombinacije vsebovalnikov, in izbere najkrajso izmed
	# Tistih, ki skupaj pokrijejo vse

	check_termi = set(termi)
	veljavne_kombinacije = []
	l_vseb = list(vsebovalniki.items())
	st_vseb = len(l_vseb)

	for i in range(1,2**st_vseb):
		s = minterm_v_niz(i,st_vseb)
		ta_komb_pokriti = set()
		vseb_komb = []
		for j, dodaj in enumerate(s):
			if dodaj == "1":
				v, termi_pokriva = l_vseb[j]
				vseb_komb.append(v)
				for mt in termi_pokriva:
					ta_komb_pokriti.add(mt)
		#kombinacija narejena
		if ta_komb_pokriti == check_termi: #pokriti vsi termi?
			veljavne_kombinacije.append(vseb_komb)
	
	veljavne_kombinacije.sort(key=len)
	return veljavne_kombinacije[0]
	#return vsebovalniki.keys()

def quin(self:Funkcija) -> Tuple[List[str],NoEscape]:
	print(self.mintermi)
	
	levels_maks = _poisci_vsebovalnike(self.st_spremenljivk, self.makstermi)
	levels_min = _poisci_vsebovalnike(self.st_spremenljivk, self.mintermi)
	
	pp.pprint(levels_min)
	pp.pprint(levels_maks)

	vseb_min = _neporabljeni_sloji(self.st_spremenljivk, levels_min)
	vseb_maks = _neporabljeni_sloji(self.st_spremenljivk, levels_maks)


	#print("MDNO", vseb_min)
	min_max_vseb_min = _odstrani_nepotrebne(vseb_min, self.mintermi)
	min_max_vseb_maks = _odstrani_nepotrebne(vseb_maks, self.makstermi)


	mdno_tex, cena_mdno = nanesi_bite(self.st_spremenljivk, min_max_vseb_min,
		vrni_ceno=True)
	
	mkno_tex, cena_mkno = nanesi_bite(self.st_spremenljivk, min_max_vseb_maks,
        pn=('0','1'), #Katere se negira, katere ne
        using=('','\lor'), #
        vrni_ceno=True,
        wrap_inner=True)
	print(cena_mdno, cena_mkno)
	mkno_tex = NoEscape(self.tex(fn_index='MKNO')+"="+mkno_tex)
	mdno_tex = NoEscape(self.tex(fn_index='MDNO')+"="+mdno_tex)

	if cena_mkno[0] < cena_mdno[0] or (cena_mdno[0] == cena_mkno[0] and cena_mkno[1]<cena_mdno[1]):
		ret_tex = NoEscape(self.tex(fn_index='MNO')+"="+mkno_tex)
		return ret_tex, vseb_maks, cena_mkno, (mdno_tex, mkno_tex)
	
	ret_tex = NoEscape(self.tex(fn_index='MNO')+"="+mdno_tex)
	return ret_tex, vseb_min, cena_mdno, (mdno_tex, mkno_tex)

def str_one_bit_diff( m1:str, m2:str):
	diffs=[]
	for idx in range(len(m1)):
		if ((m1[idx] in "X?") ^ (m2[idx] in "X?")): return None
		if m1[idx] != m2[idx]: diffs.append(idx)
		if len(diffs) >= 2: return None
	if len(diffs) != 1:
		return None
	r = list(m1)
	r[diffs[0]] = "X"
	return ''.join(r)

if __name__=="__main__":
	f = Funkcija("0011110001111100")
	print(f)
	arr, tex, eff, (mdno_tex, mkno_tex) = quin(f)
	#print(arr)
	print(tex)