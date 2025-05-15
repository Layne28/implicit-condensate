from __future__ import print_function
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import sys
import inspect
import time

#set a path to the module folder and add it to the path
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
mod_dir = current_dir + "/python-modules/"
sys.path.insert(0, mod_dir) 
print(sys.path)

import hoomd, hoomd.md
import numpy as np, math, copy, quaternion

import option_parser
import icosahell, icosahell.icosahedra
import icosahell.make_triangles, icosahell.ico_lattice

import tetrahedron
import gsd, gsd.pygsd, gsd.hoomd

NA = 6.022140857e23

# Function for potential well representing the phase separated compartment :
def well(r,rmin,rmax,r0_well,epsilon,alpha=10):#def lj(r, rmin, rmax, epsilon, sigma):
	if r<r0_well :
		V=-epsilon
		F=0
	else :
		
		V= epsilon*(np.exp(-2*alpha*(r-r0_well)) -2*np.exp(-alpha*(r-r0_well)))
		F = 2 *alpha * epsilon * (np.exp(-2*alpha*(r-r0_well)) -np.exp(-alpha*(r-r0_well))) 
	
	return (V, F)

def genSpheres(N, box_dim, R):
    #generate N spheres of radius R in a given box - periodic BC

    #init a list to store particles
    positions = []

    #subtract R/2 from box dimensions to satisfy no overlap for particles close to edges
    effective_box = np.array(box_dim) - R / 2.0

    #get the first particle
    pos = np.multiply(effective_box, [np.random.random() for i in range(3)]) + R / 4.0 - box_dim/2.0
    positions.append(pos)
    distributed = 1

    #get new particles, check for overlap
    loop_count = 0
    loop_tol   = 50000
    while (distributed < N and loop_count < loop_tol):
        pos = np.multiply(effective_box, [np.random.random() for i in range(3)]) + R/4.0 - box_dim/2.0

        overlap = False
        for particle in positions:
            d = np.linalg.norm(pos-particle)
            if (d < 2*R):
                overlap=True
                break
        if (not overlap):
            positions.append(pos)
            distributed += 1

        loop_count += 1

    if (loop_count < loop_tol):
        print("Generated configuration in {} iterations".format(loop_count))
        for i in range(N):
            positions[i] = positions[i].flatten().tolist()
        success = True
    else:
        print("Warning: could not generate configuration in allotted time.\n" + 
                 "Please reduce N or use a bigger box.\n" + 
                 "Defaulting to lattice construction + equilibration")
        success = False

    return positions, success

def get_mol_diameter( b, mol_id ):
    """ Determines the 'diameter' of given molecule. """
    xs = []
    for i in range(0, b.meta.N):
        if b.mol[i] == mol_id:
            xs.append(b.x[i])
    d2  = 0
    for xi in xs:
        for xj in xs:
            dx = xi[0] - xj[0]
            dy = xi[1] - xj[1]
            dz = xi[2] - xj[2]
            r2 = dx*dx + dy*dy + dz*dz
            if r2 > d2:
                d2 = r2
    return math.sqrt(d2)


def reload_rigid_system_gsd( traj_file, res_name, N_rows, Nbeads, lengths,
                             angles, patch_dist, min_dist, shift_top_down = False ):
    """ Reloads init file. All triangle settings __must__ match! """
    # Check the last frame in traj_file:
    gsd_fp = gsd.pygsd.GSDFile( open(traj_file, mode = 'rb') )
    n_frames = gsd_fp.nframes
    print( "Given trajectory has", n_frames, "frames in it",
           file = sys.stderr )

    system = hoomd.init.read_gsd( traj_file, restart = res_name )

    N_per_row = Nbeads
    N_rows = 3
    N_edge = 3

    print( "lengths are", lengths, "in sim units.", file = sys.stderr )
    X = make_general_T_structure( N_rows, Nbeads, lengths, angles,
                                  patch_dist, min_dist )
    if shift_top_down:
        X = shift_top(X)

    N_parts = len(X)
    constituent_types = ['1']*N_parts
    # Assign the patches the right type:
    constituent_types[N_parts-6] = '2'
    constituent_types[N_parts-5] = '3'
    constituent_types[N_parts-4] = '4'
    constituent_types[N_parts-3] = '5'
    constituent_types[N_parts-2] = '6'
    constituent_types[N_parts-1] = '7'


    rigid = hoomd.md.constrain.rigid()
    rigid.set_param( 'Center1', types = constituent_types, positions = X )
    rigid.create_bodies()

    return system


