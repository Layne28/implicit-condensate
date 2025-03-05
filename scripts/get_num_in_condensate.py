#Plot yield of a trajectory

import matplotlib.pyplot as plt
import numpy as np
import sys

import AnalysisTools.particle_io as pio
import AnalysisTools.measurement_tools as tools

myfile = sys.argv[1]

fileparts = myfile.split('/')

Vr = [e.split('=')[1] for e in fileparts if e.split('=')[0]=='Vr']
L = [e.split('=')[1] for e in fileparts if e.split('=')[0]=='L']
Vr = float(Vr[0])
L = float(L[0])

Vcond = (L**3)*Vr
Rcond = pow(Vcond/((4.0/3.0)*np.pi), 1.0/3.0)
print(Rcond)

traj = pio.load_traj(myfile)
pos = traj['pos']

print(np.min(pos))
print(np.max(pos))

num_in_condensate = np.zeros(pos.shape[0])
for t in range(pos.shape[0]):
    print(t)
    for i in range(pos.shape[1]):
        if tools.get_min_dist(pos[t,i,:], np.zeros(3), traj['edges'])<=Rcond:
            num_in_condensate[t]+=1

fig = plt.figure()
plt.plot(np.arange(0,pos.shape[0],1), num_in_condensate)
plt.savefig('num_in_condensate.png')
plt.show()

