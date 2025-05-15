This project studies capsid self-assembly coupled to liquid-liquid phase separation using coarse-grained molecular dynamics simulations in HOOMD-blue. The "scripts" directory contains Python scripts for running and analyzing simulations. The "submit_scripts" subdirectory contains bash scripts for submitting jobs on NERSC's Perlmutter supercomputer (main branch) and the Brandeis HPCC (hpcc branch).

Key simulation scripts:
1. "initialize.py": Creates an initial lattice of capsid subunits.
2. "equilibrate.py": Randomizes the subunit positions while respecting excluded volume interactions.
3. "run.py": Runs molecular dynamics simulation of capsid assembly.

Key analysis scripts:
1. "cluster.py": Uses the SAASH analysis package (https://github.com/onehalfatsquared/SAASH.git) to get cluster size distributions.
2. "cluster_track_pos.py": Uses the SAASH analysis package to track detailed properties of individual clusters. Needed to get capsid centers of mass.
3. "get_avg_yield.py": From output of "cluster.py", compute the yield of individual trajectories, and then average yields over trajectories.