def calc_mom_inertia( X, x_avg, m ):
    """ Calculates the moment of inertia of body in given data file. """

    mom_inertia = 0.0

    for x in X:
        ri_x = x[0] - x_avg[0]
        ri_y = x[1] - x_avg[1]
        ri_z = x[2] - x_avg[2]
        r2 = ri_x*ri_x + ri_y*ri_y + ri_z*ri_z
        mom_inertia += m * r2

    return mom_inertia


def side_to_types( t1, t2 ):
    """ Converts two sides to the atom types that should interact.
    This implementation provides the flexibility for implementing different
    interaction matrices for the triangular system."""
    if t1 > t2:
        t1,t2 = t2,t1
    side_pairs = []
    if t1 == 1 and t2 == 1:
        side_pairs.append( (2,3) )
    if t1 == 1 and t2 == 2:
        side_pairs.append( (2,5) )
        side_pairs.append( (3,4) )
    if t1 == 1 and t2 == 3:
        side_pairs.append( (2,7) )
        side_pairs.append( (3,6) )
    if t1 == 2 and t2 == 2:
        side_pairs.append( (4,5) )
    if t1 == 2 and t2 == 3:
        side_pairs.append( (4,7) )
        side_pairs.append( (5,6) )
    if t1 == 3 and t2 == 3:
        side_pairs.append( (6,7) )
    return side_pairs


def set_pair_interactions( side_energies, force_style, alpha, dom, R_domain = 30.0 ):
    """ Sets the pair interactions. """

    nl = hoomd.md.nlist.cell(r_buff = 3.0)
    #nl = hoomd.md.nlist.stencil( r_buff = 3.0 )

    # Interaction among subunits :
    hoomd_pair = None
    if force_style == 'lj':
        rc = 3.0
        hoomd_pair = hoomd.md.pair.lj(r_cut = rc, nlist = nl)
        ss  = 1.0
        # Cutoff for WCA Repulsion
        rc0 = ss*2.0**(1.0/6.0)
        # Cutoff for Attractive LJ interactions
        rc  = 3.0
        sc = 0
    elif force_style == 'morse':
        rc = 3.0
        hoomd_pair = hoomd.md.pair.morse(r_cut = rc, nlist = nl)
        ss = 1.0
        # Cutoff for hard repulsive interactions :
        rc0 = 1.0
        sc = 0.0
    else:
        print( "Unknown force style", force_style, file = sys.stderr )
        sys.exit(-3)

    ee = 0.0
    Ne = 0.0
    for se in side_energies:
        ee += se[1]
        Ne += 1.0
    if Ne == 0:
        eavg = 0.0
    else:
        eavg = ee / Ne
    # Set all of them to purely repulsive:
    for t1 in range(1,8):
        hoomd_pair.pair_coeff.set( str(t1), 'D', epsilon = 0.0, sigma = 0.0, r_cut = 0.0 )

        for t2 in range(1,8):
            if force_style == "lj":
                hoomd_pair.pair_coeff.set( str(t1), str(t2), epsilon = eavg,
                                           sigma = ss, r_cut = rc0 )
            elif force_style == "morse":
                hoomd_pair.pair_coeff.set( str(t1), str(t2), D0 = eavg,
                                           r0 = rc0, r_cut = rc0, alpha = alpha )
        
    hoomd_pair.pair_coeff.set( ['Center1', 'D'], 'D', epsilon = 0.0, sigma = 0.0, r_cut = 0.0 )

    for se in side_energies:
        print("At side", sc, file = sys.stderr)
        sc += 1
        side_tuple = se[0]
        ee = se[1]
        if ee == 0:
            r_cut = rc0
            ss = 1.0
        else:
            r_cut = rc
            ss = 1.0

        s1 = side_tuple[0]
        s2 = side_tuple[1]

        print("Put sides ",s1,"<-->",s2," to eps =", ee, ", rc =", r_cut, file = sys.stderr)
        particle_type_pairs = side_to_types( s1, s2 )
        for ptypes in particle_type_pairs:
            pt1 = ptypes[0]
            pt2 = ptypes[1]
            print("Putting", str(pt1), "<-->", str(pt2), " to eps =", ee, file = sys.stderr)

            if force_style == 'lj':
                hoomd_pair.pair_coeff.set( str(pt1), str(pt2), epsilon=ee,
                                           sigma=ss, r_cut = r_cut)
            elif force_style == 'morse':
                hoomd_pair.pair_coeff.set( str(pt1), str(pt2), D0 = ee,
                                           alpha = alpha, r0 = ss, r_cut = r_cut )

    for t1 in range(1,8):
        if force_style == 'lj':
            hoomd_pair.pair_coeff.set( 'Center1', str(t1), epsilon = 0, sigma = rc0 )
            hoomd_pair.pair_coeff.set( 'Center1', 'Center1', epsilon = 0, sigma = rc0)
        elif force_style == 'morse':
            hoomd_pair.pair_coeff.set( 'Center1', str(t1), D0 = 0, r0 = rc0, alpha = alpha )
            hoomd_pair.pair_coeff.set( 'Center1', 'Center1', D0 = 0, r0 = rc0, alpha = alpha )

    # Interaction with the phase separated compartment :
    nbond = dom
    table = hoomd.md.pair.table(width=1000, nlist=nl)
    table.pair_coeff.set(['Center1','1','2','3','4','5','6','7','D'],['Center1','1','2','3','4','5','6','7','D'], func=well, rmin=0, rmax=0.1,  coeff=dict(r0_well=0,epsilon=0))
    table.pair_coeff.set('D', 'Center1', func=well, rmin=0, rmax=R_domain*1.2, coeff=dict(r0_well=R_domain,epsilon=nbond))

    return nl

