#!/usr/bin/env python

#Check num frames in trajectory

import numpy as np
import sys
import os
import gsd.hoomd


def main():
    traj_len = 0
    myfile=str(sys.argv[1])

    if os.path.exists(myfile):
        traj = gsd.hoomd.open(myfile)
        traj_len = len(traj)

    return traj_len 

if __name__=="__main__":
    val = main()
    print(val)
