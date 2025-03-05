#Plot yield of a trajectory

import matplotlib.pyplot as plt
import numpy as np
import sys

myfile = sys.argv[1]

data = np.loadtxt(myfile)

#Check the no. of columns to see if there is any assembly at all
#First column is frame, last column is max. cluster size in that frame

if data.shape[1]<14: #=12+2
    myYield = np.zeros(data.shape[0])
else:
    nsubunits = data[0][1]
    myYield = 12*data[:,12]/(1.0*nsubunits)

fig = plt.figure()
plt.plot(np.arange(data.shape[0]), myYield,linewidth=0.3)
plt.ylim([0.0,1.0])
plt.savefig('test.png')
plt.show()

