import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# USER INPUT
# ==========================================================

frequency_mhz = 500

# ==========================================================
# CONSTANTS
# ==========================================================

c = 3e8

frequency_hz = frequency_mhz * 1e6

# ==========================================================
# WAVELENGTH AND DIPOLE LENGTH
# ==========================================================

wavelength = c / frequency_hz

dipole_length = wavelength / 2

# ==========================================================
# THEORETICAL PARAMETERS
# ==========================================================

gain_dbi = 2.15

directivity = 1.64

radiation_resistance = 73

# ==========================================================
# DISPLAY PARAMETERS
# ==========================================================

print("\n====================================")
print("HALF-WAVE DIPOLE ANTENNA")
print("====================================")

print(f"Frequency           : {frequency_mhz} MHz")
print(f"Wavelength          : {wavelength:.4f} m")
print(f"Dipole Length       : {dipole_length:.4f} m")
print(f"Gain                : {gain_dbi:.2f} dBi")
print(f"Directivity         : {directivity:.2f}")
print(f"Radiation Resistance: {radiation_resistance} Ohms")

# ==========================================================
# 2D RADIATION PATTERN
# ==========================================================

theta = np.linspace(0.001, np.pi - 0.001, 2000)

E = np.cos((np.pi / 2) * np.cos(theta)) / np.sin(theta)

E = np.abs(E)

E = E / np.max(E)

# ==========================================================
# POLAR PLOT
# ==========================================================

plt.figure(figsize=(8,8))

ax = plt.subplot(111, projection='polar')

ax.plot(theta, E, linewidth=2)

ax.set_title(
    f'Half-Wave Dipole Radiation Pattern\n({frequency_mhz} MHz)',
    pad=20
)

plt.show()

# ==========================================================
# 3D RADIATION PATTERN
# ==========================================================

theta = np.linspace(0.001, np.pi - 0.001, 180)

phi = np.linspace(0, 2*np.pi, 360)

THETA, PHI = np.meshgrid(theta, phi)

R = np.abs(
    np.cos((np.pi/2)*np.cos(THETA))
    /
    np.sin(THETA)
)

R = R / np.max(R)

# ==========================================================
# SPHERICAL TO CARTESIAN
# ==========================================================

X = R * np.sin(THETA) * np.cos(PHI)

Y = R * np.sin(THETA) * np.sin(PHI)

Z = R * np.cos(THETA)

# ==========================================================
# 3D SURFACE PLOT
# ==========================================================

fig = plt.figure(figsize=(10,8))

ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(
    X,
    Y,
    Z,
    cmap='jet',
    linewidth=0,
    antialiased=True
)

ax.set_title(
    f'3D Radiation Pattern\nHalf-Wave Dipole ({frequency_mhz} MHz)'
)

ax.set_xlabel('X')

ax.set_ylabel('Y')

ax.set_zlabel('Z')

plt.show()