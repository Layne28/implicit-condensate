#Compute average Kc (w/ error bars) vs time

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

avgKc = 0
stddevKc = 0

for i in range(10):

    if os.path.exists(myfolder + ("seed=%d/Kc.txt" % (i+1))) :
        nsamples += 1
        data = np.loadtxt(myfolder + ("seed=%d/Kc.txt" % (i+1)), skiprows=1)
        myKc = data[-1]
        myKcSq = data[-1]**2

        avgKc += myKc
        stddevKc += myKcSq

    #print(nsamples)
    # elif os.path.exists(myfolder + ("seed=%d/traj.gsd" % (i+1))):
    #     trajfile = myfolder + ("seed=%d/traj.gsd" % (i+1))
    #     traj = gsd.hoomd.open(trajfile)
    #     traj_len = len(traj)
    #     print(len(traj))
    #     avgKc = np.zeros(len(traj))
    #     stddevKc = np.zeros(len(traj))

if nsamples>0:
    avgKc *= 1.0/nsamples
    stddevKc *= 1.0/nsamples
    stddevKc -= avgKc**2
    stddevKc = np.sqrt(stddevKc)

np.savetxt(myfolder + '/Kc.txt', np.c_[avgKc,stddevKc], header='Avg stddev (No. samples = %d)' % nsamples)

