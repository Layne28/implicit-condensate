#!/bin/bash
#Submit production trajectories to run

n_run_per_node=24 #4
script_name="$HOME/capsid-assembly/llps/droplet/scripts/run.py"

nseed=$1
startseed=10
endseed=10

Ns=(1200)
Ls=(144.2)
Vrs=(0.100) #(0.005 0.002 0.001)
#Ebs=(5.1 5.2 5.3 5.4 5.6 5.7 5.8 5.9)
#Ebs=(0.0)
Ebs=(0.0)
Ecs=(0.0)
#Ecs=(0.0 3.0 5.0 7.0)
#Ecs=(6.0)
#Ebs=(5.0)
#Ecs=(7.0)

seeds=($(seq $startseed $endseed))

cmd_list=()

for N in "${Ns[@]}"; do
    for L in "${Ls[@]}"; do
        for Vr in "${Vrs[@]}"; do
            for Eb in "${Ebs[@]}"; do
                for Ec in "${Ecs[@]}"; do
                    for seed in "${seeds[@]}"; do
                        input_file=/work/laynefrechette/capsid-assembly/llps/droplet/initial_configurations/equil_start_N=${N}_L=${L}_seed=${seed}.gsd
                        out_file=$SCRATCH/capsid-assembly/llps/droplet/out_files/run_N=${N}_L=${L}_Vr=${Vr}_Eb=${Eb}_Ec=${Ec}_seed=${seed}.out
                        run_command="python ${script_name} --input_file ${input_file} --seed ${seed} --bond_energy ${Eb} --condensate_energy ${Ec} --volume_ratio ${Vr} --record_time_freq 200.0 --sim_time 6e5 --is_nonint 1"
                        sbatch $HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_run.sh "${run_command}"
                    done
                done
             done
        done
    done
done
