"""
Electron launch‑vehicle performance data and interpolation utilities.

Edit the altitude grid or payload arrays below as Rocket Lab publishes new figures.
The helper `capacity()` function linearly interpolates twice:
1. Along altitude for each inclination curve.
2. Across inclination to estimate capacity at any in‑between orbit.

Dependencies: numpy, scipy, pandas  (install with `pip install numpy scipy pandas`).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import os

# ---------------------------------------------------------------------------
# RAW DATA  ──────────────────────────────────────────────────────────────────
# Circular‐orbit altitudes (km). Must be strictly ascending.
orbital_altitude_km = np.array([
    400, 450, 500, 550, 600, 650, 700, 750, 800, 850,
    900, 950, 1000, 1050, 1100, 1150, 1200
], dtype=float)

# Payload mass capacity to orbit (kg) for each inclination curve at each orbital altitude
capacity_est_kg = {
    40: np.array([
        270.0, 266.6, 263.8, 259.9, 257.4, 254.0, 251.3, 247.0, 243.3,
        239.3, 235.7, 231.9, 228.3, 224.5, 221.0, 217.4, 214.0
    ], dtype=float),
    60: np.array([
        249.0, 245.9, 243.0, 240.0, 234.2, 232.4, 230.7, 227.7, 224.4,
        220.8, 217.7, 214.4, 211.4, 207.5, 204.2, 199.7, 197.3
    ], dtype=float),
    80: np.array([
        224.4, 221.2, 218.7, 216.1, 213.7, 210.4, 208.0, 204.4, 201.7,
        197.9, 194.8, 191.3, 188.4, 184.9, 181.7, 178.3, 175.7
    ], dtype=float),
    # Typical Sun‑synchronous orbit inclination 100°. Adjust if needed.
    100: np.array([
        203.7, 200.8, 198.4, 195.3, 192.9, 189.5, 187.0, 183.4, 180.3,
        177.0, 174.1, 170.7, 168.0, 164.4, 161.6, 158.5, 155.6
    ], dtype=float),
}

# Build 1‑D interpolators for every inclination curve (altitude ↦ payload).
_alt_interp = {
    inc: interp1d(orbital_altitude_km, mass, kind="linear", bounds_error=True)
    for inc, mass in capacity_est_kg.items()
}

# ---------------------------------------------------------------------------
# API  ───────────────────────────────────────────────────────────────────────

def capacity(alt_km: float, inc_deg: float) -> float:
    """Return estimated payload mass (kg) for *alt_km* and *inc_deg*.

    Parameters
    ----------
    alt_km : float
        Circular orbit altitude in kilometres. Must lie within `ALT_KM` span.
    inc_deg : float
        Desired orbital inclination in degrees. Must lie inside the bracket
        formed by the keys of ``PAYLOAD_KG``.
    """
    # Interpolate payload at *alt_km* along every stored inclination curve.
    inclinations = np.array(sorted(capacity_est_kg.keys()), dtype=float)
    payloads_alt = np.array([
        _alt_interp[inc](alt_km) for inc in inclinations
    ], dtype=float)

    # Now interpolate across inclination for the requested inc_deg.
    interp_inc = interp1d(inclinations, payloads_alt, kind="linear", bounds_error=True)
    return float(interp_inc(inc_deg))

def calculate_capacity_est_kg_python(alt_km: float, inc_deg: float) -> float | None:
    """Calculate interpolated capacity using the capacity() function.
    
    Parameters
    ----------
    alt_km : float
        Circular orbit altitude in kilometres
    inc_deg : float
        Orbital inclination in degrees
        
    Returns
    -------
    float | None
        Interpolated capacity in kg, or None if interpolation fails
    """
    try:
        return capacity(alt_km, inc_deg)
    except ValueError as e:
        # If interpolation fails (out of bounds), return None
        return None

def demo():  # pragma: no cover
    """Test interpolation with all mission data."""
    print("Testing interpolation with all mission data:")
    
    # Read the mission data using absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(os.path.dirname(script_dir), 'mission-data', 'mission_data.csv')
    df = pd.read_csv(csv_path)
    
    # Sort by mission number
    missions = df.sort_values('mission_number', ascending=True)
    
    print("\nMission Data Analysis:")
    print("-" * 80)
    
    for _, mission in missions.iterrows():
        try:
            mission_num = int(mission['mission_number'])
            name = mission['mission_name']
            
            # Get mission parameters, handling missing values
            alt = mission['orbit_altitude_km']
            inc = mission['orbital_inclination_deg']
            actual_payload = mission['payload_mass_kg']
            
            print(f"\nMission {mission_num}: {name}")
            
            # Print parameters if available
            if not np.isnan(alt):
                print(f"Altitude: {float(alt)} km", end="")
            else:
                print("Altitude: null", end="")
            
            if not np.isnan(inc):
                print(f", Inclination: {float(inc)}°")
            else:
                print(", Inclination: null")
            
            if not np.isnan(actual_payload):
                print(f"Actual Payload: {float(actual_payload)} kg")
            else:
                print("Actual Payload: null")
            
            # Calculate interpolated capacity if we have both altitude and inclination
            if not np.isnan(alt) and not np.isnan(inc):
                est_capacity = calculate_capacity_est_kg_python(float(alt), float(inc))
                if est_capacity is not None:
                    print(f"Estimated Max Capacity: {est_capacity:.1f} kg")
                    
                    # Calculate utilization if we have actual payload
                    if not np.isnan(actual_payload):
                        try:
                            payload_val = float(actual_payload)
                            if not np.isnan(payload_val) and payload_val > 0:
                                utilization = (payload_val / est_capacity) * 100
                                print(f"Capacity Utilization: {utilization:.1f}%")
                        except (ValueError, TypeError):
                            pass
                    
                    # Show bracketing values
                    alt_idx = np.searchsorted(orbital_altitude_km, float(alt))
                    if 0 < alt_idx < len(orbital_altitude_km):
                        lower_alt = orbital_altitude_km[alt_idx - 1]
                        upper_alt = orbital_altitude_km[alt_idx]
                        print(f"Bracketing altitudes: {lower_alt} km and {upper_alt} km")
                    
                    inclinations = sorted(capacity_est_kg.keys())
                    inc_idx = np.searchsorted(inclinations, float(inc))
                    if 0 < inc_idx < len(inclinations):
                        lower_inc = inclinations[inc_idx - 1]
                        upper_inc = inclinations[inc_idx]
                        print(f"Bracketing inclinations: {lower_inc}° and {upper_inc}°")
                else:
                    print("Estimated Max Capacity: null (parameters outside interpolation bounds)")
            else:
                print("Estimated Max Capacity: null (missing altitude or inclination data)")
            
            print("-" * 80)
        except ValueError:
            # If mission number is NaN, skip this iteration
            continue


if __name__ == "__main__":
    demo()
