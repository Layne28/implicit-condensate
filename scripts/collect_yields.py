#Get long-time yields for different parameter sets

import matplotlib.pyplot as plt
import numpy as np
import sys
import os

N=1200
L=144.2
Vr=0.005
Ebs=[4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8] 
Ecs=[0, 1, 3, 5, 7]

output = np.zeros((len(Ebs)*len(Ecs),4))
cnt=0
for Eb in Ebs:
    for Ec in Ecs:
        myfile = os.path.expandvars('$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=%d/L=%.01f/Vr=%.03f/E_cond=%f/E_bond=%f/yield.txt' % (N, L, Vr, Ec, Eb))
        with open(myfile, 'r') as f:
            firstline = f.readline()
        nsamples = int(firstline.split(' ')[-1])
        data = np.loadtxt(myfile, skiprows=1)
        stderr = data[:,2]/np.sqrt(nsamples)

        output[cnt,0] = Eb
        output[cnt,1] = Ec
        output[cnt,2] = data[-1,1]
        output[cnt,3] = 2*stderr[-1]

        cnt += 1

np.savetxt("yields_N=%d_L=%f_Vr=%f.txt" % (N, L, Vr), output, header="Eb Ec yield error")


