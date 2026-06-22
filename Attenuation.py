import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ==========================================================
# INPUT FILE
# ==========================================================

file_path = "data/NARL_3_5_2022.txt"

# ==========================================================
# EXTRACT DATE AUTOMATICALLY FROM FILE NAME
# ==========================================================

date_str = (
    Path(file_path)
    .stem
    .replace("NARL_", "")
    .replace("_", "-")
)

# ==========================================================
# READ FILE
# ==========================================================

df = pd.read_csv(
    file_path,
    sep=r"\s+",
    engine="python"
)

# ==========================================================
# CHECK COLUMNS
# ==========================================================

print("\nColumns Found:")
print(df.columns.tolist())

# ==========================================================
# CHANNELS
# ==========================================================

channels = [
    'Amp_Channel-1',
    'Amp_Channel-2',
    'Amp_Channel-3',
    'Amp_Channel-4'
]

# ==========================================================
# CONVERT TO NUMERIC
# ==========================================================

for ch in channels:
    df[ch] = pd.to_numeric(df[ch], errors='coerce')

df = df.dropna()

# ==========================================================
# REFERENCE = MEAN OF TOP 5% STRONGEST SAMPLES
# ==========================================================

n_top = max(1, int(len(df) * 0.05))

references = {}

for ch in channels:

    strongest_samples = df[ch].nlargest(n_top)

    references[ch] = strongest_samples.mean()

# ==========================================================
# DISPLAY REFERENCE LEVELS
# ==========================================================

print("\n========================================")
print("Reference Levels (Top 5% Mean)")
print("========================================")

for ch in channels:
    print(f"{ch}: {references[ch]:.3f} dB")

# ==========================================================
# ATTENUATION CALCULATION
# ==========================================================

for ch in channels:

    att_col = ch.replace("Amp_", "Att_")

    df[att_col] = references[ch] - df[ch]

    # Remove negative attenuation values
    df[att_col] = df[att_col].clip(lower=0)

# ==========================================================
# MAXIMUM ATTENUATION
# ==========================================================

print("\n========================================")
print("Maximum Attenuation")
print("========================================")

for i in range(1, 5):

    att_col = f"Att_Channel-{i}"

    print(f"CH{i}: {df[att_col].max():.2f} dB")

# ==========================================================
# MATLAB STYLE 2x2 SUBPLOTS
# ==========================================================

fig, ax = plt.subplots(
    2,
    2,
    figsize=(15, 8)
)

# ---------------- CH1 ----------------

ax[0, 0].plot(df['Att_Channel-1'])

ax[0, 0].set_title('CH1')

ax[0, 0].set_ylabel('Attenuation (dB)')

ax[0, 0].grid(True)

# ---------------- CH2 ----------------

ax[0, 1].plot(df['Att_Channel-2'])

ax[0, 1].set_title('CH2')

ax[0, 1].set_ylabel('Attenuation (dB)')

ax[0, 1].grid(True)

# ---------------- CH3 ----------------

ax[1, 0].plot(df['Att_Channel-3'])

ax[1, 0].set_title('CH3')

ax[1, 0].set_xlabel('Sample Number')

ax[1, 0].set_ylabel('Attenuation (dB)')

ax[1, 0].grid(True)

# ---------------- CH4 ----------------

ax[1, 1].plot(df['Att_Channel-4'])

ax[1, 1].set_title('CH4')

ax[1, 1].set_xlabel('Sample Number')

ax[1, 1].set_ylabel('Attenuation (dB)')

ax[1, 1].grid(True)

# ==========================================================
# OVERALL TITLE WITH AUTOMATIC DATE
# ==========================================================

plt.suptitle(
    f'Attenuation Analysis ({date_str})',
    fontsize=16
)

plt.tight_layout()

plt.show()