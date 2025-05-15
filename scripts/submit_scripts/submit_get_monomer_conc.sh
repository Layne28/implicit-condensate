#!/bin/bash
#Get monomer conc

#SBATCH --account=hagan-lab
#SBATCH --partition=hagan-compute
#SBATCH --nodes=1
#SBATCH --time=4:00:00
#SBATCH --ntasks-per-node=4

module load conda
module --ignore-cache load "share_modules/HOOMD/4.6.0"

c=0
for cmd in "$@"
do
    echo $cmd
    echo ""
    #eval $cmd &
    #srun --exact -u -n 1 --cpus-per-task 2 ${cmd} & #> ${out_file} &
    ${cmd}
done
wait
