#!/bin/bash
#Submit production trajectories to run

script_name="$HOME/capsid-assembly/llps/droplet/scripts/cluster.py"
ixn_file="$HOME/capsid-assembly/llps/droplet/interactions.txt"

#nseed=4
startseed=5
endseed=10

Ns=(1200)
Ls=(144.2)
Vrs=(0.100 0.050 0.020 0.010 0.003 0.002 0.001)
Ebs=(6.000000)
Ecs=(0.000000 3.000000 5.000000 7.000000)
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
		        if [ ! -f $SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=${N}/L=${L}/Vr=${Vr}/E_cond=${Ec}/E_bond=${Eb}/gamma_r=13.333333/seed=${seed}/traj.sizes ]; then
    			    echo $SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=${N}/L=${L}/Vr=${Vr}/E_cond=${Ec}/E_bond=${Eb}/gamma_r=13.333333/seed=${seed}
                            input_file=$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=${N}/L=${L}/Vr=${Vr}/E_cond=${Ec}/E_bond=${Eb}/gamma_r=13.333333/seed=${seed}/traj.gsd
			    run_command="python ${script_name} ${input_file} ${ixn_file} 1"
                            sbatch $HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_cluster.sh "${run_command}"
			fi

                        #echo $SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=${N}/L=${L}/Vr=${Vr}/E_cond=${Ec}/E_bond=${Eb}/gamma_r=13.333333/seed=${seed}
                        #ls $SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=${N}/L=${L}/Vr=${Vr}/E_cond=${Ec}/E_bond=${Eb}/gamma_r=13.333333/seed=${seed}
                    done
                done
             done
        done
    done
done
