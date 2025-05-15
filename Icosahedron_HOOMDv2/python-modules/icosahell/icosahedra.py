from __future__ import print_function

import sys, numpy as np, math, copy
import icosahell.make_triangles

def four_col_file_to_list( fname, dtype ):
    """ reads a file with four columns to a list with values of dtype. """
    vals = []
    with open( fname, "r" ) as fp:
        lc = 0
        while True:
            line = fp.readline()
            if line == "":
                break
            l = line.rstrip().split()
            lc += 1
            assert len(l) == 4, "Line {} did not have 4 ints!".format(lc)
            idi = dtype(l[0])
            c1  = dtype(l[1])
            c2  = dtype(l[2])
            c3  = dtype(l[3])
            vals.append( [idi, c1, c2, c3] )
    print( "Read {} lines from file {}.".format(lc, fname), file = sys.stderr )
    return vals

def read_connectivity_network( fname ):
    """ Reads connectivity network from file. """
    return four_col_file_to_list( fname, int )

def read_bond_types( fname ):
    """ Reads bond types from file. """
    return four_col_file_to_list( fname, int )


def make_T1_triangulation():
    """ Makes a T1 triangulation. """
    Ntris = 20
    conns = read_connectivity_network( 'T1.conns' )
    assert len(conns) == Ntris, \
            "Connectivity network did not contain 20 triangles!"
    
    conn_arr = np.zeros( [Ntris, 3], dtype = int )
    bond_types = np.zeros( [Ntris, 3], dtype = int )
    for tt in conns:
        conn_arr[ tt[0] ] = ( tt[1], tt[2], tt[3] )
        bond_types[ tt[0] ] = (1,2,3)

    return [ conn_arr, bond_types ]
    
def make_T3_triangulation():
    """ Makes a T3 triangulation. """
    Ntris = 60
    conns = read_connectivity_network( 'T3.conns' )
    assert len(conns) == Ntris, \
            "Connectivity network did not contain 60 triangles!"
    
    conn_arr = np.zeros( [Ntris, 3], dtype = int )
    bond_types = np.zeros( [Ntris, 3], dtype = int )
    for tt in conns:
        conn_arr[ tt[0] ] = ( tt[1], tt[2], tt[3] )
        bond_types[ tt[0] ] = (1,2,3)
    return [ conn_arr, bond_types ]

def make_T4_triangulation():
    """ Makes a T4 triangulation. """
    Ntris = 80
    conns = read_connectivity_network( 'T4.conns' )
    types = read_bond_types( 'T4.btypes' )

    conn_arr = np.zeros( [Ntris, 3], dtype = int )
    bond_types = np.zeros( [Ntris, 3], dtype = int )
    
    assert len(conns) == Ntris, \
            "Connectivity network did not contain 80 triangles!"
    for tt in conns:
        conn_arr[ tt[0] ] = ( tt[1], tt[2], tt[3] )
    for bb in types:
        bond_types[ bb[0] ] = ( bb[1], bb[2], bb[3] )
    return [ conn_arr, bond_types ]
    
def make_T7_triangulation():
    """ Makes a T7 triangulation. """
    Ntris = 140
    
def make_octo_triangulation():
    """ Makes an octohedron triangulation. """
    Ntris = 8
    
def make_tetra_triangulation():
    """ Makes a tetrahedron triangulation. """
    Ntris = 4

def make_triangulation( tri_type = None ):
    """ Generates a triangulation with bond and triangle types. """
    if tri_type is None:
        tri_type = 'T1'

    if tri_type == 'T1':
        return make_T1_triangulation()
    if tri_type == 'T3':
        return make_T3_triangulation()
    if tri_type == 'T4':
        return make_T4_triangulation()
    if tri_type == 'T7':
        return make_T7_triangulation()
    if tri_type == 'octo':
        return make_octo_triangulation()
    if tri_type == 'tetra':
        return make_tetra_triangulation()

    raise RuntimeError( "Unknown triangulation type {}".format(tri_type) )


def is_valid_triangulation( conns, btypes, allowed_bonds ):
    """ Checks whether or not the given triangulation is valid. """

    legal_bonds = []
    for ab in allowed_bonds:
        legal_bonds.append( ab )
        if ab[0] != ab[1]:
            legal_bonds.append( (ab[1], ab[0]) )
    print( "Checking whether {} bonds are legal, with legal bonds [ ".
           format( int(3*len(conns) / 2) ), end = "", file = sys.stderr )
    for lb in legal_bonds:
        print( "( {}, {} ), ".format(lb[0],lb[1]), end = "", file = sys.stderr )
    print( " ]", file = sys.stderr )

    Ntris = len(conns)
    for i in range(0, Ntris):
        for k in range(0,3):
            ti = btypes[i,k]
            j  = conns[i,k]

            for reverse_i in range(0,3):
                if conns[j, reverse_i] == i:
                    break
            if conns[j, reverse_i] != i:
                print( "Triangulation is not valid! Triangle {} connects to {} "
                       "but {} does not connect back to {}!".format(
                           i, j, j, i, file = sys.stderr ) )
                print( "i = {}, j = {}, reverse_i = {}, "
                       "conns[i] = [{}, {}, {}], conns[j] = [{}, {}, {}]".
                       format( i, j, reverse_i, conns[i,0], conns[i,1],
                               conns[i,2], conns[j,0], conns[j,1], conns[j,2] ),
                       file = sys.stderr )
                return False
            tj = btypes[j, reverse_i]

            if not (ti,tj) in legal_bonds:
                print( "Triangulation is not valid! Bond between {} and {} "
                       "has type ({}, {}) which is not allowed!".format(
                           i, j, ti, tj, file = sys.stderr ) )
                return False
    return True
            


def test_stuff():
    """ Tests the available connection and bond type files. """
    allowed_bonds_T1 = [ (1,1), (2,2), (1,2), (1,3), (2,3), (3,3) ]
    allowed_bonds_T3 = [ (1,2), (3,3) ]
    allowed_bonds_T4 = [ (1,2), (3,4), (3,5), (3,6) ]
    
    tri_T1 = make_triangulation('T1')
    tri_T3 = make_triangulation('T3')
    tri_T4 = make_triangulation('T4')

    print("Checking T1 triangulation...", file = sys.stderr)
    if is_valid_triangulation( tri_T1[0], tri_T1[1], allowed_bonds_T1 ):
        print( "T1 triangulation is valid!", file = sys.stderr )
    else:
        print( "T1 triangulation is invalid!", file = sys.stderr )
        sys.exit(-1)

    print("", file = sys.stderr)
    print("Checking T3 triangulation...", file = sys.stderr)
    if is_valid_triangulation( tri_T3[0], tri_T3[1], allowed_bonds_T3 ):
        print( "T3 triangulation is valid!", file = sys.stderr )
    else:
        print( "T3 triangulation is invalid!", file = sys.stderr )
    
    print("", file = sys.stderr)
    print("Checking T4 triangulation...", file = sys.stderr)
    if is_valid_triangulation( tri_T4[0], tri_T4[1], allowed_bonds_T4 ):
        print( "T4 triangulation is valid!", file = sys.stderr )
    else:
        print( "T4 triangulation is invalid!", file = sys.stderr )
    
    
if __name__ == "__main__":
    make_T1_input()
    
