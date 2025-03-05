import gsd.hoomd

filename = 'single_subunit/traj_seed=1.gsd'
#filename = '../tutorials/dodecahedron_simulation_HOOMD3/dodec_trajectory.gsd'
traj = gsd.hoomd.open(name=filename, mode='r')
"""
print(traj.__len__())
print(traj[0].particles.position)
print(traj[0].particles.velocity)
print(traj[0].particles.types)
print(traj[0].particles.mass)
print(traj[0].particles.body)
print(traj[0].particles.typeid)
"""
#Get the center of mass positions
#We need to filter by particles with typeid corresponding
#to type "Capsomer"
typeids = traj[0].particles.typeid
capsomer_index = traj[0].particles.types.index('Capsomer')
com_positions = traj[0].particles.position[typeids==capsomer_index,:]
com_orientations = traj[0].particles.orientation[typeids==capsomer_index,:]
print(com_positions.shape)
print(com_orientations.shape)