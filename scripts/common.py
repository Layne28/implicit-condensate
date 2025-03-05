import hoomd
import gsd.hoomd
import numpy as np

def create_capsomer():
    '''
    Construct pentagonal subunits
    '''

    #Position attractor ("A") beads at the fifth roots of unity
    #(in the body frame)

    theta = 2.0*np.pi/5.0
    bead_positions = []
    for i in range(5):
        root = (np.cos(i*theta), np.sin(i*theta), 0)
        bead_positions.append(root)

    bead_types = ["A"]*5

    #Position fictitious edge ("E") beads at the midpoints of
    #bonds between attractor beads.
    for i in range(5):
        root1 = np.array([np.cos(i*theta), np.sin(i*theta),0])
        root2 = np.array([np.cos((i+1)*theta), np.sin((i+1)*theta),0])
        midpt = (root1+root2)/2.0
        bead_positions.append(tuple(midpt))
        bead_types.append("E")

    #Position asymmetric top ("T") and bottom ("B") particles
    #that exclude volume and impose preferred curvature

    bead_types.append("T")
    bead_types.append("B")

    bead_positions.append((0,0,0.5))
    bead_positions.append((0,0,-0.5))

    #Create rigid body
    orientations = [(1,0,0,0)]*12
    charges      = [0.0]*12
    diameters    = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 2.1, 1.8]

    rigid = hoomd.md.constrain.Rigid()
    name = "Capsomer"

    #HOOMD version 4 does not have "charges" or "diameters"
    if hoomd.version.version.startswith('4'):
        rigid.body[name] = {
            "constituent_types": bead_types,
            "positions":         bead_positions,
            "orientations":      orientations
        }
    else:
        rigid.body[name] = {
            "constituent_types": bead_types,
            "positions":         bead_positions,
            "orientations":      orientations, 
            "charges":           charges,
            "diameters":         diameters
        }

    return rigid, name, bead_types, bead_positions, diameters