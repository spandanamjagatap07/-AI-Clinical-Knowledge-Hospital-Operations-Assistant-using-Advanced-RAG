
from backend.database.db_connection import engine
from backend.database.models import User

def create_auth_table():
    User.__table__.create(bind=engine, checkfirst=True)

    print("Authentication table created successfully!")
    print("Table name: users")

if __name__ == "__main__":
    create_auth_table()
