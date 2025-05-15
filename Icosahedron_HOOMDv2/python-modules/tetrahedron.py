#!/usr/bin/env python3
# Contains some routines for generating tetrahedra.
from __future__ import print_function

import sys, numpy as np, math
import newton

def generate_deg( L1, L2, L3, theta01, theta12, theta20 ):
    """ Generates a general, irregular tetrahedron with tilts in degrees. """
    c = math.pi / 180.0
    return generate( L1, L2, L3, theta01*c, theta12*c, theta20*c )

def trunc_tetrahedron_to_gnuplot( x0, x1, x2, z0, z1, z2 ):
    """ Outputs truncated tetrahedron vertices to a gnuplotabble format. """
    print( x0[0], x0[1], x0[2] )
    print( x1[0], x1[1], x1[2] )
    print( "\n" )
    print( x1[0], x1[1], x1[2] )
    print( x2[0], x2[1], x2[2] )
    print( "\n" )
    print( x2[0], x2[1], x2[2] )
    print( x0[0], x0[1], x0[2] )
    print( "\n" )

    print( x0[0], x0[1], x0[2] )
    print( z0[0], z0[1], z0[2] )
    print( "\n" )
    print( x1[0], x1[1], x1[2] )
    print( z1[0], z1[1], z1[2] )
    print( "\n" )
    print( x2[0], x2[1], x2[2] )
    print( z2[0], z2[1], z2[2] )
    print( "\n" )

    print( z0[0], z0[1], z0[2] )
    print( z1[0], z1[1], z1[2] )
    print( "\n" )
    print( z1[0], z1[1], z1[2] )
    print( z2[0], z2[1], z2[2] )
    print( "\n" )
    print( z2[0], z2[1], z2[2] )
    print( z0[0], z0[1], z0[2] )
    print( "\n" )



def tetrahedron_to_gnuplot( x0, x1, x2, x3 ):
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

    print( x0[0], x0[1], x0[2] )
    print( x3[0], x3[1], x3[2] )
    print( "\n" )
    print( x1[0], x1[1], x1[2] )
    print( x3[0], x3[1], x3[2] )
    print( "\n" )
    print( x2[0], x2[1], x2[2] )
    print( x3[0], x3[1], x3[2] )
    print( "\n" )


def truncate( x0, x1, x2, x3, trunc_height ):
    """ Truncates given tetrahedron to given height. """
    if trunc_height >= x3[2]:
        z0 = x3
        z1 = x3
        z2 = x3

        return [ x0, x1, x2, z0, z1, z2 ]
    else:
        b03 = x3 - x0
        b13 = x3 - x1
        b23 = x3 - x2

        t = trunc_height / x3[2]
        z0 = x0 + b03 * t
        z1 = x1 + b13 * t
        z2 = x2 + b23 * t

        return [ x0, x1, x2, z0, z1, z2 ]



def generate( L1, L2, L3, theta01, theta12, theta20 ):
    """ Generates a general, irregular tetrahedron """
    # The tetrahedron has an isocles triangle as base, and the
    # faces have tilts theta01, theta12 and theta20 (in radians)

    L32 = L3*L3
    L22 = L2*L2
    L12 = L1*L1
    L1L3 = L12/L32
    L2L3 = L22/L32

    # Check whether or not the triangle inequality is respected:
    assert ((L32 <= L12 + L22) and (L22 <= L12 + L32) and (L12 <= L32 + L22)), (
        "Sides {} {} {} do not satisfy the triangle inequality!"
        .format( L1, L2, L3) )

    x2  = (L32 - L22) / (2.0*L1)
    y22 = L22 - (x2 - L1/2)**2
    y2  = math.sqrt(y22)

    x0 = np.array( [ -0.5*L1,  0, 0 ], dtype = float )
    x1 = np.array( [  0.5*L1,  0, 0 ], dtype = float )
    x2 = np.array( [      x2, y2, 0 ], dtype = float )

    b01 = x1 - x0
    b12 = x2 - x1
    b20 = x0 - x2

    # Assert the lengths are OK.
    L01test = np.dot( b01, b01 )
    L12test = np.dot( b12, b12 )
    L20test = np.dot( b20, b20 )

    assert math.fabs( L01test - L12 ) < 1e-12, "Length of side 01 not OK!"
    assert math.fabs( L12test - L22 ) < 1e-12, "Length of side 12 not OK!"
    assert math.fabs( L20test - L32 ) < 1e-12, "Length of side 20 not OK!"

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

    maxit = 100000
    tol = 1e-14
    x3sol, it, res = newton.find_root( my_func, my_jac, xavg, tol = tol,
                                       maxit = maxit, get_res_and_it = True )
    if it == maxit or res > tol:
        print( "Failed to converge to tolerance", tol, "after",
               it, "iterations (maxit ==", maxit, ")! Final res was",
               res, "!", file = sys.stderr )
    else:
        print( "Converged to tolerance", tol, "after",
               it, "iterations (maxit ==", maxit, ") to final res of",
               res, ".", file = sys.stderr )

    # Subtract the average x, y and z from the tetrahedron.
    xavg = ( x0 + x1 + x2 + x3sol ) / 4.0
    x0 -= xavg
    x1 -= xavg
    x2 -= xavg
    x3sol -= xavg

    return [ x0, x1, x2, x3sol ]

def generate_truncated( L1, L2, L3, theta01, theta12, theta20, trunc_height ):
    """ Generates a truncated tetrahedron. """
    x0, x1, x2, x3 = generate( L1, L2, L3, theta01, theta12, theta20 )
    return truncate( x0, x1, x2, x3, trunc_height )


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print( "generating tetrahedron with base lengths 1.2, 1.0, 1.1 "
               "and tilts of 11.0 degrees each.", file = sys.stderr )
        x0, x1, x2, x3 = generate_deg( 1.2, 1.0, 1.1, 11.0, 11.0, 11.0 )
        tetrahedron_to_gnuplot( x0, x1, x2, x3 )
    elif len(sys.argv) == 2 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
        print( "Usage: ./tetrahedron L1 L2 L3 ang1 ang2 ang3 (z-trunc),\n"
               "    where L1, L2 and L3 are the side lengths of the base "
               "triangle,\n    ang1, ang2 and ang3 are the tilt angles in "
               "degrees and\n    z-trunc is an optional "
               "truncation height for a truncated tetrahedron.",
               file = sys.stderr )
    elif len(sys.argv) == 7:
        L1 = float( sys.argv[1] )
        L2 = float( sys.argv[2] )
        L3 = float( sys.argv[3] )
        f1 = float( sys.argv[4] )
        f2 = float( sys.argv[5] )
        f3 = float( sys.argv[6] )


        x0, x1, x2, x3 = generate_deg( L1, L2, L3, f1, f2, f3 )
        tetrahedron_to_gnuplot( x0, x1, x2, x3 )

    elif len(sys.argv) == 8:

        L1 = float( sys.argv[1] )
        L2 = float( sys.argv[2] )
        L3 = float( sys.argv[3] )
        f1 = float( sys.argv[4] )
        f2 = float( sys.argv[5] )
        f3 = float( sys.argv[6] )
        zc = float( sys.argv[7] )

        x0, x1, x2, x3 = generate_deg( L1, L2, L3, f1, f2, f3 )
        x0, x1, x2, z0, z1, z2 = truncate( x0, x1, x2, x3, zc )
        trunc_tetrahedron_to_gnuplot( x0, x1, x2, z0, z1, z2 )

    else:
        print( "Don't know what to do with", len(sys.argv), "args!",
               file = sys.stderr )
