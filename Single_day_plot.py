import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplcursors
from pathlib import Path

# ==========================================================
# INPUT FILE
# ==========================================================

file_path = "data/NARL_14_5_2022.txt"

# ==========================================================
# AUTOMATIC DATE EXTRACTION
# ==========================================================

date_str = (
    Path(file_path)
    .stem
    .replace("NARL_", "")
    .replace("_", "-")
)

# ==========================================================
# COLUMN NAMES
# ==========================================================

cols = [
    "Time",
    "Amp_Channel-1",
    "Amp_Channel-2",
    "Amp_Channel-3",
    "Amp_Channel-4"
]

# ==========================================================
# READ FILE
# ==========================================================

df = pd.read_csv(
    file_path,
    sep=r"\s+",
    names=cols,
    skiprows=1,
    engine="python"
)

# ==========================================================
# DISPLAY FIRST FEW ROWS
# ==========================================================

print("\nFirst 5 Rows:")
print(df.head())

# ==========================================================
# CONVERT TIME COLUMN
# ==========================================================

df['Time'] = pd.to_datetime(
    df['Time'],
    format='%H:%M:%S'
)

# ==========================================================
# CONVERT CHANNELS TO NUMERIC
# ==========================================================

for col in cols[1:]:

    df[col] = pd.to_numeric(
        df[col],
        errors='coerce'
    )

df = df.dropna()

# ==========================================================
# PRINT BASIC STATISTICS
# ==========================================================

print("\n========================================")
print("Channel Statistics")
print("========================================")

for col in cols[1:]:

    print(f"\n{col}")

    print(
        f"Maximum : {df[col].max():.3f} dBm"
    )

    print(
        f"Minimum : {df[col].min():.3f} dBm"
    )

    print(
        f"Mean    : {df[col].mean():.3f} dBm"
    )

# ==========================================================
# GLOBAL Y-LIMITS
# (same scale for all channels)
# ==========================================================

global_min = df[cols[1:]].min().min()
global_max = df[cols[1:]].max().max()

margin = 2

global_min = global_min - margin
global_max = global_max + margin

# ==========================================================
# MATLAB STYLE 2x2 SUBPLOTS
# ==========================================================

fig, ax = plt.subplots(
    2,
    2,
    figsize=(15, 8)
)

# ==========================================================
# CH1
# ==========================================================

ax[0, 0].plot(
    df['Time'],
    df['Amp_Channel-1']
)

ax[0, 0].set_title(
    'CH1'
)

ax[0, 0].set_ylabel(
    'Amplitude (dBm)'
)

ax[0, 0].grid(True)

# ==========================================================
# CH2
# ==========================================================

ax[0, 1].plot(
    df['Time'],
    df['Amp_Channel-2']
)

ax[0, 1].set_title(
    'CH2'
)

ax[0, 1].set_ylabel(
    'Amplitude (dBm)'
)

ax[0, 1].grid(True)

# ==========================================================
# CH3
# ==========================================================

ax[1, 0].plot(
    df['Time'],
    df['Amp_Channel-3']
)

ax[1, 0].set_title(
    'CH3'
)

ax[1, 0].set_xlabel(
    'Time (IST)'
)

ax[1, 0].set_ylabel(
    'Amplitude (dBm)'
)

ax[1, 0].grid(True)

# ==========================================================
# CH4
# ==========================================================

ax[1, 1].plot(
    df['Time'],
    df['Amp_Channel-4']
)

ax[1, 1].set_title(
    'CH4'
)

ax[1, 1].set_xlabel(
    'Time (IST)'
)

ax[1, 1].set_ylabel(
    'Amplitude (dBm)'
)

ax[1, 1].grid(True)

# ==========================================================
# SAME Y-SCALE FOR ALL CHANNELS
# ==========================================================

for axes in ax.flat:

    axes.set_ylim(
        global_min,
        global_max
    )

# ==========================================================
# FORMAT X AXIS
# ==========================================================

for axes in ax.flat:

    axes.xaxis.set_major_formatter(
        mdates.DateFormatter('%H:%M')
    )

    axes.xaxis.set_major_locator(
        mdates.HourLocator(
            byhour=[0, 3, 6, 9, 12, 15, 18, 21]
        )
    )

    axes.tick_params(
        axis='x',
        rotation=45
    )

# ==========================================================
# OVERALL TITLE
# ==========================================================

plt.suptitle(
    f'Radar Signal Amplitudes ({date_str})',
    fontsize=16
)

plt.tight_layout()

# ==========================================================
# MATLAB-LIKE DATA CURSOR
# ==========================================================

cursor = mplcursors.cursor(
    hover=True
)

@cursor.connect("add")
def on_add(sel):

    x = mdates.num2date(
        sel.target[0]
    )

    y = sel.target[1]

    sel.annotation.set_text(
        f"Time: {x.strftime('%H:%M:%S')}\n"
        f"Amp: {y:.2f} dBm"
    )

plt.show()