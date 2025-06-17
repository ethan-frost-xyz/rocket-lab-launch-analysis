import pandas as pd

# Create a structured DataFrame template to hold performance curve data
# for each inclination (40°, 60°, 80°, SSO) across various altitudes.

altitudes = [400, 500, 600, 700, 800, 900, 1000, 1100, 1200]

# Initialize with NaNs so user can fill in actual payload mass values
data = {
    "Altitude_km": altitudes,
    "Payload_40deg_kg": [None] * len(altitudes),
    "Payload_60deg_kg": [None] * len(altitudes),
    "Payload_80deg_kg": [None] * len(altitudes),
    "Payload_SSO_kg": [None] * len(altitudes),
}

df = pd.DataFrame(data)

# Save to CSV so user can populate it
file_path = "/mnt/data/electron_performance_curves_template.csv"
df.to_csv(file_path, index=False)