def prepare_parser():
    """ Prepares an option parser. """
    parser = option_parser.file_parser()

    parser.add_option( 'lammps_data_name', str, '' )
    parser.add_option( 'init_gsd_file', str, '' )
    parser.add_option( 'seed', int, 1 )
    parser.add_option( 'molecule_size', float, 60.0 )
    parser.add_option( 'target_concentration', float, 5e-5 )
    parser.add_option( 'energy_set', str, 'T1_1' )

    parser.add_option( 'dry_run', bool, False )
    parser.add_option( 'restart_run_instead', bool, True)
    parser.add_option( 'add_ico_bonds', bool, False )
    parser.add_option( 'connections_file', str, '' )
    parser.add_option( 'bond_type_file', str, '' )

    parser.add_option( 'restart', bool, False )
    parser.add_option( 'restart_file', str, 'triangles_restart.gsd' )
    parser.add_option( 'start_file', str, 'triangles_start.gsd' )
    parser.add_option( 'trajectory_file', str, 'triangles.gsd' )
    parser.add_option( 'log_file', str, 'triangles_log.dat' )

    parser.add_option( 'scale_initial_triangle_positions', float, 1.0 )
    # Triangle settings:
    parser.add_option( 'triangle_L1', float, 1.0 )
    parser.add_option( 'triangle_L2', float, 1.0 )
    parser.add_option( 'triangle_L3', float, 1.0 )
    parser.add_option( 'triangle_length_scale', float, 1.0 )

    parser.add_option( 'triangle_angle_01', float, 0.4 )
    parser.add_option( 'triangle_angle_12', float, 0.4 )
    parser.add_option( 'triangle_angle_20', float, 0.4 )
    parser.add_option( 'N_triangles', int, 200 )
    
    parser.add_option( 'triangle_Nbeads', int, 6 )

    # Some simulation options:

    parser.add_option( 't_dump', int, 25000 )
    parser.add_option( 't_run', int, 20000000 )
    parser.add_option( 't_log', int, 10000 )
    parser.add_option( 't_step', float, 0.0025 )
    parser.add_option( 'run_upto', bool, False )

    # Interaction settings:
    parser.add_option( 'force_style', str, 'lj' )
    parser.add_option( 'force_alpha', float, 6.0 )

    parser.add_option( 'side_energies', 'float_list',
                       [ 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 ] )
    parser.add_option( 'side_energy_factor', float, 8.0 )
    parser.add_option( 'shift_top_down', bool, False )
    parser.add_option( 'psdomain', float, 4.0 )
    return parser


