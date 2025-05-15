#!/bin/bash
#Submit production trajectories to run

n_run_per_node=12 #4
script_name="$HOME/capsid-assembly/llps/droplet/scripts/run.py"

nseed=$1
startseed=5
endseed=10

Ns=(1200)
Ls=(288.5 228.9 181.7 158.7 133.9 117.0 106.3) #(117.0 106.3 49.3) #(288.5 228.9 181.7 158.7 144.2 133.9)
#Ls=(106.3)
Vrs=(0.005) #(0.005 0.002 0.001)
Ebs=(6.0) #(0.0 6.0)
#Ecs=(0.0 1.0 3.0 5.0 7.0)
Ecs=(0.0 3.0 5.0 7.0)

seeds=($(seq $startseed $endseed))

cmd_list=()

for N in "${Ns[@]}"; do
    for Eb in "${Ebs[@]}"; do
        for L in "${Ls[@]}"; do
            for Vr in "${Vrs[@]}"; do
                for Ec in "${Ecs[@]}"; do
                    for seed in "${seeds[@]}"; do
                        input_file=/work/laynefrechette/capsid-assembly/llps/droplet/initial_configurations/equil_start_N=${N}_L=${L}_seed=${seed}.gsd

                        out_file=$SCRATCH/capsid-assembly/llps/droplet/out_files/run_N=${N}_L=${L}_Vr=${Vr}_Eb=${Eb}_Ec=${Ec}_seed=${seed}.out

                        run_command="python ${script_name} --input_file ${input_file} --seed ${seed} --bond_energy ${Eb} --condensate_energy ${Ec} --volume_ratio ${Vr} --record_time_freq 200.0 --sim_time 6e5" # > ${out_file}"
                        sbatch $HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_run.sh "${run_command}"
                    done
                done
             done
        done
    done
done

