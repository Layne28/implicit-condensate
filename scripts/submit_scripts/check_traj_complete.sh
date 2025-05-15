#!/bin/bash
#Get average yields

n_run_per_node=45 #4
script_name="$HOME/capsid-assembly/llps/droplet/scripts/check_traj_complete.py"

Ns=(1200)
Ls=(288.5 228.9 181.7 158.7 133.9 117.0 106.3)
#Ls=(144.2)
Vrs=(0.005)
Ebs=(6.000000)
#Ebs=(4.000000 4.500000 5.000000 5.500000 6.000000 6.500000 7.000000 7.500000 8.000000)
#Ebs=(5.100000 5.200000 5.300000 5.400000 5.600000 5.700000 5.800000 5.900000)
Ecs=(0.000000 3.000000 5.000000 7.000000)
#Ecs=(2.000000 4.000000)

nseed=4

seeds=($(seq 1 $nseed))

cmd_list=()

for N in "${Ns[@]}"; do
    for L in "${Ls[@]}"; do
        for Vr in "${Vrs[@]}"; do
            for Eb in "${Ebs[@]}"; do
                for Ec in "${Ecs[@]}"; do
                    input_folder=$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=${N}/L=${L}/Vr=${Vr}/E_cond=${Ec}/E_bond=${Eb}/gamma_r=13.333333/
                    echo ${input_folder}
                    out_file=$SCRATCH/capsid-assembly/llps/droplet/out_files/get_avg_yield_N=${N}_L=${L}_Vr=${Vr}_Eb=${Eb}_Ec=${Ec}.out

                    run_command="python ${script_name} ${input_folder}"
                    cmd_list+=("${run_command}")
                    eval $run_command
                done
             done
        done
    done
done

# cmd_list_short=()
# c=0
# for cmd in "${cmd_list[@]}"; do
#     echo $cmd
#     cmd_list_short+=("${cmd}")
#     c=$((c + 1))
#     if [ $((c % ${n_run_per_node})) -eq 0 ]; then
#         echo "submitting"
#         #sbatch $HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_cluster.sh "${cmd_list_short[@]}"
#         #$HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_cluster.sh "${cmd_list_short[@]}"
#         c=0
#         cmd_list_short=()
#     fi
# done

