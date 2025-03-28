#Compute average yield (w/ error bars) vs time

import numpy as np
import sys
import os
import gsd.hoomd

myfolder = sys.argv[1]

#Get num subunits from folder name
#(really should be extracting this info from traj.sizes)
nsubunits = int(([e for e in myfolder.split('/') if e.startswith('N=')][0]).split('=')[-1])
#print(nsubunits)

started = 0
traj_len = 0
nsamples = 0
for i in range(10):

    if os.path.exists(myfolder + ("seed=%d/monomer_conc_traj.txt" % (i+1))):
        nsamples += 1
        data = np.loadtxt(myfolder + ("seed=%d/monomer_conc_traj.txt" % (i+1)),skiprows=1)
        traj_len = data.shape[0]
        myRho1BG = data[:,1]
        myRho1BGSq = myRho1BG**2
        myRho1C = data[:,2]
        myRho1CSq = myRho1C**2
        if started==0:
            started = 1
            avgRho1BG = np.zeros(data.shape[0])
            stddevRho1BG = np.zeros(data.shape[0])
            avgRho1C = np.zeros(data.shape[0])
            stddevRho1C = np.zeros(data.shape[0])

        avgRho1BG += myRho1BG
        stddevRho1BG += myRho1BGSq
        avgRho1C += myRho1C
        stddevRho1C += myRho1CSq

if nsamples>0:
    avgRho1BG *= 1.0/nsamples
    avgRho1C *= 1.0/nsamples
    
    stddevRho1BG *= 1.0/nsamples
    stddevRho1BG -= avgRho1BG**2
    stddevRho1BG = np.sqrt(stddevRho1BG)
    
    stddevRho1C *= 1.0/nsamples
    stddevRho1C -= avgRho1C**2
    stddevRho1C = np.sqrt(stddevRho1C)

np.savetxt(myfolder + '/monomer_conc_avg.txt', np.c_[np.arange(traj_len),avgRho1BG,stddevRho1BG,avgRho1C,stddevRho1C], header='No. samples = %d (frame, rho1bg_avg, rho1bg_stddev, rho1c_avg, rho1c_stddev)' % nsamples)

