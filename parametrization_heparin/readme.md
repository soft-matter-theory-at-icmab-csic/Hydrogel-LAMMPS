## LAMMPS simulations of a single heparin molecule 

The objective is the parametrization of the PEG model, by changing the epsilon parameter of the LJ potential and comparing the obtained Rg with the values reported in the literature.

The files included here are:
- data_melt.equil: equilibrated coordinates of a single heparin molecule.
- equil_melt.data: 
- input_XXX.txt: example of input file for running  a simulation of a single PEG
- radi_gir.tcl: VMD analysis script in tcl to calculate the radius of gyration from the output of the LAMMPS simulation
- gnuplot_rgyr_distr.txt : script to be used with gnuplot program to make plots of the distribution of radius of gyration
