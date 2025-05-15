from __future__ import print_function

import math, numpy as np, copy, sys

def find_root( fh, Jh, x0, tol = 1e-5, maxit = 100, get_res_and_it = False ):
    """ Simple Newton iteration. """

    x = copy.copy(x0)
    res  = fh(x)
    res2 = np.dot( res, res )
    tol2 = tol*tol
    it = 0
    while res2 > tol2 and it < maxit:
        JJ = Jh(x)
        x -= np.linalg.solve( JJ, res )
        res = fh(x)
        res2 = np.dot( res, res )
        it += 1

    if get_res_and_it:
        return x, it, math.sqrt(res2)
    else:
        return x

def test_newton():
    """ Tests newton method. """

    def my_func( x ):
        return np.array( [ math.sin(x[1]) + 0.1*x[0],
                           math.exp(-x[0]) - x[0] + 0.3*x[1] ] )

    def my_jac( x ):
        A = np.zeros( (2, 2) )
        A[0,0] = 0.1
        A[0,1] = math.cos(x[1])
        A[1,0] = -math.exp(x[0]) - 1.0
        A[1,1] = 0.3

        return A

    x0 = np.array( [1,1], dtype = float )
    x, it, res = find_root( my_func, my_jac, x0, get_res_and_it = True, tol = 1e-8 )

    print( "Got solution x =", x, " after", it, "iters for res of",
           res, file = sys.stderr )

if __name__ == "__main__":
    test_newton()
