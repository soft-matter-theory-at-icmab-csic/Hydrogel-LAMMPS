import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft

# Function to read LAMMPS output file
def read_lammps_output(filename):
    data = []
    start_reading = False
    with open(filename, 'r') as file:
        for line in file:
            if "Step" in line:  # Detect header line
                start_reading = True
                continue
            if start_reading:
                values = line.split()
                if len(values) == 9:  # Ensure correct number of columns
                    try:
                        data.append(list(map(float, values)))
                    except ValueError:
                        continue
    
    columns = ["Step", "Temp", "Press", "TotEng", "Enthalpy", "E_pair", "Pxy", "Pxz", "Pyz"]
    df = pd.DataFrame(data, columns=columns)
    return df

# Compute Stress Autocorrelation Function (SACF)
def compute_sacf(stress_data):
    N = len(stress_data)
    sacf = np.correlate(stress_data, stress_data, mode='full') / N
    sacf = sacf[N-1:]  # Keep only positive time lags
    return sacf

# Compute Fourier transform to get G'(w) and G''(w)
def compute_moduli(sacf, dt):
    omega = np.fft.rfftfreq(len(sacf), d=dt) * 2 * np.pi  # Angular frequency
    G_complex = np.fft.rfft(sacf) * omega * 1j
    G_prime = G_complex.real  # Storage modulus
    G_double_prime = G_complex.imag  # Loss modulus
    print(G_prime[0:50])
    print(G_double_prime[0:50])
    return omega, G_prime, G_double_prime

# Main script
filename = "log_modified.lammps"  # Change this to your actual file name
df = read_lammps_output(filename)

if df.empty:
    print("Error: No valid data extracted from the file. Check the format.")
else:
    # Extract shear stress components
    Pxy = df["Pxy"].values
    Pxz = df["Pxz"].values
    Pyz = df["Pyz"].values

    # Average over the three components
    shear_stress = (Pxy + Pxz + Pyz) / 3

    # Compute SACF
    sacf = compute_sacf(shear_stress)

    dt = 100  # Time step between samples (modify if different)
    omega, G_prime, G_double_prime = compute_moduli(sacf, dt)

    # Plot results
    plt.figure(figsize=(8, 6))
    plt.loglog(omega[1:], G_prime[1:], label="G' (Storage Modulus)")
    #plt.loglog(omega[1:], G_double_prime[1:], label="G'' (Loss Modulus)", linestyle='dashed')
    plt.xlabel("Frequency (rad/s)")
    plt.ylabel("Modulus")
    plt.legend()
    plt.title("Storage and Loss Modulus")
    plt.grid()
    plt.show()

