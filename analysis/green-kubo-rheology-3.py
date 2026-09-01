import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.signal import hann

def read_lammps_output(filename):
    data = []
    start_reading = False
    with open(filename, 'r') as file:
        for line in file:
            if "Step" in line:
                start_reading = True
                continue
            if start_reading:
                values = line.split()
                if len(values) == 9:
                    try:
                        data.append(list(map(float, values)))
                    except ValueError:
                        continue
    
    columns = ["Step", "Temp", "Press", "TotEng", "Enthalpy", "E_pair", "Pxy", "Pxz", "Pyz"]
    df = pd.DataFrame(data, columns=columns)
    return df

def compute_sacf(stress_data):
    N = len(stress_data)
    sacf = np.correlate(stress_data, stress_data, mode='full') / N
    sacf = sacf[N-1:]  # Keep only positive time lags
    
    # Ensure SACF is non-negative
    sacf = np.maximum(sacf, 0)
    
    # Apply Hann window to reduce noise
    window = hann(len(sacf))
    sacf *= window
    
    return sacf

def moving_average(data, window_size=5):
    return np.convolve(data, np.ones(window_size)/window_size, mode='same')

def compute_moduli(sacf, dt):
    omega = np.fft.rfftfreq(len(sacf), d=dt) * 2 * np.pi
    G_complex = (1j * omega) * np.fft.rfft(sacf)  # Apply correct Green-Kubo prefactor
    G_prime = np.real(G_complex)
    G_double_prime = np.imag(G_complex)
    
    # Apply moving average filter to smooth results
    G_prime = moving_average(G_prime)
    G_double_prime = moving_average(G_double_prime)
    
    # Ensure G' is non-negative
    G_prime = np.maximum(G_prime, 0)
    
    return omega, G_prime, G_double_prime

filename = "log_modified.lammps"
df = read_lammps_output(filename)

if df.empty:
    print("Error: No valid data extracted from the file. Check the format.")
else:
    Pxy = df["Pxy"].values
    Pxz = df["Pxz"].values
    Pyz = df["Pyz"].values

    shear_stress = (Pxy + Pxz + Pyz) / 3

    sacf = compute_sacf(shear_stress)

    dt = 100
    omega, G_prime, G_double_prime = compute_moduli(sacf, dt)

    plt.figure(figsize=(8, 6))
    plt.loglog(omega[1:], G_prime[1:], label="G' (Storage Modulus)")
    plt.loglog(omega[1:], G_double_prime[1:], label="G'' (Loss Modulus)", linestyle='dashed')
    plt.xlabel("Frequency (rad/s)")
    plt.ylabel("Modulus")
    plt.legend()
    plt.title("Storage and Loss Modulus")
    plt.grid()
    plt.show()

