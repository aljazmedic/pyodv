from .funkcija import Funkcija
from typing import List, Union, Optional
import re
from pyodv.util import fixed
from abc import ABC, abstractmethod
from pylatex.utils import NoEscape
import inspect

from typing import List, Union, Optional

#print(SPLITTER_RE)
def get_tokens(tekst:str) -> List[str]:
	m = re.match("("+SPLITTER_RE+")+", tekst)
	if m:
		return re.findall(TOKEN_RE,tekst)
	return []

class Veznik:

	def __init__(self, ime:str, fn:callable, **kwargs):
		self.ime = ime
		self.fn = fn
		self.n = len(inspect.getargspec(fn).args)
		for k, v in kwargs.items():
			if k in ["logisim","latex"]:
				self.__setattr__(k,v)
	
	def izracunaj(self,*args):
		if len(args) != self.n:
			raise Exception("Invalid number of arguments: ", args)
		return self.fn(*args)

	def matches(self, tokens:List[str], idx:int) -> bool:
		if idx >= len(tokens): return False
		ans =  (tokens[idx] == self.latex)
		return ans;
	
	def __str__(self):
		return self.ime

class SpremenljivaVrednost:
	def __init__(self, name):
		self.name = name
		self.pos = None
		self.neg = None
	
	def __eq__(self, value):
		return isinstance(value,SpremenljivaVrednost) and value.name == self.name

	def __ne__(self, value):
		if not isinstance(value,SpremenljivaVrednost): return False
		return not self.__eq__(value) 

	def __hash__(self):
		return hash(self.__str__())

	def __str__(self):
		return f"Spr({self.name})"

class DoloceneSpr:
	def __init__(self, d:dict=None):
		self.vrednost = None
		if d is not None:
			self.cmb = d.copy()
		else:
			self.cmb = {}
	
	def __getitem__(self,k):
		# Ce je ze nastimana spremenljivka, vrni vrednost
		# Drugace vrni dve kopiji z definiranima vrednostima
		if k not in self:
			# generate two different NeodvisneVrednosti
			self.cmb[k.name]=0
			n1 = DoloceneSpr(d=self.cmb)
			self.cmb[k.name]=1
			n2 = DoloceneSpr(d=self.cmb)
			del self.cmb[k.name]
			return (n1, n2)
		assert isinstance(k, SpremenljivaVrednost)
		v = self.cmb[k.name]
		return v

	def __delitem__(self, k):
		del self.cmb[k]
	
	def __contains__(self, k):
		if not isinstance(k, SpremenljivaVrednost): raise Exception("Napacno dostopanje spremenljivk:" + str(k) )
		return (k.name in self.cmb)
	
	def __str__(self):
		ret = "" if self.vrednost is None else f":{self.vrednost}"
		if len(self.cmb) == 0: return "{}"+ret+"\n"
		return "{" + ','.join(
			f"{key}={value}" for key, value in self.cmb.items()
		)+"}"+ret
	
	def zap(self,_zap):
		s = ""
		for b in _zap:
			if b not in self: raise Exception("Wrong variable access "+str(b))
			s+=str(self[b])
		return s

class TokenConsumerClen(ABC):

	@abstractmethod
	def run(self, tokens:List[str], i:int, post_fix:List[any]) -> int:
		pass

class SpremenljivkaClen(TokenConsumerClen):
	def __init__(self):
		spr_r, konst_r = spr_konst_re
		self.spr_re = re.compile(spr_r)
		self.konst_re = re.compile(konst_r)
		self.vars = set()

	def matches(self, token:str) -> Union[re.match, None]:
		return (self.spr_re.match(token) or self.konst_re.match(token))
	
	def run(self, tokens:List[str], i:int, post_fix:List[any]) -> int:
		next_i = i
		next_token = tokens[next_i]
		if self.konst_re.match(next_token):
			# print("Prebral KONST:", next_token)
			post_fix.append(int(next_token))
			return next_i +1
		elif self.spr_re.match(next_token):
			# print("Prebral SPREMENLJIVKO:", next_token)
			sv = SpremenljivaVrednost(next_token)
			post_fix.append(sv)
			self.vars.add(sv)
			return next_i +1
		raise Exception("Invalid token: "+next_token)
	
