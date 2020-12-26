from ..function import Funkcija
"""
NOR
r s | D1q | D1~q
0 0 | q   | ~q
0 1 | 1   |  0
1 0 | 0   |  1
1 1 | X   |  X

    NOR (extended)
    s r q | D1q | D1~q
    0 0 0 | 0   | 1
    0 0 1 | 1   | 0
    0 1 0 | 0   | 1
    0 1 1 | 0   | 1
    1 0 0 | 1   | 0
    1 0 1 | 1   | 0
    1 1 0 | X   | X
    1 1 1 | X   | X

q D1q | r s
0   0 | x 0 
0   1 | 0 1
1   0 | 1 0
1   1 | 0 x

"""

"""
NAND
r s | D1q | D1~q
0 0 | X   |  X
0 1 | 1   |  0
1 0 | 0   |  1
1 1 | q   | ~q

    NAND (extended)
    s r q | D1q | D1~q
    0 0 0 | X   | X
    0 0 1 | X   | X
    0 1 0 | 0   | 1
    0 1 1 | 0   | 1
    1 0 0 | 1   | 0
    1 0 1 | 1   | 0
    1 1 0 | 0   | 1
    1 1 1 | 1   | 0

q D1q | r s
0   0 | x 0 
0   1 | 0 1
1   0 | 1 0
1   1 | 0 x


"""