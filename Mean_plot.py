import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# File names
# --------------------------------------------------
files = {
    "03-05-2022": "data/NARL_3_5_2022.txt",
    "04-05-2022": "data/NARL_4_5_2022.txt",
    "05-05-2022": "data/NARL_5_5_2022.txt",
    "06-05-2022": "data/NARL_6_5_2022.txt",
    "07-05-2022": "data/NARL_7_5_2022.txt",
    "08-05-2022": "data/NARL_8_5_2022.txt",
    "09-05-2022": "data/NARL_9_5_2022.txt"
}

# Column names
cols = [
    "Time",
    "Amp_Channel-1",
    "Amp_Channel-2",
    "Amp_Channel-3",
    "Amp_Channel-4"
]

# Store daily means
results = []

# --------------------------------------------------
# Process each file
# --------------------------------------------------
for date, filename in files.items():

    print(f"Processing {filename}...")

    df = pd.read_csv(
        filename,
        sep=r"\s+",
        names=cols,
        skiprows=1,
        engine="python"
    )

    # Convert channels to numeric
    for ch in cols[1:]:
        df[ch] = pd.to_numeric(df[ch], errors="coerce")

    # Remove invalid rows
    df.dropna(inplace=True)

    # Calculate mean values
    results.append({
        "Date": date,
        "Ch1_Mean": df["Amp_Channel-1"].mean(),
        "Ch2_Mean": df["Amp_Channel-2"].mean(),
        "Ch3_Mean": df["Amp_Channel-3"].mean(),
        "Ch4_Mean": df["Amp_Channel-4"].mean()
    })

# --------------------------------------------------
# Create summary DataFrame
# --------------------------------------------------
summary = pd.DataFrame(results)

print("\nDaily Mean Values:\n")
print(summary)

# --------------------------------------------------
# Plot mean comparison
# --------------------------------------------------
plt.figure(figsize=(12,6))

plt.plot(summary["Date"], summary["Ch1_Mean"],
         marker='o', linewidth=2, label='Channel 1')

plt.plot(summary["Date"], summary["Ch2_Mean"],
         marker='o', linewidth=2, label='Channel 2')

plt.plot(summary["Date"], summary["Ch3_Mean"],
         marker='o', linewidth=2, label='Channel 3')

plt.plot(summary["Date"], summary["Ch4_Mean"],
         marker='o', linewidth=2, label='Channel 4')

plt.xlabel("Date")
plt.ylabel("Mean Amplitude (dB)")
plt.title("Daily Mean Amplitude Comparison (03-05-2022 to 09-05-2022)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()