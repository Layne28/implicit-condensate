#!/bin/bash
#Submit production trajectories to run

script_name="$HOME/capsid-assembly/llps/droplet/scripts/run.py"
check_name="$HOME/capsid-assembly/llps/droplet/scripts/check_traj_len.py"

Ns=(1200)
#Ls=(144.2)
Ls=(288.5 228.9 181.7 158.7 133.9 117.0 106.3)
#Vrs=(0.100 0.050 0.020 0.010 0.003 0.002 0.001)
Vrs=(0.005)
Ebs=(6.000000)
#Ecs=(0.000000 1.000000 3.000000 5.000000 7.000000)
Ecs=(0.000000 3.000000 5.000000 7.000000)
#Ebs=(5.0)
#Ecs=(7.0)

startseed=1
endseed=10
seeds=($(seq $startseed $endseed))

cmd_list=()

for N in "${Ns[@]}"; do
    for L in "${Ls[@]}"; do
        for Vr in "${Vrs[@]}"; do
            for Eb in "${Ebs[@]}"; do
                for Ec in "${Ecs[@]}"; do
                    for seed in "${seeds[@]}"; do
                        #Check num frames in trajectory; if <3000 then rerun
                        trajfile="$SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=${N}/L=${L}/Vr=${Vr}/E_cond=${Ec}/E_bond=${Eb}/gamma_r=13.333333/seed=${seed}/traj.gsd"
                        #eval "python $HOME/capsid-assembly/llps/droplet/scripts/check_traj_len.py $trajfile"
                        nframes=$(python $HOME/capsid-assembly/llps/droplet/scripts/check_traj_len.py $trajfile)
                        #echo "num frames: $nframes"
		        if [ "$nframes" != "3000" ]; then
    			    echo $SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=${N}/L=${L}/Vr=${Vr}/E_cond=${Ec}/E_bond=${Eb}/gamma_r=13.333333/seed=${seed}
                            input_file=/work/laynefrechette/capsid-assembly/llps/droplet/initial_configurations/equil_start_N=${N}_L=${L}_seed=${seed}.gsd
			    run_command="python ${script_name} --input_file ${input_file} --seed ${seed} --bond_energy ${Eb} --condensate_energy ${Ec} --volume_ratio ${Vr} --record_time_freq 200.0 --sim_time 6e5"
                            sbatch $HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_run.sh "${run_command}"
			fi

                        #echo $SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=${N}/L=${L}/Vr=${Vr}/E_cond=${Ec}/E_bond=${Eb}/gamma_r=13.333333/seed=${seed}
                        #ls $SCRATCH/capsid-assembly/llps/droplet/assembly_trajectories/N=${N}/L=${L}/Vr=${Vr}/E_cond=${Ec}/E_bond=${Eb}/gamma_r=13.333333/seed=${seed}
                    done
                done
             done
        done
    done
done
