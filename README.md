# Clustering of structures based on modeled XRD similatiry

This package provides following utilities:
* calculate XRD using a relaxed structure (such as a DFT relaxed structure)
* cluster structures in different groups for a given alloy composition (e.g., Ta12C11N1) based on calculated XRDs
* calculate thermodynamic properties based on statistical thermodynamics: paritition function, configurational free energy, thermodynamic density of states (TDOS)

# Requirements
* [Pylada](https://github.com/pylada/pylada-light)
* numpy
* pandas

# Steps to follow to cluster structures based on XRD similarity:
1. run `write_raw_xrd.py` to calculate raw XRDs for each structure. this is a python parallelized version and can be submitted as a single node SLURM job.
2. run `xrd_scale.py` to scale pairs of structures and calculate their optimized XRD differences. optimzied XRD differences lie in a range [0,2]. 
3. run `grouping.py` to cluster structures based on optimized XRD differences computed in step 2.
4. follow `XRD_grouping_Ta12C11N1.ipynb` inside `example` folder to cluster structures for a representative composition (Ta12C11N1).

# Calculate TDOS and Configurational free energies
Follow jupyter-notebook examples inside the `example` folder.
