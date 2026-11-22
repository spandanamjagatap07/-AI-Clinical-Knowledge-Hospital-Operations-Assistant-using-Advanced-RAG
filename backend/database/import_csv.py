
from pathlib import Path
import pandas as pd
from sqlalchemy import text

from backend.database.db_connection import engine

BASE_DIR = Path(__file__).resolve().parents[2]
DATASET_DIR = BASE_DIR / "data" / "datasets"

CSV_FILES = [
    "departments",
    "patients",
    "doctors",
    "nurses",
    "appointments",
    "admissions",
    "discharges",
    "lab_results",
    "pharmacy_inventory",
    "prescriptions",
    "billing",
    "insurance",
    "bed_management",
    "ot_schedule",
    "incident_reports",
]


def import_csv_files():
    print("\n========== CSV IMPORT STARTED ==========")

    # Check that all database tables are empty
    with engine.connect() as connection:
        for table_name in CSV_FILES:
            count = connection.execute(
                text(f"SELECT COUNT(*) FROM {table_name}")
            ).scalar()

            if count > 0:
                print(
                    f"\nImport stopped: '{table_name}' "
                    "already contains records."
                )
                print("No CSV files were imported.")
                return

    # Import CSV files in dependency-friendly order
    for table_name in CSV_FILES:
        csv_path = DATASET_DIR / f"{table_name}.csv"

        if not csv_path.exists():
            print(f"\nFile not found: {csv_path}")
            return

        df = pd.read_csv(csv_path)

        df.to_sql(
            table_name,
            con=engine,
            if_exists="append",
            index=False
        )

        print(
            f"Imported {len(df)} records into "
            f"'{table_name}'"
        )

    print("\n========== CSV IMPORT COMPLETED ==========")


if __name__ == "__main__":
    import_csv_files()
