#Plot yield of a trajectory

import matplotlib.pyplot as plt
import numpy as np
import sys

myfile = sys.argv[1]

data = np.loadtxt(myfile)

#Check the no. of columns to see if there is any assembly at all
#First column is frame, last column is max. cluster size in that frame

frac_monomers = np.zeros(data.shape[0])
frac_intermediates = np.zeros(data.shape[0])
frac_malformed = np.zeros(data.shape[0])

if data.shape[1]<14: #=12+2
    nsubunits = data[0][1]
    myYield = np.zeros(data.shape[0])

    for i in range(data.shape[1]-2):
        if i>0:
            frac_intermediates += (i+1)*data[:,i+1]/(1.0*nsubunits)
else:
    nsubunits = data[0][1]
    #myYield = (11*data[:,11]+12*data[:,12])/(1.0*nsubunits)
    myYield = (12*data[:,12])/(1.0*nsubunits)

    for i in range(data.shape[1]-2):
        if i<11 and i>0:
            frac_intermediates += (i+1)*data[:,i+1]/(1.0*nsubunits)

    for i in range(data.shape[1]-2-12):
        frac_malformed += (i+1+12)*data[:,i+1+12]/(1.0*nsubunits)

frac_monomers=data[:,1]/nsubunits

fig = plt.figure()
plt.plot(np.arange(data.shape[0]), myYield,linewidth=0.3, label='yield')
plt.plot(np.arange(data.shape[0]), frac_intermediates,linewidth=0.3, label='intermed.')
plt.plot(np.arange(data.shape[0]), frac_malformed,linewidth=0.3, label='malformed')
plt.plot(np.arange(data.shape[0]), frac_monomers,linewidth=0.3, label='monomers')
plt.ylim([0.0,1.0])
plt.legend()
plt.savefig('test.png')
plt.show()

