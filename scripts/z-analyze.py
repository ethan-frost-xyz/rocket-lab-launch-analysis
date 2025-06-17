import pandas as pd
import duckdb
import os
from typing import Optional
from pathlib import Path

def load_data(csv_path: Path) -> Optional[pd.DataFrame]:
    """Load and clean the mission data from CSV."""
    try:
        # Skip the empty first row and use the second row as headers
        df = pd.read_csv(csv_path, skiprows=[0])
        
        # Drop any completely empty rows
        df = df.dropna(how='all')
        
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y')
        
        # Convert numeric columns
        numeric_cols = ['mission_no', 'type_no', 'satellite_quantity', 'payload_mass_kg']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def analyze_missions(df: pd.DataFrame) -> None:
    """Perform various analyses on the mission data."""
    try:
        # Register DataFrame with DuckDB
        duckdb.register('missions', df)
        
        # 1. Launches per customer
        customer_analysis = duckdb.query("""
            WITH split_customers AS (
                SELECT 
                    mission_no,
                    UNNEST(string_split(customers, ',')) as customer
                FROM missions
                WHERE customers IS NOT NULL
            )
            SELECT 
                trim(customer) as customer,
                COUNT(*) as launch_count,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM missions), 2) as percentage
            FROM split_customers
            GROUP BY customer
            ORDER BY launch_count DESC
            LIMIT 10
        """).to_df()
        
        print("\n=== Top 10 Customers by Launch Count ===")
        print(customer_analysis.to_string(index=False))
        
        # 2. Launch success rate by year
        success_rate = duckdb.query("""
            SELECT 
                EXTRACT(year FROM date) as year,
                COUNT(*) as total_launches,
                SUM(CASE WHEN mission_outcome = 'Success' THEN 1 ELSE 0 END) as successful_launches,
                ROUND(SUM(CASE WHEN mission_outcome = 'Success' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as success_rate
            FROM missions
            GROUP BY year
            ORDER BY year DESC
        """).to_df()
        
        print("\n=== Launch Success Rate by Year ===")
        print(success_rate.to_string(index=False))
        
        # 3. Payload statistics by orbit type
        payload_stats = duckdb.query("""
            SELECT 
                orbit_type,
                COUNT(*) as launches,
                ROUND(AVG(payload_mass_kg), 2) as avg_payload_kg,
                ROUND(MIN(payload_mass_kg), 2) as min_payload_kg,
                ROUND(MAX(payload_mass_kg), 2) as max_payload_kg
            FROM missions
            WHERE orbit_type IS NOT NULL 
                AND payload_mass_kg IS NOT NULL
            GROUP BY orbit_type
            ORDER BY launches DESC
        """).to_df()
        
        print("\n=== Payload Statistics by Orbit Type ===")
        print(payload_stats.to_string(index=False))
        
        # 4. Launch site utilization
        site_stats = duckdb.query("""
            SELECT 
                launch_site,
                COUNT(*) as launches,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM missions), 2) as percentage
            FROM missions
            WHERE launch_site IS NOT NULL
            GROUP BY launch_site
            ORDER BY launches DESC
        """).to_df()
        
        print("\n=== Launch Site Utilization ===")
        print(site_stats.to_string(index=False))

    except Exception as e:
        print(f"Error during analysis: {e}")

def main():
    # Get the project root directory
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    csv_path = project_root / "mission-data" / "mission_data.csv"
    
    # Load the data
    df = load_data(csv_path)
    if df is not None:
        analyze_missions(df)
    else:
        print("Failed to load mission data. Please check the CSV file.")

if __name__ == "__main__":
    main()
