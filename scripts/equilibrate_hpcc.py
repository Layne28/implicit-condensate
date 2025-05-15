'''
Randomize subunit positions starting from an 
initial lattice configuration.

Use (underdamped) Langevin dynamics for larger timestep
since this is equilibrium (not active) dynamics.

Input parameters:
(1) Initial lattice GSD file 
(2) Random seed
'''

import hoomd
import gsd.hoomd
import numpy as np
import argparse
import os
import random
from common import *

try:
    import cupy as cp
    CUPY_IMPORTED = True
except ImportError:
    CUPY_IMPORTED = False

#Define parameters
dt = 5e-3
kT = 1.0
epsilon = 1.0
eq_steps = 200000

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input_file",
                    help="File containing initial configuration",
                    type=str,
                    dest="input_file",
                    default="lattice.gsd")

parser.add_argument("-t", "--traj_output_dir",
                    help="Folder to place equilibration trajectory",
                    type=str,
                    dest="traj_output_dir",
                    default="$SCRATCH/capsid-assembly/llps/droplet/equilibration_trajectories")

parser.add_argument("-c", "--config_output_dir",
                    help="Folder to place final equilibrated configuration",
                    type=str,
                    dest="config_output_dir",
                    default="/work/laynefrechette/capsid-assembly/llps/droplet/initial_configurations")

parser.add_argument("-s", "--seed",
                    help="Random seed",
                    type=int,
                    dest="seed",
                    default=1)

parser.add_argument("-r", "--seed_file",
                    help="File containing random seeds",
                    type=str,
                    dest="seed_file",
                    default="$HOME/hoomd_seeds.txt")

args = parser.parse_args()

input_file = os.path.expandvars(args.input_file)
traj_output_dir = os.path.expandvars(args.traj_output_dir)
config_output_dir = os.path.expandvars(args.config_output_dir)
seed = args.seed
seed_file = os.path.expandvars(args.seed_file)

if not os.path.exists(traj_output_dir):
    os.makedirs(traj_output_dir)
if not os.path.exists(config_output_dir):
    os.makedirs(config_output_dir)
    
#Read seed from file
seednum = seed
with open(seed_file) as f:
    lines = f.readlines()
    seed_line = lines[seed-1]
    seed = int(seed_line.strip())
print('Using random seed: %d' % seed)

#Create simulation state
#check for GPU vs CPU and create simulation state
if CUPY_IMPORTED:
    print('Using GPU')
    xp = cp
    xpu = hoomd.device.GPU()
else:
    print('Using CPU')
    xp = np
    xpu = hoomd.device.CPU()
simulation = hoomd.Simulation(device=xpu, seed=seed)
simulation.create_state_from_gsd(filename=input_file)

#Get rigid body info
rigid, name, bead_types, bead_positions, diameters = create_capsomer()
rigid.create_bodies(simulation.state)

#Create integrator
integrator = hoomd.md.Integrator(dt=dt, integrate_rotational_dof=True)
integrator.rigid = rigid
filtered_bodies = hoomd.filter.Rigid(("center", "free"))
langevin = hoomd.md.methods.Langevin(filter=filtered_bodies, kT=kT)
integrator.methods.append(langevin)

#Set up interaction potential (hard sphere for equilibration)
cell = hoomd.md.nlist.Cell(buffer=3.0, exclusions=['body'])
r_dist = 1.25*max(diameters) #use slightly larger than max constituent diameter
r_cut = r_dist*2.0**(1.0/6.0)
wca = hoomd.md.pair.LJ(nlist=cell, default_r_cut=r_cut)
for type1 in [name]+list(set(bead_types)):
    for type2 in [name]+list(set(bead_types)):
        wca.params[(type1,type2)] = dict(epsilon=epsilon, sigma=r_dist)
        wca.r_cut[(type1,type2)] = r_cut
integrator.forces.append(wca)

simulation.operations.integrator = integrator

#logger to output final frame
input_file_end = input_file.split('/')[-1]
out_config = config_output_dir + '/' + input_file_end.replace('lattice','equil_start')
out_config = out_config.replace('.gsd', '_seed=%d.gsd' % seednum)
out_traj = traj_output_dir + '/' + input_file_end.replace('lattice', 'equil_traj')
out_traj = out_traj.replace('.gsd', '_seed=%d.gsd' % seednum)
gsd_writer = hoomd.write.GSD(filename=out_config, 
                             trigger=hoomd.trigger.Periodic(eq_steps-1),
                             mode='wb')
gsd_writer2 = hoomd.write.GSD(filename=out_traj, 
                             trigger=hoomd.trigger.Periodic(int(eq_steps/1000)),
                             mode='wb')
simulation.operations.writers.append(gsd_writer)
simulation.operations.writers.append(gsd_writer2)
#logger to output progress
log_period = int(eq_steps/20)
logger = hoomd.logging.Logger(categories=['scalar'])
logger.add(simulation, quantities=['timestep', 'tps'])
sim_writer = hoomd.write.Table(trigger=hoomd.trigger.Periodic(log_period), logger=logger)
simulation.operations.writers.append(sim_writer)

#run equilibration
simulation.run(eq_steps)
