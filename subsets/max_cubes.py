"""
Find all maximal cubes (patterns with 0,1,*) in a Boolean set.

A variation of the first step of the Quine-McCluskey algorithm for Boolean minimization.

See https://doi.org/10.13154/tosc.v2020.i3.327-361 .
Reformulation of Quine-McCluskey algorithm in two parts:

1. finding all subsets of (P) of the form (a xor LowerSet(u))
   with maximal (u).
   a : constant part of the cube
   u : wildcard part

2. finding a good / optimal covering of P with such subsets

This method does part 1 in the framework of dense BINARY/TERNARY sets.

Complexity: n 2^n |P| <= n 4^n (dense binary)
Complexity: n 3^n (dense ternary)
"""

from binteger import Bin

from subsets import DenseSet, DenseTernary


def _prepare_args(P: DenseSet, n=None):
    if n is None:
        if isinstance(P, DenseSet):
            n = P.n
        else:
            for v in P:
                n = len(v)
                break
            else:
                assert isinstance(P, DenseSet), "n must be given or P must be a DenseSet"

    if not isinstance(P, DenseSet):
        P = DenseSet(n, [Bin(v, n).int for v in P])

    return P, n

def MaxCubes_Dense2(P: DenseSet, n=None):
    """
    This method does part 1 in the framework of dense BINARY sets.

    Complexity: n 2^n |P|
    """
    P, n = _prepare_args(P, n)

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


def MaxCubes_Dense3(P: DenseSet, n=None):
    """
    This method does part 1 in the framework of dense TERNARY sets (0/1/*).

    Complexity: n 3^n
    """
    P, n = _prepare_args(P, n)

    ter = DenseTernary(P)

    # does:
    # do_Sweep_QmC_AND_up_OR(mask) : c |= a & b
    # do_Sweep_QmC_NOTAND_down(mask) : a &= ~c; b &= ~c
    ter.do_MaxCubes()

    S = []
    for v in ter:
        a = u = 0
        for i in range(n):
            digit = v % 3
            v //= 3
            if digit == 1:
                a ^= 1 << i
            elif digit == 2:
                u ^= 1 << i
        S.append((a, u))
    return S



MaxCubes = MaxCubes_Dense3
