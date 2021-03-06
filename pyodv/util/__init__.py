import numpy as np
from typing import List,Tuple,Optional
from pylatex import Math
from pylatex.utils import NoEscape
from contextlib import contextmanager 

ali = lambda x,y:f"{x} \lor {y}"
ter = lambda x,y:f"{x} \land {y}" # in polomy kačo
neg = lambda x:f" \overline{{{x}}}"


def dumps(s):
	# dump strig
	print(f"'{s}'", ":".join("{:02x}".format(ord(c)) for c in s))

@contextmanager
def fixed(*vars_to_save):
	_saved = [var.copy() for var in vars_to_save]
	try:
		if len(_saved) == 1:
			yield _saved[0]
		else:
			yield _saved
	finally:
		pass

def minterm_v_niz(m:int,n:Optional[int]=None) -> str:
	if n is None:
		n = np.ceil(np.log2(m)).astype(np.int32)
	return ("{:0>%d}"%n).format(bin(m)[2:])



def provide_no_escape(*values) -> List[NoEscape]:
	"""Maps non-NoEscape values to NoEscape values.
	"""
	r = [(a if isinstance(a, NoEscape) else NoEscape(a)) for a in values]
	return r


def nanesi_bite(n,nizi:List[str]=None,termi_maske:List[int] = [],pn=('0','1'),using=('\lor',''),wrap_inner=False,vrni_ceno=False) -> [NoEscape, Optional[Tuple[int, int]]]:
	x = lambda n: NoEscape(f"x_{n}")
	naredi_neg, ne_naredi_neg = pn
	glavni_veznik, pomozni_veznik = [(" "+x) if (len(x)>=1 and x[0] != " ") else x for x in using]

	if nizi is None:
		nizi = [minterm_v_niz(x,n) for x in termi_maske]
		st_komponent, st_povezav = len(termi_maske)+1, len(termi_maske) #Glavni OR
	else:
		st_komponent, st_povezav = len(nizi)+1, len(nizi) #Glavni OR
	print(nizi)
	koncno_tex = []
	for niz01 in nizi:
		term_tex=[]
		for i, b in enumerate(niz01, start=1):
			if b in "X?":continue
			elif b==naredi_neg:
				term_tex.append(f" \overline{{{x(i)}}}")
			elif b==ne_naredi_neg:
				term_tex.append(f" {x(i)}")
			else:
				raise Exception(f"Invalid bit: {b}")
			st_povezav+=1
		ta_term =pomozni_veznik.join(term_tex)
		if wrap_inner:
			ta_term = f"({ta_term})"
		koncno_tex.append(ta_term)
	ret_tex = NoEscape(glavni_veznik.join(koncno_tex))
	print(ret_tex)

	if vrni_ceno:
		return ret_tex, (st_komponent, st_povezav)
	return ret_tex

if __name__ == "__main__":
	print(*nanesi_bite(3,[1,2],vrni_ceno=True))