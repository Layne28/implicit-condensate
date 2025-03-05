#Get partition coefficient 

import matplotlib.pyplot as plt
import numpy as np
import sys
import numpy.linalg as la

import AnalysisTools.particle_io as pio
import AnalysisTools.measurement_tools as tools

myfile = sys.argv[1]

fileparts = myfile.split('/')

Vr = [e.split('=')[1] for e in fileparts if e.split('=')[0]=='Vr']
L = [e.split('=')[1] for e in fileparts if e.split('=')[0]=='L']
N = [e.split('=')[1] for e in fileparts if e.split('=')[0]=='N']
Vr = float(Vr[0])
L = float(L[0])
N = int(N[0])
print(L)
print(Vr)
print(N)

Vcond = (L**3)*Vr
Rcond = (Vcond/(4.0*np.pi/3.0))**(1.0/3)
print(Rcond)

traj = pio.load_traj(myfile)
pos = traj['pos']

num_in_condensate = np.zeros(pos.shape[0])
partition_coefficient = np.zeros(pos.shape[0])
for t in range(pos.shape[0]):
    print(t)
    ncount=0
    for i in range(pos.shape[1]):
        # if traj['particle_typeids'][i]==0:
        #     ncount += 1
        if traj['particle_typeids'][i]==0 and la.norm(pos[t,i,:])<=Rcond:#tools.get_dist(pos[t,i,:], np.zeros(3), traj['edges'])<=Rcond:
            num_in_condensate[t]+=1
    print('density in condensate/bulk:', num_in_condensate[t]/Vcond, (N-num_in_condensate[t])/(L**3-Vcond))
    rho1 = num_in_condensate[t]/Vcond
    rho2 = (N-num_in_condensate[t])/(L**3-Vcond)
    partition_coefficient[t] = rho1/rho2
    print(partition_coefficient[t])
    #print('ncount:', ncount)
    #partition_coefficient[t] = (num_in_condensate[t]/Vcond)/((N)/(L**3))

fig = plt.figure()
plt.plot(np.arange(0,pos.shape[0],1), partition_coefficient)
plt.axhline(y=np.average(partition_coefficient), color='red')
plt.savefig('partition_coefficient_vs_time.png')
plt.show()

