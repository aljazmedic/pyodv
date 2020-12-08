import re
from abc import abstractmethod
from funkcija import Funkcija
from typing import List, Union, Optional
import inspect


def dumps(s):
	print(f"'{s}'", ":".join("{:02x}".format(ord(c)) for c in s))

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
		return f"{self.ime}()"




### Tokenizing 

V_ne = Veznik("NE", lambda x:1 if x == 0 else 0,latex="\\overline")
V_ter = Veznik("IN",lambda x,y:x&y,latex="\\land")
V_scheff = Veznik("SCHEFF", lambda x,y:V_ne.izracunaj(x&y), latex="\\uparrow")
V_lukpier = Veznik("LUKPIER", lambda x,y:V_ne.izracunaj(x|y),latex="\\downarrow")
V_ali = Veznik("ALI", lambda x,y:x|y,latex="\\lor")
V_impl = Veznik("IMPL", lambda x,y:V_ne.izracunaj(x) | y,latex="\\implies")
V_xor = Veznik("XOR", lambda x,y: x^y,latex="\\oplus")
V_ekv = Veznik("EKV", lambda x,y: x==y,latex="\\Leftrightarrow")


spr_konst_re = [
	r"x_(?:(?:[a-zA-Z0-9,=]+)|(?:\{[a-zA-Z0-9,=]+\}))",
	r"[01]{1}"
	]

dvoclenski_simboli = [x.latex.replace("\\","\\\\") for x in [V_ne,V_ter,V_scheff,V_lukpier,V_ali,V_impl,V_xor,V_ekv]]
splitter_re = [
*dvoclenski_simboli,
"\\{","\\}",
*spr_konst_re
]
SPLITTER_RE = "((?:" + ")|(?:".join(splitter_re) + "))\\s?"
TOKEN_RE= re.compile(SPLITTER_RE)


def get_tokens(tekst:str) -> List[str]:
	m = re.match("("+SPLITTER_RE+")+", tekst)
	if m:
		return re.findall(TOKEN_RE,tekst)
	return []


class TokenConsumer:
	@abstractmethod
	def run(self, tokens:List[str], i:int, post_fix:List[any]) -> int:
		pass

class Spremenljivka(TokenConsumer):
	def __init__(self):
		spr_r, konst_r = spr_konst_re
		self.spr_re = re.compile(spr_r)
		self.konst_re = re.compile(konst_r)
		self.vars = set()

	def matches(self, s:str) -> Union[re.match, None]:
		return  self.spr_re.match(s) or self.konst_re.match(s)
	
	def run(self, tokens:List[str], i:int, post_fix:List[any]) -> int:
		next_i = i
		next_token = tokens[next_i]
		if self.konst_re.match(next_token):
			print("Prebral KONST:", next_token)
			post_fix.append(int(next_token))
			return next_i +1
		raise Exception("Invalid token: "+next_token)
		

class DvoClen(TokenConsumer):
	def __init__(self,fn:Veznik,naslednji:TokenConsumer):
		if not fn.latex: raise Exception("No latex matcher: "+str(fn))
		self.match_str = fn.latex
		self.fn = fn
		self.naslednji = naslednji

	def run(self, tokens:List[str], i:int, post_fix:List[any]) -> int:
		next_i = self.naslednji.run(tokens, i, post_fix)
		if self.fn.matches(tokens, next_i):
			print("Dobil", self.fn.latex, "i=", next_i)
			next_i+=1
			next_i = self.run(tokens, next_i, post_fix)
			post_fix.append(self.fn)
		return next_i

class EnoClen(TokenConsumer):
	def __init__(self, fn:Veznik, povratni:TokenConsumer, naslednji:Spremenljivka):
		self.fn = fn
		self.naslednji = naslednji
		self.povratni = povratni
		
	def run(self, tokens, i, post_fix) -> int:
		next_i = i
		next_token = tokens[i]
		if self.fn.matches(tokens, next_i):
			print("Dobil neg i=", next_i)
			# overline -> Clen
			next_i+=1
			next_i = self.run(tokens, next_i, post_fix)
			post_fix.append(self.fn)
			return next_i
		elif next_token == "{":
			print("Dobil { i=",next_token)
			next_i+=1 # consume "{"
			next_i = self.povratni.run(tokens,next_i,post_fix)
			if(tokens[next_i] != "}"): raise Exception("Unmatched {")
			print("Dobil } i=",next_i)
			next_i+=1 # consume "}"
			return next_i
		else:
			print("Dobil konstanto i=", next_i)
			next_i = self.naslednji.run(tokens, next_i, post_fix)
			print("Nazaj it K/S i=", next_i)
			return next_i


SPREMENLJIVKA = Spremenljivka()
NE = EnoClen(V_ne, None, SPREMENLJIVKA) # EKV later
IN = DvoClen(V_ter, NE)
SCHEFF = DvoClen(V_scheff,IN)
LUKPIER = DvoClen(V_lukpier,SCHEFF)
ALI = DvoClen(V_ali,LUKPIER)
IMPL = DvoClen(V_impl,ALI)
XOR = DvoClen(V_xor,IMPL)
IZRAZ = EKV = DvoClen(V_ekv,XOR)
NE.povratni = EKV # Complete cycle

def eval_postfix(postfix:List[Union[Veznik,int,str]]):
	stk = []
	while len(postfix)>0:
		ta = postfix.pop(0)
		print(stk, ta)
		if SPREMENLJIVKA.matches(str(ta)):
			stk.append(ta)
		elif isinstance(ta,Veznik):
			operandi = [stk.pop() for _ in range(ta.n)]
			operandi = reversed(operandi)
			stk.append(ta.izracunaj(*operandi))
	if len(stk) != 1:
		raise Exception("Napaka pri evalvaciji postfiksnega zapisa")
	return stk[0]


def from_latex(tekst:str)->Funkcija:
	print(SPLITTER_RE)
	tokens = get_tokens(tekst)
	print(tokens)
	POST_FIX = []
	IZRAZ.run(tokens,0,POST_FIX)
	print(*POST_FIX)
	print(eval_postfix(POST_FIX))


if __name__ == "__main__":
	from_latex("0 \\implies 0 \\lor 0")