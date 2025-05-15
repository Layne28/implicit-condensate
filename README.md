This project studies capsid self-assembly coupled to liquid-liquid phase separation using coarse-grained molecular dynamics simulations in HOOMD-blue. The "scripts" directory contains Python scripts for running and analyzing simulations. The "submit_scripts" subdirectory contains bash scripts for submitting jobs on NERSC's Perlmutter supercomputer (main branch) and the Brandeis HPCC (hpcc branch).

Key simulation scripts:
1. "initialize.py": Creates an initial lattice of capsid subunits.
2. "equilibrate.py": Randomizes the subunit positions while respecting excluded volume interactions.
3. "run.py": Runs molecular dynamics simulation of capsid assembly.
