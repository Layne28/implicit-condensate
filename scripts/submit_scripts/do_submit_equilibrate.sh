#!/bin/bash
#Get average yields

nseed=$1

script_name="$HOME/capsid-assembly/llps/droplet/scripts/equilibrate.py"

Ns=(1200)
#Ls=(288.5 228.9 181.7 158.7 144.2 133.9)
#Ls=(144.2)
Ls=(228.9 181.7 158.7 133.9 117.0 106.3)
Vrs=(0.005) #(0.005 0.002 0.001)

seeds=($(seq 1 $nseed))

cmd_list=()

for N in "${Ns[@]}"; do
    for L in "${Ls[@]}"; do
        for Vr in "${Vrs[@]}"; do
            for seed in "${seeds[@]}"; do
                input_file=$HOME/capsid-assembly/llps/droplet/initial_configurations/lattice_N=${N}_L=${L}.gsd
                echo ${input_file}

                run_command="python ${script_name} -i ${input_file} -s ${seed}"
                cmd_list+=("${run_command}")
                eval $run_command
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