class DvoClen(TokenConsumerClen):
	def __init__(self,fn:Veznik,naslednji:TokenConsumerClen):
		if not fn.latex: raise Exception("No latex matcher: "+str(fn))
		self.match_str = fn.latex
		self.fn = fn
		self.naslednji = naslednji

	def run(self, tokens:List[str], i:int, post_fix:List[any]) -> int:
		next_i = self.naslednji.run(tokens, i, post_fix)
		if self.fn.matches(tokens, next_i):
			# print("Dobil", self.fn.latex, "i=", next_i)
			next_i+=1
			next_i = self.run(tokens, next_i, post_fix)
			post_fix.append(self.fn)
		return next_i

class EnoClen(TokenConsumerClen):
	def __init__(self, fn:Veznik, povratni:TokenConsumerClen, naslednji:SpremenljivkaClen):
		self.fn = fn
		self.naslednji = naslednji
		self.povratni = povratni
		
	def run(self, tokens, i, post_fix) -> int:
		next_i = i
		next_token = tokens[i]
		if self.fn.matches(tokens, next_i):
			# print("Dobil neg i=", next_i)
			# overline -> Clen
			next_i+=1
			next_i = self.run(tokens, next_i, post_fix)
			post_fix.append(self.fn)
			return next_i
		elif next_token in "{(":
			# print("Dobil { i=",next_token)
			next_i+=1 # consume "{"
			next_i = self.povratni.run(tokens,next_i,post_fix)
			if(tokens[next_i] not in ")}"): raise Exception("Unmatched {")
			# print("Dobil } i=",next_i)
			next_i+=1 # consume "}"
			return next_i
		else:
			# print("Dobil konstanto i=", next_i)
			next_i = self.naslednji.run(tokens, next_i, post_fix)
			# print("Nazaj it K/S i=", next_i)
			return next_i
	
	def matches(self, tokens, idx):
		if idx >= len(tokens): return False
		if self.fn.matches(tokens, idx): return True # Next is negation
		if tokens[idx] in "{(": return True # Next is whole expression
		return self.naslednji.matches(tokens[idx]) # Next is constant

class InClen(TokenConsumerClen):
	def __init__(self,fn:Veznik,naslednji:EnoClen):
		if not fn.latex: raise Exception("No latex matcher: "+str(fn))
		self.match_str = fn.latex
		self.fn = fn
		self.naslednji = naslednji

	def run(self, tokens:List[str], i:int, post_fix:List[any]) -> int:
		next_i = self.naslednji.run(tokens, i, post_fix)
		if self.fn.matches(tokens, next_i):
			# print("Dobil", self.fn.latex, "i=", next_i)
			next_i += 1
			next_i = self.run(tokens, next_i, post_fix)
			post_fix.append(self.fn)
		elif self.next_in(tokens, next_i):
			next_i = self.run(tokens,next_i, post_fix)
			post_fix.append(self.fn)
		return next_i
	
	def next_in(self, tokens, idx):
		if idx >= len(tokens): return False
		return self.naslednji.matches(tokens, idx)

def eval_postfix(postfix:List[Union[Veznik,int,SpremenljivaVrednost]], za:Optional[DoloceneSpr]=None, stk=None):
	if stk is None:		
		stk = []
	if za is None:
		za = DoloceneSpr()
	while len(postfix)>0:
		ta = postfix.pop(0)
		if isinstance(ta,Veznik):
			operandi = [stk.pop() for _ in range(ta.n)]
			operandi = reversed(operandi)
			stk.append(ta.izracunaj(*operandi))
		elif isinstance(ta, SpremenljivaVrednost):
			if ta in za:
				stk.append(za[ta])
			else:
				#generate two defined 
				za_0, za_1 = za[ta]
				
				#Try with each of stacks and postfixes
				with fixed(stk, postfix) as (s_0, pf):
					s_0.append(0)
					pri_0 = eval_postfix(pf, za=za_0, stk=s_0)

				with fixed(stk, postfix) as (s_1,pf):
					s_1.append(1)
					pri_1 = eval_postfix(pf, za=za_1, stk=s_1)

				return [*pri_0, *pri_1]
		elif SPREMENLJIVKA.matches(str(ta)):
			stk.append(ta)
		else:
			raise Exception("Napaka pri evalvaciji postfiksnega zapisa")

	if len(stk) != 1:
		raise Exception("Napaka pri evalvaciji postfiksnega zapisa")
	za.vrednost = stk[0]
	return [za]


