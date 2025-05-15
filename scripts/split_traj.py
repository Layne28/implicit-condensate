import gsd.hoomd
import numpy
import os
import sys

myfile = sys.argv[1]


traj = gsd.hoomd.open(myfile)

traj_len = len(traj)
print(traj_len)
seglen = 1000

iframe1 = 0
iframe2 = 240000//600
iframe3 = 240000//60
iframe4 = 240000//6
#iframe4 = 240000//12
iframe5 = 240000-seglen
iframe6 = 250000//12-3000

iframes = [iframe1, iframe2, iframe3, iframe4, iframe5, iframe6]

for k in range(len(iframes)):
    if k==5:
        seglen=3000
    outfile1 = myfile.replace('traj.gsd', 'traj_seg%d.gsd' % (k+1))
    traj_seg = gsd.hoomd.open(outfile1, 'w')
    for i in range(seglen):
        traj_seg.append(traj[iframes[k]+i])
    print(len(traj_seg))

