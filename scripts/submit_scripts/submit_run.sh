#!/bin/bash
#Run trajectory

#SBATCH -A m4494
#SBATCH --qos=regular
#SBATCH --nodes=1
#SBATCH --constraint=gpu
#SBATCH --ntasks-per-node=4
#SBATCH --time=48:00:00

module load conda
conda activate hoomd

c=0
for cmd in "$@"
do
    echo $cmd
    echo ""
    #eval $cmd &
    srun --exact -u -n 1 --gpus-per-task 1 -c 16 --mem-per-gpu=55G ${cmd} & #> output_$SLURM_PROCID.txt &
    c=$((c + 1))
    if [ $((c % 4)) -eq 0 ]; then
        ps
        nvidia-smi
        echo "waiting"
        wait
    fi
done
wait
