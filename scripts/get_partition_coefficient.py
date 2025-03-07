#Get partition coefficient 

import matplotlib.pyplot as plt
import numpy as np
import sys
import numpy.linalg as la

import AnalysisTools.particle_io as pio
import AnalysisTools.measurement_tools as tools

myfile = sys.argv[1]

fileparts = myfile.split('/')
outfile = myfile.replace('traj.gsd', 'Kc.txt')

Vr = [e.split('=')[1] for e in fileparts if e.split('=')[0]=='Vr']
L = [e.split('=')[1] for e in fileparts if e.split('=')[0]=='L']
N = [e.split('=')[1] for e in fileparts if e.split('=')[0]=='N']
Ec = [e.split('=')[1] for e in fileparts if e.split('=')[0]=='E_cond']
Vr = float(Vr[0])
L = float(L[0])
N = int(N[0])
Ec = float(Ec[0])
print(L)
print(Vr)
print(N)
print(Ec)

Vcond = (L**3)*Vr
Rcond = (Vcond/(4.0*np.pi/3.0))**(1.0/3)
print(Rcond)

traj = pio.load_traj(myfile)
pos = traj['pos']

num_in_condensate = np.zeros(pos.shape[0])
partition_coefficient = np.zeros(pos.shape[0])
rho_bg = np.zeros(pos.shape[0])
rho_c = np.zeros(pos.shape[0])
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
    rho_bg[t] = rho2
    rho_c[t] = rho1
    print(partition_coefficient[t])
    #print('ncount:', ncount)
    #partition_coefficient[t] = (num_in_condensate[t]/Vcond)/((N)/(L**3))

#Save final partition coefficients and concentrations
rho_bg_avg = np.average(rho_bg[:-500])
rho_c_avg = np.average(rho_c[:-500])
partition_coefficient_avg = np.average(partition_coefficient[:-500])
with open(outfile, 'w') as f:
    f.write('rho_bg rho_c K_c\n')
    f.write('%f %f %f' % (rho_bg_avg, rho_c_avg, partition_coefficient_avg))

fig = plt.figure()
plt.plot(np.arange(0,pos.shape[0],1), partition_coefficient)
plt.axhline(y=np.average(partition_coefficient), color='red')
plt.savefig('partition_coefficient_vs_time_Ec=%f.png' % Ec)
#plt.show()

