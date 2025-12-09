# Rocket Lab Launch Analysis

A comprehensive Python project for analyzing Rocket Lab Electron launch vehicle performance data and mission statistics. This project provides tools for interpolating payload capacity estimates and performing detailed mission data analysis.

## Features

### 📊 Mission Data Analysis (`z-analyze.py`)
- **Customer Analytics**: Identify top customers by launch frequency and market share
- **Success Rate Tracking**: Analyze launch success rates by year and trends
- **Payload Statistics**: Examine payload mass distributions by orbit type
- **Launch Site Utilization**: Track usage patterns across different launch facilities
- **SQL-powered Analysis**: Uses DuckDB for efficient data processing

### 🚀 Payload Capacity Interpolation (`interpolation.py`)
- **Performance Modeling**: Interpolate Electron payload capacity for any altitude/inclination combination
- **Multi-dimensional Interpolation**: 
  - Linear interpolation across altitude (400-1200 km)
  - Linear interpolation across inclination (40°-100°)
- **Mission Validation**: Compare actual payloads against estimated maximum capacity
- **Capacity Utilization**: Calculate how efficiently each mission uses available payload capacity

## Data Coverage

The project analyzes **66 Rocket Lab missions** from 2017-2025, including:
- Mission outcomes (success/failure rates)
- Payload masses and satellite quantities
- Orbital parameters (altitude, inclination, orbit type)
- Customer information and launch sites
- Revenue and cost estimates
- Capacity utilization metrics

## Installation

1. Clone the repository
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Run Mission Analysis
```bash
python scripts/z-analyze.py
```

### Test Payload Interpolation
```bash
python scripts/interpolation.py
```

This will run interpolation tests against all mission data and show:
- Estimated maximum payload capacity for each mission's orbital parameters
- Actual vs. estimated capacity utilization
- Interpolation bounds and bracketing values

## Technical Details

- **Data Processing**: Pandas for data manipulation, DuckDB for SQL analytics
- **Interpolation**: SciPy for 2D linear interpolation
- **Visualization**: Matplotlib and Seaborn for plotting capabilities
- **Environment**: Jupyter notebook support for interactive analysis

## Key Insights

The analysis reveals trends in Rocket Lab's commercial operations including customer diversification, payload optimization, and operational efficiency across different orbit types and launch sites.
 
 

 













