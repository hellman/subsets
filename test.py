from binteger import Bin
from subsets import DenseSet, DenseBox, DenseTernary


# import random
# random.seed(1023)
# n = 30
# db = DenseSet(n)
# for i in range(1024):
#     db.set(random.randrange(2**n))

# print("go")
# for i in range(10):
#     v = db.copy()
#     v.do_Mobius()
#     v.do_MaxSet()
#     print(i, v)
# quit()


def Quine_McCluskey_Step1(P: DenseSet, n=None):
    """
    See https://doi.org/10.13154/tosc.v2020.i3.327-361 .
    Reformulation of Quine-McCluskey algorithm in two parts:
    1. finding all subsets of (P) of the form (a xor LowerSet(u))
       with maximal (u).
    2. finding a good / optimal covering of P with such subsets

    This method does part 1 in the framework of dense sets.

    Complexity: n 2^n |P|
    """
    if n is None:
        assert isinstance(P, DenseSet), "n must be given or P must be a DenseSet"
        n = P.n

    S = []
    for a in P:
        a = Bin(a, n).int

        # TBD: do in place and return orig P
        X = P.copy()
        X.do_Not(a)
        X.do_Complement()
        X.do_UpperSet()
        X.do_Complement()
        X.do_MaxSet()
        X.do_UnsetUp(a)
        for u in X:
            S.append((a, u))
    return S

# n = 7
# d = DenseSet(n, [
# 0b0100100,
# 0b0100111,
# 0b0100101,
# 0b0100001,
# 0b0101001,
# 0b0111001,
# 0b0011001,
# 0b0101001,
# 0b0110001,
# 0b0001001,
# 0b0010001,
# 0b0100001,
# 0b0000001,
# 0b1111111,
# ])
# pats = set()
# for a, u in Quine_McCluskey_Step1(d):
#     a = Bin(a, n)
#     u = Bin(u, n)
#     pat = ""
#     for aa, uu in zip(a.str, u.str):
#         if uu == "1":
#             assert aa == "0"
#             pat += "*"
#         else:
#             pat += aa
#     pats.add(pat)
# for pat in sorted(pats):
#     print(pat[::-1])
# quit()
from time import time
from random import randrange, sample
n = 4
itr = 0
while True:
    n = randrange(2, 12)
    n = 16
    print("itr", itr, "n", n)
    db = DenseSet(n)
    full = list(range(2**n))

    e = randrange(n+1)
    e = n
    wt = randrange(2**e+1)

    xs = sample(full, wt)
    # xs = full
    # xs = [
    #     0b0000,
    #     0b0011,
    # ]
    for x in xs:
        db.add(x)
        # print(Bin(x, n).str)
    if randrange(2):
        db.do_Not()
    print("size", len(db), "/", 2**n, "=", "%.2f" % (len(db) / 2**n))
    print()
    # db.add(0b0010)
    # db.add(0b1010)
    # db.add(0b1110)
    # db.add(0b1100)
    # db.add(0b1101)
    # db.add(0b1001)
    # db.add(0b0001)
    # db.add(0b0011)
    # db.add(0b1011)
    print("first")
    pats = set()
    t0 = time()
    for a, u in Quine_McCluskey_Step1(db):
        a = Bin(a, n)
        u = Bin(u, n)
        pat = ""
        for aa, uu in zip(a.str, u.str):
            if uu == "1":
                assert aa == "0"
                pat += "*"
            else:
                pat += aa
        pats.add(pat)
    print( "%.2f" % (time() - t0) )
    if 0:
        print("pats")
        for pat in sorted(pats):
            print(pat)
        print()

    print("second")
    ter = DenseTernary(db)
    t0 = time()
    #print(len(ter))
    ter.do_QuineMcCluskey()
    #print(len(ter))
    # box = DenseBox([2] * n)
    # for v in db.to_Bins():
    #     box.set(v.tuple)
    # box.do_Sweep_AND_up_OR()
    # box.do_Sweep_NOTAND_down()
    pats2 = set()
    for v in ter:
        digits = []
        for i in range(n):
            digits.append("*" if v % 3 == 2 else str(v % 3))
            v //= 3
        pat = "".join(digits[::-1])
        pats2.add(pat)
    print( "%.2f" % (time() - t0) )

    if 0:
        print("pats2")
        for pat in sorted(pats2):
            print(pat)
        print()

    print(pats == pats2)
    print(pats <= pats2)
    print(pats >= pats2)
    print()

    print("diff")
    for pat in pats - pats2:
        print(pat)
    print()
    assert pats == pats2
    itr += 1
