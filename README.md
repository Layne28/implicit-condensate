This project studies capsid self-assembly coupled to liquid-liquid phase separation using coarse-grained molecular dynamics simulations in HOOMD-blue (v4). The "scripts" directory contains Python scripts for running and analyzing simulations of a dodecahedral capsid model (Perlmutter et al. 2013,  https://doi.org/10.7554/eLife.00632). The "submit_scripts" subdirectory contains bash scripts for submitting jobs on NERSC's Perlmutter supercomputer (main branch) and the Brandeis HPCC (hpcc branch).

Key simulation scripts:
1. "initialize.py": Creates an initial lattice of capsid subunits.
2. "equilibrate.py": Randomizes the subunit positions while respecting excluded volume interactions.
3. "run.py": Runs molecular dynamics simulation of capsid assembly.

Key analysis scripts:
1. "cluster.py": Uses the SAASH analysis package (https://github.com/onehalfatsquared/SAASH.git) to get cluster size distributions.
2. "cluster_track_pos.py": Uses the SAASH analysis package to track detailed properties of individual clusters. Needed to get capsid centers of mass.
3. "get_avg_yield.py": From output of "cluster.py", compute the yield of individual trajectories, and then average yields over trajectories.

The "Icosahedron_HOOMDv2" directory contains scripts for running simulations of an icosahedral capsid model (Wei et al. 2024, https://doi.org/10.1073/pnas.2312775121). Within this directory, the T1IcosahedronAssembly_wLLPS.py script uses HOOMD-blue (v2) to run molecular dynamics simulations of the model. Additional python scripts needed to run the code are located in the subdirectory "python-modules."