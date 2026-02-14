import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks
from scipy.interpolate import interp1d




# PARAMETERS

rho = 1.0       # fluid density
U = 1.0          # mean inlet velocity
D = 0.2         # cylinder diameter (reference dimension)
Dq = 200        #coefficient computing



def process_geometry(input_file, rho, U, D, Dq, transient_ratio=0.6):
    data = np.loadtxt(input_file, skiprows=1)

    time = data[:, 0]
    Fx = data[:, 1]
    Fy = data[:, 2]

    dt = time[1] - time[0]

    # Aerodynamic coefficients
    q = 0.5 * rho * U**2 * Dq
    Cd = Fx / q
    Cl = Fy / q

    # Remove transient
    n = len(time)
    start = int(transient_ratio * n)

    time_ss = time[start:]
    Cl_ss = Cl[start:]
    Cd_ss = Cd[start:]

    # Find shedding period using minima of Cl
    peaks, _ = find_peaks(-Cl_ss, distance=int(0.2/dt))
    if len(peaks) < 2:
        raise RuntimeError(f"Not enough minima found in {input_file}")

    t0 = time_ss[peaks[0]]
    t1 = time_ss[peaks[1]]
    T = t1 - t0
    f = 1.0 / T

    # Extract one cycle
    mask = (time_ss >= t0) & (time_ss <= t1)
    time_cycle = time_ss[mask] - t0
    Cl_cycle = Cl_ss[mask]
    Cd_cycle = Cd_ss[mask]

    # RMS and mean values
    Cl_rms = np.sqrt(np.mean((Cl_ss - np.mean(Cl_ss))**2))
    Cd_mean = np.mean(Cd_ss)

    # Strouhal number
    St = f * D / U

    return {
        "time_cycle": time_cycle,
        "Cl_cycle": Cl_cycle,
        "Cd_cycle": Cd_cycle,
        "period": T,
        "frequency": f,
        "Strouhal": St,
        "Cl_rms": Cl_rms,
        "Cd_mean": Cd_mean
    }
    
    
    


geometries = {
    "Circular": "CC_Normal/VMS/FluidModelPart.Drag_cylinder_drag.dat",
    "Square":   "QC_Monolitich/VMS/FluidModelPart.Drag_Drag_Auto1_drag.dat",
    "Hexagon":  "HC_monolitich/VMS/FluidModelPart.Drag_Drag_Auto1_drag.dat"
}

results = {}

for name, file in geometries.items():
    results[name] = process_geometry(file, rho=1.0, U=1.0, D=0.2, Dq = 200)

    print(f"\n--- {name} ---")
    print(f"Period T           = {results[name]['period']:.4f} s")
    print(f"Frequency f        = {results[name]['frequency']:.4f} Hz")
    print(f"Strouhal number St = {results[name]['Strouhal']:.4f}")
    print(f"Mean Cd            = {results[name]['Cd_mean']:.4f}")
    print(f"Cl RMS             = {results[name]['Cl_rms']:.4f}")

#----------le seguenti figure mostrano il CD e CL con pochi punti (grafico spigoloso)-----------
#plt.figure()
#for name, data in results.items():
#    plt.plot(data["time_cycle"], data["Cl_cycle"]/data["period"], label=name)

#plt.xlabel(r"Non-dimensional time $t/T$")
#plt.ylabel(r"C_l")
#plt.legend()
#plt.grid()
#plt.savefig("post_processing/Cl_one_cycle_comparison.pdf", dpi=300)

#plt.figure()
#for name, data in results.items():
#    plt.plot(data["time_cycle"], data["Cd_cycle"]/data["period"], label=name)

#plt.xlabel(r"Non-dimensional time $t/T$")
#plt.ylabel(r"C_d")
#plt.legend()
#plt.grid()
#plt.savefig("post_processing/Cd_one_cycle_comparison.pdf", dpi=300)

plt.figure()
for name, data in results.items():
    t = data["time_cycle"]
    Cl = data["Cl_cycle"]
    T = data["period"]
    
    f_interp = interp1d(t, Cl, kind="cubic")
    t_fine = np.linspace(t.min(), t.max(), 300)
    Cl_fine = f_interp(t_fine)
    plt.plot(t_fine / T, Cl_fine, label=name)
    
plt.xlabel(r"Non-dimensional time $t/T$")
plt.ylabel(r"C_l")
plt.legend()
plt.grid()
plt.savefig("post_processing/Interpolated_Cl_one_cycle_comparison.pdf", dpi=300)

#------ CD DA VALUTARE (figura non è il massimo)------
plt.figure()
for name, data in results.items():
    t = data["time_cycle"]
    Cd = data["Cd_cycle"]
    T = data["period"]
    
    f_interp = interp1d(t, Cd, kind="cubic")
    t_fine = np.linspace(t.min(), t.max(), 300)
    Cd_fine = f_interp(t_fine)
    plt.plot(t_fine / T, Cd_fine, label=name)
    
plt.xlabel(r"Non-dimensional time $t/T$")
plt.ylabel(r"C_d")
plt.legend()
plt.grid()
plt.savefig("post_processing/Interpolated_Cd_one_cycle_comparison.pdf", dpi=300)

for name, d in results.items():
    print(f"{name} & {d['Strouhal']:.3f} & {d['Cd_mean']:.3f} & {d['Cl_rms']:.3f} \\\\")

