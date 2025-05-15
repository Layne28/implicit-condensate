#Compute average monomer concs (w/ error bars) vs time

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

avgC = 0
stddevC = 0
avgBG = 0
stddevBG = 0

for i in range(10):

    if os.path.exists(myfolder + ("seed=%d/Kc_traj.txt" % (i+1))) :
        nsamples += 1
        data = np.loadtxt(myfolder + ("seed=%d/Kc_traj.txt" % (i+1)), skiprows=1)
        traj_len = data.shape[0]

        myC = np.average(data[-(traj_len//2):,1])        
        myCSq = myC**2

        avgC += myC
        stddevC += myCSq

        myBG = np.average(data[-(traj_len//2):,0])        
        myBGSq = myBG**2

        avgBG += myBG
        stddevBG += myBGSq

    #print(nsamples)
    # elif os.path.exists(myfolder + ("seed=%d/traj.gsd" % (i+1))):
    #     trajfile = myfolder + ("seed=%d/traj.gsd" % (i+1))
    #     traj = gsd.hoomd.open(trajfile)
    #     traj_len = len(traj)
    #     print(len(traj))
    #     avgKc = np.zeros(len(traj))
    #     stddevKc = np.zeros(len(traj))

if nsamples>0:
    avgC *= 1.0/nsamples
    stddevC *= 1.0/nsamples
    stddevC -= avgC**2
    stddevC = np.sqrt(stddevC)
    avgBG *= 1.0/nsamples
    stddevBG *= 1.0/nsamples
    stddevBG -= avgBG**2
    stddevBG = np.sqrt(stddevBG)

np.savetxt(myfolder + '/rho1bg.txt', np.c_[avgBG,stddevBG], header='Avg stddev (No. samples = %d)' % nsamples)
np.savetxt(myfolder + '/rho1c.txt', np.c_[avgC,stddevC], header='Avg stddev (No. samples = %d)' % nsamples)

