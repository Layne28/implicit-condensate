#Extract capsid c.o.m. and compute g(r) plus concentration

import numpy as np
import matplotlib.pyplot as plt
import pickle
import sys
import gsd.hoomd

def apply_pbc(pos,edges):

    arr1 = edges/2.0
    arr2 = -edges/2.0

    new_pos = np.zeros((pos.shape))
    new_pos = np.where(pos>=arr1, pos-edges, pos)
    new_pos = np.where(new_pos<arr2, new_pos+edges, new_pos)
    return new_pos

def get_capsid_coms(cluster_data, edges):

    #Identify capsids (nsubunits=12, nbonds=30 in final frame, exists in last snapshot)
    capsid_coms = []
    ncapsids=0
    for i in range(len(cluster_data.cluster_info)):
        nsubs = cluster_data.cluster_info[i].get_data()[-1]['num_bodies']
        nbonds = cluster_data.cluster_info[i].get_data()[-1]['bonds']['E-E']
        lifetime=cluster_data.cluster_info[i].get_lifetime()
        if nsubs==12 and nbonds==30 and lifetime==-1:
            ncapsids += 1
            pos_list = cluster_data.cluster_info[i].get_data()[-1]['positions']
            #print(pos_list)

            #To compute center of mass, we use a trick:
            #capsids will always be much smaller than the size of the periodic box,
            #so just take the position of one of the subunits and move it to the origin.
            #Move the positions of all the other subunits by the same amount, applying
            #pbc if necessary. Compute the center of mass in this shifted reference frame,
            #then subtract the position vector by which you originally shifted.
            pos_list_shifted = [apply_pbc(np.array(pos - pos_list[0]), edges) for pos in pos_list]
            #print(pos_list_shifted)
            com = sum(pos_list_shifted)/len(pos_list_shifted)
            com += pos_list[0]
            com = apply_pbc(com, edges)
            #print('com:', com)
            capsid_coms.append(com)
            #print()

    print('ncapsids:', ncapsids)

    capsid_com_arr = np.array(capsid_coms)
    print(capsid_com_arr.shape)
    return capsid_com_arr

def get_capsid_concs(pos, edges, Vr):

    #Compute background and condensate capsid concentrations
    Vtot = edges[0]*edges[1]*edges[2]
    Vc = Vr*Vtot
    R0 = pow(Vc/((4/3)*np.pi),1.0/3.0)
    print('R0:',R0)

    rhonc = 0
    rhonbg = 0
    dists = np.linalg.norm(pos,axis=1)
    #print(dists)
    num_in_cond = np.count_nonzero(dists<=R0)
    num_in_bg = np.count_nonzero(dists>R0)

    print('num in cond/bg:', num_in_cond, num_in_bg)

    rhonbg = num_in_bg/(Vtot-Vc)
    rhonc = num_in_cond/Vc

    print('conc in cond/bg:', rhonc, rhonbg)

    return rhonbg, rhonc


def main():

    myfile = sys.argv[1] #traj.gsd
    myfile2 = sys.argv[2] #traj.cl

    Vr=5e-3

    with open(myfile2,mode='rb') as f:
        cluster_data = pickle.load(f)

    traj = gsd.hoomd.open(myfile)
    edges = traj[0].configuration.box[:3]

    #Compute capsid centers of mass
    capsid_coms = get_capsid_coms(cluster_data, edges)

    #Compute g(r)

    #Compute capsid concentrations in background/condensate
    rhonbg, rhonc = get_capsid_concs(capsid_coms, edges, Vr)
    

    # fig = plt.figure()
    # ax = fig.add_subplot(projection='3d')
    # ax.scatter(capsid_com_arr[:,0],capsid_com_arr[:,1],capsid_com_arr[:,2])
    # plt.show()


if __name__=='__main__':
    main()