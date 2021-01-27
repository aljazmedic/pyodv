import numpy as np
from functools import reduce


ALI = lambda x, y: x or y
TER = lambda x, y: x and y
XOR = lambda x, y: x != y 
EKV = lambda x, y: x==y
IMPL = lambda x, y: (not x) or y 


class Vektor:
    def __init__(self, seznam: list):
        for e in seznam:
            if e not in (1, 0):
                raise Exception("Vektor mora imeti le 1 in 0!")
        self.dolzina = len(seznam)
        self.elementi = np.array(seznam, dtype=np.int32)

    def reduciraj(self, operacija):
        return reduce(operacija, self.elementi)

    def __str__(self):
        return "Vektor(%s)"%(str(self.elementi))

    def __neg__(self):
        nov_seznam = [(not x) for x in self.elementi]
        return Vektor(nov_seznam)
    
    def solezni(self, other, op):
        if not isinstance(other, Vektor):
            raise Exception("Nepravilen tip!: "+type(other))
        if other.dolzina != self.dolzina:
            raise Exception("Dolžini se ne ujemata!")
        t =[]
        for a, b in zip(self.elementi, other.elementi):
            t.append( op(a, b) )
        return Vektor(t)
    
    def __or__( self, other):
        return self.solezni(other, ALI)

    def __and__( self, other):
        return self.solezni(other, TER)


class Matrika:
    def __init__(self, matrika):
        # Checki inputa
        dolzina_vrstice = -1
        for podana_vrstica in matrika:
            """ if not isinstance(podana_vrstica, (list, np.array)):
                raise Exception("Matrika mora vsebovati liste!") """
            if(dolzina_vrstice == -1):
                dolzina_vrstice = len(podana_vrstica)
            if(dolzina_vrstice != len(podana_vrstica)):
                raise Exception("Neenaka dolzina vrstic!")

        
        self.elementi = np.array(matrika, dtype=np.int32)

    @property
    def T(self):
        return Matrika(np.transpose(self.elementi))
    
    def __str__(self):
        return "Matrika(\n%s)"%(self.elementi)
    
    @classmethod
    def mat_mul(cls, m1, m2, o1=ALI, o2=TER):
        if isinstance(m1, Vektor):
            mat1 = m1.elementi[np.newaxis, :]
        elif isinstance(m1, Matrika):
            mat1 = m1.elementi
        else:
            raise Exception("Nepravilen prvi argument!")

        if isinstance(m2, Vektor):
            mat2 = m2.elementi[:, np.newaxis]
            print("mat2 ", mat2)
        elif isinstance(m2, Matrika):
            mat2 = m2.elementi.T
        else:
            raise Exception("Nepravilen drugi argument!")
        
        print("m1", mat1, sep="\n")
        print("m2", mat2, sep="\n")
        if mat1.shape[1] != mat2.shape[1]:
            raise Exception("Nekompatibilni matriki")

        ret_arr = np.zeros((mat1.shape[0], mat2.shape[0]))
        for i, row1 in enumerate(mat1):
            for j, col2 in enumerate(mat2):
                ret_arr[i,j] = reduce(o1, [o2(x,y) for x, y in zip(row1, col2)])
        return Matrika(ret_arr)

    @classmethod
    def W(cls, n):
        ret = np.zeros((pow(2,n), n))
        for term in range(pow(2,n)):
            for i in range(n):
                if (1<<(n-i-1)) & term != 0:
                    ret[term,i]=1
        return Matrika(ret)


if __name__ == "__main__":
    v1 = Vektor([0, 0, 1, 1])
    v2 = Vektor([1, 0, 0, 1])


    print("v1\t", v1)
    print("v2\t",v2)
    print("-v2\t", (-v2))

    print("v1|v2\t", v1|v2 )
    print("v1&v2\t", v1&v2 )
    print(v1.reduciraj(TER))

    m1 = Matrika([
        [ 1, 0, 0 ],
        [ 0, 1, 1 ]
    ])
    m2 = Matrika([
        [ 1, 0 ],
        [ 0, 1 ],
        [ 1, 1 ]
    ])
    print(Matrika.mat_mul(m1, m2))
    print(Matrika.W(3))
    v2 = Vektor([1, 0, 0, 1])
    #mintermi
    print(
        Matrika.mat_mul(v2, Matrika.W(4).T, TER, EKV)
        )
    