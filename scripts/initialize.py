'''
Initialize capsomer rigid bodies and place them
on a lattice.

Input parameters: 
(1) Box length (L)
(2) no. of subunits (N) 
(3) output folder
'''

import hoomd
import gsd.hoomd
import numpy as np
import argparse
from pprint import pprint
import common
import os

#Set parameters
#Note: the unit length here is the distance from the center of a subunit
#to one of its attractor vertices

parser = argparse.ArgumentParser()

parser.add_argument("-N", "--n_subunits",
                    help="Number of subunits",
                    type=int,
                    dest="n_subunits",
                    default=60)

parser.add_argument("-L", "--L",
                    help="Box length",
                    type=float,
                    dest="L",
                    default=20)

parser.add_argument("-o", "--out_folder",
                    help="Folder to which to save file",
                    type=str,
                    dest="out_folder",
                    default="initial_configurations")

args = parser.parse_args()

n_subunits = args.n_subunits
L = args.L
out_folder = args.out_folder
 
#Compute derived quantities
V = L**3            #volume
rho = n_subunits/V  #total density

#Echo arguments to check they are what you expect
print('No. subunits:', n_subunits)
print('Volume:', V)
print('Concentration:', rho)

if not os.path.exists(out_folder):
    os.makedirs(out_folder)

#Create rigid body
rigid, name, bead_types, bead_positions, diameters = common.create_capsomer()

#Compute inertia tensor
r = np.array(bead_positions, dtype=float)
itensor = np.zeros((3,3))
#Just loop over attractors -- T and B are fictitious beads
for i in range(0,5):
    itensor += np.dot(r[i,:], r[i,:]) * np.identity(3) - np.outer(r[i,:], r[i,:])
    
#this particular tensor is already diagonal
inertia_components = [itensor[0][0], itensor[1][1], itensor[2][2]]

#Create snapshot and add info
snapshot = gsd.hoomd.Frame()
snapshot.particles.N = n_subunits
snapshot.configuration.box = [L, L, L, 0, 0, 0]
snapshot.particles.orientation = [(1,0,0,0)]*n_subunits
snapshot.particles.types = [name] + list(set(bead_types)) #tell hoomd about rigid body, then list constituent types
snapshot.particles.typeid = [0] * n_subunits
snapshot.particles.moment_inertia = inertia_components * n_subunits

#Set subunit positions
n_particle_x = int(np.ceil((n_subunits) ** (1/3)))
n_particle_y = int(np.ceil((n_subunits) ** (1/3)))
n_particle_z = int(np.ceil((n_subunits) ** (1/3)))
positions = np.zeros((n_subunits, 3), dtype=float)
xpos = np.linspace(-L / 2.0, L / 2.0, n_particle_x+1)[:-1]
ypos = np.linspace(-L / 2.0, L / 2.0, n_particle_y+1)[:-1]
zpos = np.linspace(-L / 2.0, L / 2.0, n_particle_z+1)[:-1]

#use coordinates in x1 to generate points in all 3 dimensions
c  = 0
print(n_particle_x*n_particle_y*n_particle_z)
for i in range(n_particle_x):
    for j in range(n_particle_y):
        for k in range(n_particle_z):
            positions[c][0] = xpos[i]
            positions[c][1] = ypos[j]
            positions[c][2] = zpos[k]
            c+=1

            if c >= n_subunits:
                break
        else:
            continue
        break
    else:
        continue
    break

snapshot.particles.position = positions

print('Check: num. particles created:', c)
print('Check: concentration:', c/V)

#Save snapshot to file
with gsd.hoomd.open(name=out_folder + '/lattice_N=%d_L=%.01f.gsd' % (n_subunits, L), mode='w') as f:
    f.append(snapshot)