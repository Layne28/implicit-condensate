#!/bin/bash
#Submit production trajectories to run

n_run_per_node=10 #4
script_name="$HOME/capsid-assembly/llps/droplet/scripts/run.py"

nseed=$1

Ns=(1200)
Ls=(144.2) #(288.5 228.9 181.7 158.7 144.2 133.9)
Vrs=(0.005) #(0.005 0.002 0.001)
Ebs=(7.5)
Ecs=(0.0 1.0)
rhos=(2.0 3.0 4.0 5.0 10.0)

seeds=($(seq 1 $nseed))

cmd_list=()

for N in "${Ns[@]}"; do
    for Eb in "${Ebs[@]}"; do
        for L in "${Ls[@]}"; do
            for Vr in "${Vrs[@]}"; do
                for Ec in "${Ecs[@]}"; do
                    for rho in "${rhos[@]}"; do
                        for seed in "${seeds[@]}"; do
                            input_file=$SCRATCH/capsid-assembly/llps/droplet/initial_configurations/equil_start_N=${N}_L=${L}_seed=${seed}.gsd

                            out_file=$SCRATCH/capsid-assembly/llps/droplet/out_files/run_N=${N}_L=${L}_Vr=${Vr}_Eb=${Eb}_Ec=${Ec}_seed=${seed}.out

                            run_command="python ${script_name} --input_file ${input_file} --seed ${seed} --bond_energy ${Eb} --condensate_energy ${Ec} --volume_ratio ${Vr} --rho ${rho} --record_time_freq 100.0"
                            cmd_list+=("${run_command}")
                        done
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

