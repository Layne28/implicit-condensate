'''
Simulate subunits partitioning into condensate without assembly.
'''

import hoomd
import gsd.hoomd
import numpy as np
import argparse
from common import *
import sys
import os

#Define parameters
dt = 1e-3
nsteps = 1000000
kT = 1.0

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input_file",
                    help="File containing initial configuration",
                    type=str,
                    dest="input_file",
                    default="equil_start.gsd")

parser.add_argument("-o", "--traj_output_dir",
                    help="Folder to place trajectory",
                    type=str,
                    dest="traj_output_dir",
                    default="partitioning_trajectories")

parser.add_argument("-s", "--seed",
                    help="Random seed",
                    type=int,
                    dest="seed",
                    default=1)

parser.add_argument("-e", "--bond_energy",
                    help="Energy between attractors",
                    type=str,
                    dest="E_bond",
                    default="6.0")

parser.add_argument("-Vr", "--volume_ratio",
                    help="Ratio of condensate to box volumes",
                    type=str,
                    dest="Vr",
                    default="1e-2")

args = parser.parse_args()

input_file = args.input_file
traj_output_dir = args.traj_output_dir
seed = args.seed
E_bond = float(args.E_bond)
Vr = float(args.Vr)

#Add parameters to output directory
input_gsd_name = input_file.split('/')[-1]
rho = float(([e for e in input_gsd_name.split('_') if e.startswith('rho=')][-1]).split('=')[-1])
Lx = float(([e for e in input_gsd_name.split('_') if e.startswith('Lx=')][-1]).split('=')[-1])
Ly = float(([e for e in input_gsd_name.split('_') if e.startswith('Ly=')][-1]).split('=')[-1])
Lz = float(([e for e in input_gsd_name.split('_') if e.startswith('Lz=')][-1]).split('=')[-1])

V = Lx*Ly*Lz
n_subunits = int(rho*V)
print('concentration: ', rho)
print('volume:', V)
print('no. subunits:', n_subunits)

traj_output_dir += '/rho=%f/Lx=%.01f_Ly=%.01f_Lz=%.01f/Vr=%.03f/E_bond=%f/seed=%d/' % (rho, Lx, Ly, Lz, Vr, E_bond, seed)

#Create output directory if it doesn't exist
if not os.path.exists(traj_output_dir):
    os.makedirs(traj_output_dir)

#Create simulation state
device = hoomd.device.GPU()
simulation = hoomd.Simulation(device=device, seed=seed)
simulation.create_state_from_gsd(filename=input_file)

#Get rigid body info
rigid, name, bead_types, bead_positions, diameters = create_capsomer()

#Create integrator
integrator = hoomd.md.Integrator(dt=dt, integrate_rotational_dof=True)
integrator.rigid = rigid
filtered_bodies = hoomd.filter.Rigid(("center", "free"))
int_method = hoomd.md.methods.Langevin(filter=filtered_bodies, kT=kT)
integrator.methods = [int_method]

#Set up interaction potential
#E_bond = 6.0
#Repulsion b/t T and B
top_sigma = 2.1
top_cut = top_sigma#*2**(1.0/6.0) #Ask: why not *2**(1/6)?
repulsive_eps = E_bond/4

bot_sigma = 1.8
bot_cut = bot_sigma#*2**(1.0/6.0) #Ask: why not *2**(1/6)?

full_type_list = [name] + list(set(bead_types))

cell = hoomd.md.nlist.Cell(buffer=3.0, exclusions=['body'])

wca = hoomd.md.pair.LJ(nlist=cell, default_r_cut=3.0, mode='shift')
morse = hoomd.md.pair.Morse(nlist=cell, default_r_cut=3.0, mode='shift')

#initialize interactions to zero
wca.params[(full_type_list, full_type_list)] = dict(epsilon=0, sigma=0)
wca.r_cut[(full_type_list, full_type_list)] = 0
morse.params[(full_type_list, full_type_list)] = dict(D0=0, r0=0, alpha=0)
morse.r_cut[(full_type_list, full_type_list)] = 0

#set WCA interactions
wca.params[("T", "T")] = dict(epsilon=repulsive_eps, sigma=top_sigma)
wca.r_cut[("T", "T")] = top_cut

wca.params[("T", "B")] = dict(epsilon=repulsive_eps, sigma=bot_sigma)
wca.r_cut[("T", "B")] = bot_cut

integrator.forces.append(wca)

#set Morse interactions
rho = 2.5 #sets interaction range
r0 = 0.2 #eq bond length of attractors
alpha = rho/r0

morse.params[("A", "A")] = dict(D0=E_bond, r0=r0, alpha=alpha)
morse.r_cut[("A", "A")] = 2.0

integrator.forces.append(morse)

simulation.operations.integrator = integrator

#Set up writer
gsd_writer = hoomd.write.GSD(filename=traj_output_dir + '/traj.gsd', 
                             trigger=hoomd.trigger.Periodic(int(nsteps/1000)),
                             mode='wb')
simulation.operations.writers.append(gsd_writer)
#logger to output progress
log_period = int(nsteps/20)
logger = hoomd.logging.Logger(categories=['scalar'])
logger.add(simulation, quantities=['timestep', 'tps'])
sim_writer = hoomd.write.Table(trigger=hoomd.trigger.Periodic(log_period), logger=logger)
simulation.operations.writers.append(sim_writer)

#run simulation
simulation.run(nsteps)
