#!/bin/bash
#Submit production trajectories to run

n_run_per_node=64 #4
script_name="$HOME/capsid-assembly/llps/droplet/scripts/get_monomer_background_conc_hpcc.py"

nseed=$1
startseed=1
endseed=10

Ns=(1200)
#Ls=(288.5 228.9 181.7 158.7 133.9 117.0 106.3)
#Ls=(117.0 106.3 49.3)
Ls=(144.2)
Vrs=(0.100) #(0.005 0.002 0.001)
Ebs=(6.000000)
#Ebs=(4.000000 4.500000 5.000000 5.500000 6.000000 6.500000 7.000000 7.500000 8.000000)
#Ebs=(5.100000 5.200000 5.300000 5.400000 5.600000 5.700000 5.800000 5.900000)
#Ecs=(0.000000 3.000000 5.000000 7.000000)
#Ecs=(7.000000)
Ecs=(2.000000 4.000000)

seeds=($(seq $startseed $endseed))

cmd_list=()

for N in "${Ns[@]}"; do
    for L in "${Ls[@]}"; do
        for Vr in "${Vrs[@]}"; do
            for Eb in "${Ebs[@]}"; do
                for Ec in "${Ecs[@]}"; do
                    for seed in "${seeds[@]}"; do
                        input_file=$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=${N}/L=${L}/Vr=${Vr}/E_cond=${Ec}/E_bond=${Eb}/gamma_r=13.333333/seed=${seed}/traj.gsd
                        input_file2=$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=${N}/L=${L}/Vr=${Vr}/E_cond=${Ec}/E_bond=${Eb}/gamma_r=13.333333/seed=${seed}/traj.cl

                        run_command="python ${script_name} ${input_file} ${input_file2}"
                        sbatch $HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_get_monomer_conc.sh "${run_command}"
                    done
                done
             done
        done
    done
done


