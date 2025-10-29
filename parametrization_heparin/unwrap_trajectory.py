import MDAnalysis as mda
import MDAnalysis.transformations as trans
## from MDAnalysis.tests.datafiles import LAMMPSdata2, LAMMPSdcd2
##from MDAnalysis.analysis.molten import RadiusOfGyration
import numpy as np


# Load the LAMMPS topology and trajectory
data_file = "../equil_melt.data"  # LAMMPS data file (topology)
traj_file = "../PNCAll.dcd"  # LAMMPS trajectory file


# Load universe
u = mda.Universe(data_file, traj_file, format="LAMMPS")

# Apply unwrapping transformation
unwrap = trans.unwrap(u.atoms)
u.trajectory.add_transformations(unwrap)

# Select all atoms (or change to a specific group)
selection = u.select_atoms("all")  # Modify if you want only a subset of atoms


# Function to compute Rg for a given frame
def compute_rg(atom_group):
    masses = atom_group.masses
    total_mass = masses.sum()
    center_of_mass = np.average(atom_group.positions, weights=masses, axis=0)
    rg = np.sqrt(np.sum(masses * np.linalg.norm(atom_group.positions - center_of_mass, axis=1)**2) / total_mass)
    return rg


# Compute Rg for all frames
radii_of_gyration = []
times = []
for ts in u.trajectory:
    times.append(ts.time)
    radii_of_gyration.append(compute_rg(selection))


# Save results
output_file = "radius_of_gyration_manual.txt"
np.savetxt(output_file, np.column_stack((times, radii_of_gyration)),
           header="Time(ps) Radius_of_Gyration(Å)")

print(f"Radius of gyration data saved to {output_file}")

