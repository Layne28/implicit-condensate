#Get partition coefficient 

import matplotlib.pyplot as plt
import numpy as np
import sys
import numpy.linalg as la
import os

import AnalysisTools.particle_io as pio
import AnalysisTools.measurement_tools as tools

myfile = sys.argv[1] # traj.gsd
myfile2 = sys.argv[2] #yield.txt

dt=200

fileparts = myfile.split('/')
outfile = myfile.replace('traj.gsd', 'monomer_traj.txt')

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



#Load monomer density
monomer_data = np.loadtxt(myfile,skiprows=1)

#Load yield
yield_data = np.loadtxt(myfile2,skiprows=1)

figsize = plt.rcParams.get('figure.figsize')
figsize[0]*=2
#figsize[1]*=2
fig, ax = plt.subplots(1,2)
ax[0].plot(dt*np.arange(yield_data.shape[0])/10**5, monomer_data[:,2], label='condensate')
ax[0].plot(dt*np.arange(yield_data.shape[0])/10**5, monomer_data[:,1], label='background')
ax[0].set_ylabel(r'$\rho_1$')
ax[0].legend(loc='lower left')
ax[0].set_yscale('log')
ax[0].set_ylim([10**-5,10**-2])
ax[0].set_title('monomer concentration')
ax[0].set_xlabel(r'time $/t_0\times 10^5$')
ax[0].set_xscale('log')

ax[1].plot(dt*np.arange(yield_data.shape[0])/10**5, yield_data[:,1])
ax[1].set_ylim([0,1])
ax[1].set_title('yield')
ax[1].set_xlabel(r'time $/t_0\times 10^5$')
ax[1].set_xscale('log')

plt.savefig('plots/yield_monomer_density_vs_time_N=%d_L=%.01f_Vr=%.03f_Ec=%f_seed=%d.png' % (N, L, Vr, Ec, seed))
#plt.show()

