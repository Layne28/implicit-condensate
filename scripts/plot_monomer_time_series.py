#Plot yield of a trajectory

import matplotlib.pyplot as plt
import numpy as np
import sys

myfile = sys.argv[1]

Vr = float([e for e in myfile.split('/') if e.startswith('Vr')][0].split('=')[-1])
L = float([e for e in myfile.split('/') if e.startswith('L')][0].split('=')[-1])
Vtot = L**3
Vdrop = Vtot*Vr
Vbg = Vtot-Vdrop

data = np.loadtxt(myfile)

conc_background = np.zeros(data.shape[0])
conc_droplet = np.zeros(data.shape[0])

fig = plt.figure()
plt.plot(np.arange(data.shape[0]),conc_background,linewidth=0.3, label='monomer bg. conc.')
plt.plot(np.arange(data.shape[0]),conc_droplet,linewidth=0.3, label='monomer droplet conc.')
plt.legend()
plt.savefig('monomer_conc.png')
plt.show()

