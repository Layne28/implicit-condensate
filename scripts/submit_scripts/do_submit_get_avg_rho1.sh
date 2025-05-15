#!/bin/bash
#Get average yields

n_run_per_node=45 #4
script_name="$HOME/capsid-assembly/llps/droplet/scripts/get_avg_rho1.py"

Ns=(1200)
Ls=(144.2)
Vrs=(0.005)
Ebs=(0.000000)
Ecs=(0.000000 1.000000 2.000000 3.000000 4.000000 5.000000 6.000000 7.000000 8.000000)
#Ecs=(6.000000)

cmd_list=()

for N in "${Ns[@]}"; do
    for L in "${Ls[@]}"; do
        for Vr in "${Vrs[@]}"; do
            for Eb in "${Ebs[@]}"; do
                for Ec in "${Ecs[@]}"; do
		    input_file=/work/laynefrechette/capsid-assembly/llps/droplet/assembly_trajectories/N=${N}/L=${L}/Vr=${Vr}/E_cond=${Ec}/E_bond=${Eb}/gamma_r=13.333333/
		    echo ${input_file}
		    run_command="python ${script_name} ${input_file}"
		    eval $run_command
		    #sbatch $HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_get_partition_coefficient.sh "${run_command}"
                done
             done
        done
    done
done


