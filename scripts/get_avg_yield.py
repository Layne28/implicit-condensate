#Compute average yield (w/ error bars) vs time

import numpy as np
import sys
import os
import gsd.hoomd

def get_perfect_index(header):
    header = header.replace('Microstates: ', '')
    elems = header.split('),(')
    myentry = [i for i in elems if "'E-E', 30" in i][0]
    #print(myentry)
    myindex = myentry.split(':')[0]
    myindex = myindex.replace('(', '')
    #print(myindex)
    myindex = int(myindex)+1
    return myindex

def get_near_perfect_indices(header):
    header = header.replace('Microstates: ', '')
    elems = header.split('),(')
    myentries = [i for i in elems if (("'E-E', 28" in i) or ("'E-E', 29" in i) or ("'E-E', 27" in i) or ("'E-E', 26" in i))]
    #print(myentry)
    myindices = []
    for myentry in myentries:
        myindex = myentry.split(':')[0]
        myindex = myindex.replace('(', '')
        myindices.append(int(myindex)+1)
    #print(myindices)
    return myindices

myfolder = sys.argv[1]

do_get_near_perfect_indices = 0

#Get num subunits from folder name
#(really should be extracting this info from traj.sizes)
nsubunits = int(([e for e in myfolder.split('/') if e.startswith('N=')][0]).split('=')[-1])
#print(nsubunits)

started = 0
traj_len = 0
nsamples = 0
for i in range(10):

    #Anthony's code won't create traj_12.fsizes if no clusters of that size exist,
    #so need to open traj.sizes and check if there is any assembly >=12
    if os.path.exists(myfolder + ("seed=%d/traj.sizes" % (i+1))):# and os.path.exists(myfolder + ("seed=%d/traj_12.fsizes" % (i+1))):
        nsamples += 1
        data = np.loadtxt(myfolder + ("seed=%d/traj.sizes" % (i+1)))
        traj_len = data.shape[0]
        if data.shape[1]<14: #=12+2
            myYield = np.zeros(data.shape[0])
            myYieldSq = np.zeros(data.shape[0])
        if started==0:
            started = 1
            avgYield = np.zeros(data.shape[0])
            stddevYield = np.zeros(data.shape[0])

        if os.path.exists(myfolder + ("seed=%d/traj_12.fsizes" % (i+1))):
            with open(myfolder + ("seed=%d/traj_12.fsizes" % (i+1))) as f:
                header = f.readline()
            myindex = get_perfect_index(header)
            
            
            data2 = np.loadtxt(myfolder + ("seed=%d/traj_12.fsizes" % (i+1)),skiprows=1)

            myYield = 12*data2[:,myindex]/(1.0*nsubunits)
            myYieldSq = (12*data2[:,myindex]/(1.0*nsubunits))**2
            
            #Get near-perfect capsids
            if do_get_near_perfect_indices==1:
                other_indices = get_near_perfect_indices(header)
                tempSq = 12*data2[:,myindex]/(1.0*nsubunits)
                for ind in other_indices:
                    #print(myYield)
                    #print(12*data2[:,ind]/(1.0*nsubunits))
                    myYield += 12*data2[:,ind]/(1.0*nsubunits)
                    #print(myYield)
                    #print('space')
                    tempSq += 12*data2[:,ind]/(1.0*nsubunits)
                myYieldSq = (tempSq)**2

        avgYield += myYield
        stddevYield += myYieldSq

    #print(nsamples)
    #elif os.path.exists(myfolder + ("seed=%d/traj.gsd" % (i+1))):
    #    trajfile = myfolder + ("seed=%d/traj.gsd" % (i+1))
    #    traj = gsd.hoomd.open(trajfile)
    #    traj_len = len(traj)
    #    print(len(traj))
    #    avgYield = np.zeros(len(traj))
    #    stddevYield = np.zeros(len(traj))

if nsamples>0:
    avgYield *= 1.0/nsamples
    #print('before:', stddevYield)
    stddevYield *= 1.0/nsamples
    stddevYield -= avgYield**2
    #print('after:', stddevYield)
    stddevYield = np.sqrt(stddevYield)

if do_get_near_perfect_indices==1:
    np.savetxt(myfolder + '/yield_near_perfect.txt', np.c_[np.arange(traj_len),avgYield,stddevYield], header='No. samples = %d' % nsamples)
else:
    np.savetxt(myfolder + '/yield.txt', np.c_[np.arange(traj_len),avgYield,stddevYield], header='No. samples = %d' % nsamples)

