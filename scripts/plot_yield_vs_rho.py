#Plot yield vs Eb for varying Ec

import matplotlib.pyplot as plt
import numpy as np
import sys
import os

N=1200
L=144.2
Vr=0.005
rhos=[2.0,2.5,3.0,4.0,5.0]
Eb=7.5
Ecs=[0,1]

yield_arr=np.zeros((len(rhos),len(Ecs)))
frac_malformed_arr=np.zeros((len(rhos),len(Ecs)))

for i in range(len(rhos)):
    for j in range(len(Ecs)):
        #myfile=os.path.expandvars('$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=%d/L=%.01f/Vr=%.03f/E_cond=%f/E_bond=%f/yield.txt' % (N, L, Vr, Ecs[i], Ebs[j]))
        if rhos[i]==2.5:
            myfile=os.path.expandvars('$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=%d/L=%.01f/Vr=%.03f/E_cond=%f/E_bond=%f/seed=1/traj.sizes' % (N, L, Vr, Ecs[j], Eb))
        else:
            myfile=os.path.expandvars('$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=%d/L=%.01f/Vr=%.03f/E_cond=%f/E_bond=%f/rho=%f/seed=1/traj.sizes' % (N, L, Vr, Ecs[j], Eb, rhos[i]))
        if os.path.exists(myfile):
            data = np.loadtxt(myfile)
            #yield_arr[i,j] = data[-1,1]

            if data.shape[1]<14:
                yield_arr[i,j]=0
                frac_malformed_arr[i,j]=0
            else:
                #yield_arr[i,j] = 12*data[-1,12]/(1.0*N) + 11*data[-1,11]/(1.0*N)
                yield_arr[i,j] = 12*data[-1,12]/(1.0*N)
                for k in range(data.shape[1]-2-12):
                    frac_malformed_arr[i,j] += (i+1+12)*data[-1,k+1+12]/(1.0*N)


fig = plt.figure()
for i in range(len(Ecs)):
    plt.plot(rhos, yield_arr[:,i], label=r'$E_c=%.0f$' % Ecs[i], marker='o')
plt.ylim([0.0,1.0])
plt.ylabel(r'$f_{\text{c}}$')
plt.xlabel(r'$\rho$')
plt.legend()
plt.savefig('yield_vs_rho_vary_Ec_N=%d_L=%f_Vr=%f.png' % (N, L, Vr))

fig = plt.figure()
for i in range(len(Ecs)):
    plt.plot(rhos, frac_malformed_arr[:,i], label=r'$E_c=%.0f$' % Ecs[i], marker='o')
plt.ylim([0.0,1.0])
plt.ylabel(r'$f_{\text{malformed}}$')
plt.xlabel(r'$\rho$')
plt.legend()
plt.savefig('frac_malformed_vs_rho_vary_Ec_N=%d_L=%f_Vr=%f.png' % (N, L, Vr))
plt.show()