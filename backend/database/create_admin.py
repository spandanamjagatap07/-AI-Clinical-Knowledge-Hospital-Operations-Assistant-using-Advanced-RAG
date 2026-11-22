
from getpass import getpass

from backend.database.db_connection import SessionLocal
from backend.database.models import User
from backend.auth.security import hash_password


def create_admin():
    db = SessionLocal()

    try:
        existing_admin = db.query(User).filter(
            User.role == "admin"
        ).first()

        if existing_admin:
            print("An admin account already exists.")
            return

        username = input("Enter admin username: ").strip()
        email = input("Enter admin email: ").strip().lower()
        password = getpass("Enter admin password (minimum 8 characters): ")
        confirm_password = getpass("Confirm admin password: ")

        if len(username) < 3:
            print("Username must contain at least 3 characters.")
            return

        if len(password) < 8 or len(password) > 128:
            print("Password must contain 8 to 128 characters.")
            return

        if password != confirm_password:
            print("Passwords do not match.")
            return

        if not email or "@" not in email:
            print("Please enter a valid email address.")
            return

        if db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first():
            print("Username or email already exists.")
            return

        admin = User(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            role="admin",
            is_active=True
        )

        db.add(admin)
        db.commit()

        print("Admin account created successfully!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
