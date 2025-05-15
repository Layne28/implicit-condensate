#!/bin/bash
#Run trajectory

#SBATCH --nodes=1
#SBATCH --account=hagan-lab
#SBATCH --partition=hagan-gpu
#SBATCH --ntasks-per-node=1
#SBATCH --time=48:00:00
#SBATCH --gres=gpu:V100:1
##SBATCH --constraint="V100|RTX2"
#SBATCH --nodes=1

module load conda
#conda activate hoomd480
module --ignore-cache load "share_modules/HOOMD/4.6.0"

c=0
for cmd in "$@"
do
    echo $cmd
    echo ""
    #eval $cmd &
    srun -u -n 1 ${cmd} & #> output_$SLURM_PROCID.txt &
    c=$((c + 1))
    if [ $((c % 4)) -eq 0 ]; then
        ps
        nvidia-smi
        echo "waiting"
        wait
    fi
done
wait
