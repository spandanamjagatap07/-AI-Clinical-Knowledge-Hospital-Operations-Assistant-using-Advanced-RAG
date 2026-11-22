
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Find the main project directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Database location
DATABASE_DIR = BASE_DIR / "data" / "database"

# Create folder if it does not exist
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "hospital.db"

# SQLite database URL
DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"

# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def test_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        print("Database connection successful!")
        print("Database location:", DATABASE_PATH)

    except Exception as error:
        print("Database connection failed:", error)


if __name__ == "__main__":
    test_connection()
