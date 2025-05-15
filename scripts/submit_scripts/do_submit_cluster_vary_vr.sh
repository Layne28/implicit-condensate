#!/bin/bash
#Submit production trajectories to run

n_run_per_node=64 #4
script_name="$HOME/capsid-assembly/llps/droplet/scripts/cluster.py"
ixn_file="$HOME/capsid-assembly/llps/droplet/interactions.txt"

nseed=$1

Ns=(1200)
Ls=(144.2)
Vrs=(0.100 0.050 0.020 0.010 0.003 0.002 0.001)
#Vrs=(0.100 0.050 0.020 0.010 0.002) #(0.005 0.002 0.001)
Ebs=(6.000000)
Ecs=(0.000000 1.000000 3.000000 5.000000 7.000000)

seeds=($(seq 1 $nseed))

cmd_list=()

for N in "${Ns[@]}"; do
    for L in "${Ls[@]}"; do
        for Vr in "${Vrs[@]}"; do
            for Eb in "${Ebs[@]}"; do
                for Ec in "${Ecs[@]}"; do
                    for seed in "${seeds[@]}"; do
                        input_file=$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=${N}/L=${L}/Vr=${Vr}/E_cond=${Ec}/E_bond=${Eb}/gamma_r=13.333333/seed=${seed}/traj.gsd

                        out_file=$SCRATCH/capsid-assembly/llps/droplet/out_files/cluster_N=${N}_L=${L}_Vr=${Vr}_Eb=${Eb}_Ec=${Ec}_seed=${seed}.out

                        run_command="python ${script_name} ${input_file} ${ixn_file} 1"
                        sbatch $HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_cluster.sh "${run_command}"
                    done
                done
             done
        done
    done
done

