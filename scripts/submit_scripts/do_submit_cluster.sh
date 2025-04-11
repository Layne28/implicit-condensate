#!/bin/bash
#Submit production trajectories to run

n_run_per_node=64 #4
script_name="$HOME/capsid-assembly/llps/droplet/scripts/cluster.py"
ixn_file="$HOME/capsid-assembly/llps/droplet/interactions.txt"

nseed=$1

Ns=(1200)
#Ls=(288.5 228.9 181.7 158.7 144.2 133.9 117.0 106.3)
#Ls=(117.0 106.3 49.3)
Ls=(144.2)
Vrs=(0.005) #(0.005 0.002 0.001)
#Ebs=(6.000000)
#Ebs=(4.000000 4.500000 5.000000 5.500000 6.000000 6.500000 7.000000 7.500000 8.000000)
Ebs=(4.000000 4.500000 5.000000 5.500000 6.500000 7.000000 7.500000 8.000000)
#Ecs=(0.000000 1.000000 3.000000 5.000000 7.000000)
Ecs=(0.000000 3.000000 5.000000 7.000000)

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
                        cmd_list+=("${run_command}")
                    done
                done
             done
        done
    done
done

cmd_list_short=()
c=0
for cmd in "${cmd_list[@]}"; do
    echo $cmd
    cmd_list_short+=("${cmd}")
    c=$((c + 1))
    if [ $((c % ${n_run_per_node})) -eq 0 ]; then
        echo "submitting"
        sbatch $HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_cluster.sh "${cmd_list_short[@]}"
        #$HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_cluster.sh "${cmd_list_short[@]}"
        # for thing in "${cmd_list_short[@]}"; do
        #     echo $thing
        #     echo "\n"
        # done
        c=0
        cmd_list_short=()
    fi
done
sbatch $HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_cluster.sh "${cmd_list_short[@]}"

