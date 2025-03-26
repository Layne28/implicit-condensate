#!/bin/bash
#Submit production trajectories to run

n_run_per_node=12 #4
script_name="$HOME/capsid-assembly/llps/droplet/scripts/run.py"

nseed=$1

Ns=(1200)
Ls=(144.2)
Vrs=(0.005) #(0.005 0.002 0.001)
#Ebs=(6.5 7.0 7.5 8.0)
Ebs=(0.0 4.0 4.5 5.0 5.5 6.0 6.5 7.0 7.5 8.0)
Ecs=(0.0 1.0 3.0 5.0 7.0)

seeds=($(seq 1 $nseed))

cmd_list=()

for N in "${Ns[@]}"; do
    for L in "${Ls[@]}"; do
        for Vr in "${Vrs[@]}"; do
            for Eb in "${Ebs[@]}"; do
                for Ec in "${Ecs[@]}"; do
                    for seed in "${seeds[@]}"; do
                        input_file=$SCRATCH/capsid-assembly/llps/droplet/initial_configurations/equil_start_N=${N}_L=${L}_seed=${seed}.gsd

                        out_file=$SCRATCH/capsid-assembly/llps/droplet/out_files/run_N=${N}_L=${L}_Vr=${Vr}_Eb=${Eb}_Ec=${Ec}_seed=${seed}.out

                        run_command="python ${script_name} --input_file ${input_file} --seed ${seed} --bond_energy ${Eb} --condensate_energy ${Ec} --volume_ratio ${Vr} --record_time_freq 200.0 --sim_time 6e5"
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
        sbatch $HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_run.sh "${cmd_list_short[@]}"
        #$HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_run.sh "${cmd_list_short[@]}"
        # for thing in "${cmd_list_short[@]}"; do
        #     echo $thing
        #     echo "\n"
        # done
        c=0
        cmd_list_short=()
    fi
done
sbatch $HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_run.sh "${cmd_list_short[@]}"
