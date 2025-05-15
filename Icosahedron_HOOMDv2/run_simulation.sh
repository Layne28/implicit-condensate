#!/bin/bash

# Usage : Run the script with the following call :
# bash run_simulation <Subunit-Subunit Binding affinitiy> <Subunit Concentration > < Codnensate Potential well-depth > 

#get the strength and concentration command line args
Ess=$1
Conc=$2
Ec=$3

# Determine whether to resume or not:
RESTART=0
if [ -f T1_triangles_restart.gsd ]; then
	RESTART=1
	echo "You should resume in "$(pwd)"!" > "/dev/stderr"
fi

#set the python command to run. Check for restart and run it
cmd=python" T1IcosahedronAssembly_wLLPS.py input.conf  --user --side_energies [ $Ess $Ess $Ess $Ess $Ess $Ess ] --target_concentration $Conc --psdomain $Ec"
if (($RESTART)); then
	cmd=$cmd" --restart 1"
fi
echo $cmd
eval $cmd
