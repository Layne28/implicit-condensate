#!/bin/bash
#Submit production trajectories to run

n_run_per_node=24 #4
script_name="$HOME/capsid-assembly/llps/droplet/scripts/run.py"

N=1200
L=144.2
seed=1
input_file=/work/laynefrechette/capsid-assembly/llps/droplet/initial_configurations/equil_start_N=${N}_L=${L}_seed=${seed}.gsd

#Ec=0, Ess=6
Eb=6.0
Ec=0.0
Vr=0.005
run_command="python ${script_name} --input_file ${input_file} --seed ${seed} --bond_energy ${Eb} --condensate_energy ${Ec} --volume_ratio ${Vr} --record_time_freq 2.5 --sim_time 6e5"
sbatch $HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_run.sh "${run_command}"

#Ec=0, Ess=6, L=288.5
Eb=6.0
Ec=0.0
Vr=0.005
L=288.5
input_file=/work/laynefrechette/capsid-assembly/llps/droplet/initial_configurations/equil_start_N=${N}_L=${L}_seed=${seed}.gsd
run_command="python ${script_name} --input_file ${input_file} --seed ${seed} --bond_energy ${Eb} --condensate_energy ${Ec} --volume_ratio ${Vr} --record_time_freq 2.5 --sim_time 6e5"
sbatch $HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_run.sh "${run_command}"

#Ec=0, Ess=6, L=106.3
Eb=6.0
Ec=0.0
Vr=0.005
L=106.3
input_file=/work/laynefrechette/capsid-assembly/llps/droplet/initial_configurations/equil_start_N=${N}_L=${L}_seed=${seed}.gsd
run_command="python ${script_name} --input_file ${input_file} --seed ${seed} --bond_energy ${Eb} --condensate_energy ${Ec} --volume_ratio ${Vr} --record_time_freq 2.5 --sim_time 6e5"
sbatch $HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_run.sh "${run_command}"

#Ec=0, Ess=7
#Eb=7.0
#Ec=0.0
#Vr=0.005
#run_command="python ${script_name} --input_file ${input_file} --seed ${seed} --bond_energy ${Eb} --condensate_energy ${Ec} --volume_ratio ${Vr} --record_time_freq 2.5 --sim_time 6e5"
#sbatch $HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_run.sh "${run_command}"

#Ec=3, Ess=6
#Eb=6.0
#Ec=3.0
#Vr=0.005
#run_command="python ${script_name} --input_file ${input_file} --seed ${seed} --bond_energy ${Eb} --condensate_energy ${Ec} --volume_ratio ${Vr} --record_time_freq 2.5 --sim_time 6e5"
#sbatch $HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_run.sh "${run_command}"

#Ec=7, Ess=6
#Eb=6.0
#Ec=7.0
#Vr=0.005
#run_command="python ${script_name} --input_file ${input_file} --seed ${seed} --bond_energy ${Eb} --condensate_energy ${Ec} --volume_ratio ${Vr} --record_time_freq 2.5 --sim_time 6e5"
#sbatch $HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_run.sh "${run_command}"

#Ec=7, Ess=6, Vr=0.1
#Eb=6.0
#Ec=7.0
#Vr=0.100
#run_command="python ${script_name} --input_file ${input_file} --seed ${seed} --bond_energy ${Eb} --condensate_energy ${Ec} --volume_ratio ${Vr} --record_time_freq 2.5 --sim_time 6e5"
#sbatch $HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_run.sh "${run_command}"

#Ec=0, Ess=8
#Eb=8.0
#Ec=0.0
#Vr=0.005
#run_command="python ${script_name} --input_file ${input_file} --seed ${seed} --bond_energy ${Eb} --condensate_energy ${Ec} --volume_ratio ${Vr} --record_time_freq 2.5 --sim_time 6e5"
#sbatch $HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_run.sh "${run_command}"

#Ec=7, Ess=8
#Eb=8.0
#Ec=7.0
#Vr=0.005
#run_command="python ${script_name} --input_file ${input_file} --seed ${seed} --bond_energy ${Eb} --condensate_energy ${Ec} --volume_ratio ${Vr} --record_time_freq 2.5 --sim_time 6e5"
#sbatch $HOME/capsid-assembly/llps/droplet/scripts/submit_scripts/submit_run.sh "${run_command}"
