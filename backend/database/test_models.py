
from models import Base

print("\n========== SQLALCHEMY MODEL TEST ==========\n")

for table_name, table in Base.metadata.tables.items():
    print("Table:", table_name)
    print("Columns:", list(table.columns.keys()))
    print()

print("Total tables defined:", len(Base.metadata.tables))

print("\nModel test completed!")
