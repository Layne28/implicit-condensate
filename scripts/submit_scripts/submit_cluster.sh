#!/bin/bash
#Run trajectory

#SBATCH -A m4494
#SBATCH --qos=regular
#SBATCH --nodes=1
#SBATCH --constraint=cpu
#SBATCH --ntasks-per-node=64
#SBATCH --time=4:00:00

module load conda
conda activate hoomd

c=0
for cmd in "$@"
do
    echo $cmd
    echo ""
    #eval $cmd &
    srun --exact -u -n 1 --cpus-per-task 2 ${cmd} & #> ${out_file} &
    c=$((c + 1))
    if [ $((c % 64)) -eq 0 ]; then
        echo "waiting"
        wait
    fi
done
wait