### Tokenizing 

V_ne = Veznik("NE", lambda x:1 if x == 0 else 0,latex="\\overline",logisim="~")
V_ter = Veznik("IN",lambda x,y:x&y,latex="\\land",logisim="*")
V_scheff = Veznik("SCHEFF", lambda x,y:V_ne.izracunaj(x&y), latex="\\uparrow")
V_lukpier = Veznik("LUKPIER", lambda x,y:V_ne.izracunaj(x|y),latex="\\downarrow")
V_ali = Veznik("ALI", lambda x,y:x|y,latex="\\lor",logisim="+")
V_impl = Veznik("IMPL", lambda x,y:V_ne.izracunaj(x) | y,latex="\\implies")
V_xor = Veznik("XOR", lambda x,y: x^y,latex="\\oplus")
V_ekv = Veznik("EKV", lambda x,y: x==y,latex="\\Leftrightarrow")


spr_konst_re = [
	r"x_(?:(?:[a-zA-Z0-9,=_]+)|(?:\{[a-zA-Z0-9,=_]+\}))",
	r"[01]{1}"
	]

dvoclenski_simboli = [x.latex.replace("\\","\\\\") for x in [V_ne,V_ter,V_scheff,V_lukpier,V_ali,V_impl,V_xor,V_ekv]]
splitter_re = [
	*dvoclenski_simboli,
	"[\\{\\(]",
	"[\\})]",
	*spr_konst_re
]

SPLITTER_RE = "((?:" + ")|(?:".join(splitter_re) + "))\\s?"
TOKEN_RE= re.compile(SPLITTER_RE)


SPREMENLJIVKA = SpremenljivkaClen()
NE = EnoClen(V_ne, None, SPREMENLJIVKA) # EKV later
IN = InClen(V_ter, NE)
SCHEFF = DvoClen(V_scheff,IN)
LUKPIER = DvoClen(V_lukpier,SCHEFF)
ALI = DvoClen(V_ali,LUKPIER)
IMPL = DvoClen(V_impl,ALI)
XOR = DvoClen(V_xor,IMPL)
IZRAZ = EKV = DvoClen(V_ekv,XOR)
NE.povratni = EKV # Complete cycle

def from_latex(tekst:str, **fn_init_args)->Funkcija:
	"""
	Parameters
	----------
	tekst : str
		LaTeX representation of equation, using \\lor, \\land, \\overline,
		\\downarrow, \\uparrow, \\implies, \\oplus, \\Leftrightarrow
		Variables following format x_<idx> may be used
	
	fn_kwargs : dict, optional
		Argumenti, ki so posredovani v kreacijo objekta funkcije
	
	Returns
	--------
	fn : Funkcija
		funkcija, ovrednotena pri različnih vrednostih spremenljivk.
	"""
	#print(SPLITTER_RE)
	print("LaTeX:", tekst)
	tokens = get_tokens(tekst)
	print("Tokenizirano:", tokens)
	POST_FIX = []
	IZRAZ.run(tokens,0,POST_FIX)
	print("Postfiksni zapis:", *POST_FIX)
	if len(SPREMENLJIVKA.vars) == 0:
		vr = eval_postfix(POST_FIX)
		fn_init_args.update({"spremenljivke":[],"n":0})
		return Funkcija(str(vr[0].vrednost),**fn_init_args)
	else:
		order = list(SPREMENLJIVKA.vars)
		order.sort(key=lambda x:x.name)
		resitve = eval_postfix(POST_FIX)
		biti_ = ''.join([str(v.vrednost) for v in resitve])
		fn_init_args.update({"spremenljivke":[NoEscape(sv.name) for sv in order]})
		return Funkcija(biti_, **fn_init_args)
