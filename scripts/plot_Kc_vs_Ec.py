#Get partition coefficient 

import matplotlib.pyplot as plt
import numpy as np
import sys
import os.path

def muex(rho, sigma):
    eta = (np.pi/6)*rho*sigma**3
    return eta*(3*eta**2 - 9*eta + 8)/((1-eta)**3)

#Get theoretical prediction
theory_data = np.loadtxt('actual_Kc.dat')
# vmuex = np.vectorize(muex)
# rhoT = 1200/(144.2**3)
# sigma = 2.4
# Vr=0.005
# rho1c_arr = np.linspace(0,0.05,num=100)
# rho1bg_arr = (rhoT-Vr*rho1c_arr)/(1-Vr)
# expEc_arr = (rho1c_arr/rho1bg_arr)*np.exp(muex(rho1c_arr, sigma) - muex(rho1bg_arr, sigma))

Ecs = [0.0,1.0,3.0,5.0,7.0]

basedir = '$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=1200/L=144.2/Vr=0.005/'

Kcs = []
Kcerrs = []

for Ec in Ecs:
    myfile = os.path.expandvars(basedir) + 'E_cond=%f/E_bond=0.000000/Kc.txt' % Ec
    with open(myfile, 'r') as f:
        firstline = f.readline() #skip header
        nsamples = int((firstline.split('= ')[-1]).split(')')[0])
        print(nsamples)
        line = f.readline()
        

    elems = line.split(' ')
    Kc = float(elems[0])
    Kcstdev = float(elems[1])
    Kcs.append(Kc)
    Kcerrs.append(Kcstdev/np.sqrt(nsamples))

print(Kcs)
print(Kcerrs)
fig = plt.figure()
plt.errorbar(np.exp(np.array(Ecs)), np.array(Kcs), yerr=2*np.array(Kcerrs), marker='o',markersize=3,capsize=2,label='simulation')
#plt.plot(np.exp(np.array(Ecs)),np.exp(np.array(Ecs)), color='black', linestyle='--', label='ideal solution')
#plt.plot(expEc_arr, rho1c_arr/rho1bg_arr, color='black', linestyle='--', label='Carnahan-Starling')
plt.plot(theory_data[:,0], theory_data[:,1], color='black', linestyle='--', label='Carnahan-Starling')
plt.plot(theory_data[:,0], theory_data[:,0], color='gray', linestyle=':', label='Ideal solution')

plt.xlabel(r'$e^{\beta E_{\text{c}}}$')
plt.ylabel(r'$K_{\text{c}}$')
plt.xscale('log')
plt.yscale('log')
plt.xlim([1,2000])
ax = plt.gca()
ax.set_aspect('equal')
plt.legend(fontsize=8)
plt.savefig('Kc_vs_Ec.png')
plt.show()

