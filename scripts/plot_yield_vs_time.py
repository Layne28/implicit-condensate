#Plot yield vs Eb for varying Ec

import matplotlib.pyplot as plt
import numpy as np
import sys
import os

do_near_perfect=0

N=1200
L=144.2
Vr=0.005
Eb=6.0
Ecs=[0,1,3,5,7]

dt = 200

yields = []
errs = []

for i in range(len(Ecs)):
    if do_near_perfect==1:
        myfile=os.path.expandvars('$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=%d/L=%.01f/Vr=%.03f/E_cond=%f/E_bond=%f/yield_near_perfect.txt' % (N, L, Vr, Ecs[i], Eb))
    else:
        myfile=os.path.expandvars('$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=%d/L=%.01f/Vr=%.03f/E_cond=%f/E_bond=%f/yield.txt' % (N, L, Vr, Ecs[i], Eb))
    if os.path.exists(myfile):
        with open(myfile, 'r') as f:
            firstline = f.readline()
        nsamples = int(firstline.split(' ')[-1])
        data = np.loadtxt(myfile,skiprows=1)
        yields.append(data[:,1])
        errs.append(data[:,2]/np.sqrt(nsamples))

fig = plt.figure()
for i in range(len(Ecs)):
    plt.plot(dt*np.arange(yields[i].shape[0])/10**5, yields[i], label=r'$E_c=%.0f$' % Ecs[i], linewidth=1.0)
    ax = plt.gca()
    ax.fill_between(dt*np.arange(yields[i].shape[0])/10**5, yields[i]-2*errs[i], yields[i]+2*errs[i], alpha=0.5)
    #plt.errorbar(dt*np.arange(yields[i].shape[0]), yields[i], yerr=2*errs[i], label=r'$E_c=%.0f$' % Ecs[i], marker='o',markersize=3,capsize=2)
plt.ylim([-0.01,1.0])
plt.xlim([0,6])
#plt.xscale('log')
#plt.yscale('log')
#plt.xlim([0,1.05])
plt.ylabel(r'yield, $f_{\text{c}}$')
plt.xlabel(r'time $/t_0\times 10^5$')
ax = plt.gca()
ax.legend(bbox_to_anchor=(0.93,1.6),ncol=2)
plt.savefig('yield_vs_time_vary_Ec_N=%d_Eb=%f_Vr=%f_L=%f.png' % (N, Eb, Vr, L))
#plt.show()