def get_pair_settings(energies):
    """ Returns pair energy list for a T3. """
    # A list of side pairs and the epsilon they go with. Epsilon
    # of 0 means the side is disabled.

    sides = [ (1,1), (1,2), (1,3), (2,2), (2,3), (3,3) ]
    side_energies = zip( sides, energies )

    list_energies = list(side_energies)
    print("Side energies: ", file = sys.stderr, end = "")
    for ss in list_energies:
        print(" ", ss, file = sys.stderr, end = "")
    print("", file = sys.stderr)
    return list_energies



def shift_top(X):
    """ Shifts the top row of the particles in X down by half the layer space."""
    max_z = np.max(X[:,2])
    min_z = np.min(X[:,2])
    L = max_z - min_z
    dz = 0.2*L
    delta = 1e-6
    print( "Shifting tops down!", file = sys.stderr )

        # for each particle in the top row there are corresponding particles
    # in the other two rows. The easiest way to shift is to find those
    # and extrapolate along the line that goes through them.
    Np = len(X) - 6 # -6 for the patches.
    stride = int(Np/3)
    print( "Stride is", stride, "Np =", Np, file = sys.stderr )

    for i in range(len(X)):
        if X[i,2] > max_z - delta:
            # the top also has to be shifted out to make sure
            # the dihedral angle is still correct.
            i0 = i - 2*stride
            i1 = i - stride
            v = X[i1] - X[i0]
            v /= np.linalg.norm(v)
            print( "Vector to", i, " points along", i0, i1,
                   "as", v[0], v[1], v[2], file = sys.stderr )

            X[i,2] -= dz*v[2]
            X[i,1] -= dz*v[1]
            X[i,0] -= dz*v[0]

    return X;


def make_general_T_structure( Nrows, Nbeads, lengths, angles,
                              patch_dist, min_dist = 0.0 ):
    """ Makes a general triangle. """

    L1 = lengths[0]
    L2 = lengths[1]
    L3 = lengths[2]

    # Remap L1 to 0.5*Nbeads.
    tilt1 = angles[0]
    tilt2 = angles[1]
    tilt3 = angles[2]

    # Make the length so that it is 0.5*Nbeads long.
    sim_scale = 0.5*Nbeads / L1
    L1_sim = L1 * sim_scale

    largest_tilt = np.max( [ tilt1, tilt2, tilt3 ] )
    print( "L1 =", L1, ", L2 =", L2, file = sys.stderr )
    l = 1 - 1.0 * math.tan(largest_tilt)
    scale = 1 - l

    print( "Top row is at max a factor of", scale, " further inward.",
           file = sys.stderr )
    print( "Therefore, the particle distance there will be",
           scale * L1_sim, file = sys.stderr )

    print( "For", Nbeads, "beads the real lengths become", L1, L2, L3,
           file = sys.stderr)

    verts = tetrahedron.generate_truncated( L1, L2, L3, tilt1, tilt2, tilt3, 1.0 )
    X = icosahell.make_triangles.make_triangles( Nrows, Nbeads, verts,
                                                 patch_dist, min_dist )

    return X


