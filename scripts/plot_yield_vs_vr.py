#Plot yield vs Eb for varying Ec

import matplotlib.pyplot as plt
import numpy as np
import sys
import os

do_near_perfect=0

N=1200
L=144.2
Vrs=[0.002, 0.005, 0.01, 0.02, 0.05, 0.1]
Eb=6.0
Ecs=[0,1,3,5,7]

yield_arr=np.zeros((len(Ecs),len(Vrs)))
err_arr=np.zeros((len(Ecs),len(Vrs)))

for i in range(len(Ecs)):
    for j in range(len(Vrs)):
        if do_near_perfect==1:
            myfile=os.path.expandvars('$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=%d/L=%.01f/Vr=%.03f/E_cond=%f/E_bond=%f/yield_near_perfect.txt' % (N, L, Vrs[j], Ecs[i], Eb))
        else:
            myfile=os.path.expandvars('$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=%d/L=%.01f/Vr=%.03f/E_cond=%f/E_bond=%f/yield.txt' % (N, L, Vrs[j], Ecs[i], Eb))
        if os.path.exists(myfile):
            with open(myfile, 'r') as f:
                firstline = f.readline()
            nsamples = int(firstline.split(' ')[-1])
            data = np.loadtxt(myfile,skiprows=1)
            yield_arr[i,j] = data[-1,1]
            err_arr[i,j] = data[-1,2]/np.sqrt(nsamples)


fig = plt.figure()
for i in range(len(Ecs)):
    plt.errorbar(Vrs, yield_arr[i,:], yerr=2*err_arr[i,:], label=r'$E_c=%.0f$' % Ecs[i], marker='o',markersize=3,capsize=2)
plt.ylim([0.0,1.0])
plt.ylabel(r'yield, $f_{\text{c}}$')
plt.xlabel(r'volume fraction, $V_{\text{r}}$')
plt.legend(bbox_to_anchor=(0.93,1.6),ncol=2)
plt.xscale('log')
if do_near_perfect==1:
    plt.savefig('yield_near_perfect_vs_Vr_vary_Ec_N=%d_Eb=%f_L=%f.png' % (N, Eb, L))
else:
    plt.savefig('yield_vs_Vr_vary_Ec_N=%d_Eb=%f_L=%f.png' % (N, Eb, L))
plt.show()

