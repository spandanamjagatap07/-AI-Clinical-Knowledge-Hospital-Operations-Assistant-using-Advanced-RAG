
from backend.database.db_connection import engine
from backend.database.models import Base
def create_tables():

    print("\nCreating hospital database tables...")

    Base.metadata.create_all(bind=engine)

    print("\nAll database tables created successfully!")

    print("\n========== CREATED TABLES ==========")

    for table_name in Base.metadata.tables.keys():
        print("-", table_name)

    print("\nTotal tables:", len(Base.metadata.tables))


if __name__ == "__main__":
    create_tables()