def init_T_structure( N_tris, lengths, angles, Nbeads, patch_dist,
                      target_conc, molecule_size, shift_top_down = False ):
    """ Initializes system. """
    N_per_row = Nbeads
    N_rows = 3
    N_edge = 3

    print( "lengths are", lengths, "in sim units.", file = sys.stderr )
    min_dist = 0.0
    X = make_general_T_structure( N_rows, Nbeads, lengths, angles,
                                  patch_dist, min_dist )
    if shift_top_down:
        X = shift_top(X)
    N_parts = len(X)
    l_tri = np.max( lengths )

    l_tri3 = l_tri ** 3.0
    msize3 = mol_size ** 3.0
    len_scale = mol_size / l_tri
    len_scale3 = len_scale ** 3

    edge = 200.0
    edge_real_units = edge*len_scale
    target_vol = edge_real_units**(3.0)
    N_tris = int((target_vol*target_conc)*NA)

    print( "We have", N_tris, "triangles of length", l_tri, "which is",
           l_tri*len_scale, "m", file = sys.stderr )
    print( "To reach a concentration of", target_conc,
           "mM we should have a volume of", target_vol, "m^3.", file = sys.stderr )
    print( "That means a square box with edges of", edge_real_units,
           "m or ", edge, " sim units.", file = sys.stderr )

    print( "", file = sys.stderr )

    half_edge = 0.5*edge
    quart_edge = 0.5*half_edge

    min_edge = 20
    if edge < min_edge: edge = min_edge

    mybox = hoomd.data.boxdim( Lx = edge, Ly = edge, Lz = edge )
    snap = hoomd.data.make_snapshot(N_tris+1, box = mybox)

    print( "My box is", edge, file = sys.stderr )

    x_avg = np.array( [ np.average( X[:,0] ),
                        np.average( X[:,1] ),
                        np.average( X[:,2] ) ] )
    print( "<x> =", x_avg, file = sys.stderr )
    mom_inertia = calc_mom_inertia( X, x_avg, 1.0 )

    # For HOOMD it's important to keep the center particles and the
    # constituent particles separate.


    snap.particles.types = [ 'Center1', '1', '2', '3', '4', '5', '6', '7', 'D' ]

    N_per_dim = int( 1.5*math.ceil( N_tris ** (1.0/3.0) ) )
    lattice_const = math.floor( edge / N_per_dim )
    Xcc, signs = icosahell.ico_lattice.generate_cubic( N_tris, lattice_const )

    Xc = np.zeros( [len(Xcc), 3], dtype = float )
    Xc, bool1a = genSpheres(N_tris, edge, 2.5)

    # Add the particles and stuff:
    for i in range(0, len(Xcc)):
        snap.particles.position[i] = Xc[i]
        snap.particles.moment_inertia[i] = mom_inertia

    snap.particles.position[N_tris] = np.array([0,0,0])
    snap.particles.typeid[N_tris] = len(snap.particles.types) - 1

    system = hoomd.init.read_snapshot( snap )
    rigid = hoomd.md.constrain.rigid()
    constituent_types = ['1']*N_parts

    # Assign the patches the right type:
    constituent_types[N_parts-6] = '2'
    constituent_types[N_parts-5] = '3'
    constituent_types[N_parts-4] = '4'
    constituent_types[N_parts-3] = '5'
    constituent_types[N_parts-2] = '6'
    constituent_types[N_parts-1] = '7'


    rigid.set_param( 'Center1', types = constituent_types, positions = X )
    rigid.create_bodies()

    return system



