
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATASET_DIR = BASE_DIR / "data" / "datasets"

print("\n========== HOSPITAL CSV SCHEMA REPORT ==========\n")

csv_files = sorted(DATASET_DIR.glob("*.csv"))

if not csv_files:
    print("No CSV files found!")
else:
    for file_path in csv_files:
        df = pd.read_csv(file_path)

        print("\n================================")
        print("FILE:", file_path.name)
        print("TOTAL ROWS:", len(df))
        print("TOTAL COLUMNS:", len(df.columns))
        print("\nCOLUMN NAMES AND DATA TYPES:")

        for column in df.columns:
            print(f"{column}: {df[column].dtype}")

print("\n========== INSPECTION COMPLETED ==========")
