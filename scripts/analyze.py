import pandas as pd
import duckdb
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

# Load your data, skipping empty rows and specifying header row
csv_path = os.path.join(project_root, "mission-data", "mission_data.csv")
df = pd.read_csv(csv_path, skiprows=2)

# Sample analysis: how many launches by customer
launches_per_customer = duckdb.query("""
    SELECT "Customer(s)" as customer, COUNT(*) as launches
    FROM df
    WHERE "Customer(s)" IS NOT NULL
    GROUP BY "Customer(s)"
    ORDER BY launches DESC
""").to_df()

print(launches_per_customer)
