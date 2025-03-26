#Plot yield vs Eb for varying Ec

import matplotlib.pyplot as plt
import numpy as np
import sys
import os

do_near_perfect=0

N=1200
Ls=[288.5, 228.9, 181.7, 158.7, 144.2, 133.9, 117.0, 106.3]#, 49.3]
Vr=0.005
Eb=6.0
Ecs=[0,1,3,5,7]
densities = []
for L in Ls:
    densities.append(N/L**3)

yield_arr=np.zeros((len(Ecs),len(Ls)))
err_arr=np.zeros((len(Ecs),len(Ls)))

for i in range(len(Ecs)):
    for j in range(len(Ls)):
        if do_near_perfect==1:
            myfile=os.path.expandvars('$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=%d/L=%.01f/Vr=%.03f/E_cond=%f/E_bond=%f/yield_near_perfect.txt' % (N, Ls[j], Vr, Ecs[i], Eb))
        else:
            myfile=os.path.expandvars('$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=%d/L=%.01f/Vr=%.03f/E_cond=%f/E_bond=%f/yield.txt' % (N, Ls[j], Vr, Ecs[i], Eb))
        if os.path.exists(myfile):
            with open(myfile, 'r') as f:
                firstline = f.readline()
            nsamples = int(firstline.split(' ')[-1])
            data = np.loadtxt(myfile,skiprows=1)
            yield_arr[i,j] = data[-1,1]
            #print(nsamples)
            err_arr[i,j] = data[-1,2]/np.sqrt(nsamples)


fig = plt.figure()
for i in range(len(Ecs)):
    plt.errorbar(np.array(densities)*(10**3), yield_arr[i,:], yerr=2*err_arr[i,:], label=r'$E_c=%.0f$' % Ecs[i], marker='o',markersize=3,capsize=2)
plt.ylim([-0.01,1.0])
plt.xlim([0,1.05])
plt.ylabel(r'yield, $f_{\text{c}}$')
plt.xlabel(r'total subunit concentration, $\rho_{\text{T}}\times 10^3$')
ax = plt.gca()
ax.legend(bbox_to_anchor=(0.93,1.6),ncol=2)
plt.savefig('yield_vs_density_vary_Ec_N=%d_Eb=%f_Vr=%f.png' % (N, Eb, Vr))
#plt.show()

