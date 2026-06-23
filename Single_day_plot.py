import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Read the radar data file
# -----------------------------
cols = [
    "Time",
    "Amp_Channel-1",
    "Amp_Channel-2",
    "Amp_Channel-3",
    "Amp_Channel-4"
]

df = pd.read_csv(
    "data/NARL_4_5_2022.txt",
    sep=r"\s+",
    names=cols,
    skiprows=1,
    engine="python"
)

# Display first few rows
print(df.head())

# Convert columns to float
for col in cols[1:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Remove any invalid rows
df = df.dropna()

# Create time axis (seconds)
time = np.arange(len(df))

# -----------------------------
# Plot all channels
# -----------------------------
plt.figure(figsize=(12, 6))

for col in cols[1:]:
    plt.plot(time, df[col], label=col)

plt.xlabel("Time (s)")
plt.ylabel("Amplitude (dB)")
plt.title("Radar Signal Amplitudes")
plt.legend()
plt.grid(True)

plt.show()

