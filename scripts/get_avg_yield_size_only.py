#Compute average yield (w/ error bars) vs time

import numpy as np
import sys
import os

myfolder = sys.argv[1]

started = 0

nsamples = 0
for i in range(10):

    if os.path.exists(myfolder + ("seed=%d/traj.sizes" % (i+1))):
        nsamples += 1
        data = np.loadtxt(myfolder + ("seed=%d/traj.sizes" % (i+1)))
        if started==0:
            started = 1
            avgYield = np.zeros(data.shape[0])
            stddevYield = np.zeros(data.shape[0])

        #Check the no. of columns to see if there is any assembly at all
        #First column is frame, last column is max. cluster size in that frame

        if data.shape[1]<14: #=12+2
            myYield = np.zeros(data.shape[0])
            myYieldSq = np.zeros(data.shape[0])
        else:
            nsubunits = data[0][1]
            myYield = 12*data[:,12]/(1.0*nsubunits)
            myYieldSq = (12*data[:,12]/(1.0*nsubunits))**2

        avgYield += myYield
        stddevYield += myYieldSq

avgYield *= 1.0/nsamples
stddevYield *= 1.0/nsamples
stddevYield -= avgYield**2
stddevYield = np.sqrt(stddevYield)

np.savetxt(myfolder + '/yield.txt', np.c_[np.arange(data.shape[0]),avgYield,stddevYield], header='No. samples = %d' % nsamples)

