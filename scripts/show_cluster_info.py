import numpy as np
import pickle

#myfile="/pscratch/sd/l/lfrechet/capsid-assembly/llps/droplet/assembly_trajectories/N=1200/L=144.2/Vr=0.005/E_cond=7.000000/E_bond=6.000000/seed=1/traj.cl"
myfile='example.cl'

with open(myfile,mode='rb') as f:
    data = pickle.load(f)

print(dir(data))
#print(data.__dict__['monomer_types'])
#print(len(data.__dict__['cluster_info']))
#print(data.__dict__['cluster_info'])
#print(data.__dict__['monomer_frac'])
#print(data.__dict__['cluster_info'][1].__dict__)
#print(len(data.__dict__['cluster_info'][1].__dict__['_ClusterInfo__stored_data']))
print(len(data.__dict__['monomer_ids']))
#print(len(data.__dict__['monomer_ids'][-1]))
print(sorted([int(e) for e in data.__dict__['monomer_ids'][-1]]))