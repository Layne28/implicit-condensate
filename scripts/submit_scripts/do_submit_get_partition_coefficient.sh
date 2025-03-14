#!/bin/bash
#Get average yields

n_run_per_node=45 #4
script_name="$HOME/capsid-assembly/llps/droplet/scripts/get_partition_coefficient.py"

Ns=(1200)
Ls=(144.2)
Vrs=(0.005)
Ebs=(0.000000)
Ecs=(0.000000 1.000000 3.000000 5.000000 7.000000)

nseed=$1
seeds=($(seq 1 $nseed))

cmd_list=()

for N in "${Ns[@]}"; do
    for L in "${Ls[@]}"; do
        for Vr in "${Vrs[@]}"; do
            for Eb in "${Ebs[@]}"; do
                for Ec in "${Ecs[@]}"; do
                    input_folder=$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=${N}/L=${L}/Vr=${Vr}/E_cond=${Ec}/E_bond=${Eb}/
                    echo ${input_folder}
                    for seed in "${seeds[@]}"; do
                        seed_file="${input_folder}seed=${seed}/traj.gsd"
                        echo ${seed_file}
                        #out_file=$SCRATCH/capsid-assembly/llps/droplet/out_files/get_avg_yield_N=${N}_L=${L}_Vr=${Vr}_Eb=${Eb}_Ec=${Ec}.out

                        run_command="python ${script_name} ${seed_file}"
                        cmd_list+=("${run_command}")
                        eval $run_command
                    done
                    avg_script_name="$HOME/capsid-assembly/llps/droplet/scripts/get_avg_partition_coefficient.py"
                    avg_command="python ${avg_script_name} ${input_folder}"
                    eval $avg_command
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

