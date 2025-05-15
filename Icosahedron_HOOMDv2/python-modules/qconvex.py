#!/usr/bin/env python
# 
# Takes qconvex output and turns it into a gnuplottable file
#
from __future__ import print_function

import sys, os, numpy as np

def get_vertices( f, nverts ):
    """ Reads the vertices. """
    verts = np.zeros( [nverts, 3], dtype = float )
    for i in range(0, nverts):
        line = f.readline()
        if line == "":
            print( "Unexpected end of file when "
                   "trying to read vertex {}!".format(i), file = sys.stderr )
            return None
        l = line.rstrip().split()
        verts[i] = float(l[0]), float(l[1]), float(l[2])
    return verts

def get_faces( f, vertices, nfaces ):
    """ Reads the faces. """
    # Construct the faces:
    faces = []
    for i in range(0,nfaces):
        line = f.readline()
        if line == "":
            print( "Unexpected end of file when "
                   "trying to read face {}!".format(i), file = sys.stderr )
            return None
        
        l = line.rstrip().split()
        verts_per_face = int(l[0])
        verts_for_face = np.zeros( verts_per_face, dtype = int )
        for j in range(0, verts_per_face):
            verts_for_face[j] = int(l[j+1])
        faces.append( (verts_per_face, verts_for_face) )
    return faces

def get_edges( vertices, faces, nedges ):
    """ Determines the edges. """
    edges = np.zeros( [nedges, 2], dtype = int )
    edge_idx = 0
    face_idx = 0
    for ff in faces:
        nverts = ff[0]
        vertices = ff[1]

        for i in range(0, nverts-1):
            vert1 = vertices[i]
            vert2 = vertices[i+1]
            if vert1 > vert2:
                vert1, vert2 = vert2, vert1

            # Check for duplicates:
            got_duplicate = False
            for j in range(0, edge_idx):
                if edges[j,0] == vert1 and edges[j,1] == vert2:
                    print( "      Skipping duplicate (", vert1, ",",
                           vert2, ")", file = sys.stderr )
                    got_duplicate = True
                    break
            if got_duplicate: continue
            
            edges[edge_idx,0] = vert1
            edges[edge_idx,1] = vert2
            print( "      Added edge", edge_idx+1, "(", vert1, ",", vert2, ")",
                   file = sys.stderr )
            edge_idx += 1
            
        face_idx += 1
    return edges

def get_meta_data(f):
    """ Gets the metadata from qconvex file. """

    # Meta is simple enough. Line 1 is dimension
    # Line 2 is verts/edges/faces
    line = f.readline()
    if line == "":
        print("Unexpected end of file when trying to read dimensions!",
              file = sys.stderr)

    # dims:
    l = line.rstrip()
    dims = int(l)
    print("  dims =", dims, file = sys.stderr)

    # verts, edges, faces:
    line = f.readline()
    if line == "":
        print("Unexpected end of file when trying to read # of edges",
              ", # of faces and # of vertices!", file = sys.stderr)
    data = line.rstrip().split()
    nverts, nfaces, nedges = int(data[0]), int(data[1]), int(data[2])
    print("  # of verts =", nverts, ", # of edges =", nedges,
          ", # of faces =", nfaces, file = sys.stderr)
    return nverts, nfaces, nedges


def extract_qconvex_info( f ):
    """ Reads file object and constructs gnuplot data from it. """

    nverts, nfaces, nedges = get_meta_data(f)
    
    
    # Now that verts is known, it is easy to parse the rest. Read verts first:
    verts = get_vertices( f, nverts )
    if verts is None: sys.exit(-2)

    faces = get_faces( f, verts, nfaces )
    if faces is None: sys.exit(-2)
    
    # Edges are easier, because they always are a pair of 2 points.
    # However, the file contains faces, which include duplicate edges.
    edges = get_edges( verts, faces, nedges )
    print("  Reconstructed", len(edges), "edges.", file = sys.stderr)

    return verts, faces, edges


def get_body_connectivity( verts, faces, edges ):
    """ Reads in a qconvex file and converts it to handy info. """

    Nbodies = len(faces)
    
    fc = 0
    n3s = 0
    for ff in faces:
        if ff[0] != 3:
            print( "Warning! Face", fc+1, "does not have 3 edges!",
                   file = sys.stderr )
        else:
            n3s += 1
        fc += 1

    assert n3s == Nbodies, "Did not find {} triangles!".format(Nbodies)

    def edge_equal( edge1, edge2 ):
        """ test if two edges are the same. """
        return ( (edge1[0] == edge2[0] and edge1[1] == edge2[1]) or
                 (edge1[0] == edge2[1] and edge1[1] == edge2[0]) )

    # 1) Identify each face with a triangle.
    # 2) Find which edges are shared between two triangles.

    body_connections = -np.ones( [Nbodies, 3], dtype = int )
    nconns_per_body = np.zeros( Nbodies, dtype = int )
    
    nconns = 0
    for i in range(0,Nbodies):
        face_i = faces[i]
        verts_i = faces[i][1]
        edges_i = []
        nverts_i = face_i[0]
        for j in range(0, face_i[0]):
            edges_i.append( (verts_i[j], verts_i[(j+1) % nverts_i]) )
        for j in range(0,i):

            if j in body_connections[i] or i in body_connections[j]:
                continue
            
            face_j = faces[j]
            verts_j = faces[j][1]
            edges_j = []
            nverts_j = face_j[0]
            for k in range(0, face_j[0]):
                edges_j.append( (verts_j[k], verts_j[(k+1) % nverts_j]) )

            for ei in edges_i:
                for ej in edges_j:
                    if edge_equal( ei, ej ):
                        
                        body_connections[i, nconns_per_body[i]] = j
                        body_connections[j, nconns_per_body[j]] = i

                        nconns_per_body[i] += 1
                        nconns_per_body[j] += 1
                        nconns += 1

    return body_connections


if __name__ == "__main__":
    """ Do nothing. """