if __name__ == "__main__":

    if len( sys.argv ) < 2:
        print( "Pass a config file!", file = sys.stderr )
        sys.exit(-1)

    parser = prepare_parser()
    opts = parser.read_file( sys.argv[1] )

    user_argv = []
    hoomd_args = ""
    to_user = False
    if len( sys.argv ) > 2:
        i = 2
        while i < len(sys.argv):
            arg = sys.argv[i]
            if arg == "--user":
                to_user = True
                i += 1
                continue

            if to_user:
                user_argv.append( arg )
            else:
                hoomd_args += arg + " "
            i += 1

    # Override options from command line.
    if len( user_argv ) > 0:
        print( "Parsing rest of args", user_argv, file = sys.stderr )
        opts = parser.set_from_cmdline( user_argv, opts )

    parser.write( ".parsed_options.conf", opts,
                  "# Options as parsed by hoomd_triangle.py" )


    # Grab the options from the dictionary:
    energy_set = opts['energy_set'][0]
    make_ico = opts['add_ico_bonds'][0]
    target_conc = opts['target_concentration'][0]
    dname = opts['lammps_data_name'][0]
    mol_size = opts['molecule_size'][0]
    seed = opts['seed'][0]
    in_file = opts['init_gsd_file'][0]
    res_file = opts['restart_file'][0]
    restart = opts['restart'][0]
    traj_file = opts['trajectory_file'][0]
    log_file = opts['log_file'][0]
    N_triangles = opts['N_triangles'][0]
    start_file = opts['start_file'][0]

    t_dump = opts['t_dump'][0]
    t_run  = opts['t_run'][0]
    t_log  = opts['t_log'][0]

    triangle_Ls = [ opts['triangle_L1'][0],
                    opts['triangle_L2'][0],
                    opts['triangle_L3'][0] ]
    triangle_L_scale = opts['triangle_length_scale'][0]
    triangle_angles = [ opts['triangle_angle_01'][0],
                        opts['triangle_angle_12'][0],
                        opts['triangle_angle_20'][0] ]
    triangle_Nbeads = opts['triangle_Nbeads'][0]
    t_step = opts['t_step'][0]
    conns_file = opts['connections_file'][0]
    btype_file = opts['bond_type_file'][0]

    triangle_Ls[0] *= triangle_L_scale
    triangle_Ls[1] *= triangle_L_scale
    triangle_Ls[2] *= triangle_L_scale


    force_style = opts['force_style'][0]
    force_alpha = opts['force_alpha'][0]
    es = opts['side_energies'][0]
    ef = opts['side_energy_factor'][0]
    energy_set = [ ef*x for x in es ]
    dom = opts['psdomain'][0]

    shift_top_down = opts['shift_top_down'][0]

    run_upto_instead = opts['run_upto'][0]

    dry_run = opts['dry_run'][0]
    if dry_run:
        print("This was only a dry run... Stopping after parsing options.",
                file = sys.stderr )
        sys.exit(0)

    if make_ico:
        print("Adding explicit bonds between icosahedral parts.",
              file = sys.stderr)
    else:
        print("Not adding explicit bonds between icosahedral parts.",
              file = sys.stderr)

    side_energies = get_pair_settings( energy_set )
    hoomd.context.initialize( hoomd_args )

    ico_conc_factor = 1.8
    if make_ico:
        target_conc *= ico_conc_factor
        no_force_initially = False

    if restart:
        print("Reloading state from ", res_file, "!", file = sys.stderr )
        print("Init file is ", in_file, "!", file = sys.stderr )

        N_rows = 3
        system = reload_rigid_system_gsd( in_file, res_file, N_rows,
                                          triangle_Nbeads, triangle_Ls,
                                          triangle_angles, 1.0, 0, shift_top_down )

        group_all = hoomd.group.all()
        hoomd.dump.gsd( ".restart_reload_test.gsd", period = None,
                        group = group_all, overwrite = True )
    else:
        print("Initting run...", file = sys.stderr)
        system = init_T_structure( N_triangles, triangle_Ls, triangle_angles,
                                   triangle_Nbeads, 1.0,
                                   target_conc, mol_size, shift_top_down )

        group_all = hoomd.group.all()
        hoomd.dump.gsd( in_file, period = None,
                        group = group_all, overwrite = True )


    seed = int(str(time.time())[-3:])
    side_types = [ (2,3), (4,5), (6,7) ]
    rigid_group = hoomd.group.rigid_center()
    hoomd.md.integrate.mode_standard(dt=t_step)
    print("Seed =", seed, file = sys.stderr)
    lan = hoomd.md.integrate.langevin(group = rigid_group, kT=1.0, seed=seed)

    nl = set_pair_interactions( side_energies, force_style, force_alpha, dom, R_domain = 20.0 )

    lan.set_gamma( 'Center1', gamma = 10.0 ) 
    lan.set_gamma_r( 'Center1', 40.0 ) 
    lan.set_params( kT = 1.0 )
    # Periodically write restart file:
    hoomd.dump.gsd( res_file, group = hoomd.group.all(),
                    truncate = True, period = t_dump, phase = 0 )

    log_quants = [ 'time', 'kinetic_energy', 'translational_kinetic_energy',
                   'rotational_kinetic_energy', 'potential_energy',
                   'temperature' ]
    log_head = "# "
    if restart:
        print("Resuming run, appending to ", traj_file, "...", file=sys.stderr)

        hoomd.dump.gsd( traj_file, period = t_dump, group = group_all,
                        overwrite = False )
        hoomd.analyze.log( log_file, log_quants, t_log,
                           overwrite = False, header_prefix = log_head )
        if run_upto_instead:
            print("Executing run hoomd.run_upto(", t_run, ")", file=sys.stderr)
            hoomd.run_upto(t_run)
        else:

            print("Executing run hoomd.run(", t_run, ")", file=sys.stderr)
            hoomd.run(t_run)
    else:
        print("Beginning fresh run...", file=sys.stderr)
        hoomd.dump.gsd( traj_file, period = t_dump, group = group_all,
                        overwrite = True )
        hoomd.dump.gsd( start_file, period = None,
                        group = group_all, overwrite = True )
        hoomd.analyze.log( log_file, log_quants, t_log,
                           overwrite = True, header_prefix = log_head )

        hoomd.run(t_run)
        print("Executing run hoomd.run(", t_run, ")", file=sys.stderr)

