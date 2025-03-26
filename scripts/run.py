import hoomd
import gsd.hoomd
import numpy as np
import argparse
from common import *
import sys
import os

def main():

    #####################################
    #Define parameters
    #####################################

    dt = 5e-3
    kT = 1.0
    gamma=10.0
    gamma_r=4*gamma/3

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
                        default="$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories")

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

    parser.add_argument("-eb", "--bond_energy",
                        help="Energy between attractors",
                        type=str,
                        dest="E_bond",
                        default="6.0")
    
    parser.add_argument("-t", "--sim_time",
                        help="total simulation time",
                        type=str,
                        dest="sim_time",
                        default="2e5")

    parser.add_argument("-f", "--record_time_freq",
                        help="time interval at which to output configurations",
                        type=str,
                        dest="record_time_freq",
                        default="20.0")
    
    parser.add_argument("-ec", "--condensate_energy",
                        help="Well depth of condensate",
                        type=str,
                        dest="E_cond",
                        default="10.0")

    parser.add_argument("-Vr", "--volume_ratio",
                        help="Ratio of condensate to box volumes",
                        type=str,
                        dest="Vr",
                        default="1e-2")
    
    parser.add_argument("-rho", "--rho",
                        help="Specificity of Morse potential",
                        type=str,
                        dest="rho",
                        default="2.5")

    args = parser.parse_args()

    input_file = os.path.expandvars(args.input_file)
    traj_output_dir = os.path.expandvars(args.traj_output_dir)
    seed = args.seed
    seed_file = os.path.expandvars(args.seed_file)
    E_bond = float(args.E_bond)
    E_cond = float(args.E_cond)
    Vr = float(args.Vr)
    rho = float(args.rho)
    sim_time = float(args.sim_time)
    record_time_freq = float(args.record_time_freq)

    #Read seed from file
    seednum = seed
    with open(seed_file) as f:
        lines = f.readlines()
        seed_line = lines[seed-1]
        seed = int(seed_line.strip())
    print('Using random seed: %d' % seed)

    #Add parameters to output directory
    input_gsd_name = input_file.split('/')[-1]
    n_subunits = int(([e for e in input_gsd_name.split('_') if e.startswith('N=')][-1]).split('=')[-1])
    L = float(([e for e in input_gsd_name.split('_') if e.startswith('L=')][-1]).split('=')[-1])

    #derived quantities
    nsteps = int(sim_time/dt)
    print('nsteps:', nsteps)
    freq=int(record_time_freq/dt)
    V = L**3
    conc = n_subunits/V
    V_cond = V*Vr
    R_cond = (V_cond/(4.0*np.pi/3.0))**(1.0/3)
    print('concentration: ', conc)
    print('volume:', V)
    print('no. subunits:', n_subunits)
    print('condensate radius:', R_cond)

    if rho==2.5: #default specificity
        traj_output_dir += '/N=%d/L=%.01f/Vr=%.03f/E_cond=%f/E_bond=%f/gamma_r=%f/seed=%d/' % (n_subunits, L, Vr, E_cond, E_bond, gamma_r, seednum)
    else:
        traj_output_dir += '/N=%d/L=%.01f/Vr=%.03f/E_cond=%f/E_bond=%f/gamma_r=%f/rho=%f/seed=%d/' % (n_subunits, L, Vr, E_cond, E_bond, gamma_r, rho, seednum)

    #Create output directory if it doesn't exist
    if not os.path.exists(traj_output_dir):
        os.makedirs(traj_output_dir)
        

    #####################################
    #Create simulation state
    #####################################
    device = hoomd.device.GPU()
    simulation = hoomd.Simulation(device=device, seed=seed)
    simulation.timestep=0
    simulation.create_state_from_gsd(filename=input_file)

    #Get rigid body info
    rigid, name, bead_types, bead_positions, diameters = create_capsomer()
    full_type_list = [name] + list(set(bead_types))

    #Create integrator
    integrator = hoomd.md.Integrator(dt=dt, integrate_rotational_dof=True)
    integrator.rigid = rigid
    filtered_bodies = hoomd.filter.Rigid(("center", "free"))
    int_method = hoomd.md.methods.Langevin(filter=filtered_bodies, kT=kT, default_gamma=gamma, default_gamma_r=(gamma_r,gamma_r,gamma_r))
    integrator.methods = [int_method]

    #####################################
    #Set up condensate ("well") potential
    #####################################

    walls = [hoomd.wall.Sphere(radius=R_cond, origin=(0,0,0), inside=False)]
    condensate = hoomd.md.external.wall.Morse(walls=walls)
    #Set condensate interactions with everything except subunit c.o.m. to zero
    condensate.params[full_type_list] = {"D0": 0, "alpha": 10.0, "r0": 0.0, "r_cut": 3.0} 
    condensate.params["Capsomer"] = {"D0": E_cond, "alpha": 10.0, "r0": 0.0, "r_cut": 3.0}
    integrator.forces.append(condensate)

    #####################################
    #Set up interaction potential
    #####################################
    #Repulsion b/t T and B
    top_sigma = 2.1
    top_cut = top_sigma
    repulsive_eps = 1.0

    bot_sigma = 1.8
    bot_cut = bot_sigma

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
    r0 = 0.2 #eq bond length of attractors
    alpha = rho/r0

    morse.params[("A", "A")] = dict(D0=E_bond, r0=r0, alpha=alpha)
    morse.r_cut[("A", "A")] = 2.0

    integrator.forces.append(morse)

    simulation.operations.integrator = integrator

    #####################################
    #Set up writer
    #####################################
    gsd_writer = hoomd.write.GSD(filename=traj_output_dir + '/traj.gsd', 
                                trigger=hoomd.trigger.Periodic(freq),
                                mode='wb')
    simulation.operations.writers.append(gsd_writer)
    
    #logger to output progress
    progress_logger = hoomd.logging.Logger(categories=['scalar', 'string'])
    progress_logger.add(simulation, quantities=['timestep', 'tps'])
    log_period = freq*10
    progress_logger[('Time', 'time')] = (lambda: simulation.operations.integrator.dt*simulation.timestep, 'scalar')
    table = hoomd.write.Table(trigger=hoomd.trigger.Periodic(period=log_period),
                              logger=progress_logger)
    simulation.operations.writers.append(table)

    #####################################
    #run simulation
    #####################################
    simulation.run(nsteps)

main()