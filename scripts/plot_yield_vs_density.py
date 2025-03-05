#Plot yield vs Eb for varying Ec

import matplotlib.pyplot as plt
import numpy as np
import sys
import os

N=1200
Ls=[288.5, 228.9, 181.7, 158.7, 144.2, 133.9, 117.0, 106.3]#, 49.3]
Vr=0.005
Eb=6.0
Ecs=[0,1,3,5,7]
densities = []
for L in Ls:
    densities.append(N/L**3)

yield_arr=np.zeros((len(Ecs),len(Ls)))

for i in range(len(Ecs)):
    for j in range(len(Ls)):
        #myfile=os.path.expandvars('$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=%d/L=%.01f/Vr=%.03f/E_cond=%f/E_bond=%f/yield.txt' % (N, L, Vr, Ecs[i], Ebs[j]))
        myfile=os.path.expandvars('$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=%d/L=%.01f/Vr=%.03f/E_cond=%f/E_bond=%f/seed=1/traj.sizes' % (N, Ls[j], Vr, Ecs[i], Eb))
        if os.path.exists(myfile):
            data = np.loadtxt(myfile)
            #yield_arr[i,j] = data[-1,1]

            if data.shape[1]<14:
                yield_arr[i,j]=0
            else:
                #yield_arr[i,j] = 12*data[-1,12]/(1.0*N) + 11*data[-1,11]/(1.0*N)
                yield_arr[i,j] = 12*data[-1,12]/(1.0*N)


fig = plt.figure()
for i in range(len(Ecs)):
    plt.plot(densities, yield_arr[i,:], label=r'$E_c=%.0f$' % Ecs[i], marker='o')
plt.ylim([0.0,1.0])
plt.ylabel(r'$f_{\text{c}}$')
plt.xlabel(r'$\rho_{\text{T}}$')
plt.legend()
plt.savefig('yield_vs_density_vary_Ec_N=%d_Eb=%f_Vr=%f.png' % (N, Eb, Vr))
plt.show()

