#!/bin/bash
#Submit production trajectories to run

nseed=4

Ns=(1200)
Ls=(144.2)
Vrs=(0.005) #(0.005 0.002 0.001)
Ebs=(5.100000 5.200000 5.300000 5.400000 5.600000 5.700000 5.800000 5.900000)
Ecs=(0.000000 1.000000 3.000000 5.000000 7.000000)
#Ebs=(5.0)
#Ecs=(7.0)

seeds=($(seq 1 $nseed))

cmd_list=()

for N in "${Ns[@]}"; do
    for L in "${Ls[@]}"; do
        for Vr in "${Vrs[@]}"; do
            for Eb in "${Ebs[@]}"; do
                for Ec in "${Ecs[@]}"; do
                    for seed in "${seeds[@]}"; do
		        if [ ! -f $SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=${N}/L=${L}/Vr=${Vr}/E_cond=${Ec}/E_bond=${Eb}/gamma_r=13.333333/seed=${seed}/traj.cl ]; then
    			    echo $SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=${N}/L=${L}/Vr=${Vr}/E_cond=${Ec}/E_bond=${Eb}/gamma_r=13.333333/seed=${seed}
			fi

                        #echo $SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=${N}/L=${L}/Vr=${Vr}/E_cond=${Ec}/E_bond=${Eb}/gamma_r=13.333333/seed=${seed}
                        #ls $SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=${N}/L=${L}/Vr=${Vr}/E_cond=${Ec}/E_bond=${Eb}/gamma_r=13.333333/seed=${seed}
                    done
                done
             done
        done
    done
done
