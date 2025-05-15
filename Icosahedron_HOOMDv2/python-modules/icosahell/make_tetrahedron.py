# Contains some routines for generating tetrahedra.
from __future__ import print_function

import sys, numpy as np, math

def generate_deg( L1, L2, theta01, theta12, theta20 ):
    """ Generates a general, irregular tetrahedron with tilts in degrees. """
    c = math.pi / 180.0
    return generate_tetrahedron( L1, L2, theta01*c, theta12*c, theta20*c )


def tetrahedron_to_gnuplot( x0, x1, x2, x3, trunc_height = None ):
    """ Outputs tetrahedron vertices to a gnuplotabble format. """

    print( x0[0], x0[1], x0[2] )
    print( x1[0], x1[1], x1[2] )
    print( "\n" )
    print( x1[0], x1[1], x1[2] )
    print( x2[0], x2[1], x2[2] )
    print( "\n" )
    print( x2[0], x2[1], x2[2] )
    print( x0[0], x0[1], x0[2] )
    print( "\n" )

    if trunc_height is None:
        print( x0[0], x0[1], x0[2] )
        print( x3[0], x3[1], x3[2] )
        print( "\n" )
        print( x1[0], x1[1], x1[2] )
        print( x3[0], x3[1], x3[2] )
        print( "\n" )
        print( x2[0], x2[1], x2[2] )
        print( x3[0], x3[1], x3[2] )
        print( "\n" )
        
    else:
        pass


    
def generate( L1, L2, theta01, theta12, theta20 ):
    """ Generates a general, irregular tetrahedron """
    # The tetrahedron has an isocles triangle as base, and the
    # faces have tilts theta01, theta12 and theta20 (in radians)

    y2 = math.sqrt( L2*L2 - 0.25*L1*L1 )
    x0 = np.array( [ -0.5*L1,  0, 0 ], dtype = float )
    x1 = np.array( [  0.5*L1,  0, 0 ], dtype = float )
    x2 = np.array( [       0, y2, 0 ], dtype = float )

    b01 = x1 - x0
    b12 = x2 - x1
    b20 = x0 - x2

    xavg = 0.3333333333333*( x0 + x1 + x2 )
    xavg[2] = L1

    phi01 = 0.5*math.pi - theta01
    phi12 = 0.5*math.pi - theta12
    phi20 = 0.5*math.pi - theta20

    c01 = math.tan( phi01 )
    c12 = math.tan( phi12 )
    c20 = math.tan( phi20 )


    def L2( x3, x00, b00 ):
        """ Returns the length squared from b00 to x3_perp. """
        x3p = np.array( [x3[0], x3[1], 0.0], dtype = float )
        x3mx0 = x3p - x00

        x3m2 = np.dot( x3mx0, x3mx0 )
        x3mx0b00 = np.dot( x3mx0, b00 )
        b002 = np.dot( b00, b00 )

        return x3m2 - x3mx0b00*x3mx0b00 / b002

    def L2_jac( x3, x00, b00 ):
        """ Returns the Jacobi matrix of the length squared function. """
        x3p = np.array( [x3[0], x3[1], 0.0], dtype = float )
        x3mx0 = x3p - x00

        x3m2 = np.dot( x3mx0, x3mx0 )
        x3mx0b00 = np.dot( x3mx0, b00 )
        b002 = np.dot( b00, b00 )

        return 2.0*( x3mx0 + x3mx0b00 * b00 / (b002*b002) )
        
    
    def my_func( x3 ):
        """ The function whose roots to find. """
        return np.array( [ L2( x3, x0, b01 ) * c01*c01 - x3[2]*x3[2],
                           L2( x3, x1, b12 ) * c12*c12 - x3[2]*x3[2],
                           L2( x3, x2, b20 ) * c20*c20 - x3[2]*x3[2] ] )

        
    def my_jac( x3 ):
        """ Jacobi matrix of my_func. """
        JJ = np.zeros( [3,3], dtype = float )

        L2j01 = L2_jac( x3, x0, b01 )
        L2j12 = L2_jac( x3, x1, b12 )
        L2j20 = L2_jac( x3, x2, b20 )
        
        JJ[0,0] = L2j01[0] * c01*c01
        JJ[0,1] = L2j01[1] * c01*c01
        JJ[0,2] = -2*x3[2]

        JJ[1,0] = L2j12[0] * c12*c12
        JJ[1,1] = L2j12[1] * c12*c12
        JJ[1,2] = -2*x3[2]

        JJ[2,0] = L2j20[0] * c20*c20
        JJ[2,1] = L2j20[1] * c20*c20
        JJ[2,2] = -2*x3[2]

        return JJ

    x3sol, it, res = newton.find_root( my_func, my_jac, xavg, tol = 1e-32,
                                       maxit = 1000, get_res_and_it = True )
    print( "Got solution x =", x3sol, " after", it, "iters for res of",
           res, file = sys.stderr )

    return [ x0, x1, x2, x3sol ]

    

def test_vertices():
    """ Tests the vertex generator. """
    x0, x1, x2, x3 = generate_tetrahedron_deg( 1.2, 1.0, 11.0, 11.0, 11.0 )
    tetrahedron_to_gnuplot( x0, x1, x2, x3, trunc_height = None )


