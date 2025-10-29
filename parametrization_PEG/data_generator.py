def generate_lammps_data(filename="lammps_data.txt"):
    """
    Generates a LAMMPS data file with atoms aligned along the x-axis.
    Atoms are placed at integer positions from x = -238 to x = 238.

    Parameters:
        filename (str): The name of the output file to save the data.

    Output format:
    atom_id molecule_id atom_type charge x y z
    """
    start_x = -238
    end_x = 238
    step = 1

    with open(filename, "w") as file:
        for atom_id, x in enumerate(range(start_x, end_x + step, step), start=1):
            file.write(f"{atom_id} 1 1 0.0 {x:.1f} 0.0 0.0\n")

# Generate the LAMMPS data file
generate_lammps_data("lammps_data.txt")

