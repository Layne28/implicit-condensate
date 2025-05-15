#Check that trajectory is complete

import numpy as np
import sys
import os
import gsd.hoomd

myfolder = sys.argv[1]

traj_len = 0
for i in range(10):

    if os.path.exists(myfolder + ("seed=%d/traj.gsd" % (i+1))):
        trajfile = myfolder + ("seed=%d/traj.gsd" % (i+1))
        traj = gsd.hoomd.open(trajfile)
        traj_len = len(traj)
        if traj_len<3000:
            print('TRAJECTORY INCOMPLETE')
            print(trajfile) 
            print(len(traj))


