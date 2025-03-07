#Plot rho_c vs exp(beta*ec)

import matplotlib.pyplot as plt
import numpy as np
import sys
import os.path

def muex(rho, sigma):
    eta = (np.pi/6)*rho*sigma**3
    return eta*(3*eta**2 - 9*eta + 8)/((1-eta)**3)

#Get theoretical prediction
vmuex = np.vectorize(muex)
rhoT = 1200/(144.2**3)
sigma = 2.4
Vr=0.005
rho1c_arr = np.linspace(0,0.05,num=100)
rho1bg_arr = (rhoT-Vr*rho1c_arr)/(1-Vr)
expEc_arr = (rho1c_arr/rho1bg_arr)*np.exp(muex(rho1c_arr, sigma) - muex(rho1bg_arr, sigma))

#Get simulation data
Ecs = [0.0,1.0,3.0,5.0,7.0]

basedir = '$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=1200/L=144.2/Vr=0.005/short/'

rho1cs = []

for Ec in Ecs:
    myfile = os.path.expandvars(basedir) + 'E_cond=%f/E_bond=0.000000/seed=1/Kc.txt' % Ec
    with open(myfile, 'r') as f:
        f.readline() #skip header
        line = f.readline()

    elems = line.split(' ')
    rho1c = float(elems[-2])
    rho1cs.append(rho1c)

fig = plt.figure()
plt.plot(np.exp(np.array(Ecs)), np.array(rho1cs), marker='o',label='simulation')
plt.plot(expEc_arr,rho1c_arr, color='black', linestyle='--', label='Carnahan-Starling')
plt.xlabel(r'$e^{\beta E_{\text{c}}}$')
plt.ylabel(r'$\rho_1^{\text{c}}$')
plt.xscale('log')
plt.yscale('log')
plt.xlim([1,2000])
ax = plt.gca()
ax.set_aspect('equal')
plt.legend(fontsize=8)
plt.savefig('rho1c_vs_Ec.png')
plt.show()

