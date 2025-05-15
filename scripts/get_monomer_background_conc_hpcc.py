#Get concentration of monomers in background (+ condensate)

#import matplotlib.pyplot as plt
import numpy as np
import sys
import numpy.linalg as la
import os
import pickle
import gsd.hoomd

import AnalysisTools.particle_io as pio

myfile = sys.argv[1]  #traj.gsd
myfile2 = sys.argv[2] #traj.cl

fileparts = myfile.split('/')
outfile = myfile.replace('traj.gsd', 'monomer_conc_traj.txt')

Vr = [e.split('=')[1] for e in fileparts if e.split('=')[0]=='Vr']
L = [e.split('=')[1] for e in fileparts if e.split('=')[0]=='L']
N = [e.split('=')[1] for e in fileparts if e.split('=')[0]=='N']
Ec = [e.split('=')[1] for e in fileparts if e.split('=')[0]=='E_cond']
seed = [e.split('=')[1] for e in fileparts if e.split('=')[0]=='seed']
Vr = float(Vr[0])
L = float(L[0])
N = int(N[0])
Ec = float(Ec[0])
seed = int(seed[0])
print(L)
print(Vr)
print(N)
print(Ec)
print(seed)

Vcond = (L**3)*Vr
Rcond = (Vcond/(4.0*np.pi/3.0))**(1.0/3)
print(Rcond)

#Load actual trajectory
#traj = pio.load_traj(myfile)

traj2 = gsd.hoomd.open(myfile)


#Load size distribution
with open(myfile2,mode='rb') as f:
    cluster_data = pickle.load(f)
#counts = np.loadtxt(myfile2)
#tot_monomer_count = counts[:,1]

traj_len = len(traj2)

print(traj_len)
print(dir(cluster_data))
print(len(cluster_data.__dict__['monomer_ids']))

num_out_condensate = np.zeros(traj_len)
rho1_bg = np.zeros(traj_len)
rho1_c = np.zeros(traj_len)
for t in range(traj_len-1):
    print(t)
    monomer_id_list = sorted([int(e) for e in cluster_data.__dict__['monomer_ids'][t]])
    tot_monomer_count = len(monomer_id_list)
    pos = traj2[t].particles.position
    ncount=0
    for i in range(pos.shape[0]):
        #print(monomer_id_list)
        #check if (1) atom is a "Capsomer" (2) atom is within Rcond of origin (3) atom is in the monomer list
        if traj2[t].particles.typeid[i]==0 and la.norm(pos[i,:])>(Rcond) and (traj2[t].particles.body[i] in monomer_id_list):#tools.get_dist(pos[t,i,:], np.zeros(3), traj['edges'])<=Rcond:
            num_out_condensate[t]+=1
    print('concentration in condensate/bulk:', (tot_monomer_count-num_out_condensate[t])/Vcond, (num_out_condensate[t])/(L**3-Vcond))
    rho1 = (tot_monomer_count - num_out_condensate[t])/Vcond
    rho2 = num_out_condensate[t]/(L**3-Vcond)
    rho1_bg[t] = rho2
    rho1_c[t] = rho1
with open(outfile, 'w') as f:
    f.write('frame rho1_bg rho1_c\n')
    for t in range(rho1_bg.shape[0]):
        f.write('%d %f %f\n' % (t, rho1_bg[t], rho1_c[t]))

#fig = plt.figure()
#plt.plot(np.arange(0,pos.shape[0],1), rho1_c/rho1_c[0], label='condensate')
#plt.plot(np.arange(0,pos.shape[0],1), rho1_bg/rho1_bg[0], label='background')
#if not os.path.isdir('plots/monomer_density'):
#    os.makedirs('plots/monomer_density')
#plt.xlabel('frame')
#plt.ylabel(r'$\rho_1$')
#plt.legend()
#plt.savefig('plots/monomer_density/monomer_density_vs_time_N=%d_L=%.01f_Vr=%.03f_Ec=%f_seed=%d.png' % (N, L, Vr, Ec, seed))
#plt.show()

