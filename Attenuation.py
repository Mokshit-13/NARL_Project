import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
import mplcursors

# ==========================================================
# INPUT FILE
# ==========================================================

file_path = "data/NARL_11_5_2022.txt"

# ==========================================================
# EXTRACT DATE AUTOMATICALLY
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
# CONVERT TIME COLUMN
# ==========================================================

df['Time'] = pd.to_datetime(
    df['Time'],
    format='%H:%M:%S'
)

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
    df[ch] = pd.to_numeric(
        df[ch],
        errors='coerce'
    )

df = df.dropna()
# ==========================================================
# REFERENCE = TOP 5% MEAN
# ==========================================================

n_top = max(
    1,
    int(len(df) * 0.05)
)

references = {}

for ch in channels:

    strongest_samples = (
        df[ch]
        .nlargest(n_top)
    )

    references[ch] = (
        strongest_samples.mean()
    )

    print(f"\n{ch}")

    print(
        "Top 5 Values :",
        strongest_samples
        .nlargest(5)
        .tolist()
    )

    print(
        f"Reference (Mean of Top 5) : "
        f"{references[ch]:.3f}"
    )
# ==========================================================
# DISPLAY REFERENCE LEVELS
# ==========================================================

print("\n========================================")
print("Reference Levels (Top-5 Mean)")
print("========================================")

for ch in channels:

    print(
        f"{ch}: "
        f"{references[ch]:.3f} dB"
    )

# ==========================================================
# ATTENUATION CALCULATION
# ==========================================================

for ch in channels:

    att_col = (
        ch.replace(
            "Amp_",
            "Att_"
        )
    )

    df[att_col] = (
        references[ch]
        - df[ch]
    )

    df[att_col] = (
        df[att_col]
        .clip(lower=0)
    )
# ==========================================================
# CREATE PER-MINUTE ATTENUATION DATA
# ==========================================================

minute_df = pd.DataFrame()

# Convert HH:MM:SS -> HH:MM

minute_df['Minute'] = (
    df['Time']
    .dt.strftime('%H:%M')
)

minute_df['Att_Channel-1'] = df['Att_Channel-1']
minute_df['Att_Channel-2'] = df['Att_Channel-2']
minute_df['Att_Channel-3'] = df['Att_Channel-3']
minute_df['Att_Channel-4'] = df['Att_Channel-4']

# ==========================================================
# AVERAGE ATTENUATION FOR EACH MINUTE
# ==========================================================

minute_df = (
    minute_df
    .groupby('Minute')
    .mean()
    .reset_index()
)

# ==========================================================
# SAVE FILE
# ==========================================================

output_file = (
    Path(file_path).parent
    /
    f"Attenuation_{Path(file_path).name}"
)

minute_df.to_csv(
    output_file,
    sep='\t',
    index=False,
    float_format='%.4f'
)

print("\n========================================")
print("Per-Minute Attenuation File Saved")
print("========================================")
print(output_file)

# ==========================================================
# MAXIMUM ATTENUATION
# ==========================================================

print("\n========================================")
print("Maximum Attenuation")
print("========================================")

for i in range(1, 5):

    att_col = f"Att_Channel-{i}"

    print(
        f"CH{i}: "
        f"{df[att_col].max():.2f} dB"
    )

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
    df['Att_Channel-1']
)

ax[0, 0].set_title(
    'CH1'
)

ax[0, 0].set_ylabel(
    'Attenuation (dB)'
)

ax[0, 0].grid(True)

# ==========================================================
# CH2
# ==========================================================

ax[0, 1].plot(
    df['Time'],
    df['Att_Channel-2']
)

ax[0, 1].set_title(
    'CH2'
)

ax[0, 1].set_ylabel(
    'Attenuation (dB)'
)

ax[0, 1].grid(True)

# ==========================================================
# CH3
# ==========================================================

ax[1, 0].plot(
    df['Time'],
    df['Att_Channel-3']
)

ax[1, 0].set_title(
    'CH3'
)

ax[1, 0].set_xlabel(
    'Time (IST)'
)

ax[1, 0].set_ylabel(
    'Attenuation (dB)'
)

ax[1, 0].grid(True)

# ==========================================================
# CH4
# ==========================================================

ax[1, 1].plot(
    df['Time'],
    df['Att_Channel-4']
)

ax[1, 1].set_title(
    'CH4'
)

ax[1, 1].set_xlabel(
    'Time (IST)'
)

ax[1, 1].set_ylabel(
    'Attenuation (dB)'
)

ax[1, 1].grid(True)

# ==========================================================
# FORMAT X AXIS AS HOURS
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
# FORCE Y-AXIS TO START FROM 0 dB
# ==========================================================

for axes in ax.flat:

    ymax = axes.get_ylim()[1]

    axes.set_ylim(
        0,
        ymax
    )

# ==========================================================
# OVERALL TITLE
# ==========================================================

plt.suptitle(
    f'DRSP Rain Attenuation ({date_str})',
    fontsize=16
)

plt.tight_layout()

# ==========================================================
# DATA CURSOR (MATLAB-LIKE)
# ==========================================================

cursor = mplcursors.cursor(
    hover=True
)

@cursor.connect("add")
def on_add(sel):

    x = mdates.num2date(sel.target[0])

    y = sel.target[1]

    sel.annotation.set_text(
        f"Time: {x.strftime('%H:%M:%S')}\n"
        f"Att: {y:.2f} dB"
    )

plt.show()
