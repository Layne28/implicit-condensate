#Plot yield vs Eb for varying Ec

import matplotlib.pyplot as plt
import numpy as np
import sys
import os

do_near_perfect=1

N=1200
L=144.2
Vr=0.005
Ebs=[4,4.5,5,5.5,6,6.5,7,7.5,8]
Ecs=[0,1,3,5,7]

yield_arr=np.zeros((len(Ecs),len(Ebs)))
err_arr=np.zeros((len(Ecs),len(Ebs)))

for i in range(len(Ecs)):
    for j in range(len(Ebs)):
        if do_near_perfect==1:
            myfile=os.path.expandvars('$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=%d/L=%.01f/Vr=%.03f/E_cond=%f/E_bond=%f/yield_near_perfect.txt' % (N, L, Vr, Ecs[i], Ebs[j]))
        else:
            myfile=os.path.expandvars('$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=%d/L=%.01f/Vr=%.03f/E_cond=%f/E_bond=%f/yield.txt' % (N, L, Vr, Ecs[i], Ebs[j]))
        #myfile=os.path.expandvars('$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=%d/L=%.01f/Vr=%.03f/E_cond=%f/E_bond=%f/seed=1/traj.sizes' % (N, L, Vr, Ecs[i], Ebs[j]))
        if os.path.exists(myfile):
            with open(myfile, 'r') as f:
                firstline = f.readline()
            nsamples = int(firstline.split(' ')[-1])
            data = np.loadtxt(myfile,skiprows=1)
            yield_arr[i,j] = data[-1,1]
            err_arr[i,j] = data[-1,2]/np.sqrt(nsamples)

            # if data.shape[1]<14:
            #     yield_arr[i,j]=0
            # else:
            #     #yield_arr[i,j] = 12*data[-1,12]/(1.0*N) + 11*data[-1,11]/(1.0*N)
            #     yield_arr[i,j] = 12*data[-1,12]/(1.0*N)


fig = plt.figure()
for i in range(len(Ecs)):
    plt.errorbar(Ebs, yield_arr[i,:], yerr=2*err_arr[i,:], label=r'$E_c=%.0f$' % Ecs[i], marker='o',markersize=3,capsize=2)
plt.ylim([0.0,1.0])
plt.ylabel(r'$f_{\text{c}}$')
plt.xlabel(r'$\epsilon_{\text{ss}}$')
ax = plt.gca()
ax.legend(bbox_to_anchor=(0.93,1.6),ncol=2)
if do_near_perfect==1:
    plt.savefig('yield_near_perfect_vs_Eb_vary_Ec_N=%d_L=%f_Vr=%f.png' % (N, L, Vr))
else:
    plt.savefig('yield_vs_Eb_vary_Ec_N=%d_L=%f_Vr=%f.png' % (N, L, Vr))
#plt.show()

